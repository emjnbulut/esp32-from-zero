# 3D Short: "I turned my ESP32 into a treasure detector" (EN)

Style of the reference Shorts the creator picked (realistic 3D, macro camera, word-by-word captions), built with the
3D pipeline from `video/pilot3d` (Blender EEVEE, vertical 1080x1920). Project: `projects/05-treasure-detector`
(episodes 1-8 only: knob GPIO 34, button 22, RGB 25/26/27, red LED 23).

Build (from `video/`, one heavy job at a time):
1. `../.venv/Scripts/python.exe short3d/treasure/voice.py` - Chatterbox narration (channel voice), Whisper check/retakes, `build/schedule.json`
2. `node short3d/treasure/export.mjs` - 3D circuit (three.js) -> `build/scene.glb`, `build/scene_info.json`
3. `node short3d/treasure/track.mjs` - `story.mjs` evaluated per frame -> `build/track.json` (knob, LEDs from the real sketch logic, camera)
4. `blender -b -P short3d/treasure/blender_short.py -- <abs build dir> 48` - frames (~4 s each, resumable), `build/anchors.json`
5. `bash short3d/treasure/make.sh` - glow, overlay (captions, ruler, live code, confetti), sound (blips synced to the LED, click, fanfare, music), mp4

`story.mjs` is the single source of timing: captions, 3D and sound all read it.
