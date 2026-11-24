"""Build the phone-doorbell Short (Episode 12 phone control) end to end, EN or TR (run from the repo root with the repo venv):

    .venv/Scripts/python video/short3d/doorbell/make.py --lang en               # everything that is missing
    .venv/Scripts/python video/short3d/doorbell/make.py --lang tr voice         # 1 narration (+ Whisper retakes) -> schedule.json
    .venv/Scripts/python video/short3d/doorbell/make.py --lang tr render         # 2 Blender, one process per shot (resumable)
    .venv/Scripts/python video/short3d/doorbell/make.py --lang en compose mix final thumb
    .venv/Scripts/python video/short3d/doorbell/make.py --lang en --renarrate   # new narration -> re-time -> re-render all shots

Steps: voice (voice.py) -> render (scene3d.py per shot, PBL_SAMPLES=16) -> repair -> compose (compose.py: rings,
labels, captions, on-screen text, CTA) -> mix (mix.py: narration + buzzer + effects + music) -> final
(build/doorbell_<lang>_final.mp4, build/doorbell_<lang>_upload.mp4 < 10 MB HEVC) -> thumb (build/thumb_<lang>.jpg).
Everything language-specific lives in build/<lang>/. Heavy steps wait while another blender.exe or Chatterbox job
runs (16 GB PC shared with other renders).
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LANG = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else "en"
assert LANG in ("en", "tr"), LANG
os.environ["DOORBELL_LANG"] = LANG
B = HERE / "build"
BL = B / LANG
BLENDER = os.environ.get("BLENDER", "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe")
PY = sys.executable
THUMB_T = 1.6  # the hook: just after the ding - DING on screen, rings at the buzzer, "RING!" on the OLED
sys.path.insert(0, str(HERE))


def busy(tts=True):
    """other heavy jobs: Blender (one at a time) and, for the narration, Chatterbox (two on the 8 GB GPU stall)"""
    tts_q = " -or ($_.Name -eq 'python.exe' -and $_.CommandLine -like '*chatterbox*')" if tts else ""
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'blender.exe'" + tts_q + " } | "
                          "Select-Object -ExpandProperty ProcessId"], capture_output=True, text=True).stdout.split()
    return [p for p in out if p.strip() and int(p) != os.getpid()]


def free_gb():
    out = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"],
                         capture_output=True, text=True).stdout.strip()
    return int(out or 0) / 1024 / 1024


MIN_FREE_GB = float(os.environ.get("MIN_FREE_GB", "3.5"))  # a 1080x1920 EEVEE shot needs ~2-3 GB; VoxCPM dubs take 8 GB


def wait_free(tts=True):
    while True:
        b, g = busy(tts), free_gb()
        if not b and g >= MIN_FREE_GB:
            return
        print(f"waiting: other blender / chatterbox job {b}, {g:.1f} GB free", flush=True)
        time.sleep(60)


def voice():
    wait_free()
    subprocess.run([PY, str(HERE / "voice.py"), "--lang", LANG], cwd=ROOT, check=True)


def shots():
    import story
    return story.Story(LANG).shots


def render(force=False):
    env = {**os.environ, "PBL_SAMPLES": os.environ.get("PBL_SAMPLES", "16")}
    for sh in shots():
        d = BL / "shots" / sh["id"]
        if force and d.exists():
            shutil.rmtree(d)
        done = len(list(d.glob("f_*.png"))) if d.exists() else 0
        anc = d / "anchors.json"
        if done >= sh["n"] and anc.exists() and json.loads(anc.read_text())["n"] == sh["n"]:
            continue
        wait_free(tts=False)  # a render can share the GPU with a narration job; RAM is the limit
        print(f"render {LANG} {sh['id']}: {done}/{sh['n']} frames there", flush=True)
        with open(BL / f"render_{sh['id']}.log", "w") as log:
            subprocess.run([BLENDER, "-b", "-P", str(HERE / "scene3d.py"), "--", "--lang", LANG, "--shot", sh["id"]],
                           cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)


def broken(d):
    """frames a killed Blender left half-written"""
    from PIL import Image
    bad = []
    for p in sorted(d.glob("f_*.png")):
        try:
            with Image.open(p) as im:
                im.load()
        except Exception:  # noqa: BLE001
            bad.append(int(p.stem[2:]))
    return bad


def repair():
    env = {**os.environ, "PBL_SAMPLES": os.environ.get("PBL_SAMPLES", "16")}
    for sh in shots():
        d = BL / "shots" / sh["id"]
        bad = broken(d) if d.exists() else []
        if bad:
            wait_free(tts=False)
            print(f"repair {LANG} {sh['id']}: frames {bad}", flush=True)
            subprocess.run([BLENDER, "-b", "-P", str(HERE / "scene3d.py"), "--", "--lang", LANG, "--shot", sh["id"],
                            "--frames", ",".join(map(str, bad))], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, check=True)


def compose():
    subprocess.run([PY, str(HERE / "compose.py"), "--lang", LANG], cwd=ROOT, check=True)


def mix():
    subprocess.run([PY, str(HERE / "mix.py"), "--lang", LANG], cwd=ROOT, check=True)


def final():
    pic, aud = BL / "picture.mp4", BL / "audio.wav"
    out = B / f"doorbell_{LANG}_final.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(pic), "-i", str(aud), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)]))
    # upload copy under 10 MB (HEVC like the other 3D Shorts): video bitrate from the size budget
    kbps = int((9.6 * 8 * 1024 / dur) - 130)
    up = B / f"doorbell_{LANG}_upload.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-c:v", "libx265", "-preset", "slow", "-b:v", f"{kbps}k",
                    "-maxrate", f"{int(kbps * 1.6)}k", "-bufsize", f"{kbps * 2}k", "-tag:v", "hvc1", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(up)], check=True)
    print(f"final {out.name} {dur:.1f} s {out.stat().st_size / 1e6:.1f} MB; upload {up.stat().st_size / 1e6:.2f} MB")


def thumb():
    subprocess.run([PY, str(HERE / "compose.py"), "--lang", LANG, "--thumb", str(THUMB_T)], cwd=ROOT, check=True)


STEPS = {"voice": voice, "render": render, "repair": repair, "compose": compose, "mix": mix, "final": final, "thumb": thumb}

if __name__ == "__main__":
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--lang"]
    if "--renarrate" in sys.argv:
        voice()
        render(force=True)
        repair(); compose(); mix(); final(); thumb()
    elif args:
        for a in args:
            STEPS[a]()
    else:
        if not (BL / "schedule.json").exists():
            voice()
        render(); repair(); compose(); mix(); final(); thumb()
