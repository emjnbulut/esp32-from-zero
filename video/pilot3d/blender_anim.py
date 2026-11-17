"""20 s cinematic version (B) of the 3D pilot, rendered in Blender.

Same story and timing as the three.js version (scene3d.js): assembly, LED breathing with analogWrite(),
1000x slow motion, back to real speed, hero shot. Every animated value is keyed on every frame from the same
time functions, so it stays frame-exact with the 2D overlay (rendered separately with --alpha and composited).

  blender -b -P pilot3d/blender_anim.py -- <scene.glb> <scene.json> <abs out dir> <engine eevee|cycles> <samples> [frames e.g. 30,200]

Without a frame list it renders all 600 frames into <out dir>/f_0000.png ... (skips frames that already exist,
so an interrupted render can simply be restarted). Also writes <out dir>/../overlay_data.json for render.mjs.
"""
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1])))
from b3d_scene import MM, build, color_management, gl, use_gpu_cycles  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
GLB, INFO, OUT, ENGINE, SAMPLES = argv[0], argv[1], argv[2], argv[3], int(argv[4])
ONLY = [int(x) for x in argv[5].split(",")] if len(argv) > 5 else None
FPS, DUR = 30, 20.0
N = int(FPS * DUR)

info = json.load(open(INFO))
scene, root, lib, ledlight = build(GLB)
bpy.context.view_layer.update()


def bl_mm(p):
    """three.js mm (y-up) -> Blender axes, still in mm (children of the scaled root)."""
    return Vector((p[0], -p[2], p[1]))


# ---------- animated groups: re-parent parts to an empty at the group's pivot ----------
groups = {}
for g, origin in info["groups"].items():
    e = bpy.data.objects.new("grp_" + g, None)
    scene.collection.objects.link(e)
    e.parent = root
    e.location = bl_mm(origin)
    groups[g] = e
bpy.context.view_layer.update()
for o in list(scene.objects):
    if o.type == "MESH" and "|" in o.name:
        g = o.name.split("|")[0]
        if g in groups:
            mw = o.matrix_world.copy()
            o.parent = groups[g]
            o.matrix_world = mw

# ---------- wires as curves so they can "draw" themselves ----------
for o in list(scene.objects):
    if o.name.split(".")[0] in ("wire_gpio23", "wire_gnd"):
        bpy.data.objects.remove(o, do_unlink=True)
wires = {}
for name, pts in info["wires"].items():
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.6
    cu.bevel_resolution = 4
    cu.use_fill_caps = True
    cu.bevel_factor_mapping_end = "SPLINE"
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        v = bl_mm(p)
        sp.points[i].co = (v.x, v.y, v.z, 1.0)
    sp.use_smooth = True
    ob = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(ob)
    ob.parent = root
    cu.materials.append(lib[name])
    wires[name] = cu

# ---------- the same time functions as scene3d.js ----------
def clamp01(x):
    return min(1.0, max(0.0, x))


