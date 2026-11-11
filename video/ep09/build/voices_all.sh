#!/usr/bin/env bash
# Episode 9 dub narration, one GPU job at a time; resumable (build/rebuild.done + dub caches)
set -euo pipefail
cd "$(dirname "$0")/../../.."
PY=.venv/Scripts/python; export PYTHONIOENCODING=utf-8
E=video/ep09; D=$E/build/rebuild.done
step() { local n=$1; shift; grep -qx "$n" $D 2>/dev/null && { echo "skip $n"; return; }; echo "$n $(date +%H:%M:%S)"; "$@"; echo $n >> $D; }
for l in tr hi pt es; do
  step narrate_$l $PY tools/dub.py $E $l --report
  step retake_$l $PY tools/cbx_retake.py $E $l
done
echo "ALL DUB VOICES DONE $(date +%H:%M:%S)"
