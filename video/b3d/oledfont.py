"""Pixel-exact SSD1306 screens with the Adafruit GFX built-in font (glcdfont.c), so the 3D OLED shows exactly what
the episode's sketch draws. Runs in the repo venv (Pillow).

    from oledfont import Screen
    sc = Screen(); sc.text(0, 0, "REFLEX 2.0  best:", 1); sc.text(0, 28, "214ms", 3); sc.png("out.png")
"""
import os
import re


GLCD = os.path.expanduser("~/Documents/Arduino/libraries/Adafruit_GFX_Library/glcdfont.c")
_FONT = None


def font():
    global _FONT
    if _FONT is None:
        src = open(GLCD, encoding="utf-8", errors="ignore").read()
        body = src[src.index("{") + 1: src.rindex("}")]
        body = re.sub(r"//.*", "", body)
        body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
        _FONT = [int(x, 16) for x in re.findall(r"0x[0-9A-Fa-f]{2}", body)]
    return _FONT


class Screen:
    W, H = 128, 64

    def __init__(self):
        self.px = bytearray(self.W * self.H)

    def clear(self):
        self.px = bytearray(self.W * self.H)

    def set(self, x, y, v=1):
        if 0 <= x < self.W and 0 <= y < self.H:
            self.px[y * self.W + x] = v

    def rect(self, x, y, w, h, fill=True, v=1):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if fill or yy in (y, y + h - 1) or xx in (x, x + w - 1):
                    self.set(xx, yy, v)

    def char(self, x, y, c, size=1, v=1):
        f = font()
        code = ord(c)
        if code >= 176:  # Adafruit's classic-font quirk (cp437 offset) is irrelevant for ASCII
            code += 1
        for i in range(5):
            line = f[code * 5 + i]
            for j in range(8):
                if line & 1:
                    self.rect(x + i * size, y + j * size, size, size, True, v)
                line >>= 1

    def text(self, x, y, s, size=1, v=1):
        """Adafruit print(): 6 px advance per character (x size), no wrap beyond the screen"""
        cx = x
        for c in s:
            if c == "\n":
                cx = x
                y += 8 * size
                continue
            self.char(cx, y, c, size, v)
            cx += 6 * size
        return cx

    def show(self, top, big):
        """the episode's show() helper: size-1 line at (0,0), size-3 line at (0,28)"""
        self.clear()
        self.text(0, 0, top, 1)
        self.text(0, 28, big, 3)
        return self

    def invert(self):
        self.px = bytearray(1 - p for p in self.px)
        return self

    def image(self, scale=8, on=(232, 246, 255), gap=True):
        from PIL import Image
        out = Image.new("RGB", (self.W * scale, self.H * scale), (0, 0, 0))
        o = out.load()
        for y in range(self.H):
            for x in range(self.W):
                if self.px[y * self.W + x]:
                    for yy in range(scale - (1 if gap else 0)):
                        for xx in range(scale - (1 if gap else 0)):
                            o[x * scale + xx, y * scale + yy] = on
        return out

    def key(self):
        return bytes(self.px)
