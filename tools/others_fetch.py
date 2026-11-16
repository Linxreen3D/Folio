"""Magic (Scryfall), Yu-Gi-Oh! (YGOPRODeck), Lorcana (Lorcast), One Piece (official card list).
Writes raw/<game>_norm.json with normalized sets + cards.
usage: python3 -I others_fetch.py RAW_DIR [games...]
"""
import json, os, re, sys, time, html, datetime, urllib.request, urllib.parse

RAW = sys.argv[1]
GAMES = sys.argv[2:] or ["mtg", "ygo", "lor", "op"]
UA = {"User-Agent": "foilio-catalog/1.0", "Accept": "application/json;q=0.9,*/*;q=0.8"}
TODAY = datetime.date.today()

def fetch(url, tries=4, raw=False):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                b = r.read()
                return b if raw else json.loads(b)
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))

def num(x):
    try:
        v = float(x)
        return v if v > 0 else None
    except Exception:
        return None

def save(game, sets, cards):
    json.dump({"sets": sets, "cards": cards}, open(os.path.join(RAW, f"{game}_norm.json"), "w"))
    print(game, "sets", len(sets), "cards", len(cards), flush=True)

# ---------------- Magic ----------------
def mtg():
    sets = fetch("https://api.scryfall.com/sets")["data"]
    keep_types = {"core", "expansion", "masters", "draft_innovation", "commander", "funny", "starter", "box", "duel_deck", "from_the_vault", "spellbook", "premium_deck", "eternal", "masterpiece", "arsenal", "planechase", "archenemy", "treasure_chest", "promo"}
    smeta = {s["code"]: s for s in sets if not s.get("digital") and s["set_type"] in keep_types}
    def img(c):
        u = c.get("image_uris") or ((c.get("card_faces") or [{}])[0].get("image_uris")) or {}
        return u.get("small")
    def norm(c):
        p = c.get("prices") or {}
        return {"id": c["id"], "name": c["name"], "set": c["set"], "no": c["collector_number"], "r": c.get("rarity"),
                "p": num(p.get("eur")) or num(p.get("eur_foil")), "img": img(c)}
    q = "game:paper -layout:token -layout:double_faced_token -layout:art_series -layout:emblem -is:digital"
    url = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode({"q": q, "unique": "cards", "order": "released"})
    cards, page = [], 0
    while url:
        d = fetch(url); page += 1
        cards += [norm(c) for c in d["data"]]
        url = d.get("next_page") if d.get("has_more") else None
        if page % 25 == 0: print("mtg page", page, len(cards), flush=True)
        time.sleep(0.12)
    # newest sets: all printings, so set pages are complete for fresh releases
    seen = {c["id"] for c in cards}
    recent = [s for s in smeta.values() if s["set_type"] in ("core", "expansion", "masters", "draft_innovation", "commander")
              and s.get("released_at") and (TODAY - datetime.date.fromisoformat(s["released_at"])).days <= 120]
    for s in recent:
        url = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode({"q": f"e:{s['code']} -is:digital", "unique": "prints", "order": "set"})
        while url:
            try: d = fetch(url)
            except Exception as e: print("mtg recent fail", s["code"], e); break
            for c in d["data"]:
                if c["id"] not in seen and c.get("layout") not in ("token", "art_series", "emblem"):
                    cards.append(norm(c)); seen.add(c["id"])
            url = d.get("next_page") if d.get("has_more") else None
            time.sleep(0.12)
    used = {c["set"] for c in cards}
    out_sets = [{"k": code, "n": s["name"], "c": code.upper(), "d": s.get("released_at"), "t": s.get("card_count"), "s": s["set_type"]}
                for code, s in smeta.items() if code in used]
    # upcoming sets with no cards yet are still listed (pre-release calendar)
    for code, s in smeta.items():
        if code not in used and s.get("released_at") and datetime.date.fromisoformat(s["released_at"]) > TODAY and s["set_type"] in ("expansion", "core", "masters", "draft_innovation", "commander"):
            out_sets.append({"k": code, "n": s["name"], "c": code.upper(), "d": s["released_at"], "t": s.get("card_count"), "s": s["set_type"]})
    cards = [c for c in cards if c["set"] in smeta]
    save("mtg", out_sets, cards)

