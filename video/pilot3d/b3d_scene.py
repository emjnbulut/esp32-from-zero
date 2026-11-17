"""Shared Blender setup for the 3D pilot: imports the three.js export, applies physical materials,
desk, world, lights and colour management. Used by blender_hero.py (one frame) and blender_anim.py (animation).
"""
import bpy
from mathutils import Vector

MM = 0.001


def gl(x, y, z):
    """three.js / glTF (y-up, mm) -> Blender (z-up, m)."""
    return Vector((x * MM, -z * MM, y * MM))


def hexrgb(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, a)


def pbr(name, color, rough=0.5, metal=0.0, coat=0.0, emit=None, strength=0.0, trans=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexrgb(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Transmission Weight"].default_value = trans
    if emit:
        b.inputs["Emission Color"].default_value = hexrgb(emit)
        b.inputs["Emission Strength"].default_value = strength
    return m


def build(glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    scene = bpy.context.scene

    # the export is in millimetres -> real metres
    root = bpy.data.objects.new("pilot_root", None)
    scene.collection.objects.link(root)
    for o in list(scene.objects):
        if o is not root and o.parent is None:
            o.parent = root
    root.scale = (MM, MM, MM)

    lib = {
        "breadboard": pbr("bb", "#ecebe6", 0.42),
        "groove": pbr("groove", "#d3d0c7", 0.5),
        "hole": pbr("hole", "#24231f", 0.9),
        "rail#e5484d": pbr("railR", "#e5484d", 0.5),
        "rail#3b6fe0": pbr("railB", "#3b6fe0", 0.5),
        "pcb": pbr("pcb", "#0e1218", 0.55, coat=0.08),
        "header": pbr("header", "#111317", 0.45),
        "gold": pbr("gold", "#f2c35a", 0.22, metal=1.0),
        "module": pbr("module", "#22364c", 0.38, coat=0.4),
        "shield": pbr("shield", "#d4dae2", 0.24, metal=1.0),
        "usb": pbr("usb", "#d8dee6", 0.2, metal=1.0),
        "ic": pbr("ic", "#121418", 0.55),
        "button": pbr("button", "#d3d8de", 0.45),
        "pwrled": pbr("pwrled", "#ff3030", 0.3, emit="#ff2a2a", strength=6),
        "io2led": pbr("io2led", "#1d3f7a", 0.3),
        "led": pbr("led", "#a80000", 0.08, coat=1.0, emit="#ff0400", strength=4.0),
        "lead": pbr("lead", "#c3c9d1", 0.28, metal=1.0),
        "resistor": pbr("resistor", "#d9c39a", 0.55),
        "wire_gpio23": pbr("wireO", "#ff8a2a", 0.35, coat=0.3, emit="#ffb547", strength=0.0),
        "wire_gnd": pbr("wireK", "#1d1f24", 0.35, coat=0.3),
    }
    for o in scene.objects:
        if o.type != "MESH":
            continue
        for slot in o.material_slots:
            n = slot.material.name if slot.material else ""
            base = n.split(".")[0]
            if base in lib:
                slot.material = lib[base]
            elif base.startswith("band"):
                col = slot.material.diffuse_color
                slot.material = pbr(n + "_p", "#%02x%02x%02x" % tuple(int(max(0, min(1, c ** (1 / 2.2))) * 255) for c in col[:3]), 0.5)
        # flat boxes keep crisp edges: smooth only meshes with many faces (LED, wires, capsules)
        smooth = len(o.data.polygons) >= 200
        o.data.polygons.foreach_set("use_smooth", [smooth] * len(o.data.polygons))

    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(pbr("desk", "#16203a", 0.55))

    world = bpy.data.worlds.new("w")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = hexrgb("#0b1220")
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.12

    def area(name, loc, target, power, size, color="#ffffff"):
        d = bpy.data.lights.new(name, "AREA")
        d.energy, d.size, d.color = power, size, hexrgb(color)[:3]
        o = bpy.data.objects.new(name, d)
        scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = (target - o.location).to_track_quat("-Z", "Y").to_euler()
        return o

    c = gl(12, 8, 2)
    area("key", c + Vector((-0.10, -0.08, 0.16)), c, 1.1, 0.12, "#fff3e6")
    area("rim", c + Vector((0.06, 0.16, 0.08)), c, 0.9, 0.08, "#7fe8de")
    area("fill", c + Vector((0.14, -0.12, 0.05)), c, 0.25, 0.15, "#a9c4ff")
    ledp = bpy.data.lights.new("ledlight", "POINT")
    ledp.energy = 0.12
    ledp.color = hexrgb("#ff3b30")[:3]
    ledp.shadow_soft_size = 0.002
    ledlight = bpy.data.objects.new("ledlight", ledp)
    scene.collection.objects.link(ledlight)
    ledlight.location = gl(39.37, 19.5, 10.16)
    return scene, root, lib, ledlight


def color_management(scene):
    names = [i.identifier for i in scene.view_settings.bl_rna.properties["view_transform"].enum_items]
    scene.view_settings.view_transform = "Filmic" if "Filmic" in names else "Standard"
    scene.view_settings.exposure = -1.1


def use_gpu_cycles(scene, samples):
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = kind
            prefs.get_devices()
            if any(d.type == kind for d in prefs.devices):
                break
        except TypeError:
            continue
    for d in prefs.devices:
        d.use = d.type != "CPU"
    scene.cycles.device = "GPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    return [(d.name, d.type) for d in prefs.devices if d.use]
