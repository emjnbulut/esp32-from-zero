"""Music bed under the narration.

The track is the first audio file in video/assets/music/ (sorted by name), or the old
generated video/assets/music.wav. Loops are joined with a long equal-power crossfade so
there is no audible seam, and the music ducks under the voice and comes back up in pauses.
"""
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
XFADE = 4.0     # seconds of overlap where the track wraps around
DUCK = 0.45     # music gain while someone is talking (relative)


def track() -> Path | None:
    d = ROOT / "video" / "assets" / "music"
    files = sorted(p for p in d.glob("*") if p.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg", ".flac")) if d.exists() else []
    if files:
        return files[0]
    old = ROOT / "video" / "assets" / "music.wav"
    return old if old.exists() else None


def loop_to(m: np.ndarray, n: int, sr: int) -> np.ndarray:
    """Repeat m to n samples, overlapping each repeat by XFADE with an equal-power crossfade."""
    if len(m) >= n:
        return m[:n].copy()
    x = min(int(XFADE * sr), len(m) // 4)
    fade_in = np.sin(np.linspace(0, np.pi / 2, x)) ** 2
    out = np.zeros(n + len(m), dtype=np.float32)
    pos = 0
    while pos < n:
        seg = m.copy()
        if pos > 0:
            seg[:x] *= fade_in
            out[pos:pos + x] *= fade_in[::-1]
        out[pos:pos + len(seg)] += seg
        pos += len(m) - x
    return out[:n]


def duck_env(voice: np.ndarray, sr: int) -> np.ndarray:
    """Gain curve: DUCK while the voice is active, 1.0 in pauses, with smooth attack/release."""
    hop = sr // 50
    frames = -(-len(voice) // hop)
    rms = np.array([np.sqrt(np.mean(voice[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(frames)])
    active = (rms > 0.02).astype(np.float32)
    # hold over short gaps between words (0.6 s) so the music doesn't pump
    hold = int(0.6 * 50)
    active = np.convolve(active, np.ones(hold), mode="same") > 0
    g = np.where(active, DUCK, 1.0).astype(np.float32)
    # one-pole smoothing: ~0.15 s attack, ~0.8 s release
    out = np.empty_like(g)
    cur = g[0]
    for i, v in enumerate(g):
        k = 0.13 if v < cur else 0.025
        cur += (v - cur) * k
        out[i] = cur
    return np.repeat(out, hop)[: len(voice)]


def mix(voice: np.ndarray, sr: int, decode, level: float, fade_in=3.0, fade_out=3.0) -> np.ndarray:
    """voice + music bed (if a track exists). `decode(path)` returns mono float32 at sr."""
    t = track()
    if t is None:
        return voice
    m = loop_to(decode(t), len(voice), sr) * level
    m *= duck_env(voice, sr)
    if fade_in:
        f = int(fade_in * sr); m[:f] *= np.linspace(0, 1, f)
    f = int(fade_out * sr); m[-f:] *= np.linspace(1, 0, f)
    return voice + m
