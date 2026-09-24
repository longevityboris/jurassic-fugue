# Concert-grand renderer

Turns the multi-voice MIDI written by `tools/perform.py` (or any one-voice-per-track
MIDI; in files not written by perform.py, CC11 is expression and CC1 is General
MIDI modulation, which the piano ignores) into a concert-grand recording: Salamander Grand Piano V3 (Yamaha C5, 16
velocity layers) played by sfizz, one stem per voice, convolved with a measured
concert hall (Detmold Konzerthaus). Output is 48 kHz / 24-bit stereo WAV
normalised to -1 dBTP, plus a 256 kb/s AAC `.m4a`. Nothing is played through
the speakers.

## Setup (once)

```sh
./setup_piano.sh            # install what is missing, verify everything (about 6 s when all is present)
./setup_piano.sh --check    # verify only, and HEAD the download URLs
./setup_piano.sh --force    # also rebuild the derived SFZ and the hall IR
```

Assets live outside git in `$PIANO_LIB` (default `~/Music/SampleLibraries`).
The script:

| step | what | verified by |
|---|---|---|
| Salamander V3 | FreePats tarball, 742 MB, extracted to `SalamanderGrandPiano/` | tarball length, SHA-256 of the stock SFZ, manifest hash over all 641 FLAC samples (FreePats publishes no checksum) |
| Detmold IRs | 3 WAVs (Omni, Fig8, DummyHead at seat S1R163) cut out of the 986 MB Zenodo zip with HTTP range requests (`fetch_zip_members.py`, ~3 MB transferred) | pinned SHA-256 |
| sfizz_render | sfizz at commit `f5c6e29`, `sfizz_render_float32.patch` (32-bit float output instead of 16-bit PCM), CMake Release build | renders a sine test and must write IEEE float at 48 kHz |
| derived SFZ | `make_sfz.py`: onset alignment, L/R time alignment of every note (lossless copies in `samples-aligned/`, 670 MB), continuous velocity-to-loudness calibration, keyboard evenness at every dynamic, stretch tuning key by key, damper release, samples held in RAM | the SFZ header records the SHA-256 of the `make_sfz.py` that wrote it; a different script means a stale instrument, which setup regenerates (and `render_piano.py` refuses); 480 aligned copies present |
| hall IR | `make_ir.py`: Omni + Fig8 decoded as M/S to stereo, direct sound removed, late tail continued per octave band to 3.1 s (the measurement is 1.44 s long, the bass reverberates longer) | the IR's JSON records the SHA-256 of the `make_ir.py` that wrote it; setup rebuilds a stale IR (and `render_piano.py` refuses it) |
| smoke test | two-voice render through `render_piano.py` | render report |

Needs python3 with numpy, scipy, soundfile, mido; git, cmake and a C++ compiler
only if sfizz has to be built; `afconvert` (macOS) for `.m4a`; `ffmpeg` for the
loudness figures in render reports.

## The chain

```sh
# score + performance plan -> MIDI -> piano
python3 ../../tools/perform.py SCORE.ly PLAN.json out/x.mid --target piano
python3 render_piano.py out/x.mid -o out/x            # writes out/x.wav, out/x.m4a

# the demo: the old organ fugue (fugue-jp/fugue.ly), pedal part an octave down as a 16' stop
python3 ../../tools/perform.py ../../../fugue.ly plans/fugue_jp.plan.json out/fugue_jp.mid --target piano
python3 render_piano.py out/fugue_jp.mid -o out/fugue_jp_piano --transpose pedal=-12 \
    --stems out/fugue_jp_piano_stems --json out/fugue_jp_piano.render.json

# both dynamics tests, end to end (about 25 s)
./run_tests.sh
```

Useful options (all in `python3 render_piano.py --help`):

| option | default | meaning |
|---|---|---|
| `--wet-db` | -4 | hall energy relative to the dry piano; -4 gives C80 of about +8 dB, clear enough for counterpoint with the hall audible. -7 is drier, -2 more distant |
| `--transpose VOICE=N` | | shift one voice (name matched case-insensitively) |
| `--dyn-db` | 0 | global dynamic offset, realised as hammer velocity, so timbre follows |
| `--velocity-scale` | auto | `perform` for perform.py files (see below), else `raw` |
| `--cc-dynamics` | auto | `velocity` (min of CC1, CC11), `cc11` (CC11 only), `gain`, `off`; auto: `velocity` for perform.py piano files, `off` for perform.py strings files, `cc11` for any other file |
| `--stems DIR` | | write each voice's dry stem |
| `--json PATH` | | render report: per-voice velocities and levels, key sharing, C80, LUFS, LRA, true peak of WAV and M4A |
| `--jobs` | 4 | parallel sfizz instances; each holds its voice's samples in RAM (about 1 GB for a fugue voice) |
| `--no-fold` | | fail on notes outside A0-C8 instead of folding them back by octaves with a warning |
| `--no-reverb`, `--no-m4a`, `--peak-db`, `--lead-in`, `--quality`, `--keep-temp` | | |

