"""HC-SR501 PIR motion sensor for the Pin by Pin Lab Blender kit (Episode 11). Separate module so pbl.py stays untouched.

    import pbl, parts_pir
    k = pbl.Kit(); F, B = k.boards()
    pir = parts_pir.pir(k, [B.hole(40, "f"), B.hole(41, "f"), B.hole(42, "f")])   # VCC, OUT, GND legs
    beams = parts_pir.zones(k, pir)                                              # fan of lens "windows"
    parts_pir.set_zones(beams, {2: 1.0})                                         # light window 2
    pir["pot_time"].rotation_euler.z = angle                                     # trim pots turn

Real module: green PCB 32 x 24 mm, white faceted Fresnel dome (~23 mm) on top; on the underside the three pins
(VCC, OUT, GND), two orange trim pots (time, sensitivity) and the L/H jumper. Here the PCB sits on 7 mm pins with the
dome up, so the pots are under the board: shots of the knobs lift and tilt the module with pir["lift"] (an empty
between the legs and the PCB; rotate/translate it). All sizes in mm, parented to the kit root like every part.
"""
import math

import bmesh
import bpy
from mathutils import Vector

import pbl
from pbl import TOP, lin

PCB = (32.0, 24.0, 1.6)
STANDOFF = 7.0      # pin length above the breadboard
DOME_R = 11.5


