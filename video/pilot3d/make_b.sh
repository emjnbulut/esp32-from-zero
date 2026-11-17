#!/usr/bin/env bash
# Builds the cinematic (B) 20 s pilot from the Blender frames: LED glow -> 2D overlay (alpha) -> composite.
# Run from video/ after blender_anim.py has written pilot3d/build/bframes/ and pilot3d/build/overlay_data.json.
set -euo pipefail
B=pilot3d/build
python pilot3d/glow.py "$B/bframes" "$B/bglow"
node engine/render.mjs pilot3d --data "$B/overlay_data.json" --alpha --workers 1 --out "$B/overlay_b.mov"
ffmpeg -v error -y -framerate 30 -i "$B/bglow/f_%04d.png" -i "$B/overlay_b.mov" \
  -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p" -c:v libx264 -preset medium -crf 17 -r 30 "$B/pilot3d_blender.mp4"
echo "wrote $B/pilot3d_blender.mp4"
