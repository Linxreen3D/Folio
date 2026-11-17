"""Static, crawlable pages for every card, set and game, plus sitemaps and robots.txt.

The app itself routes with #hash addresses, which search engines treat as one page.
These pages give each card a real address (/karte/<slug>/) with its facts, real prices,
real price history and a link into the app. Rebuilt daily by the workflow.

usage: python3 -I static_pages.py RAW_DIR SITE_DIR SITE_URL
"""
import json, os, re, sys, html, datetime

RAW, SITE, BASE = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")
DATA = os.path.join(SITE, "data")
TODAY = datetime.date.today().isoformat()
GAMES = {  # key: (name, url slug, price source)
    "pkm": ("Pokémon", "pokemon", "Cardmarket (über TCGdex)"),
    "mtg": ("Magic: The Gathering", "magic", "Cardmarket (über Scryfall und MTGJSON)"),
    "ygo": ("Yu-Gi-Oh!", "yugioh", "Cardmarket (über YGOPRODeck)"),
    "lor": ("Disney Lorcana", "lorcana", "TCGplayer (über Lorcast, in Euro umgerechnet)"),
    "op": ("One Piece Card Game", "one-piece", "keine freie Preisquelle, Schätzung nach Seltenheit"),
}
# image hosts that allow hotlinking; YGOPRODeck and the One Piece site ask not to
HOTLINK_OK = {"pkm", "mtg", "lor"}
esc = lambda s: html.escape(str(s or ""), quote=True)
slug = lambda s: re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(s).lower()
                 .replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
                 .replace("é", "e").replace("è", "e").replace("á", "a").replace("ō", "o"))).strip("-")
eur = lambda v: ("%.2f" % v).replace(".", ",") + " €"
appslug = lambda s: re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

def load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d

imgs = load(os.path.join(RAW, "img_map.json"), {})
urls = []  # (path, lastmod, priority)

CSS = """:root{--bg:#f6f7fb;--fg:#12131a;--mut:#5b6072;--card:#fff;--line:#e3e6ee;--acc:#5b5bf6;--pos:#0e9f6e;--neg:#d23f3f}
@media (prefers-color-scheme:dark){:root{--bg:#0d0e14;--fg:#eef0f6;--mut:#9aa0b4;--card:#171923;--line:#262a38;--acc:#8b8bff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--acc)}header,main,footer{max-width:980px;margin:0 auto;padding:16px}
header{display:flex;align-items:center;gap:12px;justify-content:space-between}
.logo{font-weight:800;font-size:20px;text-decoration:none;color:var(--fg);letter-spacing:-.02em}
.crumb{font-size:14px;color:var(--mut)}.crumb a{color:var(--mut)}
h1{font-size:clamp(24px,4vw,34px);line-height:1.15;margin:8px 0 4px;letter-spacing:-.02em}
.sub{color:var(--mut);margin:0 0 18px}
.wrap{display:grid;gap:20px;grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.wrap{grid-template-columns:300px minmax(0,1fr)}}
.pic{width:100%;max-width:300px;aspect-ratio:5/7;border-radius:14px;background:var(--card);border:1px solid var(--line);object-fit:cover}
.box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:16px}
.price{font-size:34px;font-weight:800;letter-spacing:-.02em}.est{font-size:13px;color:var(--mut)}
dl{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0}dt{color:var(--mut)}dd{margin:0;font-weight:600}
.btn{display:inline-block;background:var(--acc);color:#fff;padding:12px 18px;border-radius:12px;text-decoration:none;font-weight:700}
svg.spark{width:100%;height:90px}table{width:100%;border-collapse:collapse;font-size:15px}
td,th{padding:8px 6px;border-bottom:1px solid var(--line);text-align:left}td.r,th.r{text-align:right}
ul.cols{columns:2 240px;padding-left:18px}footer{color:var(--mut);font-size:13px}"""

