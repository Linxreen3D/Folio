# Startplan: die ersten 100 Verkäufer:innen und 1.000 Besucher:innen

Ein Marktplatz scheitert fast nie an der Technik, sondern daran, dass am Anfang keine Angebote da sind.
Deshalb: **erst Verkäufer:innen, dann Käufer:innen**, und mit einem klaren Fokus starten.

## Fokus
- **Pokémon, Österreich + Deutschland.** Größte Nachfrage, deutschsprachig, Versand innerhalb der EU einfach.
- Andere Spiele bleiben sichtbar (Preise, Google-Seiten), aber Werbung und Ansprache gehen erst an Pokémon-Sammler:innen.

## Was Foilio Verkäufer:innen bietet (für jede Ansprache)
1. **0 % Provision** in der Startphase (Cardmarket nimmt Provision auf jeden Verkauf).
2. **Bestand in 2 Minuten umziehen:** Cardmarket → Stock → Export als CSV → bei Foilio unter Verkäufe „CSV importieren“. Foilio erkennt das Cardmarket-Format automatisch.
3. **Scanner:** Karte vors Handy halten, Preis aus echten Verkäufen, einstellen.
4. **Portfolio mit echtem Preisverlauf** für die eigene Sammlung.

## Woche 1–2: Fundament
- [ ] Backend live (docs/1-BACKEND.md), `betreiber.json` ausgefüllt, Gewerbe angemeldet (docs/2-RECHT.md)
- [ ] Google Search Console: Domain hinzufügen → Sitemap `sitemap.xml` einreichen. Die 80.000 Kartenseiten werden dann nach und nach indexiert (dauert Wochen, kostet nichts).
- [ ] Bing Webmaster Tools: Sitemap ebenfalls einreichen (speist auch ChatGPT-Suche und Copilot)
- [ ] Eigene Domain verbinden (World4You → CNAME) und als Repository-Variable `SITE_URL` setzen, damit Sitemap und Kartenseiten die richtige Adresse tragen
- [ ] 20 eigene Karten einstellen, damit der Marktplatz nicht leer wirkt

## Woche 2–4: Verkäufer:innen gewinnen
**Kartenläden (Österreich zuerst):** Liste aller Pokémon-Händler in Wien, Graz, Linz, Salzburg, Innsbruck (Google Maps „Pokémon Karten“ + Cardmarket-Händlerliste Österreich). Persönlich vorbeigehen oder anrufen, nicht nur mailen.

> **Vorlage E-Mail / DM an Kartenläden**
> Hallo [Name],
> ich habe Foilio gestartet, einen neuen Sammelkarten-Marktplatz aus Österreich. In der Startphase verlangen wir **keine Provision**. Euren Cardmarket-Bestand könnt ihr per CSV in 2 Minuten übernehmen und parallel weiter auf Cardmarket verkaufen.
> Dazu gibt es einen Kartenscanner und für jede Karte eine Seite mit echtem Preisverlauf, die bei Google gefunden wird.
> Darf ich euch das in 10 Minuten zeigen, gern auch im Laden?
> Liebe Grüße, [Name] – [Link]

**Private Power-Seller:** Auf Cardmarket Verkäufer:innen aus AT/DE mit 100–2.000 Verkäufen (keine Großhändler) über ihre öffentlichen Kontaktwege ansprechen, ebenso in Facebook-Gruppen und Discords. Angebot: 0 % Provision für immer für die ersten 50 Verkäufer:innen („Gründungsmitglied“). Verifizierung bevorzugt durchführen.

**Discord:** eigenen Foilio-Server anlegen mit Kanälen #neue-angebote, #preis-fragen, #feedback, #tausch. In bestehenden Pokémon-Discords nur dort posten, wo Eigenwerbung erlaubt ist.

## Laufend: Käufer:innen gewinnen (ohne Werbebudget)
**Kurzvideos (TikTok, Instagram Reels, YouTube Shorts), 2–3 pro Woche.** Formate, die funktionieren:
1. *„Was ist diese Karte wert?“* – Karte scannen, Preis und Verlauf zeigen, Überraschung bei teuren Karten.
2. *„Pack-Opening mit Live-Wert“* – jede gezogene Karte sofort scannen, am Ende Gesamtwert vs. Packpreis.
3. *„Top 5 Karten, die gerade steigen“* – aus der Foilio-Startseite („Gewinner“), echte Daten, wöchentlich.
4. *„So verkaufst du deine alten Karten ohne Provision“* – Scan → Einstellen in 30 Sekunden.

Immer: Link in Bio, Hashtags #pokemonkarten #pokemontcg #tcgösterreich #pokemondeutsch.

**Turniere und Events:** Bei lokalen Pokémon-Turnieren und Börsen Flyer mit QR-Code („Scan deine Karte, sieh den Wert“). Kostet nur den Druck.

**Reddit / Foren:** r/PokemonTCG, r/pkmntcgcollections, deutschsprachige Foren – nur mit echtem Mehrwert (z. B. wöchentliche Preisanalyse mit Daten), nicht als Werbung.

## Messen, ob es funktioniert
| Kennzahl | Ziel nach 3 Monaten |
|---|---|
| Aktive Angebote | 2.000 |
| Verkäufer:innen mit ≥ 1 Angebot | 100 |
| Bestellungen pro Woche | 25 |
| Kartenseiten bei Google indexiert (Search Console) | 20.000 |
| Klicks von Google pro Woche | 1.000 |

Search Console ist kostenlos und braucht kein Tracking auf der Seite. Für Besucherzahlen ohne Cookie-Banner: GoatCounter (kostenlos für kleine Seiten) – das kann ich einbauen, sobald du ein Konto angelegt hast.

## Wann Gebühren einführen?
Erst wenn Käufer:innen regelmäßig wiederkommen (z. B. 100 Bestellungen pro Woche) **und** die Treuhand-Zahlung über Stripe Connect / Mangopay läuft. Dann z. B. 3 % Provision, also klar unter Cardmarket, mit 30 Tagen Ankündigung. Gründungsmitglieder behalten 0 %.
