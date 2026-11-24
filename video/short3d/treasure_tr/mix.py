"""Soundtrack of the Turkish treasure-detector Short -> build/audio.wav (48 kHz stereo, loudness -16 LUFS).

Narration (build/voice.wav) + effects from story.events() + the music bed (tools/music.py, ducked under the voice,
level as in the other 3D Shorts). Every buzzer sound is video/b3d/assemble.py piezo() (the approved shrill passive
buzzer) at the frequency the sketch uses: Geiger ticks tone(pin, 800..3000 Hz, 15 ms), the fanfare 1047/1319/1568/2093 Hz,
the "BOŞ" buzz tone(pin, 150, 400). Clicks/pops/plugs from assemble.SFX.
"""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "video", "b3d"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import assemble as A  # noqa: E402
import music  # noqa: E402
import story as S  # noqa: E402

SR = A.SR
B = os.path.join(HERE, "build")


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


_cache = {}


def piezo(f, d, vol):
    k = (f, d)
    if k not in _cache:
        _cache[k] = A.piezo(f, d, 1.0)
    return _cache[k] * vol


def whoosh(d=0.28, vol=0.10):
    rng = np.random.default_rng(9)
    n = int(d * SR)
    x = rng.standard_normal(n).astype(np.float32)
    y, prev = np.empty_like(x), 0.0
    for i, v in enumerate(x):  # sweeping one-pole low-pass: air rushing past
        a = 0.02 + 0.25 * (i / n)
        prev += a * (v - prev)
        y[i] = prev
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return (y / (np.max(np.abs(y)) or 1) * env * vol).astype(np.float32)


def chime(vol=0.12):
    return A.seq((0, A.tone(1319, 0.18, vol)), (0.09, A.tone(1760, 0.3, vol)))


def main():
    st = S.Story()
    voice = decode(os.path.join(B, "voice.wav"))
    n = len(voice)
    fx = np.zeros(n, np.float32)

    def put(sig, t):
        i = int(t * SR)
        if 0 <= i < n:
            j = min(n, i + len(sig))
            fx[i:j] += sig[: j - i]

    for t, kind, arg in st.events():
        if kind == "tick":
            put(piezo(arg["f"], 0.015, arg["vol"] * 1.15), t)
        elif kind == "fanfare":
            acc = 0.0
            for f, d in S.FANFARE:
                put(piezo(f, d, 0.42), t + acc)
                acc += d
        elif kind == "buzz_lo":
            put(piezo(150, 0.40, 0.45), t)
        elif kind == "click":
            put(A.SFX["click"](), t)
        elif kind == "tap":
            put(A.SFX["click"]() * 0.6, t)
        elif kind == "whoosh":
            put(whoosh(), t)
        elif kind in ("pop", "snap", "unplug", "plug"):
            put(A.SFX[kind]() * (0.7 if kind == "snap" else 1.0), t)
        elif kind == "boot":
            put(A.tone(1200, 0.06, 0.06), t)  # soft UI blip (the sketch itself does not beep at boot)
        elif kind == "ding":
            put(chime(), t)
    mixed = music.mix(voice + fx, SR, decode, level=0.11, fade_in=0.5, fade_out=1.5)
    peak = float(np.max(np.abs(mixed)))
    if peak > 0.98:
        mixed *= 0.98 / peak
    # two-pass loudnorm (one pass ended at -18 LUFS: the buzzer clicks are peaky); limiter first so the
    # linear second pass can reach -16 LUFS like the other Shorts
    pre = "alimiter=limit=0.6:attack=2:release=40:level=false,"
    pcm = mixed.astype(np.float32).tobytes()
    import json
    import re
    m = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                        pre + "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       input=pcm, capture_output=True, check=True).stderr.decode("utf-8", "ignore")
    j = json.loads(re.findall(r"\{[^{}]*\}", m)[-1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                    pre + ln, "-ar", str(SR), "-ac", "2", os.path.join(B, "audio.wav")], input=pcm, check=True)
    print("audio.wav", round(n / SR, 2), "s, peak", round(peak, 3))


if __name__ == "__main__":
    main()
