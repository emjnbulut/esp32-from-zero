"""Narrate a batch of lines with Chatterbox. Runs in its own venv (.venv-tts, see tools/CHATTERBOX.md);
tools/tts.py and tools/dub.py call it through tools/cbx.py.

Usage: .venv-tts/Scripts/python tools/chatterbox_say.py jobs.json
jobs.json: {"model": "en" | "multilingual", "lang": "en", "prompt": "voice.wav" | null,
            "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1, "pauses": {"sentence": 0.32, "comma": 0.12},
            "accent_prompt": "native.wav" (optional), "accent_speaker": "prompt" (optional), "polish": "ffmpeg -af chain",
            "denoise": "deepfilternet" (optional),
            "items": [{"text": "...", "out": "s01.mp3"}]}

Punctuation: every line is cut into sentences (. ! ? : ; ...) and, when both sides are long enough, at
commas; each piece is narrated on its own, trimmed, and joined with a fixed pause, so the narrator always
stops at a full stop and breathes at a comma. Numbers like 3.3 or 1,3 are never split.
"""
import json
import re
import subprocess
import sys

import numpy as np
import torch

SENT = re.compile(r"(?<=[.!?:;…])\s+")
COMMA = re.compile(r"(?<=,)\s+")
MIN_WORDS = 3  # a comma piece shorter than this stays attached (very short inputs narrate badly)


def pieces(text: str):
    """[(piece, pause_after_kind)] with kind 'sentence' | 'comma' | None (last)."""
    out = []
    sents = []
    for x in [x for x in SENT.split(text.strip()) if x]:
        # A sentence of one or two words ("Watch this.") narrated alone often starts with a stray mumble;
        # it rides along with the next sentence instead (the model still pauses at the full stop).
        if sents and len(sents[-1].split()) < MIN_WORDS:
            sents[-1] += " " + x
        else:
            sents.append(x)
    if len(sents) > 1 and len(sents[-1].split()) < MIN_WORDS:  # a short last sentence joins the one before
        last = sents.pop()
        sents[-1] += " " + last
    for si, sent in enumerate(sents):
        parts = []
        for c in [x for x in COMMA.split(sent) if x]:
            if parts and (len(c.split()) < MIN_WORDS or len(parts[-1].split()) < MIN_WORDS):
                parts[-1] += " " + c
            else:
                parts.append(c)
        for ci, c in enumerate(parts):
            last_in_sent = ci == len(parts) - 1
            kind = None if (last_in_sent and si == len(sents) - 1) else ("sentence" if last_in_sent else "comma")
            out.append((c, kind))
    return out


def trim(wav: np.ndarray, sr: int, thresh_db=-35.0, keep=0.05):
    """Cut leading/trailing silence, keeping `keep` seconds around the speech."""
    hop = int(sr * 0.01)
    if len(wav) < hop * 3:
        return wav
    fr = wav[: len(wav) // hop * hop].reshape(-1, hop)
    db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    loud = np.where(db > db.max() + thresh_db)[0]
    if not len(loud):
        return wav
    a = max(0, loud[0] * hop - int(keep * sr))
    b = min(len(wav), (loud[-1] + 1) * hop + int(keep * sr))
    return wav[a:b]


def patch_analyzer():
    """Chatterbox's alignment analyzer indexes A[:, :-5], which is empty for pieces of 5 text tokens or less
    ("Başlayalım.") and raises IndexError on every seed. Skip its check for that step instead;
    cbx_retake.py still catches the long tails it would have cut."""
    from chatterbox.models.t3.inference import alignment_stream_analyzer as asa
    step = asa.AlignmentStreamAnalyzer.step

    def safe_step(self, logits, *args, **kwargs):
        try:
            return step(self, logits, *args, **kwargs)
        except IndexError:
            return logits
    asa.AlignmentStreamAnalyzer.step = safe_step


def load(cfg, device):
    patch_analyzer()
    if cfg["model"] == "multilingual":
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        return ChatterboxMultilingualTTS.from_pretrained(device=device)
    from chatterbox.tts import ChatterboxTTS
    return ChatterboxTTS.from_pretrained(device=device)


def main(path):
    cfg = json.loads(open(path, encoding="utf-8").read())
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = load(cfg, device)
    opts = {"exaggeration": cfg.get("exaggeration", 0.5), "cfg_weight": cfg.get("cfg_weight", 0.5)}
    if cfg.get("prompt") and cfg.get("accent_prompt"):
        # Split voice: the text-to-speech-token model (T3: rhythm, accent) follows accent_prompt, the decoder
        # (S3Gen: timbre) follows prompt. accent_speaker "prompt" keeps prompt's speaker embedding in T3 too.
        tts.prepare_conditionals(cfg["accent_prompt"], exaggeration=opts["exaggeration"])
        t3 = tts.conds.t3
        tts.prepare_conditionals(cfg["prompt"], exaggeration=opts["exaggeration"])
        if cfg.get("accent_speaker") == "prompt":
            t3.speaker_emb = tts.conds.t3.speaker_emb
        tts.conds.t3 = t3
    elif cfg.get("prompt"):
        opts["audio_prompt_path"] = cfg["prompt"]
    if cfg["model"] == "multilingual":
        opts["language_id"] = cfg.get("lang", "en")
    pauses = cfg.get("pauses") or {}
    denoiser = None
    if cfg.get("denoise") == "deepfilternet":
        # Removes the faint hiss/rasp Chatterbox leaves in its takes (tools/CHATTERBOX.md, 2026-10-25)
        import warnings
        warnings.filterwarnings("ignore", module="df")
        from df.enhance import enhance, init_df
        denoiser = init_df(log_level="ERROR")[:2]

    def denoise(x):
        y = enhance(denoiser[0], denoiser[1], torch.from_numpy(x.copy())[None], atten_lim_db=None)
        return y.squeeze().cpu().numpy().astype("float32")

    def gen(text):
        for attempt in range(4):  # chatterbox's alignment analyzer sometimes crashes (IndexError) on a take
            try:
                return tts.generate(text, **opts).squeeze().cpu().numpy().astype("float32")
            except IndexError:
                if attempt == 3:
                    raise
                torch.manual_seed(1000 + attempt)

    for n, item in enumerate(cfg["items"], 1):
        torch.manual_seed(item.get("seed", cfg.get("seed", 1)))  # same text + settings -> same take
        if pauses:
            chunks = []
            for piece, kind in pieces(item["text"]):
                w = trim(gen(piece), tts.sr)
                chunks.append(w)
                if kind:
                    chunks.append(np.zeros(int(pauses.get(kind, 0.3) * tts.sr), dtype="float32"))
            wav = np.concatenate(chunks)
        else:
            wav = gen(item["text"])
        polish = ["-af", cfg["polish"]] if cfg.get("polish") else []
        sr = tts.sr
        if denoiser:  # same order the user approved (2026-10-25): polish, then DeepFilterNet
            raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", *polish,
                                  "-ar", str(denoiser[1].sr()), "-f", "f32le", "-"],
                                 input=wav.tobytes(), capture_output=True, check=True).stdout
            wav, sr, polish = denoise(np.frombuffer(raw, np.float32)), denoiser[1].sr(), []
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-",
                        *polish, "-b:a", "192k", item["out"]], input=wav.tobytes(), check=True)
        print(f"[{n}/{len(cfg['items'])}] {item['out']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
