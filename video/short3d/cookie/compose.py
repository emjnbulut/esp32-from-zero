"""2D layer of the cookie-jar-guard Short (EN or TR) on top of the Blender frames -> build/<lang>/picture.mp4 (no sound).

    .venv/Scripts/python video/short3d/cookie/compose.py --lang en                # whole Short
    .venv/Scripts/python video/short3d/cookie/compose.py --lang tr --at 1.5,12    # stills -> build/tr/comp_stills/
    .venv/Scripts/python video/short3d/cookie/compose.py --lang en --thumb 1.85    # build/thumb_en.jpg (no captions)

Per frame: sound-wave rings at the buzzer on every buzzer tone (video/b3d/overlay.py waves(): countdown tick =
tone(2000, 30), siren 1800 / 2600 Hz every 250 ms), a red edge glow while the siren plays, part labels, word-timed
captions in the Short's language, on-screen text per shot (hook title + INTRUDER, countdown HUD, CAUGHT!, 2 min ago,
HOW IT WORKS: PIR / YES! / parking ticket + lastMotion = now, the whole guard, CTA follow card).
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

W, H, FPS = 1080, 1920, S.FPS
SAFE_L, SAFE_R, SAFE_B = 60, 948, 1574
CX = (SAFE_L + SAFE_R) // 2
FD = "C:/Windows/Fonts/"
AMBER, TEAL, WHITE, INK, RED, GREEN, GOLD = "#ffb547", "#2dd4bf", "#ffffff", "#0b1220", "#ff4d5e", "#3ddc84", "#ffc531"
# countdown tick (2000 Hz, 30 ms), siren 1800 Hz (lo) / 2600 Hz (hi): colour, life s, radius px, stagger s
overlay.WAVE.update({"tick": ("#7fe8de", 0.45, 190, 0.07), "lo": ("#ff5a4f", 0.60, 250, 0.09),
                     "hi": ("#ffc531", 0.60, 290, 0.09)})
LANG = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else os.environ.get("COOKIE_LANG", "en")
os.environ["COOKIE_LANG"] = LANG
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
    if anchor == "mm" and f.path.endswith(DISP):  # big display lines (TR words run long): shrink to the safe width
        maxw = SAFE_R - SAFE_L - 20
        while f.size > 40 and d.textlength(s, font=f) + 2 * stroke > maxw:
            f = font(DISP, f.size - 4)
    d.text(xy, s, font=f, fill=rgba(fill, a), anchor=anchor, stroke_width=stroke, stroke_fill=rgba(sfill, a * 0.9))


def pill(d, cx, cy, s, f, fg, bg, a=1.0, pad=(30, 14), outline=None):
    if a <= 0.01:
        return 0
    tick = s.endswith(" ✓")  # Segoe UI has no check mark glyph: drawn as lines
    s = s[:-2] if tick else s
    ck = f.size * 0.9 if tick else 0
    tw = d.textlength(s, font=f) + ck
    h = f.size + 2 * pad[1]
    box = [cx - tw / 2 - pad[0], cy - h / 2, cx + tw / 2 + pad[0], cy + h / 2]
    d.rounded_rectangle(box, radius=h / 2, fill=rgba(bg, a * 0.94), outline=rgba(outline, a) if outline else None,
                        width=4 if outline else 0)
    d.text((cx - ck / 2, cy + 1), s, font=f, fill=rgba(fg, a), anchor="mm")
    if tick:
        r = f.size * 0.3
        x = cx + tw / 2 - r - 2
        d.line([(x - r, cy), (x - r * 0.3, cy + r * 0.7), (x + r, cy - r * 0.8)], fill=rgba(fg, a), width=max(3, int(r / 2.5)),
               joint="curve")
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
        # "show" is a caption only when it re-spells the spoken line (TR "E Se Pe otuz iki" -> "ESP32"); a short
        # "show" (hook title, CAUGHT!, the CTA headline) is on-screen text, and the caption follows the narration
        src = ln["show"] if len(ln["show"].split()) >= 0.7 * len(ln["text"].split()) else ln["text"]
        shown = [w for w in src.split() if w not in ("-", "–")]
        n, m = len(shown), len(ln["words"])
        wt = [ln["words"][min(m - 1, round(j * m / n))]["t"] for j in range(n)]
        chunk = []

        def flush():
            if chunk:
                caps.append({"words": list(chunk), "t0": chunk[0][1]})
            chunk.clear()
        for j, w in enumerate(shown):
            if chunk and len(" ".join(c[0] for c in chunk) + " " + w) > 20:  # long Turkish words: keep the size up
                flush()
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



def check(d, cx, cy, r, col, a):
    d.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.8)], fill=rgba(col, a), width=max(3, int(r / 3)), joint="curve")





# ------------------------------------------------------------------ cookie-guard on-screen text (EN / TR)
TXT = {
    "en": {"badge": "ESP32 COOKIE GUARD", "title": ("Who's stealing", "my cookies?"), "intruder": "INTRUDER!",
           "arming": "ARMING", "leave": "leave the room!", "later": "10 s later · ARMED", "caught": "CAUGHT!",
           "back": "2 MIN LATER", "ago": "2 min ago", "how": "HOW IT WORKS", "pir": "PIR motion sensor",
           "yes": "YES!", "ticket": "TICKET #1", "seen": "motion seen at", "siren": "1800 / 2600 Hz · every 250 ms",
           "parts": "The whole guard", "head": ("Follow for", "more builds!"), "btn": "FOLLOW", "done": "FOLLOWING",
           "chan": "ESP32 From Zero", "comments": "What would you guard? ↓"},
    "tr": {"badge": "ESP32 KURABİYE BEKÇİSİ", "title": ("Kurabiyelerimi", "kim çalıyor?"), "intruder": "HIRSIZ VAR!",
           "arming": "KURULUYOR", "leave": "odadan çık!", "later": "10 sn sonra · KURULU", "caught": "YAKALANDIN!",
           "back": "2 DK SONRA", "ago": "2 dk önce", "how": "NASIL ÇALIŞIYOR?", "pir": "PIR hareket sensörü",
           "yes": "EVET!", "ticket": "BİLET #1", "seen": "hareket zamanı", "siren": "1800 / 2600 Hz · 250 ms'de bir",
           "parts": "Bütün bekçi bu", "head": ("Daha fazlası için", "takip et!"), "btn": "TAKİP ET", "done": "TAKİPTESİN",
           "chan": "ESP32, sıfırdan", "comments": "Sen neyi korurdun? ↓"},
}[LANG]
DIM = "#9fb0cc"
PAPER, INKP = "#f4ead2", "#3a2c1a"


def _vignette():
    """red edge glow for the siren (alpha mask, built once)"""
    m = Image.new("L", (W // 8, H // 8), 0)
    px_ = m.load()
    for y in range(H // 8):
        for x in range(W // 8):
            dx = abs(x / (W / 8) - 0.5) * 2
            dy = abs(y / (H / 8) - 0.5) * 2
            e = max(dx ** 3, dy ** 4)
            px_[x, y] = int(255 * min(1.0, e))
    return m.resize((W, H), Image.BILINEAR)


VIG = None


def siren_glow(img, st, t, t0, t1):
    """pulsing red edge while the siren plays (brighter on the 2600 Hz half)"""
    global VIG
    if not (t0 <= t < t1):
        return img
    if VIG is None:
        VIG = _vignette()
    i = int((t - t0) / S.SIREN_STEP)
    ph = ((t - t0) % S.SIREN_STEP) / S.SIREN_STEP
    k = (0.6 if i % 2 else 0.4) * (1 - 0.5 * ph) * S.smooth((t - t0) / 0.08)
    red = Image.new("RGBA", (W, H), (255, 40, 50, 0))
    red.putalpha(VIG.point(lambda v: int(v * k)))
    img.alpha_composite(red)
    return img


def countdown_hud(d, st, t, a):
    """the arm shot: 'leave the room!' with the seconds left, a tick ring per second"""
    if a <= 0.01:
        return
    left = st.countdown_left(t)
    panel(d, [CX - 300, 170, CX + 300, 470], a, outline=TEAL if left else "#2b3a5c")
    if left is None:
        text(d, (CX, 230), TXT["arming"], font(UI, 40), DIM, a, stroke=0)
        text(d, (CX, 350), "10 s", font(DISP, 120), WHITE, a, stroke=7)
        return
    text(d, (CX, 222), TXT["arming"] + "...", font(UI, 40), TEAL, a, stroke=0)
    u = (t - st.PRESS) % 1.0
    _, sc = appear(u, 0.0, ramp=0.06)
    text(d, (CX, 338), f"{left} s", font(DISP, int(132 * (1.0 + 0.12 * (1 - S.smooth(u / 0.25))))), WHITE, a, stroke=8)
    text(d, (CX, 432), TXT["leave"], font(UI, 40), AMBER, a, stroke=0)


def ticket(d, st, t, a):
    """parking-ticket card: the ESP32 stamps the time (lastMotion = now) on 'stamps'. Compact (y 235-605) so the
    OLED (INTRUDER) and the buzzer rings stay visible under it"""
    if a <= 0.01:
        return
    tl = st.STAMP + 0.2  # the stamp lands (mix.py plays the stamp sound here)
    x0, x1, y0, y1 = CX - 290, CX + 290, 235, 605
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=rgba(PAPER, a), outline=rgba("#c9b994", a), width=4)
    for x in range(int(x0) + 20, int(x1) - 10, 34):  # perforated top edge
        d.ellipse([x, y0 + 12, x + 12, y0 + 24], fill=rgba("#0b1220", a))
    d.text((CX, y0 + 64), TXT["ticket"], font=font(DISP, 46), fill=rgba(INKP, a), anchor="mm")
    d.line([(x0 + 40, y0 + 98), (x1 - 40, y0 + 98)], fill=rgba("#c9b994", a), width=3)
    d.text((CX, y0 + 128), TXT["seen"], font=font(UI, 32), fill=rgba("#7a6748", a), anchor="mm")
    if t >= tl - 0.12:  # the stamp: comes down big, lands with a bump
        u = (t - (tl - 0.12)) / 0.12
        sc = 1.0 + 0.9 * (1 - S.smooth(u)) if u < 1 else 1.0
        sa = a * S.smooth(u * 1.5)
        s = f"{S.STAMP_MS:,} ms".replace(",", " ")
        f = font(MONO, int(58 * sc))
        tw = d.textlength(s, font=f)
        cy = y0 + 205
        lay = Image.new("RGBA", (int(tw + 70), int(58 * sc + 50)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([4, 4, lay.width - 5, lay.height - 5], radius=10, outline=(214, 40, 52, 255), width=7)
        ld.text((lay.width / 2, lay.height / 2), s, font=f, fill=(214, 40, 52, 255), anchor="mm")
        lay = lay.rotate(-5, expand=True, resample=Image.BICUBIC)
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * sa)))
        d.img.alpha_composite(lay, (int(CX - lay.width / 2), int(cy - lay.height / 2)))
    ac = a * S.smooth((t - tl - 0.3) / 0.25)  # the code line, printed on the ticket
    if ac > 0.01:
        d.rounded_rectangle([x0 + 50, y1 - 88, x1 - 50, y1 - 26], radius=14, fill=rgba("#0e1526", ac))
        d.text((CX, y1 - 57), "lastMotion = now;", font=font(MONO, 40), fill=rgba(WHITE, ac), anchor="mm")


LOGO = Image.open(os.path.join(HERE, "..", "..", "..", "brand", "export", "profile_800.png")).convert("RGB")


def ui(img, d, st, t, anc, caps):
    sh = st.shot_at(t)
    sid = sh["id"]
    if sid == "hook":
        a, _ = appear(t, 0.1, sh["end"] - 0.12)
        pill(d, CX, 150, TXT["badge"], font(UI, 38), INK, AMBER, a)
        h1, h2 = TXT["title"]
        text(d, (CX, 240), h1, font(DISP, 76), WHITE, a, stroke=8)
        text(d, (CX, 326), h2, font(DISP, 76), WHITE, a, stroke=8)
        if t >= st.H_CATCH:
            _, sc = appear(t, st.H_CATCH)
            fl = int((t - st.H_CATCH) / S.SIREN_STEP) % 2
            text(d, (CX, 440), TXT["intruder"], font(DISP, int(112 * sc)), RED if not fl else WHITE, a, stroke=10,
                 sfill="#5a0010" if fl else INK)
    elif sid == "arm":
        countdown_hud(d, st, t, appear(t, sh["start"], sh["end"] - 0.12)[0])
    elif sid == "catch":
        a, _ = appear(t, sh["start"], st.TC - 0.05)
        pill(d, CX, 200, TXT["later"], font(UI, 44), INK, TEAL, a)
        if t >= st.TC:
            a2, sc = appear(t, st.TC, sh["end"] - 0.1)
            fl = int((t - st.TC) / S.SIREN_STEP) % 2
            text(d, (CX, 310), TXT["caught"], font(DISP, int(136 * sc)), RED if not fl else WHITE, a2, stroke=11,
                 sfill="#5a0010" if fl else INK)
    elif sid == "ago":
        a, _ = appear(t, sh["start"], sh["end"] - 0.1)
        pill(d, CX, 200, TXT["back"], font(UI, 44), INK, TEAL, a)
        if t >= st.TWO - 0.1:
            a2, sc = appear(t, st.TWO - 0.1, sh["end"] - 0.1)
            text(d, (CX, 330), TXT["ago"], font(DISP, int(120 * sc)), GOLD, a2, stroke=9)
    elif sid in ("how_lens", "how_yes", "how_stamp"):
        a, _ = appear(t, st.S["how_lens"]["start"], st.S["how_stamp"]["end"] - 0.1)
        pill(d, CX, 180, TXT["how"], font(UI, 42), INK, TEAL, a)
        if sid == "how_lens":
            a2, sc = appear(t, st.word("motion") - 0.1, sh["end"] - 0.1)
            text(d, (CX, 290), TXT["pir"], font(DISP, int(76 * sc)), WHITE, a2, stroke=8)
        elif sid == "how_yes" and t >= st.YES:
            a2, sc = appear(t, st.YES, sh["end"] - 0.1)
            text(d, (CX, 310), TXT["yes"], font(DISP, int(150 * sc)), GREEN, a2, stroke=10)
        elif sid == "how_stamp":
            ticket(d, st, t, appear(t, st.STAMP - 0.25, sh["end"] - 0.1)[0])
            if t >= st.SIREN2 - 0.1:
                pill(d, CX, 1370, TXT["siren"], font(UI, 40), INK, RED, appear(t, st.SIREN2 - 0.1, sh["end"] - 0.1)[0])
    elif sid == "parts":
        a, sc = appear(t, sh["start"] + 0.05, sh["end"] - 0.1)
        text(d, (CX, 230), TXT["parts"], font(DISP, int(84 * sc)), WHITE, a, stroke=8)
    else:  # cta
        a, _ = appear(t, sh["start"] + 0.05, 1e9)
        follow(img, d, st, t, a)
        ac = S.smooth((t - st.word("comments") + 0.1) / 0.25)
        pill(d, CX, 1330, TXT["comments"], font(UI, 44), INK, AMBER, ac)
    if not os.environ.get("NOCAP"):  # NOCAP=1: stills without captions (thumbnail)
        draw_caption(d, caps, t)


def follow(img, d, st, t, a):
    """CTA card: headline + channel row + a big follow button; a touch dot taps it on 'Follow' / 'takip'"""
    if a <= 0.01:
        return
    tap = st.TAP
    panel(d, [SAFE_L + 10, 160, SAFE_R - 10, 700], a, outline=AMBER)
    h1, h2 = TXT["head"]
    text(d, (CX, 240), h1, font(DISP, 64), WHITE, a, stroke=0)
    text(d, (CX, 316), h2, font(DISP, 64), AMBER, a, stroke=0)
    lx, ly = CX - 230, 445
    if a > 0.5:
        av = LOGO.resize((110, 110))
        m = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(m).ellipse([0, 0, 109, 109], fill=255)
        img.paste(av, (int(lx), ly - 55), m)
    d.text((lx + 135, ly - 18), "Pin by Pin Lab", font=font(UI, 48), fill=rgba(WHITE, a), anchor="lm")
    d.text((lx + 135, ly + 30), TXT["chan"], font=font(UI, 32), fill=rgba(DIM, a), anchor="lm")
    done = t >= tap + 0.08
    press = 1 - 0.08 * math.exp(-((t - tap - 0.04) / 0.07) ** 2)
    bw, bh, by = 470 * press, 100 * press, 600
    box = [CX - bw / 2, by - bh / 2, CX + bw / 2, by + bh / 2]
    d.rounded_rectangle(box, radius=bh / 2, fill=rgba("#3a4256" if done else "#ff2d3d", a))
    if done:
        tw = d.textlength(TXT["done"], font=font(UI, 44))
        check(d, CX - tw / 2 - 10, by, 16, WHITE, a)
        d.text((CX + 22, by + 2), TXT["done"], font=font(UI, 44), fill=rgba(WHITE, a), anchor="mm")
        u = (t - tap - 0.08) / 0.6
        if 0 <= u <= 1:
            r = 70 * u
            d.rounded_rectangle([box[0] - r, box[1] - r * 0.4, box[2] + r, box[3] + r * 0.4], radius=bh / 2 + r * 0.4,
                                outline=rgba("#ff2d3d", a * (1 - u)), width=6)
    else:
        d.text((CX, by + 2), TXT["btn"], font=font(UI, 48), fill=rgba(WHITE, a), anchor="mm")
    if tap - 0.8 <= t <= tap + 0.7:  # touch dot flies in and taps
        u = S.smooth((t - (tap - 0.8)) / 0.75)
        fx, fy = CX + 120 + 200 * (1 - u), by + 20 + 300 * (1 - u)
        fa = a * (1 - S.smooth((t - tap - 0.3) / 0.35))
        r = 34 - 10 * math.exp(-((t - tap) / 0.08) ** 2)
        d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=rgba(WHITE, 0.55 * fa), outline=rgba(WHITE, fa), width=5)


LOGO = Image.open(os.path.join(HERE, "..", "..", "..", "brand", "export", "profile_800.png")).convert("RGB")


# ------------------------------------------------------------------ frames
B = os.path.join(HERE, "build", LANG)


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
        still = os.path.join(B, "stills", f"at_{t:06.2f}.png")  # layout checks before the shot is rendered
        if not have and os.path.exists(still):
            src = still
    img = Image.open(src).convert("RGB") if src else Image.new("RGB", (W, H), (11, 18, 32))
    anc = ANCH.get(sh["id"], {}).get(str(f), {})
    waves = []
    bp = anc.get("buzzer")
    if bp:
        for tb, kind in WAVES:
            age = t - tb
            if 0 <= age <= 1.2:
                waves.append({"x": bp[0], "y": bp[1], "age": round(age, 3), "kind": kind})
    img = overlay.draw(img, [], waves)
    img = img.convert("RGBA")
    for t0, t1 in ((st.H_CATCH, st.HOOK_END), (st.TC, st.CATCH_END), (st.STAMP, st.STAMP_END)):
        img = siren_glow(img, st, t, t0, t1)
    d = AD(img)
    tags_draw(d, anc.get("tags", []))
    ui(img, d, st, t, anc, CAPS)
    return img.convert("RGB").tobytes()


def init():
    global STORY, ANCH, WAVES, CAPS
    STORY = S.Story(LANG)
    ANCH = {}
    for sh in STORY.shots:
        p = os.path.join(B, "shots", sh["id"], "anchors.json")
        if os.path.exists(p):
            ANCH[sh["id"]] = json.load(open(p))["frames"]
    WAVES = STORY.waves()
    CAPS = build_captions(STORY)


def main():
    init()
    if "--thumb" in sys.argv:  # build/thumb_<lang>.jpg: one frame without captions
        os.environ["NOCAP"] = "1"
        g = round(float(sys.argv[sys.argv.index("--thumb") + 1]) * FPS)
        Image.frombytes("RGB", (W, H), job(g)).save(os.path.join(HERE, "build", f"thumb_{LANG}.jpg"), quality=92)
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
