"""Build the Turkish treasure-detector Short end to end (run from the repo root with the repo venv):

    .venv/Scripts/python video/short3d/treasure_tr/make.py               # everything that is missing
    .venv/Scripts/python video/short3d/treasure_tr/make.py voice         # 1 narration (+ Whisper retakes) -> schedule.json
    .venv/Scripts/python video/short3d/treasure_tr/make.py render        # 2 Blender, one process per shot (resumable)
    .venv/Scripts/python video/short3d/treasure_tr/make.py compose mix final
    .venv/Scripts/python video/short3d/treasure_tr/make.py --renarrate   # new narration -> re-time -> re-render all shots

Steps: voice (voice.py) -> render (scene3d.py per shot, PBL_SAMPLES=16) -> compose (compose.py: tags, sound-wave rings,
captions, Turkish on-screen text, CTA) -> mix (mix.py: narration + buzzer + effects + music) -> final
(build/treasure_tr_final.mp4, build/treasure_tr_upload.mp4 < 10 MB, build/thumb.jpg).
Heavy steps wait while another blender.exe or Chatterbox job runs (16 GB PC shared with other renders).
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
B = HERE / "build"
BLENDER = os.environ.get("BLENDER", "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe")
PY = sys.executable
sys.path.insert(0, str(HERE))


def busy():
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'blender.exe' -or "
                          "($_.Name -eq 'python.exe' -and $_.CommandLine -like '*chatterbox*') } | "
                          "Select-Object -ExpandProperty ProcessId"], capture_output=True, text=True).stdout.split()
    return [p for p in out if p.strip() and int(p) != os.getpid()]


def wait_free():
    while True:
        b = busy()
        if not b:
            return
        print("waiting: another blender / chatterbox job runs", b, flush=True)
        time.sleep(60)


def voice():
    wait_free()
    subprocess.run([PY, str(HERE / "voice.py")], cwd=ROOT, check=True)


def shots():
    import story
    return story.Story().shots


def render(force=False):
    env = {**os.environ, "PBL_SAMPLES": os.environ.get("PBL_SAMPLES", "16")}
    for sh in shots():
        d = B / "shots" / sh["id"]
        if force and d.exists():
            shutil.rmtree(d)
        done = len(list(d.glob("f_*.png"))) if d.exists() else 0
        anc = d / "anchors.json"
        if done >= sh["n"] and anc.exists() and json.loads(anc.read_text())["n"] == sh["n"]:
            continue
        wait_free()
        print(f"render {sh['id']}: {done}/{sh['n']} frames there", flush=True)
        with open(B / f"render_{sh['id']}.log", "w") as log:
            subprocess.run([BLENDER, "-b", "-P", str(HERE / "scene3d.py"), "--", "--shot", sh["id"]], cwd=ROOT, env=env,
                           stdout=log, stderr=subprocess.STDOUT, check=True)


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
        d = B / "shots" / sh["id"]
        bad = broken(d) if d.exists() else []
        if bad:
            wait_free()
            print(f"repair {sh['id']}: frames {bad}", flush=True)
            subprocess.run([BLENDER, "-b", "-P", str(HERE / "scene3d.py"), "--", "--shot", sh["id"], "--frames",
                            ",".join(map(str, bad))], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, check=True)


def compose():
    subprocess.run([PY, str(HERE / "compose.py")], cwd=ROOT, check=True)


def mix():
    subprocess.run([PY, str(HERE / "mix.py")], cwd=ROOT, check=True)


def final():
    pic, aud = B / "picture.mp4", B / "audio.wav"
    out = B / "treasure_tr_final.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(pic), "-i", str(aud), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)]))
    # upload copy under 10 MB (HEVC like the other 3D Shorts): video bitrate from the size budget
    kbps = int((9.6 * 8 * 1024 / dur) - 130)
    up = B / "treasure_tr_upload.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-c:v", "libx265", "-preset", "slow", "-b:v", f"{kbps}k",
                    "-maxrate", f"{int(kbps * 1.6)}k", "-bufsize", f"{kbps * 2}k", "-tag:v", "hvc1", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(up)], check=True)
    print(f"final {out.name} {dur:.1f} s {out.stat().st_size / 1e6:.1f} MB; upload {up.stat().st_size / 1e6:.2f} MB")


STEPS = {"voice": voice, "render": render, "repair": repair, "compose": compose, "mix": mix, "final": final}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--renarrate" in sys.argv:
        voice()
        render(force=True)
        repair(); compose(); mix(); final()
    elif args:
        for a in args:
            STEPS[a]()
    else:
        if not (B / "schedule.json").exists():
            voice()
        render(); repair(); compose(); mix(); final()
