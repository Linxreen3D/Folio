"""Turn raw source data into the compact catalog files the site loads.
usage: python3 -I build_catalog.py RAW_DIR OUT_DIR
Writes OUT_DIR/{pkm,mtg,ygo,lor,op}.json, index.json, curated.json, changes.json and RAW_DIR/sprite_todo.json.
"""
import json, os, re, sys, datetime

RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
TODAY = datetime.date.today().isoformat()
slug = lambda s: re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(s).lower())).strip("-")

EST = {  # rarity based estimate in EUR, used only when no market price exists (always labelled as estimate)
 "pkm": [("secret", 8), ("special illustration", 15), ("hyper", 10), ("illustration", 4), ("ultra", 3), ("double", 1), ("holo", 1.2), ("rare", .4), ("uncommon", .15), ("common", .08)],
 "mtg": [("mythic", 2.5), ("special", 3), ("bonus", 3), ("rare", .7), ("uncommon", .15), ("common", .08)],
 "ygo": [("starlight", 60), ("ghost", 40), ("quarter century", 20), ("collector", 12), ("prismatic", 8), ("secret", 5), ("ultimate", 6), ("ultra", 2), ("super", .8), ("rare", .3), ("common", .1)],
 "lor": [("enchanted", 60), ("iconic", 80), ("epic", 15), ("legendary", 4), ("super", 1), ("rare", .4), ("uncommon", .15), ("common", .08), ("promo", 3)],
 "op":  [("sec parallel", 60), ("sr parallel", 12), ("l parallel", 10), ("parallel", 4), ("sp", 25), ("sec", 15), ("tr", 8), ("sr", 2), ("l", 1.5), ("p", 1), ("r", .4), ("uc", .15), ("c", .08)],
}
def estimate(g, rar):
    r = (rar or "").lower()
    for k, v in EST[g]:
        if (r == k) or (len(k) > 2 and k in r) or (g == "op" and r.split(" ")[0] == k.split(" ")[0] and ("parallel" in k) == ("parallel" in r)):
            return v
    return .3

CURATED = {"glurak-ex-151": "p-sv03-5-199", "pikachu-ex-ssp": "p-sv08-238", "nachtara-ex-pre": "p-sv08-5-161", "mew-ex-151": "p-sv03-5-205",
           "lugia-v-sit": "p-swsh12-186", "guardevoir-ex-svi": "p-sv01-245", "bisasam-mew": "p-sv03-5-166",
           "the-one-ring-ltr": "m-ltr-246", "sheoldred-dmu": "m-dmu-107", "ragavan-mh2": "m-mh2-138", "bowmasters-ltr": "m-ltr-103", "force-of-will-2xm": "m-2xm-51",
           "ash-blossom-mp": "y-14558127", "dunkler-magier-lob": "y-46986414", "bewd-lob": "y-89631139", "snake-eye-ash": "y-9674034",
           "elsa-tfc": "l-1-207", "mickey-tfc": "l-1-208", "hades-tfc": "l-1-205", "belle-tfc": "l-1-214",
           "shanks-op01": "o-op01-120-p1", "ruffy-op05": "o-op05-119", "nami-op01": "o-op01-016-p1", "zoro-op01": "o-op01-025-p1"}
REV = {v: k for k, v in CURATED.items()}

games = {}
# ---------------- Pokémon ----------------
def have(*names):
    miss = [n for n in names if not os.path.exists(f"{RAW}/{n}")]
    if miss: print("WARNING: skipping game, raw data missing:", miss, flush=True)
    return not miss
