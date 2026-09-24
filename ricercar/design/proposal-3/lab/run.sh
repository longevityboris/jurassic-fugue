#!/bin/sh
# usage: ./run.sh FILE.ly [extra checker args]
# Runs the official checker (ricercar/tools/check.py) with the ricercar ranges.
# Lab files always define all four voices (rests where silent), so the official checker applies.
f="$1"; shift
python3 "$(dirname "$0")/../../../tools/check.py" "$f" --voices soprano,alto,tenor,bass \
  --range soprano=60-84 --range alto=53-77 --range tenor=48-72 --range bass=36-62 "$@"
