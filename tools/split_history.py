"""Split OUT_DIR/hist/<game>.json into ~1 MB chunks the site loads on demand: OUT_DIR/histc/<game>-<n>.json + meta.json.
A card's chunk is fnv1a32(cardId) % chunks (same hash as the page's hashStr).
usage: python3 -I split_history.py OUT_DIR
"""
import json, math, os, sys

OUT = sys.argv[1]
src, dst = os.path.join(OUT, "hist"), os.path.join(OUT, "histc")
os.makedirs(dst, exist_ok=True)
for f in os.listdir(dst): os.remove(os.path.join(dst, f))

def fnv(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch); h = (h * 16777619) & 0xFFFFFFFF
    return h

meta = {}
for f in sorted(os.listdir(src)):
    if not f.endswith(".json"): continue
    g = f[:-5]
    hist = json.load(open(os.path.join(src, f)))
    n = max(1, math.ceil(os.path.getsize(os.path.join(src, f)) / 1_000_000))
    parts = [{"days": hist["days"], "p": {}} for _ in range(n)]
    for cid, row in hist["p"].items():
        parts[fnv(cid) % n]["p"][cid] = row
    for i, part in enumerate(parts):
        json.dump(part, open(os.path.join(dst, f"{g}-{i}.json"), "w"), separators=(",", ":"))
    meta[g] = n
json.dump(meta, open(os.path.join(dst, "meta.json"), "w"))
print(meta)
