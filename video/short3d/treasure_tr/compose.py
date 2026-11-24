"""2D layer of the Turkish treasure-detector Short on top of the Blender frames -> build/picture.mp4 (no sound).

    .venv/Scripts/python video/short3d/treasure_tr/compose.py                 # whole Short
    .venv/Scripts/python video/short3d/treasure_tr/compose.py --at 1.5,12,30   # stills -> build/comp_stills/

Per frame: part labels (build montage), sound-wave rings at the buzzer on every buzzer beep (video/b3d/overlay.py
waves(), one ring per Geiger tick, coloured cold blue -> hot red), word-timed Turkish captions, Turkish on-screen
text per shot (hook title, heat meter, HAZİNE! + confetti, how-it-works cards, CTA with a follow button).
Shorts safe area: nothing in the bottom 18 % (y > 1574) or the right 12 % (x > 950).
"""
import json
import math
import os
import random
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import overlay  # noqa: E402
import story as S  # noqa: E402

B = os.path.join(HERE, "build")
W, H, FPS = 1080, 1920, S.FPS
SAFE_L, SAFE_R, SAFE_B = 60, 948, 1574
CX = (SAFE_L + SAFE_R) // 2
FD = "C:/Windows/Fonts/"
AMBER, TEAL, WHITE, INK, RED, GREEN, GOLD = "#ffb547", "#2dd4bf", "#ffffff", "#0b1220", "#ff4d5e", "#3ddc84", "#ffc531"
# one ring per Geiger tick, cold -> hot (colour, life s, radius px, stagger s: > life so only one ring)
overlay.WAVE.update({"tick0": ("#5b9cff", 0.42, 125, 9), "tick1": ("#8f7bff", 0.42, 125, 9), "tick2": ("#c86bff", 0.42, 125, 9),
                     "tick3": ("#ff5d8f", 0.42, 125, 9), "tick4": ("#ff3b3b", 0.42, 125, 9)})
_F = {}


def font(name, size):
    k = (name, int(size))
    if k not in _F:
        _F[k] = ImageFont.truetype(FD + name, max(4, int(size)))
    return _F[k]


DISP, UI, MONO, SYM = "seguibl.ttf", "segoeuib.ttf", "consolab.ttf", "seguisym.ttf"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(h, a=1.0):
    return rgb(h) + (int(255 * max(0.0, min(1.0, a))),)


def mixc(a, b, u):
    a, b = rgb(a), rgb(b)
    return "#%02x%02x%02x" % tuple(int(x + (y - x) * u) for x, y in zip(a, b))


def heat_col(heat):
    u = heat / 255
    return mixc("#5b9cff", "#c86bff", u * 2) if u < 0.5 else mixc("#c86bff", "#ff3b3b", u * 2 - 1)


def ease_back(u):
    u = max(0.0, min(1.0, u))
    return 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2


def appear(t, t0, t1=1e9, ramp=0.22):
    """(alpha, pop scale) of an element shown from t0 to t1"""
    a = S.smooth((t - t0) / ramp) * (1 - S.smooth((t - t1) / ramp))
    return a, 0.6 + 0.4 * ease_back((t - t0) / 0.3)


def text(d, xy, s, f, fill, a=1.0, anchor="mm", stroke=6, sfill=INK):
    if a <= 0.01:
        return
    d.text(xy, s, font=f, fill=rgba(fill, a), anchor=anchor, stroke_width=stroke, stroke_fill=rgba(sfill, a * 0.9))


def pill(d, cx, cy, s, f, fg, bg, a=1.0, pad=(30, 14), outline=None):
    if a <= 0.01:
        return 0
    tw = d.textlength(s, font=f)
    h = f.size + 2 * pad[1]
    box = [cx - tw / 2 - pad[0], cy - h / 2, cx + tw / 2 + pad[0], cy + h / 2]
    d.rounded_rectangle(box, radius=h / 2, fill=rgba(bg, a * 0.94), outline=rgba(outline, a) if outline else None,
                        width=4 if outline else 0)
    d.text((cx, cy + 1), s, font=f, fill=rgba(fg, a), anchor="mm")
    return box[2] - box[0]