def page(path, title, desc, body, crumbs, ld, image=None, prio="0.5"):
    canon = f"{BASE}/{path}/"
    root = "../" * (path.count("/") + 1) if path else ""
    cr = " › ".join(f'<a href="{root}{p}">{esc(n)}</a>' if p is not None else esc(n) for n, p in crumbs)
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")}</script>' for x in ld)
    og = f'<meta property="og:image" content="{esc(image)}">' if image else ""
    doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{esc(canon)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(canon)}"><meta property="og:type" content="website">{og}
<link rel="stylesheet" href="{root}k.css">{lds}</head><body>
<header><a class="logo" href="{root}">Foilio</a><a href="{root}#markt">Zum Marktplatz</a></header>
<main><nav class="crumb">{cr}</nav>{body}</main>
<footer><p>Preise sind Marktdaten der genannten Quelle, Stand {TODAY}. Foilio ist ein unabhängiger Marktplatz und steht in keiner Verbindung zu den Herstellern der Spiele.
<a href="{root}#impressum">Impressum</a> · <a href="{root}#datenschutz">Datenschutz</a> · <a href="{root}spiel/">Alle Spiele</a></p></footer></body></html>"""
    out = os.path.join(SITE, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    urls.append((path, TODAY, prio))

def spark(vals):
    pts = [(i, v) for i, v in enumerate(vals) if v]
    if len(pts) < 2: return ""
    lo, hi = min(v for _, v in pts), max(v for _, v in pts)
    n = len(vals) - 1 or 1; rng = (hi - lo) or 1
    d = " ".join(f"{'M' if k == 0 else 'L'}{i / n * 300:.1f},{80 - (v - lo) / rng * 70:.1f}" for k, (i, v) in enumerate(pts))
    return f'<svg class="spark" viewBox="0 0 300 90" preserveAspectRatio="none" role="img" aria-label="Preisverlauf"><path d="{d}" fill="none" stroke="var(--acc)" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>'

game_index = []
for g, (gname, gslug, src) in GAMES.items():
    cat = load(os.path.join(DATA, g + ".json"))
    if not cat: print("skip", g, "(no catalog)"); continue
    hist = load(os.path.join(DATA, "hist", g + ".json"), {"days": [], "p": {}})
    days, hp = hist.get("days", []), hist.get("p", {})
    sets = cat["sets"]; rar = cat["rar"]
    by_set = {}
    for r in cat["cards"]: by_set.setdefault(r[3], []).append(r)
    set_paths = {}
    for si, s in enumerate(sets):
        if si in by_set: set_paths[si] = f"set/{gslug}/{slug(s[0] if g == 'mtg' else s[1])}-{slug(s[2]) or si}"
    n_cards = 0
    for si, rows in by_set.items():
        s = sets[si]; sname, scode, sdate = s[1], s[2], s[3]
        spath = set_paths[si]
        card_links = []
        for r in rows:
            cid, name, alias, no, rr, price, est, a30, a7, a1, low, usd = r[0], r[1], r[2], r[4], rar[r[5]], r[6], r[7], r[8], r[9], r[10], r[11], r[12]
            path = f"karte/{slug(name)[:60]}-{cid}"
            card_links.append((path, name, no, price, est))
            series = hp.get(cid) or []
            vals = series[-90:]
            real = [v for v in vals if v]
            chg = ""
            if len(real) >= 2 and real[0]:
                pc = (real[-1] - real[0]) / real[0] * 100
                chg = f'<p>Veränderung seit {esc(days[-len(vals)])}: <b style="color:var({"--pos" if pc >= 0 else "--neg"})">{pc:+.1f} %</b></p>'
            img = imgs.get(cid) if g in HOTLINK_OK else None
            title = f"{name} – {sname} {no} | Preis & Wert | Foilio"
            pstr = eur(price)
            desc = (f"{name} aus {sname} ({scode} {no}, {rr}): aktueller Marktpreis {pstr}" + (" (Schätzung)" if est else "") +
                    f", Preisverlauf und Angebote auf Foilio.")
            rows_html = "".join(f"<tr><td>{k}</td><td class=r>{eur(v)}</td></tr>" for k, v in
                                (("Trend", price if not est else 0), ("Ø 30 Tage", a30), ("Ø 7 Tage", a7), ("Ø 1 Tag", a1), ("Niedrigster Preis", low)) if v)
            faq = [(f"Was ist {name} ({sname}) wert?",
                    f"Der aktuelle Marktpreis liegt bei {pstr}" + (" (Schätzung nach Seltenheit, weil keine Marktdaten vorliegen)." if est else f" laut {src}, Stand {TODAY}.")),
                   (f"Aus welchem Set stammt {name}?", f"{name} ist die Karte {no} aus {sname}" + (f" ({scode}), erschienen am {sdate}." if sdate else f" ({scode})."))]
            body = f"""<h1>{esc(name)}</h1><p class="sub">{esc(gname)} · {esc(sname)} · {esc(scode)} {esc(no)}{" · " + esc(alias) if alias else ""}</p>
