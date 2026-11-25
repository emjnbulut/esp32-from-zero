"""Look test for the Ep 15 props: blender -b -P video/ep15/b3d/props_test.py -> video/ep15/b3d/build/props_test.png"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import pbl  # noqa: E402
import parts_ep15 as p15  # noqa: E402

k = pbl.Kit(engine="EEVEE")
k.desk()
k.lights(center=(0.0, 0.0, 0.0), key=2.2)
m = p15.ldr_module(k, (-70, 0, 0), yaw_deg=-10)
d = p15.drawer(k, (20, 10, 0))
d["set_open"](26)
c = p15.light_cone(k, (95, 0, 0))
c["set"](0.6)
for f, t in ((m, "ldr"), (d, "drawer"), (c, "light")):
    k.tag(t, f["top"])
cam, tgt = k.camera(lens=50, fstop=4.0)
cam.location = k.world_pos((10, -300, 170))
tgt.location = k.world_pos((10, 0, 18))
os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
k.scene.render.filepath = os.path.join(HERE, "build", "props_test.png")
bpy.ops.render.render(write_still=True)
print("WROTE", k.scene.render.filepath)
