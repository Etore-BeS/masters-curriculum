#!/usr/bin/env bash
# Render all FT108A classification study scenes → figures/manim/
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../../../../ && pwd)"
# Prefer repo-root shared venv
if [[ -x "$ROOT/.venv/bin/manim" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
elif [[ -x ../../../.venv/bin/manim ]]; then
  source ../../../.venv/bin/activate
else
  echo "No manim in repo-root .venv. Run: uv sync --group manim" >&2
  exit 1
fi

QUALITY="${1:--ql}"
SCENES=(BiasVariance EntropyGain TreePrune KNNScale MLPForward OverfitGap MajorityVote NaiveBayesProduct)
OUT="figures/manim"
mkdir -p "$OUT"

for s in "${SCENES[@]}"; do
  echo "=== Rendering $s ==="
  manim "$QUALITY" scenes.py "$s"
done

for s in "${SCENES[@]}"; do
  mp4=$(find media/videos/scenes -type f -name "${s}.mp4" 2>/dev/null | head -1 || true)
  if [[ -n "${mp4:-}" ]]; then
    cp -f "$mp4" "$OUT/${s}.mp4"
    # Mid-clip frame (end frames are often black fades)
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/${s}.mp4" 2>/dev/null || echo 2)
    mid=$(python3 -c "print(max(0.5, float('${dur}') * 0.45))")
    ffmpeg -y -ss "$mid" -i "$OUT/${s}.mp4" -frames:v 1 -update 1 "$OUT/${s}.png" 2>/dev/null || true
    echo "copied $s (thumb @ ${mid}s)"
  else
    echo "MISSING $s" >&2
  fi
done
ls -la "$OUT/"
