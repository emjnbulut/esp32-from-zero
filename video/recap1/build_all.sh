#!/usr/bin/env bash
# Recap: TR dub -> final schedule -> render -> audio -> compose -> TR dub video -> subs. Resumable via build/rebuild.done.
set -euo pipefail
cd "$(dirname "$0")/../.."
PY=.venv/Scripts/python
export PYTHONIOENCODING=utf-8
E=video/recap1
step() { local n=$1; shift; if grep -qx "$n" $E/build/rebuild.done 2>/dev/null; then echo "[recap1] skip $n"; return; fi; echo "[recap1] $n  $(date +%H:%M:%S)"; "$@"; echo "$n" >> $E/build/rebuild.done; }
step narrate_tr $PY tools/dub.py $E tr --report
step retake_tr $PY tools/cbx_retake.py $E tr
step schedule $PY tools/build.py $E schedule
step render bash -c "cd video && node engine/render.mjs recap1 > recap1/build/render.log 2>&1"
step audio $PY tools/build.py $E audio
step compose $PY tools/build.py $E compose
step dub_tr $PY tools/dub.py $E tr
step subs $PY tools/build.py $E subs
echo "[recap1] DONE $(date +%H:%M:%S)"
