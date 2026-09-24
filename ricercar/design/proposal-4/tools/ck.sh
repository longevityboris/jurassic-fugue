#!/bin/sh
# run the project checker with the four voice ranges
python3 /Users/biobook/Music/llm-music/fugue-jp/ricercar/tools/check.py "$@" --voices soprano,alto,tenor,bass --range soprano=60-84 --range alto=53-77 --range tenor=48-72 --range bass=36-62
