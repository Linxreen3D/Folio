-- Foilio backend on Supabase (free tier).
-- Run once in the Supabase dashboard: SQL Editor -> New query -> paste this file -> Run.
-- Safe to run again: everything is created "if not exists" or replaced.
--
-- Data model: one JSON document per (collection, id), the same shape the site already uses.
--   listings/<uid>, orders/<uid>, msgs/<uid>, bids/<uid>, trade/<uid>, profiles/<uid>, reports/<uid>
--   data/users/<uid>/<name>   private documents (portfolio, alerts, wants, wallet, tax)
-- Everyone writes only documents that belong to them; row level security enforces it.

create table if not exists public.docs (
  col        text        not null,
  id         text        not null,
  owner      uuid        not null default auth.uid() references auth.users(id) on delete cascade,
  data       jsonb       not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (col, id),
  constraint docs_size check (octet_length(data::text) < 1500000)
);
create index if not exists docs_owner on public.docs (owner);

alter table public.docs enable row level security;
grant select on public.docs to anon;
grant select, insert, update, delete on public.docs to authenticated;

-- Who may write a document: its owner, and only at an address that belongs to them.
create or replace function public.foilio_own_address(c text, i text) returns boolean
language sql stable as $$
  select auth.uid() is not null and (
    (c in ('listings','orders','msgs','bids','trade','profiles','reports') and i = auth.uid()::text)
    or c = 'data/users/' || auth.uid()::text
  )
$$;

drop policy if exists docs_read_public  on public.docs;
drop policy if exists docs_read_private on public.docs;
drop policy if exists docs_read_msgs    on public.docs;
drop policy if exists docs_read_orders  on public.docs;
drop policy if exists docs_insert       on public.docs;
drop policy if exists docs_update       on public.docs;
drop policy if exists docs_delete       on public.docs;

-- public: offers, collector profiles, trade lists, price proposals
create policy docs_read_public on public.docs for select
  using (col in ('listings','profiles','trade','bids'));
-- private documents and own reports: only the owner
create policy docs_read_private on public.docs for select
  using (owner = auth.uid() and (col like 'data/users/%' or col = 'reports'));
-- messages: sender, and anyone a message in the document is addressed to
create policy docs_read_msgs on public.docs for select
  using (col = 'msgs' and (owner = auth.uid() or exists (
    select 1 from jsonb_array_elements(coalesce(data->'items','[]'::jsonb)) m where m->>'to' = auth.uid()::text)));
-- orders: buyer, and sellers of items in the order
create policy docs_read_orders on public.docs for select
  using (col = 'orders' and (owner = auth.uid() or exists (
    select 1 from jsonb_array_elements(coalesce(data->'items','[]'::jsonb)) o where o->>'seller' = auth.uid()::text)));

create policy docs_insert on public.docs for insert
  with check (owner = auth.uid() and public.foilio_own_address(col, id));
create policy docs_update on public.docs for update
  using (owner = auth.uid()) with check (owner = auth.uid() and public.foilio_own_address(col, id));
create policy docs_delete on public.docs for delete
  using (owner = auth.uid());

-- Anonymous sales feed: which offers are sold and at what price, without who bought them.
-- Needed for the "sold" state of offers and for Foilio's own price (median of real sales).
create or replace function public.public_sales() returns table (id text, data jsonb)
language sql stable security definer set search_path = public as $$
  select md5(d.id), jsonb_build_object('items', coalesce(jsonb_agg(jsonb_build_object(
           'oid', o->>'oid', 'lid', o->>'lid', 'cardId', o->>'cardId', 'price', (o->>'price')::numeric,
           'cond', o->>'cond', 'graded', o->'graded', 'seller', o->>'seller', 'at', (o->>'at')::bigint,
           'receivedAt', o->'receivedAt', 'refund', o->'refund')) filter (where o is not null), '[]'::jsonb))
  from public.docs d left join lateral jsonb_array_elements(coalesce(d.data->'items','[]'::jsonb)) o on true
  where d.col = 'orders' and coalesce((o->>'demo')::boolean, false) = false
    -- documents the caller can already read in full are not repeated here
    and d.owner is distinct from auth.uid()
    and not exists (select 1 from jsonb_array_elements(coalesce(d.data->'items','[]'::jsonb)) x where x->>'seller' = auth.uid()::text)
  group by d.id
$$;
grant execute on function public.public_sales() to anon, authenticated;

-- Verified badge: only the operator sets it (Table Editor -> verified_sellers -> Insert row).
-- Whatever a user writes into their own profile under "verified" is replaced by this table.
create table if not exists public.verified_sellers (
  uid uuid primary key references auth.users(id) on delete cascade,
  verified_at timestamptz not null default now(),
  note text
);
alter table public.verified_sellers enable row level security;
drop policy if exists verified_read on public.verified_sellers;
create policy verified_read on public.verified_sellers for select using (true);
grant select on public.verified_sellers to anon, authenticated;

create or replace function public.foilio_profile_guard() returns trigger
language plpgsql security definer set search_path = public as $$
declare v timestamptz;
begin
  new.updated_at := now();
  if new.col = 'profiles' then
    select verified_at into v from public.verified_sellers where uid = new.owner;
    new.data := (new.data - 'verified') || case when v is null then '{}'::jsonb
                 else jsonb_build_object('verified', jsonb_build_object('at', (extract(epoch from v) * 1000)::bigint, 'by', 'Foilio')) end;
  end if;
  return new;
end $$;
drop trigger if exists docs_guard on public.docs;
create trigger docs_guard before insert or update on public.docs
  for each row execute function public.foilio_profile_guard();

-- Live updates in the browser
do $$ begin
  alter publication supabase_realtime add table public.docs;
exception when duplicate_object then null; end $$;

-- Photos of offered cards: public to view, each user uploads only into their own folder.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('photos', 'photos', true, 5242880, array['image/jpeg','image/png','image/webp'])
on conflict (id) do update set public = true, file_size_limit = 5242880, allowed_mime_types = array['image/jpeg','image/png','image/webp'];

drop policy if exists photos_read   on storage.objects;
drop policy if exists photos_upload on storage.objects;
drop policy if exists photos_delete on storage.objects;
create policy photos_read on storage.objects for select using (bucket_id = 'photos');
create policy photos_upload on storage.objects for insert to authenticated
  with check (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);
create policy photos_delete on storage.objects for delete to authenticated
  using (bucket_id = 'photos' and (storage.foldername(name))[1] = auth.uid()::text);

-- Operator view of reports (DSA notice and action): Table Editor -> docs, filter col = reports,
-- or run:  select owner, jsonb_array_elements(data->'items') from docs where col = 'reports';