def panel(d, box, a, outline="#2b3a5c", fill=(14, 21, 38)):
    d.rounded_rectangle(box, radius=30, fill=fill + (int(232 * a),), outline=rgba(outline, a), width=4)


def star(d, cx, cy, r, col, a=1.0):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=rgba(col, a), outline=rgba(INK, a))


class AD:
    """ImageDraw proxy for an RGBA frame that really blends: Pillow replaces pixels when a shape is drawn on an
    RGBA image and ignores the alpha of a text fill, so every translucent primitive is drawn on its own small
    layer and alpha-composited (text: drawn opaque, then its layer alpha is scaled)."""

    def __init__(self, img):
        self.img, self.d = img, ImageDraw.Draw(img)

    def textlength(self, *a, **k):
        return self.d.textlength(*a, **k)

    @staticmethod
    def _a(*cols):
        al = [c[3] for c in cols if isinstance(c, tuple) and len(c) == 4]
        return min(al) if al else 255

    def _layer(self, pts, pad, draw):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, y0 = int(min(xs) - pad), int(min(ys) - pad)
        x1, y1 = int(max(xs) + pad) + 1, int(max(ys) + pad) + 1
        if x1 <= 0 or y1 <= 0 or x0 >= self.img.width or y0 >= self.img.height:
            return None
        lay = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(lay), x0, y0)
        return lay, x0, y0

    def _paste(self, res, scale=None):
        if not res:
            return
        lay, x0, y0 = res
        if scale is not None and scale < 255:
            lay.putalpha(lay.getchannel("A").point(lambda v: v * scale // 255))
        sx, sy = max(0, -x0), max(0, -y0)
        if sx or sy:
            lay = lay.crop((sx, sy, lay.width, lay.height))
        self.img.alpha_composite(lay, (max(0, x0), max(0, y0)))

    def _shape(self, name, pts_arg, pts, kw, pad=12):
        if self._a(kw.get("fill"), kw.get("outline")) >= 255:
            return getattr(self.d, name)(pts_arg, **kw)
        def dr(dd, x0, y0):
            sh = [(p[0] - x0, p[1] - y0) for p in pts]
            arg = [c for p in sh for c in p] if name in ("rounded_rectangle", "rectangle", "ellipse") else sh
            getattr(dd, name)(arg, **kw)
        self._paste(self._layer(pts, pad + kw.get("width", 0), dr))

    def rounded_rectangle(self, box, **kw):
        self._shape("rounded_rectangle", box, [(box[0], box[1]), (box[2], box[3])], kw)

    def rectangle(self, box, **kw):
        self._shape("rectangle", box, [(box[0], box[1]), (box[2], box[3])], kw)

    def ellipse(self, box, **kw):
        self._shape("ellipse", box, [(box[0], box[1]), (box[2], box[3])], kw)

    def line(self, pts, **kw):
        self._shape("line", pts, [tuple(p) for p in pts], kw)

    def polygon(self, pts, **kw):
        self._shape("polygon", pts, [tuple(p) for p in pts], kw)

    def text(self, xy, s, **kw):
        a = self._a(kw.get("fill"), kw.get("stroke_fill") if kw.get("stroke_width") else None)
        if a >= 255:
            return self.d.text(xy, s, **kw)
        if a <= 2:
            return
        k2 = dict(kw)
        for key in ("fill", "stroke_fill"):
            if isinstance(k2.get(key), tuple) and len(k2[key]) == 4:
                k2[key] = k2[key][:3] + (255,)
        bb = self.d.textbbox(xy, s, **{k: v for k, v in k2.items() if k in ("font", "anchor", "stroke_width")})
        def dr(dd, x0, y0):
            dd.text((xy[0] - x0, xy[1] - y0), s, **k2)
        self._paste(self._layer([(bb[0], bb[1]), (bb[2], bb[3])], 6, dr), a)


# ------------------------------------------------------------------ captions
def build_captions(st):
    caps = []
    for ln in st.sched["lines"]:
        shown = ln["show"].split()
        n, m = len(shown), len(ln["words"])
        wt = [ln["words"][min(m - 1, round(j * m / n))]["t"] for j in range(n)]
        chunk = []

        def flush():
            if chunk:
                caps.append({"words": list(chunk), "t0": chunk[0][1]})
            chunk.clear()
        for j, w in enumerate(shown):
            chunk.append((w, wt[j]))
            ln_len = len(" ".join(c[0] for c in chunk))
            if ln_len >= 15 or w[-1] in ".!?,:" or len(chunk) >= 3:
                flush()
        flush()
        caps[-1]["end"] = ln["t1"] + 0.15
    for i, c in enumerate(caps):
        c["t1"] = c.get("end", caps[i + 1]["t0"] if i + 1 < len(caps) else st.dur)
    return caps


def draw_caption(d, caps, t):
    c = next((x for x in caps if x["t0"] - 0.05 <= t < x["t1"]), None)
    if not c:
        return
    size = 88
    f = font(DISP, size)
    words = [w for w, _ in c["words"]]
    while d.textlength(" ".join(words), font=f) > SAFE_R - SAFE_L - 40 and size > 56:
        size -= 4
        f = font(DISP, size)
    total = d.textlength(" ".join(words), font=f)
    x = CX - total / 2
    y = 1488
    k = (t - c["t0"]) / 0.12
    for i, (w, wt) in enumerate(c["words"]):
        nxt = c["words"][i + 1][1] if i + 1 < len(c["words"]) else 1e9
        now = wt <= t < nxt
        col = AMBER if now else (WHITE if t >= wt else "#dfe6f2")
        yy = y - (6 if now else 0) + (1 - min(1.0, max(0.0, k))) * 18
        d.text((x, yy), w, font=f, fill=rgba(col, 1.0), anchor="lm", stroke_width=9, stroke_fill=rgba(INK, 0.95))
        x += d.textlength(w + " ", font=f)


# ------------------------------------------------------------------ per-shot on-screen text
def tags_draw(d, tags):
    """part labels (same look as overlay.py's, but kept inside the Shorts safe area)"""
    boxes = []
    for tg in sorted(tags, key=lambda x: -x["b"][1]):
        on = tg["on"]
        a = (tg["a"][0] * W, tg["a"][1] * H)
        b = (tg["b"][0] * W, tg["b"][1] * H)
        f = font(UI, 36)
        tw = d.textlength(tg["text"], font=f)
        bw, bh = tw + 40, 36 + 24
        x0 = max(SAFE_L - 40, min(SAFE_R - bw, b[0] - bw / 2))
        y0 = max(150, b[1] - bh - 20)
        for _ in range(6):  # nudge up while it overlaps a label already placed
            hit = [bx for bx in boxes if x0 < bx[2] + 6 and x0 + bw > bx[0] - 6 and y0 < bx[3] + 6 and y0 + bh > bx[1] - 6]
            if not hit:
                break
            y0 = min(bx[1] for bx in hit) - bh - 8
        boxes.append((x0, y0, x0 + bw, y0 + bh))
        col = rgb(tg["color"])
        d.line([a, (x0 + bw / 2, y0 + bh)], fill=col + (int(220 * on),), width=4)
        d.ellipse([a[0] - 6, a[1] - 6, a[0] + 6, a[1] + 6], fill=col + (int(255 * on),))
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=bh * 0.3, fill=(11, 18, 32, int(225 * on)), outline=col + (int(255 * on),), width=3)
        d.text((x0 + bw / 2, y0 + bh / 2 + 1), tg["text"], font=f, fill=col + (int(255 * on),), anchor="mm")


def heat_hud(d, st, t, a):
    sec = S.SECRET1
    heat, dist = S.heat_of(st.knob(t), sec)
    word = S.HEAT_WORD_TR[S.word_for(heat)]
    col = heat_col(heat)
    panel(d, [CX - 330, 170, CX + 330, 420], a, outline=col)
    shake = (math.sin(t * 60) * 4 if heat >= 230 else 0)
    text(d, (CX + shake, 255), word, font(DISP, 104), col, a, stroke=7)
    n = S.amap(heat, 0, 255, 0, 12)
    x0 = CX - 270
    for i in range(12):
        c = heat_col(i * 255 / 11) if i < n else "#25324d"
        d.rounded_rectangle([x0 + i * 46, 345, x0 + i * 46 + 38, 390], radius=8, fill=rgba(c, a))


CONF = [(random.Random(i).uniform(-1, 1), random.Random(i * 7 + 1).uniform(0.4, 1.0), random.Random(i * 13 + 2).uniform(0, 6.28),
         ["#ffb547", "#2dd4bf", "#ff4d5e", "#5b9cff", "#ffffff", "#ffc531"][i % 6]) for i in range(110)]


def confetti(d, t, t0, cx=540, cy=520):
    u = t - t0
    if not 0 <= u <= 2.6:
        return
    a = 1 - S.smooth((u - 2.0) / 0.6)
    for vx, vy, ph, col in CONF:
        x = cx + vx * 900 * u
        y = cy - vy * 1500 * u + 1900 * u * u
        if not (0 <= x <= SAFE_R and 120 <= y <= 1500):
            continue
        r = 14
        ang = ph + u * 9
        pts = [(x + r * math.cos(ang + k * math.pi / 2) * (1 if k % 2 else 0.45), y + r * math.sin(ang + k * math.pi / 2) * (1 if k % 2 else 0.45)) for k in range(4)]
        d.polygon(pts, fill=rgba(col, a))


def found_banner(d, st, t, t0, a_end=1e9):
    a, sc = appear(t, t0, a_end)
    if a <= 0.01:
        return
    text(d, (CX, 290), "HAZİNE!", font(DISP, int(150 * sc)), GOLD, a, stroke=10)
    pill(d, CX, 440, "12,4 sn  ·  YENİ REKOR", font(UI, 50), INK, GOLD, a * S.smooth((t - t0 - 0.25) / 0.2))


def code_card(d, lines, top, a, title=None):
    if a <= 0.01:
        return
    f = font(MONO, 44)
    w = max(d.textlength(s, font=f) for s, _ in lines) + 80
    h = len(lines) * 64 + 50 + (44 if title else 0)
    box = [CX - w / 2, top, CX + w / 2, top + h]
    panel(d, box, a)
    y = top + 30
    if title:
        d.text((box[0] + 40, y + 8), title, font=font(UI, 30), fill=rgba(TEAL, a), anchor="lm")
        y += 44
    for s, col in lines:
        d.text((box[0] + 40, y + 30), s, font=f, fill=rgba(col, a), anchor="lm")
        y += 64


def bubble_at(d, anc, s, col, a, size=64, dy=-150, dx=-150, label=None):
    if not anc or a <= 0.01:
        return
    ax, ay = anc[0] * W, anc[1] * H
    bx = max(SAFE_L + 120, min(SAFE_R - 120, ax + dx))
    by = max(300, ay + dy)
    d.line([(ax, ay), (bx, by)], fill=rgba(col, a * 0.9), width=5)
    d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=rgba(col, a))
    f = font(DISP, size)
    tw = max(d.textlength(s, font=f), d.textlength(label, font=font(UI, 28)) - 30 if label else 0)
    hh = size + 36 + (34 if label else 0)
    box = [bx - tw / 2 - 34, by - hh / 2, bx + tw / 2 + 34, by + hh / 2]
    d.rounded_rectangle(box, radius=26, fill=(11, 18, 32, int(235 * a)), outline=rgba(col, a), width=4)
    if label:
        d.text((bx, box[1] + 30), label, font=font(UI, 28), fill=rgba(TEAL, a), anchor="mm")
        d.text((bx, box[1] + 34 + (hh - 34) / 2), s, font=f, fill=rgba(col, a), anchor="mm")
    else:
        d.text((bx, by), s, font=f, fill=rgba(col, a), anchor="mm")


