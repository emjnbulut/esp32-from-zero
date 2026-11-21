"""Textures for the Blender kit (run with the repo venv, needs Pillow):

    .venv/Scripts/python video/b3d/tex.py

Writes video/b3d/build/breadboard.png: the top of an 830-point breadboard lying HORIZONTALLY (row 1 on the
left, row 63 on the right, letters a at the bottom .. j at the top), printed numbers and letters readable
from the front camera. Board-local mm: X = (row - 32) * 2.54 (-82.5..82.5), Y = letter offset (-27.5..27.5).
"""
import os

from PIL import Image, ImageDraw, ImageFont

P = 2.54
W_MM, L_MM = 55.0, 165.0
PX = 32  # pixels per mm -> sharp in close-ups
LETTER = {"a": -15.24, "b": -12.7, "c": -10.16, "d": -7.62, "e": -5.08,
          "f": 5.08, "g": 7.62, "h": 10.16, "i": 12.7, "j": 15.24}
RAILY = {"lminus": -24.14, "lplus": -21.6, "rplus": 21.6, "rminus": 24.14}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")


def font(bold, size):
    for name in (("segoeuib.ttf", "seguisb.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(os.path.join("C:/Windows/Fonts", name), size)
        except OSError:
            continue
    return ImageFont.load_default()


def rail_hole(n):
    return n % 6 != 0  # rail holes come in groups of five


def breadboard():
    w, h = int(L_MM * PX), int(W_MM * PX)
    img = Image.new("RGB", (w, h), "#efeee9")
    g = ImageDraw.Draw(img)
    X = lambda mm: (mm + L_MM / 2) * PX
    Y = lambda mm: (W_MM / 2 - mm) * PX
    # centre groove
    g.rectangle([X(-80), Y(1.6), X(80), Y(-1.6)], fill="#d6d3ca")

    def hole(x, y):
        s = 1.3 * PX / 2
        g.rectangle([X(x) - s - 5, Y(y) - s - 5, X(x) + s + 5, Y(y) + s + 5], fill="#cdcac1")
        g.rectangle([X(x) - s, Y(y) - s, X(x) + s, Y(y) + s], fill="#34322e")

    small, big = font(False, int(1.45 * PX)), font(True, int(1.9 * PX))
    for n in range(1, 64):
        x = (n - 32) * P
        for y in LETTER.values():
            hole(x, y)
        if rail_hole(n):
            for y in RAILY.values():
                hole(x, y)
        major = n % 5 == 0 or n == 1
        f = big if major else small
        for y in (-18.55, 18.55):
            g.text((X(x), Y(y)), str(n), font=f, fill="#353b48" if major else "#7a8191", anchor="mm")
    lf = font(True, int(2.0 * PX))
    for l, y in LETTER.items():
        for x in (-80.4, 80.4):
            g.text((X(x), Y(y)), l, font=lf, fill="#353b48", anchor="mm")
    # rail stripes and signs
    for y, col in ((-26.0, "#3b6fe0"), (-19.75, "#e5484d"), (19.75, "#e5484d"), (26.0, "#3b6fe0")):
        g.rectangle([X(-79), Y(y) - 0.28 * PX, X(79), Y(y) + 0.28 * PX], fill=col)
    sf = font(True, int(2.6 * PX))
    for x in (-80.6, 80.6):
        for y, s, col in ((-24.14, "-", "#3b6fe0"), (24.14, "-", "#3b6fe0"), (-21.6, "+", "#e5484d"), (21.6, "+", "#e5484d")):
            g.text((X(x), Y(y)), s, font=sf, fill=col, anchor="mm")
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, "breadboard.png"), optimize=True)
    print("breadboard.png", img.size)


if __name__ == "__main__":
    breadboard()
