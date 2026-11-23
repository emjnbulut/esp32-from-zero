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


WAVE = {"hi": ("#ffd166", 0.50, 150, 0.08), "lo": ("#ff8a5b", 0.80, 210, 0.16)}  # colour, life s, radius px, stagger s


def waves(g, W, H, items):
    """sound-wave bursts around the buzzer (creator 2026-11-24: beeps must be visible, not only heard).
    items: [{"x", "y" (0..1), "age" (s since the beep), "kind": hi|lo}] -> 3 expanding glowing rings each."""
    for it in items:
        col, life, rad, stag = WAVE.get(it["kind"], WAVE["hi"])
        c = rgb(col)
        cx, cy = it["x"] * W * SS, it["y"] * H * SS
        for i in range(3):
            u = (it["age"] - i * stag) / life
            if not 0 <= u <= 1:
                continue
            r = (18 + rad * u ** 0.7) * SS
            a = (1 - u) ** 1.4
            for wdt, al in ((14, 0.22), (5, 0.95)):  # soft glow, then the bright ring
                g.ellipse([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], outline=c + (int(255 * a * al),),
                          width=int(wdt * SS * (1 - 0.5 * u)))


def draw(img, tags, wav=()):
    if not tags and not wav:
        return img
    W, H = img.size
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    g = ImageDraw.Draw(layer)
    waves(g, W, H, wav)
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
    src, dst, tags, wav = (*job, ())[:4]
    draw(Image.open(src), tags, wav).save(dst)
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
        wp = os.path.join(os.path.dirname(ovp), "waves.json")  # optional, written by assemble.py
        wv = json.load(open(wp)) if os.path.exists(wp) else {}
        jobs = [(os.path.join(frames, fn), os.path.join(out, fn), ov.get(str(int(fn[2:6])), []),
                 wv.get(str(int(fn[2:6])), []))
                for fn in sorted(os.listdir(frames)) if fn.startswith("f_") and fn.endswith(".png")]
    with ProcessPoolExecutor(4) as ex:  # 4, not 6: the 16 GB PC ran out of memory with other jobs (2026-11-24)
        n = sum(1 for _ in ex.map(one, jobs, chunksize=8))
    print(n, "frames")


if __name__ == "__main__":
    main()