def number_line(d, st, t, a):
    if a <= 0.01:
        return
    panel(d, [SAFE_L + 10, 170, SAFE_R - 10, 480], a)
    x0, x1, y = SAFE_L + 80, SAFE_R - 80, 350
    X = lambda v: x0 + (x1 - x0) * v / 99  # noqa: E731
    d.rounded_rectangle([x0, y - 6, x1, y + 6], radius=6, fill=rgba("#3a4a6c", a))
    for v in (0, 50, 99):
        d.text((X(v), y + 46), str(v), font=font(UI, 34), fill=rgba("#9fb0cc", a), anchor="mm")
    sec = S.SECRET2
    pos = int(round(st.knob(t)))
    dist = abs(pos - sec)
    heat, _ = S.heat_of(pos, sec)
    lo, hi = sorted((X(pos), X(sec)))
    d.rectangle([lo, y - 6, hi, y + 6], fill=rgba(heat_col(heat), a))
    star(d, X(sec), y, 30, GOLD, a)
    d.text((X(sec), y + 88), "HAZİNE", font=font(UI, 30), fill=rgba(GOLD, a), anchor="mm")  # below: never hits SAYI
    d.polygon([(X(pos) - 20, y - 46), (X(pos) + 20, y - 46), (X(pos), y - 12)], fill=rgba(AMBER, a))
    d.text((X(pos), y - 70), f"SAYI {pos}", font=font(UI, 30), fill=rgba(AMBER, a), anchor="mm")
    text(d, (CX, 222), f"uzaklık = {min(dist, 50)}" + ("+" if dist > 50 else ""), font(DISP, 58), heat_col(heat), a, stroke=5)


