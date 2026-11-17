#!/usr/bin/env bash
# Quick build montage + final cut. Run from video/ after make.sh (main pieces) has finished.
set -euo pipefail
D=short3d/treasure
B=$D/build
../.venv/Scripts/python.exe $D/voice.py script_build.json build_
node $D/build_track.mjs
FRAMES_DIR=frames_build TRACK=build_track.json ANCHORS=build_anchors.json \
  "/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b -P $D/blender_short.py -- "$(pwd -W)/$B" 48 > $B/blender_build.log 2>&1
python pilot3d/glow.py "$B/frames_build" "$B/glow_frames_build" 120
node -e "
const fs=require('fs'); const r=(f)=>JSON.parse(fs.readFileSync('$B/'+f));
const s=r('build_schedule.json'), t=r('build_track.json');
fs.writeFileSync('$B/build_overlay_data.json', JSON.stringify({schedule:{duration:t.frames/30,segments:{}}, sched:s, events:r('build_events.json'), anchors:r('build_anchors.json')}));"
node engine/render.mjs $D --page $D/build_overlay.html --data $B/build_overlay_data.json --size 1080x1920 --alpha --workers 1 --out $B/build_overlay.mov
../.venv/Scripts/python.exe $D/assemble.py
