"""Bridge to Chatterbox, which lives in its own venv (.venv-tts) because it needs torch.

A script or dub file opts in with  "engine": "chatterbox"  and optional settings:
  "cbx": {"model": "en" | "multilingual", "prompt": "tools/voice_samples/narrator.wav",
          "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1}
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv-tts" / "Scripts" / "python.exe"


# The channel's narrators. Since 2026-10-25 every language speaks with the creator's own voice (timbre, S3Gen)
# while the rhythm/accent model (T3) follows a native speaker of that language (accent_prompt).
# Sources: tools/voice_samples/README.md. Before: en mark, tr/pt pt_fleurs2, hi hi_fleurs5, es es_fleurs2 alone.
_S = "tools/voice_samples/"
VOICES = {
    "en": {"prompt": _S + "creator_en.wav", "accent_prompt": _S + "mark.wav"},        # user pick EN_3
    "tr": {"prompt": _S + "creator_tr.wav", "accent_prompt": _S + "tr_fleurs3.wav"},  # user pick TR_2
    "hi": {"prompt": _S + "creator_en.wav", "accent_prompt": _S + "hi_fleurs5.wav"},
    "pt": {"prompt": _S + "creator_en.wav", "accent_prompt": _S + "pt_fleurs2.wav"},
    "es": {"prompt": _S + "creator_en.wav", "accent_prompt": _S + "es_fleurs2.wav"},
}
# Dub voices that speak slower than the English narration are played this much faster (atempo) when the dub is
# laid out, so their slots need not stretch the English video (ep04 2026-10-26: es median x1.26, pt x1.21 vs en).
DUB_TEMPO = {"es": 1.15, "pt": 1.12}
ENGINE = "chatterbox"  # default for every script / dub / Short; a file can still say "engine": "edge"


def engine(spec: dict) -> str:
    return spec.get("engine", ENGINE)


PAUSES = {"sentence": 0.32, "comma": 0.12}  # seconds of silence at . ! ? : ; and at commas
# Voice clean-up on every take (user approved 2026-10-25): rumble cut, less mud, more presence, softer "s", gentle compression
POLISH = ("highpass=f=80,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,deesser=i=0.4,"
          "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120")


def settings(spec: dict, lang: str) -> dict:
    cfg = {"model": "en" if lang == "en" else "multilingual", "lang": lang, "prompt": None,
           "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1, "pauses": PAUSES, "polish": POLISH,
           "denoise": "deepfilternet"}  # DeepFilterNet in .venv-tts (pip deepfilternet deepfilterlib --no-deps, loguru, appdirs)
    cfg.update(VOICES.get(lang, {}))
    if cfg.get("accent_prompt"):
        cfg["accent_speaker"] = "prompt"  # T3 keeps the creator's speaker embedding too
    over = spec.get("cbx", {})
    if "prompt" in over:  # a file that picks its own voice drops the split-voice accent
        cfg.pop("accent_prompt", None)
        cfg.pop("accent_speaker", None)
    cfg.update(over)
    for k in ("prompt", "accent_prompt"):
        if cfg.get(k):
            cfg[k] = str((ROOT / cfg[k]).resolve())
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
        # The models are cached locally; offline mode keeps a slow or dropped connection from hanging the load
        # (2026-10-26: from_pretrained waited 5 hours on the Hugging Face hub).
        env = {**os.environ, "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
        subprocess.run([str(PY), str(ROOT / "tools" / "chatterbox_say.py"), str(jobs)], check=True, env=env)