def check(d, cx, cy, r, col, a):
    d.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.8)], fill=rgba(col, a), width=max(3, int(r / 3)), joint="curve")


def follow(img, d, st, t, a):
    """CTA card: channel row + a big follow button; a touch dot taps it on 'takip'"""
    if a <= 0.01:
        return
    tap = st.w("l12", "takip") + 0.1
    panel(d, [SAFE_L + 10, 160, SAFE_R - 10, 700], a, outline=AMBER)
    text(d, (CX, 240), "Böyle projeler yapmayı", font(DISP, 60), WHITE, a, stroke=0)
    text(d, (CX, 312), "öğrenmek istiyor musun?", font(DISP, 60), AMBER, a, stroke=0)
    lx, ly = CX - 230, 445
    if a > 0.5:
        av = LOGO.resize((110, 110))
        m = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(m).ellipse([0, 0, 109, 109], fill=255)
        img.paste(av, (int(lx), ly - 55), m)
    d.text((lx + 135, ly - 18), "Pin by Pin Lab", font=font(UI, 48), fill=rgba(WHITE, a), anchor="lm")
    d.text((lx + 135, ly + 30), "ESP32, sıfırdan", font=font(UI, 32), fill=rgba("#9fb0cc", a), anchor="lm")
    done = t >= tap + 0.08
    press = 1 - 0.08 * math.exp(-((t - tap - 0.04) / 0.07) ** 2)
    bw, bh, by = 470 * press, 100 * press, 600
    box = [CX - bw / 2, by - bh / 2, CX + bw / 2, by + bh / 2]
    d.rounded_rectangle(box, radius=bh / 2, fill=rgba("#3a4256" if done else "#ff2d3d", a))
    if done:
        check(d, CX - 150, by, 16, WHITE, a)
        d.text((CX + 22, by + 2), "TAKİPTESİN", font=font(UI, 44), fill=rgba(WHITE, a), anchor="mm")
        u = (t - tap - 0.08) / 0.6
        if 0 <= u <= 1:
            r = 70 * u
            d.rounded_rectangle([box[0] - r, box[1] - r * 0.4, box[2] + r, box[3] + r * 0.4], radius=bh / 2 + r * 0.4,
                                outline=rgba("#ff2d3d", a * (1 - u)), width=6)
    else:
        d.text((CX, by + 2), "TAKİP ET", font=font(UI, 48), fill=rgba(WHITE, a), anchor="mm")
    if tap - 0.8 <= t <= tap + 0.7:  # touch dot flies in and taps
        u = S.smooth((t - (tap - 0.8)) / 0.75)
        fx, fy = CX + 120 + 200 * (1 - u), by + 20 + 300 * (1 - u)
        fa = a * (1 - S.smooth((t - tap - 0.3) / 0.35))
        r = 34 - 10 * math.exp(-((t - tap) / 0.08) ** 2)
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=rgba(WHITE, 0.55 * fa), outline=rgba(WHITE, fa), width=5)


