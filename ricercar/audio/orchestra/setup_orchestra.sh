#!/usr/bin/env bash
# Install, build and verify everything render_orchestra.py needs.  Idempotent:
# a second run checks what is there and only redoes what is missing or stale.
#
#   ./setup_orchestra.sh            install what is missing, build, verify
#   ./setup_orchestra.sh --check    verify only (no downloads, no builds); exit 1 if anything is missing
#   ./setup_orchestra.sh --force    also rebuild the instruments and re-measure the tuning
#   ./setup_orchestra.sh --fetch    downloads only
#
# Assets live outside git in $SAMPLE_LIBRARIES (default ~/Music/SampleLibraries):
#   Orchestra/VSCO-2-CE/     Versilian Studios Chamber Orchestra 2, Community Edition
#                            (Samuel Gossner), CC0 1.0.  git sparse checkout of the
#                            directories below at a pinned commit:
#                            https://github.com/sgossner/VSCO-2-CE
#   Orchestra/IowaMIS-winds/ University of Iowa Electronic Music Studios, Musical
#                            Instrument Samples (pre-2012 recordings: pp / mf / ff
#                            chromatic runs, anechoic chamber).  "freely available
#                            ... may be downloaded and used for any projects, without
#                            restrictions": https://theremin.music.uiowa.edu/MIS.html
#                            (file list: sources/iowa_winds_brass.txt)
#   VPO3/                    Virtual Playing Orchestra 3 (Paul Battersby), already
#                            installed by the strings setup (setup_strings.sh
#                            --with-vpo3); free for any music, credit on
#                            redistribution: https://virtualplaying.com/virtual-playing-orchestra/
#                            Used here for the string sections' second recording
#                            (Sonatina Symphonic Orchestra, CC Sampling Plus 1.0) and
#                            the four-horn section (Mattias Westlund, CC BY 3.0?:
#                            see VPO3 Documentation/license.htm).
#   IR/Detmold-Konzerthaus-S1R163-MS-48k.wav   the hall (built by audio/piano/setup_piano.sh,
#                            Detmold SRIR database, Zenodo 4116247, CC BY 4.0)
#   bin/sfizz_render or tools/sfizz/...        the project's pinned sfizz (piano/strings setup)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
LIB="${SAMPLE_LIBRARIES:-$HOME/Music/SampleLibraries}"
ORCH="$LIB/Orchestra"
MODE="${1:-install}"
PY=python3

VSCO_URL="https://github.com/sgossner/VSCO-2-CE.git"
VSCO_SHA="440300901dfe9275fd84e0b7763af1f8443ae62e"      # master, 2020-08-05
VSCO_DIRS=(
  "Strings/Violin Section/susVib" "Strings/Violin Section/Spic"
  "Strings/Viola Section/susvib" "Strings/Viola Section/spic"
  "Strings/Cello Section/susvib" "Strings/Cello Section/spic"
  "Strings/Solo Contrabass/SusVib" "Strings/Solo Contrabass/SusNV" "Strings/Solo Contrabass/Spic"
  "Brass/F Horn/sus" "Brass/F Horn/stac"
  "Brass/Trumpet/sus" "Brass/Trumpet/susvib" "Brass/Trumpet/stac"
  "Brass/Tenor Trombone/sus" "Brass/Tenor Trombone/stac"
  "Brass/Tuba/sus" "Brass/Tuba/stac"
  "Woodwinds/Flute/susNV" "Woodwinds/Flute/susvib" "Woodwinds/Flute/stac"
  "Woodwinds/Oboe/Sus" "Woodwinds/Oboe/Vib" "Woodwinds/Oboe/Stacc"
  "Woodwinds/Clarinet/susLong" "Woodwinds/Clarinet/stac"
  "Woodwinds/Bassoon/sus" "Woodwinds/Bassoon/vib" "Woodwinds/Bassoon/stac"
  "Percussion/Timpani"
)
IOWA_BASE="https://theremin.music.uiowa.edu"
IOWA_LIST="$HERE/sources/iowa_winds_brass.txt"

say() { printf '[setup_orchestra] %s\n' "$*"; }
fail() { printf '[setup_orchestra] FAIL: %s\n' "$*" >&2; exit 1; }
missing=0

