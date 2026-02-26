#!/usr/bin/env bash

# Usage:
#   ./run_maps.sh "/data/Twitter dataset" "results"
#
# Notes:
# - Launches one nohup job per geoTwitter*.zip
# - Writes per-file logs to logs/
# - Jobs run in parallel (one per zip)

DATASET_DIR="${1:-/data/Twitter dataset}"
OUTDIR="${2:-results}"
LOGDIR="${OUTDIR}/logs"

mkdir -p "$OUTDIR" "$LOGDIR"

shopt -s nullglob

count=0
for zipfile in "$DATASET_DIR"/geoTwitter20-*.zip; do
  base="$(basename "$zipfile")"
  logfile="${LOGDIR}/${base}.log"

  echo "Launching: $zipfile  ->  $logfile"
  nohup python3 map2.py \
    --input_path "$zipfile" \
    --output_folder "$OUTDIR" \
    > "$logfile" 2>&1 &

  ((count+=1))
done

echo "Launched $count jobs."
echo "To monitor: ls -1 ${LOGDIR} | head ; tail -f ${LOGDIR}/<somefile>.log"
echo "To see running PIDs: pgrep -af 'python3 map2.py'"
