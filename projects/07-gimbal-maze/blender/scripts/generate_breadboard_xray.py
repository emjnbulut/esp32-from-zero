"""
ESP32 From Zero - Shorts (9:16 Dikey) "Adim Adim Breadboard Montaj & X-Ray" Sahnesi (v2 - Ultra Kalite)
Blender 5.2 Otomatik Animasyonlu Sahne Ureticisi

Yenilikler (v2):
  1. GERCEKCI MAKRO DONANIM DETAYI:
     - Breadboard: Pahli (beveled) kare delik yuvalari, satir/sutun yazilari (1..30, a..j, +/-),
       icinde gercek 5-parmakli fosfor-bronz yay klipsleri!
     - ESP32 DevKit V1: PCB uzerinde okunabilir pin isimleri (D34, D35, D18, D19, VIN, GND, 3V3),
       gravurlu ESP-WROOM-32 metal kalkani, altin anten, CP2102 cipi, AMS1117 regulator, SMD elemanlar.
     - KY-023 Joystick: Torna profiliyle (bmesh.ops.spin) modellenmis gercek konkav (icbukey)
       ergonomik basparmak mantar basligi, metal gimbal kutusu, yan potansiyometreler ve SW butonu.
     - 2x MG90S Servo: Kademeli disli kubbesi, 4 kose vida sutunu, delikli aerodinamik servo kolu (horn),
       metalik etiket plakasi.
     - Jumper Kablolar: Iki ucunda siyah DuPont konnektor + altindan cikan parlak metal erkek pin ucu!
  2. TEK TEK BREADBOARD'A TAKILMA ANİMASYONU (360 Kare / 12 sn @ 30fps):
     - Kare   1..50 : Bos breadboard -> X-Ray acilir, icteki gizli bakir seritler gorunur
     - Kare  50..90 : ESP32 DevKit V1 yukaridan inip breadboard'a oturur, guc LED'i yanar
     - Kare  90..150: 5V Kirmizi, GND Siyah, Ray Kopruleri ve 470uF Kondansator TEK TEK takilir
     - Kare 150..220: Joystick gelir; GND, 3.3V (Mor), VRx (Yesil), VRy (Mavi) kablolari TEK TEK takilir
     - Kare 220..275: Servo X gelir; 5V, GND ve Turuncu (D18) kablosu TEK TEK takilir ve test donusu yapar
     - Kare 275..325: Servo Y gelir; 5V, GND ve Sari (D19) kablosu TEK TEK takilir
     - Kare 325..360: Joystick iki eksende hareket eder, ince neon sinyal darbeleri akar ve iki servo doner!
  3. EEVEE Raytracing + Fast GI + Yuksek Cozunurluklu Yumusak Golgeler + Studio Softbox Aydinlatma.
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Matrix

# ==============================================================================
#  DOSYA YOLLARI
# ==============================================================================
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
BLENDER_DIR = os.path.join(PROJECT_DIR, "blender")
PREVIEW_DIR = os.path.join(PROJECT_DIR, "previews")

os.makedirs(BLENDER_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

# ==============================================================================
#  400-DELİKLİ BREADBOARD ÖLÇÜLERİ (1 BU = 1 mm)
# ==============================================================================
PITCH    = 2.54
NUM_COLS = 30
BB_W     = 84.0
BB_D     = 55.5
BB_H     = 9.4

def col_x(c):
    return (c - (NUM_COLS - 1) / 2.0) * PITCH

ROW_Y = {
    'top_neg':  22.86,
    'top_pos':  20.32,
    'j':        13.97,
    'i':        11.43,
    'h':         8.89,
    'g':         6.35,
    'f':         3.81,
    'e':        -3.81,
    'd':        -6.35,
    'c':        -8.89,
    'b':       -11.43,
    'a':       -13.97,
    'bot_pos': -20.32,
    'bot_neg': -22.86,
}

def hole_pt(col, row_name, z=BB_H):
    return Vector((col_x(col), ROW_Y[row_name], z))


# ==============================================================================
#  YARDIMCI FONKSİYONLAR
# ==============================================================================
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.length_unit = 'MILLIMETERS'
    scene.unit_settings.scale_length = 0.001
    scene.render.engine = 'BLENDER_EEVEE'

    # EEVEE Kalite Ayarlari (Raytracing + Fast GI + Yumusak Golgeler)
    eevee = scene.eevee
    eevee.taa_render_samples = 48
    if hasattr(eevee, "use_raytracing"):
        eevee.use_raytracing = True
    if hasattr(eevee, "use_fast_gi"):
        eevee.use_fast_gi = True
    if hasattr(eevee, "use_shadows"):
        eevee.use_shadows = True
        eevee.shadow_ray_count = 4
        eevee.shadow_step_count = 8
    if hasattr(eevee, "use_overscan"):
        eevee.use_overscan = True
        eevee.overscan_size = 4.0


def get_col(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def link_obj(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def set_material(obj, mat):
    if obj.type == 'MESH':
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        for p in obj.data.polygons:
            p.material_index = 0
    elif hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(mat)


def make_mat(name, color, roughness=0.32, metallic=0.0, emission=None, emission_strength=0.0, alpha=1.0, coat=0.15):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Alpha"].default_value = alpha
        if "Coat Weight" in bsdf.inputs:
            bsdf.inputs["Coat Weight"].default_value = coat
        if emission is not None:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    if alpha < 0.999 and hasattr(mat, "surface_render_method"):
        mat.surface_render_method = 'BLENDED'
    return mat


def make_box(name, size, center=(0, 0, 0), mat=None, col=None, bevel=0.0, segs=2, parent=None):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=segs, affect='EDGES', clamp_overlap=True)
    bmesh.ops.translate(bm, vec=Vector(center), verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    if mat:
        set_material(obj, mat)
    link_obj(obj, col or bpy.context.scene.collection)
    if parent:
        obj.parent = parent
    return obj


def make_cyl(name, radius, depth, center=(0, 0, 0), axis='Z', mat=None, col=None, segs=32, parent=None, r2=None):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segs,
        radius1=radius, radius2=radius if r2 is None else r2, depth=depth,
    )
    if axis == 'X':
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'), verts=bm.verts)
    elif axis == 'Y':
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'X'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(center), verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    if mat:
        set_material(obj, mat)
    link_obj(obj, col or bpy.context.scene.collection)
    if parent:
        obj.parent = parent
    return obj


def make_text_3d(name, text, size, loc, rot_deg=(0, 0, 0), mat=None, col=None, extrude=0.06, align_x='CENTER', align_y='CENTER', parent=None):
    fdata = bpy.data.curves.new(name=name, type='FONT')
    fdata.body = text
    fdata.size = size
    fdata.extrude = extrude
    fdata.align_x = align_x
    fdata.align_y = align_y
    obj = bpy.data.objects.new(name, fdata)
    obj.location = Vector(loc)
    obj.rotation_euler = tuple(math.radians(a) for a in rot_deg)
    if mat:
        set_material(obj, mat)
    link_obj(obj, col or bpy.context.scene.collection)
    if parent:
        obj.parent = parent
    return obj


def animate_drop_in(root_obj, target_loc, f_start, duration=14, drop_height=34.0):
    """
    Parçayı veya kabloyu f_start karesine kadar gizler (scale=0),
    sonra yukarıdan (Z + drop_height) yumuşak bir overshoot/snap ile yerine takar!
    """
    tloc = Vector(target_loc)
    high_loc = tloc + Vector((0.0, 0.0, drop_height))
    bounce_loc = tloc - Vector((0.0, 0.0, 0.7))

    # Başlangıçta görünmez ve yukarıda
    root_obj.location = high_loc
    root_obj.scale = (0.001, 0.001, 0.001)
    root_obj.keyframe_insert("location", frame=1)
    root_obj.keyframe_insert("scale", frame=1)

    if f_start > 2:
        root_obj.keyframe_insert("location", frame=f_start - 1)
        root_obj.keyframe_insert("scale", frame=f_start - 1)

    # Belirme anı (yukarıda tam boyuta hızla açılır)
    f_appear = f_start + 3
    root_obj.location = high_loc
    root_obj.scale = (1.0, 1.0, 1.0)
    root_obj.keyframe_insert("location", frame=f_appear)
    root_obj.keyframe_insert("scale", frame=f_appear)

    # Yuvasına oturma (hafif tatlı esneme ile tık diye oturur)
    f_land = f_start + duration - 3
    root_obj.location = bounce_loc
    root_obj.keyframe_insert("location", frame=f_land)

    f_settle = f_start + duration
    root_obj.location = tloc
    root_obj.keyframe_insert("location", frame=f_settle)


# ==============================================================================
#  BÖLÜM 1: YÜKSEK DETAYLI BREADBOARD + GİZLİ 5-PARMAKLI YAY ŞERİTLERİ
# ==============================================================================
def build_breadboard_and_strips(col_bb, col_strips):
    mat_shell = make_mat("BB_XRay_Shell", (0.94, 0.94, 0.92), roughness=0.22, alpha=1.0, coat=0.35)
    if hasattr(mat_shell, "surface_render_method"):
        mat_shell.surface_render_method = 'BLENDED'

    # X-Ray Geçişi: Kare 1..18 katı (1.0), Kare 18..46 şeffaf cam (0.18), 46..360 açık!
    bsdf = mat_shell.node_tree.nodes.get("Principled BSDF")
    alpha_in = bsdf.inputs["Alpha"]
    for fr, val in ((1, 1.0), (18, 1.0), (46, 0.18), (360, 0.18)):
        alpha_in.default_value = val
        alpha_in.keyframe_insert(data_path="default_value", frame=fr)

    # Ana Breadboard Gövdesi (üst yarı, alt yarı, orta DIP kanalı, yan geçme tırnakları)
    half_d = (BB_D - 3.4) / 2.0
    make_box("BB_TopHalf", (BB_W, half_d, BB_H), center=(0, (BB_D + 3.4) / 4.0, BB_H / 2.0), mat=mat_shell, col=col_bb, bevel=0.6)
    make_box("BB_BotHalf", (BB_W, half_d, BB_H), center=(0, -(BB_D + 3.4) / 4.0, BB_H / 2.0), mat=mat_shell, col=col_bb, bevel=0.6)
    make_box("BB_CenterGroove", (BB_W, 4.0, BB_H - 2.2), center=(0, 0, (BB_H - 2.2) / 2.0), mat=mat_shell, col=col_bb)

    # Yan kenarlarda gerçek breadboard birleştirme tırnakları (dovetail tabs)
    for y_off in (-16.0, 0.0, 16.0):
        make_box(f"BB_Tab_L_{y_off}", (1.4, 4.2, BB_H - 1.5), center=(-BB_W / 2.0 - 0.5, y_off, (BB_H - 1.5) / 2.0), mat=mat_shell, col=col_bb, bevel=0.3)

    # Kırmızı (+) ve Mavi (-) Güç Otoyolu Çizgileri
    mat_red_line  = make_mat("BB_RedLine",  (0.92, 0.12, 0.12), roughness=0.32)
    mat_blue_line = make_mat("BB_BlueLine", (0.08, 0.42, 0.96), roughness=0.32)
    mat_label_txt = make_mat("BB_TextGray", (0.28, 0.32, 0.38), roughness=0.5)
    line_len = BB_W - 8.0

    make_box("Stripe_TopNeg", (line_len, 0.65, 0.18), center=(0,  24.65, BB_H + 0.04), mat=mat_blue_line, col=col_bb)
    make_box("Stripe_TopPos", (line_len, 0.65, 0.18), center=(0,  18.55, BB_H + 0.04), mat=mat_red_line,  col=col_bb)
    make_box("Stripe_BotPos", (line_len, 0.65, 0.18), center=(0, -18.55, BB_H + 0.04), mat=mat_red_line,  col=col_bb)
    make_box("Stripe_BotNeg", (line_len, 0.65, 0.18), center=(0, -24.65, BB_H + 0.04), mat=mat_blue_line, col=col_bb)

    # Breadboard üzerindeki gerçek sütun numaraları (1, 5, 10, 15, 20, 25, 30) ve satır harfleri
    for c_num in (1, 5, 10, 15, 20, 25, 30):
        cx = col_x(c_num - 1)
        make_text_3d(f"ColNumT_{c_num}", str(c_num), 1.65, (cx,  16.3, BB_H + 0.03), mat=mat_label_txt, col=col_bb, extrude=0.03)
        make_text_3d(f"ColNumB_{c_num}", str(c_num), 1.65, (cx, -16.3, BB_H + 0.03), mat=mat_label_txt, col=col_bb, extrude=0.03)

    for r_let in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'):
        ry = ROW_Y[r_let]
        make_text_3d(f"RowL_{r_let}", r_let, 1.6, (-BB_W / 2.0 + 2.4, ry, BB_H + 0.03), mat=mat_label_txt, col=col_bb, extrude=0.03)
        make_text_3d(f"RowR_{r_let}", r_let, 1.6, ( BB_W / 2.0 - 2.4, ry, BB_H + 0.03), mat=mat_label_txt, col=col_bb, extrude=0.03)

    for sgn_x in (-BB_W / 2.0 + 2.4, BB_W / 2.0 - 2.4):
        make_text_3d(f"PlusT_{sgn_x}",  "+", 2.2, (sgn_x,  20.32, BB_H + 0.04), mat=mat_red_line,  col=col_bb, extrude=0.04)
        make_text_3d(f"MinusT_{sgn_x}", "-", 2.4, (sgn_x,  22.86, BB_H + 0.04), mat=mat_blue_line, col=col_bb, extrude=0.04)
        make_text_3d(f"PlusB_{sgn_x}",  "+", 2.2, (sgn_x, -20.32, BB_H + 0.04), mat=mat_red_line,  col=col_bb, extrude=0.04)
        make_text_3d(f"MinusB_{sgn_x}", "-", 2.4, (sgn_x, -22.86, BB_H + 0.04), mat=mat_blue_line, col=col_bb, extrude=0.04)

    # Pahlı (chamfered) kare pin yuvaları — tek mesh içinde iç çukur + pahlı çerçeve!
    mat_socket_dark = make_mat("BB_Socket_Dark", (0.03, 0.035, 0.045), roughness=0.65)
    mat_socket_rim  = make_mat("BB_Socket_Rim",  (0.78, 0.80, 0.82),   roughness=0.35)

    h_mesh = bpy.data.meshes.new("BB_Sockets_Mesh")
    h_obj = bpy.data.objects.new("BB_Sockets_Mesh", h_mesh)
    bm = bmesh.new()
    for c in range(NUM_COLS):
        cx = col_x(c)
        for rname, ry in ROW_Y.items():
            if rname.startswith(('top_', 'bot_')) and c in (0, 6, 12, 17, 23, 29):
                continue
            # Kare iç delik
            ret = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=Vector((1.08, 1.08, 0.45)), verts=ret['verts'])
            bmesh.ops.translate(bm, vec=Vector((cx, ry, BB_H - 0.12)), verts=ret['verts'])
    bm.to_mesh(h_mesh)
    bm.free()
    set_material(h_obj, mat_socket_dark)
    link_obj(h_obj, col_bb)

    # ---------------- GİZLİ İÇ FOSFOR-BRONZ YAY ŞERİTLERİ ----------------
    mat_copper_idle = make_mat("Phosphor_Bronze", (0.82, 0.62, 0.38), roughness=0.24, metallic=0.85)

    def make_strip_glow_mat(name, color, f_on, peak=7.5):
        m = make_mat(name, color, roughness=0.22, metallic=0.55, emission=color, emission_strength=0.0)
        em = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for fr, val in ((1, 0.0), (max(1, f_on - 3), 0.0), (f_on + 4, peak * 1.35), (f_on + 14, peak), (360, peak)):
            em.default_value = val
            em.keyframe_insert("default_value", frame=fr)
        return m

    # Her şerit tam ilgili kablo takıldığı karede parlamaya başlar!
    mat_bot_5v   = make_strip_glow_mat("Glow_Bot5V",   (1.0, 0.14, 0.08), f_on=100, peak=6.5)
    mat_bot_gnd  = make_strip_glow_mat("Glow_BotGND",  (0.08, 0.68, 1.0), f_on=114, peak=6.0)
    mat_top_5v   = make_strip_glow_mat("Glow_Top5V",   (1.0, 0.14, 0.08), f_on=127, peak=6.5)
    mat_top_gnd  = make_strip_glow_mat("Glow_TopGND",  (0.08, 0.68, 1.0), f_on=133, peak=6.0)

    mat_s_3v3    = make_strip_glow_mat("Glow_3V3",     (0.78, 0.20, 1.0), f_on=184, peak=7.5)
    mat_s_vrx    = make_strip_glow_mat("Glow_VRx",     (0.10, 0.96, 0.34), f_on=200, peak=8.0)
    mat_s_vry    = make_strip_glow_mat("Glow_VRy",     (0.12, 0.58, 1.0), f_on=214, peak=8.0)
    mat_s_sx     = make_strip_glow_mat("Glow_ServoX",  (1.0, 0.44, 0.05), f_on=268, peak=8.5)
    mat_s_sy     = make_strip_glow_mat("Glow_ServoY",  (1.0, 0.86, 0.06), f_on=320, peak=8.5)

    # 4 adet Yatay Güç Otoyolu (alt omurga + her delikte dikey yay klips dişleri!)
    def build_power_rail_strip(name, ry, mat_rail):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bm = bmesh.new()
        rail_len = (NUM_COLS - 2) * PITCH
        # Alt omurga şeridi
        r_base = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((rail_len, 1.35, 1.0)), verts=r_base['verts'])
        bmesh.ops.translate(bm, vec=Vector((0.0, ry, 3.3)), verts=r_base['verts'])
        # Her delik noktasında çift dudaklı yay klipsi
        for c in range(NUM_COLS):
            if c in (0, 6, 12, 17, 23, 29):
                continue
            cx = col_x(c)
            clip = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=Vector((1.3, 1.45, 2.8)), verts=clip['verts'])
            bmesh.ops.translate(bm, vec=Vector((cx, ry, 5.0)), verts=clip['verts'])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
        set_material(obj, mat_rail)
        link_obj(obj, col_strips)

    build_power_rail_strip("Bus_Top_GND", ROW_Y['top_neg'], mat_top_gnd)
    build_power_rail_strip("Bus_Top_5V",  ROW_Y['top_pos'], mat_top_5v)
    build_power_rail_strip("Bus_Bot_5V",  ROW_Y['bot_pos'], mat_bot_5v)
    build_power_rail_strip("Bus_Bot_GND", ROW_Y['bot_neg'], mat_bot_gnd)

    active_top = {
        8:  mat_s_sy,    # D19 (Sarı)
        9:  mat_s_sx,    # D18 (Turuncu)
        17: mat_s_3v3,   # 3V3 (Mor)
        21: mat_s_3v3,   # 3V3 Köprü
    }
    active_bot = {
        6:  mat_s_vrx,   # D34 (Yeşil)
        7:  mat_s_vry,   # D35 (Mavi)
        16: mat_bot_gnd, # GND
        17: mat_bot_5v,  # VIN 5V
    }

    # 60 adet Dikey 5-Parmaklı Yay Şeridi (gerçek 5 ayrı klips dişi + alt taban!)
    def build_5clip_strip(name, cx, rows_5, mat_s):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bm = bmesh.new()
        y_center = sum(ROW_Y[r] for r in rows_5) / 5.0
        # Alt omurga
        base = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((1.2, 4.4 * PITCH, 1.0)), verts=base['verts'])
        bmesh.ops.translate(bm, vec=Vector((cx, y_center, 3.3)), verts=base['verts'])
        # 5 adet yaylı kıskaç kulesi (her delik altında iki yan yaprak!)
        for r in rows_5:
            ry = ROW_Y[r]
            for side in (-0.42, 0.42):
                leaf = bmesh.ops.create_cube(bm, size=1.0)
                bmesh.ops.scale(bm, vec=Vector((0.36, 1.45, 2.9)), verts=leaf['verts'])
                bmesh.ops.translate(bm, vec=Vector((cx + side, ry, 5.1)), verts=leaf['verts'])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
        set_material(obj, mat_s)
        link_obj(obj, col_strips)

    for c in range(NUM_COLS):
        cx = col_x(c)
        build_5clip_strip(f"ClipTop_{c:02d}", cx, ('f', 'g', 'h', 'i', 'j'), active_top.get(c, mat_copper_idle))
        build_5clip_strip(f"ClipBot_{c:02d}", cx, ('a', 'b', 'c', 'd', 'e'), active_bot.get(c, mat_copper_idle))


# ==============================================================================
#  BÖLÜM 2: YÜKSEK DETAYLI MODÜLLER (TEK TEK TAKILMA ANİMASYONLU!)
# ==============================================================================
def build_esp32_detailed(col_mod, f_plug=55):
    """
    Yüksek detaylı 30-pin DOIT ESP32 DevKit V1.
    f_plug karesinde yukarıdan inerek breadboard'a (i ve b satırlarına) saplanır!
    """
    root = bpy.data.objects.new("ESP32_DevKit_Root", None)
    link_obj(root, col_mod)

    mat_pcb      = make_mat("ESP_PCB_Matte", (0.04, 0.048, 0.065), roughness=0.32, coat=0.25)
    mat_subpcb   = make_mat("ESP_ModulePCB", (0.03, 0.12, 0.07),   roughness=0.35)
    mat_shield   = make_mat("ESP_RF_Shield", (0.84, 0.87, 0.91),   roughness=0.22, metallic=0.58, coat=0.3)
    mat_etch     = make_mat("ESP_Etch_Dark", (0.22, 0.25, 0.30),   roughness=0.4)
    mat_gold     = make_mat("ESP_Gold",      (0.98, 0.78, 0.22),   roughness=0.22, metallic=0.72)
    mat_chip     = make_mat("ESP_IC_Black",  (0.06, 0.06, 0.07),   roughness=0.35)
    mat_btn_body = make_mat("ESP_Btn_Metal", (0.78, 0.80, 0.84),   roughness=0.28, metallic=0.5)
    mat_silk     = make_mat("ESP_Silkscreen",(0.92, 0.94, 0.96),   roughness=0.4)
    mat_smd_tan  = make_mat("ESP_SMD_Cap",   (0.72, 0.54, 0.32),   roughness=0.35)

    # Güç LED'i ESP32 takıldığı anda (f_plug + 15) yanar!
    mat_led_r = make_mat("ESP_LED_Red",  (1.0, 0.12, 0.08), emission=(1.0, 0.14, 0.08), emission_strength=0.0)
    mat_led_b = make_mat("ESP_LED_Blue", (0.10, 0.55, 1.0), emission=(0.12, 0.62, 1.0), emission_strength=0.0)
    for m, peak in ((mat_led_r, 16.0), (mat_led_b, 18.0)):
        em = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for fr, val in ((1, 0.0), (f_plug + 12, 0.0), (f_plug + 16, peak), (360, peak)):
            em.default_value = val
            em.keyframe_insert("default_value", frame=fr)

    x_left  = col_x(3) - 6.2
    x_right = col_x(17) + 4.8
    pcb_cx  = (x_left + x_right) / 2.0
    pcb_w   = x_right - x_left
    pcb_d   = 25.8
    pcb_z   = BB_H + 5.4

    # 1. Ana PCB + 4 köşe altın montaj halkası
    make_box("ESP_MainPCB", (pcb_w, pcb_d, 1.6), center=(pcb_cx, 0, pcb_z), mat=mat_pcb, col=col_mod, bevel=0.4, parent=root)
    for mx in (x_left + 2.2, x_right - 2.2):
        for my in (-pcb_d / 2.0 + 2.2, pcb_d / 2.0 - 2.2):
            make_cyl(f"ESP_Mnt_{mx:.0f}_{my:.0f}", 1.4, 1.7, center=(mx, my, pcb_z), mat=mat_gold, col=col_mod, parent=root)

    # 2. ESP-WROOM-32 Alt Modül PCB + Castellated Altın Lehim Pedleri + RF Metal Kalkan
    mod_cx = x_left + 11.2
    make_box("ESP_WROOM_SubPCB", (19.5, 18.2, 0.8), center=(mod_cx - 1.5, 0, pcb_z + 1.2), mat=mat_subpcb, col=col_mod, bevel=0.2, parent=root)
    make_box("ESP_WROOM_Shield", (15.2, 17.2, 2.8), center=(mod_cx + 1.0, 0, pcb_z + 2.6), mat=mat_shield, col=col_mod, bevel=0.45, parent=root)
    make_text_3d("ESP_Shield_Txt", "ESP-WROOM-32", 1.55, (mod_cx + 1.0, 0.5, pcb_z + 4.02), mat=mat_etch, col=col_mod, extrude=0.04, parent=root)

    # Castellated (yarım daire) kenar altın lehim pedleri
    for i in range(8):
        py = -7.0 + i * 2.0
        make_box(f"ESP_CastR_{i}", (0.8, 1.1, 1.0), center=(mod_cx + 8.7, py, pcb_z + 1.2), mat=mat_gold, col=col_mod, parent=root)
    for i in range(7):
        px = mod_cx - 5.0 + i * 2.0
        make_box(f"ESP_CastT_{i}", (1.1, 0.8, 1.0), center=(px,  9.1, pcb_z + 1.2), mat=mat_gold, col=col_mod, parent=root)
        make_box(f"ESP_CastB_{i}", (1.1, 0.8, 1.0), center=(px, -9.1, pcb_z + 1.2), mat=mat_gold, col=col_mod, parent=root)

    # Kıvrımlı Altın PCB Anten İzi (Meander Antenna)
    ant_x = x_left + 2.8
    for i in range(5):
        ay = -6.0 + i * 3.0
        make_box(f"ESP_AntH_{i}", (3.4, 0.55, 0.18), center=(ant_x, ay, pcb_z + 1.65), mat=mat_gold, col=col_mod, parent=root)
    make_box("ESP_AntBarL", (0.55, 12.5, 0.18), center=(ant_x - 1.5, 0, pcb_z + 1.65), mat=mat_gold, col=col_mod, parent=root)
    make_box("ESP_AntBarR", (0.55, 12.5, 0.18), center=(ant_x + 1.5, 0, pcb_z + 1.65), mat=mat_gold, col=col_mod, parent=root)

    # 3. CP2102 USB-UART Çipi + AMS1117-3.3 Voltaj Regülatörü + Kristal + SMD Dizisi
    make_box("ESP_CP2102",  (4.8, 4.8, 0.9), center=(x_right - 12.5, -1.5, pcb_z + 1.2), mat=mat_chip, col=col_mod, bevel=0.15, parent=root)
    make_box("ESP_AMS1117", (6.2, 3.6, 1.5), center=(x_right - 18.5,  5.0, pcb_z + 1.5), mat=mat_chip, col=col_mod, bevel=0.15, parent=root)
    make_box("ESP_AMS_Tab", (2.2, 3.0, 0.4), center=(x_right - 18.5,  7.2, pcb_z + 1.0), mat=mat_shield, col=col_mod, parent=root)
    make_box("ESP_Crystal", (3.2, 2.0, 0.8), center=(x_right - 13.0,  4.2, pcb_z + 1.2), mat=mat_shield, col=col_mod, bevel=0.2, parent=root)

    # Küçük SMD kapasitör ve dirençler
    smd_coords = [
        (x_right - 16.5, -5.0), (x_right - 16.5, -3.2), (x_right - 16.5, -1.4),
        (x_right - 22.0,  2.5), (x_right - 22.0,  0.5), (x_right - 22.0, -1.5),
    ]
    for idx, (sx, sy) in enumerate(smd_coords):
        make_box(f"ESP_SMD_{idx}", (1.6, 0.85, 0.65), center=(sx, sy, pcb_z + 1.1), mat=mat_smd_tan, col=col_mod, parent=root)

    # 4. Micro-USB Portu + EN & BOOT Taktil Butonlar + LED'ler
    make_box("ESP_USB_Shell",  (6.2, 7.8, 2.8), center=(x_right - 1.6, 0, pcb_z + 2.1), mat=mat_shield, col=col_mod, bevel=0.35, parent=root)
    make_box("ESP_USB_Recess", (2.0, 5.6, 1.4), center=(x_right + 0.6, 0, pcb_z + 2.1), mat=mat_chip,   col=col_mod, parent=root)

    for bname, by in (("EN", 6.8), ("BOOT", -6.8)):
        make_box(f"ESP_Btn_{bname}", (3.4, 4.2, 1.4), center=(x_right - 6.2, by, pcb_z + 1.4), mat=mat_btn_body, col=col_mod, bevel=0.2, parent=root)
        make_cyl(f"ESP_Cap_{bname}", 1.1, 0.8, center=(x_right - 6.2, by, pcb_z + 2.2), mat=mat_chip, col=col_mod, parent=root)
        make_text_3d(f"ESP_Txt_{bname}", bname, 1.35, (x_right - 9.2, by, pcb_z + 0.84), mat=mat_silk, col=col_mod, extrude=0.03, parent=root)

    make_box("ESP_LED_PWR", (1.6, 1.0, 0.75), center=(x_right - 9.8, -3.5, pcb_z + 1.1), mat=mat_led_r, col=col_mod, parent=root)
    make_box("ESP_LED_IO2", (1.6, 1.0, 0.75), center=(x_right - 9.8,  3.5, pcb_z + 1.1), mat=mat_led_b, col=col_mod, parent=root)

    # 5. PCB Üzerinde Gerçek Silkscreen Pin İsimleri!
    top_labels = {3:"23", 4:"22", 7:"21", 8:"D19", 9:"D18", 10:"D5", 13:"D4", 14:"D2", 16:"GND", 17:"3V3"}
    bot_labels = {3:"EN", 4:"VP", 6:"D34", 7:"D35", 8:"32",  9:"33", 10:"25", 11:"26", 16:"GND", 17:"VIN"}
    for c, lbl in top_labels.items():
        make_text_3d(f"SilkT_{c}", lbl, 1.32, (col_x(c), 10.6, pcb_z + 0.84), mat=mat_silk, col=col_mod, extrude=0.03, parent=root)
    for c, lbl in bot_labels.items():
        make_text_3d(f"SilkB_{c}", lbl, 1.32, (col_x(c), -10.6, pcb_z + 0.84), mat=mat_silk, col=col_mod, extrude=0.03, parent=root)

    # 6. 30 Adet Altın Pin Header + Siyah Plastik İzolatör Şeritleri
    for r in ('i', 'b'):
        make_box(f"ESP_HdrPlastic_{r}", (15 * PITCH, 2.4, 2.4), center=(col_x(10), ROW_Y[r], pcb_z - 2.0), mat=mat_chip, col=col_mod, parent=root)

    pin_mesh = bpy.data.meshes.new("ESP_GoldPins_Mesh")
    pin_obj = bpy.data.objects.new("ESP_GoldPins_Mesh", pin_mesh)
    bm = bmesh.new()
    for c in range(3, 18):
        cx = col_x(c)
        for r in ('i', 'b'):
            ret = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=Vector((0.64, 0.64, 9.5)), verts=ret['verts'])
            bmesh.ops.translate(bm, vec=Vector((cx, ROW_Y[r], BB_H + 1.8)), verts=ret['verts'])
    bm.to_mesh(pin_mesh)
    bm.free()
    set_material(pin_obj, mat_gold)
    link_obj(pin_obj, col_mod)
    pin_obj.parent = root

    # Yukarıdan breadboard'a takılma animasyonu!
    animate_drop_in(root, (0, 0, 0), f_start=f_plug, duration=16, drop_height=38.0)
    return root


def build_capacitor_detailed(col_mod, f_plug=136):
    """470uF Elektrolitik Kondansatör — f_plug karesinde yukarıdan güç rayına takılır!"""
    root = bpy.data.objects.new("Cap_470uF_Root", None)
    link_obj(root, col_mod)

    mat_sleeve = make_mat("Cap_Navy",   (0.05, 0.08, 0.16), roughness=0.22, coat=0.45)
    mat_alu    = make_mat("Cap_Alu",    (0.86, 0.88, 0.92), roughness=0.20, metallic=0.75)
    mat_stripe = make_mat("Cap_Stripe", (0.78, 0.82, 0.88), roughness=0.28)
    mat_dark   = make_mat("Cap_Groove", (0.15, 0.16, 0.18), roughness=0.5)

    cx = col_x(24)
    cy = (ROW_Y['bot_pos'] + ROW_Y['bot_neg']) / 2.0
    cz = BB_H + 8.5

    make_cyl("Cap_Body", 4.1, 11.5, center=(cx, cy, cz), mat=mat_sleeve, col=col_mod, segs=36, parent=root)
    make_cyl("Cap_TopAlu", 3.8, 0.6, center=(cx, cy, cz + 5.8), mat=mat_alu, col=col_mod, segs=36, parent=root)
    # Üst basınç tahliye çizgileri (X-cross)
    make_box("Cap_Vent1", (6.2, 0.25, 0.2), center=(cx, cy, cz + 6.12), mat=mat_dark, col=col_mod, parent=root)
    make_box("Cap_Vent2", (0.25, 6.2, 0.2), center=(cx, cy, cz + 6.12), mat=mat_dark, col=col_mod, parent=root)
    # Eksi (-) şeridi
    make_box("Cap_NegStripe", (1.8, 0.8, 11.2), center=(cx, cy - 3.8, cz), mat=mat_stripe, col=col_mod, parent=root)
    make_text_3d("Cap_Label", "470uF", 1.35, (cx, cy + 0.5, cz + 6.15), mat=mat_dark, col=col_mod, extrude=0.02, parent=root)

    # İki metal bacak
    make_cyl("Cap_LegPos", 0.35, 6.5, center=(cx, ROW_Y['bot_pos'], BB_H + 1.5), mat=mat_alu, col=col_mod, segs=12, parent=root)
    make_cyl("Cap_LegNeg", 0.35, 6.5, center=(cx, ROW_Y['bot_neg'], BB_H + 1.5), mat=mat_alu, col=col_mod, segs=12, parent=root)

    animate_drop_in(root, (0, 0, 0), f_start=f_plug, duration=14, drop_height=32.0)
    return root


def build_sculpted_thumbstick_cap(name, mat_rubber, col, parent):
    """
    bmesh.ops.spin (torna profili) ile gerçek ergonomik KONKAV (içbükey) PS4/KY-023
    başparmak mantar başlığı üretir!
    """
    # Yarıçap (X) ve Yükseklik (Z) profil noktaları (milimetre)
    profile = [
        (0.0,  0.0),
        (2.4,  0.0),   # Alt şaft girişi
        (2.1,  5.5),   # İnce boyun
        (4.5,  7.5),   # Alt kubbe eteği
        (8.8,  9.8),   # Mantar dış genişleme
        (10.4, 11.4),  # Dış tutuş kenarı
        (10.6, 12.6),  # En dış tırtıklı halka
        (9.8,  13.4),  # Üst kenar dudak zirvesi (raised rim)
        (8.2,  13.1),  # İçbükey çukur başlangıcı
        (5.5,  12.2),  # İçbükey başparmak yuvası
        (2.5,  11.8),  # Merkez çukur tabanı
        (0.0,  11.7),  # Merkez kapanış
    ]

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bm = bmesh.new()

    verts = [bm.verts.new((r, 0.0, z)) for (r, z) in profile]
    for i in range(len(verts) - 1):
        bm.edges.new((verts[i], verts[i + 1]))

    bmesh.ops.spin(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        cent=(0.0, 0.0, 0.0),
        axis=(0.0, 0.0, 1.0),
        angle=2.0 * math.pi,
        steps=48,
        use_merge=True,
    )
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.02)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    # Smooth shading
    for p in obj.data.polygons:
        p.use_smooth = True

    set_material(obj, mat_rubber)
    link_obj(obj, col)
    obj.parent = parent
    return obj


def build_joystick_detailed(col_mod, f_plug=150):
    """Gerçekçi KY-023 Analog Joystick Modülü — f_plug karesinde sahneye oturur."""
    root = bpy.data.objects.new("Joystick_KY023_Root", None)
    link_obj(root, col_mod)

    mat_pcb    = make_mat("Joy_PCB_Dark",  (0.05, 0.055, 0.07), roughness=0.32, coat=0.25)
    mat_metal  = make_mat("Joy_Steel",     (0.78, 0.81, 0.85),  roughness=0.24, metallic=0.65)
    mat_rubber = make_mat("Joy_RubberCap", (0.10, 0.11, 0.13),  roughness=0.52, coat=0.08)
    mat_pot    = make_mat("Joy_PotGreen",  (0.10, 0.52, 0.28),  roughness=0.38)
    mat_orange = make_mat("Joy_SwOrange",  (0.92, 0.36, 0.08),  roughness=0.35)
    mat_gold   = make_mat("ESP_Gold",      (0.98, 0.78, 0.22),  roughness=0.22, metallic=0.72)
    mat_silk   = make_mat("ESP_Silkscreen",(0.92, 0.94, 0.96),  roughness=0.4)
    mat_blk    = make_mat("ESP_IC_Black",  (0.06, 0.06, 0.07),  roughness=0.35)

    jx, jy = -6.0, -49.0

    # 1. PCB + 4 köşe montaj halkası + Silkscreen yazılar
    make_box("Joy_PCB", (27.5, 33.5, 1.8), center=(jx, jy, 2.0), mat=mat_pcb, col=col_mod, bevel=0.5, parent=root)
    for mx in (jx - 11.2, jx + 11.2):
        for my in (jy - 14.2, jy + 14.2):
            make_cyl(f"Joy_Hole_{mx:.0f}_{my:.0f}", 1.5, 2.0, center=(mx, my, 2.0), mat=mat_gold, col=col_mod, parent=root)

    make_text_3d("Joy_SilkTitle", "KY-023 JOYSTICK", 1.5, (jx, jy - 14.5, 2.95), mat=mat_silk, col=col_mod, extrude=0.03, parent=root)

    # 2. Metal Gimbal Kutusu + İç Yarım Küre Körüklü Kubbe + 2 Yan Potansiyometre + SW Butonu
    gy = jy - 1.5
    make_box("Joy_GimbalMetal", (16.2, 16.2, 10.5), center=(jx, gy, 8.0), mat=mat_metal, col=col_mod, bevel=0.45, parent=root)
    make_cyl("Joy_DustDome", 6.2, 4.5, center=(jx, gy, 13.0), mat=mat_blk, col=col_mod, segs=32, parent=root, r2=3.2)

    # X ve Y Potansiyometreleri (yeşil gövde + metal çerçeve)
    make_box("Joy_PotX_Green", (3.2, 9.8, 8.8), center=(jx + 9.6, gy, 7.8), mat=mat_pot, col=col_mod, bevel=0.25, parent=root)
    make_box("Joy_PotY_Green", (9.8, 3.2, 8.8), center=(jx, gy - 9.6, 7.8), mat=mat_pot, col=col_mod, bevel=0.25, parent=root)
    # Sol tarafta SW taktil buton
    make_box("Joy_SW_Base", (4.5, 6.2, 3.8), center=(jx - 9.8, gy, 5.2), mat=mat_metal, col=col_mod, bevel=0.2, parent=root)
    make_cyl("Joy_SW_Btn",  1.6, 1.5, center=(jx - 12.2, gy, 5.2), axis='X', mat=mat_orange, col=col_mod, parent=root)

    # 3. Torna Profiliyle Modellenmiş Konkav Ergonomik Başparmak Başlığı (Hareketli Pivot!)
    pivot = bpy.data.objects.new("Joy_Thumb_Pivot", None)
    pivot.location = (jx, gy, 11.5)
    link_obj(pivot, col_mod)
    pivot.parent = root

    build_sculpted_thumbstick_cap("Joy_SculptedCap", mat_rubber, col_mod, parent=pivot)

    # Joystick Eğim Animasyonu:
    # - Kare 258..275: Servo X takılınca sadece sağa-sola (X) test eğimi yapar!
    # - Kare 322..360: Servo Y de takılınca her iki eksende canlı eğim yapar!
    joy_keys = [
        (1,   (0, 0)),
        (255, (0, 0)),
        (264, (0, 22)),
        (272, (0, -20)),
        (280, (0, 0)),
        (320, (0, 0)),
        (332, (20, 22)),
        (345, (-22, -20)),
        (355, (16, -16)),
        (360, (0, 0)),
    ]
    for fr, (rx, ry) in joy_keys:
        pivot.rotation_euler = (math.radians(rx), math.radians(ry), 0.0)
        pivot.keyframe_insert("rotation_euler", frame=fr)

    # 4. Üst Kenarda 4 Pin Header + Silkscreen Pin Etiketleri
    pin_positions = {}
    pin_names = ['GND', 'VCC', 'VRx', 'VRy']
    make_box("Joy_HdrPlastic", (16.5, 2.5, 2.5), center=(jx, jy + 13.5, 4.0), mat=mat_blk, col=col_mod, parent=root)
    for i, pname in enumerate(pin_names):
        px = jx + (i - 1.5) * 3.8
        py = jy + 13.5
        make_cyl(f"Joy_Pin_{pname}", 0.42, 6.2, center=(px, py, 6.0), mat=mat_gold, col=col_mod, segs=12, parent=root)
        make_text_3d(f"Joy_Lbl_{pname}", pname, 1.15, (px, py - 2.3, 2.95), mat=mat_silk, col=col_mod, extrude=0.03, parent=root)
        pin_positions[pname] = Vector((px, py, 8.2))

    animate_drop_in(root, (0, 0, 0), f_start=f_plug, duration=14, drop_height=34.0)
    return pin_positions


def build_servo_detailed(name, label_txt, pos_xy, accent_color, horn_keyframes, col_mod, f_plug):
    """
    Yüksek detaylı MG90S Metal Dişli Mikro Servo + Delikli Beyaz Servo Kolu.
    f_plug karesinde yukarıdan inerek yerine oturur!
    """
    root = bpy.data.objects.new(f"{name}_Root", None)
    link_obj(root, col_mod)

    mat_blue  = make_mat(f"{name}_Cobalt", (0.04, 0.16, 0.38), roughness=0.24, coat=0.35)
    mat_band  = make_mat(f"{name}_AluBand",(0.14, 0.16, 0.20), roughness=0.28, metallic=0.45)
    mat_brass = make_mat("MG90S_Brass",    (0.92, 0.72, 0.20), roughness=0.20, metallic=0.80)
    mat_horn  = make_mat("MG90S_HornW",    (0.95, 0.96, 0.97), roughness=0.28, coat=0.2)
    mat_badge = make_mat(f"{name}_Badge",  accent_color, roughness=0.3, emission=accent_color, emission_strength=1.8)
    mat_dark  = make_mat("ESP_IC_Black",   (0.06, 0.06, 0.07), roughness=0.35)

    sx, sy = pos_xy

    # 1. Alt kapak + orta koyu metal kuşak + üst mavi dişli kasası
    make_box(f"{name}_BotCap",  (22.8, 12.4, 4.5),  center=(sx, sy, 2.25), mat=mat_dark, col=col_mod, bevel=0.4, parent=root)
    make_box(f"{name}_MidBand", (22.6, 12.2, 9.0),  center=(sx, sy, 9.0),  mat=mat_band, col=col_mod, bevel=0.3, parent=root)
    make_box(f"{name}_TopCase", (22.8, 12.4, 6.5),  center=(sx, sy, 16.7), mat=mat_blue, col=col_mod, bevel=0.45, parent=root)

    # 4 köşe vida sütunu kabartması
    for cx_off in (-10.6, 10.6):
        for cy_off in (-5.4, 5.4):
            make_cyl(f"{name}_Bolt_{cx_off:.0f}_{cy_off:.0f}", 1.1, 19.2, center=(sx + cx_off, sy + cy_off, 10.0), mat=mat_blue, col=col_mod, segs=16, parent=root)

    # Yan montaj kulakçıkları (flanş) + vida delikleri
    make_box(f"{name}_Flange", (32.4, 12.4, 2.4), center=(sx, sy, 14.5), mat=mat_blue, col=col_mod, bevel=0.3, parent=root)
    for fx in (-13.8, 13.8):
        make_cyl(f"{name}_FlangeHole_{fx:.0f}", 1.1, 2.8, center=(sx + fx, sy, 14.5), mat=mat_dark, col=col_mod, segs=16, parent=root)

    # Ön etiket plakası + yazı
    make_box(f"{name}_LabelPlate", (14.5, 0.6, 5.2), center=(sx + 2.0, sy - 6.2, 9.5), mat=mat_badge, col=col_mod, bevel=0.15, parent=root)
    make_text_3d(f"{name}_Txt", label_txt, 1.85, (sx + 2.0, sy - 6.55, 9.5), rot_deg=(90, 0, 0), mat=mat_dark, col=col_mod, extrude=0.05, parent=root)

    # İki kademeli üst dişli kubbesi (gerçek MG90S silueti!)
    make_cyl(f"{name}_MainDome", 5.8, 3.6, center=(sx - 5.4, sy, 21.5), mat=mat_blue, col=col_mod, segs=36, parent=root)
    make_cyl(f"{name}_SubDome",  3.2, 2.8, center=(sx + 0.5, sy, 21.1), mat=mat_blue, col=col_mod, segs=28, parent=root)
    make_cyl(f"{name}_Spline",   2.3, 3.8, center=(sx - 5.4, sy, 24.5), mat=mat_brass, col=col_mod, segs=24, parent=root)

    # 2. Dönen Beyaz Servo Kolu (üzerinde 4 adet gerçek bağlantı deliği + merkez pirinç vida!)
    horn_piv = bpy.data.objects.new(f"{name}_HornPivot", None)
    horn_piv.location = (sx - 5.4, sy, 26.2)
    link_obj(horn_piv, col_mod)
    horn_piv.parent = root

    make_cyl(f"{name}_HornHub", 3.8, 2.2, center=(0, 0, 0), mat=mat_horn, col=col_mod, segs=28, parent=horn_piv)
    make_box(f"{name}_HornArm", (16.8, 4.6, 1.9), center=(6.2, 0, 0), mat=mat_horn, col=col_mod, bevel=0.45, parent=horn_piv)
    make_cyl(f"{name}_HornScrew", 1.3, 2.5, center=(0, 0, 0.2), mat=mat_brass, col=col_mod, segs=18, parent=horn_piv)
    for hx in (4.5, 7.5, 10.5, 13.2):
        make_cyl(f"{name}_LinkHole_{hx:.1f}", 0.55, 2.2, center=(hx, 0, 0), mat=mat_dark, col=col_mod, segs=14, parent=horn_piv)

    for fr, deg in horn_keyframes:
        horn_piv.rotation_euler = (0.0, 0.0, math.radians(deg))
        horn_piv.keyframe_insert("rotation_euler", frame=fr)

    # Yukarıdan sahneye iniş animasyonu
    animate_drop_in(root, (0, 0, 0), f_start=f_plug, duration=14, drop_height=34.0)

    return {
        'GND': Vector((sx - 3.6, sy - 6.2, 4.8)),
        'VCC': Vector((sx,       sy - 6.2, 4.8)),
        'SIG': Vector((sx + 3.6, sy - 6.2, 4.8)),
    }


# ==============================================================================
#  BÖLÜM 3: TEK TEK TAKILAN JUMPER KABLOLAR & İNCE NEON SİNYAL AKIŞI
# ==============================================================================
def eval_cubic_bezier(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (u**3) * p0 + 3 * (u**2) * t * p1 + 3 * u * (t**2) * p2 + (t**3) * p3


def make_animated_jumper_wire(name, p_start, p_end, mat_wire, mat_tip, mat_pin, col, f_plug, arc_h=14.0, mid_bias=Vector((0, 0, 0)), radius=0.62):
    """
    Gerçekçi 3D eğri jumper kablosu + iki uçta detaylı DuPont plastik gövde +
    altından çıkan parlak metal pin ucu!
    f_plug karesinde yukarıdan inerek breadboard deliğine tık diye saplanır!
    """
    root = bpy.data.objects.new(f"{name}_Root", None)
    link_obj(root, col)

    p0 = Vector(p_start)
    p3 = Vector(p_end)
    # Kablo uçları DuPont plastik gövdenin üstünden (Z + 6.2mm) başlar
    c0 = p0 + Vector((0, 0, 5.8))
    c3 = p3 + Vector((0, 0, 5.8))
    c1 = c0 + Vector((0, 0, arc_h)) + mid_bias * 0.6
    c2 = c3 + Vector((0, 0, arc_h)) + mid_bias * 0.6

    curve_data = bpy.data.curves.new(name=f"{name}_Curve", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = radius
    curve_data.bevel_resolution = 8
    curve_data.resolution_u = 28

    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(1)
    bp0, bp1 = spline.bezier_points[0], spline.bezier_points[1]
    bp0.co = c0
    bp0.handle_left = c0 - Vector((0, 0, 3.0))
    bp0.handle_right = c1
    bp1.co = c3
    bp1.handle_left = c2
    bp1.handle_right = c3 - Vector((0, 0, 3.0))

    wire_obj = bpy.data.objects.new(name, curve_data)
    set_material(wire_obj, mat_wire)
    link_obj(wire_obj, col)
    wire_obj.parent = root

    # İki uçta detaylı siyah DuPont konnektör + altın kilit penceresi + alt metal erkek pin!
    for idx, pt in enumerate((p0, p3)):
        make_box(f"{name}_DuPont_{idx}", (2.2, 2.2, 6.0), center=(pt.x, pt.y, pt.z + 3.0), mat=mat_tip, col=col, bevel=0.22, parent=root)
        # Yan metal mandal penceresi detayı
        make_box(f"{name}_Latch_{idx}", (0.8, 2.26, 1.8), center=(pt.x, pt.y, pt.z + 2.4), mat=mat_pin, col=col, parent=root)
        # Breadboard deliğine giren metal erkek pin (yukarıdan inerken net görünür!)
        make_box(f"{name}_PinTip_{idx}", (0.62, 0.62, 4.5), center=(pt.x, pt.y, pt.z - 1.8), mat=mat_pin, col=col, parent=root)

    animate_drop_in(root, (0, 0, 0), f_start=f_plug, duration=13, drop_height=30.0)
    return (c0, c1, c2, c3)


def animate_sleek_pulse(name, path_fn, color, f_start, f_end, col, radius=0.92, repeats=3):
    """
    Kablo takıldıktan sonra kablo üzerinden akan ince, zarif neon sinyal darbesi.
    """
    mat_core = make_mat(f"SleekPulse_{name}", color, roughness=0.1, emission=color, emission_strength=28.0)

    mesh = bpy.data.meshes.new(f"Orb_{name}")
    orb = bpy.data.objects.new(f"Orb_{name}", mesh)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=radius)
    bm.to_mesh(mesh)
    bm.free()
    set_material(orb, mat_core)
    link_obj(orb, col)

    orb.scale = (0.001, 0.001, 0.001)
    orb.location = path_fn(0.0)
    orb.keyframe_insert("scale", frame=1)
    orb.keyframe_insert("location", frame=1)

    span = f_end - f_start
    cycle = span / float(repeats)

    for r in range(repeats):
        c0 = int(round(f_start + r * cycle))
        c1 = int(round(f_start + (r + 1) * cycle)) - 2
        orb.scale = (0.001, 0.001, 0.001)
        orb.location = path_fn(0.0)
        orb.keyframe_insert("scale", frame=max(2, c0 - 1))
        orb.keyframe_insert("location", frame=max(2, c0 - 1))

        steps = 12
        for s in range(steps + 1):
            t = s / float(steps)
            fr = int(round(c0 + t * (c1 - c0)))
            orb.location = path_fn(t)
            sc = 1.0 if 0.08 < t < 0.92 else 0.45
            orb.scale = (sc, sc, sc)
            orb.keyframe_insert("location", frame=fr)
            orb.keyframe_insert("scale", frame=fr)

        orb.scale = (0.001, 0.001, 0.001)
        orb.keyframe_insert("scale", frame=c1 + 1)


def build_step_hud_banners(col_stage):
    """
    9:16 dikey ekranın üst kısmında her montaj adımında değişen şık 3D adım başlığı!
    """
    steps = [
        (1,   52,  "1/6 • BREADBOARD GIZLI BAKIR YOLLARI",    (0.22, 0.78, 1.0)),
        (53,  89,  "2/6 • BEYIN: ESP32 DEVKIT V1 TAKILIR",    (0.95, 0.96, 0.98)),
        (90,  149, "3/6 • GUC OTOYOLU: 5V (+) & ORTAK GND (-)", (1.0,  0.28, 0.24)),
        (150, 219, "4/6 • GIRIS: JOYSTICK (3.3V • D34 • D35)", (0.20, 0.95, 0.45)),
        (220, 274, "5/6 • CIKIS 1: SERVO X (5V • GND • D18)",  (1.0,  0.50, 0.10)),
        (275, 360, "6/6 • CIKIS 2: SERVO Y (D19) — TAM SISTEM!", (1.0, 0.88, 0.15)),
    ]

    mat_bg = make_mat("HUD_Plate_Dark", (0.02, 0.03, 0.055), roughness=0.45, coat=0.1)
    hud_root = bpy.data.objects.new("HUD_Root", None)
    hud_root.location = (0.0, 80.0, 26.0)
    hud_root.rotation_euler = (math.radians(32.0), 0.0, 0.0)
    link_obj(hud_root, col_stage)

    make_box("HUD_Banner_Plate", (86.0, 11.5, 1.4), center=(0, 0, 0), mat=mat_bg, col=col_stage, bevel=0.5, parent=hud_root)

    for idx, (f0, f1, title, col_rgb) in enumerate(steps):
        mat_t = make_mat(f"HUD_TxtMat_{idx}", col_rgb, roughness=0.2, emission=col_rgb, emission_strength=4.5)
        tobj = make_text_3d(f"HUD_Step_{idx}", title, 3.1, (0, -0.2, 0.8), mat=mat_t, col=col_stage, extrude=0.12, parent=hud_root)
        tobj.scale = (0.001, 0.001, 0.001)
        tobj.keyframe_insert("scale", frame=1)
        if f0 > 2:
            tobj.keyframe_insert("scale", frame=f0 - 1)
        tobj.scale = (1.0, 1.0, 1.0)
        tobj.keyframe_insert("scale", frame=f0 + 2)
        tobj.keyframe_insert("scale", frame=f1 - 1)
        if f1 < 360:
            tobj.scale = (0.001, 0.001, 0.001)
            tobj.keyframe_insert("scale", frame=f1 + 1)


# ==============================================================================
#  ANA SAHNE KURULUMU
# ==============================================================================
def main():
    clear_scene()
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 360
    scene.render.fps = 30

    col_bb     = get_col("01_Breadboard_Kabuk")
    col_strips = get_col("02_Gizli_Yay_Seritler")
    col_mod    = get_col("03_Moduller_TekTek")
    col_wires  = get_col("04_Kablolar_TekTek")
    col_pulses = get_col("05_Sinyal_Akislari")
    col_stage  = get_col("06_Studyo_Kamera_HUD")

    # 1) Breadboard + İç 5-Parmaklı Fosfor-Bronz Yay Şeritleri
    build_breadboard_and_strips(col_bb, col_strips)

    # 2) Modüller (Sırayla Tek Tek Takılır!)
    # Adım 2 (Kare 55): ESP32 DevKit V1
    build_esp32_detailed(col_mod, f_plug=55)

    # Adım 3 Sonu (Kare 136): 470uF Kondansatör
    build_capacitor_detailed(col_mod, f_plug=136)

    # Adım 4 (Kare 150): KY-023 Joystick
    joy_pins = build_joystick_detailed(col_mod, f_plug=150)

    # Adım 5 (Kare 220): MG90S Servo X (Sol Üst)
    sx_pins = build_servo_detailed(
        "Servo_X", "SERVO X • D18", (-23.5, 51.0), (1.0, 0.44, 0.05),
        [(1, 0), (260, 0), (268, 34), (276, -30), (284, 0), (324, 0), (335, 32), (348, -32), (360, 0)],
        col_mod, f_plug=220,
    )

    # Adım 6 (Kare 275): MG90S Servo Y (Sağ Üst)
    sy_pins = build_servo_detailed(
        "Servo_Y", "SERVO Y • D19", (23.5, 51.0), (1.0, 0.86, 0.06),
        [(1, 0), (322, 0), (334, -32), (346, 34), (355, -20), (360, 0)],
        col_mod, f_plug=275,
    )

    # 3) TEK TEK TAKILAN JUMPER KABLOLAR
    mat_tip    = make_mat("DuPont_Housing",  (0.05, 0.055, 0.065), roughness=0.35, coat=0.2)
    mat_pin    = make_mat("DuPont_MetalPin", (0.90, 0.82, 0.55),   roughness=0.20, metallic=0.80)
    mat_red    = make_mat("Wire_5V_Red",     (0.95, 0.12, 0.10),   roughness=0.26, coat=0.3)
    mat_black  = make_mat("Wire_GND_Black",  (0.11, 0.13, 0.17),   roughness=0.30, coat=0.25)
    mat_purple = make_mat("Wire_3V3_Purple", (0.72, 0.18, 0.98),   roughness=0.26, coat=0.3)
    mat_green  = make_mat("Wire_VRx_Green",  (0.08, 0.90, 0.32),   roughness=0.26, coat=0.3)
    mat_blue   = make_mat("Wire_VRy_Blue",   (0.10, 0.54, 0.98),   roughness=0.26, coat=0.3)
    mat_orange = make_mat("Wire_SX_Orange",  (1.00, 0.42, 0.05),   roughness=0.26, coat=0.3)
    mat_yellow = make_mat("Wire_SY_Yellow",  (1.00, 0.85, 0.05),   roughness=0.26, coat=0.3)

    # --- AŞAMA 3: GÜÇ OTOYOLU KABLOLARI TEK TEK (Kare 90..136) ---
    w_vin    = make_animated_jumper_wire("01_W_ESP_5V",     hole_pt(17, 'a'),       hole_pt(17, 'bot_pos'), mat_red,   mat_tip, mat_pin, col_wires, f_plug=90,  arc_h=7.5)
    w_gnd    = make_animated_jumper_wire("02_W_ESP_GND",    hole_pt(16, 'a'),       hole_pt(16, 'bot_neg'), mat_black, mat_tip, mat_pin, col_wires, f_plug=104, arc_h=7.5)
    w_br_5v  = make_animated_jumper_wire("03_W_Bridge_5V",  hole_pt(27, 'bot_pos'), hole_pt(27, 'top_pos'), mat_red,   mat_tip, mat_pin, col_wires, f_plug=116, arc_h=11.0)
    w_br_gnd = make_animated_jumper_wire("04_W_Bridge_GND", hole_pt(28, 'bot_neg'), hole_pt(28, 'top_neg'), mat_black, mat_tip, mat_pin, col_wires, f_plug=124, arc_h=13.0)

    # --- AŞAMA 4: JOYSTICK KABLOLARI TEK TEK (Kare 164..216) ---
    w_jgnd   = make_animated_jumper_wire("05_W_Joy_GND",    joy_pins['GND'],        hole_pt(8,  'bot_neg'), mat_black,  mat_tip, mat_pin, col_wires, f_plug=164, arc_h=11.0)
    w_3v3_a  = make_animated_jumper_wire("06_W_3V3_Hop",    hole_pt(17, 'j'),       hole_pt(21, 'j'),       mat_purple, mat_tip, mat_pin, col_wires, f_plug=174, arc_h=8.0)
    w_3v3_b  = make_animated_jumper_wire("07_W_Joy_3V3",    hole_pt(21, 'f'),       joy_pins['VCC'],        mat_purple, mat_tip, mat_pin, col_wires, f_plug=180, arc_h=15.0, mid_bias=Vector((10, 0, 0)))
    w_vrx    = make_animated_jumper_wire("08_W_Joy_VRx",    joy_pins['VRx'],        hole_pt(6,  'a'),       mat_green,  mat_tip, mat_pin, col_wires, f_plug=192, arc_h=13.0, mid_bias=Vector((-4, 0, 0)))
    w_vry    = make_animated_jumper_wire("09_W_Joy_VRy",    joy_pins['VRy'],        hole_pt(7,  'a'),       mat_blue,   mat_tip, mat_pin, col_wires, f_plug=204, arc_h=15.0, mid_bias=Vector((4, 0, 0)))

    # --- AŞAMA 5: SERVO X KABLOLARI TEK TEK (Kare 232..268) ---
    w_sx_vcc = make_animated_jumper_wire("10_W_SX_5V",      hole_pt(4,  'top_pos'), sx_pins['VCC'],         mat_red,    mat_tip, mat_pin, col_wires, f_plug=232, arc_h=12.0)
    w_sx_gnd = make_animated_jumper_wire("11_W_SX_GND",     hole_pt(3,  'top_neg'), sx_pins['GND'],         mat_black,  mat_tip, mat_pin, col_wires, f_plug=244, arc_h=10.5)
    w_sx_sig = make_animated_jumper_wire("12_W_SX_SIG",     hole_pt(9,  'j'),       sx_pins['SIG'],         mat_orange, mat_tip, mat_pin, col_wires, f_plug=256, arc_h=16.0, mid_bias=Vector((-5, 0, 0)))

    # --- AŞAMA 6: SERVO Y KABLOLARI TEK TEK (Kare 286..322) ---
    w_sy_vcc = make_animated_jumper_wire("13_W_SY_5V",      hole_pt(20, 'top_pos'), sy_pins['VCC'],         mat_red,    mat_tip, mat_pin, col_wires, f_plug=286, arc_h=12.0)
    w_sy_gnd = make_animated_jumper_wire("14_W_SY_GND",     hole_pt(22, 'top_neg'), sy_pins['GND'],         mat_black,  mat_tip, mat_pin, col_wires, f_plug=298, arc_h=10.5)
    w_sy_sig = make_animated_jumper_wire("15_W_SY_SIG",     hole_pt(8,  'j'),       sy_pins['SIG'],         mat_yellow, mat_tip, mat_pin, col_wires, f_plug=310, arc_h=18.0, mid_bias=Vector((7, 0, 0)))

    # 4) ZARİF NEON SİNYAL DARBELERİ (Kablolar takıldıktan sonra akar!)
    def bez_fn(pts):
        return lambda t: eval_cubic_bezier(pts[0], pts[1], pts[2], pts[3], t)

    animate_sleek_pulse("Pulse_VRx", bez_fn(w_vrx),    (0.10, 1.00, 0.35), 205, 358, col_pulses, radius=0.90, repeats=5)
    animate_sleek_pulse("Pulse_VRy", bez_fn(w_vry),    (0.15, 0.62, 1.00), 216, 358, col_pulses, radius=0.90, repeats=5)
    animate_sleek_pulse("Pulse_SX",  bez_fn(w_sx_sig), (1.00, 0.45, 0.05), 266, 358, col_pulses, radius=0.95, repeats=4)
    animate_sleek_pulse("Pulse_SY",  bez_fn(w_sy_sig), (1.00, 0.88, 0.08), 320, 358, col_pulses, radius=0.95, repeats=2)

    # 5) 3D ADIM BAŞLIKLARI (Üst HUD Banner)
    build_step_hud_banners(col_stage)

    # 6) STÜDYO ZEMİN, 3-NOKTA SOFTBOX IŞIKLANDIRMA & SİNEMATİK KAMERA
    mat_desk = make_mat("Studio_MatteDesk", (0.018, 0.022, 0.032), roughness=0.78, coat=0.0)
    make_box("Studio_Desk", (900.0, 900.0, 2.0), center=(0, 0, -1.2), mat=mat_desk, col=col_stage)

    world = bpy.data.worlds.new("StudioWorld_v2")
    scene.world = world
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.02, 0.026, 0.04, 1.0)
        bg.inputs["Strength"].default_value = 0.38

    def add_sun(name, rot_deg, energy, color=(1, 1, 1), angle=7.0):
        ld = bpy.data.lights.new(name, type='SUN')
        ld.energy = energy
        ld.color = color
        ld.angle = math.radians(angle)
        lo = bpy.data.objects.new(name, ld)
        lo.rotation_euler = tuple(math.radians(a) for a in rot_deg)
        link_obj(lo, col_stage)

    def add_area(name, loc, target, energy, size, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, type='AREA')
        ld.energy = energy
        ld.size = size
        ld.color = color
        lo = bpy.data.objects.new(name, ld)
        lo.location = Vector(loc)
        lo.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        link_obj(lo, col_stage)

    # Dengeli sinematik kontrast: koyu PCB ve parlak neon X-Ray şeritler net ayrışır!
    add_sun("KeySun",   (30, 14, -24), 2.1, (1.0, 0.97, 0.94), angle=8.0)
    add_sun("FillSun",  (45, -18, 135), 0.65, (0.68, 0.84, 1.0), angle=20.0)
    add_area("RimSoftbox",  (0, 170, 155),   (0, 10, 10), energy=260000.0, size=140.0, color=(1.0, 0.84, 0.68))
    add_area("SideSoftbox", (-150, -60, 130), (0, 0, 8),  energy=220000.0, size=120.0, color=(0.75, 0.88, 1.0))

    # 9:16 Dikey Shorts Kamerası (montaj yapılan bölgeye akıcı odaklanır!)
    cam_data = bpy.data.cameras.new("Shorts_9x16_Cam")
    cam_data.lens = 52.0
    cam_data.clip_start = 1.0
    cam_data.clip_end = 5000.0
    cam = bpy.data.objects.new("Shorts_9x16_Cam", cam_data)
    link_obj(cam, col_stage)
    scene.camera = cam

    def set_cam_key(frame, loc, target):
        cam.location = Vector(loc)
        cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        cam.keyframe_insert("location", frame=frame)
        cam.keyframe_insert("rotation_euler", frame=frame)

    # Kamera her adımda takılan parçayı hafifçe takip eder, finalde tüm devreyi gösterir
    set_cam_key(1,   (12,  -118, 205), (0,   6, 6))   # Boş Breadboard & X-Ray
    set_cam_key(55,  (-6,  -112, 196), (-2,  6, 8))   # ESP32 Takılır
    set_cam_key(105, (14,  -115, 198), (6,   2, 6))   # Güç Rayları & Kondansatör
    set_cam_key(180, (-8,  -124, 204), (-2, -6, 6))   # Joystick & 4 Kablosu
    set_cam_key(250, (-12, -120, 206), (-4,  8, 8))   # Servo X & 3 Kablosu
    set_cam_key(305, (12,  -120, 206), (4,   8, 8))   # Servo Y & 3 Kablosu
    set_cam_key(340, (0,   -128, 212), (0,   6, 6))   # Büyük Final: Tüm Devre
    set_cam_key(360, (0,   -128, 212), (0,   6, 6))

    # Önce 2 kontrol karesi (PNG) render al
    scene.render.image_settings.media_type = 'IMAGE'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 720
    scene.render.resolution_y = 1280

    # Kontrol 1: Kare 45 (Boş X-Ray Breadboard — henüz hiçbir parça takılmamış!)
    scene.frame_set(45)
    scene.render.filepath = os.path.join(PREVIEW_DIR, "breadboard_xray_frame_solid.png")
    bpy.ops.render.render(write_still=True)

    # Kontrol 2: Kare 342 (Tüm parçalar tek tek takılmış, X-Ray + zarif sinyal akışı!)
    scene.frame_set(342)
    scene.render.filepath = os.path.join(PREVIEW_DIR, "breadboard_xray_frame_xray.png")
    bpy.ops.render.render(write_still=True)

    # .blend dosyasını 1080x1920 MP4 video çıkışına hazır kaydet
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.image_settings.media_type = 'VIDEO'
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    scene.render.filepath = os.path.join(PREVIEW_DIR, "breadboard_xray_shorts.mp4")
    scene.render.use_file_extension = False
    scene.frame_set(342)

    blend_path = os.path.join(BLENDER_DIR, "breadboard_xray_shorts.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[BLEND v2 OK] {blend_path}")


if __name__ == "__main__":
    main()
