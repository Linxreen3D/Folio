/* Foilio backend adapter.
   The site talks to a small capability interface (window.claude.use("db" | "user" | "assets" | "downloads")).
   Inside claude.ai that interface exists already. On the public website this file provides it,
   backed by Supabase (accounts, database, photo storage) when config.js names a project.
   Without a project the site runs in preview mode: everything stays on this device. */
(function(){
  if (window.claude && window.claude.use) return; // running inside claude.ai: keep the native runtime
  const cfg = window.FOLIO_CONFIG || {};
  const LIVE = !!(cfg.supabaseUrl && cfg.supabaseKey && window.supabase && window.supabase.createClient);
  let sb = null, ready = Promise.resolve(null);
  if (LIVE) {
    sb = window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseKey, {
      auth: { flowType: "pkce", persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
    });
    ready = sb.auth.getSession().then(r => r.data && r.data.session || null).catch(() => null);
  }
  const split = path => { const i = path.lastIndexOf("/"); return [path.slice(0, i), path.slice(i + 1)]; };
  const snapDoc = (id, data) => ({ id, exists: data != null, data: () => data == null ? undefined : JSON.parse(JSON.stringify(data)) });
  let chan = 0;
  function live(filterCol, onChange) {
    const ch = sb.channel("foilio-" + (++chan)).on("postgres_changes",
      { event: "*", schema: "public", table: "docs", filter: "col=eq." + filterCol }, onChange).subscribe();
    return () => { try { sb.removeChannel(ch); } catch (e) {} };
  }
  function debounce(fn, ms) { let t; return () => { clearTimeout(t); t = setTimeout(fn, ms); }; }

  const db = LIVE && {
    collection(col) {
      return {
        onSnapshot(cb, err) {
          let stop = false;
          const load = async () => {
            try {
              const { data, error } = await sb.from("docs").select("id,data").eq("col", col).limit(5000);
              if (error) throw error;
              let rows = data || [];
              if (col === "orders") { // others' sales, anonymised (who bought stays private)
                const pub = await sb.rpc("public_sales");
                if (!pub.error && pub.data) rows = rows.concat(pub.data.map(r => ({ id: "sale-" + r.id, data: r.data })));
              }
              if (!stop) cb({ docs: rows.map(r => snapDoc(r.id, r.data)) });
            } catch (e) { if (!stop && err) err(e); }
          };
          load();
          const unlive = live(col, debounce(load, 400));
          const poll = col === "orders" ? setInterval(load, 300000) : null;
          return () => { stop = true; unlive(); if (poll) clearInterval(poll); };
        }
      };
    },
    doc(path) {
      const [col, id] = split(path);
      return {
        async set(data) {
          const s = await ready; if (!s) throw new Error("Nicht angemeldet");
          if (col === "profiles") data = { ...data, name: (s.user.user_metadata && s.user.user_metadata.name) || data.name || "" };
          const { error } = await sb.from("docs").upsert({ col, id, data, owner: s.user.id }, { onConflict: "col,id" });
          if (error) throw error;
        },
        onSnapshot(cb, err) {
          let stop = false;
          const load = async () => {
            try {
              const { data, error } = await sb.from("docs").select("data").eq("col", col).eq("id", id).maybeSingle();
              if (error) throw error;
              if (!stop) cb(snapDoc(id, data ? data.data : null));
            } catch (e) { if (!stop && err) err(e); }
          };
          load();
          const unlive = live(col, debounce(load, 400));
          return () => { stop = true; unlive(); };
        }
      };
    }
  };

  const user = LIVE && {
    async id() { const s = await ready; return s ? s.user.id : null; },
    async me() { const s = await ready; return s ? { name: (s.user.user_metadata && s.user.user_metadata.name) || "" } : null; },
    async profiles(ids) {
      const out = {}; if (!ids || !ids.length) return out;
      const { data } = await sb.from("docs").select("id,data").eq("col", "profiles").in("id", ids.slice(0, 200));
      (data || []).forEach(r => out[r.id] = { name: (r.data && r.data.name) || "Sammler:in" });
      return out;
    }
  };

  const assets = LIVE && {
    async upload(blob) {
      const s = await ready; if (!s) throw new Error("Bitte zuerst anmelden");
      const ext = (blob.type || "image/jpeg").split("/")[1].replace("jpeg", "jpg");
      const path = s.user.id + "/" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8) + "." + ext;
      const { error } = await sb.storage.from("photos").upload(path, blob, { contentType: blob.type || "image/jpeg", upsert: false });
      if (error) throw error;
      return { id: path, url: sb.storage.from("photos").getPublicUrl(path).data.publicUrl };
    }
  };

  // Works everywhere: hands a file to the browser's download.
  const downloads = {
    async save({ filename, data }) {
      const blob = data instanceof Blob ? data : new Blob([data], { type: /\.json$/.test(filename) ? "application/json" : /\.csv$/.test(filename) ? "text/csv" : "text/plain" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = filename;
      document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
    }
  };

  window.claude = { use: async name => ({ db, user, assets, downloads, sample: null })[name] || null };

  window.FolioBackend = {
    live: LIVE,
    payments: cfg.payments || "off",
    ready,
    async signIn(email, name) {
      const back = location.origin + location.pathname;
      const { error } = await sb.auth.signInWithOtp({ email, options: { emailRedirectTo: back, data: name ? { name } : undefined } });
      if (error) throw error;
    },
    async setName(name) { const { error } = await sb.auth.updateUser({ data: { name } }); if (error) throw error; },
    async signOut() { await sb.auth.signOut(); location.hash = "#markt"; location.reload(); },
    async email() { const s = await ready; return s ? s.user.email : ""; },
    // reload once after the sign-in link has been opened in another tab of this browser
    watch() { if (!sb) return; ready.then(s0 => sb.auth.onAuthStateChange((ev, s) => { if (ev === "SIGNED_IN" && !s0 && s) location.reload(); })); }
  };
  if (LIVE) window.FolioBackend.watch();
})();