<div class="wrap"><div>{f'<img class="pic" src="{esc(img)}" alt="{esc(name)} ({esc(sname)})" loading="lazy" width="300" height="420">' if img else ""}</div><div>
<div class="box"><div class="price">{pstr}</div><div class="est">{"Schätzung nach Seltenheit, keine Marktdaten" if est else "Marktpreis laut " + esc(src) + ", Stand " + TODAY}</div>
{f"<table>{rows_html}</table>" if rows_html and not est else ""}{spark(vals) if len(real) >= 2 else ""}{chg}
<p style="margin-top:14px"><a class="btn" href="{"../../#karte-" + esc(cid)}">Angebote ansehen und verkaufen</a></p></div>
<div class="box"><dl><dt>Spiel</dt><dd>{esc(gname)}</dd><dt>Set</dt><dd><a href="../../{spath}/">{esc(sname)}</a></dd><dt>Nummer</dt><dd>{esc(no)}</dd><dt>Seltenheit</dt><dd>{esc(rr) or "–"}</dd>{f"<dt>Erschienen</dt><dd>{esc(sdate)}</dd>" if sdate else ""}</dl></div>
<div class="box"><h2 style="margin-top:0;font-size:19px">Häufige Fragen</h2>{"".join(f"<h3 style='font-size:16px;margin:10px 0 2px'>{esc(q)}</h3><p style='margin:0'>{esc(a)}</p>" for q, a in faq)}</div>
</div></div>"""
            ld = [{"@context": "https://schema.org", "@type": "Product", "name": name, "category": f"Sammelkarte · {gname}",
                   "sku": cid, "mpn": f"{scode} {no}", "brand": {"@type": "Brand", "name": gname},
                   **({"image": img} if img else {}), "description": desc, "url": f"{BASE}/{path}/"},
                  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
                  {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": gname, "item": f"{BASE}/spiel/{gslug}/"},
                      {"@type": "ListItem", "position": 2, "name": sname, "item": f"{BASE}/{spath}/"},
                      {"@type": "ListItem", "position": 3, "name": name, "item": f"{BASE}/{path}/"}]}]
            page(path, title, desc, body, [("Foilio", ""), (gname, f"spiel/{gslug}/"), (sname, spath + "/"), (name, None)], ld, img,
                 "0.6" if not est else "0.4")
            n_cards += 1
        top = sorted(card_links, key=lambda x: -x[3])
        priced = [x for x in card_links if not x[4]]
        body = f"""<h1>{esc(sname)}</h1><p class="sub">{esc(gname)} · {esc(scode)}{" · erschienen " + esc(sdate) if sdate else ""} · {len(rows)} Karten</p>
