"""
ESP32 From Zero - 2 Eksenli Gimbal Labirent (MG90S / SG90)
Blender 5.2 Parametrik 3D Baskı & Montaj Üretici Scripti

Bu script:
  1. 3D baskıya tam hazır, milimetrik toleranslı 5 parçayı üretir:
       - 01_taban_stand.stl       (Sabit U-Taban, Servo X yuvalı)
       - 02_dis_gimbal_halka.stl  (Dış Gimbal Halkası, Servo Y yuvalı)
       - 03_ic_labirent_tabla.stl (90x90mm 5x5 garantili çözülebilir labirent)
       - 04_pivot_pim_x2.stl      (2 adet sürtünmesiz pivot pimi)
       - 05_yedek_bilye_10mm.stl  (3D basılabilir 10mm yedek top)
  2. Montajlı + hareket animasyonlu önizleme sahnesi ve 3D baskı tablası düzeni
     içeren 'gimbal_maze_3dprint.blend' dosyasını kaydeder.
  3. Önizleme görsellerini (PNG) render alır.

Kullanım:
  blender --background --python generate_gimbal_maze.py
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
STL_DIR     = os.path.join(PROJECT_DIR, "stl")
PREVIEW_DIR = os.path.join(PROJECT_DIR, "previews")

os.makedirs(BLENDER_DIR, exist_ok=True)
os.makedirs(STL_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

# ==============================================================================
#  MİLİMETRİK TASARIM PARAMETRELERİ (1 Blender Birimi = 1.0 mm)
# ==============================================================================
Z_AXIS = 72.0          # Gimbal dönme ekseninin yerden yüksekliği (mm)

# MG90S / SG90 Mikro Servo ölçüleri (+0.3mm 3D baskı toleranslı)
SERVO_CUT_L    = 23.2  # Gövde uzunluğu yuvası (gerçek 22.8mm)
SERVO_CUT_W    = 12.6  # Gövde genişliği yuvası (gerçek 12.2mm)
SERVO_SHAFT_OFF = 5.4  # Gövde merkezi ile mil arasındaki kaçıklık (22.8/2 - 6.0)
SERVO_SCREW_DX = 13.75 # Gövde merkezinden M2 vida deliklerine mesafe (27.5/2)
SERVO_SCREW_R  = 1.0   # M2 vida ön delik yarıçapı (2.0mm çap)

# Servo Horn (beyaz tek kollu plastik kol) gömme yuvası
HORN_SLOT_L    = 16.5  # Kol uzunluğu yuvası
HORN_SLOT_W    = 5.4   # Kol genişliği yuvası
HORN_HUB_R     = 3.9   # Merkez göbek dairesi yarıçapı
HORN_DEPTH     = 2.2   # Gömme derinliği
HORN_SCREW_R   = 1.15  # Merkez sabitleme vidası deliği

# Pivot pim / delik ölçüleri (M3 vida ile de uyumlu)
PIVOT_HOLE_R   = 2.15  # 4.3mm delik çapı (3.85mm pim rahat döner)
PIVOT_PIN_R    = 1.92  # 3.84mm pim gövde çapı

# 1) İç Labirent Tablası
MAZE_SIZE      = 90.0  # 90x90 mm kare tabla
MAZE_FLOOR_H   = 4.0   # Taban kalınlığı (hedef çukuru için yeterli et)
MAZE_WALL_H    = 11.5  # Duvar yüksekliği (toplam 15.5mm)
MAZE_OUTER_T   = 3.0   # Dış kenar duvar kalınlığı (iç boşluk 84x84 mm)
MAZE_INNER_T   = 2.6   # İç labirent duvar kalınlığı (koridor: ~14.2mm -> 8-10mm bilye)
MAZE_TOTAL_H   = MAZE_FLOOR_H + MAZE_WALL_H  # 15.5 mm

# 2) Dış Gimbal Halkası
RING_INNER_X   = 100.0 # X iç boşluğu (labirentin her iki yanında 5mm pay)
RING_INNER_Y   = 98.0  # Y iç boşluğu (servo mili tam horn yuvasına oturur)
RING_WALL_T    = 8.0   # Halka duvar kalınlığı (MG90S üst gövdesini tam saklar)
RING_OUTER_X   = RING_INNER_X + 2 * RING_WALL_T  # 116.0 mm
RING_OUTER_Y   = RING_INNER_Y + 2 * RING_WALL_T  # 114.0 mm
RING_H         = 18.0  # Halka yüksekliği (12.6mm servo yuvasına üst/alt 2.7mm et)

# 3) Sabit U-Taban (Stand)
STAND_INNER_X  = 124.0 # Dış halkanın (116mm) her yanında 4mm pay
STAND_WALL_T   = 8.0   # Kule duvar kalınlığı
STAND_OUTER_X  = STAND_INNER_X + 2 * STAND_WALL_T  # 140.0 mm
STAND_TOWER_Y  = 26.0  # Kule derinliği (Y yönünde)
STAND_TOWER_H  = 88.0  # Kule yüksekliği (Z=0..88, mil Z=72'de)
STAND_BASE_Y   = 86.0  # Taban plakası derinliği
STAND_BASE_H   = 6.5   # Taban plakası kalınlığı


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


def get_or_create_collection(name, parent=None):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    if parent is None:
        bpy.context.scene.collection.children.link(col)
    else:
        parent.children.link(col)
    return col


def link_to_collection(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def set_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.material_index = 0


def make_material(name, color, roughness=0.38, metallic=0.0, coat=0.15):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Coat Weight" in bsdf.inputs:
            bsdf.inputs["Coat Weight"].default_value = coat
    return mat


def create_box(name, size, center=(0, 0, 0), bevel=0.0, bevel_segments=2):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if bevel > 0.0:
        bmesh.ops.bevel(
            bm,
            geom=list(bm.edges),
            offset=bevel,
            segments=bevel_segments,
            affect='EDGES',
            clamp_overlap=True,
        )
    bmesh.ops.translate(bm, vec=Vector(center), verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj


def create_cylinder(name, radius, depth, center=(0, 0, 0), axis='Z', segments=48):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=segments,
        radius1=radius,
        radius2=radius,
        depth=depth,
    )
    if axis == 'X':
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'Y'), verts=bm.verts)
    elif axis == 'Y':
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, 'X'), verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(center), verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return obj


def apply_boolean(target, cutter, operation='DIFFERENCE', delete_cutter=True):
    mod = target.modifiers.new(name="Bool", type='BOOLEAN')
    mod.operation = operation
    mod.solver = 'EXACT'
    mod.object = cutter

    bpy.context.view_layer.objects.active = target
    bpy.ops.object.select_all(action='DESELECT')
    target.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)

    if delete_cutter:
        bpy.data.objects.remove(cutter, do_unlink=True)


def fix_normals(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


def add_servo_horn_pocket(target, face_pos, axis='Y', sign=1):
    """
    MG90S/SG90 tek kollu beyaz servo horn için gömme yuva ve merkez vida deliği açar.
    axis='Y', sign=+1 -> +Y yüzeyine (Y=face_pos) dıştan içeri (-Y yönünde) oyar.
    axis='X', sign=+1 -> +X yüzeyine (X=face_pos) dıştan içeri (-X yönünde) oyar.
    """
    overshoot = 1.5
    depth = HORN_DEPTH + overshoot
    if axis == 'Y':
        cy = face_pos - sign * (HORN_DEPTH / 2.0) + sign * (overshoot / 2.0)
        # Yatay kol kanalı (X ekseni boyunca uzanır)
        slot = create_box("HornSlot", (HORN_SLOT_L, depth, HORN_SLOT_W),
                          center=(HORN_SLOT_L * 0.25, cy, 0.0))
        hub  = create_cylinder("HornHub", HORN_HUB_R, depth,
                               center=(0.0, cy, 0.0), axis='Y', segments=36)
        hole = create_cylinder("HornScrew", HORN_SCREW_R, 14.0,
                               center=(0.0, face_pos - sign * 4.0, 0.0), axis='Y', segments=24)
    else:  # axis == 'X'
        cx = face_pos - sign * (HORN_DEPTH / 2.0) + sign * (overshoot / 2.0)
        # Yatay kol kanalı (Y ekseni boyunca uzanır)
        slot = create_box("HornSlot", (depth, HORN_SLOT_L, HORN_SLOT_W),
                          center=(cx, HORN_SLOT_L * 0.25, 0.0))
        hub  = create_cylinder("HornHub", HORN_HUB_R, depth,
                               center=(cx, 0.0, 0.0), axis='X', segments=36)
        hole = create_cylinder("HornScrew", HORN_SCREW_R, 14.0,
                               center=(face_pos - sign * 4.0, 0.0, 0.0), axis='X', segments=24)

    apply_boolean(target, slot, 'DIFFERENCE')
    apply_boolean(target, hub, 'DIFFERENCE')
    apply_boolean(target, hole, 'DIFFERENCE')


# ==============================================================================
#  PARÇA 1: İÇ LABİRENT TABLASI (03_ic_labirent_tabla)
#  Yerel eksen: Merkez (0,0,0) = Gimbal ekseni! (Z=-7.75..+7.75)
# ==============================================================================
def build_inner_maze():
    half = MAZE_SIZE / 2.0           # 45.0 mm
    z_bot = -MAZE_TOTAL_H / 2.0      # -7.75 mm
    z_floor_top = z_bot + MAZE_FLOOR_H  # -3.75 mm
    z_top = z_bot + MAZE_TOTAL_H     # +7.75 mm

    # 1. Taban plakası
    maze = create_box(
        "03_ic_labirent_tabla",
        (MAZE_SIZE, MAZE_SIZE, MAZE_FLOOR_H),
        center=(0.0, 0.0, z_bot + MAZE_FLOOR_H / 2.0),
    )

    # 2. Dış çevre duvarları (4 kenar)
    wall_z = z_floor_top + MAZE_WALL_H / 2.0
    # +Y ve -Y kenarları (servo & pivot bağlantısı olduğu için 4.2mm güçlendirilmiş)
    y_edge_t = 4.2
    x_edge_t = MAZE_OUTER_T
    w_pos_y = create_box("W_PY", (MAZE_SIZE, y_edge_t, MAZE_WALL_H + 0.4),
                         center=(0.0, half - y_edge_t / 2.0, wall_z - 0.2))
    w_neg_y = create_box("W_NY", (MAZE_SIZE, y_edge_t, MAZE_WALL_H + 0.4),
                         center=(0.0, -half + y_edge_t / 2.0, wall_z - 0.2))
    w_pos_x = create_box("W_PX", (x_edge_t, MAZE_SIZE - 2 * y_edge_t + 0.4, MAZE_WALL_H + 0.4),
                         center=(half - x_edge_t / 2.0, 0.0, wall_z - 0.2))
    w_neg_x = create_box("W_NX", (x_edge_t, MAZE_SIZE - 2 * y_edge_t + 0.4, MAZE_WALL_H + 0.4),
                         center=(-half + x_edge_t / 2.0, 0.0, wall_z - 0.2))

    for w in (w_pos_y, w_neg_y, w_pos_x, w_neg_x):
        apply_boolean(maze, w, 'UNION')

    # 3. 5x5 Garantili Çözülebilir Labirent İç Duvarları
    # Oynanabilir iç alan: X ∈ [-42, +42] (84mm), Y ∈ [-40.8, +40.8] (81.6mm)
    play_x = MAZE_SIZE - 2 * x_edge_t   # 84.0 mm
    play_y = MAZE_SIZE - 2 * y_edge_t   # 81.6 mm
    cell_x = play_x / 5.0               # 16.80 mm
    cell_y = play_y / 5.0               # 16.32 mm
    x0 = -play_x / 2.0
    y0 = -play_y / 2.0

    # Açık geçişler (25 hücreli yayılan ağaç — (0,0) Başlangıç -> (4,4) Hedef)
    open_passages = {
        # Ana çözüm yolu (hem X hem Y eğimi gerektirir)
        ((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (2, 1)),
        ((2, 1), (1, 1)), ((1, 1), (1, 2)), ((1, 2), (0, 2)),
        ((0, 2), (0, 3)), ((0, 3), (0, 4)), ((0, 4), (1, 4)),
        ((1, 4), (2, 4)), ((2, 4), (2, 3)), ((2, 3), (3, 3)),
        ((3, 3), (3, 2)), ((3, 2), (4, 2)), ((4, 2), (4, 3)),
        ((4, 3), (4, 4)),
        # Eğlenceli çıkmaz sokaklar (tuzak dallar)
        ((0, 0), (0, 1)),
        ((2, 0), (3, 0)), ((3, 0), (4, 0)), ((4, 0), (4, 1)), ((4, 1), (3, 1)),
        ((1, 2), (2, 2)),
        ((0, 3), (1, 3)),
        ((2, 4), (3, 4)),
    }

    def is_open(a, b):
        return (a, b) in open_passages or (b, a) in open_passages

    inner_wall_h = MAZE_WALL_H - 0.5  # Dış çerçeveden 0.5mm alçak (estetik kontrast)
    iw_z = z_floor_top + inner_wall_h / 2.0 - 0.2

    # Dikey iç duvarlar (col ile col+1 arası)
    for col in range(4):
        for row in range(5):
            if not is_open((col, row), (col + 1, row)):
                wx = x0 + (col + 1) * cell_x
                wy = y0 + (row + 0.5) * cell_y
                seg = create_box(
                    f"VW_{col}_{row}",
                    (MAZE_INNER_T, cell_y + MAZE_INNER_T, inner_wall_h + 0.4),
                    center=(wx, wy, iw_z),
                )
                apply_boolean(maze, seg, 'UNION')

    # Yatay iç duvarlar (row ile row+1 arası)
    for col in range(5):
        for row in range(4):
            if not is_open((col, row), (col, row + 1)):
                wx = x0 + (col + 0.5) * cell_x
                wy = y0 + (row + 1) * cell_y
                seg = create_box(
                    f"HW_{col}_{row}",
                    (cell_x + MAZE_INNER_T, MAZE_INNER_T, inner_wall_h + 0.4),
                    center=(wx, wy, iw_z),
                )
                apply_boolean(maze, seg, 'UNION')

    # 4. Hedef Çukuru (4,4 hücresi — sağ üst köşe): 11.6mm çap, 2.8mm derinlik
    goal_x = x0 + 4.5 * cell_x
    goal_y = y0 + 4.5 * cell_y
    goal_cup = create_cylinder(
        "GoalCup",
        radius=5.8,
        depth=4.0,
        center=(goal_x, goal_y, z_floor_top - 2.8 + 2.0),
        axis='Z',
        segments=40,
    )
    apply_boolean(maze, goal_cup, 'DIFFERENCE')

    # Başlangıç işaret halkası (0,0 hücresi — sol alt köşe): 0.8mm sığ çukur
    start_x = x0 + 0.5 * cell_x
    start_y = y0 + 0.5 * cell_y
    start_dimple = create_cylinder(
        "StartDimple",
        radius=4.5,
        depth=2.0,
        center=(start_x, start_y, z_floor_top - 0.8 + 1.0),
        axis='Z',
        segments=32,
    )
    apply_boolean(maze, start_dimple, 'DIFFERENCE')

    # 5. +Y Kenarında Servo Y Horn Yuvası (Z=0 hizasında)
    add_servo_horn_pocket(maze, face_pos=half, axis='Y', sign=1)

    # 6. -Y Kenarında Pivot Pim Deliği (4.3mm çap, 7mm derinlik)
    pivot_hole = create_cylinder(
        "MazePivotHole",
        radius=PIVOT_HOLE_R,
        depth=9.0,
        center=(0.0, -half + 3.0, 0.0),
        axis='Y',
        segments=32,
    )
    apply_boolean(maze, pivot_hole, 'DIFFERENCE')

    fix_normals(maze)
    return maze, (start_x, start_y, z_floor_top)


# ==============================================================================
#  PARÇA 2: DIŞ GİMBAL HALKASI (02_dis_gimbal_halka)
#  Yerel eksen: Merkez (0,0,0) = Gimbal ekseni! (Z=-9.0..+9.0)
# ==============================================================================
def build_outer_ring():
    # Dış bloktan iç boşluğu çıkararak tam su geçirmez çerçeve oluştur
    ring = create_box(
        "02_dis_gimbal_halka",
        (RING_OUTER_X, RING_OUTER_Y, RING_H),
        center=(0.0, 0.0, 0.0),
        bevel=1.2,
        bevel_segments=2,
    )
    inner_cut = create_box(
        "RingInnerCut",
        (RING_INNER_X, RING_INNER_Y, RING_H + 6.0),
        center=(0.0, 0.0, 0.0),
        bevel=1.5,
        bevel_segments=2,
    )
    apply_boolean(ring, inner_cut, 'DIFFERENCE')

    # +Y duvarında Servo Y (MG90S/SG90) yatay montaj yuvası
    # Mil tam X=0'da olsun diye gövde merkezi X = +SERVO_SHAFT_OFF (+5.4mm) kaydırılır
    y_wall_center = (RING_INNER_Y + RING_OUTER_Y) / 4.0  # (98+114)/4 = 53.0 mm
    servo_cut = create_box(
        "ServoY_Cutout",
        (SERVO_CUT_L, RING_WALL_T + 4.0, SERVO_CUT_W),
        center=(SERVO_SHAFT_OFF, y_wall_center, 0.0),
    )
    apply_boolean(ring, servo_cut, 'DIFFERENCE')

    # Servo Y M2 vida delikleri
    for sgn in (-1, 1):
        sh = create_cylinder(
            f"ServoY_Screw_{sgn}",
            radius=SERVO_SCREW_R,
            depth=RING_WALL_T + 4.0,
            center=(SERVO_SHAFT_OFF + sgn * SERVO_SCREW_DX, y_wall_center, 0.0),
            axis='Y',
            segments=24,
        )
        apply_boolean(ring, sh, 'DIFFERENCE')

    # -Y duvarında İç Labirent pivot deliği (dıştan içe boydan boya)
    piv_y = create_cylinder(
        "RingPivotY",
        radius=PIVOT_HOLE_R,
        depth=RING_WALL_T + 4.0,
        center=(0.0, -y_wall_center, 0.0),
        axis='Y',
        segments=32,
    )
    apply_boolean(ring, piv_y, 'DIFFERENCE')

    # +X dış yüzeyinde Servo X Horn Yuvası
    add_servo_horn_pocket(ring, face_pos=RING_OUTER_X / 2.0, axis='X', sign=1)

    # -X duvarında Dış Halka pivot deliği (Taban Sol Kule ile birleşir)
    x_wall_center = (RING_INNER_X + RING_OUTER_X) / 4.0  # 54.0 mm
    piv_x = create_cylinder(
        "RingPivotX",
        radius=PIVOT_HOLE_R,
        depth=RING_WALL_T + 4.0,
        center=(-x_wall_center, 0.0, 0.0),
        axis='X',
        segments=32,
    )
    apply_boolean(ring, piv_x, 'DIFFERENCE')

    fix_normals(ring)
    return ring


# ==============================================================================
#  PARÇA 3: SABİT U-TABAN / STAND (01_taban_stand)
#  Yerel eksen: Taban alt yüzü Z = 0, Gimbal ekseni Z = Z_AXIS (72mm)
# ==============================================================================
def build_base_stand():
    half_outer_x = STAND_OUTER_X / 2.0  # 70.0 mm
    half_inner_x = STAND_INNER_X / 2.0  # 62.0 mm
    tower_cx = (half_inner_x + half_outer_x) / 2.0  # 66.0 mm

    # 1. Ana taban plakası
    stand = create_box(
        "01_taban_stand",
        (STAND_OUTER_X, STAND_BASE_Y, STAND_BASE_H),
        center=(0.0, 0.0, STAND_BASE_H / 2.0),
        bevel=1.5,
        bevel_segments=2,
    )

    # Taban ortasında şık hafifletme/kablo kanalı girintisi
    recess = create_box(
        "BaseRecess",
        (82.0, 48.0, 3.0),
        center=(0.0, 0.0, STAND_BASE_H + 0.5),
        bevel=2.0,
        bevel_segments=2,
    )
    apply_boolean(stand, recess, 'DIFFERENCE')

    # 2. Sağ (+X) ve Sol (-X) Kuleler
    tower_h = STAND_TOWER_H - STAND_BASE_H + 1.0
    tower_cz = STAND_BASE_H - 1.0 + tower_h / 2.0

    for side, sgn in (("Right", 1), ("Left", -1)):
        tower = create_box(
            f"Tower_{side}",
            (STAND_WALL_T, STAND_TOWER_Y, tower_h),
            center=(sgn * tower_cx, 0.0, tower_cz),
            bevel=1.0,
            bevel_segments=2,
        )
        apply_boolean(stand, tower, 'UNION')

        # Ön ve arka destek üçgen/kademeli payandalar (kuleyi taş gibi sağlamlaştırır)
        for y_sgn in (-1, 1):
            buttress = create_box(
                f"Buttress_{side}_{y_sgn}",
                (STAND_WALL_T, 18.0, 26.0),
                center=(sgn * tower_cx, y_sgn * (STAND_TOWER_Y / 2.0 + 7.5), STAND_BASE_H + 12.0),
            )
            # Üst köşeyi 45° eğimli kes (baskıda desteksiz çıkar ve endüstriyel görünür)
            slash = create_box(
                "Slash",
                (STAND_WALL_T + 4.0, 32.0, 32.0),
                center=(sgn * tower_cx, y_sgn * (STAND_TOWER_Y / 2.0 + 18.0), STAND_BASE_H + 26.0),
            )
            slash.rotation_euler = (y_sgn * math.radians(45), 0.0, 0.0)
            bpy.context.view_layer.update()
            apply_boolean(buttress, slash, 'DIFFERENCE')
            apply_boolean(stand, buttress, 'UNION')

    # 3. Sağ Kulede (+X) Servo X DİKEY montaj yuvası (Mil Z = Z_AXIS = 72mm)
    # Servo dikey yerleştiğinde mil üstte: gövde merkezi Z = Z_AXIS - SERVO_SHAFT_OFF
    servo_z_center = Z_AXIS - SERVO_SHAFT_OFF  # 66.6 mm
    servo_x_cut = create_box(
        "ServoX_Cutout",
        (STAND_WALL_T + 4.0, SERVO_CUT_W, SERVO_CUT_L),
        center=(tower_cx, 0.0, servo_z_center),
    )
    apply_boolean(stand, servo_x_cut, 'DIFFERENCE')

    # Servo X M2 vida delikleri (üst ve alt)
    for sgn in (-1, 1):
        sh = create_cylinder(
            f"ServoX_Screw_{sgn}",
            radius=SERVO_SCREW_R,
            depth=STAND_WALL_T + 4.0,
            center=(tower_cx, 0.0, servo_z_center + sgn * SERVO_SCREW_DX),
            axis='X',
            segments=24,
        )
        apply_boolean(stand, sh, 'DIFFERENCE')

    # 4. Sol Kulede (-X) Pivot Pim Deliği (Z = Z_AXIS = 72mm)
    left_piv = create_cylinder(
        "StandLeftPivot",
        radius=PIVOT_HOLE_R,
        depth=STAND_WALL_T + 4.0,
        center=(-tower_cx, 0.0, Z_AXIS),
        axis='X',
        segments=32,
    )
    apply_boolean(stand, left_piv, 'DIFFERENCE')

    # 5. Sağ kule alt kısmında kablo geçiş çentiği (servo kablosu arkadan temiz çıkar)
    cable_notch = create_box(
        "CableNotch",
        (STAND_WALL_T + 4.0, 7.0, 9.0),
        center=(tower_cx, 0.0, STAND_BASE_H + 4.5),
    )
    apply_boolean(stand, cable_notch, 'DIFFERENCE')

    fix_normals(stand)
    return stand


# ==============================================================================
#  PARÇA 4: PİVOT PİMLERİ (x2) VE YEDEK 10mm TOP
# ==============================================================================
def build_pivot_pin(name="PivotPin", length=18.0):
    # Baş kısmı Z=0..2.6, gövde Z=2.6..2.6+length (dikey baskıya hazır)
    head = create_cylinder(name, radius=4.2, depth=2.6, center=(0.0, 0.0, 1.3), axis='Z', segments=32)
    shaft = create_cylinder("PinShaft", radius=PIVOT_PIN_R, depth=length + 0.5,
                            center=(0.0, 0.0, 2.4 + length / 2.0), axis='Z', segments=32)
    apply_boolean(head, shaft, 'UNION')
    fix_normals(head)
    return head


def build_backup_ball(name="05_yedek_bilye_10mm", diameter=10.0):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    r = diameter / 2.0
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=32, radius=r)
    bmesh.ops.translate(bm, vec=Vector((0.0, 0.0, r - 0.35)), verts=bm.verts)
    bm.to_mesh(mesh)
    bm.free()

    # Tabana yapışması için altını 0.35mm düzle (desteksiz baskı!)
    flat_cut = create_box("BallFlatCut", (20.0, 20.0, 10.0), center=(0.0, 0.0, -5.0))
    apply_boolean(obj, flat_cut, 'DIFFERENCE')
    fix_normals(obj)
    return obj


# ==============================================================================
#  GÖRSEL REFERANS: GERÇEKÇİ MG90S SERVO MODELİ (Baskıya dahil değil!)
# ==============================================================================
def build_mg90s_visual(name, mat_body, mat_metal, mat_horn):
    """
    Yerel eksende (0,0,0) = Çıkış milinin tabanı (flanştan 6.5mm yukarıda).
    Mil +Z yönüne bakar; gövde -Z yönünde uzanır.
    """
    parent = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(parent)

    # Gövde: 22.8 x 12.2 x 22.5 mm, mil +X ucundan 6mm içeride -> gövde merkezi X = +5.4
    body = create_box(f"{name}_Body", (22.6, 12.0, 22.2),
                      center=(SERVO_SHAFT_OFF, 0.0, -11.1), bevel=0.5)
    flange = create_box(f"{name}_Flange", (32.2, 12.0, 2.4),
                        center=(SERVO_SHAFT_OFF, 0.0, -6.5), bevel=0.3)
    gear_cap = create_cylinder(f"{name}_Cap", radius=5.8, depth=4.0,
                               center=(0.0, 0.0, -2.0), axis='Z', segments=28)
    shaft = create_cylinder(f"{name}_Shaft", radius=2.4, depth=4.2,
                            center=(0.0, 0.0, 2.0), axis='Z', segments=24)
    horn_hub = create_cylinder(f"{name}_HornHub", radius=3.5, depth=2.0,
                               center=(0.0, 0.0, 3.8), axis='Z', segments=24)
    horn_arm = create_box(f"{name}_HornArm", (15.0, 4.6, 1.8),
                          center=(4.0, 0.0, 3.8), bevel=0.3)

    for p in (body, flange, gear_cap):
        p.data.materials.append(mat_body)
        p.parent = parent
    shaft.data.materials.append(mat_metal)
    shaft.parent = parent
    for p in (horn_hub, horn_arm):
        p.data.materials.append(mat_horn)
        p.parent = parent

    return parent


# ==============================================================================
#  STL DIŞA AKTARIM & BOYUT DOĞRULAMA
# ==============================================================================
def export_single_stl(obj, filepath, align_z_zero=True):
    # Geçici kopya al, merkeze ve Z=0'a oturt, STL yaz, kopyayı sil
    tmp = obj.copy()
    tmp.data = obj.data.copy()
    bpy.context.scene.collection.objects.link(tmp)
    tmp.parent = None
    tmp.matrix_world = Matrix.Identity(4)

    # Bounding box'a göre XY merkeze, alt yüz Z=0'a taşı
    bpy.context.view_layer.update()
    bbox = [tmp.matrix_world @ Vector(c) for c in tmp.bound_box]
    min_x = min(v.x for v in bbox)
    max_x = max(v.x for v in bbox)
    min_y = min(v.y for v in bbox)
    max_y = max(v.y for v in bbox)
    min_z = min(v.z for v in bbox)
    max_z = max(v.z for v in bbox)

    shift = Vector((-(min_x + max_x) / 2.0, -(min_y + max_y) / 2.0, -min_z if align_z_zero else 0.0))
    bm = bmesh.new()
    bm.from_mesh(tmp.data)
    bmesh.ops.translate(bm, vec=shift, verts=bm.verts)
    bm.to_mesh(tmp.data)
    bm.free()
    tmp.data.update()

    bpy.ops.object.select_all(action='DESELECT')
    tmp.select_set(True)
    bpy.context.view_layer.objects.active = tmp

    bpy.ops.wm.stl_export(
        filepath=filepath,
        export_selected_objects=True,
        global_scale=1.0,
        use_scene_unit=False,
        apply_modifiers=True,
    )

    dims = (max_x - min_x, max_y - min_y, max_z - min_z)
    print(f"[STL OK] {os.path.basename(filepath):28s} -> {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm")

    bpy.data.objects.remove(tmp, do_unlink=True)


# ==============================================================================
#  ANA SAHNE KURULUMU
# ==============================================================================
def main():
    clear_scene()

    col_asm   = get_or_create_collection("01_Montaj_Onizleme")
    col_plate = get_or_create_collection("02_3D_Baski_Tablasi")
    col_stage = get_or_create_collection("03_Stüdyo_Isik_Kamera")

    # Malzemeler (modern endüstriyel renk paleti)
    mat_stand  = make_material("PLA_Antrasit", (0.09, 0.10, 0.12), roughness=0.35)
    mat_ring   = make_material("PLA_Turuncu",  (0.95, 0.36, 0.06), roughness=0.32)
    mat_maze   = make_material("PLA_KremBeyaz",(0.90, 0.89, 0.86), roughness=0.35)
    mat_pin    = make_material("PLA_Sari",     (0.95, 0.72, 0.05), roughness=0.35)
    mat_servo  = make_material("MG90S_Koyu",   (0.05, 0.16, 0.34), roughness=0.28)
    mat_metal  = make_material("Celik_Bilye",  (0.85, 0.88, 0.92), roughness=0.08, metallic=1.0, coat=0.4)
    mat_horn   = make_material("Servo_Horn",   (0.96, 0.96, 0.96), roughness=0.40)

    # ---------------- 1) 3D BASKI PARÇALARINI ÜRET ----------------
    print("Parcalar uretiliyor...")
    stand = build_base_stand()
    ring  = build_outer_ring()
    maze, start_pos = build_inner_maze()
    pin1  = build_pivot_pin("PivotPin_X", length=18.0)
    pin2  = build_pivot_pin("PivotPin_Y", length=18.0)
    ball_print = build_backup_ball("05_yedek_bilye_10mm", diameter=10.0)

    set_material(stand, mat_stand)
    set_material(ring, mat_ring)
    set_material(maze, mat_maze)
    set_material(pin1, mat_pin)
    set_material(pin2, mat_pin)
    set_material(ball_print, mat_pin)

    # ---------------- 2) STL DOSYALARINI DIŞA AKTAR ----------------
    export_single_stl(stand, os.path.join(STL_DIR, "01_taban_stand.stl"))
    export_single_stl(ring,  os.path.join(STL_DIR, "02_dis_gimbal_halka.stl"))
    export_single_stl(maze,  os.path.join(STL_DIR, "03_ic_labirent_tabla.stl"))

    # 2 pivot pimini tek STL'de yan yana birleştir
    pin_pair = pin1.copy()
    pin_pair.data = pin1.data.copy()
    bpy.context.scene.collection.objects.link(pin_pair)
    pin_b = pin2.copy()
    pin_b.data = pin2.data.copy()
    bpy.context.scene.collection.objects.link(pin_b)
    bm = bmesh.new()
    bm.from_mesh(pin_b.data)
    bmesh.ops.translate(bm, vec=Vector((14.0, 0.0, 0.0)), verts=bm.verts)
    bm.to_mesh(pin_b.data)
    bm.free()
    apply_boolean(pin_pair, pin_b, 'UNION')
    export_single_stl(pin_pair, os.path.join(STL_DIR, "04_pivot_pim_x2.stl"))
    bpy.data.objects.remove(pin_pair, do_unlink=True)

    export_single_stl(ball_print, os.path.join(STL_DIR, "05_yedek_bilye_10mm.stl"))

    # ---------------- 3) 3D BASKI TABLASI KOLEKSİYONU (Z=0'DA DÜZ) ----------------
    def add_to_plate(src, name, loc_xy):
        cp = src.copy()
        cp.data = src.data.copy()
        cp.name = name
        link_to_collection(cp, col_plate)
        bpy.context.view_layer.update()
        bbox = [Vector(c) for c in cp.bound_box]
        min_z = min(v.z for v in bbox)
        cp.location = (loc_xy[0], loc_xy[1], -min_z)
        return cp

    # 256x256 baskı tablasını 300mm sağa yerleştir (montajla çakışmasın)
    PLATE_X = 310.0
    bed = create_box("Baski_Tablasi_256x256_Ref", (256.0, 256.0, 2.0), center=(PLATE_X, 0.0, -1.0))
    bed.data.materials.append(make_material("Bed_Grid", (0.12, 0.13, 0.15), roughness=0.65))
    link_to_collection(bed, col_plate)

    # Her parça arasında en az 14mm temiz boşluk bırak (140x86, 116x114, 90x90)
    add_to_plate(stand,      "PLATE_01_Taban",       (PLATE_X - 42.0, -68.0))
    add_to_plate(ring,       "PLATE_02_Dis_Halka",   (PLATE_X - 54.0,  52.0))
    add_to_plate(maze,       "PLATE_03_Ic_Labirent", (PLATE_X + 66.0,  52.0))
    add_to_plate(pin1,       "PLATE_04_Pim_1",       (PLATE_X + 58.0, -45.0))
    add_to_plate(pin2,       "PLATE_04_Pim_2",       (PLATE_X + 78.0, -45.0))
    add_to_plate(ball_print, "PLATE_05_Yedek_Bilye", (PLATE_X + 68.0, -76.0))

    # Yedek baskı topunu montajdan kaldır (montajda parlak çelik bilye olacak)
    bpy.data.objects.remove(ball_print, do_unlink=True)

    # ---------------- 4) MONTAJLI & HAREKETLİ GİMBAL HİYERARŞİSİ ----------------
    link_to_collection(stand, col_asm)
    link_to_collection(ring, col_asm)
    link_to_collection(maze, col_asm)
    link_to_collection(pin1, col_asm)
    link_to_collection(pin2, col_asm)

    # Dış Halka -> (0, 0, Z_AXIS) konumunda, X ekseninde eğilir
    ring.location = (0.0, 0.0, Z_AXIS)
    # İç Labirent -> Dış Halkanın çocuğu, Y ekseninde eğilir
    maze.parent = ring
    maze.location = (0.0, 0.0, 0.0)

    # Pivot pimlerini yerlerine tak
    # X ekseni pimi (Sol kule dışından X=-70 -> içeri +X yönüne)
    pin1.location = (-72.0, 0.0, Z_AXIS)
    pin1.rotation_euler = (0.0, math.pi / 2.0, 0.0)

    # Y ekseni pimi (Dış halka -Y dışından içeri +Y yönüne, ring'e bağlı)
    pin2.parent = ring
    pin2.location = (0.0, -59.0, 0.0)
    pin2.rotation_euler = (-math.pi / 2.0, 0.0, 0.0)

    # Referans MG90S Servo X (Sağ Kule dışına monteli: mil -X'e, gövde -Z'ye bakar)
    servo_x = build_mg90s_visual("Ref_MG90S_Servo_X", mat_servo, mat_metal, mat_horn)
    servo_x.location = (63.5, 0.0, Z_AXIS)
    rot_sx = Matrix.Rotation(-math.pi / 2.0, 3, 'Y') @ Matrix.Rotation(math.pi, 3, 'Z')
    servo_x.rotation_euler = rot_sx.to_euler()
    for o in [servo_x] + list(servo_x.children):
        link_to_collection(o, col_asm)

    # Referans MG90S Servo Y (Dış Halka +Y dışına monteli, mil -Y'ye bakar, ring ile döner!)
    servo_y = build_mg90s_visual("Ref_MG90S_Servo_Y", mat_servo, mat_metal, mat_horn)
    servo_y.parent = ring
    servo_y.location = (0.0, 50.5, 0.0)
    servo_y.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
    for o in [servo_y] + list(servo_y.children):
        link_to_collection(o, col_asm)

    # Parlak 9.5mm çelik bilye (labirentin içinde başlangıç noktasının biraz ilerisinde)
    ball_mesh = bpy.data.meshes.new("Celik_Bilye_Ref")
    ball = bpy.data.objects.new("Celik_Bilye_Ref", ball_mesh)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=32, radius=4.75)
    bm.to_mesh(ball_mesh)
    bm.free()
    ball.data.materials.append(mat_metal)
    ball.parent = maze
    ball.location = (start_pos[0] + 16.8, start_pos[1], start_pos[2] + 4.75)
    link_to_collection(ball, col_asm)

    # Kısa demo gimbal animasyonu (Spacebar'a basınca eğim testi görünür!)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 120
    scene.render.fps = 30

    keyframes_x = [(1, 0), (25, 14), (55, -14), (85, 10), (120, 0)]
    keyframes_y = [(1, 0), (35, -16), (70, 16), (95, -10), (120, 0)]
    for f, deg in keyframes_x:
        ring.rotation_euler = (math.radians(deg), 0.0, 0.0)
        ring.keyframe_insert(data_path="rotation_euler", frame=f)
    for f, deg in keyframes_y:
        maze.rotation_euler = (0.0, math.radians(deg), 0.0)
        maze.keyframe_insert(data_path="rotation_euler", frame=f)

    # Kare 24'te estetik hafif eğimli pozda dursun (render için harika açı!)
    scene.frame_set(24)

    # ---------------- 5) STÜDYO IŞIK & KAMERA + RENDER ÖNİZLEMELERİ ----------------
    # Zemin
    floor = create_box("Studio_Floor", (2000.0, 2000.0, 2.0), center=(150.0, 0.0, -2.5))
    floor.data.materials.append(make_material("Studio_BG", (0.07, 0.08, 0.10), roughness=0.55))
    link_to_collection(floor, col_stage)

    # Arka plan (koyu mühendislik stüdyosu + dolgu aydınlatma)
    world = bpy.data.worlds.new("StudioWorld")
    scene.world = world
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.09, 0.11, 0.15, 1.0)
        bg.inputs["Strength"].default_value = 0.85

    def add_sun_light(name, rot_deg, energy, color=(1, 1, 1), angle_deg=6.0):
        ld = bpy.data.lights.new(name, type='SUN')
        ld.energy = energy
        ld.color = color
        ld.angle = math.radians(angle_deg)
        lo = bpy.data.objects.new(name, ld)
        lo.rotation_euler = tuple(math.radians(a) for a in rot_deg)
        link_to_collection(lo, col_stage)
        return lo

    def add_area_light(name, loc, target, energy, size, color=(1, 1, 1)):
        ld = bpy.data.lights.new(name, type='AREA')
        ld.energy = energy
        ld.size = size
        ld.color = color
        lo = bpy.data.objects.new(name, ld)
        lo.location = Vector(loc)
        direction = Vector(target) - Vector(loc)
        lo.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        link_to_collection(lo, col_stage)
        return lo

    # Mesafeden bağımsız keskin stüdyo güneş + sıcak/soğuk 3-nokta alan ışıkları
    add_sun_light("KeySun",  (38, 12, -32),  energy=3.8, color=(1.0, 0.97, 0.93), angle_deg=8.0)
    add_sun_light("FillSun", (52, -10, 125), energy=1.3, color=(0.72, 0.85, 1.0), angle_deg=25.0)
    add_area_light("RimLight", (30, 220, 180), (0, 0, 60), energy=1800000.0, size=140.0, color=(1.0, 0.78, 0.58))

    # Kamera
    cam_data = bpy.data.cameras.new("PreviewCam")
    cam_data.lens = 48
    cam_data.clip_start = 1.0
    cam_data.clip_end = 5000.0
    cam = bpy.data.objects.new("PreviewCam", cam_data)
    link_to_collection(cam, col_stage)
    scene.camera = cam

    def aim_camera(cam_obj, loc, target):
        cam_obj.location = Vector(loc)
        direction = Vector(target) - Vector(loc)
        cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    scene.render.resolution_x = 1280
    scene.render.resolution_y = 960
    scene.render.image_settings.file_format = 'PNG'

    # Render 1: Montajlı Gimbal Labirent (baskı tablasını geçici gizle)
    col_plate.hide_render = True
    aim_camera(cam, (165, -230, 210), (0, 0, 50))
    scene.render.filepath = os.path.join(PREVIEW_DIR, "gimbal_maze_assembled.png")
    bpy.ops.render.render(write_still=True)

    # Render 2: 3D Baskı Tablası Düzeni
    col_plate.hide_render = False
    col_asm.hide_render = True
    aim_camera(cam, (PLATE_X - 5, -285, 345), (PLATE_X - 5, -5, 10))
    scene.render.filepath = os.path.join(PREVIEW_DIR, "gimbal_maze_print_plate.png")
    bpy.ops.render.render(write_still=True)

    # İkisini de görünür bırak, kamerayı montaja çevir ve .blend kaydet
    col_asm.hide_render = False
    col_plate.hide_render = False
    aim_camera(cam, (165, -230, 210), (0, 0, 50))

    blend_path = os.path.join(BLENDER_DIR, "gimbal_maze_3dprint.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[BLEND OK] {blend_path}")


if __name__ == "__main__":
    main()
