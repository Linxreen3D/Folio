# Foilio

Sammelkarten-Marktplatz für Pokémon, Magic, Yu-Gi-Oh!, One Piece und Lorcana: über 79.000 Karten, echte Marktpreise mit täglichem Verlauf, Kamera-Scanner, Portfolio, Treuhand-Kauf und Tauschbörse.

## Wie es läuft

Jeden Morgen um 04:23 UTC startet der Workflow `.github/workflows/daily.yml` (kostenlos, ohne KI):

1. holt alle Karten, Sets und Preise (TCGdex, Scryfall, YGOPRODeck, Lorcast, offizielle One-Piece-Kartenliste),
2. erkennt neue Sets und Karten,
3. hängt den heutigen Preis an den echten Preisverlauf an und ergänzt Magic aus MTGJSON,
4. erzeugt die Kartenbilder,
5. sichert den Preisverlauf in `data/hist/` und veröffentlicht die Website über GitHub Pages.

## Ordner

| Ordner | Inhalt |
|---|---|
| `site/` | Website (eine Seite, `index.html`) und Bilder der Vitrinen-Karten |
| `tools/` | Import-Skripte (Python) |
| `data/hist/` | **Echter Preisverlauf, eine Spalte pro Tag. Nicht löschen – lässt sich nicht wiederherstellen.** |
| `.github/workflows/` | Täglicher Zeitplan |

Katalog, Preise und Bilder werden bei jedem Lauf neu erzeugt und nicht im Repository gespeichert.

## Einmalig einrichten

1. **Settings → Pages → Build and deployment → Source: „GitHub Actions“** auswählen.
2. **Actions → „Tägliche Preise und neue Karten“ → „Run workflow“** einmal starten (danach läuft er jeden Morgen von selbst).

Die Website ist danach unter `https://linxreen3d.github.io/folio/` erreichbar.

## Eigene Domain (z. B. bei World4You)

Im DNS bei World4You einen CNAME-Eintrag `www` → `linxreen3d.github.io` anlegen und unter Settings → Pages die Domain `www.deine-domain.at` eintragen, „Enforce HTTPS“ aktivieren.

## Lokal ausführen

```bash
pip install pillow ijson
python tools/pkm_fetch.py raw --refresh-prices
python tools/others_fetch.py raw mtg ygo lor op
python tools/build_catalog.py raw _site/data
```

## Hinweise

- Preise stammen aus Cardmarket (über TCGdex, Scryfall, YGOPRODeck), TCGplayer (Lorcast, aus USD umgerechnet) und MTGJSON. Für One Piece gibt es noch keine offene Preisquelle; dort steht eine gekennzeichnete Schätzung. Vor einem kommerziellen Start die Nutzungsbedingungen der Quellen klären.
- Auf GitHub Pages speichert die Seite Konten, Angebote und Chat nur im Browser. Für echten Mehrbenutzer-Betrieb kommt eine Datenbank dazu (z. B. Firebase).
- Impressum, AGB und Datenschutz in der Seite sind Vorlagen mit Platzhaltern und müssen vor dem Start befüllt und geprüft werden.
- Pokémon, Magic: The Gathering, Yu-Gi-Oh!, One Piece Card Game und Disney Lorcana sind Marken ihrer jeweiligen Inhaber. Foilio ist mit ihnen nicht verbunden.
