"""Voice test: narrate a few lines with Chatterbox next to the current edge-tts takes.

Usage: python tools/cbx_compare.py video/ep02 s03 s10 s20 [--lang tr] [--prompt tools/voice_samples/x.wav]
Writes build/voice_test/<id>_edge.mp3 and <id>_cbx.mp3 (for --lang tr: the dub_tr takes and the dub text).
"""
import argparse
import json
import shutil
from pathlib import Path

import cbx

ROOT = Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("ep")
ap.add_argument("ids", nargs="+")
ap.add_argument("--lang", default="en")
ap.add_argument("--prompt")
a = ap.parse_args()
ep = (ROOT / a.ep).resolve()
if a.lang == "en":
    texts = {s["id"]: s["text"] for s in json.loads((ep / "script.json").read_text(encoding="utf-8"))["segments"]}
    edge_dir = ep / "build" / "audio"
else:
    texts = json.loads((ep / "dub" / f"{a.lang}.json").read_text(encoding="utf-8"))["segments"]
    edge_dir = ep / "build" / f"dub_{a.lang}"
out = ep / "build" / "voice_test"
out.mkdir(parents=True, exist_ok=True)
cfg = cbx.settings({"cbx": {"prompt": a.prompt}} if a.prompt else {}, a.lang)
for sid in a.ids:
    if (edge_dir / f"{sid}.mp3").exists():
        shutil.copy(edge_dir / f"{sid}.mp3", out / f"{sid}_{a.lang}_edge.mp3")
cbx.say(cfg, [(texts[sid], out / f"{sid}_{a.lang}_cbx.mp3") for sid in a.ids])
print("listen:", out)
