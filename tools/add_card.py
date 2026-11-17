"""Add a product card to the top of index.html and mark it "Latest video".

Usage:
  python3 tools/add_card.py --key zolo20k --name "Anker Zolo power bank 20,000 mAh" \
      --cat "Phone & tech" --facts "Built-in USB-C cable · 20,000 mAh · 30 W max" \
      --link "https://www.amazon.se/dp/B0CZ9LH53B?tag=worththebuy0c-21" --image card.png

--image: a 400x400 transparent PNG of the product figure (with face), drawn with the
worththebuy-studio plugin, e.g. render_card_image.py. If the key already exists the
script does nothing (safe to run twice). Only facts that appear in the video may be used;
never prices, ratings or "best"/"tested" claims. The link must carry tag=worththebuy0c-21.
"""
import argparse, base64, html, os, re, sys

ap = argparse.ArgumentParser()
for a in ("key", "name", "cat", "facts", "link", "image"):
    ap.add_argument("--" + a, required=True)
ap.add_argument("--file", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html"))
o = ap.parse_args()

if "tag=worththebuy0c-21" not in o.link or not o.link.startswith("https://www.amazon.se/dp/"):
    sys.exit("link must be https://www.amazon.se/dp/<ASIN>?tag=worththebuy0c-21")
s = open(o.file, encoding="utf-8").read()
if f'id="{o.key}"' in s:
    print("already on the page:", o.key); sys.exit(0)

b64 = base64.b64encode(open(o.image, "rb").read()).decode()
e = lambda t: html.escape(t, quote=True)
# demote the current first card
s = s.replace('<article class="card first"', '<article class="card"', 1)
s = re.sub(r'<span class="new">Latest video</span>', '', s, count=1)
card = f'''<article class="card first" id="{e(o.key)}">
  <div class="pic"><img src="data:image/png;base64,{b64}" alt="Illustration of {e(o.name)}"><span class="new">Latest video</span></div>
  <div class="body">
    <div class="cat">{e(o.cat)}</div>
    <h2>{e(o.name)}</h2>
    <p>{e(o.facts)}</p>
    <a class="btn" href="{e(o.link)}" target="_blank" rel="sponsored nofollow noopener">View on Amazon</a>
  </div>
</article>'''
i = s.index("<main>") + len("<main>")
s = s[:i] + "\n" + card + s[i:].lstrip("\n")
open(o.file, "w", encoding="utf-8").write(s)
print("added:", o.key, "| cards:", s.count("<article"))