## MIDI contract (summary; full text in the `render_piano.py` docstring)

* **Voices.** One voice per track (or per channel), named by the track name.
  perform.py writes a `tempo` track and then `soprano`, `alto`, `tenor`,
  `bass`/`pedal` on channels 1-4. Tempo maps and tick timing are honoured.
  Two tracks with the same name stay two voices: the second `soprano` becomes
  `soprano.2`, with a warning, and gets its own stem, CC7 fader and
  `--transpose` name.
* **Velocity = hammer velocity.** It picks one of 16 recorded layers (timbre)
  and the level on a calibrated, monotonic curve: pp 30, p 42, mp 63, mf 86,
  f 103, ff 115 (-27, -21, -15, -10, -6, -3 dB re 127; `suggested_velocities`
  in the calibration JSON).
* **perform.py's velocity scale.** perform.py writes pp 32, p 44, mp 56,
  mf 68, f 82, ff 98. Played raw, its f would be this piano's mf-, and the
  chain test's pp-ff span shrinks from 22.1 dB to 16.8 dB. `--velocity-scale
  perform` maps its anchors piecewise-linearly onto the calibrated ones (read
  from the calibration JSON). perform.py now tags its files
  with a text meta event `perform.py target=piano|strings`, so `auto` does
  this by itself. (This one-line marker is the only change the piano renderer
  needed in perform.py; other consumers ignore it.)
* **CC11 (and CC1 in perform.py files)** = dynamics envelope: the value at
  each note-on becomes a different hammer velocity (40·log10(cc/127) dB), not
  a fader (unless `--cc-dynamics gain`), so the timbre follows. Which
  controllers count depends on who wrote the file (`--cc-dynamics auto`):
  * perform.py `--target piano`: the lower of CC1 and CC11 (perform.py uses
    both for dynamics; its piano files send neither, so velocity carries the
    dynamics).
  * perform.py `--target strings`: none. These files carry the dynamic in the
    velocities *and* in CC1/CC11, so the CCs are ignored rather than applied
    twice. For the piano, use `--target piano`.
  * any other file: CC11 only. In General MIDI, CC1 is modulation, and a GM
    reset sends CC1=0; read as dynamics it would play every note at velocity 1.
  A voice whose mean velocity the controllers pull below 10 (from 30 or more),
  and a render that needs more than +20 dB of make-up gain, are warned about
  and listed under `warnings` in the render report.
* **CC7** = static per-voice fader (100 = 0 dB). **CC64** = the one sustain
  pedal (any track).
* **One keyboard.** Two voices striking one key less than 30 ms apart (a
  notated unison; perform.py's humanising and melody lead spread those over
  0-20 ms) play one hammer blow at the earlier onset and the stronger
  velocity. A key struck by one voice while another holds it is re-struck: the
  earlier note is released 15 ms before.
* **Range and odd events.** Notes outside A0-C8 (for example after
  `--transpose`) are folded back by octaves with a warning and counted in the
  report (`folded_notes`); `--no-fold` makes them an error. A note-on and
  note-off on the same tick is played as a 10 ms touch of the key; a note-on
  without a note-off sounds for 1 s. Both are warned about and counted per
  voice.

## Evidence: dynamics change timbre, not just gain

Two tests. `make_test_midi.py` writes calibrated velocities directly (what the
instrument can do). `make_chain_test.py` writes only a score and a plan
(`tests/`) and lets perform.py produce the MIDI (what the chain delivers). In
each, the same phrase (theme bars 1-4 over a bass line) is played pp, mf and ff.
RMS is of the final render; centroid and HF ratio (energy above 2 kHz relative
to the total) are of the dry stems. Gain changes neither the centroid nor the
HF ratio, because both are ratios within one spectrum.

| test | segment | RMS dBFS | centroid Hz | HF>2k dB | 4 kHz band after gain-matching to ff |
|---|---|---|---|---|---|
| direct | pp (vel 30) | -41.0 | 298 | -44.4 | -24.2 dB |
| direct | mf (vel 86) | -24.9 | 397 | -26.2 | -3.0 dB |
| direct | ff (vel 115) | -17.9 | 429 | -23.1 | 0 |
| chain | pp (plan pp) | -39.7 | 279 | -42.8 | -22.3 dB |
| chain | mf (plan mf) | -24.7 | 378 | -26.4 | -3.1 dB |
| chain | ff (plan ff) | -17.5 | 415 | -23.4 | 0 |

Brought up to the ff level, the pp phrase is still 22-24 dB darker at 4 kHz
and 28-30 dB darker at 8 kHz. A pure gain change would leave every band at 0.

Crescendo / diminuendo, constant pitch so that pitch does not affect timbre:

| ramp | control | level span | HF-ratio span | corr(level, control) | monotonic |
|---|---|---|---|---|---|
| direct, repeated chord, 29 hits | velocity 18-120-18 | 27.5 dB | 29.1 dB | 0.992 | yes, no step against the ramp |
| direct, same chord at velocity 120 | CC11 36-127-36 | 20.2 dB | 13.6 dB | 0.990 | yes |
| chain, repeated bar of eighths, per half bar | plan pp-ff-pp hairpin | 21.5 dB | 15.3 dB | 0.987 | yes |

The CC11 ramp keeps the note velocity at 120 throughout and still moves the HF
ratio by 13.6 dB between the softest and loudest chord, so expression is
realised as hammer velocity rather than as a fader. Voicing: raising the tenor
from 60 to 80 while the others drop to 56 moves it from +2.5 dB to +7.3 dB
above the other voices, and its centroid from 360 to 378 Hz.

With `--velocity-scale raw` the chain test spans only 16.8 dB from pp to ff
(-34.5 to -17.7 dBFS), instead of 22.1 dB.

## Instrument fixes and how they were measured

An adversarial QA pass (`qa/`, results in `qa/results/*.json`) found ten
defects; all are fixed and re-measured with the same scripts.

| defect | fix | before -> after |
|---|---|---|
| sfizz_render's disk streaming sometimes fell behind the 8192-frame preload and dropped a held note 160-180 ms after its onset (3 of 8 renders) | `<control> hint_ram_based=1` in the derived SFZ; each stem gets a copy pruned to the regions its keys can trigger (1.06 GB instead of 2.97 GB, bit-identical audio); every stem is scanned for a >25 dB drop while a key is held or pedalled, rendered again, then the render fails | 3 concurrent demo renders plus the shipped one (16 stems, load about 250): 0 truncations, all stems sample-identical (`qa/results/truncation_after_fix.json`); `truncation_check` in every report |
| fixed 1 s damper release everywhere: fast passages and the bass blurred | 0.35 s from F2 up, 0.5-0.375 s below (per region); F6-C8 keep 5 s | previous 16th in the first 100 ms of the next (q66/100/132): bass -8.7/-7.5/-7.0 -> -16.4/-15.0/-14.4 dB, tenor -10.5/-9.1/-8.0 -> -19.5/-18.3/-17.1 dB |
| unisons merged only within 5 ms; perform.py spreads them over 0-20 ms, so most became a 10 ms stub plus a restrike | 30 ms window, one blow at the earlier onset with the stronger velocity | offsets 0-25 ms: RMS equal to a single note (was up to +2.6 dB) |
| spaced-pair samples: many notes anti-phase between L and R | one inter-channel delay per note (<= 3 ms, same for all layers) from the layer-averaged cross-correlation; lossless aligned copies | 440 isolated notes: correlation min -0.87 -> +0.19, 133 -> 0 anti-phase; mono loss worst -9.1 -> -2.3 dB; demo mix correlation -0.01 -> +0.47, mono -3.05 -> -1.36 dB |
| evenness smoothed at velocity 80 only; soft layers 3-5 dB off | keyboard trend fitted at 13 velocities, corrected within +/-4 dB | max key deviation from the trend: v20 7.4 -> 3.4, v30 5.4 -> 1.4, v45 3.7 -> 1.3, v70 0.95 -> 0.36, v110 1.5 -> 0.24 dB |
| zero-length note paired with the next note-off of its key | orphan note-off consumed by the note-on on the same tick; 10 ms touch | C4 0.50-0.51, E4, C4 1.40-1.65 as written |
| notes pushed off the keyboard folded silently | warning, `folded_notes` in the report, `--no-fold` | warning printed |
| 8-12 cent stretch steps between sample groups in the top octave; C8 measured on a band edge | `pitch_keytrack` = 100 + local stretch slope per region; prominence-checked peaks, unison clusters averaged, bass judged by partials 2-3 | largest semitone step 11.9 -> 3.9 cents; every key within 3.2 cents of a smooth curve (was 12.0); worst bass octave 14.8 -> 8.0 cents wide |
| documentation drift | this README, the docstrings and `run_tests.sh` re-measured | |
| no attribution in the files | WAV RIFF INFO (title, artist, comment, copyright, software); M4A tags via an ffmpeg remux with the audio copied | M4A decodes sample-aligned with the WAV (lag 0), true peak unchanged, 250 trailing samples of silence (-121 dBFS) |

## Demo

`out/fugue_jp_piano.{wav,m4a}` (not in git): the four-voice organ fugue on the
Jurassic Park theme (`fugue-jp/fugue.ly`), plan `plans/fugue_jp.plan.json`.
It opens pp with the alto subject alone and grows as the voices enter. The
episodes ease back, Episode 4 (bars 22-25, pedal returns) crescendos to f at
the three-voice stretto (bar 26), and the final pedal entry rises to ff. There
is a rit. into the last bar and a fermata. Subject and answer entries are
voiced +12 (perform.py units), countersubjects +3, the theme quotation in
Episode 3 +5, free voices -5. In the stretto each entry is a subject for its
first bar only and its tail then recedes with the free voices, so that every
new head is heard over the previous one. Quarter = 66, 141 s.

Measured (`out/fugue_jp_piano.render.json`): -19.0 LUFS integrated, loudness
range 22.1 LU (the pp opening sits near -40 LUFS, the close near -14.5),
true peak -1.0 dBTP in both WAV and M4A, C80 +8.4 dB. The four stems sit
within 0.7 dB of each other in RMS. Stereo: L/R correlation +0.47 in the mix
(+0.56 dry), mono fold-down -1.4 dB (worst second -2.3 dB). The soprano sits
7.3 dB to the right and the pedal 2.7 dB to the left: the treble-right,
bass-left image of the recording, heard from the keyboard. No stem needed a
second render (`truncation_check`). Each of the 13 subject and answer entries
sits 0.4-6.6 dB above the loudest other voice and 2.5-9.8 dB above their mean
during its first bar (`qa/results/mix.json`; with the earlier +9/-4 voicing
some entries were 0.2-0.3 dB above, and the stretto 1.3 dB).

`out/fugue_organmidi.json` is the earlier render of LilyPond's own flat MIDI
(every note velocity 90, no plan), kept for comparison.

## Files

| file | role |
|---|---|
| `render_piano.py` | the renderer |
| `qa/` | adversarial QA scripts and their results (`qa/results/*.json`); audio goes to `/tmp/pianoqa` |
| `setup_piano.sh`, `fetch_zip_members.py`, `sfizz_render_float32.patch` | installation |
| `make_sfz.py`, `make_ir.py`, `piano_paths.py` | derived instrument, hall IR, shared paths |
| `plans/fugue_jp.plan.json` | demo performance plan |
| `make_test_midi.py`, `make_chain_test.py`, `tests/`, `analyse_dynamics.py`, `run_tests.sh` | dynamics tests |
| `out/*.mid`, `out/*.json` | test and demo MIDI, segment maps, render reports, analyses (audio is not committed) |

## Limits

* A piano cannot swell a held note, and neither can this one: a crescendo is
  successive notes struck harder. CC1/CC11 act at note-on.
* Each voice is rendered by its own sfizz instance, so sympathetic resonance
  between voices under the pedal is not modelled. Half-pedalling is not modelled.
* Each sfizz instance holds its voice's samples in RAM (about 1 GB for a fugue
  voice, up to 3 GB for a voice that spans the keyboard); four run in parallel
  by default.
* The string-resonance and hammer release samples are used as recorded (not
  L/R aligned); they are quiet and short.
* After alignment the image is carried by the level difference between the
  channels. A few notes still correlate weakly (C8 +0.23, F#7 +0.31, D#1 +0.40).
* The Salamander samples decay quickly in the mid register (20-25 dB in the
  first second at A4, as recorded). Long held notes in slow music thin out, as
  on a real C5.
* `--transpose pedal=-12` in the demo is a musical choice (organ pedal at 16'),
  not part of the contract. The lowest note becomes C1.

## Sources and licences

* **Salamander Grand Piano V3**, Alexander Holm, CC-BY 3.0
  (<https://creativecommons.org/licenses/by/3.0/>). FLAC/SFZ packaging by
  FreePats: <https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html>,
  file `SalamanderGrandPiano/SalamanderGrandPiano-SFZ+FLAC-V3+20200602.tar.gz`.
  Renders must credit Alexander Holm; `render_piano.py` writes the credit
  into every WAV (RIFF INFO) and M4A (tags).
* **Open Database of Spatial Room Impulse Responses at Detmold University of
  Music**, S. V. Amengual Gari, B. Sahin, D. Eddy, M. Kob, AES 149th
  Convention (2020), CC-BY 4.0, <https://zenodo.org/records/4116247>
  (`DetmoldSRIR_v01.zip`, md5 `dce94799dbab211b72f537395b3b4e47`).
* **sfizz**, BSD-2-Clause, <https://github.com/sfztools/sfizz>, commit
  `f5c6e29f23b8057867c08e88f5f6ac6738baa30b`, patched locally for float output.