# ---------------- Yu-Gi-Oh! ----------------
def ygo():
    en = fetch("https://db.ygoprodeck.com/api/v7/cardinfo.php")["data"]
    try: de = {c["id"]: c["name"] for c in fetch("https://db.ygoprodeck.com/api/v7/cardinfo.php?language=de")["data"]}
    except Exception as e: print("ygo de fail", e); de = {}
    sets = fetch("https://db.ygoprodeck.com/api/v7/cardsets.php")
    sdate = {s["set_name"]: s.get("tcg_date") for s in sets}
    scode = {s["set_name"]: s.get("set_code") for s in sets}
    cards = []
    for c in en:
        prints = [p for p in (c.get("card_sets") or []) if sdate.get(p["set_name"])]
        if not prints: continue
        first = min(prints, key=lambda p: sdate[p["set_name"]])
        price = num(((c.get("card_prices") or [{}])[0]).get("cardmarket_price"))
        cards.append({"id": str(c["id"]), "name": de.get(c["id"]) or c["name"], "en": c["name"], "set": first["set_name"], "no": first["set_code"],
                      "r": first.get("set_rarity"), "p": price, "img": f"https://images.ygoprodeck.com/images/cards_small/{c['id']}.jpg"})
    used = {c["set"] for c in cards}
    out_sets = [{"k": s["set_name"], "n": s["set_name"], "c": s.get("set_code"), "d": s.get("tcg_date"), "t": s.get("num_of_cards"), "s": ""}
                for s in sets if s["set_name"] in used or (s.get("tcg_date") and s["tcg_date"] > TODAY.isoformat())]
    save("ygo", out_sets, cards)

# ---------------- Lorcana ----------------
def lor():
    sets = fetch("https://api.lorcast.com/v0/sets")["results"]
    rar = ["common", "uncommon", "rare", "super_rare", "legendary", "enchanted", "epic", "iconic", "promo", "special"]
    cards, seen = [], set()
    for s in sets:
        for r in rar:
            url = "https://api.lorcast.com/v0/cards/search?" + urllib.parse.urlencode({"q": f"set:{s['code']} rarity:{r}"})
            try: d = fetch(url)
            except Exception as e: print("lor fail", s["code"], r, e); continue
            for c in d.get("results", []):
                if c["id"] in seen: continue
                seen.add(c["id"])
                p = c.get("prices") or {}
                usd = num(p.get("usd")) or num(p.get("usd_foil"))
                cards.append({"id": c["id"], "name": c["name"] + (" – " + c["version"] if c.get("version") else ""), "set": s["code"], "no": c.get("collector_number"),
                              "r": c.get("rarity"), "p": round(usd * 0.86, 2) if usd else None, "usd": True,
                              "img": ((c.get("image_uris") or {}).get("digital") or {}).get("small")})
            time.sleep(0.1)
    out_sets = [{"k": s["code"], "n": s["name"], "c": s["code"], "d": s.get("released_at"), "t": None, "s": ""} for s in sets]
    save("lor", out_sets, cards)

# ---------------- One Piece ----------------
def op():
    base = "https://en.onepiece-cardgame.com/cardlist/"
    page = fetch(base, raw=True).decode("utf-8", "replace")
    opts = re.findall(r'option value="(\d+)"[^>]*>(.*?)</option>', page, re.S)
    series = []
    for v, label in opts:
        t = re.sub(r"<[^>]+>", " ", html.unescape(html.unescape(label)))
        t = re.sub(r"\s+", " ", t).strip()
        m = re.search(r"\[([^\]]+)\]\s*$", t)
        code = m.group(1) if m else v
        name = re.sub(r"\s*\[[^\]]+\]\s*$", "", t).strip(" -")
        series.append((v, code, name))
    cards, seen = [], {}
    for v, code, name in series:
        try: h = fetch(base + "?series=" + v, raw=True).decode("utf-8", "replace")
        except Exception as e: print("op fail", code, e); continue
        for m in re.finditer(r'<dl class="modalCol" id="([^"]+)">(.*?)</dl>', h, re.S):
            cid, body = m.group(1), m.group(2)
            info = re.findall(r"<span>(.*?)</span>", re.search(r'class="infoCol">(.*?)</div>', body, re.S).group(1))
            nm = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'class="cardName">(.*?)</div>', body, re.S).group(1))).strip()
            if cid in seen: continue
            seen[cid] = 1
            no = info[0] if info else cid
            alt = "_p" in cid or "_r" in cid
            cards.append({"id": cid, "name": nm, "set": code, "no": no + (" (Parallel)" if alt else ""), "r": (info[1] if len(info) > 1 else "") + (" Parallel" if alt else ""),
                          "p": None, "img": f"https://en.onepiece-cardgame.com/images/cardlist/card/{cid}.png"})
        time.sleep(0.3)
    out_sets = [{"k": code, "n": name.title() if name.isupper() else name, "c": code, "d": None, "t": None, "s": "", "o": i} for i, (v, code, name) in enumerate(series)]
    save("op", out_sets, cards)

for g in GAMES:
    try:
        {"mtg": mtg, "ygo": ygo, "lor": lor, "op": op}[g]()
    except Exception as e:
        print("FAILED", g, repr(e), flush=True)
