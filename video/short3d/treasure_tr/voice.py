"""Narration for the Turkish treasure-detector Short (creator's cloned voice, cbx.settings(spec, "tr")).

    .venv/Scripts/python video/short3d/treasure_tr/voice.py            # narrate missing/changed lines, Whisper retakes, schedule
    .venv/Scripts/python video/short3d/treasure_tr/voice.py --schedule # only rebuild voice.wav + schedule.json

1. every line of short.json is narrated into build/tr/<id>.mp3 (cached by text + voice settings in
   build/tr/cbx_cache.json, so only changed lines are narrated again), word times via tools/align.py
2. tools/cbx_retake.py <this dir> tr --short: Whisper listens to every line, weak lines get other seeds
3. build/voice.wav (48 kHz mono, the whole narration with pauses) + build/schedule.json:
   {"duration", "lines": [{"id", "vis", "text", "show", "t0", "t1", "words": [{"w", "t"}]}]} (Short seconds)
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import align  # noqa: E402
import cbx  # noqa: E402

SR = 48000
spec = json.loads((HERE / "short.json").read_text(encoding="utf-8"))
LANG = spec["lang"]
cfg = cbx.settings(spec, LANG)
B = HERE / "build"
V = B / LANG
V.mkdir(parents=True, exist_ok=True)
cache_p = V / "cbx_cache.json"


def load_cache():
    return json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}


def narrate():
    cache = load_cache()
    todo = []
    for s in spec["segments"]:
        text, mp3 = s["say"][LANG], V / f"{s['id']}.mp3"
        if cache.get(s["id"], {}).get("key") == cbx.key(cfg, text) and mp3.exists():
            continue
        todo.append((text, mp3))
    if todo:
        print(f"narrating {len(todo)} lines", flush=True)
        cbx.say(cfg, todo)
    for text, mp3 in todo:
        cache[mp3.stem] = {"key": cbx.key(cfg, text), "text": text,
                           "words": [w["t"] for w in align.align(mp3, text, LANG)]}
    cache_p.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def trim_tail(a, keep=0.12):
    """drop the quiet tail Chatterbox sometimes leaves after the last word (room noise, > 40 dB below the voice)"""
    hop = SR // 50
    fr = a[: len(a) // hop * hop].reshape(-1, hop)
    db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    loud = np.where(db > db.max() - 40)[0]
    if not len(loud):
        return a
    end = min(len(a), (loud[-1] + 1) * hop + int(keep * SR))
    out = a[:end].copy()
    f = min(len(out), int(0.05 * SR))
    out[-f:] *= np.linspace(1, 0, f, dtype=np.float32)
    return out


def schedule():
    cache = load_cache()
    lead, gap, tail = spec.get("lead", 0.2), spec.get("gap", 0.25), spec.get("tail", 1.4)
    out, lines, t = [np.zeros(int(lead * SR), np.float32)], [], lead
    for s in spec["segments"]:
        pre = s.get("before", 0.0)
        if pre:
            out.append(np.zeros(int(pre * SR), np.float32))
            t += pre
        text, mp3 = s["say"][LANG], V / f"{s['id']}.mp3"
        a = trim_tail(decode(mp3))
        names = align.script_words(text)
        ts = cache.get(s["id"], {}).get("words")
        if not ts or len(ts) != len(names):
            ts = [w["t"] for w in align.align(mp3, text, LANG)]
        lines.append({"id": s["id"], "vis": s["vis"], "text": text, "show": s.get("show", text), "t0": round(t, 3),
                      "t1": round(t + len(a) / SR, 3), "words": [{"w": w, "t": round(t + x, 3)} for w, x in zip(names, ts)]})
        out += [a, np.zeros(int(gap * SR), np.float32)]
        t += len(a) / SR + gap
    out.append(np.zeros(int(tail * SR), np.float32))
    t += tail
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(B / "voice.wav")],
                   input=np.concatenate(out).tobytes(), check=True)
    (B / "schedule.json").write_text(json.dumps({"duration": round(t, 3), "lines": lines}, indent=1, ensure_ascii=False),
                                     encoding="utf-8")
    print("schedule.json: duration", round(t, 2), "s")


if __name__ == "__main__":
    if "--schedule" not in sys.argv:
        narrate()
        subprocess.run([sys.executable, str(ROOT / "tools" / "cbx_retake.py"), str(HERE.relative_to(ROOT)), LANG, "--short"],
                       cwd=ROOT, check=True)
    schedule()
