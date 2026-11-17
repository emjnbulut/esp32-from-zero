"""Treasure-detector Short in Blender (vertical 1080x1920, EEVEE): reads build/scene.glb + build/track.json.

  blender -b -P video/short3d/treasure/blender_short.py -- <abs build dir> <samples> [frames e.g. 0,300,700]

Without a frame list: every frame into <build>/frames/f_0000.png (existing frames are skipped, so a stopped render
just continues). Always writes <build>/anchors.json (2D positions of the knob, LEDs and button for the overlay).
"""
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pilot3d"))
from b3d_scene import MM, build, color_management, gl, hexrgb, pbr  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
B, SAMPLES = argv[0], int(argv[1])
ONLY = [int(x) for x in argv[2].split(",")] if len(argv) > 2 else None
T = json.load(open(os.path.join(B, os.environ.get("TRACK", "track.json"))))
info, track, FPS, N = T["info"], T["track"], T["fps"], T["frames"]

scene, root, lib, ledlight = build(os.path.join(B, "scene.glb"))
bpy.context.view_layer.update()


def bl_mm(p):
    return Vector((p[0], -p[2], p[1]))


def lin(c255):
    return hexrgb("#%02x%02x%02x" % tuple(int(max(0, min(255, v))) for v in c255))


# ---------- extra materials for the Short's parts ----------
EXTRA = {
    "rgbled": pbr("rgbled", "#f2efe8", 0.32, trans=0.25, emit="#000000", strength=0.0),
    "btnbody": pbr("btnbody", "#16181d", 0.5),
    "btncap": pbr("btncap", "#ffb547", 0.35, coat=0.5),
    "potbase": pbr("potbase", "#1b2433", 0.5),
    "potcan": pbr("potcan", "#c8ced6", 0.25, metal=1.0),
    "knob": pbr("knob", "#18191d", 0.42),
    "knobtop": pbr("knobtop", "#22252b", 0.35, coat=0.4),
    "knobmark": pbr("knobmark", "#ffffff", 0.4, emit="#ffffff", strength=0.4),
}
for o in scene.objects:
    if o.type != "MESH":
        continue
    for slot in o.material_slots:
        n = slot.material.name.split(".")[0] if slot.material else ""
        if n in EXTRA:
            slot.material = EXTRA[n]
        elif n.startswith("wire#"):
            m = pbr("w_" + n[5:], n[4:], 0.35, coat=0.35)
            slot.material = m

# ---------- smooth round parts, keep box edges crisp (auto smooth by angle) ----------
meshes = [o for o in scene.objects if o.type == "MESH"]
for o in meshes:
    o.data.polygons.foreach_set("use_smooth", [True] * len(o.data.polygons))
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
try:
    bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
except Exception as e:  # older API
    print("auto smooth fallback:", e)
    for o in meshes:
        if hasattr(o.data, "use_auto_smooth"):
            o.data.use_auto_smooth, o.data.auto_smooth_angle = True, math.radians(35)
for o in meshes:
    o.select_set(False)

# ---------- animated groups ----------
groups = {}
prefixes = sorted({o.name.split("|")[0] for o in scene.objects if o.type == "MESH" and "|" in o.name} - {"wire"})
for g in prefixes:
    piv = info["pivots"].get(g, [0, 0, 0])
    e = bpy.data.objects.new("grp_" + g, None)
    scene.collection.objects.link(e)
    e.parent = root
    e.location = bl_mm(piv)
    groups[g] = e
bpy.context.view_layer.update()
for o in list(scene.objects):
    if o.type == "MESH" and "|" in o.name:
        g = o.name.split("|")[0]
        if g in groups:
            mw = o.matrix_world.copy()
            o.parent = groups[g]
            o.matrix_world = mw

# wires as curves, so the build part can draw them hole to hole
WIREMAT = {}
for o in list(scene.objects):
    if o.type == "MESH" and o.name.startswith("wire|"):
        WIREMAT[o.name.split("|")[1].split(".")[0]] = o.material_slots[0].material
        bpy.data.objects.remove(o, do_unlink=True)
wires = {}
for name, pts in info["wires"].items():
    cu = bpy.data.curves.new("wire_" + name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = 0.6, 4, True
    cu.bevel_factor_mapping_end = "SPLINE"
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        v = bl_mm(p)
        sp.points[i].co = (v.x, v.y, v.z, 1.0)
    sp.use_smooth = True
    ob = bpy.data.objects.new("wire_" + name, cu)
    scene.collection.objects.link(ob)
    ob.parent = root
    cu.materials.append(WIREMAT[name])
    wires[name] = cu
REST = {g: e.location.copy() for g, e in groups.items()}

A = dict(info["anchors"], **T.get("anchors3d", {}))
ledlight.location = gl(A["rledTop"][0], A["rledTop"][1] + 1.5, A["rledTop"][2])
rgb_light_d = bpy.data.lights.new("rgblight", "POINT")
rgb_light_d.shadow_soft_size = 0.003
rgb_light = bpy.data.objects.new("rgblight", rgb_light_d)
scene.collection.objects.link(rgb_light)
rgb_light.location = gl(A["rgbTop"][0], A["rgbTop"][1] - 2, A["rgbTop"][2])
keylights = [scene.objects[n] for n in ("key", "rim", "fill")]
base_energy = {o.name: o.data.energy for o in keylights}
world_bg = scene.world.node_tree.nodes["Background"].inputs["Strength"]
WORLD0 = world_bg.default_value


# ---------- heat rings around the knob ----------
def ring_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)
    bsdf.inputs["Emission Strength"].default_value = 6.0
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    return m, bsdf


