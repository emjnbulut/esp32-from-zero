#!/usr/bin/env bash
# Same steps as tools/rebuild_voices.sh, in two parallel workers sharing build/rebuild.done:
#   bash tools/rebuild_split.sh voice   ep01 ep02 ...   narration + retakes + schedule (GPU, one at a time)
#   bash tools/rebuild_split.sh picture ep01 ep02 ...   render, mix, subs, compose, dub tracks (CPU);
#                                                        waits until the episode's schedule is done
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python
export PYTHONIOENCODING=utf-8
LANGS="tr hi pt es"
MODE=$1; shift

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
  if [ "$MODE" = voice ]; then
    if [ -f $E/make_script.py ]; then step $ep script $PY $E/make_script.py; fi
    step $ep tts $PY tools/tts.py $E
    step $ep retake_en $PY tools/cbx_retake.py $E en
    step $ep schedule0 $PY tools/build.py $E schedule
    for l in $LANGS; do
      step $ep narrate_$l $PY tools/dub.py $E $l --report
      step $ep retake_$l $PY tools/cbx_retake.py $E $l
    done
    step $ep schedule $PY tools/build.py $E schedule
    echo "[$ep] VOICE DONE $(date +%H:%M:%S)"
  else
    until grep -qx schedule $E/build/rebuild.done 2>/dev/null; do sleep 30; done
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
  fi
done
