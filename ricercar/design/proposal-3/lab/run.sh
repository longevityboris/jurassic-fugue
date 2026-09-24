#!/bin/sh
# usage: ./run.sh FILE.ly [extra checker args]
# Runs the lab copy of the checker (identical to ricercar/tools/check.py except that
# the voice-pair loop uses len(VOICES) instead of a hardcoded 4, so 2-3 voice labs work)
# with the ricercar ranges.
f="$1"; shift
python3 "$(dirname "$0")/check.py" "$f" --voices soprano,alto,tenor,bass \
  --range soprano=60-84 --range alto=53-77 --range tenor=48-72 --range bass=36-62 "$@"
