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


# The channel's narrators (chosen 2026-10-18, sources in tools/voice_samples/README.md)
VOICES = {
    "en": "tools/voice_samples/mark.wav",        # Mark F. Smith, LibriVox (public domain)
    "tr": "tools/voice_samples/tr_fleurs2.wav",  # FLEURS speakers (CC BY 4.0), picked by the user (tr)
    "hi": "tools/voice_samples/hi_fleurs5.wav",  # and by Whisper score + closeness to mark/tr (hi, pt, es)
    "pt": "tools/voice_samples/pt_fleurs2.wav",
    "es": "tools/voice_samples/es_fleurs2.wav",
}
ENGINE = "chatterbox"  # default for every script / dub / Short; a file can still say "engine": "edge"


def engine(spec: dict) -> str:
    return spec.get("engine", ENGINE)


PAUSES = {"sentence": 0.32, "comma": 0.12}  # seconds of silence at . ! ? : ; and at commas


def settings(spec: dict, lang: str) -> dict:
    cfg = {"model": "en" if lang == "en" else "multilingual", "lang": lang, "prompt": VOICES.get(lang),
           "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1, "pauses": PAUSES}
    cfg.update(spec.get("cbx", {}))
    if cfg["prompt"]:
        cfg["prompt"] = str((ROOT / cfg["prompt"]).resolve())
    return cfg


def key(cfg: dict, text: str) -> str:
    """Cache key: changes when the text or any voice setting changes."""
    import hashlib
    return hashlib.sha1(json.dumps([cfg, text], sort_keys=True).encode()).hexdigest()


def say(cfg: dict, items: list):
    """items: [(text, out_mp3)] or [(text, out_mp3, seed)]. Narrates them all in one run (the model loads once)."""
    if not items:
        return
    if not PY.exists():
        raise SystemExit(f"Chatterbox venv missing: {PY} (setup in tools/CHATTERBOX.md)")
    with tempfile.TemporaryDirectory() as tmp:
        jobs = Path(tmp) / "jobs.json"
        jobs.write_text(json.dumps({**cfg, "items": [{"text": it[0], "out": str(it[1]), **({"seed": it[2]} if len(it) > 2 else {})}
                                                     for it in items]},
                                   ensure_ascii=False), encoding="utf-8")
        subprocess.run([str(PY), str(ROOT / "tools" / "chatterbox_say.py"), str(jobs)], check=True)