<div class="box"><p style="margin-top:0">{len(priced)} von {len(rows)} Karten mit Marktpreis. Wertvollste Karte: <b>{esc(top[0][1])}</b> ({eur(top[0][3])}).</p>
<a class="btn" href="../../../#set-{esc(g[0] + "-" + appslug(s[0]))}">Set im Marktplatz öffnen</a></div>
<div class="box"><table><tr><th>Nr.</th><th>Karte</th><th class=r>Preis</th></tr>{"".join(f'<tr><td>{esc(no)}</td><td><a href="../../../{p}/">{esc(n)}</a></td><td class=r>{eur(pr)}{"*" if e else ""}</td></tr>' for p, n, no, pr, e in sorted(card_links, key=lambda x: (len(str(x[2])), str(x[2]))))}</table>
<p class="est">* Schätzung nach Seltenheit</p></div>"""
        ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{sname} ({gname})", "url": f"{BASE}/{spath}/",
               "about": {"@type": "Thing", "name": sname}, "numberOfItems": len(rows)}]
        page(spath, f"{sname} – alle Karten & Preise ({gname}) | Foilio",
             f"Alle {len(rows)} Karten aus {sname} ({gname}) mit aktuellen Preisen. Wertvollste Karte: {top[0][1]} ({eur(top[0][3])}).",
             body, [("Foilio", ""), (gname, f"spiel/{gslug}/"), (sname, None)], ld, None, "0.7")
    sl = sorted(set_paths.items(), key=lambda x: sets[x[0]][3] or "0000", reverse=True)
    body = f"""<h1>{esc(gname)}: alle Sets und Karten</h1><p class="sub">{len(sl)} Sets · {n_cards} Karten · Preise: {esc(src)}</p>
<div class="box"><ul class="cols">{"".join(f'<li><a href="../../{p}/">{esc(sets[i][1])}</a>{" (" + esc(sets[i][3][:4]) + ")" if sets[i][3] else ""}</li>' for i, p in sl)}</ul></div>"""
    page(f"spiel/{gslug}", f"{gname} Karten & Preise – alle Sets | Foilio", f"Alle {gname}-Sets und {n_cards} Karten mit aktuellen Marktpreisen und echtem Preisverlauf.",
         body, [("Foilio", ""), ("Spiele", "spiel/"), (gname, None)], [], None, "0.8")
    game_index.append((gname, gslug, len(sl), n_cards))
    print(g, "sets", len(sl), "cards", n_cards, flush=True)

body = "<h1>Alle Spiele</h1><div class='box'><ul>" + "".join(f'<li><a href="{s}/">{esc(n)}</a> – {k} Sets, {c} Karten</li>' for n, s, k, c in game_index) + "</ul></div>"
page("spiel", "Sammelkarten-Preise: Pokémon, Magic, Yu-Gi-Oh!, Lorcana, One Piece | Foilio",
     "Preise und Preisverlauf für Pokémon, Magic, Yu-Gi-Oh!, Lorcana und One Piece: alle Sets und Karten.", body, [("Foilio", ""), ("Spiele", None)], [], None, "0.9")
open(os.path.join(SITE, "k.css"), "w").write(CSS)

# sitemaps (max 50,000 addresses per file) and robots.txt
urls.insert(0, ("", TODAY, "1.0"))
os.makedirs(os.path.join(SITE, "sitemaps"), exist_ok=True)
chunks = [urls[i:i + 40000] for i in range(0, len(urls), 40000)]
for i, ch in enumerate(chunks):
    with open(os.path.join(SITE, "sitemaps", f"s{i}.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        f.write("".join(f"<url><loc>{esc(BASE + '/' + p + ('/' if p else ''))}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>" for p, d, pr in ch))
        f.write("</urlset>")
with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    f.write("".join(f"<sitemap><loc>{BASE}/sitemaps/s{i}.xml</loc><lastmod>{TODAY}</lastmod></sitemap>" for i in range(len(chunks))))
    f.write("</sitemapindex>")
open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print("pages", len(urls), "sitemaps", len(chunks))