free_gb() { df -g "$HOME" | awk 'NR==2 {print $4}'; }

# ------------------------------------------------------------------ VSCO-2-CE
vsco_ok() {
  [ -d "$ORCH/VSCO-2-CE/.git" ] || return 1
  [ "$(git -C "$ORCH/VSCO-2-CE" rev-parse HEAD 2>/dev/null)" = "$VSCO_SHA" ] || return 1
  for d in "${VSCO_DIRS[@]}"; do
    [ -n "$(ls "$ORCH/VSCO-2-CE/$d" 2>/dev/null | head -1)" ] || return 1
  done
  [ -f "$ORCH/VSCO-2-CE/.ricercar_complete" ] || return 1
}
fetch_vsco() {
  say "VSCO-2-CE: sparse checkout of ${#VSCO_DIRS[@]} directories at ${VSCO_SHA:0:10} (about 1 GB)"
  mkdir -p "$ORCH"
  if [ ! -d "$ORCH/VSCO-2-CE/.git" ]; then
    git clone --filter=blob:none --no-checkout --sparse "$VSCO_URL" "$ORCH/VSCO-2-CE"
  fi
  git -C "$ORCH/VSCO-2-CE" sparse-checkout set --no-cone "${VSCO_DIRS[@]/#//}" /LICENSE /README.md /Readme.txt
  git -C "$ORCH/VSCO-2-CE" checkout -q "$VSCO_SHA"
  touch "$ORCH/VSCO-2-CE/.ricercar_complete"
}

# ------------------------------------------------------------------ Iowa MIS winds and brass
iowa_ok() {
  local n; n=$(grep -c . "$IOWA_LIST")
  [ -f "$ORCH/IowaMIS-winds/manifest.sha256" ] || return 1
  [ "$(grep -c . "$ORCH/IowaMIS-winds/manifest.sha256")" = "$n" ] || return 1
  (cd "$ORCH/IowaMIS-winds" && shasum -a 256 -c --quiet manifest.sha256) >/dev/null 2>&1 || return 1
}
fetch_iowa() {
  say "Iowa MIS winds and brass: $(grep -c . "$IOWA_LIST") files (about 480 MB)"
  mkdir -p "$ORCH/IowaMIS-winds"
  while IFS= read -r rel; do
    [ -n "$rel" ] || continue
    local name="${rel##*/}"
    local dst="$ORCH/IowaMIS-winds/$name"
    if [ -s "$dst" ]; then continue; fi
    local url="$IOWA_BASE/${rel// /%20}"
    curl -sfL --retry 4 --retry-delay 3 --max-time 600 -o "$dst.part" "$url" || fail "download $url"
    # an AIFF starts with FORM....AIFF / AIFC
    head -c 12 "$dst.part" | grep -q "AIF" || fail "not an AIFF: $url"
    mv "$dst.part" "$dst"
  done < "$IOWA_LIST"
  (cd "$ORCH/IowaMIS-winds" && while IFS= read -r rel; do [ -n "$rel" ] && shasum -a 256 "${rel##*/}"; done < "$IOWA_LIST") \
    > "$ORCH/IowaMIS-winds/manifest.sha256"
}

# ------------------------------------------------------------------ run
if [ "$MODE" = "--check" ]; then
  vsco_ok && say "VSCO-2-CE ok" || { say "VSCO-2-CE missing or incomplete"; missing=1; }
  iowa_ok && say "Iowa winds/brass ok" || { say "Iowa winds/brass missing or corrupt"; missing=1; }
else
  if ! vsco_ok || ! iowa_ok; then
    [ "$(free_gb)" -ge 8 ] || fail "less than 8 GB free on $HOME"
  fi
  vsco_ok && say "VSCO-2-CE ok" || fetch_vsco
  iowa_ok && say "Iowa winds/brass ok" || fetch_iowa
  vsco_ok || fail "VSCO-2-CE incomplete after fetch"
  iowa_ok || fail "Iowa winds/brass incomplete after fetch"
fi
[ "$MODE" = "--fetch" ] && { say "downloads done"; exit 0; }

# (build and verification stages follow once their scripts exist)
say "done$( [ $missing = 1 ] && echo ' (with missing items)' )"
exit $missing
