"""Voice menu: the same two lines in every language, once per Chatterbox voice/style.

Usage: python tools/cbx_variants.py video/ep02 s03 s20 [--langs en,tr,hi,pt,es]
Writes build/voice_test/variants/<lang>/<n>_<voice>.mp3 (both lines joined) plus <lang>_all.mp3,
which plays every voice in order, so one file per language is enough to compare.
Clone prompts are public-domain LibriVox readings (tools/voice_samples/README.md).
"""
import argparse
import json
import subprocess
from pathlib import Path

import cbx

ROOT = Path(__file__).resolve().parent.parent

VOICES = [  # name, settings
    ("default", {}),
    ("calm", {"exaggeration": 0.35, "cfg_weight": 0.6}),
    ("lively", {"exaggeration": 0.75, "cfg_weight": 0.35}),
    ("mark_male", {"prompt": "tools/voice_samples/mark.wav"}),
    ("bob_male", {"prompt": "tools/voice_samples/bob.wav"}),
    ("kara_female", {"prompt": "tools/voice_samples/kara.wav"}),
    ("ruth_female", {"prompt": "tools/voice_samples/ruth.wav"}),
]

ap = argparse.ArgumentParser()
ap.add_argument("ep")
ap.add_argument("ids", nargs="+")
ap.add_argument("--langs", default="en,tr,hi,pt,es")
a = ap.parse_args()
ep = (ROOT / a.ep).resolve()


def concat(parts, out, gap=0.6):
    args, f = [], ""
    for n, p in enumerate(parts):
        args += ["-i", str(p)]
        f += f"[{n}:a]aresample=24000,aformat=channel_layouts=mono,apad=pad_dur={gap}[a{n}];"
    f += "".join(f"[a{n}]" for n in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", f, "-b:a", "160k", str(out)], check=True)


for lang in a.langs.split(","):
    if lang == "en":
        texts = {s["id"]: s["text"] for s in json.loads((ep / "script.json").read_text(encoding="utf-8"))["segments"]}
    else:
        texts = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))["segments"]
    out = ep / "build" / "voice_test" / "variants" / lang
    (out / "lines").mkdir(parents=True, exist_ok=True)
    joined = []
    for n, (name, spec) in enumerate(VOICES, 1):
        cfg = cbx.settings({"cbx": spec}, lang)
        lines = [out / "lines" / f"{name}_{sid}.mp3" for sid in a.ids]
        todo = [(texts[sid], p) for sid, p in zip(a.ids, lines) if not p.exists()]
        cbx.say(cfg, todo)
        joined.append(out / f"{n}_{name}.mp3")
        concat(lines, joined[-1], gap=0.4)
    concat(joined, out.parent / f"{lang}_all.mp3", gap=1.2)
    print("done:", lang, out.parent / f"{lang}_all.mp3", flush=True)
