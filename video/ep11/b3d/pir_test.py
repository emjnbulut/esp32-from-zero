"""Quick look at the PIR part: blender -b -P video/ep11/b3d/pir_test.py -> video/ep11/b3d/build/pir_test_*.png"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import bpy
from mathutils import Vector
import pbl, parts_pir
from pbl import MM
os.environ.setdefault("PBL_SAMPLES", "16")
k = pbl.Kit(engine="EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"D33", "VIN", "GND"})
pir = parts_pir.pir(k, [B.hole(40, "f"), B.hole(41, "f"), B.hole(42, "f")])
beams = parts_pir.zones(k, pir)
parts_pir.set_zones(beams, {4: 1.0, 5: 0.5}, idle=0.08)
k.lights(center=(0.035, 0.0, 0.0), key=2.2)
cam, tgt = k.camera(lens=50, fstop=10.0)
out = os.path.join(HERE, "build"); os.makedirs(out, exist_ok=True)
c = pir["center"]
for name, pos, look in (("hero", c + Vector((-40, -110, 80)), pir["top"]),
                        ("wide", c + Vector((-60, -260, 200)), c + Vector((0, -40, 20)))):
    cam.location = pos * MM; tgt.location = look * MM
    k.scene.render.filepath = os.path.join(out, f"pir_test_{name}.png")
    bpy.ops.render.render(write_still=True)
parts_pir.set_zones(beams, {})
pir["lift"].location.z += 22; pir["lift"].rotation_euler.x = math.radians(150)
cam.location = (c + Vector((-30, -90, 70))) * MM; tgt.location = (c + Vector((0, 0, 28))) * MM
k.scene.render.filepath = os.path.join(out, "pir_test_lifted.png")
bpy.ops.render.render(write_still=True)
print("PIR TEST DONE")
