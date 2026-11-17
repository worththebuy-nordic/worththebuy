"""Render a 400x400 transparent card image of a product figure.

Usage: python3 tools/render_card_image.py <plugin scripts dir> <figure> <out.png> [spec_dir]
<figure> is a draw_* name from make_batch.py / make_mascot2.py, or a path to a figure .py
file that defines draw(d, cx, cy, s, talking, phase, mood, look, blink, t, face_on=True).
"""
import sys, os, importlib.util
scripts, fig, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scripts)
from PIL import Image, ImageDraw
import make_batch as B, make_mascot2 as M
if fig.endswith(".py"):
    sp = importlib.util.spec_from_file_location("fig", fig); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    draw = lambda d, *a: m.draw(d, *a, face_on=True)
else:
    fn = getattr(B, fig, None) or getattr(M, fig)
    def draw(d, *a):
        try: fn(d, *a, face_on=True)
        except TypeError: fn(d, *a, face=True)
big = Image.new("RGBA", (1200, 1200), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
draw(d, 600, 640, 560, False, 0, "smug", 0, False, 0.0)
big.resize((400, 400), Image.LANCZOS).save(out); print("image:", out)
