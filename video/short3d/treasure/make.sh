#!/usr/bin/env bash
# Treasure-detector 3D Short: full build after the Blender frames exist. Run from video/.
#   1 voice.py (narration + schedule)  2 export.mjs (3D scene)  3 track.mjs  4 blender_short.py (frames)
#   5 this script: LED glow -> overlay (alpha) -> sound -> final mp4
set -euo pipefail
D=short3d/treasure
B=$D/build
python pilot3d/glow.py "$B/${FRAMES_DIR:-frames}" "$B/glow_${FRAMES_DIR:-frames}" 120
node -e "
const fs=require('fs'); const s=JSON.parse(fs.readFileSync('$B/schedule.json')); const i=JSON.parse(fs.readFileSync('$B/scene_info.json'));
fs.writeFileSync('$B/overlay_data.json', JSON.stringify({schedule:{duration:s.duration,segments:{}}, sched:s, info:i}));"
node engine/render.mjs $D --page $D/overlay.html --data $B/overlay_data.json --size 1080x1920 --alpha --workers 1 --out $B/overlay.mov
../.venv/Scripts/python.exe $D/mix.py
ffmpeg -v error -y -framerate 30 -i "$B/glow_${FRAMES_DIR:-frames}/f_%04d.png" -i "$B/overlay.mov" -i "$B/audio.wav" \
  -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a \
  -c:v libx264 -preset medium -crf 18 -r 30 -c:a aac -b:a 192k -shortest "$B/treasure_short_en.mp4"
echo "wrote $B/treasure_short_en.mp4"