LOGO = Image.open(os.path.join(HERE, "..", "..", "..", "brand", "export", "profile_800.png")).convert("RGB")


def ui(img, d, st, t, anc, caps):
    sh = st.shot_at(t)
    sid = sh["id"]
    if sid == "hook":
        a, sc = appear(t, 0.15, sh["end"] - 0.15)
        pill(d, CX, 190, "ESP32 PROJESİ", font(UI, 40), INK, AMBER, a)
        text(d, (CX, 300), "HAZİNE", font(DISP, int(118 * sc)), WHITE, a, stroke=9)
        text(d, (CX, 420), "DEDEKTÖRÜ 2.0", font(DISP, int(96 * sc)), AMBER, a, stroke=9)
        confetti(d, t, st.HOOK_PRESS, cy=1050)
    elif sid == "build":
        a, sc = appear(t, sh["start"] + 0.05, sh["end"] - 0.1)
        text(d, (CX, 230), "10. bölümün devresi", font(DISP, int(76 * sc)), WHITE, a, stroke=8)
        pill(d, CX, 340, "+ potansiyometre  + RGB LED", font(UI, 42), INK, TEAL, a * S.smooth((t - st.DROP["pot"]) / 0.25))
    elif sid == "hunt":
        if t < st.PRESS_FOUND:
            heat_hud(d, st, t, appear(t, st.t0("l04") - 0.2, st.PRESS_FOUND - 0.05, 0.2)[0])
            a = S.fade(t, st.t0("l03") + 0.3, st.t1("l03") + 0.2, 0.2)
            bubble_at(d, anc.get("knob"), "?", GOLD, a, size=90, dy=-260, dx=-260, label="HAZİNE NEREDE")
        else:
            found_banner(d, st, t, st.PRESS_FOUND)
            confetti(d, t, st.PRESS_FOUND)
    elif sid == "found":
        found_banner(d, st, t, st.PRESS_FOUND, min(sh["end"] - 0.15, st.FOUND_END - 0.1))
        confetti(d, t, st.PRESS_FOUND)
    elif sid == "how_knob":
        a, _ = appear(t, sh["start"], sh["end"] - 0.1)
        pill(d, CX, 190, "NASIL ÇALIŞIYOR?", font(UI, 42), INK, TEAL, a)
        code_card(d, [("analogRead(34) → 0…4095", WHITE), ("map(…)         → 0…99", AMBER)], 260,
                  a * S.smooth((t - st.w("l08", "Düğme") + 0.1) / 0.25))
        bubble_at(d, anc.get("knob"), str(int(round(st.knob(t)))), AMBER, S.fade(t, st.w("l08", "Düğme"), sh["end"] - 0.1, 0.2),
                  size=96, dy=-170, dx=-300, label="SAYI")
    elif sid == "how_dist":
        a, _ = appear(t, sh["start"], sh["end"] - 0.1)
        number_line(d, st, t, a)
        code_card(d, [("uzaklik = abs(sayi - hazine);", WHITE)], 500, a * S.smooth((t - st.w("l09", "uzaklığını")) / 0.25))
    elif sid == "how_dig":
        a, _ = appear(t, sh["start"], sh["end"] - 0.1)
        hit = t >= st.PRESS_EMPTY
        panel(d, [SAFE_L + 30, 170, SAFE_R - 30, 430], a)
        text(d, (CX, 230), "KAZ! basınca", font(DISP, 54), AMBER, a, stroke=0)
        text(d, (CX, 310), "uzaklık ≤ 2  →  HAZİNE!", font(UI, 46), GREEN, a * (0.45 if hit else 1.0), stroke=0)
        sh_x = math.sin(t * 70) * 8 * math.exp(-max(0.0, t - st.PRESS_EMPTY) * 5) if hit else 0
        text(d, (CX + sh_x, 380), "değilse  →  BOŞ!", font(UI, 46 if not hit else 52), RED, a, stroke=0)
    elif sid == "how_save":
        a, _ = appear(t, sh["start"], sh["end"] - 0.1)
        off = st.UNPLUG + 0.1 <= t < st.REBOOT + 0.1
        pill(d, CX, 200, "FİŞ ÇEKİLDİ" if off else ("REKOR HÂLÂ 12,4 sn ✓" if t >= st.REBOOT else "Preferences = kalıcı hafıza"),
             font(UI, 44), INK, RED if off else (GREEN if t >= st.REBOOT else TEAL), a)
    else:  # cta
        a, _ = appear(t, sh["start"] + 0.05, 1e9)
        follow(img, d, st, t, a)
        ac = S.smooth((t - st.t0("l13") + 0.1) / 0.25)
        pill(d, CX, 1270, "Kodun tamamı açıklamada ↓", font(UI, 46), INK, AMBER, ac)
    if not os.environ.get("NOCAP"):  # NOCAP=1: stills without captions (thumbnail)
        draw_caption(d, caps, t)


