"""Look test for the Ep 17 props: blender -b -P video/ep17/b3d/props_test.py -> video/ep17/b3d/build/props_test.png"""
import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import pbl  # noqa: E402
import parts_ep17 as p17  # noqa: E402

k = pbl.Kit(engine="EEVEE")
k.desk()
k.lights(center=(0.0, 0.0, 0.0), key=2.2)
r = p17.relay_module(k, (-85, 0, 0), yaw_deg=160)
r["set_led"](0, 1.0)
f = p17.usb_fan(k, (5, 5, 0))
f["set_spin"](0.5)
c = p17.relay_cutaway(k, (85, 0, 0))
c["set_arm"](0.85)
c["set_spark"](0.7)
for p, t in ((r, "relay"), (f, "fan"), (c, "inside")):
    k.tag(t, p["top"])
cam, tgt = k.camera(lens=50, fstop=4.0)
cam.location = k.world_pos((0, -330, 170))
tgt.location = k.world_pos((0, 0, 25))
os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
k.scene.render.filepath = os.path.join(HERE, "build", "props_test.png")
bpy.ops.render.render(write_still=True)
print("WROTE", k.scene.render.filepath)
