"""Crisp 2D labels over Blender frames, from the projected tag points the scene script exports.

    .venv/Scripts/python video/b3d/overlay.py <frames dir> <overlay.json> <out dir>
    .venv/Scripts/python video/b3d/overlay.py --stills <stills dir>      (uses <shot>_overlay.json next to the stills)

Label = rounded dark box with coloured text, a leader line down to the hole, drawn at 2x and downsampled.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/segoeuib.ttf"
SS = 2  # supersampling


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw(img, tags):
    if not tags:
        return img
    W, H = img.size
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    g = ImageDraw.Draw(layer)
    boxes = []
    for tg in sorted(tags, key=lambda x: x["b"][1]):
        on = max(0.0, min(1.0, tg["on"]))
        a = (tg["a"][0] * W * SS, tg["a"][1] * H * SS)
        b = (tg["b"][0] * W * SS, tg["b"][1] * H * SS)
        size = int(36 * SS * max(0.7, min(1.4, tg.get("scale", 1.0))))
        f = ImageFont.truetype(FONT, size)
        tw = g.textlength(tg["text"], font=f)
        pad_x, pad_y = size * 0.55, size * 0.32
        bw, bh = tw + 2 * pad_x, size + 2 * pad_y
        x0, y0 = b[0] - bw / 2, b[1] - bh
        for (px0, py0, px1, py1) in boxes:  # nudge up when two labels overlap
            if x0 < px1 and x0 + bw > px0 and y0 < py1 and y0 + bh > py0:
                y0 = py0 - bh - 6 * SS
        x0 = max(8 * SS, min(W * SS - bw - 8 * SS, x0))
        y0 = max(8 * SS, y0)
        boxes.append((x0, y0, x0 + bw, y0 + bh))
        col = rgb(tg["color"])
        al = int(255 * on)
        g.line([a, (x0 + bw / 2, y0 + bh)], fill=col + (int(220 * on),), width=3 * SS)
        g.ellipse([a[0] - 5 * SS, a[1] - 5 * SS, a[0] + 5 * SS, a[1] + 5 * SS], fill=col + (al,))
        g.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=bh * 0.3, fill=(11, 18, 32, int(225 * on)),
                            outline=col + (al,), width=2 * SS)
        g.text((x0 + pad_x, y0 + pad_y + size * 0.02), tg["text"], font=f, fill=col + (al,))
    layer = layer.resize((W, H), Image.LANCZOS)
    out = img.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def one(job):
    src, dst, tags = job
    draw(Image.open(src), tags).save(dst)
    return dst


def main():
    if sys.argv[1] == "--stills":
        d = sys.argv[2]
        jobs = []
        for fn in os.listdir(d):
            if fn.endswith("_overlay.json"):
                sid = fn[:-13]
                ov = json.load(open(os.path.join(d, fn)))
                for f, tags in ov.items():
                    src = os.path.join(d, f"{sid}_f_{int(f):04d}.png")
                    if os.path.exists(src):
                        jobs.append((src, os.path.join(d, f"{sid}_f_{int(f):04d}_ov.png"), tags))
    else:
        frames, ovp, out = sys.argv[1:4]
        os.makedirs(out, exist_ok=True)
        ov = json.load(open(ovp))
        jobs = [(os.path.join(frames, fn), os.path.join(out, fn), ov.get(str(int(fn[2:6])), []))
                for fn in sorted(os.listdir(frames)) if fn.startswith("f_") and fn.endswith(".png")]
    with ProcessPoolExecutor(6) as ex:
        n = sum(1 for _ in ex.map(one, jobs, chunksize=8))
    print(n, "frames")


if __name__ == "__main__":
    main()
