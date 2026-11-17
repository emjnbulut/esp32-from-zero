"""Soft bloom around the lit LED in the Blender hero frame (only bright *red* pixels glow, metal stays clean).
   python pilot3d/glow.py in.png out.png"""
import sys
from PIL import Image, ImageChops, ImageFilter

im = Image.open(sys.argv[1]).convert("RGB")
r, g, b = im.split()
mask = ImageChops.multiply(r.point(lambda v: 255 if v > 205 else 0), g.point(lambda v: 255 if v < 185 else 0))
src = Image.composite(im, Image.new("RGB", im.size), mask)
out = ImageChops.screen(im, src.filter(ImageFilter.GaussianBlur(30)))
out = ImageChops.screen(out, src.filter(ImageFilter.GaussianBlur(9)))
out.save(sys.argv[2])
