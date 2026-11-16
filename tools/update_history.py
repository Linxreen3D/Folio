"""Append today's real market prices to the per-game price history (one value per card per day).
Only real prices are stored (no estimates). Keeps the last 400 days.
usage: python3 -I update_history.py OUT_DIR
Reads OUT_DIR/{game}.json, OUT_DIR/curated.json, OUT_DIR/index.json; writes OUT_DIR/hist/{game}.json and OUT_DIR/hist/cur.json
Format: {"days": ["2026-11-14", ...], "p": {"cardId": [price or null per day]}}
"""
import json, os, sys

OUT = sys.argv[1]
H = os.path.join(OUT, "hist"); os.makedirs(H, exist_ok=True)
day = json.load(open(os.path.join(OUT, "index.json")))["built"][:10]
KEEP = 400

def update(name, today):  # today: {id: price}
    p = os.path.join(H, name + ".json")
    hist = json.load(open(p)) if os.path.exists(p) else {"days": [], "p": {}}
    if day in hist["days"]:
        i = hist["days"].index(day)  # re-run on the same day: overwrite that column
    else:
        hist["days"].append(day); i = len(hist["days"]) - 1
        for v in hist["p"].values(): v.append(None)
    n = len(hist["days"])
    for cid, price in today.items():
        row = hist["p"].setdefault(cid, [None] * n)
        row += [None] * (n - len(row))
        row[i] = round(price, 2)
    if n > KEEP:
        cut = n - KEEP
        hist["days"] = hist["days"][cut:]
        hist["p"] = {k: v[cut:] for k, v in hist["p"].items() if any(x is not None for x in v[cut:])}
    json.dump(hist, open(p, "w"), separators=(",", ":"))
    return len(today), n

for g in ("pkm", "mtg", "ygo", "lor", "op"):
    if not os.path.exists(os.path.join(OUT, g + ".json")): print(g, "skipped (no catalog today)"); continue
    d = json.load(open(os.path.join(OUT, g + ".json")))
    today = {r[0]: r[6] for r in d["cards"] if not r[7] and r[6]}  # r[7] = estimate flag
    print(g, *update(g, today))
cur = json.load(open(os.path.join(OUT, "curated.json")))
print("cur", *update("cur", {k: v["p"] for k, v in cur.items() if v.get("p")}))
