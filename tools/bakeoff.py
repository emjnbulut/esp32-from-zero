"""Local voice bake-off (tools/TTS_UPGRADE_RESEARCH.md 4d, local engines only - user 2026-11-21: voice never leaves the PC).

    python tools/bakeoff.py            # narrate every engine x line that is missing, then build the listening files
    python tools/bakeoff.py --mix      # only rebuild the listening files

Output: build/voice_test/bakeoff/<lang>/<engine>_<line>.mp3 (raw takes) and
        build/voice_test/bakeoff/DINLE_<lang>_<letter>.mp3 (3 lines, loudness-matched, letters shuffled per language).
The letter -> engine key is in build/voice_test/bakeoff/ANAHTAR.json (do not show it before the creator picks).
"""
import json
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cbx  # noqa: E402

ROOT = cbx.ROOT
OUT = ROOT / "build" / "voice_test" / "bakeoff"
S = ROOT / "tools" / "voice_samples"
VOX_PY = ROOT / ".venv-vox" / "Scripts" / "python.exe"

LINES = {
    "en": {
        "explain": "It has eight thousand little dots, and every dot makes its own light. That's why black on this "
                   "screen is truly black: those dots are simply off.",
        "terms": "The two chat wires: green from pin twenty-two to the clock leg, and blue from pin twenty-one to the data leg.",
        "mixed": "But the ESP32 also has a small drawer that keeps things without power. It's called Preferences.",
    },
    "tr": {
        "explain": "Üzerinde sekiz bine yakın küçük nokta var ve her nokta kendi ışığını üretiyor. Bu yüzden bu ekranda "
                   "siyah gerçekten siyah: o noktalar sadece kapalı.",
        "terms": "İki sohbet kablosu: yeşil kablo yirmi iki numaralı pinden saat bacağına, mavi kablo da yirmi bir "
                 "numaralı pinden veri bacağına.",
        "mixed": "Ama ESP otuz ikinin elektrik olmadan da bir şeyleri saklayan küçük bir çekmecesi var. Adı Preferıns.",
    },
    "hi": {
        "explain": "इस पर क़रीब आठ हज़ार छोटे-छोटे डॉट्स हैं, और हर डॉट अपनी रोशनी ख़ुद बनाता है। इसलिए इस स्क्रीन पर "
                   "काला सच में काला दिखता है: वो डॉट्स बस बंद होते हैं।",
        "terms": "दो चैट वाली तारें: हरी तार पिन बाईस से क्लॉक वाली टांग तक, और नीली तार पिन इक्कीस से डेटा वाली टांग तक।",
        "mixed": "लेकिन ई एस पी बत्तीस में एक छोटी सी दराज़ भी है, जो बिजली के बिना भी चीज़ें संभाल कर रखती है। "
                 "इसका नाम है प्रेफ़रेंसेज़।",
    },
}


def cbx_cfg(lang, **over):
    cfg = cbx.settings({}, lang)
    cfg.update(over)
    if over.get("own_accent"):
        cfg.pop("accent_prompt", None)
        cfg.pop("accent_speaker", None)
        cfg.pop("own_accent")
    for k in ("prompt", "accent_prompt"):
        if cfg.get(k):
            cfg[k] = str((ROOT / cfg[k]).resolve())
    return cfg


def vox_cfg(ref):
    return {"vox": True, "reference": str(ref), "cfg_value": 2.0, "steps": 10, "seed": 1, "polish": cbx.POLISH}


# engine id -> (description for the key, settings)
ENGINES = {
    # EN decided 2026-11-23: option B (tools/cbx.py VOICES en), no bake-off needed
    "tr": {
        "cbx_v2": ("Chatterbox Multilingual V2, today's voice", cbx_cfg("tr")),
        "cbx_v3": ("Chatterbox Multilingual V3, creator timbre + native accent", cbx_cfg("tr", mtl="v3")),
        "cbx_v3_own": ("Chatterbox Multilingual V3, 24 s creator reference, own accent",
                       cbx_cfg("tr", mtl="v3", prompt="tools/voice_samples/creator_tr_long.wav", own_accent=True)),
        "vox2": ("VoxCPM2, 24 s creator reference", vox_cfg(S / "creator_tr_long.wav")),
    },
    "hi": {
        "cbx_v2": ("Chatterbox Multilingual V2, today's voice", cbx_cfg("hi")),
        "cbx_v3": ("Chatterbox Multilingual V3", cbx_cfg("hi", mtl="v3", cfg_weight=0.3)),
        "cbx_hi": ("Chatterbox Multilingual-hi pack", cbx_cfg("hi", mtl="hi")),
        "vox2": ("VoxCPM2, 23 s creator EN reference", vox_cfg(S / "creator_en_long.wav")),
    },
}


def run_jobs(cfg, items):
    env = {**os.environ, "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "PYTHONIOENCODING": "utf-8"}
    with tempfile.TemporaryDirectory() as tmp:
        jobs = Path(tmp) / "jobs.json"
        body = {k: v for k, v in cfg.items() if k != "vox"}
        body["items"] = [{"text": t, "out": str(o)} for t, o in items]
        jobs.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        if cfg.get("vox"):
            cmd = [str(VOX_PY), str(ROOT / "tools" / "vox_say.py"), str(jobs)]
        else:
            cmd = [str(cbx.PY), str(ROOT / "tools" / "chatterbox_say.py"), str(jobs)]
        subprocess.run(cmd, check=True, env=env)


def narrate():
    for lang, engines in ENGINES.items():
        (OUT / lang).mkdir(parents=True, exist_ok=True)
        for eid, (_, cfg) in engines.items():
            items = [(text, OUT / lang / f"{eid}_{line}.mp3") for line, text in LINES[lang].items()]
            items = [it for it in items if not it[1].exists()]
            if items:
                print(f"== {lang} {eid}: {len(items)} lines", flush=True)
                try:
                    run_jobs(cfg, items)
                except subprocess.CalledProcessError as e:
                    print(f"!! {lang} {eid} failed: {e}", flush=True)


def mix():
    rng = random.Random(23)
    key = {}
    for lang, engines in ENGINES.items():
        ids = [e for e in engines if all((OUT / lang / f"{e}_{ln}.mp3").exists() for ln in LINES[lang])]
        rng.shuffle(ids)
        for letter, eid in zip("ABCDEFG", ids):
            key[f"{lang}_{letter}"] = {"engine": eid, "what": engines[eid][0]}
            files = [OUT / lang / f"{eid}_{ln}.mp3" for ln in LINES[lang]]
            inputs, parts = [], []
            for i, f in enumerate(files):
                inputs += ["-i", str(f)]
                parts.append(f"[{i}:a]aresample=48000,loudnorm=I=-18:TP=-1.5,apad=pad_dur=0.9[a{i}]")
            graph = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(len(files))) + \
                f"concat=n={len(files)}:v=0:a=1[out]"
            subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]",
                            "-b:a", "192k", str(OUT / f"DINLE_{lang}_{letter}.mp3")], check=True)
    (OUT / "ANAHTAR.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v["engine"] for k, v in key.items()}, indent=0))


if __name__ == "__main__":
    if "--mix" not in sys.argv:
        narrate()
    mix()
