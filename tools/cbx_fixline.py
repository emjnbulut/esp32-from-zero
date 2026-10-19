"""Extra retakes for single dub lines after cbx_retake.py: tries more seeds and keeps the take that fits its slot
(schedule.json), has no stray sound or long pause, and the best Whisper match. Updates cache.json; then run
tools/dub.py <ep> <lang> to rebuild the dub track.

Usage: python tools/cbx_fixline.py video/ep02 tr s16,s27 [seeds, default 21-26]
"""
import json, sys, shutil, difflib, subprocess, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import cbx
from dub_check import load16k, words
from faster_whisper import WhisperModel
ep, lang, ids = ROOT / sys.argv[1], sys.argv[2], sys.argv[3].split(",")
seeds = [int(x) for x in (sys.argv[4] if len(sys.argv) > 4 else "21,22,23,24,25,26").split(",")]
dub = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))
sch = json.loads((ep / "build" / "schedule.json").read_text())["segments"]; order = list(sch)
out = ep / "build" / f"dub_{lang}"; tmp = out / "retakes"; tmp.mkdir(exist_ok=True)
cfg = cbx.settings(dub, lang)
tag = lambda s: cbx.key(cfg, dub["segments"][s])[:8]
todo = [(dub["segments"][s], tmp / f"{s}_x{seed}_{tag(s)}.mp3", seed) for s in ids for seed in seeds
        if not (tmp / f"{s}_x{seed}_{tag(s)}.mp3").exists()]
cbx.say(cfg, todo)
m = WhisperModel("small", device="cpu", compute_type="int8")
def check(p, text):
    audio = load16k(p); segs = list(m.transcribe(audio, language=lang, beam_size=5, word_timestamps=True)[0])
    match = difflib.SequenceMatcher(None, "".join(words(text)), "".join(words(" ".join(s.text for s in segs))), autojunk=False).ratio()
    fr = audio[: len(audio)//320*320].reshape(-1, 320); db = 10*np.log10((fr**2).mean(1)+1e-12)
    voiced = np.where(db > db.max()-38)[0]; gap = float(np.diff(voiced).max()-1)*0.02 if len(voiced) > 1 else 0
    near = np.zeros(len(db), bool)
    for w in (w for sg in segs for w in (sg.words or [])):
        near[max(0, int((w.start-0.3)/0.02)):int((w.end+0.3)/0.02)+1] = True
    junk = float(((db > db.max()-30) & ~near).sum())*0.02
    return match, gap, junk, len(audio)/16000
cache_p = out / "cache.json"; cache = json.loads(cache_p.read_text())
for s in ids:
    i = order.index(s); room = sch[order[i+1]]["start"] - sch[s]["start"] - 0.2 if i+1 < len(order) else 1e9
    best = None
    for p in [out / f"{s}.mp3"] + [tmp / f"{s}_x{seed}_{tag(s)}.mp3" for seed in seeds]:
        match, gap, junk, d = check(p, dub["segments"][s])
        score = (d/room <= 1.08, junk <= 0.25, gap <= 0.75, match - 0.2*junk)
        print(f"{s} {p.name:24s} match={match:.2f} gap={gap:.1f} junk={junk:.2f} x{d/room:.2f}")
        if best is None or score > best[0]: best = (score, p, d)
    if best[1] != out / f"{s}.mp3":
        shutil.copy(best[1], out / f"{s}.mp3"); cache[s]["duration"] = best[2]
    print(s, "->", best[1].name, "ok" if all(best[0][:3]) else "STILL WEAK")
cache_p.write_text(json.dumps(cache, indent=1), encoding="utf-8")
