"""Channel intro (logo sting) and outro (end screen), added around every episode.

The pictures are rendered once from video/bumper/ (re-rendered when bumper.js changes):
  video/bumper/build/intro.mp4 (3.5 s), outro.mp4 (20 s)
Audio: the intro gets a soft synthesized sting (one note per pin lighting up, then a chord
under the P); the outro gets the music bed on its own. No speech, so dubs need nothing extra.
Anything timed against the episode (subtitles, chapters) shifts by INTRO seconds.
Cold open (ep04 on): script.json "sting_after": "<segment id>" plays the episode up to the next
segment first, then the sting, then the rest; only times after that cut shift (see cut()/shift()).

Usage: python tools/bumpers.py        # (re)render the bumper videos
"""
import hashlib
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import music  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "video" / "bumper"
BUILD = DIR / "build"
INTRO, OUTRO = 3.5, 20.0


def render():
    """Render intro.mp4 / outro.mp4 unless they are up to date with bumper.js + index.html."""
    BUILD.mkdir(parents=True, exist_ok=True)
    stamp = hashlib.sha1(b"".join((DIR / f).read_bytes() for f in ("bumper.js", "index.html"))).hexdigest()
    for kind, dur in (("intro", INTRO), ("outro", OUTRO)):
        out, tag = BUILD / f"{kind}.mp4", BUILD / f"{kind}.stamp"
        if out.exists() and tag.exists() and tag.read_text() == stamp:
            continue
        data = BUILD / f"{kind}.json"
        data.write_text(f'{{"kind": "{kind}", "schedule": {{"duration": {dur}}}}}', encoding="utf-8")
        subprocess.run(["node", "engine/render.mjs", "bumper", "--page", str(DIR / "index.html"), "--data", str(data),
                        "--size", "1920x1080", "--out", str(out)], cwd=ROOT / "video", check=True)
        tag.write_text(stamp)
        print("bumper:", out)
    return BUILD / "intro.mp4", BUILD / "outro.mp4"


def _pluck(f, dur, sr):
    t = np.arange(int(dur * sr)) / sr
    return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 5) * np.minimum(1, t / 0.004)


def intro_audio(sr: int) -> np.ndarray:
    n = int(INTRO * sr)
    a = np.zeros(n, np.float32)
    notes = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.66, 1318.51]  # C major pentatonic, up
    for i, f in enumerate(notes):  # one note per pin (bumper.js: pin i lights at 0.35 + 0.15 i)
        s = int((0.35 + i * 0.15) * sr)
        p = _pluck(f, 1.2, sr) * 0.16
        a[s:s + len(p)] += p[: n - s]
    s = int(1.45 * sr)  # warm chord as the P is drawn
    t = np.arange(n - s) / sr
    env = np.minimum(1, t / 0.25) * np.exp(-t / 1.4)
    for f in (130.81, 196.0, 261.63, 329.63, 392.0):
        a[s:] += (0.09 * env * np.sin(2 * np.pi * f * t)).astype(np.float32)
    a = np.convolve(a, np.ones(5) / 5, mode="same")  # take the edge off the highs
    f = int(0.45 * sr)
    a[-f:] *= np.linspace(1, 0, f)
    return (a / np.max(np.abs(a)) * 0.55).astype(np.float32)


def outro_audio(sr: int, decode) -> np.ndarray:
    n = int(OUTRO * sr)
    t = music.track()
    if t is None:
        return np.zeros(n, np.float32)
    m = decode(t)
    start = min(int(30 * sr), max(0, len(m) - n))  # skip the track's intro
    m = music.loop_to(m[start:], n, sr) * 0.22
    f0, f1 = int(0.6 * sr), int(3 * sr)
    m[:f0] *= np.linspace(0, 1, f0)
    m[-f1:] *= np.linspace(1, 0, f1)
    return m.astype(np.float32)


def body_seconds(ep: Path) -> float:
    """Length of the episode picture (build/video.mp4); the audio body is cut/padded to it."""
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          str(ep / "build" / "video.mp4")]).strip())


def cut(ep: Path) -> float:
    """Episode time where the sting plays: 0 (before everything) unless script.json has "sting_after"."""
    import json
    sid = json.loads((ep / "script.json").read_text(encoding="utf-8")).get("sting_after")
    if not sid:
        return 0.0
    segs = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
    ids = list(segs)
    return round(segs[ids[ids.index(sid) + 1]]["start"] - 0.1, 3)


def shift(t: float, c: float) -> float:
    """Episode time -> time in the final video (with the sting inserted at c)."""
    return t + INTRO if t >= c else t


def wrap(buf: np.ndarray, sr: int, decode, ep: Path) -> np.ndarray:
    """intro sting + episode audio (fitted to the picture length) + outro music, matching the bumper videos.
    With a cold open the sting sits at cut(ep) instead of the very start."""
    n = int(round(body_seconds(ep) * sr))
    body = np.zeros(n, np.float32)
    body[: min(n, len(buf))] = buf[:n]
    k = int(round(cut(ep) * sr))
    return np.concatenate([body[:k], intro_audio(sr), body[k:], outro_audio(sr, decode)])


if __name__ == "__main__":
    render()