# ------------------------------------------------------------------ frames
def job(g):
    st = STORY
    t = g / FPS
    sh = st.shot_at(t)
    f = g - sh["F0"] + 1
    d0 = os.path.join(B, "shots", sh["id"])
    src = os.path.join(d0, f"f_{f:04d}.png")
    if not os.path.exists(src):
        have = sorted(x for x in os.listdir(d0) if x.startswith("f_")) if os.path.isdir(d0) else []
        src = os.path.join(d0, have[-1]) if have else None
    img = Image.open(src).convert("RGB") if src else Image.new("RGB", (W, H), (11, 18, 32))
    anc = ANCH.get(sh["id"], {}).get(str(f), {})
    waves = []
    bp = anc.get("buzzer")
    if bp:
        for tb, kind in WAVES:
            age = t - tb
            life = overlay.WAVE[kind][1] if kind.startswith("tick") else 1.2
            if 0 <= age <= life:
                waves.append({"x": bp[0], "y": bp[1], "age": round(age, 3), "kind": kind})
    img = overlay.draw(img, [], waves)
    img = img.convert("RGBA")
    d = AD(img)
    tags_draw(d, anc.get("tags", []))
    ui(img, d, st, t, anc, CAPS)
    return img.convert("RGB").tobytes()


def init():
    global STORY, ANCH, WAVES, CAPS
    STORY = S.Story()
    ANCH = {}
    for sh in STORY.shots:
        p = os.path.join(B, "shots", sh["id"], "anchors.json")
        if os.path.exists(p):
            ANCH[sh["id"]] = json.load(open(p))["frames"]
    WAVES = STORY.waves()
    CAPS = build_captions(STORY)


