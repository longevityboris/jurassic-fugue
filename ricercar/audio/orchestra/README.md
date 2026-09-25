# Orchestra renderer (symphonic version)

`render_orchestra.py` turns a multi-track MIDI file (the interface is `CONTRACT.md`) into a romantic
symphony orchestra in the measured Detmold Konzerthaus: 48 kHz / 24-bit WAV at -1 dBTP, AAC m4a, and a
JSON report. Free samples: VSCO-2-CE (CC0), University of Iowa MIS winds and brass, Virtual Playing
Orchestra 3 (string sections' second recording, four-horn section). `setup_orchestra.sh` installs,
builds and verifies everything once (assets live outside git in `~/Music/SampleLibraries`).

## Chain

```sh
# score + plan + orchestration spec -> one MIDI per renderer group (integrity-checked)
python3 tools/orchestrate.py SCORE.ly PLAN.json SPEC.json OUTDIR
python3 audio/orchestra/render_orchestra.py OUTDIR/orchestra.mid -o OUT      # reads OUTDIR/orchestra.orchestra.json
# or, inside an ensemble: python3 tools/mix.py OUTDIR/manifest.json
```

A plain `perform.py --target strings` file also renders (soprano/alto/tenor/bass -> Violins I,
Violins II, violas, cellos).

The demo skeleton goes through the real chain: `python3 make_demo.py --render` writes
`out/demo_instruments`, `out/demo_tutti`, `out/demo_crescendo` and `out/skeleton_orchestra` (perform.py
+ orchestrate.py with `specs/skeleton_symphonic.json`: 16 part tracks, strings on the four voices,
basses 8vb, the arioso's lament on a solo clarinet, woodwind doublings, a horn and a timpani roll on the
dominant pedal, a2 horns, trumpet, trombones and tuba only in the two climaxes and the apotheosis peak).
It is a renderer test, not the final scoring. Rendering the 232 s skeleton takes about 30 s.

## Measurements

`python3 probe_orchestra.py` (per part, alone, dry: held notes low/middle/high of the compass at mf, a
pp-ff-pp hairpin inside one held note, six short notes, a slur; timpani strokes and a crescendo roll)
writes `evidence/probe.json`; `python3 qa_orchestra.py` (skeleton stems, instrument demo, crescendo
demo, final file) writes `evidence/qa.json`. Numbers below are from the current commit.

**Pitch (A4 = 440 Hz).** Probe: 112 of 112 held and slurred notes measured, median 1.0 cents, worst
7.8 cents. Skeleton stems: 1290 of 1314 notes measured, median 0.7 c, p95 3.0 c; the one note over 25 c
is a 0.41 s tuba Eb1 that YIN cannot read (its held Eb1 measures +0.3 c on harmonics 2-5). Timpani are
tuned by the builder's kettledrum partial-template fit (YIN reads a roll +33 c; not a valid measure
for a drum).

**Dynamics change the timbre.** Per part at pp / mf / ff (demo_instruments, K-weighted level dB and
spectral centroid Hz; richness = harmonics 3+ re 1-2):

| part | pp | mf | ff | richness pp->ff dB | centroid pp / mf / ff |
|---|---|---|---|---|---|
| fl | -43.4 | -34.6 | -27.6 | +6.4 | 2124 / 2461 / 2716 |
| ob | -43.6 | -35.3 | -28.5 | +4.5 | 2314 / 1893 / 2684 |
| cl | -50.0 | -37.3 | -29.0 | +11.5 | 4451 / 2725 / 3495 |
| bn | -46.1 | -36.8 | -30.0 | +3.0 | 1017 / 1103 / 1620 |
| hn | -46.7 | -33.6 | -23.8 | +5.9 | 746 / 692 / 792 |
| tpt | -45.4 | -32.1 | -22.2 | +11.3 | 1202 / 2218 / 2589 |
| tbn | -45.9 | -33.3 | -23.2 | +6.8 | 1439 / 1560 / 3275 |
| btbn | -46.3 | -33.2 | -22.7 | +4.6 | 1242 / 1216 / 2965 |
| tba | -48.0 | -36.0 | -25.9 | +13.9 | 1210 / 751 / 1081 |
| timp | -50.8 | -37.2 | -25.8 | | 1785 / 400 / 414 |
| vn1 | -44.6 | -31.9 | -21.8 | +2.0 | 3699 / 4135 / 4516 |
| vn2 | -43.9 | -31.3 | -21.5 | +9.1 | 2653 / 3312 / 3651 |
| va | -44.6 | -32.0 | -23.4 | -0.7 | 1820 / 2290 / 2645 |
| vc | -42.1 | -30.6 | -21.5 | +0.5 | 1532 / 1983 / 2296 |
| cb | -47.2 | -36.2 | -27.7 | +3.9 | 971 / 1265 / 1491 |

