"""Pin by Pin Lab Blender kit: procedural ESP32 parts for the 3D clips (Blender 5.x, EEVEE).

Layout (the same in every episode from Ep10 on): two 830-point breadboards lie HORIZONTALLY, one behind the
other; the ESP32 DevKit (30 pins) bridges them. Front board = "F", back board = "B". Rows run left -> right
(row 1 left), letters a (front) .. j (back) on both boards. ESP32 back pin row (D23 .. 3V3) sits in column a of
B, the front pin row (EN .. VIN) in column j of F; pin 1 (D23 / EN) on row 18, the pins run to row 4, USB on the
left. All part coordinates are millimetres under a root empty scaled 0.001 (Blender metres); the camera and
lights live in metres.

    import pbl; k = pbl.Kit(); F, B = k.boards(); esp = k.esp32(hot={"D21", ...}); k.wire(B.hole(4,"e"), ...)
"""
import math
import os

import bmesh
import bpy
from mathutils import Vector

P = 2.54
MM = 0.001
BB_W, BB_L, BB_H = 55.0, 165.0, 9.0
TOP = BB_H
LETTER = {"a": -15.24, "b": -12.7, "c": -10.16, "d": -7.62, "e": -5.08,
          "f": 5.08, "g": 7.62, "h": 10.16, "i": 12.7, "j": 15.24}
RAILY = {"lminus": -24.14, "lplus": -21.6, "rplus": 21.6, "rminus": 24.14}
BACK_PINS = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]
FRONT_PINS = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "C:/Windows/Fonts"

COL = {"red": "#e5484d", "black": "#202227", "yellow": "#f2c037", "green": "#2fbf71", "blue": "#3b82f6",
       "orange": "#ff8a2a", "white": "#e9edf2", "purple": "#9b6cf0"}


def lin(h):
    h = h.lstrip("#")
    s = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in s]


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


class Board:
    def __init__(self, name, yc, xc):
        self.name, self.yc, self.xc = name, yc, xc

    def hole(self, n, l):
        return Vector((self.xc + (n - 32) * P, self.yc + LETTER[l], TOP))

    def rail(self, n, side, sign):
        if n % 6 == 0:
            raise ValueError(f"no rail hole at row {n}")
        key = ("l" if side == "l" else "r") + ("plus" if sign == "+" else "minus")
        return Vector((self.xc + (n - 32) * P, self.yc + RAILY[key], TOP))


