"""Secret knock lock Short soundtrack: narration + ducked music bed + effects synced to the lock.
  python video/short3d/knocklock/mix.py en   -> build/<lang>/audio.wav
Effects come from build/<lang>_events.json (story.mjs): press clicks, a rising note per right beat, a buzzer on a
wrong beat, a fanfare when the lock opens, a clunk when it locks again, countdown ticks, pops in the build montage."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import music  # noqa: E402

SR = 48000
LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
B = HERE / "build"
EV = json.loads((B / f"{LANG}_events.json").read_text())


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


voice = decode(B / f"{LANG}_voice.wav")
n = len(voice)
fx = np.zeros(n, np.float32)


def put(sig, t, gain):
    i = int(t * SR)
    if i >= n or i < 0:
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


rng = np.random.default_rng(5)
click = (rng.standard_normal(int(0.012 * SR)) * np.exp(-np.arange(int(0.012 * SR)) / (0.002 * SR))).astype(np.float32)
NOTE = {1: 659.25, 2: 783.99, 3: 1046.5}
for t, kind, val in EV["ev"]:
    if kind == "down":
        put(click, t, 0.32); put(tone(170, 0.05, decay=0.012), t, 0.35)
    elif kind == "up":
        put(click, t, 0.18)
    elif kind == "beat":
        put(tone(NOTE[val], 0.22, decay=0.08) + 0.25 * tone(NOTE[val] * 2, 0.22, decay=0.05), t + 0.01, 0.16)
    elif kind == "wrong":
        for k in range(4):
            put(tone(150, 0.12, decay=0.08, shape="square"), t + k * 0.24, 0.16)
    elif kind == "unlock":
        for k, (fr, dt) in enumerate([(523.25, 0.0), (659.25, 0.09), (783.99, 0.18), (1046.5, 0.27), (1318.5, 0.36)]):
            put(tone(fr, 0.5, decay=0.18) + 0.3 * tone(fr * 2, 0.5, decay=0.1), t + 0.05 + dt, 0.15)
        for k in range(12):
            put(tone(2600 + rng.random() * 2200, 0.12, decay=0.03), t + 0.4 + k * 0.07, 0.045)
    elif kind == "relock":
        put(tone(110, 0.18, decay=0.05, shape="square"), t, 0.18); put(click, t, 0.4)
    elif kind == "forget":
        for k, fr in enumerate([700, 520, 380]):
            put(tone(fr, 0.12, decay=0.05), t + k * 0.08, 0.13)
    elif kind == "tick":
        put(tone(1400, 0.05, decay=0.015), t, 0.14)
m0, m1 = EV["mont"]
for k in range(16):  # parts snapping in
    tk = m0 + 0.15 + k * (m1 - m0 - 0.6) / 16
    put(tone(900 + 60 * k, 0.05, decay=0.015), tk, 0.08); put(click, tk, 0.12)

mixed = music.mix(voice + fx, SR, decode, level=0.11, fade_in=0.5, fade_out=1.5)
peak = np.max(np.abs(mixed))
if peak > 0.98:
    mixed *= 0.98 / peak
(B / LANG).mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", str(B / LANG / "audio.wav")],
               input=mixed.astype(np.float32).tobytes(), check=True)
print("audio.wav", round(n / SR, 2), "s, peak", round(float(peak), 3))
