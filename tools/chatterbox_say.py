"""Narrate a batch of lines with Chatterbox. Runs in its own venv (.venv-tts, see tools/CHATTERBOX.md);
tools/tts.py and tools/dub.py call it through tools/cbx.py.

Usage: .venv-tts/Scripts/python tools/chatterbox_say.py jobs.json
jobs.json: {"model": "en" | "multilingual", "lang": "en", "prompt": "voice.wav" | null,
            "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1, "items": [{"text": "...", "out": "s01.mp3"}]}
"""
import json
import subprocess
import sys

import torch


def load(cfg, device):
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
    if cfg.get("prompt"):
        opts["audio_prompt_path"] = cfg["prompt"]
    if cfg["model"] == "multilingual":
        opts["language_id"] = cfg.get("lang", "en")
    for n, item in enumerate(cfg["items"], 1):
        torch.manual_seed(cfg.get("seed", 1))  # same text + settings -> same take
        wav = tts.generate(item["text"], **opts).squeeze().cpu().numpy().astype("float32")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(tts.sr), "-ac", "1", "-i", "-",
                        "-b:a", "192k", item["out"]], input=wav.tobytes(), check=True)
        print(f"[{n}/{len(cfg['items'])}] {item['out']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
