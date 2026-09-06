#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
ROOT="$(cd ../../../../.. && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  echo "Missing repo-root .venv. From the repository root run: uv sync" >&2
  exit 1
fi
# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"

jupyter nbconvert --to notebook --execute report.ipynb --output report.ipynb

if command -v quarto >/dev/null 2>&1; then
  quarto render report.ipynb --to pdf
else
  jupyter nbconvert --to markdown report.ipynb --output report-body.md
  pandoc report-body.md -o report.pdf \
    --pdf-engine=xelatex \
    -V documentclass=article \
    -V papersize=a4 \
    -V mainfont="Times New Roman" \
    -V fontsize=12pt \
    -V linestretch=1.15 \
    -V geometry:margin=2cm
  rm -f report-body.md
fi
