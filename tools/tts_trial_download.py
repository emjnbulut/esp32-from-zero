"""Downloads for the TTS bake-off (user approved 2026-11-21). Run with .venv-tts python. Resumable (HF cache)."""
import time
from huggingface_hub import hf_hub_download, snapshot_download

jobs = [
    ("ResembleAI/chatterbox", ["t3_mtl23ls_v3.safetensors"]),
    ("ResembleAI/Chatterbox-Multilingual-hi", None),
    ("openbmb/VoxCPM2", None),
    ("mobiuslabsgmbh/faster-whisper-large-v3-turbo", None),
]
for repo, files in jobs:
    t = time.time()
    for attempt in range(5):
        try:
            if files:
                for f in files:
                    p = hf_hub_download(repo, f)
            else:
                p = snapshot_download(repo)
            break
        except Exception as e:  # noqa: BLE001
            print("retry", repo, attempt, e, flush=True)
            time.sleep(20)
    print("DONE", repo, p, f"{time.time() - t:.0f}s", flush=True)
