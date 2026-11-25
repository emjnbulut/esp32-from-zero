"""Look test for the Ep 14 fruit props: blender -b -P video/ep14/b3d/fruit_test.py  -> video/ep14/b3d/build/fruit_test.png"""
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import pbl  # noqa: E402
import parts_ep14 as p14  # noqa: E402

k = pbl.Kit(engine="EEVEE")
k.desk()
k.lights(center=(0.0, 0.0, 0.0), key=2.2)
b = p14.banana(k, (-85, -5, 0), yaw_deg=15)
a = p14.apple(k, (0, 5, 0))
o = p14.orange(k, (60, 0, 0))
glow = p14.touch_glow(k, a["centre"], radius=27)
glow(0.8)
for f, tagtxt in ((b, "do"), (a, "mi"), (o, "sol")):
    k.tag(tagtxt, f["top"])
cam, tgt = k.camera(lens=50, fstop=4.0)
cam.location = k.world_pos((0, -330, 190))
tgt.location = k.world_pos((0, 0, 18))
os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
k.scene.render.filepath = os.path.join(HERE, "build", "fruit_test.png")
bpy.ops.render.render(write_still=True)
print("WROTE", k.scene.render.filepath)
