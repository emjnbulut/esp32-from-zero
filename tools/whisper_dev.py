"""Where faster-whisper runs: the GPU (CUDA, int8_float16) when it works, else the CPU (int8).

The CUDA libraries come from the pip wheels nvidia-cublas-cu12 and nvidia-cudnn-cu12 (cuDNN 9) in .venv;
on Windows their DLL folders must be registered before ctranslate2 loads them.
WHISPER_DEVICE=cpu forces the old CPU path.
"""
import os
import sys
from pathlib import Path

_choice = None


def _add_cuda_dlls():
    if sys.platform != "win32":
        return
    for base in sys.path:
        nv = Path(base) / "nvidia"
        if nv.is_dir():
            for b in nv.glob("*/bin"):
                os.add_dll_directory(str(b))
                os.environ["PATH"] = str(b) + os.pathsep + os.environ.get("PATH", "")


def model(name="small"):
    """A WhisperModel on the best available device."""
    global _choice
    from faster_whisper import WhisperModel
    if _choice is None:
        _choice = ("cpu", "int8")
        if os.environ.get("WHISPER_DEVICE", "").lower() != "cpu":
            try:
                import ctranslate2
                if ctranslate2.get_cuda_device_count() > 0:
                    _add_cuda_dlls()
                    _choice = ("cuda", "int8_float16")  # int8 weights like the CPU path: near-identical transcripts, ~4x faster
            except Exception:
                pass
    try:
        return WhisperModel(name, device=_choice[0], compute_type=_choice[1])
    except Exception as e:  # missing/mismatched CUDA libraries: fall back to the CPU
        if _choice[0] == "cpu":
            raise
        print(f"whisper: GPU failed ({e}), using the CPU", file=sys.stderr)
        _choice = ("cpu", "int8")
        return WhisperModel(name, device="cpu", compute_type="int8")
