#!/usr/bin/env bash
# After tools/rebuild_voices.sh: Shorts (new voices, retakes), trailer, then the delivery folder.
# Usage: bash tools/finish_all.sh   (resumable: steps recorded in build/finish.done)
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python
export PYTHONIOENCODING=utf-8
mkdir -p build
DONE=build/finish.done
step() { local name=$1; shift; if grep -qx "$name" $DONE 2>/dev/null; then echo "skip $name"; return; fi
  echo "[finish] $name  $(date +%H:%M:%S)"; "$@"; echo "$name" >> $DONE; }

for spec in "ep01:en tr hi pt" "ep02:en tr" "ep03:en tr" "ep04:en tr"; do
  ep=${spec%%:*}
  for l in ${spec#*:}; do
    # narrate first (short.py caches the takes), retake weak lines, then the full build reuses them
    step short_${ep}_$l $PY tools/short.py video/shorts/$ep $l --narrate
    step retake_short_${ep}_$l $PY tools/cbx_retake.py video/shorts/$ep $l --short
    step short2_${ep}_$l $PY tools/short.py video/shorts/$ep $l
  done
done
step trailer $PY tools/trailer.py
echo "[finish] DONE $(date +%H:%M:%S)"
