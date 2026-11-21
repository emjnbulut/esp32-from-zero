#!/usr/bin/env bash
# Encode the Blender pilot frames + synthesized buzzer/click sounds -> build/ep10_pilot_3d.mp4
# Times come from times.json (go, react, record, unplug, plug).
set -euo pipefail
cd "$(dirname "$0")"
read -r GO REACT REC UNP PLUG < <(python -c "import json;t=json.load(open('times.json'));print(t['go'],t['react'],t['record'],t['unplug'],t['plug'])")
ms() { python -c "print(int(round(($1)*1000)))"; }
tone() { # freq dur delay_s vol
  echo "sine=f=$1:d=$2,volume=$4,afade=t=in:d=0.005,afade=t=out:st=$(python -c "print(max(0,$2-0.03))"):d=0.03,adelay=$(ms "$3")|$(ms "$3")"
}
click() { # delay_s vol
  echo "anoisesrc=d=0.03:c=white:a=$2,highpass=f=1800,afade=t=out:d=0.03,adelay=$(ms "$1")|$(ms "$1")"
}
F=(
  "$(tone 1568 0.20 "$GO" 0.35)"
  "$(click "$REACT" 0.5)"
  "$(tone 1047 0.14 "$REC" 0.3)"
  "$(tone 1319 0.14 "$REC+0.22" 0.3)"
  "$(tone 1568 0.26 "$REC+0.44" 0.3)"
  "$(click "$UNP" 0.35)"
  "$(click "$PLUG+0.2" 0.35)"
  "$(tone 2093 0.08 "$PLUG+0.35" 0.2)"
)
FC=""
for i in "${!F[@]}"; do FC+="${F[$i]}[a$i];"; done
for i in "${!F[@]}"; do FC+="[a$i]"; done
FC+="amix=inputs=${#F[@]}:normalize=0,apad=whole_dur=9[aout]"
ffmpeg -y -loglevel error -framerate 30 -i build/frames/f_%04d.png -filter_complex "$FC" -map 0:v -map "[aout]" \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest build/ep10_pilot_3d.mp4
echo "build/ep10_pilot_3d.mp4"
