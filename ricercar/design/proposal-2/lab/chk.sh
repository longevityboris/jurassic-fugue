#!/bin/sh
# Run the project counterpoint checker with the task's instrument ranges enforced.
# usage: sh chk.sh FILE.ly [extra check.py args]
# Every lab defines all four variables (unused ones as rests): check.py indexes 4 voices.
HERE=$(cd "$(dirname "$0")" && pwd)
exec python3 "$HERE/../../../tools/check.py" "$@" --voices soprano,alto,tenor,bass \
  --range soprano=60-84 --range alto=53-77 --range tenor=48-72 --range bass=36-62