if have("tcg_cards_en.json", "tcg_cards_de.json", "tcg_details.json", "tcg_setmeta.json"):
    en = json.load(open(f"{RAW}/tcg_cards_en.json")); de = {c["id"]: c["name"] for c in json.load(open(f"{RAW}/tcg_cards_de.json"))}
    det = json.load(open(f"{RAW}/tcg_details.json")); meta = json.load(open(f"{RAW}/tcg_setmeta.json"))
    serie = {}
    for f in os.listdir(RAW):
        if f.startswith("tcg_serie_") and f != "tcg_series_en.json":
            d = json.load(open(f"{RAW}/{f}"))
            for st in d.get("sets", []): serie[st["id"]] = (d["id"], d["name"])
    sets, cards = {}, []
    for c in en:
        if c["id"] not in det: continue
        sid = c["id"].rsplit("-", 1)[0]; m = meta.get(sid) or {}; dd = det[c["id"]]
        if sid not in sets: sets[sid] = {"k": sid, "n": m.get("name") or sid, "c": m.get("code") or sid.upper(), "d": m.get("date"), "t": m.get("total"), "s": (serie.get(sid) or ("", ""))[1]}
        price = next((v for v in (dd.get("t"), dd.get("th"), dd.get("a30"), dd.get("a7"), dd.get("lo")) if v), None)
        nm_de = de.get(c["id"]); nm_en = c["name"]
        lang = "de" if nm_de else "en"
        cards.append({"id": "p-" + slug(c["id"]), "name": nm_de or nm_en, "en": nm_en if nm_de and nm_de != nm_en else "", "set": sid, "no": c["localId"], "r": dd.get("r") or "",
                      "p": price, "a30": dd.get("a30"), "a7": dd.get("a7"), "a1": dd.get("a1"), "lo": dd.get("lo"),
                      "img": f"https://assets.tcgdex.net/{lang}/{(serie.get(sid) or ('misc',))[0]}/{sid}/{c['localId']}/low.webp"})
    games["pkm"] = (list(sets.values()), cards)

# ---------------- others ----------------
for g, pre in (("mtg", "m"), ("ygo", "y"), ("lor", "l"), ("op", "o")):
    if not have(f"{g}_norm.json"): continue
    n = json.load(open(f"{RAW}/{g}_norm.json"))
    for c in n["cards"]:
        c["id"] = pre + "-" + (slug(c["id"]) if g in ("ygo", "op") else slug(c["set"] + "-" + str(c["no"])))
        if g == "mtg": c["img"] = (c.get("img") or "").replace("/small/", "/normal/")
        if g == "ygo": c["img"] = c["img"].replace("cards_small", "cards")
        if g == "lor": c["img"] = (c.get("img") or "").replace("/small/", "/normal/")
    if g == "op":
        for st in n["sets"]:
            nm = st["n"]
            if sum(ch.isupper() for ch in nm) > sum(ch.islower() for ch in nm): nm = nm.title()
            st["n"] = re.sub(r"\s+-\s*|\s*-\s+|^-|-$", " – ", nm).strip(" –").replace("’S", "’s").replace("'S", "'s")
    games[g] = (n["sets"], n["cards"])

prev = {}
if os.path.exists(f"{OUT}/index.json"):
    try: prev = json.load(open(f"{OUT}/index.json"))
    except Exception: prev = {}
prev_sets = {(s["g"], s["k"]) for s in prev.get("allSets", [])}
prev_counts = {g: v.get("cards", 0) for g, v in prev.get("games", {}).items()}

