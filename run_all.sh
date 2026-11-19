#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
for t in Task01 Task02 Task03 Task04 Task05 Task06 Task07; do mkdir -p "$t/outputs"; done
echo '=== 1/3 BUILDING ALL C PROGRAMS ==='
make all
echo '=== 2/3 RUNNING TASK PROGRAMS ==='
for t in Task01 Task02 Task03 Task04 Task05 Task06 Task07; do
  echo "===== $t ====="
  make -C "$t" run 2>&1 | tee "$t/outputs/run.txt"
  if [[ "$t" == "Task03" ]]; then
    echo "[Expected fault demonstration]"
    (cd Task03 && ulimit -c 0; ./run_segfault.sh) 2>&1 | tee "$t/outputs/segfault.txt" || true
  fi
done
echo '=== 3/3 GENERATING ADDITIONAL EXPERIMENTS ==='
python3 experiments.py
echo '=== COMPLETE: check Task01–Task07/outputs/ ==='
