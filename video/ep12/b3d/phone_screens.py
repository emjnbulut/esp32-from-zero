"""Phone screen images for the Episode 12 Blender shots (the board's web page, Wi-Fi settings, the troubles).

    .venv/Scripts/python video/ep12/b3d/phone_screens.py        # -> video/ep12/b3d/build/phone/<state>.png

ep12_3d.py runs this automatically (Blender's Python has no PIL) and imports the layout part (TAPS, STATES) to know
where each button sits on the screen, for the glowing finger-tap dot. The page follows the sketch's PAGE template
(lessons/12-phone-control/code/phone_remote): dark background, "ESP32 remote", RED / GREEN / BLUE / OFF / RING links.
"""
import os
import sys

W, H = 540, 1170
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build", "phone")
FONT_B = "C:/Windows/Fonts/segoeuib.ttf"
FONT_R = "C:/Windows/Fonts/segoeui.ttf"
ADDR = "192.168.4.1"
NET = "PinByPin-ESP32"

BTN = {"red": ("RED", "#e5484d"), "green": ("GREEN", "#2fbf71"), "blue": ("BLUE", "#3b82f6"),
       "off": ("OFF", "#334155"), "ring": ("RING", "#f59e0b"), "party": ("PARTY", None)}


def page_buttons(party=False):
    """name -> (x0, y0, x1, y1) in px, like the sketch's <a> blocks"""
    names = ["red", "green", "blue", "off", "ring"] + (["party"] if party else [])
    h, gap, y = (104, 20, 250) if party else (118, 26, 262)
    out = {}
    for n in names:
        out[n] = (50, y, 490, y + h)
        y += h + gap
    return out


WIFI_ROWS = ["HomeNet-5G", NET, "Cafe_Free", "NETGEAR-22"]


def wifi_row_rect(i):
    return (24, 300 + i * 96, 516, 300 + i * 96 + 84)


DIALOG_STAY = (290, 690, 500, 760)  # "YES, STAY" in the no-internet dialog


def _center(r):
    return ((r[0] + r[2]) / 2 / W, (r[1] + r[3]) / 2 / H)


TAPS = {n: _center(r) for n, r in page_buttons(True).items()}
TAPS["wifi_net"] = _center(wifi_row_rect(1))
TAPS["stay"] = _center(DIALOG_STAY)
TAPS["addr"] = _center((24, 70, 516, 130))

STATES = (["page", "page_party", "page_party_party", "mobile", "nointernet", "nointernet_stay", "pass7", "pass8",
           "addr_www", "addr_https", "addr_ok", "wifi_list", "wifi_tap", "wifi_connected"]
          + ["page_" + n for n in BTN if n != "party"]
          + ["wifi_pass_%d" % i for i in range(9)] + ["addr_type_%d" % i for i in range(len(ADDR) + 1)])


# ----------------------------------------------------------------------------------------------- drawing
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(c, w, u):
    return tuple(int(a + (b - a) * u) for a, b in zip(c, w))


