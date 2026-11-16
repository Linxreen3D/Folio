"""Magic: merge MTGJSON's real daily Cardmarket prices (last ~90 days) into OUT_DIR/hist/mtg.json (and cur.json).
usage: python3 -I mtgjson_backfill.py MTGJSON_DIR OUT_DIR
MTGJSON_DIR needs AllPrices.json.xz and AllPrintings.sqlite from https://mtgjson.com/api/v5/
"""
import json, lzma, os, re, sqlite3, sys
import ijson

SRC, OUT = sys.argv[1], sys.argv[2]
slug = lambda s: re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(s).lower())).strip("-")
CURATED = {"m-ltr-246": "the-one-ring-ltr", "m-dmu-107": "sheoldred-dmu", "m-mh2-138": "ragavan-mh2", "m-ltr-103": "bowmasters-ltr", "m-2xm-51": "force-of-will-2xm"}

ours = {r[0] for r in json.load(open(os.path.join(OUT, "mtg.json")))["cards"]} | set(CURATED)
db = sqlite3.connect(os.path.join(SRC, "AllPrintings.sqlite"))
uuid2id = {}
for uuid, code, num in db.execute("SELECT uuid, setCode, number FROM cards"):
    cid = "m-" + slug(f"{code}-{num}")
    if cid in ours: uuid2id[uuid] = cid
print("mapped printings", len(uuid2id), "of our", len(ours), flush=True)

series = {}  # cardId -> {date: price}
with lzma.open(os.path.join(SRC, "AllPrices.json.xz"), "rb") as f:
    for uuid, obj in ijson.kvitems(f, "data", use_float=True):
        cid = uuid2id.get(uuid)
        if not cid: continue
        cm = (((obj or {}).get("paper") or {}).get("cardmarket") or {}).get("retail") or {}
        pts = cm.get("normal") or cm.get("foil") or {}
        if pts: series[CURATED.get(cid, cid)] = {d: float(v) for d, v in pts.items() if v}
print("cards with history", len(series), flush=True)

def merge(name, data):
    p = os.path.join(OUT, "hist", name + ".json")
    hist = json.load(open(p)) if os.path.exists(p) else {"days": [], "p": {}}
    days = sorted(set(hist["days"]) | {d for s in data.values() for d in s})
    idx = {d: i for i, d in enumerate(hist["days"])}
    out = {}
    for cid in set(hist["p"]) | set(data):
        old, new = hist["p"].get(cid, []), data.get(cid, {})
        row = []
        for d in days:
            v = new.get(d)
            if v is None and d in idx and idx[d] < len(old): v = old[idx[d]]  # keep our own snapshot
            row.append(round(v, 2) if v is not None else None)
        if any(x is not None for x in row): out[cid] = row
    json.dump({"days": days, "p": out}, open(p, "w"), separators=(",", ":"))
    print(name, "days", len(days), days[0] if days else "", "->", days[-1] if days else "", "cards", len(out))

merge("mtg", {k: v for k, v in series.items() if k.startswith("m-")})
merge("cur", {k: v for k, v in series.items() if not k.startswith("m-")})
