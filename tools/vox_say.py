"""Narrate a batch of lines with VoxCPM2 (runs in .venv-vox, see tools/CHATTERBOX.md "TTS upgrade trial").

Usage: .venv-vox/Scripts/python tools/vox_say.py jobs.json
jobs.json: {"reference": "voice.wav", "prompt_wav": null, "prompt_text": null, "cfg_value": 2.0, "steps": 10,
            "seed": 1, "polish": "ffmpeg -af chain", "items": [{"text": "...", "out": "x.mp3"}]}
The model's own denoiser stays off (we polish/denoise ourselves, same chain as Chatterbox).
"""
import json
import subprocess
import sys

import numpy as np
import torch


def main(path):
    cfg = json.loads(open(path, encoding="utf-8").read())
    from voxcpm import VoxCPM
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, local_files_only=True)
    sr = model.tts_model.sample_rate
    for n, item in enumerate(cfg["items"], 1):
        torch.manual_seed(item.get("seed", cfg.get("seed", 1)))
        np.random.seed(item.get("seed", cfg.get("seed", 1)))
        kw = {"reference_wav_path": cfg.get("reference")}
        if cfg.get("prompt_wav"):
            kw.update(prompt_wav_path=cfg["prompt_wav"], prompt_text=cfg["prompt_text"])
        wav = model.generate(text=item["text"], cfg_value=cfg.get("cfg_value", 2.0),
                             inference_timesteps=cfg.get("steps", 10), **kw).astype("float32")
        polish = ["-af", cfg["polish"]] if cfg.get("polish") else []
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", *polish,
                        "-b:a", "192k", item["out"]], input=wav.tobytes(), check=True)
        print(f"[{n}/{len(cfg['items'])}] {item['out']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
