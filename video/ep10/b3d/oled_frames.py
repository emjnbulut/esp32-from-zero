"""OLED screen frames for the Ep10 Blender pilot (128x64 monochrome, drawn like the real SSD1306).

    .venv/Scripts/python video/ep10/b3d/oled_frames.py   -> video/ep10/b3d/build/oled/s_0001.png ...

Timeline (seconds) is shared with pilot.py through TIMES below.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build", "oled")
FPS, DUR = 30, 9.0
T = json.load(open(os.path.join(HERE, "times.json")))
SCALE = 8
ON = (232, 246, 255)


def f(size, bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/" + ("consolab.ttf" if bold else "consola.ttf"), size)


F_SMALL, F_MID, F_BIG, F_HUGE = f(10), f(14), f(24), f(34)


def screen(t):
    img = Image.new("1", (128, 64), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    go, react = T["go"], T["react"]
    ms = round((react - go) * 1000)
    if T["unplug"] <= t < T["plug"] + 0.25:
        return img  # power off
    if t >= T["plug"] + 0.25:
        if t < T["plug"] + 0.75:  # boot splash
            d.text((64, 26), "PIN BY PIN", font=F_MID, fill=1, anchor="mm")
            d.text((64, 44), "booting...", font=F_SMALL, fill=1, anchor="mm")
            return img
        d.text((2, 1), "REFLEX 2.0", font=F_SMALL, fill=1)
        d.line((0, 13, 127, 13), fill=1)
        d.text((64, 24), "BEST", font=F_MID, fill=1, anchor="mm")
        d.text((64, 46), f"{ms} ms", font=F_BIG, fill=1, anchor="mm")
        if int(t * 2) % 2 == 0:
            d.text((64, 61), "press to play", font=F_SMALL, fill=1, anchor="mb")
        return img
    if t < go:
        d.text((2, 1), "REFLEX 2.0", font=F_SMALL, fill=1)
        d.text((126, 1), "BEST 231", font=F_SMALL, fill=1, anchor="ra")
        d.line((0, 13, 127, 13), fill=1)
        dots = "." * (1 + int(t * 3) % 3)
        d.text((64, 36), "WAIT" + dots.ljust(3), font=F_BIG, fill=1, anchor="mm")
        d.rectangle((14, 54, 114, 59), outline=1)
        k = min(1.0, t / go)
        d.rectangle((16, 56, 16 + int(96 * k), 57), fill=1)
        return img
    if t < react:
        d.rectangle((0, 0, 127, 63), fill=1)
        d.text((64, 33), "GO!", font=F_HUGE, fill=0, anchor="mm")
        return img
    # result: count up quickly, then NEW RECORD blinking
    k = min(1.0, (t - react) / 0.35)
    shown = int(ms * (1 - (1 - k) ** 3))
    d.text((64, 36), f"{shown} ms", font=F_BIG, fill=1, anchor="mm")
    if t >= T["record"]:
        if int((t - T["record"]) / 0.18) % 2 == 0:
            d.rectangle((6, 0, 121, 15), fill=1)
            d.text((64, 8), "NEW RECORD!", font=F_MID, fill=0, anchor="mm")
        d.text((64, 61), "saved", font=F_SMALL, fill=1, anchor="mb")
    else:
        d.text((64, 8), "your time", font=F_SMALL, fill=1, anchor="mm")
    return img


def upscale(img):
    big = img.convert("L").resize((128 * SCALE, 64 * SCALE), Image.NEAREST)
    out = Image.new("RGB", big.size, (0, 0, 0))
    px = big.load()
    o = out.load()
    for y in range(big.size[1]):
        gy = (y % SCALE) == SCALE - 1
        for x in range(big.size[0]):
            if px[x, y] and not gy and (x % SCALE) != SCALE - 1:
                o[x, y] = ON
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    n = int(FPS * DUR)
    cache = {}
    for i in range(n):
        t = i / FPS
        s = screen(t)
        key = s.tobytes()
        if key not in cache:
            cache[key] = upscale(s)
        cache[key].save(os.path.join(OUT, f"s_{i + 1:04d}.png"))
    print(n, "frames,", len(cache), "unique")


if __name__ == "__main__":
    main()
