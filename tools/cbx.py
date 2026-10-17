"""Bridge to Chatterbox, which lives in its own venv (.venv-tts) because it needs torch.

A script or dub file opts in with  "engine": "chatterbox"  and optional settings:
  "cbx": {"model": "en" | "multilingual", "prompt": "tools/voice_samples/narrator.wav",
          "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1}
"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv-tts" / "Scripts" / "python.exe"


def settings(spec: dict, lang: str) -> dict:
    cfg = {"model": "en" if lang == "en" else "multilingual", "lang": lang, "prompt": None,
           "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1}
    cfg.update(spec.get("cbx", {}))
    if cfg["prompt"]:
        cfg["prompt"] = str((ROOT / cfg["prompt"]).resolve())
    return cfg


def key(cfg: dict, text: str) -> str:
    """Cache key: changes when the text or any voice setting changes."""
    import hashlib
    return hashlib.sha1(json.dumps([cfg, text], sort_keys=True).encode()).hexdigest()


def say(cfg: dict, items: list):
    """items: [(text, out_mp3)]. Narrates them all in one run (the model loads once)."""
    if not items:
        return
    if not PY.exists():
        raise SystemExit(f"Chatterbox venv missing: {PY} (setup in tools/CHATTERBOX.md)")
    with tempfile.TemporaryDirectory() as tmp:
        jobs = Path(tmp) / "jobs.json"
        jobs.write_text(json.dumps({**cfg, "items": [{"text": t, "out": str(o)} for t, o in items]},
                                   ensure_ascii=False), encoding="utf-8")
        subprocess.run([str(PY), str(ROOT / "tools" / "chatterbox_say.py"), str(jobs)], check=True)