def _value_mat(k, name, color, strength=4.0, alpha_max=0.55, fade_len=None):
    """emission <-> transparent mix driven by a Value node (0 = invisible), like pbl.sound_rings"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*lin(color), 1)
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    val = nt.nodes.new("ShaderNodeValue")
    val.outputs[0].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = alpha_max
    nt.links.new(val.outputs[0], mul.inputs[0])
    if fade_len:  # fade out with the distance from the object origin (the beam's tip at the dome)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        ln = nt.nodes.new("ShaderNodeVectorMath")
        ln.operation = "LENGTH"
        dv = nt.nodes.new("ShaderNodeMath")
        dv.operation = "DIVIDE"
        dv.inputs[1].default_value = fade_len
        inv = nt.nodes.new("ShaderNodeMath")
        inv.operation = "SUBTRACT"
        inv.inputs[0].default_value = 1.0
        inv.use_clamp = True
        m2 = nt.nodes.new("ShaderNodeMath")
        m2.operation = "MULTIPLY"
        nt.links.new(tc.outputs["Object"], ln.inputs[0])
        nt.links.new(ln.outputs["Value"], dv.inputs[0])
        nt.links.new(dv.outputs[0], inv.inputs[1])
        nt.links.new(mul.outputs[0], m2.inputs[0])
        nt.links.new(inv.outputs[0], m2.inputs[1])
        nt.links.new(m2.outputs[0], mix.inputs["Fac"])
    else:
        nt.links.new(mul.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    elif hasattr(m, "blend_method"):
        m.blend_method = "BLEND"
    return m, val


def _dome(k, parent, z):
    """faceted half-sphere (the Fresnel lens): low segment count + flat shading reads as the real facets"""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=10, radius=DOME_R)
    for v in [v for v in bm.verts if v.co.z < -0.01]:
        bm.verts.remove(v)
    for v in bm.verts:
        v.co.z *= 0.78
    white = k.mat("pirdome", "#f4f5f2", 0.55, coat=0.1)
    tr = white.node_tree.nodes["Principled BSDF"]
    if "Subsurface Weight" in tr.inputs:  # milky plastic
        tr.inputs["Subsurface Weight"].default_value = 0.25
    ob = k.mesh("pir_dome", bm, white, (0, 0, z), parent)
    k.cyl("pir_ring", DOME_R + 0.8, 1.8, (0, 0, z - 0.6), k.mat("pirring", "#e9ebe6", 0.5), parent, segs=48, bevel=0.3)
    return ob


def pir(k, legs, dy=0.0):
    """legs = three hole Vectors in one letter column, rows next to each other: VCC, OUT, GND (left -> right)."""
    legs = [Vector(h) for h in legs]
    g = k.empty("pir")
    c = sum(legs, Vector()) / 3 + Vector((0, dy, 0))
    steel = k.mat("legsteel", "#c8ced6", 0.3, metal=1.0)
    for i, h in enumerate(legs):  # pins standing in the holes, plastic header block on top
        k.box("pir_pin%d" % i, (0.64, 0.64, STANDOFF + 1.0), (h.x, h.y, TOP + (STANDOFF - 1.0) / 2), steel, g)
    k.box("pir_header", (7.6, 2.5, 2.5), (c.x, legs[0].y, TOP + STANDOFF - 1.25), k.mat("hdrblack", "#16181c", 0.5), g)
    lift = k.empty("pir_lift", (c.x, c.y, TOP + STANDOFF), g)  # move/rotate this to show the underside
    k.box("pir_pcb", PCB, (0, 0, PCB[2] / 2), k.mat("pirpcb", "#1f7a46", 0.45, coat=0.3), lift, bevel=0.3)
    # underside parts (visible when lifted): two trim pots, jumper, a chip
    pot_m = k.mat("pirpot", "#ff8a2a", 0.4)
    slot_m = k.mat("pirslot", "#2a1606", 0.6)
    pots = {}
    for name, x in (("time", -9.0), ("sens", 9.0)):
        holder = k.empty("pir_pot_" + name, (x, -7.0, -1.6), lift)
        k.cyl("pir_potbody_" + name, 2.6, 2.6, (0, 0, 0), pot_m, holder, segs=32, bevel=0.3)
        k.box("pir_potslot_" + name, (3.6, 0.6, 0.4), (0, 0, -1.4), slot_m, holder)
        pots[name] = holder
    k.box("pir_jumper", (2.6, 5.0, 2.2), (0, 7.5, -1.1), k.mat("jumper", "#f2c037", 0.5), lift)
    k.box("pir_chip", (6.0, 4.0, 1.2), (0, 0, -0.6), k.mat("pirchip", "#101215", 0.4), lift)
    silk = k.mats.get("silk") or k.mat("silk", "#eef2f6", 0.6)
    for txt, h in zip(("VCC", "OUT", "GND"), legs):  # printed pin names on the PCB edge (top side)
        k.text("pir_lbl_" + txt, txt, 1.6, (h.x - c.x, h.y - c.y + 2.6, PCB[2] + 0.02), silk, lift)
    dome = _dome(k, lift, PCB[2] + 1.0)
    top = Vector((c.x, c.y, TOP + STANDOFF + PCB[2] + 1.0 + DOME_R * 0.78))
    info = {"group": g, "lift": lift, "dome": dome, "pot_time": pots["time"], "pot_sens": pots["sens"],
            "pins": {"VCC": legs[0], "OUT": legs[1], "GND": legs[2]}, "center": c, "top": top}
    k.pir_info = info
    return info


def zones(k, info, n=9, spread=110.0, reach=85.0, tilt=16.0, color="#ffb547"):
    """fan of translucent wedges from the dome = the lens windows, each looking at its own slice of the room.
    Returns [(object, value node)]; value 0 = hidden, 1 = lit. Wedges fan out toward -Y (the camera side)."""
    beams = []
    half = math.radians(spread) / 2
    step = 2 * half / n
    base = info["top"] - Vector((0, 0, 3.0))
    for i in range(n):
        a0 = -half + i * step + step * 0.08
        a1 = a0 + step * 0.84
        bm = bmesh.new()
        z_up = math.tan(math.radians(tilt)) * reach
        v0 = bm.verts.new((0, 0, 0))
        far = []
        for a in (a0, a1):
            for dz in (-z_up * 0.15, z_up):
                far.append(bm.verts.new((reach * math.sin(a), -reach * math.cos(a), dz)))
        bm.faces.new((v0, far[0], far[1]))
        bm.faces.new((v0, far[3], far[2]))
        bm.faces.new((v0, far[1], far[3]))
        bm.faces.new((v0, far[2], far[0]))
        bm.faces.new((far[0], far[2], far[3], far[1]))
        m, val = _value_mat(k, "pirbeam%d" % i, color, strength=3.0, alpha_max=0.42, fade_len=reach)
        ob = k.mesh("pir_beam%d" % i, bm, m, tuple(base))
        beams.append((ob, val))
    return beams


def set_zones(beams, lit, idle=0.0):
    """lit = {index: 0..1}; every other wedge gets `idle` (e.g. 0.08 for a faint 'the sensor is watching')"""
    for i, (ob, val) in enumerate(beams):
        v = max(idle, lit.get(i, 0.0))
        val.outputs[0].default_value = v
        ob.hide_render = v <= 0.001