def draw(state):
    from PIL import Image, ImageDraw, ImageFont

    def f(size, bold=True):
        return ImageFont.truetype(FONT_B if bold else FONT_R, size)

    img = Image.new("RGB", (W, H), _rgb("#0b1220"))
    g = ImageDraw.Draw(img)

    def text_c(cx, cy, s, font, fill):
        tw = g.textlength(s, font=font)
        g.text((cx - tw / 2, cy - font.size * 0.62), s, font=font, fill=fill)

    def status(mobile=False):
        g.rectangle([0, 0, W, 56], fill=_rgb("#05080f"))
        g.text((26, 12), "9:41", font=f(26), fill=(255, 255, 255))
        if mobile:
            g.text((W - 150, 12), "4G", font=f(26), fill=(255, 255, 255))
        else:  # wifi fan
            cx, cy = W - 128, 42
            for r in (8, 16, 24):
                g.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=(255, 255, 255), width=4)
        g.rounded_rectangle([W - 82, 18, W - 34, 40], radius=5, outline=(255, 255, 255), width=3)
        g.rectangle([W - 78, 22, W - 48, 36], fill=(255, 255, 255))

    def browser(addr=ADDR, col="#e5e7eb", border=None):
        g.rectangle([0, 56, W, 150], fill=_rgb("#1f2937"))
        g.rounded_rectangle([24, 70, 516, 130], radius=30, fill=_rgb("#111827"),
                            outline=_rgb(border) if border else None, width=4 if border else 0)
        g.text((54, 80), addr, font=f(30, False), fill=_rgb(col))

    def page(party=False, pressed=None):
        browser()
        text_c(W / 2, 205, "ESP32 remote", f(46), (255, 255, 255))
        for n, r in page_buttons(party).items():
            label, col = BTN[n]
            if col is None:  # PARTY: red-green-blue gradient
                strip = Image.new("RGB", (r[2] - r[0], r[3] - r[1]))
                sd = ImageDraw.Draw(strip)
                cols = [_rgb("#e5484d"), _rgb("#2fbf71"), _rgb("#3b82f6")]
                for x in range(strip.width):
                    u = x / (strip.width - 1) * 2
                    i = min(1, int(u))
                    sd.line([(x, 0), (x, strip.height)], fill=_mix(cols[i], cols[i + 1], u - i))
                m = Image.new("L", strip.size, 0)
                ImageDraw.Draw(m).rounded_rectangle([0, 0, strip.width - 1, strip.height - 1], radius=18, fill=255)
                img.paste(strip, (r[0], r[1]), m)
            else:
                c = _rgb(col)
                if n == pressed:
                    c = _mix(c, (255, 255, 255), 0.3)
                g.rounded_rectangle(r, radius=18, fill=c)
            if n == pressed:
                g.rounded_rectangle([r[0] - 7, r[1] - 7, r[2] + 7, r[3] + 7], radius=24, outline=(255, 255, 255), width=6)
            text_c((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + 4, label, f(34), (255, 255, 255))

    def wifi(highlight=None, connected=False, rows=WIFI_ROWS):
        g.rectangle([0, 56, W, H], fill=_rgb("#111827"))
        g.text((28, 90), "Wi-Fi", font=f(52), fill=(255, 255, 255))
        g.rounded_rectangle([420, 102, 500, 142], radius=20, fill=_rgb("#2fbf71"))
        g.ellipse([462, 106, 494, 138], fill=(255, 255, 255))
        g.text((30, 240), "NETWORKS", font=f(22), fill=_rgb("#9ca3af"))
        for i, name in enumerate(rows):
            r = wifi_row_rect(i)
            on = name == highlight
            g.rounded_rectangle(r, radius=16, fill=_rgb("#1e3a5f") if on else _rgb("#1f2937"))
            g.text((r[0] + 26, r[1] + 14 if not (connected and name == NET) else r[1] + 6), name, font=f(30, on),
                   fill=(255, 255, 255))
            if connected and name == NET:
                g.text((r[0] + 26, r[1] + 46), "Connected, no internet", font=f(20, False), fill=_rgb("#2fbf71"))
                g.line([(r[2] - 64, r[1] + 44), (r[2] - 52, r[1] + 56), (r[2] - 30, r[1] + 28)], fill=_rgb("#2fbf71"), width=6)
            else:  # padlock
                x, y = r[2] - 56, r[1] + 30
                g.rounded_rectangle([x, y + 10, x + 24, y + 30], radius=4, fill=_rgb("#9ca3af"))
                g.arc([x + 3, y - 2, x + 21, y + 22], 180, 360, fill=_rgb("#9ca3af"), width=4)

    def keyboard():
        g.rectangle([0, 820, W, H], fill=_rgb("#1f2937"))
        for row, (n, y) in enumerate(((10, 840), (9, 924), (7, 1008))):
            kw = (W - 20) / 10
            x0 = (W - n * kw) / 2
            for i in range(n):
                g.rounded_rectangle([x0 + i * kw + 4, y, x0 + (i + 1) * kw - 4, y + 70], radius=8, fill=_rgb("#4b5563"))
        g.rounded_rectangle([130, 1092, 410, 1150], radius=8, fill=_rgb("#4b5563"))

    def pass_dialog(n):
        img.paste(_mix(_rgb("#111827"), (0, 0, 0), 0.5), [0, 56, W, H])
        g.rounded_rectangle([30, 360, 510, 760], radius=26, fill=_rgb("#1f2937"))
        text_c(W / 2, 420, NET, f(34), (255, 255, 255))
        g.text((60, 470), "Password", font=f(24, False), fill=_rgb("#9ca3af"))
        g.rounded_rectangle([60, 510, 480, 580], radius=12, fill=_rgb("#111827"), outline=_rgb("#3b82f6"), width=3)
        for i in range(n):
            cx = 90 + i * 34
            g.ellipse([cx - 9, 536, cx + 9, 554], fill=(255, 255, 255))
        g.line([(90 + n * 34 - 8, 526), (90 + n * 34 - 8, 566)], fill=_rgb("#3b82f6"), width=3)
        text_c(150, 690, "Cancel", f(30, False), _rgb("#9ca3af"))
        text_c(390, 690, "Join", f(30), _rgb("#3b82f6") if n >= 8 else _rgb("#4b5563"))
        keyboard()

    def error_page(addr, col):
        browser(addr, col, border=col)
        text_c(W / 2, 420, ":(", f(90), _rgb("#6b7280"))
        text_c(W / 2, 560, "This site can't be reached", f(30), (255, 255, 255))
        text_c(W / 2, 610, addr, f(26, False), _rgb("#9ca3af"))

    status(mobile=state == "mobile")
    if state == "page":
        page()
    elif state.startswith("page_party"):
        page(True, "party" if state == "page_party_party" else None)
    elif state.startswith("page_"):
        page(False, state[5:])
    elif state == "mobile":
        error_page(ADDR, "#e5e7eb")
        g.rounded_rectangle([40, 700, 500, 800], radius=18, fill=_rgb("#1f2937"))
        text_c(W / 2, 752, "Using mobile data", f(28), _rgb("#f59e0b"))
    elif state.startswith("nointernet"):
        page()
        ov = Image.new("RGB", (W, H), (0, 0, 0))
        img.paste(Image.blend(img, ov, 0.55))
        g = ImageDraw.Draw(img)
        g.rounded_rectangle([30, 420, 510, 790], radius=26, fill=_rgb("#1f2937"))
        text_c(W / 2, 480, NET, f(32), (255, 255, 255))
        text_c(W / 2, 545, "has no internet access.", f(28, False), _rgb("#d1d5db"))
        text_c(W / 2, 600, "Stay connected?", f(32), (255, 255, 255))
        stay = state == "nointernet_stay"
        g.rounded_rectangle([40, 690, 250, 760], radius=16, fill=_rgb("#374151"))
        text_c(145, 729, "NO", f(28), (255, 255, 255))
        g.rounded_rectangle(DIALOG_STAY, radius=16, fill=_rgb("#60a5fa") if stay else _rgb("#3b82f6"),
                            outline=(255, 255, 255) if stay else None, width=5 if stay else 0)
        text_c((DIALOG_STAY[0] + DIALOG_STAY[2]) / 2, 729, "YES, STAY", f(28), (255, 255, 255))
    elif state in ("pass7", "pass8"):
        ok = state == "pass8"
        g.rectangle([0, 56, W, H], fill=_rgb("#111827"))
        g.text((30, 84), "in the sketch:", font=f(24, False), fill=_rgb("#9ca3af"))
        g.rounded_rectangle([24, 124, 516, 330], radius=18, fill=_rgb("#0b1220"),
                            outline=_rgb("#2fbf71" if ok else "#e5484d"), width=4)
        g.text((44, 140), "WIFI_PASSWORD =", font=f(28, False), fill=_rgb("#7fe8de"))
        pw = "esp32lab" if ok else "esp32la"
        g.text((44, 190), '"%s"' % pw, font=f(44), fill=_rgb("#ffd166"))
        g.text((44, 262), "%d characters" % len(pw), font=f(30), fill=_rgb("#2fbf71" if ok else "#e5484d"))
        if ok:
            g.line([(430, 210), (452, 236), (494, 176)], fill=_rgb("#2fbf71"), width=10)
        else:
            g.line([(436, 176), (490, 236)], fill=_rgb("#e5484d"), width=10)
            g.line([(490, 176), (436, 236)], fill=_rgb("#e5484d"), width=10)
        g.text((30, 380), "Wi-Fi networks", font=f(34), fill=(255, 255, 255))
        rows = ["HomeNet-5G", NET, "Cafe_Free"] if ok else ["HomeNet-5G", "Cafe_Free"]
        for i, name in enumerate(rows):
            r = (24, 450 + i * 96, 516, 534 + i * 96)
            on = name == NET
            g.rounded_rectangle(r, radius=16, fill=_rgb("#14532d") if on else _rgb("#1f2937"))
            g.text((r[0] + 26, r[1] + 22), name, font=f(30, on), fill=(255, 255, 255))
        if not ok:
            text_c(W / 2, 700, "(no PinByPin-ESP32)", f(28, False), _rgb("#e5484d"))
    elif state == "addr_www":
        error_page("www." + ADDR, "#e5484d")
    elif state == "addr_https":
        error_page("https://" + ADDR, "#e5484d")
    elif state == "addr_ok":
        page()
        g.rounded_rectangle([24, 70, 516, 130], radius=30, outline=_rgb("#2fbf71"), width=4)
    elif state.startswith("addr_type_"):
        n = int(state.rsplit("_", 1)[1])
        browser(ADDR[:n] + "|", "#ffffff", border="#3b82f6")
        keyboard()
    elif state == "wifi_list":
        wifi()
    elif state == "wifi_tap":
        wifi(highlight=NET)
    elif state.startswith("wifi_pass_"):
        wifi(highlight=NET)
        pass_dialog(int(state.rsplit("_", 1)[1]))
    elif state == "wifi_connected":
        wifi(highlight=NET, connected=True, rows=[NET, "HomeNet-5G", "Cafe_Free", "NETGEAR-22"])
    else:
        raise KeyError(state)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    for s in STATES:
        draw(s).save(os.path.join(OUT, s + ".png"))
    print(len(STATES), "phone screens ->", OUT)


if __name__ == "__main__":
    sys.exit(main())
