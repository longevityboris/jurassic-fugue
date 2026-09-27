#!/bin/sh
# Publish The Neighbour into the repo's top-level final/ folder: the five recordings and five
# scores under clean, shareable names, the listener's guide as a PDF, and one zip of everything.
#
# Usage:  sh ricercar/tools/publish.sh [piano|quartet|organ|orchestra|quintet|scores|all]   (default: all)
# Render scripts call it with their own version; run it with no argument after re-engraving.
# Sources: performance/<version>/ricercar_<version>.m4a (renders) and score/out/*.pdf (engraved;
# the full orchestral score comes from tools/full_score.py). Nothing is played through the speakers.
set -eu
VERSION="1.1"
T=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$T/.." && pwd)                 # ricercar/
FINAL=$(cd "$R/.." && pwd)/final
mkdir -p "$FINAL"
WHAT="${1:-all}"
ALBUM="The Neighbour: Ricercar on the Theme from Jurassic Park"

audio() {   # $1 key  $2 source m4a  $3 clean name  $4 track  $5 title suffix
  src="$R/$2"
  [ -f "$src" ] || { echo "skip $1: no render at $2 (run its render script)"; return 0; }
  ffmpeg -loglevel error -y -i "$src" -c copy -movflags +faststart \
    -metadata title="The Neighbour ($5)" -metadata album="$ALBUM" \
    -metadata artist="Boris Djordjevic" -metadata album_artist="Boris Djordjevic" \
    -metadata composer="John Williams (theme); Boris Djordjevic (ricercar)" \
    -metadata track="$4/5" -metadata date="2026" -metadata genre="Classical" \
    -metadata comment="Version $VERSION" "$FINAL/$3"
  echo "  $3"
}

score() {   # $1 source pdf  $2 clean name
  if [ -f "$R/$1" ]; then cp "$R/$1" "$FINAL/$2"; echo "  $2"; else echo "skip: no $1"; fi
}

want() { [ "$WHAT" = all ] || [ "$WHAT" = "$1" ]; }

echo "publishing to $FINAL"
want piano     && audio piano     performance/beethoven_piano/ricercar_beethoven_piano.m4a     The-Neighbour-Piano.m4a          1 "Piano"
want quartet   && audio quartet   performance/beethoven_quartet/ricercar_beethoven_quartet.m4a The-Neighbour-String-Quartet.m4a 2 "String Quartet"
want organ     && audio organ     performance/bach_organ/ricercar_bach_organ.m4a               The-Neighbour-Organ.m4a          3 "Organ"
want orchestra && audio orchestra performance/symphonic/ricercar_symphonic.m4a                 The-Neighbour-Orchestra.m4a      4 "Orchestra"
want quintet   && audio quintet   performance/quintet/ricercar_quintet.m4a                     The-Neighbour-Piano-Quintet.m4a  5 "Piano Quintet"

if [ "$WHAT" = all ] || [ "$WHAT" = scores ]; then
  score score/out/piano.pdf          The-Neighbour-Score-Piano.pdf
  score score/out/quartet.pdf        The-Neighbour-Score-String-Quartet.pdf
  score score/out/organ.pdf          The-Neighbour-Score-Organ.pdf
  score score/out/orchestra-full.pdf The-Neighbour-Score-Orchestra.pdf
  score score/out/ensemble.pdf       The-Neighbour-Score-Piano-Quintet.pdf
  # listener's guide: NOTES.md -> HTML (pandoc) -> A4 PDF (headless Chrome; weasyprint lacks its
  # native libraries on this Mac and pandoc's typst tables overlap)
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  if command -v pandoc >/dev/null 2>&1 && [ -x "$CHROME" ]; then
    TMP="${TMPDIR:-/tmp}/neighbour-guide"
    mkdir -p "$TMP"
    cat > "$TMP/guide.css" <<'EOF'
@page { size: A4; margin: 16mm 15mm; }
body { font-family: "Iowan Old Style", Georgia, serif; font-size: 10.5pt; line-height: 1.45; color: #1d1d1d; max-width: none; margin: 0; }
h1 { font-size: 21pt; margin: 0 0 4pt; } h2 { font-size: 13.5pt; margin-top: 16pt; border-bottom: 1px solid #ccc; padding-bottom: 2pt; }
table { border-collapse: collapse; font-size: 8.8pt; width: 100%; } tr { page-break-inside: avoid; }
th, td { border-bottom: 1px solid #ddd; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { background: #f4f1ea; } code { font-size: 8.8pt; } a { color: #1d1d1d; text-decoration: none; }
header#title-block-header { display: none; }
EOF
    (cd "$R" && pandoc NOTES.md -f gfm -t html5 --standalone --embed-resources \
        --metadata title="The Neighbour: a listener's guide" --css "$TMP/guide.css" -o "$TMP/guide.html") \
      && "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
           --print-to-pdf="$FINAL/The-Neighbour-Listening-Guide.pdf" "file://$TMP/guide.html" >/dev/null 2>&1 \
      && echo "  The-Neighbour-Listening-Guide.pdf" || echo "skip: listener's guide (pandoc/Chrome failed)"
  else
    echo "skip: listener's guide (needs pandoc and Google Chrome)"
  fi
fi

# one zip with everything, for sharing
(cd "$FINAL" && rm -f The-Neighbour-v*.zip && zip -q -X "The-Neighbour-v$VERSION.zip" The-Neighbour-*.m4a The-Neighbour-*.pdf 2>/dev/null) \
  && echo "  The-Neighbour-v$VERSION.zip"
echo "done"
