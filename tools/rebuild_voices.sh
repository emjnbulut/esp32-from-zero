#!/usr/bin/env bash
# Re-narrate and rebuild whole episodes with the Chatterbox voices (tools/cbx.py VOICES).
# Usage: bash tools/rebuild_voices.sh ep01 ep02 ...   (log: build/rebuild_voices.log)
# Each finished step is recorded in video/<ep>/build/rebuild.done, so a rerun skips it.
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python
export PYTHONIOENCODING=utf-8
LANGS="tr hi pt es"

step() {  # step <ep> <name> <command...>
  local ep=$1 name=$2; shift 2
  local done=video/$ep/build/rebuild.done
  if grep -qx "$name" "$done" 2>/dev/null; then echo "[$ep] skip $name"; return; fi
  echo "[$ep] $name  $(date +%H:%M:%S)"
  "$@"
  echo "$name" >> "$done"
}

for ep in "$@"; do
  E=video/$ep
  mkdir -p $E/build
  if [ -f $E/make_script.py ]; then step $ep script $PY $E/make_script.py; fi
  step $ep tts $PY tools/tts.py $E
  step $ep retake_en $PY tools/cbx_retake.py $E en
  step $ep schedule0 $PY tools/build.py $E schedule   # dub.py needs a schedule; redone below with the dubs
  for l in $LANGS; do
    step $ep narrate_$l $PY tools/dub.py $E $l --report
    step $ep retake_$l $PY tools/cbx_retake.py $E $l
  done
  step $ep schedule $PY tools/build.py $E schedule
  step $ep render bash -c "cd video && node engine/render.mjs $ep > $ep/build/render.log 2>&1"
  step $ep audio $PY tools/build.py $E audio
  step $ep subs $PY tools/build.py $E subs
  step $ep compose $PY tools/build.py $E compose
  for l in $LANGS; do
    step $ep dub_$l $PY tools/dub.py $E $l
  done
  if [ -f $E/make_localize.py ]; then step $ep localize $PY $E/make_localize.py
  else step $ep localize $PY tools/rechapter.py $E; fi
  echo "[$ep] DONE $(date +%H:%M:%S)"
done
