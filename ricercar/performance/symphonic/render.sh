#!/bin/sh
# The Neighbour, symphony orchestra: score + plan + scoring -> WAV + m4a, the reports, the copy in final/.
#   design/final-lab/plan.json  the performance (tempo, breaths, fermatas, dynamics, roles)
#   symphonic.json              the scoring (who plays what, octave doublings, pedal points, levels),
#                               its dynamics override (Climax I under Climax II, the quiet floor), hall
# Usage: sh render.sh [--keep-build]   (--keep-build keeps build/render and the seated stems for
# balance checks). Nothing is played through the speakers.
set -e
D=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$D/../.." && pwd)
python3 "$R/tools/orchestrate.py" "$R/score/music-voices.ly" "$R/design/final-lab/plan.json" "$D/symphonic.json" "$D/build"
if [ "$1" = "--keep-build" ]; then KS="--keep-stems"; else KS=""; fi
python3 "$R/tools/mix.py" "$D/build/manifest.json" $KS
# qa_mix.py reads the mix report next to its OUTDIR under the OUTDIR's name
ln -sf ricercar_symphonic.mix.json "$D/build.mix.json"
python3 "$R/orchestration/tests/qa_mix.py" "$D/build" --out "$D/ricercar_symphonic.qa.json" || QA=failed
rm -f "$D/build.mix.json"
if [ "${QA:-}" = failed ]; then echo "qa_mix.py FAILED: see ricercar_symphonic.qa.json"; fi
cp "$D/build/integrity.json" "$D/ricercar_symphonic.integrity.json"
cp "$D/build/orchestration.json" "$D/ricercar_symphonic.orchestration.json"
sh "$R/tools/publish.sh" orchestra   # clean-named, tagged copy in the top-level final/ folder
if [ "$1" != "--keep-build" ]; then
  # keep the reports, drop the dry stems and the intermediate MIDI (disk)
  rm -rf "$D/build/render" "$D/build/perform"
fi
echo "done: $D/ricercar_symphonic.wav, .m4a (published to final/)"
