"""Pokémon: fetch set meta (series, release date, code) and per-card rarity + Cardmarket prices from TCGdex.
Incremental: card details already cached are skipped unless --refresh-prices is given.
usage: python3 -I pkm_fetch.py RAW_DIR [--refresh-prices]
"""
import json, os, sys, time, urllib.request, concurrent.futures as cf

RAW = sys.argv[1]
REFRESH = "--refresh-prices" in sys.argv
API = "https://api.tcgdex.net/v2"
UA = {"User-Agent": "foilio-catalog/1.0"}

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read())
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))

def cached(name, url):
    p = os.path.join(RAW, name)
    if os.path.exists(p):
        return json.load(open(p))
    d = get(url)
    json.dump(d, open(p, "w"))
    return d

series = cached("tcg_series_en.json", f"{API}/en/series")
set_serie = {}
for s in series:
    sd = cached(f"tcg_serie_{s['id']}.json", f"{API}/en/series/{s['id']}")
    for st in sd.get("sets", []):
        set_serie[st["id"]] = (s["id"], s["name"])

sets = cached("tcg_sets_en.json", f"{API}/en/sets")
meta_p = os.path.join(RAW, "tcg_setmeta.json")
meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
for st in sets:
    if st["id"] in meta:
        continue
    try:
        d = get(f"{API}/en/sets/{st['id']}")
        meta[st["id"]] = {"name": d.get("name"), "date": d.get("releaseDate"), "code": (d.get("abbreviation") or {}).get("official"),
                          "total": (d.get("cardCount") or {}).get("total"), "official": (d.get("cardCount") or {}).get("official")}
    except Exception as e:
        print("set meta fail", st["id"], e)
json.dump(meta, open(meta_p, "w"))
print("sets", len(meta), flush=True)

cards = cached("tcg_cards_en.json", f"{API}/en/cards")
skip_sets = {sid for sid, (ser, _) in set_serie.items() if ser == "tcgp"}  # TCG Pocket is digital-only
todo = [c["id"] for c in cards if c["id"].rsplit("-", 1)[0] not in skip_sets]
det_p = os.path.join(RAW, "tcg_details.json")
det = json.load(open(det_p)) if os.path.exists(det_p) else {}
need = [i for i in todo if REFRESH or i not in det]
print("cards", len(todo), "to fetch", len(need), flush=True)

def one(cid):
    d = get(f"{API}/en/cards/{cid}")
    cm = ((d.get("pricing") or {}).get("cardmarket") or {})
    return cid, {"r": d.get("rarity"), "t": cm.get("trend"), "a1": cm.get("avg1"), "a7": cm.get("avg7"), "a30": cm.get("avg30"),
                 "lo": cm.get("low"), "th": cm.get("trend-holo"), "u": cm.get("updated"), "set": (d.get("set") or {}).get("id")}

done = 0
with cf.ThreadPoolExecutor(8) as ex:
    futs = [ex.submit(one, c) for c in need]
    for f in cf.as_completed(futs):
        try:
            cid, v = f.result()
            det[cid] = v
        except Exception as e:
            pass
        done += 1
        if done % 1000 == 0:
            json.dump(det, open(det_p, "w"))
            print("progress", done, len(need), flush=True)
json.dump(det, open(det_p, "w"))
print("done", len(det), flush=True)