def main():
    init()
    if "--thumb" in sys.argv:  # build/thumb.jpg: one frame without captions
        os.environ["NOCAP"] = "1"
        g = round(float(sys.argv[sys.argv.index("--thumb") + 1]) * FPS)
        Image.frombytes("RGB", (W, H), job(g)).save(os.path.join(B, "thumb.jpg"), quality=92)
        return
    if "--at" in sys.argv:
        out = os.path.join(B, "comp_stills")
        os.makedirs(out, exist_ok=True)
        for x in sys.argv[sys.argv.index("--at") + 1].split(","):
            g = round(float(x) * FPS)
            Image.frombytes("RGB", (W, H), job(g)).save(os.path.join(out, f"c_{float(x):06.2f}.png"))
        return
    n = STORY.nframes()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                            os.path.join(B, "picture.mp4")], stdin=subprocess.PIPE)
    with ProcessPoolExecutor(int(os.environ.get("COMPOSE_WORKERS", "2")), initializer=init) as ex:  # 2: the 16 GB PC runs other jobs too
        # bounded windows: ex.map over all frames would queue every finished frame (6 MB each) in memory
        # whenever the encoder is slower than the workers (that ran the PC out of memory, 2026-11-24)
        for w0 in range(0, n, 24):
            for fr in ex.map(job, range(w0, min(n, w0 + 24)), chunksize=3):
                enc.stdin.write(fr)
            if w0 % 240 == 0:
                print("compose", w0, "/", n, flush=True)
    enc.stdin.close()
    enc.wait()
    print("picture.mp4", n, "frames")


if __name__ == "__main__":
    main()
