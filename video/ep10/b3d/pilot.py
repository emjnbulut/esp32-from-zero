"""Ep10 Blender pilot: Reflex Game 2.0 (button + OLED + passive buzzer), record survives unplugging.

    blender -b -P video/ep10/b3d/pilot.py -- <out dir> [frames e.g. 1,60,75] [--cycles]

Needs video/b3d/build/breadboard.png (video/b3d/tex.py) and build/oled frames (oled_frames.py).
Wiring (front board F, back board B; pbl.py layout):
  B 4e  -> B rail(r,+) 4     3V3 to the back + rail          B 5d  -> B rail(r,-) 5    GND to the back - rail
  B 17e -> B 36h  SCL (D22)  B 14e -> B 37g  SDA (D21)       OLED header B 34f..37f = GND VCC SCL SDA
  B 34j -> rail(r,-) 34      B 35j -> rail(r,+) 35
  button B 24e/26e/24f/26f   B 13d -> B 24d  (D19)            B 26j -> rail(r,-) 26
  buzzer F 30c (+) / F 33c   F 13i -> F 30a  (D32)   F 5h -> F rail(l,-) 5   F 33a -> F rail(l,-) 33
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import pbl  # noqa: E402
from pbl import MM, key, smooth  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = os.path.abspath(argv[0])
ONLY = [int(x) for x in argv[1].split(",")] if len(argv) > 1 and argv[1][0].isdigit() else None
CYCLES = "--cycles" in argv
FPS, DUR = 30, 9.0
N = int(FPS * DUR)
T = json.load(open(os.path.join(HERE, "times.json")))

k = pbl.Kit(fps=FPS, engine="CYCLES" if CYCLES else "EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32"})
usb = k.usb_cable()
oled = k.oled(B, (34, 35, 36, 37), "f", frames_dir=os.path.join(HERE, "build", "oled"), nframes=N)
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
W = k.wire
W(B.hole(4, "e"), B.rail(4, "r", "+"), "red")
W(B.hole(5, "d"), B.rail(5, "r", "-"), "black")
W(B.hole(17, "e"), B.hole(36, "h"), "green", h=9)
W(B.hole(14, "e"), B.hole(37, "g"), "blue", h=11)
W(B.hole(34, "j"), B.rail(34, "r", "-"), "black")
W(B.hole(35, "j"), B.rail(35, "r", "+"), "red")
W(B.hole(13, "d"), B.hole(24, "d"), "yellow", h=5)
W(B.hole(26, "j"), B.rail(26, "r", "-"), "black")
W(F.hole(13, "i"), F.hole(30, "a"), "orange", h=7)
W(F.hole(5, "h"), F.rail(5, "l", "-"), "black")
W(F.hole(33, "a"), F.rail(33, "l", "-"), "black")
rings = k.sound_rings(bz["top"], 3)
k.lights(center=(0.035, 0.0, 0.0), key=2.2)
cam, tgt = k.camera(lens=50, fstop=10.0)
k.glare(threshold=2.5)

# ---------------------------------------------------------------- animation
sc = k.scene
sc.frame_start, sc.frame_end = 1, N


def fr(t):
    return 1 + round(t * FPS)


press = btn["press"]
base_z = press.location.z
for i in range(N):
    t = i / FPS
    f = i + 1
    # button: down 0.9 mm while pressed
    dz = 0.0
    if T["react"] - 0.05 <= t <= T["react"] + 0.16:
        dz = -0.9 * math.sin(math.pi * (t - (T["react"] - 0.05)) / 0.21)
    key(press, "location", f, base_z + dz, index=2)
    # usb cable: pull out 16 mm, push back
    pull = smooth((t - T["unplug"]) / 0.35) - smooth((t - T["plug"]) / 0.3)
    key(usb, "location", f, -16.0 * pull, index=0)
    # power LED
    on = not (T["unplug"] + 0.12 <= t < T["plug"] + 0.2)
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if on else 0.0
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].keyframe_insert("default_value", frame=f)

# buzzer rings: one beep at GO, a three-note melody for the record
beeps = [T["go"], T["record"], T["record"] + 0.22, T["record"] + 0.44]
for idx, (ob, val) in enumerate(rings):
    for i in range(N):
        t = i / FPS
        a, s = 0.0, 1.0
        for j, tb in enumerate(beeps):
            if j % len(rings) != idx and len(beeps) > len(rings) and j != idx:
                pass
            u = (t - tb - idx * 0.07) / 0.45
            if 0 <= u <= 1:
                a = max(a, (1 - u) ** 1.5)
                s = 6.5 + 14 * u
        key(ob, "scale", i + 1, s, index=0)
        key(ob, "scale", i + 1, s, index=1)
        val.outputs[0].default_value = a
        val.outputs[0].keyframe_insert("default_value", frame=i + 1)

# camera: wide establishing -> button + screen -> USB unplug -> push into the screen
oc = oled["center"]
bt = btn["top"]
usbp = Vector((esp["xU"] - 8, 0, 14))
mid = (oc + bt) / 2
shots = [  # (time, camera position mm, target mm)
    (0.0, Vector((20, -235, 230)), Vector((30, 5, 0))),
    (1.8, Vector((44, -150, 140)), mid + Vector((-4, -6, 0))),
    (3.6, Vector((50, -118, 105)), mid + Vector((0, -2, 2))),
    (4.6, Vector((5, -150, 120)), (mid + usbp) / 2),
    (5.4, Vector((-55, -120, 95)), usbp + Vector((4, 0, 0))),
    (6.3, Vector((-35, -135, 110)), usbp + Vector((20, 0, 0))),
    (7.4, Vector((44, -92, 82)), oc + Vector((0, -2, 0))),
    (9.0, Vector((44, -78, 70)), oc + Vector((0, -1, 0))),
]
for t, cpos, tpos in shots:
    cam.location = cpos * MM
    cam.keyframe_insert("location", frame=fr(t))
    tgt.location = tpos * MM
    tgt.keyframe_insert("location", frame=fr(t))
for ob in (cam, tgt):
    ad = ob.animation_data
    if ad and ad.action:
        try:
            curves = ad.action.fcurves
        except AttributeError:
            curves = [c for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for c in bag.fcurves]
        for c in curves:
            for kp in c.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"

# ---------------------------------------------------------------- render
os.makedirs(OUT, exist_ok=True)
sc.render.image_settings.file_format = "PNG"
if CYCLES:
    pbl_dev = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            pbl_dev.compute_device_type = kind
            pbl_dev.get_devices()
            break
        except TypeError:
            continue
    for d in pbl_dev.devices:
        d.use = d.type != "CPU"
    sc.cycles.device = "GPU"
    sc.cycles.samples = 96
    sc.cycles.use_denoising = True
frames = ONLY or list(range(1, N + 1))
for f in frames:
    path = os.path.join(OUT, f"f_{f:04d}.png")
    if os.path.exists(path) and not ONLY:
        continue
    sc.frame_set(f)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("frame", f, flush=True)
