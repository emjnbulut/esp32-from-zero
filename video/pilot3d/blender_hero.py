"""Cinematic hero frame of the 3D pilot in Blender (Cycles, GPU).

Same geometry as the three.js pilot (exported by export_glb.mjs), re-lit with physical materials,
a perspective macro camera and depth of field. Used for thumbnails and cold-open hero shots.

  blender -b -P pilot3d/blender_hero.py -- pilot3d/build/scene.glb <abs out.png> [samples] [resolution %]
"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1])))
from b3d_scene import build, color_management, gl, use_gpu_cycles  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
GLB, OUT = argv[0], argv[1]
SAMPLES = int(argv[2]) if len(argv) > 2 else 128

scene, root, lib, ledlight = build(GLB)

# camera: low macro angle, LED in focus
cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 50
cam_d.clip_start = 0.001
cam_d.dof.use_dof = True
cam_d.dof.aperture_fstop = 11
cam = bpy.data.objects.new("cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam
look = gl(14, 9, 6)
th, el, dist = math.radians(-30), math.radians(24), 0.135
cam.location = look + Vector((dist * math.cos(el) * math.sin(th), -dist * math.cos(el) * math.cos(th), dist * math.sin(el)))
cam.rotation_euler = (look - cam.location).to_track_quat("-Z", "Y").to_euler()
cam_d.dof.focus_distance = (gl(39.37, 14, 10.16) - cam.location).length

print("devices:", use_gpu_cycles(scene, SAMPLES))
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.resolution_percentage = int(argv[3]) if len(argv) > 3 else 100
color_management(scene)
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("wrote", OUT)
