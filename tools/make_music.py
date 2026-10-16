"""Generate a soft, royalty-free ambient music bed (procedural, no samples).
Usage: python tools/make_music.py  -> video/assets/music.wav (64 s loop)"""
import subprocess
from pathlib import Path

import numpy as np

SR = 48000
BPM = 80
beat = 60 / BPM
bar = beat * 4
ROOT = Path(__file__).resolve().parent.parent

# Cmaj7 - Am7 - Fmaj7 - G6, two bars each, played twice (16 bars = 48 s at 80 bpm)
CHORDS = [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 52, 59]]
freq = lambda m: 440 * 2 ** ((m - 69) / 12)
n_bars = 16
dur = n_bars * bar
t = np.arange(int(dur * SR)) / SR
out = np.zeros_like(t)
rng = np.random.default_rng(3)

for b in range(n_bars):
    chord = CHORDS[(b // 2) % 4]
    t0 = b * bar
    i0, i1 = int(t0 * SR), int((t0 + bar * 1.15) * SR)
    seg = t[i0:min(i1, len(t))] - t0
    env = np.minimum(1, seg / 0.8) * np.exp(-seg / 3.5)
    for m in chord:
        f = freq(m + 12)
        tone = np.sin(2 * np.pi * f * seg) + 0.3 * np.sin(2 * np.pi * 2 * f * seg + 0.3)
        out[i0:i0 + len(seg)] += 0.06 * env * tone
    # soft arpeggio on eighth notes (pluck)
    for k in range(8):
        if rng.random() < 0.35:
            continue
        m = chord[k % 4] + 24
        a0 = t0 + k * beat / 2
        j0 = int(a0 * SR)
        s2 = t[j0:j0 + int(1.2 * SR)] - a0
        pl = np.exp(-s2 * 4) * np.sin(2 * np.pi * freq(m) * s2)
        out[j0:j0 + len(s2)] += 0.035 * pl

# gentle low-pass via moving average and a touch of echo
k = 9
out = np.convolve(out, np.ones(k) / k, mode="same")
d = int(beat * 0.75 * SR)
echo = np.zeros_like(out); echo[d:] = out[:-d] * 0.3
out = out + echo
out /= np.max(np.abs(out)) * 1.1
pcm = (out * 32767).astype(np.int16)
dst = ROOT / "video" / "assets" / "music.wav"
dst.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(dst)], input=pcm.tobytes(), check=True)
print(dst, f"{dur:.1f}s")
