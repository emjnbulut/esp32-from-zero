"""Narration for the 3D treasure-detector Short: Chatterbox (channel voice) -> Whisper check -> word timings -> schedule.

  python video/short3d/treasure/voice.py [script.json] [prefix]   (cached: only changed lines are narrated again)
  e.g. voice.py script_build.json build_  -> build/build_voice.wav, build/build_schedule.json, build/voice_build/

Writes build/voice/<id>.mp3, build/voice.wav (the whole narration, 48 kHz mono) and build/schedule.json:
  {"duration": s, "lines": [{"id", "text", "t0", "t1", "words": [{"w", "t"}]}]}   (times in Short seconds)
"""
import difflib
import json
import re
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
LEAD, GAP, TAIL = 0.25, 0.28, 1.6
# extra breathing room before a line (seconds): the Short's beats
BEFORE = {"l03": 0.2, "l06": 0.25, "l07": 0.1, "l08": 0.25, "l09": 0.9, "l12": 0.2, "l13": 0.25}

SCRIPT = sys.argv[1] if len(sys.argv) > 1 else "script.json"
PREFIX = sys.argv[2] if len(sys.argv) > 2 else ""
spec = json.loads((HERE / SCRIPT).read_text(encoding="utf-8"))
BEFORE.update(spec.get("before", {}))
LEAD, TAIL = spec.get("lead", LEAD), spec.get("tail", TAIL)
build = HERE / "build"
vdir = build / ("voice_" + PREFIX.rstrip("_") if PREFIX else "voice")
vdir.mkdir(parents=True, exist_ok=True)
cfg = cbx.settings(spec, "en")
cache_p = vdir / "cache.json"
cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}


def norm_words(s):
    return [w for w in re.sub(r"[^a-z0-9' ]", " ", s.lower()).split() if w]


def heard(path, text):
    segs, _ = align.model().transcribe(align.load16k(path), language="en", initial_prompt=None)
    return " ".join(s.text for s in segs)


def score(path, text):
    a, b = norm_words(text.replace("ESP32", "esp32").replace("map()", "map")), norm_words(heard(path, text))
    return difflib.SequenceMatcher(None, a, b).ratio()


for attempt in range(4):
    todo = []
    for ln in spec["lines"]:
        k = cbx.key(cfg, ln["text"]) + f"-s{attempt}"
        c = cache.get(ln["id"], {})
        if c.get("ok") and (vdir / f"{ln['id']}.mp3").exists() and c.get("text") == ln["text"]:
            continue
        todo.append((ln["text"], vdir / f"{ln['id']}.mp3", 1 + attempt * 17))
        cache[ln["id"]] = {"text": ln["text"], "key": k}
    if not todo:
        break
    print(f"narrating {len(todo)} lines (attempt {attempt})", flush=True)
    cbx.say(cfg, todo)
    for text, path, _ in todo:
        lid = path.stem
        sc = score(path, text)
        cache[lid]["score"] = round(sc, 3)
        cache[lid]["ok"] = sc >= 0.85 or attempt == 3
        print(lid, "match", round(sc, 3), "OK" if cache[lid]["ok"] else "retake", flush=True)
    cache_p.write_text(json.dumps(cache, indent=1))


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


out, lines, t = [], [], LEAD
out.append(np.zeros(int(LEAD * SR), np.float32))
for ln in spec["lines"]:
    pre = BEFORE.get(ln["id"], 0.0)
    if pre:
        out.append(np.zeros(int(pre * SR), np.float32)); t += pre
    p = vdir / f"{ln['id']}.mp3"
    a = decode(p)
    words = [{"w": w["w"], "t": round(t + w["t"], 3)} for w in align.align(p, ln["text"], "en")]
    lines.append({"id": ln["id"], "text": ln["text"], "t0": round(t, 3), "t1": round(t + len(a) / SR, 3), "words": words})
    out.append(a); t += len(a) / SR
    out.append(np.zeros(int(GAP * SR), np.float32)); t += GAP
out.append(np.zeros(int(TAIL * SR), np.float32)); t += TAIL
voice = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(build / (PREFIX + "voice.wav"))],
               input=voice.tobytes(), check=True)
(build / (PREFIX + "schedule.json")).write_text(json.dumps({"duration": round(t, 3), "lines": lines}, indent=1))
print("duration", round(t, 2), "s")
