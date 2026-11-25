"""Look test for the Ep 16 props: blender -b -P video/ep16/b3d/props_test.py -> video/ep16/b3d/build/props_test.png"""
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import pbl  # noqa: E402
import parts_ep16 as p16  # noqa: E402

k = pbl.Kit(engine="EEVEE")
k.desk()
k.lights(center=(0.0, 0.0, 0.0), key=2.2)
h = p16.hoop(k, (55, 10, 0))
pz = h["sensor_spot"].z - 7.6                      # raise the module so its beam crosses the cup mouth
k.box("pedestal", (30, 20, pz - 3.0), (-60, 10, (pz - 3.0) / 2), k.mat("ped", "#5a6478", 0.6), None, bevel=0.5)
m = p16.ir_module(k, (-60, 10, pz - 3.0), yaw_deg=-90)
m["set"](0.9)
ball = p16.paper_ball(k, (-15, 0, pz + 22))
e = m["emitter"]
beam = p16.ir_beam(k, e, (h["sensor_spot"].x, e.y, e.z))
for f, t in ((m, "ir"), (h, "hoop")):
    k.tag(t, f["top"])
cam, tgt = k.camera(lens=50, fstop=4.0)
cam.location = k.world_pos((-5, -330, 170))
tgt.location = k.world_pos((-5, 0, 30))
os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
k.scene.render.filepath = os.path.join(HERE, "build", "props_test.png")
bpy.ops.render.render(write_still=True)
print("WROTE", k.scene.render.filepath)
