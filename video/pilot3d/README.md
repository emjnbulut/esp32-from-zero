# 3D pilot (17 Nov 2026): PWM dims an LED

Trial of the hybrid 2D/3D style (PRODUCTION_GUIDELINES section 12). Same wiring as episode 5: red LED on GPIO 23 + 220 ohm to GND.

- **A) three.js, stylized** (`index.html` + `scene3d.js`): toon shading + outlines, orthographic camera, runs inside the normal
  Playwright engine (every frame is a pure function of t; 2D code card/labels are ordinary engine overlays).
  `node engine/render.mjs pilot3d --data pilot3d/data.json --gpu --workers 2 --out pilot3d/build/pilot3d_threejs.mp4`
  (20 s in ~1 min on the RTX 4060). `--gpu` and `--allow-file-access-from-files` were added to render.mjs for this.
- **B) Blender Cycles, cinematic hero frame** (same geometry): `node pilot3d/export_glb.mjs 18.5` ->
  `blender -b -P pilot3d/blender_hero.py -- pilot3d/build/scene.glb <abs out.png> 160` -> `python pilot3d/glow.py raw.png out.png`.
  ~1 min per 1080p frame, so Blender is for thumbnails / short hero shots, not whole scenes.
- Comparison: `build/compare_A_B.png`. Models are procedural (no downloaded assets, no license questions).