Inside a held note (probe hairpin), level follows CC1 with r = 0.96-1.00 for every part; the timbre
follows it (centroid or richness r > 0.5) for all but the double basses, whose recorded layers barely
differ in colour at A2 (both measures fall slightly as they swell: accepted). The crescendo demo's
centroid does not rise because low brass and timpani join as it grows; its level rises 31 dB with
r = 0.996.

**Short and long notes.** Short notes (CC20 short, 0.2 s) fall 20 dB within 0.25-0.40 s in every part
except the low strings, whose spiccato recordings ring to the next note 0.45 s later (the room of the
recording). Held notes at a constant CC1 hold within 3-5 dB (winds, brass, basses); the upper strings
move 6-11 dB in 100 ms frames inside a held note, as each recording does alone (vibrato and bow; a
sweep of every key, stack against each recording, `sweep_strings.py`). No clicks in any stem or in the
mix; no dropped or stuck notes.

**Seating and hall.** American seating by default (German with the sidecar): violins I 30 deg left at
1 m, cellos 27 deg right, basses 37 deg right at 5 m, woodwinds 6.5-8 m, brass 9-10.5 m, timpani 12 m;
depth delays the direct sound and lowers it `20 log10(10 / (10 + depth))`, the hall is not
attenuated, so the back rows sound further away and wetter. Hall -5 dB re dry, C80 +9.3 dB. Final
skeleton file: -19.1 LUFS integrated, loudness range 26.7 LU, true peak -1.0 dBTP (m4a -0.99 dBFS),
L/R correlation 0.48, lead-in 0.3 s (`offset_s` -0.3).

**Tutti.** The string voices in the skeleton sit within a few dB of the loudest (median re loudest:
vn1 -1.5, vn2 -4.4, va -2.9, vc 0.0 dB), so the inner voices stay audible under the brass.

## Fixes in this round (why)

* Notes inside the contract compass were silent where no recording reached (Violins I D7-E7, cello A5,
  basses E4-G4, tuba E4-F4): the extreme samples' regions now reach the part's compass
  (`orch_build.key_bounds`), and the renderer still routes such notes to the set with the closest
  sample.
* The two double-bass recordings summed on one held note beat slowly against each other (a held A2
  faded 12 dB in 4 s): the basses play VSCO, with VPO3 only where VSCO has no sample.
* A note only some recordings of a string stack reach keeps the stack's total level (Violins II's top
  octave was 4 dB low).
* The Iowa tuba's pp layer carried hiss that the layer calibration lifted (-13 dB re the note above
  5 kHz): the tuba is low-passed at 3.5 kHz (its ff has nothing above 5 kHz at -43 dB).
* Low notes were tuned on their first second with YIN, which is biased below 80 Hz and misses a
  recording that settles later (held tuba Eb1 -22 c, F#1 +10 c): `tune_orchestra.py` now measures
  sustains 1.0-3.8 s into a 4 s note, from harmonics 2-5 below 80 Hz, and the tuba, bass trombone and
  basses were retuned (median 0.4 c, p95 1.8 c). `evidence/tuning_summary.json` is refreshed from
  `built/tuning_verify.json`: horns, bassoons and cellos were only re-verified with the new low-note
  measure, not retuned (their worst values, vc/vsco 11 c and hn/vsco 5 c, are 0.2 s short-note regions
  below 80 Hz, where the harmonic measure has little to work with).

## Limits

* Upper strings fluctuate inside held notes as their recordings do; the vn1 stack is not worse than
  either recording alone, but it is not a steady modern library sustain.
* Timbre inside a double-bass hairpin barely changes (see above).
* In the skeleton QA a few entries after long rests speak 65-80 ms early (violas, 2 of 3) or 30-60 ms late
  (clarinet at pp); the mix's time base is gated on short notes (`tools/mix.py`), which are aligned.
* Wind chords on one track render but are logged; the orchestration tool keeps winds monophonic.
* `tools/mix.py` on the symphonic skeleton (`out/skeleton_symphonic.mix.json`): attacks against MIDI
  -3.9 ms (357 entries), all notes +0.0 ms; its click scan flags 129 bursts in Climax I, which are the
  bass trombone's ff rasp at E2/Eb2 (bursts every 12 ms = one period; the btbn stem carries the
  energy above 12 kHz there), not splices: the stems' own click scan finds none.
* The tuning corrections and the regenerated SFZ files live in `~/Music/SampleLibraries/Orchestra/built/`
  (outside git); `setup_orchestra.sh --force` rebuilds them from the committed `orch_build.py` and
  `tune_orchestra.py`.
