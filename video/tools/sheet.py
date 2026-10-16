"""Combine render stills into 2x2 contact sheets for quick review.
Usage: python sheet.py <stills_dir>  -> <stills_dir>/sheet_<n>.png"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

d = Path(sys.argv[1])
files = sorted((p for p in d.glob("t*.png")), key=lambda p: float(p.stem[1:]))
for old in d.glob("sheet_*.png"):
    old.unlink()
for i in range(0, len(files), 4):
    sheet = Image.new("RGB", (1920, 1080), "black")
    for j, f in enumerate(files[i:i + 4]):
        im = Image.open(f).convert("RGB").resize((958, 538))
        x, y = (j % 2) * 962, (j // 2) * 542
        sheet.paste(im, (x, y))
        ImageDraw.Draw(sheet).text((x + 8, y + 6), f.stem, fill="yellow")
    sheet.save(d / f"sheet_{i // 4}.png")
    print(d / f"sheet_{i // 4}.png")
