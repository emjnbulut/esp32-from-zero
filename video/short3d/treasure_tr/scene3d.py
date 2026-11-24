"""Blender shots of the Turkish treasure-detector Short (vertical 1080x1920), driven by story.py.

    blender -b -P video/short3d/treasure_tr/scene3d.py -- --shot hunt            # all frames of one shot (resumable)
    blender -b -P video/short3d/treasure_tr/scene3d.py -- --stills hook,hunt      # 3 stills per shot -> build/stills/
    blender -b -P video/short3d/treasure_tr/scene3d.py -- --at 3.5,12.0           # stills at global times

One Blender process per shot (make.py does that): a process that renders thousands of frames grows in memory.
Output: build/shots/<id>/f_0001.png ... + anchors.json (projected buzzer / LED / knob / OLED / button / tags per frame).
Circuit = the Ep10 circuit (pbl layout, front board F, back board B) + knob + RGB LED:
  Ep10: B4e->B r+ 4 (3V3), B5d->B r- 5 (GND), OLED B34f..37f, SCL B17e->B36h, SDA B14e->B37g, button B24/26 e-f,
        B13d->B24d (D19), B26j->r- 26, buzzer F30c(+)/F33c, F13i->F30a (D32), F5h->F l- 5, F33a->F l- 33
  new:  + line to the front board B r+ 57 -> F l+ 57; knob legs F40e/42e/44e: F40a->F l+ 40, F44a->F l- 44, F42c->F15h (D34)
        RGB LED legs F22b R / F23b - / F24b G / F25b B, 220 ohm F22e-f, F24e-f, F25e-f,
        F11h->F22h (D25), F10g->F24g (D26), F9i->F25i (D27), F23a->F l- 23
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


ST = S.Story()
FPS = S.FPS
OUT = os.path.join(HERE, "build")

# ======================================================================= scene
k = pbl.Kit(fps=FPS, res=(1080, 1920))
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D34", "D25", "D26", "D27"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=45, fstop=28.0)
oled = k.oled(B, (34, 35, 36, 37), "f")
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
pot = k.pot([F.hole(40, "e"), F.hole(42, "e"), F.hole(44, "e")], dy=6.0)
rgb = k.rgb_led([F.hole(22, "b"), F.hole(23, "b"), F.hole(24, "b"), F.hole(25, "b")])
RES = {"res_r": k.resistor(F.hole(22, "e"), F.hole(22, "f"), name="res_r"),
       "res_g": k.resistor(F.hole(24, "e"), F.hole(24, "f"), name="res_g"),
       "res_b": k.resistor(F.hole(25, "e"), F.hole(25, "f"), name="res_b")}
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
W["bridge"] = k.wire(B.rail(57, "r", "+"), F.rail(57, "l", "+"), "red", h=18, name="bridge")
W["pot_vcc"] = k.wire(F.hole(40, "a"), F.rail(40, "l", "+"), "red", name="pot_vcc")
W["pot_gnd"] = k.wire(F.hole(44, "a"), F.rail(44, "l", "-"), "black", name="pot_gnd")
W["pot_sig"] = k.wire(F.hole(42, "c"), F.hole(15, "h"), "purple", h=17, name="pot_sig", via=[(46, -31), (8, -27)])
W["rgb_r"] = k.wire(F.hole(11, "h"), F.hole(22, "h"), "red", h=6, name="rgb_r")
W["rgb_g"] = k.wire(F.hole(10, "g"), F.hole(24, "g"), "green", h=8, name="rgb_g")
W["rgb_b"] = k.wire(F.hole(9, "i"), F.hole(25, "i"), "blue", h=10, name="rgb_b")
W["rgb_k"] = k.wire(F.hole(23, "a"), F.rail(23, "l", "-"), "black", name="rgb_k")
k.lights(center=(0.035, 0.0, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene

TAGAT = {"oled": oled["center"] + Vector((0, 4, 0)), "buzzer": bz["top"], "button": btn["top"], "pot": pot["top"],
         "rgb": rgb["top"], "dig": btn["top"]}
TAGCOL = {"oled": "#2dd4bf", "buzzer": "#ff8a2a", "button": "#f2c037", "pot": "#b78cff", "rgb": "#ff6b8b", "dig": "#f2c037"}
PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"], "pot": pot["group"], "rgb": rgb["group"]}
for n, r in RES.items():
    PARTS[n] = r["group"]
BASE_Z = {n: g.location.z for n, g in PARTS.items()}
PRESS_Z = btn["press"].location.z


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


def apply(st, T):
    parts = set(st["parts"])
    if "rgb" in parts:
        parts |= set(RES)
    drop = dict(st["drop"])
    for r in RES:
        if "rgb" in drop:
            drop[r] = drop["rgb"] + 0.12 * (1 + list(RES).index(r))
    for n, g in PARTS.items():
        on = n in parts
        g.location.z = BASE_Z[n]
        if n in drop:
            on = on and T >= drop[n] - 0.3
            if on:  # falls in from above with a little overshoot
                u = min(1.0, (T - (drop[n] - 0.3)) / 0.45)
                back = 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2
                g.location.z = BASE_Z[n] + 60 * (1 - back)
        vis(g, on)
    if pot["mark"] is not None and "pot" not in parts:
        pot["mark"].hide_render = True
    for n, w in W.items():
        w["draw"](1.0 if st["wires"] is None else st["wires"].get(n, 0.0))
    pot["set"](st["knob"])
    if "pot" in parts:
        pot["set_mark"](st["mark"])
    rgb["set"](st["led"], st["led_level"])
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
    d = {"buzzer": proj(bz["top"]), "led": proj(rgb["top"]), "knob": proj(pot["top"]), "oled": proj(oled["center"]),
         "button": proj(btn["top"]), "usb": proj(Vector(S.USBP))}
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
    apply(st, T)
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