rings = []
kc = A["knobCenter"]
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(major_radius=9.5 * MM, minor_radius=0.32 * MM, major_segments=96, minor_segments=8,
                                     location=gl(kc[0], 9.4, kc[2]))
    r = bpy.context.active_object
    r.name = f"ring{i}"
    m, bsdf = ring_mat(f"ringmat{i}")
    r.data.materials.append(m)
    rings.append((r, bsdf))

# ---------- the treasure: a gold coin ----------
bpy.ops.mesh.primitive_cylinder_add(radius=9 * MM, depth=1.8 * MM, vertices=64, location=(0, 0, 0))
coin = bpy.context.active_object
coin.name = "coin"
bev = coin.modifiers.new("bev", "BEVEL")
bev.width, bev.segments = 0.35 * MM, 3
gold = pbr("coin_gold", "#ffcf4a", 0.18, metal=1.0, emit="#ffb300", strength=0.4)
coin.data.materials.append(gold)
bpy.ops.mesh.primitive_cylinder_add(radius=6 * MM, depth=2.4 * MM, vertices=5, location=(0, 0, 0))  # a star-ish boss
boss = bpy.context.active_object
boss.data.materials.append(gold)
boss.parent = coin
coin.rotation_mode = "XYZ"
COIN_AT = gl(46, 14, -12)

