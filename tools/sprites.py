"""Download card thumbnails for RAW/sprite_todo.json and pack them into sprite sheets (10x10, 240x336 per card).
usage: python3 -I sprites.py RAW_DIR OUT_DIR
Writes OUT_DIR/sp/<n>.webp and OUT_DIR/sprites.json {cardId: [sheet, index]}.
"""
import io, json, os, sys, time, urllib.request, concurrent.futures as cf
from PIL import Image

RAW, OUT = sys.argv[1], sys.argv[2]
CACHE = os.path.join(RAW, "thumbs"); os.makedirs(CACHE, exist_ok=True); os.makedirs(os.path.join(OUT, "sp"), exist_ok=True)
W, H, COLS, ROWS = 240, 336, 10, 10
todo = json.load(open(os.path.join(RAW, "sprite_todo.json")))

def grab(item):
    p = os.path.join(CACHE, item["id"] + ".webp")
    if os.path.exists(p): return item["id"], True
    urls = [item["img"]] + ([item["img"].replace("/de/", "/en/")] if "/de/" in item["img"] else [])
    for i in range(3):
        try:
            req = urllib.request.Request(urls[min(i, len(urls) - 1)], headers={"User-Agent": "foilio-catalog/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r: b = r.read()
            im = Image.open(io.BytesIO(b)).convert("RGB")
            # cover-crop to the card ratio, then resize
            tr = W / H; sr = im.width / im.height
            if sr > tr: nw = int(im.height * tr); im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
            elif sr < tr: nh = int(im.width / tr); im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
            im.resize((W, H), Image.LANCZOS).save(p, "WEBP", quality=82)
            return item["id"], True
        except Exception as e:
            time.sleep(1 + i)
    return item["id"], False

ok = {}
with cf.ThreadPoolExecutor(8) as ex:
    for cid, good in ex.map(grab, todo):
        ok[cid] = good
got = [t["id"] for t in todo if ok.get(t["id"])]
print("downloaded", len(got), "of", len(todo), flush=True)

index, per = {}, COLS * ROWS
for s in range(0, len(got), per):
    sheet = Image.new("RGB", (W * COLS, H * ROWS), (20, 24, 36))
    for k, cid in enumerate(got[s:s + per]):
        sheet.paste(Image.open(os.path.join(CACHE, cid + ".webp")), ((k % COLS) * W, (k // COLS) * H))
        index[cid] = [s // per, k]
    sheet.save(os.path.join(OUT, "sp", f"{s // per}.webp"), "WEBP", quality=72, method=6)
json.dump(index, open(os.path.join(OUT, "sprites.json"), "w"), separators=(",", ":"))
print("sheets", (len(got) + per - 1) // per)