index = {"built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "games": {}, "allSets": [], "latest": [], "upcoming": []}
curated_prices, sprite_todo, changes = {}, [], {"at": index["built"], "newSets": [], "newCards": {}}
for g, (sets, cards) in games.items():
    seen, out_cards = set(), []
    rar = sorted({c.get("r") or "" for c in cards}); ri = {r: i for i, r in enumerate(rar)}
    set_list = sorted(sets, key=lambda s: (s.get("d") or "0000", s.get("o", 0)))
    if g == "op": set_list = sorted(sets, key=lambda s: s.get("o", 0))  # official list is newest first
    si = {s["k"]: i for i, s in enumerate(set_list)}
    for c in cards:
        if c["set"] not in si: continue
        cid = c["id"]
        while cid in seen: cid += "x"
        seen.add(cid)
        if cid in REV:
            curated_prices[REV[cid]] = {k: c.get(k) for k in ("p", "a30", "a7", "a1", "lo") if c.get(k)}
            continue
        est = 0
        p = c.get("p")
        if not p: p, est = estimate(g, c.get("r")), 1
        # [id, name, alias, setIdx, no, rarIdx, price, est, a30, a7, a1, low, usd]
        row = [cid, c["name"], c.get("en") or "", si[c["set"]], str(c.get("no") or ""), ri[c.get("r") or ""], round(p, 2), est,
               c.get("a30") or 0, c.get("a7") or 0, c.get("a1") or 0, c.get("lo") or 0, 1 if c.get("usd") else 0]
        out_cards.append(row)
        sprite_todo.append({"id": cid, "g": g, "p": p, "est": est, "img": c.get("img"), "set": c["set"], "d": (set_list[si[c["set"]]].get("d") or "")})
    sl = [[s["k"], s["n"], s.get("c") or "", s.get("d") or "", s.get("t") or 0, s.get("s") or ""] for s in set_list]
    json.dump({"g": g, "built": index["built"], "rar": rar, "sets": sl, "cards": out_cards}, open(f"{OUT}/{g}.json", "w"), ensure_ascii=False, separators=(",", ":"))
    counts = {}
    for r in out_cards: counts[r[3]] = counts.get(r[3], 0) + 1
    index["games"][g] = {"cards": len(out_cards), "sets": len(sl), "priced": sum(1 for r in out_cards if not r[7])}
    for i, s in enumerate(sl):
        ent = {"g": g, "k": s[0], "n": s[1], "c": s[2], "d": s[3], "t": s[4], "have": counts.get(i, 0)}
        index["allSets"].append({"g": g, "k": s[0]})
        if (g, s[0]) not in prev_sets and prev_sets: changes["newSets"].append(ent)
        if s[3] and s[3] > TODAY: index["upcoming"].append(ent)
    recent = [s for s in sl if s[3] and s[3] <= TODAY and counts.get(si[s[0]], 0) >= 10]
    recent = sorted(recent, key=lambda s: s[3])[-2:] if g != "op" else [s for s in sl if counts.get(si[s[0]], 0) >= 10 and re.match(r"^(OP|EB|PRB)", s[2] or "")][:2]
    for s in recent: index["latest"].append({"g": g, "k": s[0], "n": s[1], "c": s[2], "d": s[3], "t": s[4], "have": counts.get(si[s[0]], 0)})
    changes["newCards"][g] = len(out_cards) - prev_counts.get(g, 0) if prev_counts else 0
index["latest"].sort(key=lambda s: s["d"] or "", reverse=True)
index["upcoming"].sort(key=lambda s: s["d"])
json.dump(index, open(f"{OUT}/index.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(curated_prices, open(f"{OUT}/curated.json", "w"), separators=(",", ":"))
json.dump(changes, open(f"{OUT}/changes.json", "w"), ensure_ascii=False, indent=1)

# sprite selection: most valuable real-priced cards per game + the newest set of each game
quota = {"pkm": 600, "mtg": 450, "ygo": 350, "lor": 250, "op": 250}
pick, chosen = [], set()
for g, q in quota.items():
    rows = [r for r in sprite_todo if r["g"] == g and r["img"]]
    top = sorted(rows, key=lambda r: (-(r["est"] == 0) if g != "op" else 0, -r["p"]))[:q]
    newest = max((r["d"] for r in rows if r["d"] and r["d"] <= TODAY), default="")
    fresh = sorted([r for r in rows if r["d"] == newest], key=lambda r: -r["p"])[:60] if newest else []
    if g == "op":
        latest_set = next((s["k"] for s in index["latest"] if s["g"] == "op"), None)
        fresh = sorted([r for r in rows if r["set"] == latest_set], key=lambda r: -r["p"])[:60]
    for r in top + fresh:
        if r["id"] not in chosen: chosen.add(r["id"]); pick.append({"id": r["id"], "img": r["img"]})
json.dump(pick, open(f"{RAW}/sprite_todo.json", "w"))
print(json.dumps(index["games"]), "curated", len(curated_prices), "sprites", len(pick))
print("latest", [(s["g"], s["n"], s["d"]) for s in index["latest"]])
print("upcoming", [(s["g"], s["n"], s["d"]) for s in index["upcoming"]][:12])
