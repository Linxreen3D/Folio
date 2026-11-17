# Backend einrichten (Supabase, kostenlos)

Ohne Backend läuft Foilio im **Vorschau-Modus**: Preise und Preisverlauf sind echt, Angebote und Verkäufer:innen sind Beispiele.
Mit Backend wird daraus ein echter Marktplatz mit Konten, Angeboten für alle, Bestellungen, Chat und Fotos.

Dauer: etwa 15 Minuten. Kosten: 0 € (Supabase Free: 50.000 aktive Nutzer pro Monat, 500 MB Datenbank, 1 GB Fotos).

## 1. Projekt anlegen
1. Auf https://supabase.com mit GitHub anmelden → **New project**.
2. Name `foilio`, ein sicheres Datenbank-Passwort (gut aufheben), **Region: Central EU (Frankfurt)** (wichtig für den Datenschutz).
3. Warten, bis das Projekt bereit ist (1–2 Minuten).

## 2. Datenbank einrichten
1. Links **SQL Editor** → **New query**.
2. Den kompletten Inhalt von [`supabase/schema.sql`](../supabase/schema.sql) einfügen → **Run**.
3. Es muss „Success“ erscheinen. Das Skript darf jederzeit erneut ausgeführt werden.

Das legt an: die Datentabelle mit Zugriffsregeln (jede Person schreibt nur ihre eigenen Daten, Nachrichten und Bestellungen sehen nur die Beteiligten), den anonymen Verkaufsfeed für Preise, die Liste verifizierter Verkäufer:innen und den Fotospeicher.

## 3. Anmeldung einstellen
**Authentication → URL Configuration**
- **Site URL:** die Adresse der Website, z. B. `https://linxreen3d.github.io/Folio/` (später die eigene Domain)
- **Redirect URLs:** dieselbe Adresse noch einmal eintragen (bei eigener Domain beide)

**Authentication → Sign In / Providers → Email:** aktiviert lassen, „Confirm email“ an.

**E-Mail-Versand (wichtig):** Der eingebaute Versand von Supabase schafft nur wenige Mails pro Stunde. Für den echten Betrieb unter
**Authentication → Emails → SMTP Settings** einen eigenen Versand eintragen, z. B. kostenlos über Brevo (300 Mails pro Tag):
Brevo-Konto anlegen → SMTP & API → SMTP-Zugangsdaten in Supabase eintragen. Absender: eine Adresse deiner Domain.

Optional unter **Authentication → Emails → Templates** den Text der Anmelde-Mail auf Deutsch ändern, z. B.:
`Hier ist dein Anmeldelink für Foilio: {{ .ConfirmationURL }}`

## 4. Website verbinden
1. In Supabase **Project Settings → API**: „Project URL“ und den Schlüssel **anon / public** kopieren.
   (Der anon-Schlüssel ist öffentlich gedacht. Geschützt wird alles durch die Regeln aus Schritt 2. Den **service_role**-Schlüssel niemals weitergeben.)
2. Auf GitHub im Repository: **Settings → Secrets and variables → Actions → Variables → New repository variable**
   - `SUPABASE_URL` = Project URL
   - `SUPABASE_ANON_KEY` = anon-Schlüssel
3. **Actions → „Tägliche Preise und neue Karten“ → Run workflow.** Nach dem Lauf ist der Marktplatz live.

## Betrieb
- **Verkäufer:innen verifizieren:** Table Editor → `verified_sellers` → Insert row → `uid` der Person (steht in `docs`, Spalte `owner`). Vorher die Verkäuferdaten prüfen:
  `select owner, data from docs where id = 'tax';`
- **Meldungen (DSA) ansehen:** SQL Editor → `select owner, jsonb_array_elements(data->'items') from docs where col = 'reports';`
  Jede Meldung zeitnah prüfen, der meldenden Person per E-Mail antworten (Entscheidung mit Begründung).
- **Angebot entfernen:** Table Editor → `docs` → Zeile mit `col = listings` und `id = <uid>` bearbeiten. Betroffene Person per E-Mail mit Begründung informieren.
- **Sicherung:** Der Free-Plan macht keine automatischen Backups zum Herunterladen. Einmal pro Woche unter Database → Backups bzw. per `pg_dump` sichern.

## Später: echte Bezahlung mit Käuferschutz
Solange `PAYMENTS` nicht gesetzt ist, bezahlen Käufer:innen direkt bei den Verkäufer:innen (PayPal „Waren und Dienstleistungen“ empfohlen) und Foilio nimmt kein Geld entgegen. Das ist rechtlich der einfachste Start.
Für Treuhand und Provision: Konto bei **Stripe Connect** oder **Mangopay** (beide ohne Fixkosten). Geld fremder Leute selbst zu halten ist in der EU ohne Zahlungsinstituts-Lizenz nicht erlaubt, deshalb immer über einen solchen Anbieter. Wenn es so weit ist, baue ich die Anbindung (Supabase Edge Function + Webhook) und dann wird `PAYMENTS=stripe` gesetzt.