# ---------- camera ----------
cam_d = bpy.data.cameras.new("cam")
cam_d.sensor_fit = "VERTICAL"
cam_d.sensor_height = 24
cam_d.clip_start = 0.001
cam_d.dof.use_dof = True
cam = bpy.data.objects.new("cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam

rgb_bsdf = EXTRA["rgbled"].node_tree.nodes["Principled BSDF"]
led_bsdf = lib["led"].node_tree.nodes["Principled BSDF"]
led_bsdf.inputs["Emission Strength"].default_value = 0
pwr_bsdf = lib["pwrled"].node_tree.nodes["Principled BSDF"]
pwr_bsdf.inputs["Emission Strength"].default_value = 6


def K(obj, path, f, index=-1):
    obj.keyframe_insert(path, frame=f, index=index)


prev = None
for f, s in enumerate(track):
    t = f / FPS
    parts = s.get("parts")
    if parts is not None:  # build: parts drop in from above (mm), 9999 = not there yet
        for g, e in groups.items():
            dz = parts.get(g, 0)
            e.location = REST[g] + Vector((0, 0, dz))
            K(e, "location", f)
    wp = s.get("wires")
    for name, cu in wires.items():
        cu.bevel_factor_end = max(0.0005, wp.get(name, 1.0) if wp is not None else 1.0)
        K(cu, "bevel_factor_end", f)
    groups["knob"].rotation_euler = (0, 0, math.radians(-s["knobDeg"]))  # three.js +y rotation -> Blender -z
    K(groups["knob"], "rotation_euler", f, 2)
    groups["btncap"].location.z = REST["btncap"].z + (parts.get("btncap", 0) if parts is not None else 0) - 1.3 * s["cap"]
    K(groups["btncap"], "location", f, 2)

    col = s["rgb"]
    bright = max(col) / 255
    rgb_bsdf.inputs["Emission Color"].default_value = lin([v if bright == 0 else v / bright for v in col])
    rgb_bsdf.inputs["Emission Strength"].default_value = 2.6 * bright
    K(rgb_bsdf.inputs["Emission Color"], "default_value", f)
    K(rgb_bsdf.inputs["Emission Strength"], "default_value", f)
    pure = lin([v if bright == 0 else v / bright for v in col])
    frost = hexrgb("#f2efe8")
    rgb_bsdf.inputs["Base Color"].default_value = tuple(frost[i] + (pure[i] * 0.85 - frost[i]) * min(1.0, bright * 1.3) for i in range(3)) + (1,)
    K(rgb_bsdf.inputs["Base Color"], "default_value", f)
    rgb_light_d.color = lin([v if bright == 0 else v / bright for v in col])[:3]
    rgb_light_d.energy = (0.5 if s["party"] else 0.22) * bright
    K(rgb_light_d, "color", f)
    K(rgb_light_d, "energy", f)
    led_bsdf.inputs["Emission Strength"].default_value = 5.5 * s["rled"]
    K(led_bsdf.inputs["Emission Strength"], "default_value", f)
    ledlight.data.energy = 0.12 * s["rled"]
    K(ledlight.data, "energy", f)

    # rings: 3 waves travelling outwards, colour = the LED's heat colour
    hc = lin([s["rgb"][0], 30, s["rgb"][2]])
    for i, (r, bsdf) in enumerate(rings):
        ph = (t * 0.85 + i / 3) % 1.0
        sc = 1 + 2.3 * ph
        r.scale = (sc, sc, sc)
        K(r, "scale", f)
        bsdf.inputs["Emission Color"].default_value = hc
        bsdf.inputs["Alpha"].default_value = s["rings"] * (1 - ph) ** 1.5
        K(bsdf.inputs["Emission Color"], "default_value", f)
        K(bsdf.inputs["Alpha"], "default_value", f)

    c = s["coin"]
    if c and c["scale"] > 0.001:
        coin.location = COIN_AT + Vector((0, 0, c["y"] * MM))
        coin.rotation_euler = (math.radians(90), 0, math.radians(c["spin"]))
        coin.scale = (c["scale"],) * 3
    else:
        coin.location = COIN_AT + Vector((0, 0, -0.05))
        coin.scale = (0.001,) * 3
    K(coin, "location", f)
    K(coin, "rotation_euler", f)
    K(coin, "scale", f)

    dimk = 1 - 0.7 * s["dim"]
    for o in keylights:
        o.data.energy = base_energy[o.name] * dimk
        K(o.data, "energy", f)
    world_bg.default_value = WORLD0 * dimk
    K(world_bg, "default_value", f)

    cm = s["cam"]
    pos, tgt = gl(*cm["pos"]), gl(*cm["tgt"])
    cam.location = pos
    q = (tgt - pos).to_track_quat("-Z", "Y")
    rot = q.to_euler("XYZ", prev) if prev else q.to_euler()
    prev = rot
    cam.rotation_euler = rot
    K(cam, "location", f)
    K(cam, "rotation_euler", f)
    cam_d.lens = 12 / math.tan(math.radians(cm["fov"]) / 2)
    dist = (tgt - pos).length
    cam_d.dof.focus_distance = dist
    cam_d.dof.aperture_fstop = min(90.0, 11 * 135 / (dist / MM))  # same relative blur as the pilot hero (f/11 at 135 mm)
    for path in ("lens",):
        K(cam_d, path, f)
    K(cam_d.dof, "focus_distance", f)
    K(cam_d.dof, "aperture_fstop", f)


def all_fcurves(ad):
    try:
        return list(ad.action.fcurves)
    except AttributeError:
        return [fc for layer in ad.action.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]


for idb in list(bpy.data.objects) + list(bpy.data.lights) + list(bpy.data.cameras) + list(bpy.data.materials) + list(bpy.data.worlds):
    for ad in (getattr(idb, "animation_data", None), getattr(getattr(idb, "node_tree", None), "animation_data", None)):
        if ad and ad.action:
            for fc in all_fcurves(ad):
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"

# ---------- 2D anchors for the overlay ----------
scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
scene.render.resolution_percentage = 100
anchors = {k: [] for k in T.get("anchorKeys", ["knobTop", "rgbTop", "rledTop", "btnTop"])}
for f in range(N):
    scene.frame_set(f)
    for k in anchors:
        c = world_to_camera_view(scene, cam, gl(*A[k]))
        anchors[k].append([round(c.x * 1080, 1), round((1 - c.y) * 1920, 1), 1 if c.z > 0 else 0])
with open(os.path.join(B, os.environ.get("ANCHORS", "anchors.json")), "w") as fh:
    json.dump({"fps": FPS, **anchors}, fh)

# ---------- render ----------
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
out = os.path.join(B, os.environ.get("FRAMES_DIR", "frames"))
os.makedirs(out, exist_ok=True)
if ONLY:
    for f in ONLY:
        scene.frame_set(f)
        scene.render.filepath = os.path.join(out, "test_%04d.png" % f)
        print("dbg", f, [tuple(round(x, 3) for x in rgb_bsdf.inputs[k].default_value) for k in ("Base Color", "Emission Color")],
              rgb_bsdf.inputs["Emission Strength"].default_value, [s.material.name for s in scene.objects["rgb|rgbled"].material_slots] if "rgb|rgbled" in scene.objects else [o.name for o in scene.objects if o.name.startswith("rgb")], flush=True)
        bpy.ops.render.render(write_still=True)
        print("frame", f, flush=True)
else:
    scene.frame_start, scene.frame_end = 0, N - 1
    scene.render.filepath = os.path.join(out, "f_")
    scene.render.use_overwrite = False
    scene.render.use_placeholder = True
    bpy.ops.render.render(animation=True)
print("done")
