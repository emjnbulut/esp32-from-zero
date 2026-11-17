"""Treasure Short soundtrack: narration + music bed (ducked) + synced sound effects.
  python video/short3d/treasure/mix.py   -> build/audio.wav
Effects follow build/track.json: a metal-detector blip on every red-LED flash (pitch rises with heat),
a click on the button press, and a little fanfare + coin sparkle when the treasure is found."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import music  # noqa: E402

SR = 48000
B = HERE / "build"
T = json.loads((B / "track.json").read_text())


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


voice = decode(B / "voice.wav")
n = len(voice)
fx = np.zeros(n, np.float32)


def put(sig, t, gain):
    i = int(t * SR)
    if i >= n:
        return
    j = min(n, i + len(sig))
    fx[i:j] += sig[: j - i] * gain


def tone(freq, dur, attack=0.004, decay=None, shape="sine"):
    tt = np.arange(int(dur * SR)) / SR
    w = np.sin(2 * np.pi * freq * tt)
    if shape == "square":
        w = np.sign(w) * 0.6 + w * 0.4
    env = np.minimum(1, tt / attack) * np.exp(-tt / (decay or dur / 3))
    return (w * env).astype(np.float32)


# metal-detector blips on each rising edge of the red LED
win = T["windows"]["beep"]
fps, tr = T["fps"], T["track"]
for f in range(1, len(tr)):
    t = f / fps
    if tr[f]["rled"] and not tr[f - 1]["rled"] and any(a <= t <= b for a, b in win) and not tr[f]["party"]:
        h = T["heat"][f] / 255
        put(tone(950 + 650 * h, 0.05, decay=0.02, shape="square"), t, 0.11)

# button click
tp = T["T"]["press"]
click = (np.random.default_rng(3).standard_normal(int(0.012 * SR)) * np.exp(-np.arange(int(0.012 * SR)) / (0.002 * SR))).astype(np.float32)
put(click, tp - 0.02, 0.35)
put(tone(180, 0.05, decay=0.012), tp - 0.02, 0.4)

# fanfare: quick major arpeggio + sparkle
tf = T["T"]["party"]
for k, (fr, dt) in enumerate([(523.25, 0.0), (659.25, 0.09), (783.99, 0.18), (1046.5, 0.27), (1318.5, 0.36)]):
    put(tone(fr, 0.5, decay=0.18) + 0.3 * tone(fr * 2, 0.5, decay=0.1), tf + dt, 0.16)
rng = np.random.default_rng(11)
for k in range(14):
    put(tone(2600 + rng.random() * 2200, 0.12, decay=0.03), tf + 0.3 + k * 0.07, 0.05)

mixed = music.mix(voice + fx, SR, decode, level=0.12, fade_in=0.5, fade_out=1.5)
peak = np.max(np.abs(mixed))
if peak > 0.98:
    mixed *= 0.98 / peak
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", str(B / "audio.wav")],
               input=mixed.astype(np.float32).tobytes(), check=True)
print("audio.wav", round(n / SR, 2), "s, peak", round(float(peak), 3))