def smooth(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def back_out(x):
    x = clamp01(x)
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


def lerp(a, b, k):
    return a + (b - a) * k


T_BREATH, T_SLOW0, T_SLOW, T_FAST, T_AVG, T_FULL = 3.6, 9.0, 9.6, 13.6, 14.8, 15.2
BREATH_PERIOD, SLOW_PERIOD, DUTY = 2.7, 1.0, 64 / 255


def slow_phase(tau):
    if tau < T_FAST:
        return (tau - T_SLOW) / SLOW_PERIOD
    ph = (T_FAST - T_SLOW) / SLOW_PERIOD
    dt, s = 1 / 240, T_FAST
    while s < tau:
        ph += (1 + 23 * smooth((s - T_FAST) / (T_AVG - T_FAST))) * dt
        s += dt
    return ph


def pin_high(tau):
    return tau >= T_SLOW and (slow_phase(tau) % 1.0) < DUTY


def value_at(t):
    if t < T_BREATH:
        return 0.0
    if t < T_SLOW0:
        return 255 * (0.5 - 0.5 * math.cos(2 * math.pi * (t - T_BREATH) / BREATH_PERIOD))
    if t < T_FULL:
        return lerp(0, 64, smooth((t - T_SLOW0) / 0.6))
    return lerp(64, 255, smooth((t - T_FULL) / 0.9))


def led_at(t):
    v = value_at(t) / 255
    if t < T_SLOW:
        return v if t < T_SLOW0 else v * (1 - smooth((t - T_SLOW0) / 0.6))
    if t < T_AVG:
        b = 1.0 if pin_high(t) else 0.0
        return lerp(b, DUTY, 0.0 if t < T_FAST else smooth((t - T_FAST) / (T_AVG - T_FAST)))
    return v


# camera keys: (time, yaw deg, elevation deg, half-height mm, target mm in three.js axes)
KEYS = [
    (0.0, -40, 36, 40, (6, 8, 3)),
    (3.4, -28, 30, 44, (2, 8, 3)),
    (4.4, -24, 28, 46, (-27, 8, 3)),
    (9.0, -14, 26, 46, (-27, 8, 3)),
    (10.0, 4, 22, 18, (30, 13, 10)),
    (14.6, 10, 22, 19, (30.5, 13, 10)),
    (15.8, -32, 28, 50, (-4, 14, -8)),
    (20.0, -24, 26, 47, (-4, 14, -8)),
]


def cam_at(t):
    i = 0
    while i < len(KEYS) - 2 and t >= KEYS[i + 1][0]:
        i += 1
    a, b = KEYS[i], KEYS[i + 1]
    k = smooth((t - a[0]) / (b[0] - a[0]))
    tgt = [lerp(a[4][j], b[4][j], k) for j in range(3)]
    return lerp(a[1], b[1], k), lerp(a[2], b[2], k), lerp(a[3], b[3], k), tgt


# ---------- camera ----------
cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 50
cam_d.clip_start = 0.001
cam_d.dof.use_dof = True
cam = bpy.data.objects.new("cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam
HALF_V = math.atan(18 / 50 * 9 / 16)  # half vertical field of view (36 mm sensor, 16:9)
LEDP = gl(*info["led"])

# ---------- key every frame ----------
led_bsdf = lib["led"].node_tree.nodes["Principled BSDF"]
wire_bsdf = lib["wire_gpio23"].node_tree.nodes["Principled BSDF"]
pwr_bsdf = lib["pwrled"].node_tree.nodes["Principled BSDF"]
anchors = {"gpio23": [], "ledTop": []}
prev_rot = None
drop = []
for f in range(N):
    t = f / FPS
    # assembly
    bd = back_out((t - 0.25) / 1.15)
    groups["esp32"].location.z = bl_mm(info["groups"]["esp32"]).z + (1 - bd) * 70
    groups["esp32"].keyframe_insert("location", index=2, frame=f)
    drop.append((1 - bd) * 70)
    for g, t0 in (("led", 1.35), ("resistor", 1.6)):
        s = max(0.001, back_out((t - t0) / 0.5))
        groups[g].scale = (s, s, s)
        groups[g].keyframe_insert("scale", frame=f)
    for name, t0, d in (("wire_gpio23", 2.0, 1.1), ("wire_gnd", 2.4, 0.9)):
        p = smooth((t - t0) / d)
        wires[name].bevel_factor_end = max(0.0005, p)
        wires[name].keyframe_insert("bevel_factor_end", frame=f)
    pwr_bsdf.inputs["Emission Strength"].default_value = 6.0 if t > 3.1 else 0.0
    pwr_bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=f)

    # light
    L = led_at(t)
    vis = L ** 0.6
    led_bsdf.inputs["Emission Strength"].default_value = 5.0 * vis
    led_bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=f)
    ledlight.data.energy = 0.16 * vis
    ledlight.data.keyframe_insert("energy", frame=f)
    pin_on = (1.0 if pin_high(t) else 0.0) if T_SLOW <= t < T_AVG else L
    wire_bsdf.inputs["Emission Strength"].default_value = (1.6 if T_SLOW <= t < T_FAST else 1.0) * pin_on
    wire_bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=f)

    # camera
    th, el, hh, tgt = cam_at(t)
    th, el = math.radians(th), math.radians(el)
    target = gl(*tgt)
    dist = hh * MM / math.tan(HALF_V)
    cam.location = target + Vector((dist * math.cos(el) * math.sin(th), -dist * math.cos(el) * math.cos(th), dist * math.sin(el)))
    rot = (target - cam.location).to_track_quat("-Z", "Y").to_euler("XYZ", prev_rot) if prev_rot else (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    prev_rot = rot
    cam.rotation_euler = rot
    cam.keyframe_insert("location", frame=f)
    cam.keyframe_insert("rotation_euler", frame=f)
    close = clamp01((46 - hh) / (46 - 18))
    cam_d.dof.focus_distance = ((target.lerp(LEDP, close)) - cam.location).length
    cam_d.dof.aperture_fstop = lerp(8.0, 4.5, close)
    cam_d.dof.keyframe_insert("focus_distance", frame=f)
    cam_d.dof.keyframe_insert("aperture_fstop", frame=f)

for o in [cam, cam_d, groups["esp32"], groups["led"], groups["resistor"], ledlight.data] + [lib[k] for k in ("led", "wire_gpio23", "pwrled")] + list(wires.values()):
    ad = getattr(o, "animation_data", None) or (o.node_tree.animation_data if hasattr(o, "node_tree") else None)
    if ad and ad.action:
        try:
            curves = ad.action.fcurves
        except AttributeError:  # Blender 5 layered actions
            curves = [fc for layer in ad.action.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]
        for fc in curves:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"

# ---------- 2D anchors for the overlay (GPIO 23 tag, LED tag), projected by this camera ----------
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.resolution_percentage = 100
for f in range(N):
    scene.frame_set(f)
    for key, base in (("gpio23", info["anchors"]["gpio23"]), ("ledTop", info["anchors"]["ledTop"])):
        p = gl(*base)
        if key == "gpio23":
            p = p + Vector((0, 0, drop[f] * MM))
        c = world_to_camera_view(scene, cam, p)
        anchors[key].append([round(c.x * 1920, 1), round((1 - c.y) * 1080, 1)])
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(os.path.dirname(OUT.rstrip("/\\")), "overlay_data.json"), "w") as fh:
    json.dump({"schedule": {"duration": DUR, "segments": {}}, "overlay": dict(fps=FPS, **anchors)}, fh)

# ---------- render ----------
if ENGINE == "cycles":
    print("devices:", use_gpu_cycles(scene, SAMPLES))
else:
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            scene.render.engine = eng
            break
        except TypeError:
            continue
    scene.eevee.taa_render_samples = SAMPLES
    for attr in ("use_raytracing", "use_shadows"):
        if hasattr(scene.eevee, attr):
            setattr(scene.eevee, attr, True)
color_management(scene)
scene.render.image_settings.file_format = "PNG"
scene.render.fps = FPS
if ONLY:
    for f in ONLY:
        scene.frame_set(f)
        scene.render.filepath = os.path.join(OUT, "f_%04d.png" % f)
        bpy.ops.render.render(write_still=True)
        print("frame", f)
else:
    scene.frame_start, scene.frame_end = 0, N - 1
    scene.render.filepath = os.path.join(OUT, "f_")
    scene.render.use_overwrite = False
    scene.render.use_placeholder = True
    bpy.ops.render.render(animation=True)
print("done", ENGINE)
