# Foilio

Sammelkarten-Marktplatz für Pokémon, Magic, Yu-Gi-Oh!, One Piece und Lorcana: über 79.000 Karten, echte Marktpreise mit täglichem Verlauf, Kamera-Scanner, Portfolio, Tauschbörse – und für jede Karte eine eigene Seite, die Google und KI-Suchen finden.

## Startklar machen – Reihenfolge

| Schritt | Anleitung | Dauer |
|---|---|---|
| 1. Website veröffentlichen | unten „Einmalig einrichten“ | 2 Min. |
| 2. Echter Marktplatz mit Konten (Supabase, kostenlos) | [docs/1-BACKEND.md](docs/1-BACKEND.md) | 15 Min. |
| 3. Rechtliches (Gewerbe, Impressum-Daten, Prüfung) | [docs/2-RECHT.md](docs/2-RECHT.md) | einige Tage |
| 4. Verkäufer:innen und Besucher:innen gewinnen | [docs/3-START.md](docs/3-START.md) | laufend |

## Einmalig einrichten

1. **Settings → Pages → Build and deployment → Source: „GitHub Actions“** auswählen.
2. **Actions → „Tägliche Preise und neue Karten“ → „Run workflow“** einmal starten (danach läuft er jeden Morgen von selbst).

Die Website ist danach unter `https://linxreen3d.github.io/Folio/` erreichbar.
Ohne Backend läuft sie im **Vorschau-Modus** (echte Preise, Beispiel-Angebote, deutlich gekennzeichnet).

## Wie es läuft

Jeden Morgen um 04:23 UTC startet `.github/workflows/daily.yml` (kostenlos, ohne KI):

1. holt alle Karten, Sets und Preise (TCGdex, Scryfall, YGOPRODeck, Lorcast, offizielle One-Piece-Kartenliste); fällt eine Quelle aus, wird ihr letzter Stand verwendet,
2. erkennt neue Sets und Karten,
3. hängt den heutigen Preis an den echten Preisverlauf an und ergänzt Magic aus MTGJSON,
4. erzeugt Kartenbilder, **eine Seite pro Karte, Set und Spiel** (`/karte/…`, `/set/…`, `/spiel/…`), Sitemap und robots.txt,
5. sichert den Preisverlauf in `data/hist/` und veröffentlicht die Website über GitHub Pages.

## Einstellungen (Settings → Secrets and variables → Actions → Variables)

| Variable | Wofür |
|---|---|
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | schaltet den echten Marktplatz ein (siehe docs/1-BACKEND.md) |
| `SITE_URL` | nur bei eigener Domain, z. B. `https://www.foilio.at` (für Sitemap und Google-Seiten) |
| `PAYMENTS` | erst setzen, wenn eine Zahlungsanbindung (Stripe Connect / Mangopay) gebaut ist |

Betreiberdaten für Impressum, AGB und Datenschutz stehen in [`site/betreiber.json`](site/betreiber.json) – direkt auf GitHub bearbeiten.

## Ordner

| Ordner | Inhalt |
|---|---|
| `site/` | Website (`index.html`), Backend-Anbindung (`backend.js`), Betreiberdaten, Bilder |
| `supabase/` | Datenbank-Schema mit Zugriffsregeln |
| `tools/` | Import-Skripte und Seiten-Generator (Python) |
| `data/hist/` | **Echter Preisverlauf, eine Spalte pro Tag. Nicht löschen – lässt sich nicht wiederherstellen.** |
| `docs/` | Anleitungen für Backend, Recht und Start |

## Eigene Domain (z. B. bei World4You)

Im DNS bei World4You einen CNAME-Eintrag `www` → `linxreen3d.github.io` anlegen, unter Settings → Pages die Domain `www.deine-domain.at` eintragen und „Enforce HTTPS“ aktivieren. Dann die Variable `SITE_URL` setzen und in Supabase die Site URL anpassen.

## Lokal ausführen

```bash
pip install pillow ijson
python tools/pkm_fetch.py raw --refresh-prices
python tools/others_fetch.py raw mtg ygo lor op
python tools/build_catalog.py raw _site/data
python tools/static_pages.py raw _site http://localhost:8000
```

## Hinweise

- Preise stammen aus Cardmarket (über TCGdex, Scryfall, YGOPRODeck), TCGplayer (Lorcast, aus USD umgerechnet) und MTGJSON. Für One Piece gibt es noch keine offene Preisquelle; dort steht eine gekennzeichnete Schätzung, bis eigene Verkäufe vorliegen.
- Pokémon, Magic: The Gathering, Yu-Gi-Oh!, One Piece Card Game und Disney Lorcana sind Marken ihrer jeweiligen Inhaber. Foilio ist mit ihnen nicht verbunden.
