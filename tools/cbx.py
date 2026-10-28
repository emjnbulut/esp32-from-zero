"""Bridge to Chatterbox, which lives in its own venv (.venv-tts) because it needs torch.

A script or dub file opts in with  "engine": "chatterbox"  and optional settings:
  "cbx": {"model": "en" | "multilingual", "prompt": "tools/voice_samples/narrator.wav",
          "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1}
"""
import json
import os
import re
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
VOWELS = re.compile(r"[aeiouyáéíóúâêîôûãõàèìòùäëïöüıœæ]+", re.I)


def syllables(text: str) -> int:
    """Rough syllable count: vowel groups for Latin scripts, aksharas (consonant or vowel not followed by a virama)
    for Devanagari. Only used to compare lines with their own language's pace limit."""
    n = sum(1 for m in re.finditer(r"[ऄ-औक-हक़-य़]", text)
            if text[m.end():m.end() + 1] != "्")
    return n + len(VOWELS.findall(re.sub(r"[ऀ-ॿ]", " ", text)))


# Pace per language in syllables per voiced second, for reports (tools/pace_check.py): a line above this is an outlier.
# Measured 2026-10-28 on the recap: EN 4.5, TR 5.0, HI 5.3 median, single lines up to 7.0 -> "rushed, jumpy".
# NOT enforced by time-stretching (that sounded robotic and too slow, user 2026-10-28); cbx_retake.py re-narrates
# lines whose pace is far from the episode's median instead.
MAX_SPS = {"en": 4.9, "tr": 5.4, "hi": 5.8, "pt": 5.8, "es": 6.2}
# Dubs used to be played up to 1.2x faster (base tempo) so they fit the English slots. User 2026-10-28: every
# language sounded rushed -> no base speed-up any more (DUB_TEMPO_MAX 1.0); build.py schedule lets the picture wait
# for the longest dub instead. The base-tempo code stays so the cap can be raised again on purpose.
DUB_TEMPO_MAX = 1.0
DUB_TEMPO_FIXED = {"tr": 1.0}


def dub_tempo(ep: Path, lang: str) -> float:
    if lang in DUB_TEMPO_FIXED:
        return DUB_TEMPO_FIXED[lang]
    b = ep / "build"
    try:
        en = json.loads((b / "audio" / "timings.json").read_text(encoding="utf-8"))
        dub = json.loads((b / f"dub_{lang}" / "cache.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return 1.0
    r = sorted(dub[s]["duration"] / en[s]["duration"] for s in en if s in dub and en[s]["duration"] > 0)
    return round(min(DUB_TEMPO_MAX, max(1.0, r[len(r) // 2])), 3) if r else 1.0


ENGINE = "chatterbox"  # default for every script / dub / Short; a file can still say "engine": "edge"


def engine(spec: dict) -> str:
    return spec.get("engine", ENGINE)


# seconds of silence after a piece, by the punctuation it ends on (user 2026-10-28: the narrator must breathe at
# punctuation; 0.32 / 0.12 s made sentences run into each other; 0.6 / 0.28 felt too slow)
PAUSES = {"sentence": 0.5, "question": 0.7, "colon": 0.35, "comma": 0.22}
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