class Kit:
    def __init__(self, fps=30, res=(1920, 1080), engine="EEVEE"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        sc.render.fps = fps
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.resolution_percentage = 100
        self.mats = {}
        self.root = bpy.data.objects.new("kit_root", None)
        sc.collection.objects.link(self.root)
        self.root.scale = (MM, MM, MM)
        self.font_b = bpy.data.fonts.load(os.path.join(FONTS, "segoeuib.ttf")) if os.path.exists(os.path.join(FONTS, "segoeuib.ttf")) else None
        self.font_r = bpy.data.fonts.load(os.path.join(FONTS, "segoeui.ttf")) if os.path.exists(os.path.join(FONTS, "segoeui.ttf")) else None
        self._engine(engine)
        self._world()

    # ------------------------------------------------------------------ basics
    def _engine(self, engine):
        sc = self.scene
        ids = [i.identifier for i in sc.render.bl_rna.properties["engine"].enum_items]
        if engine == "CYCLES":
            sc.render.engine = "CYCLES"
        else:
            sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in ids else "BLENDER_EEVEE_NEXT"
            ee = sc.eevee
            for attr, val in (("taa_render_samples", 64), ("use_raytracing", True), ("use_shadows", True),
                              ("shadow_ray_count", 2), ("shadow_step_count", 8), ("use_gtao", True),
                              ("fast_gi_method", "GLOBAL_ILLUMINATION")):
                if hasattr(ee, attr):
                    try:
                        setattr(ee, attr, val)
                    except (TypeError, ValueError):
                        pass
            if hasattr(ee, "ray_tracing_options"):
                try:
                    ee.ray_tracing_options.resolution_scale = "1"
                except (TypeError, ValueError):
                    pass
        names = [i.identifier for i in sc.view_settings.bl_rna.properties["view_transform"].enum_items]
        sc.view_settings.view_transform = "AgX" if "AgX" in names else "Filmic"
        try:
            sc.view_settings.look = "AgX - Medium High Contrast"
        except TypeError:
            pass
        sc.view_settings.exposure = 0.0

    def _world(self):
        w = bpy.data.worlds.new("world")
        self.scene.world = w
        w.use_nodes = True
        bg = w.node_tree.nodes["Background"]
        bg.inputs["Color"].default_value = (*lin("#0d1424"), 1)
        bg.inputs["Strength"].default_value = 0.35

    def mat(self, name, color, rough=0.5, metal=0.0, coat=0.0, emit=None, strength=0.0, alpha=1.0, spec=0.5):
        if name in self.mats:
            return self.mats[name]
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*lin(color), 1)
        b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal
        b.inputs["Coat Weight"].default_value = coat
        if "Specular IOR Level" in b.inputs:
            b.inputs["Specular IOR Level"].default_value = spec
        if emit:
            b.inputs["Emission Color"].default_value = (*lin(emit), 1)
            b.inputs["Emission Strength"].default_value = strength
        if alpha < 1.0:
            b.inputs["Alpha"].default_value = alpha
        self.mats[name] = m
        return m

    def _link(self, ob, parent=None):
        self.scene.collection.objects.link(ob)
        ob.parent = parent or self.root
        return ob

    def empty(self, name, loc=(0, 0, 0), parent=None):
        e = bpy.data.objects.new(name, None)
        e.location = loc
        return self._link(e, parent)

    def mesh(self, name, bm, material, loc=(0, 0, 0), parent=None, bevel=0.0, smooth_shade=False, segs=2):
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        if smooth_shade:
            me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
        me.materials.append(material)
        ob = bpy.data.objects.new(name, me)
        ob.location = loc
        self._link(ob, parent)
        if bevel > 0:
            mod = ob.modifiers.new("bevel", "BEVEL")
            mod.width, mod.segments, mod.limit_method = bevel, segs, "ANGLE"
            mod.harden_normals = False
            if smooth_shade is False:
                try:
                    ob.data.shade_smooth()
                    mod.harden_normals = True
                except AttributeError:
                    pass
        return ob

    @staticmethod
    def bm_box(sx, sy, sz):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co.x *= sx
            v.co.y *= sy
            v.co.z *= sz
        return bm

    @staticmethod
    def bm_cyl(r, h, segs=32, r2=None):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r, radius2=r if r2 is None else r2, depth=h)
        return bm

    def box(self, name, size, loc, material, parent=None, bevel=0.0):
        return self.mesh(name, self.bm_box(*size), material, loc, parent, bevel)

    def cyl(self, name, r, h, loc, material, parent=None, segs=32, bevel=0.0, r2=None):
        ob = self.mesh(name, self.bm_cyl(r, h, segs, r2), material, loc, parent, bevel)
        ob.data.shade_smooth() if hasattr(ob.data, "shade_smooth") else None
        return ob

    def text(self, name, body, size, loc, material, parent=None, rot_z=0.0, align="CENTER", bold=True, valign="CENTER"):
        cu = bpy.data.curves.new(name, "FONT")
        cu.body = body
        cu.size = size
        cu.align_x = align
        cu.align_y = valign
        f = self.font_b if bold else self.font_r
        if f:
            cu.font = f
        ob = bpy.data.objects.new(name, cu)
        ob.location = loc
        ob.rotation_euler = (0, 0, rot_z)
        cu.materials.append(material)
        return self._link(ob, parent)

    # ------------------------------------------------------------------ desk + light
    def desk(self):
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=600)
        m = bpy.data.materials.new("desk")
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 0.08
        noise.inputs["Detail"].default_value = 6
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*lin("#121a2b"), 1)
        ramp.color_ramp.elements[1].color = (*lin("#1b263b"), 1)
        nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = 0.62
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.08
        nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
        return self.mesh("desk", bm, m, (35, 0, 0))

    def lights(self, center=(0.035, 0.0, 0.0), key=40.0):
        c = Vector(center)

        def area(name, offset, power, size, color):
            d = bpy.data.lights.new(name, "AREA")
            d.energy, d.size, d.color = power, size, lin(color)
            o = bpy.data.objects.new(name, d)
            self.scene.collection.objects.link(o)
            o.location = c + Vector(offset)
            o.rotation_euler = (c - o.location).to_track_quat("-Z", "Y").to_euler()
            return o

        area("key", (-0.16, -0.20, 0.30), key, 0.25, "#fff1e2")
        area("rim", (0.10, 0.26, 0.14), key * 0.9, 0.18, "#7fe8de")
        area("fill", (0.26, -0.12, 0.10), key * 0.25, 0.3, "#a9c4ff")

    # ------------------------------------------------------------------ breadboards
    def _bb_top_material(self):
        if "bbtop" in self.mats:
            return self.mats["bbtop"]
        m = bpy.data.materials.new("bbtop")
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        img = nt.nodes.new("ShaderNodeTexImage")
        img.image = bpy.data.images.load(os.path.join(HERE, "build", "breadboard.png"), check_existing=True)
        img.interpolation = "Cubic"
        nt.links.new(img.outputs["Color"], b.inputs["Base Color"])
        bw = nt.nodes.new("ShaderNodeRGBToBW")
        nt.links.new(img.outputs["Color"], bw.inputs["Color"])
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.35
        bump.inputs["Distance"].default_value = 0.6
        nt.links.new(bw.outputs["Val"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
        b.inputs["Roughness"].default_value = 0.42
        self.mats["bbtop"] = m
        return m

    def breadboard(self, name, yc, xc=(32 - 18) * P):
        side = self.mat("bbside", "#e6e4dd", 0.45)
        self.box(name + "_body", (BB_L, BB_W, BB_H), (xc, yc, BB_H / 2), side, bevel=1.2)
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        uvl = bm.loops.layers.uv.new()
        ix, iy = 1.2, 1.2
        for f in bm.faces:
            for loop in f.loops:
                v = loop.vert.co
                u, w = v.x + 0.5, v.y + 0.5
                loop[uvl].uv = (ix / 2 / BB_L + u * (1 - ix / BB_L), iy / 2 / BB_W + w * (1 - iy / BB_W))
        for v in bm.verts:
            v.co.x *= (BB_L - ix)
            v.co.y *= (BB_W - iy)
        self.mesh(name + "_top", bm, self._bb_top_material(), (xc, yc, BB_H + 0.012))
        return Board(name, yc, xc)

    def boards(self):
        """front board F (letters a-j, j next to the ESP32) and back board B (a next to the ESP32)"""
        F = self.breadboard("F", -28.0)
        B = self.breadboard("B", 28.0)
        return F, B

    # ------------------------------------------------------------------ ESP32 DevKit
    def esp32(self, hot=()):
        hot = set(hot)
        g = self.empty("esp32")
        yb, yf = LETTER["a"] + 28.0, LETTER["j"] - 28.0  # +12.76 / -12.76
        xA, xU = 8.94, 8.94 - 51.5  # antenna edge, USB edge
        pcb_z = TOP + 2.5
        pcb_top = pcb_z + 1.6
        Wd = (yb - yf) + 2.9
        xc = (xA + xU) / 2
        self.box("esp_pcb", (51.5, Wd, 1.6), (xc, 0, pcb_z + 0.8), self.mat("pcb", "#161b23", 0.5, coat=0.15), g, bevel=0.5)
        for y in (yb, yf):
            self.box("esp_header", (15 * P, 2.5, 2.5), (-7 * P, y, TOP + 1.25), self.mat("header", "#14171c", 0.5), g, bevel=0.2)
        gold = self.mat("gold", "#e9bd55", 0.25, metal=1.0)
        bm = bmesh.new()
        for i in range(15):
            for y in (yb, yf):
                for (sx, sy, sz, z) in ((1.9, 1.9, 0.06, pcb_top + 0.03), (0.64, 0.64, 1.4, pcb_top + 0.7)):
                    t = self.bm_box(sx, sy, sz)
                    bmesh.ops.translate(t, verts=t.verts, vec=(-i * P, y, z))
                    me = bpy.data.meshes.new("tmp")
                    t.to_mesh(me)
                    t.free()
                    bm.from_mesh(me)
                    bpy.data.meshes.remove(me)
        self.mesh("esp_pins", bm, gold, (0, 0, 0), g)
        modW, modL = (yb - yf) - 9.5, 25.5
        self.box("esp_module", (modL, modW, 0.8), (xA - 0.4 - modL / 2, 0, pcb_top + 0.4), self.mat("module", "#22364f", 0.4, coat=0.3), g)
        shX = xA - 0.4 - 6.3 - 17.8 / 2
        self.box("esp_shield", (17.8, modW - 2.4, 2.4), (shX, 0, pcb_top + 2.0), self.mat("shield", "#c9d0d9", 0.28, metal=1.0), g, bevel=0.35)
        lab = self.mat("shieldtext", "#5d6670", 0.6)
        self.text("esp_lab1", "ESP32-WROOM-32", 2.0, (shX, 1.5, pcb_top + 3.21), lab, g)
        self.text("esp_lab2", "Pin by Pin Lab", 1.3, (shX, -2.0, pcb_top + 3.21), lab, g, bold=False)
        for s in range(5):  # antenna meander
            self.box("esp_ant", (0.45, modW - 5, 0.05), (xA - 1.6 - s * 0.9, 0, pcb_top + 0.83), gold, g)
        self.box("esp_usb", (5.8, 7.8, 2.8), (xU + 1.9, 0, pcb_top + 1.4), self.mat("usbmetal", "#d5dbe2", 0.22, metal=1.0), g, bevel=0.4)
        ic = self.mat("ic", "#111317", 0.5)
        self.box("esp_ic1", (5, 5, 1), (xU + 12, 4.5, pcb_top + 0.5), ic, g, bevel=0.2)
        self.box("esp_ic2", (3.6, 6.5, 1.6), (xU + 13, -5.0, pcb_top + 0.8), ic, g, bevel=0.2)
        for dy in (-9.0, 9.0):
            self.box("esp_btn", (4.0, 3.6, 1.3), (xU + 5.5, dy, pcb_top + 0.65), self.mat("btnbody", "#cfd5dc", 0.4, metal=0.6), g)
            self.cyl("esp_btncap", 1.1, 0.8, (xU + 5.5, dy, pcb_top + 1.6), ic, g)
        self.pwr_mat = bpy.data.materials.new("pwrled")
        self.pwr_mat.use_nodes = True
        pb = self.pwr_mat.node_tree.nodes["Principled BSDF"]
        pb.inputs["Base Color"].default_value = (*lin("#5a1a1a"), 1)
        pb.inputs["Emission Color"].default_value = (*lin("#ff2a2a"), 1)
        pb.inputs["Emission Strength"].default_value = 30.0
        pwr = self.box("esp_pwr", (1.6, 1.0, 0.7), (xU + 9.5, -2.2, pcb_top + 0.35), self.pwr_mat, g)
        # printed pin names, reading bottom -> top from the front camera; amber = used in this video
        cold = self.mat("pintext", "#c3cbd7", 0.6)
        warm = self.mat("pinhot", "#ffb547", 0.4, emit="#ffb547", strength=1.2)
        for i in range(15):
            x = -i * P + 0.42
            for names, y, align in ((BACK_PINS, yb - 1.45, "RIGHT"), (FRONT_PINS, yf + 1.45, "LEFT")):
                nm = names[i]
                on = nm in hot
                self.text("pin_" + nm + str(i), nm, 1.25 if on else 1.05, (x, y, pcb_top + 0.02), warm if on else cold, g,
                          rot_z=math.pi / 2, align=align, valign="CENTER")
        self.esp = {"group": g, "pcb_top": pcb_top, "xU": xU, "xA": xA, "pwr": pwr}
        return self.esp

    def pin(self, row_side, i):
        """position of ESP32 pin i (0 = D23/EN) on the back ('b') or front ('f') row"""
        return Vector((-i * P, 12.76 if row_side == "b" else -12.76, self.esp["pcb_top"] + 1.4))

    def usb_cable(self):
        e = self.esp
        g = self.empty("usb", (0, 0, 0))
        z = e["pcb_top"] + 1.4
        x0 = e["xU"]
        dark = self.mat("usbcord", "#24282f", 0.45)
        self.box("usb_plug", (13, 10.5, 6.2), (x0 - 7.2, 0, z), dark, g, bevel=1.4)
        self.box("usb_metal", (3.0, 7.0, 2.2), (x0 - 0.6, 0, z), self.mats["usbmetal"], g, bevel=0.2)
        cu = bpy.data.curves.new("usb_cord", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = 2.0
        cu.bevel_resolution = 4
        sp = cu.splines.new("BEZIER")
        pts = [(x0 - 13.5, 0, z), (x0 - 32, 2, z - 1), (x0 - 52, 10, 3.0), (x0 - 120, 38, 2.0)]
        sp.bezier_points.add(len(pts) - 1)
        for bp, p in zip(sp.bezier_points, pts):
            bp.co = p
            bp.handle_left_type = bp.handle_right_type = "AUTO"
        ob = bpy.data.objects.new("usb_cord", cu)
        cu.materials.append(dark)
        self._link(ob, g)
        return g

    # ------------------------------------------------------------------ parts
    def wire(self, a, b, color, h=None, name="wire", via=None):
        a, b = Vector(a), Vector(b)
        d = (b - a).length
        if h is None:
            h = max(3.0, min(13.0, 0.16 * d + 2.0))
        cu = bpy.data.curves.new(name, "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = 0.62
        cu.bevel_resolution = 3
        cu.use_fill_caps = True
        sp = cu.splines.new("BEZIER")
        lift = Vector((0, 0, 2.4))
        mids = [Vector((p[0], p[1], TOP + h)) for p in via] if via else [a.lerp(b, 0.12) + Vector((0, 0, h)), a.lerp(b, 0.88) + Vector((0, 0, h))]
        pts = [a + lift] + mids + [b + lift]
        sp.bezier_points.add(len(pts) - 1)
        for bp, p in zip(sp.bezier_points, pts):
            bp.co = p
            bp.handle_left_type = bp.handle_right_type = "AUTO"
        for bp, sgn in ((sp.bezier_points[0], 1), (sp.bezier_points[-1], -1)):
            bp.handle_left_type = bp.handle_right_type = "FREE"
            up = Vector((0, 0, min(h * 0.55, 4.0)))
            if sgn > 0:
                bp.handle_right = bp.co + up
                bp.handle_left = bp.co - up
            else:
                bp.handle_left = bp.co + up
                bp.handle_right = bp.co - up
        ob = bpy.data.objects.new(name, cu)
        cu.materials.append(self.mat("wire_" + color, COL.get(color, color), 0.38, coat=0.35))
        self._link(ob)
        tip = self.mat("tip", "#c8ced6", 0.25, metal=1.0)
        for p in (a, b):
            self.cyl(name + "_tip", 0.33, 3.6, (p.x, p.y, TOP + 0.6), tip, segs=12)
        return ob

    def oled(self, board, rows, col="f", frames_dir=None, nframes=1):
        """0.96" I2C OLED lying on its header (GND VCC SCL SDA on rows[0..3], column col), screen toward the front"""
        hs = [board.hole(r, col) for r in rows]
        g = self.empty("oled")
        cx = sum(h.x for h in hs) / 4
        hy = hs[0].y
        pw, ph = 27.3, 27.8
        cy = hy - (ph / 2 - 1.7)
        z0 = TOP + 2.5
        self.box("oled_spacer", (4 * P, 2.5, 2.5), (cx, hy, TOP + 1.25), self.mats.get("header") or self.mat("header", "#14171c", 0.5), g, bevel=0.2)
        self.box("oled_pcb", (pw, ph, 1.2), (cx, cy, z0 + 0.6), self.mat("oledpcb", "#1d4f91", 0.42, coat=0.3), g, bevel=0.4)
        gold = self.mats["gold"]
        for h in hs:
            self.box("oled_pin", (0.64, 0.64, 1.2), (h.x, h.y, z0 + 1.8), gold, g)
            self.cyl("oled_pad", 0.95, 0.05, (h.x, h.y, z0 + 1.22), gold, g, segs=20)
        for dx in (-pw / 2 + 2.0, pw / 2 - 2.0):
            for dy in (-ph / 2 + 2.0, ph / 2 - 2.0):
                self.cyl("oled_hole_ring", 1.4, 0.04, (cx + dx, cy + dy, z0 + 1.22), gold, g, segs=24)
                self.cyl("oled_hole", 0.9, 0.06, (cx + dx, cy + dy, z0 + 1.24), self.mat("holedark", "#0a0c10", 0.9), g, segs=24)
        silk = self.mat("silk", "#eef2f6", 0.6)
        for h, nm in zip(hs, ("GND", "VCC", "SCL", "SDA")):
            self.text("oled_lab_" + nm, nm, 0.95, (h.x, h.y - 2.0, z0 + 1.21), silk, g)
        gy = cy - 1.6
        self.box("oled_glass", (26.0, 15.0, 1.3), (cx, gy, z0 + 1.2 + 0.65), self.mat("oledglass", "#050608", 0.22, coat=0.25, spec=0.3), g, bevel=0.15)
        self.box("oled_flex", (12, 2.0, 0.3), (cx, gy - 8.3, z0 + 1.35), self.mat("flex", "#c98a2b", 0.4), g)
        # screen: emissive image (sequence)
        m = bpy.data.materials.new("oledscreen")
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.003, 0.003, 0.004, 1)
        b.inputs["Roughness"].default_value = 0.25
        b.inputs["Coat Weight"].default_value = 0.2
        if "Specular IOR Level" in b.inputs:
            b.inputs["Specular IOR Level"].default_value = 0.25
        img = nt.nodes.new("ShaderNodeTexImage")
        img.interpolation = "Closest"
        if frames_dir:
            first = os.path.join(frames_dir, "s_0001.png")
            im = bpy.data.images.load(first)
            im.source = "SEQUENCE" if nframes > 1 else "FILE"
            img.image = im
            if nframes > 1:
                img.image_user.frame_duration = nframes
                img.image_user.frame_start = 1
                img.image_user.frame_offset = 0
                img.image_user.use_auto_refresh = True
        nt.links.new(img.outputs["Color"], b.inputs["Emission Color"])
        b.inputs["Emission Strength"].default_value = 7.0
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        uvl = bm.loops.layers.uv.new()
        for f in bm.faces:
            for loop in f.loops:
                loop[uvl].uv = (loop.vert.co.x + 0.5, loop.vert.co.y + 0.5)
        for v in bm.verts:
            v.co.x *= 21.74
            v.co.y *= 10.86
        self.mesh("oled_screen", bm, m, (cx, gy + 0.6, z0 + 1.2 + 1.31), g)
        self.oled_info = {"group": g, "center": Vector((cx, gy + 0.6, z0 + 2.5)), "screen_mat": m}
        return self.oled_info

    def buzzer(self, plus, minus):
        """passive buzzer, + leg in hole `plus`, - leg in hole `minus`"""
        plus, minus = Vector(plus), Vector(minus)
        c = (plus + minus) / 2
        g = self.empty("buzzer")
        body = self.mat("buzzbody", "#16181c", 0.42)
        self.cyl("buzz_body", 6.0, 8.5, (c.x, c.y, TOP + 0.6 + 4.25), body, g, segs=48, bevel=0.6)
        self.cyl("buzz_hole", 1.1, 0.4, (c.x, c.y, TOP + 0.6 + 8.35), self.mat("holedark", "#0a0c10", 0.9), g, segs=24)
        self.cyl("buzz_ring", 2.3, 0.1, (c.x, c.y, TOP + 0.6 + 8.52), self.mat("buzzring", "#2a2d33", 0.3), g, segs=40)
        self.text("buzz_plus", "+", 2.4, (plus.x + (c.x - plus.x) * 0.25, plus.y + 2.6, TOP + 0.6 + 8.52), self.mats.get("silk") or self.mat("silk", "#eef2f6", 0.6), g)
        self.buzz = {"group": g, "top": Vector((c.x, c.y, TOP + 9.2))}
        return self.buzz

    def button(self, holes, cap="#f2c037"):
        """12x12 tactile switch straddling the groove; holes = four Vector hole positions"""
        c = sum((Vector(h) for h in holes), Vector()) / 4
        g = self.empty("button")
        self.box("btn_body", (12, 12, 3.5), (c.x, c.y, TOP + 1.75), self.mat("btnblack", "#15171b", 0.5), g, bevel=0.3)
        self.box("btn_plate", (12.2, 12.2, 0.3), (c.x, c.y, TOP + 3.65), self.mat("steel", "#c3c9d1", 0.3, metal=1.0), g)
        for dx in (-4.6, 4.6):
            for dy in (-4.6, 4.6):
                self.cyl("btn_dot", 0.6, 0.4, (c.x + dx, c.y + dy, TOP + 3.9), self.mats["steel"], g, segs=12)
        press = self.empty("btn_press", (c.x, c.y, TOP + 3.8), g)
        self.cyl("btn_plunger", 1.8, 1.6, (0, 0, 0.6), self.mats["btnblack"], press, segs=24)
        self.cyl("btn_cap", 4.6, 3.6, (0, 0, 2.7), self.mat("btncap", cap, 0.35, coat=0.4), press, segs=48, bevel=0.8)
        self.btn = {"group": g, "press": press, "top": Vector((c.x, c.y, TOP + 8))}
        return self.btn

    def sound_rings(self, center, n=3, color="#7fe8de"):
        """expanding rings above a buzzer; returns list of (object, value node) to key"""
        rings = []
        for i in range(n):
            m = bpy.data.materials.new(f"ring{i}")
            m.use_nodes = True
            nt = m.node_tree
            for nd in list(nt.nodes):
                nt.nodes.remove(nd)
            out = nt.nodes.new("ShaderNodeOutputMaterial")
            em = nt.nodes.new("ShaderNodeEmission")
            em.inputs["Color"].default_value = (*lin(color), 1)
            em.inputs["Strength"].default_value = 6.0
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            mix = nt.nodes.new("ShaderNodeMixShader")
            val = nt.nodes.new("ShaderNodeValue")
            val.outputs[0].default_value = 0.0
            nt.links.new(val.outputs[0], mix.inputs["Fac"])
            nt.links.new(tr.outputs[0], mix.inputs[1])
            nt.links.new(em.outputs[0], mix.inputs[2])
            nt.links.new(mix.outputs[0], out.inputs["Surface"])
            if hasattr(m, "surface_render_method"):
                m.surface_render_method = "BLENDED"
            elif hasattr(m, "blend_method"):
                m.blend_method = "BLEND"
            bm = bmesh.new()
            bmesh.ops.create_circle(bm, cap_ends=False, segments=64, radius=1.0)
            me = bpy.data.meshes.new("ring")
            bm.to_mesh(me)
            bm.free()
            ob = bpy.data.objects.new(f"ring{i}", me)
            me.materials.append(m)
            ob.location = center
            self._link(ob)
            sk = ob.modifiers.new("skin", "WIREFRAME")
            sk.thickness = 0.03
            sk.use_relative_offset = False
            rings.append((ob, val))
        return rings

    # ------------------------------------------------------------------ camera
    def camera(self, lens=50, fstop=2.2):
        cd = bpy.data.cameras.new("cam")
        cd.lens = lens
        cd.sensor_width = 36
        cd.clip_start = 0.005
        cd.clip_end = 10
        cam = bpy.data.objects.new("cam", cd)
        self.scene.collection.objects.link(cam)
        tgt = bpy.data.objects.new("cam_target", None)
        self.scene.collection.objects.link(tgt)
        con = cam.constraints.new("TRACK_TO")
        con.target = tgt
        con.track_axis = "TRACK_NEGATIVE_Z"
        con.up_axis = "UP_Y"
        cd.dof.use_dof = True
        cd.dof.focus_object = tgt
        cd.dof.aperture_fstop = fstop
        self.scene.camera = cam
        self.cam, self.tgt = cam, tgt
        return cam, tgt

    def world_pos(self, v_mm):
        return Vector(v_mm) * MM

    def glare(self, threshold=1.0, size=7):
        """bloom on bright pixels (screen, LEDs, rings) via the compositor; silently skipped if the API differs"""
        sc = self.scene
        try:
            if hasattr(sc, "compositing_node_group"):
                ng = bpy.data.node_groups.new("comp", "CompositorNodeTree")
                sc.compositing_node_group = ng
                rl = ng.nodes.new("CompositorNodeRLayers")
                gl = ng.nodes.new("CompositorNodeGlare")
                out = ng.nodes.new("NodeGroupOutput")
                ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
                for key, val in (("Type", "Bloom"), ("Quality", "High")):
                    if key in gl.inputs:
                        try:
                            gl.inputs[key].default_value = val
                        except (TypeError, ValueError):
                            gl.inputs[key].default_value = "Fog Glow"
                for key, val in (("Threshold", threshold), ("Size", 0.55), ("Strength", 0.6)):
                    if key in gl.inputs:
                        gl.inputs[key].default_value = val
                ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
                ng.links.new(gl.outputs["Image"], out.inputs[0])
            else:
                sc.use_nodes = True
                nt = sc.node_tree
                rl = nt.nodes.get("Render Layers") or nt.nodes.new("CompositorNodeRLayers")
                comp = nt.nodes.get("Composite") or nt.nodes.new("CompositorNodeComposite")
                gl = nt.nodes.new("CompositorNodeGlare")
                gl.glare_type = "FOG_GLOW"
                gl.threshold = threshold
                gl.size = size
                nt.links.new(rl.outputs["Image"], gl.inputs["Image"])
                nt.links.new(gl.outputs["Image"], comp.inputs["Image"])
            return True
        except Exception as e:  # noqa: BLE001
            print("glare skipped:", e)
            return False


def key(ob, path, frame, value=None, index=-1):
    if value is not None:
        if index >= 0:
            getattr(ob, path)[index] = value
        else:
            setattr(ob, path, value)
    ob.keyframe_insert(path, frame=frame, index=index)
