"""Blender shots of the reflex-game Short (vertical 1080x1920), driven by story.py. Language: env REFLEX_LANG.

    blender -b -P video/short3d/reflex/scene3d.py -- --shot play               # all frames of one shot (resumable)
    blender -b -P video/short3d/reflex/scene3d.py -- --stills hook,play         # 3 stills per shot -> build/<lang>/stills/
    blender -b -P video/short3d/reflex/scene3d.py -- --at 1.0,12.0              # stills at global times

One Blender process per shot (make.py does that): a process that renders thousands of frames grows in memory.
Output: build/<lang>/shots/<id>/f_0001.png ... + anchors.json (projected buzzer / OLED / button / USB / tags per frame).
Circuit = the Ep10 circuit exactly (video/ep10/b3d/ep10_3d.py, pbl layout, front board F, back board B):
  B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f GND VCC SCL SDA, B34j->r- 34, B35j->r+ 35
  B17e->B36h green SCL (D22)  B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
  buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
"""
import json
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import pbl  # noqa: E402
from pbl import MM  # noqa: E402
import story as S  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


ST = S.Story(opt("--lang"))
FPS = S.FPS
OUT = ST.B

# ======================================================================= scene
k = pbl.Kit(fps=FPS, res=(1080, 1920))
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=45, fstop=28.0)
oled = k.oled(B, (34, 35, 36, 37), "f")
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
W = {}
W["pwr_red"] = k.wire(B.hole(4, "e"), B.rail(4, "r", "+"), "red", name="pwr_red")
W["pwr_blk"] = k.wire(B.hole(5, "d"), B.rail(5, "r", "-"), "black", name="pwr_blk")
W["oled_gnd"] = k.wire(B.hole(34, "j"), B.rail(34, "r", "-"), "black", name="oled_gnd")
W["oled_vcc"] = k.wire(B.hole(35, "j"), B.rail(35, "r", "+"), "red", name="oled_vcc")
W["scl"] = k.wire(B.hole(17, "e"), B.hole(36, "h"), "green", h=9, name="scl")
W["sda"] = k.wire(B.hole(14, "e"), B.hole(37, "g"), "blue", h=11, name="sda")
W["btn"] = k.wire(B.hole(13, "d"), B.hole(24, "d"), "yellow", h=5, name="btn")
W["btn_gnd"] = k.wire(B.hole(26, "j"), B.rail(26, "r", "-"), "black", name="btn_gnd")
W["bz"] = k.wire(F.hole(13, "i"), F.hole(30, "a"), "orange", h=7, name="bz")
W["bz_gnd1"] = k.wire(F.hole(5, "h"), F.rail(5, "l", "-"), "black", name="bz_gnd1")
W["bz_gnd2"] = k.wire(F.hole(33, "a"), F.rail(33, "l", "-"), "black", name="bz_gnd2")
for w in W.values():
    w["draw"](1.0)
k.lights(center=(0.035, 0.0, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene

TAGAT = {"oled": oled["center"] + Vector((0, 4, 0)), "buzzer": bz["top"], "button": btn["top"]}
TAGCOL = {"oled": "#2dd4bf", "buzzer": "#ff8a2a", "button": "#f2c037"}
PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"]}
BASE_Z = {n: g.location.z for n, g in PARTS.items()}
PRESS_Z = btn["press"].location.z


def apply(st):
    for n, g in PARTS.items():
        g.location.z = BASE_Z[n] + st["hop"].get(n, 0.0)
    btn["press"].location.z = PRESS_Z + st["press"]
    usb.location.x = -16.0 * st["pull"]
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if st["pwr"] else 0.0
    k.set_screen(st["screen"])
    p, q, lens = st["cam"]
    cam.location = Vector(p) * MM
    tgt.location = Vector(q) * MM
    cam.data.lens = lens


def proj(v):
    a = world_to_camera_view(sc, cam, Vector(v) * MM)
    return [round(a.x, 4), round(1 - a.y, 4)] if a.z > 0 else None


def anchors(st):
    d = {"buzzer": proj(bz["top"]), "oled": proj(oled["center"]), "button": proj(btn["top"]), "usb": proj(Vector(S.USBP)),
         "chip": proj(Vector(S.CHIP))}
    tags = []
    for name, (on, text) in st["tags"].items():
        if on > 0.02:
            a, b = proj(TAGAT[name]), proj(TAGAT[name] + Vector((0, 0, 10)))
            if a and b:
                tags.append({"text": text, "color": TAGCOL[name], "on": round(on, 3), "scale": 1.0, "a": a, "b": b})
    d["tags"] = tags
    return d


sc.render.image_settings.file_format = "PNG"
REDO = "--redo" in argv  # re-render frames that already exist (overwrite in place)


def render_frame(T, path):
    st = ST.state(T)
    apply(st)
    bpy.context.view_layer.update()
    a = anchors(st)
    if path and (REDO or not os.path.exists(path)):
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
    return a


if opt("--at"):
    os.makedirs(os.path.join(OUT, "stills"), exist_ok=True)
    for x in opt("--at").split(","):
        T = float(x)
        p = os.path.join(OUT, "stills", f"at_{T:06.2f}.png")
        if os.path.exists(p):
            os.remove(p)
        render_frame(T, p)
elif opt("--stills"):
    os.makedirs(os.path.join(OUT, "stills"), exist_ok=True)
    for sid in opt("--stills").split(","):
        sh = ST.S[sid]
        for f in sorted({1, sh["n"] // 2 + 1, sh["n"]}):
            T = (sh["F0"] + f - 1) / FPS
            p = os.path.join(OUT, "stills", f"{sid}_f_{f:04d}.png")
            if os.path.exists(p):
                os.remove(p)
            render_frame(T, p)
else:
    sid = opt("--shot")
    sh = ST.S[sid]
    d = os.path.join(OUT, "shots", sid)
    os.makedirs(d, exist_ok=True)
    anc = {}
    ONLYF = {int(x) for x in opt("--frames").split(",")} if opt("--frames") else None  # re-render just these (broken files)
    for f in range(1, sh["n"] + 1):
        T = (sh["F0"] + f - 1) / FPS
        p = os.path.join(d, f"f_{f:04d}.png")
        if ONLYF and f not in ONLYF:
            continue
        if ONLYF:
            REDO = True
        anc[str(f)] = render_frame(T, p)
        print("frame", sid, f, "/", sh["n"], flush=True)
    if not ONLYF:
        json.dump({"F0": sh["F0"], "n": sh["n"], "frames": anc}, open(os.path.join(d, "anchors.json"), "w"))
    print("done", sid)
