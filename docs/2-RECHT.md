# Rechtliches vor dem Start (Österreich / EU)

> Das ist eine Arbeitsliste, keine Rechtsberatung. Die Texte auf der Website sind Entwürfe und sollten vor dem Start einmal anwaltlich geprüft werden.
> Viele Punkte sind dank der Startphase ohne eigene Zahlungsabwicklung deutlich einfacher.

## Schon auf der Website umgesetzt
| Pflicht | Wo |
|---|---|
| Impressum (§ 5 ECG, § 25 MedienG) | Seite „Impressum“, Daten kommen aus `site/betreiber.json` |
| AGB für die Startphase (direkte Bezahlung, 0 % Provision, Sperren mit Begründung) | Seite „AGB“ |
| Datenschutzerklärung passend zu GitHub Pages + Supabase, ohne Tracking | Seite „Datenschutz“ |
| **DSA Art. 16** Meldeverfahren für rechtswidrige Inhalte, auch ohne Konto | „Angebot oder Inhalt melden“ auf jeder Kartenseite |
| Nachverfolgbarkeit gewerblicher Verkäufer:innen (DSA Art. 30; für Klein- und Kleinstunternehmen nach Art. 29 freiwillig, aber vertrauensbildend und für das Verbraucherrecht nützlich) | Verkäuferdaten „Gewerblich“, Angaben werden auf der Kartenseite angezeigt |
| **DAC7** Daten der Verkäufer:innen (Name, Anschrift, Geburtsdatum, Steuernummer, IBAN) | Konto → Verkäuferdaten, Hinweis ab 25 Verkäufen oder 1.500 € pro Jahr |
| Kennzeichnung Privat / Gewerblich bei jedem Angebot | Kartenseite |
| Altersgrenze 18 und Zustimmung zu AGB bei der Anmeldung | Anmeldeseite |
| Keine Cookies / kein Tracking → kein Cookie-Banner nötig | gesamte Seite |

## Das musst du selbst erledigen
1. **Gewerbe anmelden** – „Betrieb eines Online-Marktplatzes“ ist ein freies Gewerbe. Online über das Unternehmensserviceportal (usp.gv.at) oder bei der Bezirkshauptmannschaft / dem Magistrat. Kosten: 0 €. Damit bist du automatisch WKO-Mitglied (Grundumlage, im Gründungsjahr oft ermäßigt).
2. **`site/betreiber.json` ausfüllen** (auf GitHub die Datei öffnen → Stift-Symbol → speichern). Name, Rechtsform, Anschrift, E-Mail, Telefon, Gewerbebehörde, WKO-Fachgruppe; UID und Firmenbuch nur falls vorhanden. Danach verschwinden die Platzhalter auf Impressum, AGB und Datenschutz.
3. **E-Mail-Adresse** einrichten, die du regelmäßig liest (Kontaktstelle nach DSA Art. 11/12 und für Meldungen). Bei World4You ist eine E-Mail-Adresse zur Domain dabei.
4. **Auftragsverarbeitungsverträge**: Bei Supabase (Dashboard → Legal → DPA) und ggf. Brevo das DPA annehmen. GitHub: DPA ist in den Bedingungen enthalten.
5. **DAC7-Registrierung**: Plattformbetreiber müssen bis 31. Jänner des Folgejahres an das Finanzamt melden (über FinanzOnline). Frühzeitig beim Finanzamt bzw. Steuerberater klären, sobald die ersten Verkäufer:innen die Schwelle (30 Verkäufe oder 2.000 €) erreichen. Auch eine **Nullmeldung** kann nötig sein.
6. **Anwaltliche Prüfung** von AGB und Datenschutz – einmalig, grob 500–1.500 €. Günstiger: Musterpakete der WKO oder Gründungsberatung der WKO (für Mitglieder kostenlos).
7. **Marken**: Den Namen „Foilio“ vor größeren Ausgaben auf Kollisionen prüfen (markenrecherche über tmview.org). Anmeldung beim Österreichischen Patentamt ab ca. 300 €, optional.
8. **Steuern**: Solange keine Provision verlangt wird, hat Foilio keine Umsätze. Sobald Gebühren kommen: Kleinunternehmerregelung (bis 55.000 € Jahresumsatz) mit Steuerberatung prüfen.

## Später, wenn Geld über Foilio fließt
- Treuhand **nur über** Stripe Connect / Mangopay (Zahlungsinstituts-Lizenz liegt dort).
- Eine AGB-Version mit Treuhand und Provision liegt bereits als Entwurf im Code (`INFO.agb`). Sie wird erst aktiv, wenn die Zahlungsanbindung gebaut ist und die Variable `PAYMENTS` gesetzt wird – vorher `PAYMENTS` nicht setzen.
- Die Meldefunktion (DSA Art. 16) und Begründungen bei Sperren (Art. 17) gelten für alle. Interne Beschwerdeverfahren, Transparenzberichte und Art. 30 werden erst ab 50 Mitarbeitenden oder mehr als 10 Mio. € Umsatz Pflicht (Art. 19 und 29) – Foilio erfüllt sie trotzdem schon in einfacher Form.

## Bilder und Daten
- **Kartenbilder**: Scryfall (Magic) und TCGdex (Pokémon) erlauben die Einbindung mit Quellenangabe, steht in der Fußzeile. Yu-Gi-Oh!- und One-Piece-Bilder werden auf den Google-Kartenseiten nicht eingebunden. Bei Angeboten stehen die Fotos der Verkäufer:innen im Vordergrund.
- **Preise**: Quellen werden auf jeder Kartenseite genannt. Keine Werbung mit „offiziellen“ Preisen, keine Logos der Hersteller.
