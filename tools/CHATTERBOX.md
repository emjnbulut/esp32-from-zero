# Chatterbox narration (local TTS)

Chatterbox needs torch, so it lives in its own venv `.venv-tts` (gitignored). The main `.venv` only talks
to it through `tools/cbx.py`; word timings for the scenes come from `tools/align.py` (faster-whisper,
already installed; checked on ep03's edge-tts takes: same words, mean error 0.06 s).

## Setup (one time, ~5-7 GB download: torch CUDA + model weights)
Chatterbox is tested on Python 3.11; with 3.12 its pinned numpy may not install.

    py install 3.11                       # Python install manager (or python.org installer)
    py -3.11 -m venv .venv-tts
    .venv-tts/Scripts/python -m pip install chatterbox-tts
    # pip installs a CPU-only torch on Windows; swap in the CUDA build of the SAME version it chose:
    .venv-tts/Scripts/python -m pip show torch          # e.g. 2.6.0
    .venv-tts/Scripts/python -m pip install --force-reinstall torch==<ver> torchaudio==<ver> --index-url https://download.pytorch.org/whl/cu124
    .venv-tts/Scripts/python -c "import torch; print(torch.cuda.is_available())"   # True on the RTX 4060

The weights download from Hugging Face on the first run.

Done on 2026-10-18 with uv instead (Python 3.11.17, chatterbox-tts 0.1.7, torch 2.6.0+cu124):

    uv python install 3.11 && uv venv .venv-tts --python 3.11
    uv pip install --python .venv-tts/Scripts/python.exe chatterbox-tts "setuptools<81"
    uv pip install --python .venv-tts/Scripts/python.exe --reinstall torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

`setuptools<81` is needed: the watermarker (perth) imports `pkg_resources`, otherwise
`PerthImplicitWatermarker` is None. Speed on the RTX 4060: ~40 it/s, about 4 s per line.

## Voice test (before switching anything)

    python tools/cbx_compare.py video/ep02 s03 s10 s20 s30
    python tools/cbx_compare.py video/ep02 s03 s10 s20 s30 --lang tr
    # optional voice clone (10-20 s clean recording, only of a voice we may use):
    python tools/cbx_compare.py video/ep02 s03 s10 --prompt tools/voice_samples/narrator.wav

Listen in `video/ep02/build/voice_test/` (`*_edge.mp3` vs `*_cbx.mp3`).

## Switching an episode
In `script.json` (or `dub/<lang>.json`) add:

    "engine": "chatterbox",
    "cbx": {"prompt": "tools/voice_samples/narrator.wav", "exaggeration": 0.5, "cfg_weight": 0.5, "seed": 1}

(`cbx` is optional; English uses the English model, other languages the multilingual one.)
For ep03 the script comes from `video/ep03/make_script.py`: put the keys there, then

    python video/ep03/make_script.py
    python tools/tts.py video/ep03 && python tools/build.py video/ep03 schedule
    cd video && node engine/render.mjs ep03 && cd ..
    python tools/build.py video/ep03 audio && python tools/build.py video/ep03 subs && python tools/build.py video/ep03 compose
    python video/ep03/make_localize.py      # chapter times follow the new narration

A take is cached by text + settings; change `seed` to get a different take of every line, or delete
`build/audio/<id>.mp3` to redo one line. Check takes with `tools/dub_check.py` for the dubs.

## Voice menu (2026-10-18)
`python tools/cbx_variants.py video/ep02 s03 s20` narrates two lines per language with 7 voices/styles
(default, calm, lively, and clones of four public-domain LibriVox readers: mark, bob, kara, ruth) →
`build/voice_test/variants/<lang>_all.mp3`. The clone prompts live in `tools/voice_samples/` (gitignored;
sources and the ffmpeg cut are in its README). **Chosen narrator: mark** (Mark F. Smith,
`tools/voice_samples/mark.wav`): Whisper match 1.00 in English, ~164 wpm.

## Creator's own voice (2026-10-25)
All languages now speak with the creator's voice: `tools/cbx.py` VOICES gives each language a `prompt`
(timbre, S3Gen) = `creator_en.wav` (`creator_tr.wav` for Turkish) and an `accent_prompt` (rhythm/accent, T3) =
a native speaker (en mark, tr tr_fleurs3, hi hi_fleurs5, pt pt_fleurs2, es es_fleurs2); T3 keeps the creator's
speaker embedding (`accent_speaker: "prompt"`). Every take also gets `cbx.POLISH` (EQ, de-esser, light compression).
References (gitignored): creator recordings `footage/voice/{en,tr}_raw.m4a`, cut with
`ffmpeg -ss 18.75 -t 15.6` (en) / `-ss 13.85 -t 14.2` (tr) `-ac 1 -ar 24000 -af "highpass=f=70,loudnorm=I=-18"`.
A file whose `cbx` sets its own `prompt` drops the accent split. Published episodes ep01-ep04 used the old voices.
