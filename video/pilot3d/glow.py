"""Soft bloom around the lit LED in Blender frames (only bright *red* pixels glow, metal stays clean).
   python pilot3d/glow.py in.png out.png
   python pilot3d/glow.py <in dir> <out dir>      (every f_*.png, skips frames already done)"""
import os
import sys

from PIL import Image, ImageChops, ImageFilter


def glow(src_path, out_path):
    im = Image.open(src_path).convert("RGB")
    r, g, _ = im.split()
    mask = ImageChops.multiply(r.point(lambda v: 255 if v > 205 else 0), g.point(lambda v: 255 if v < 185 else 0))
    src = Image.composite(im, Image.new("RGB", im.size), mask)
    out = ImageChops.screen(im, src.filter(ImageFilter.GaussianBlur(30)))
    out = ImageChops.screen(out, src.filter(ImageFilter.GaussianBlur(9)))
    out.save(out_path)


a, b = sys.argv[1], sys.argv[2]
if os.path.isdir(a):
    os.makedirs(b, exist_ok=True)
    names = sorted(n for n in os.listdir(a) if n.startswith("f_") and n.endswith(".png"))
    for i, n in enumerate(names):
        if not os.path.exists(os.path.join(b, n)):
            glow(os.path.join(a, n), os.path.join(b, n))
        if i % 100 == 0:
            print(i, "/", len(names), flush=True)
else:
    glow(a, b)
