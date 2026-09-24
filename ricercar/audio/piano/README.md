# Concert-grand renderer

Turns the multi-voice MIDI written by `tools/perform.py` (or any one-voice-per-track
MIDI) into a concert-grand recording: Salamander Grand Piano V3 (Yamaha C5, 16
velocity layers) played by sfizz, one stem per voice, convolved with a measured
concert hall (Detmold Konzerthaus). Output is 48 kHz / 24-bit stereo WAV
normalised to -1 dBTP, plus a 256 kb/s AAC `.m4a`. Nothing is played through
the speakers.

## Setup (once)

```sh
./setup_piano.sh            # install what is missing, verify everything (5 s when all is present)
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
| derived SFZ | `make_sfz.py`: onset alignment, continuous velocity-to-loudness calibration, keyboard evenness, tuning smoothing | files present |
| hall IR | `make_ir.py`: Omni + Fig8 decoded as M/S to stereo, direct sound removed | files present |
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

# both dynamics tests, end to end (about 15 s)
./run_tests.sh
```

Useful options (all in `python3 render_piano.py --help`):

| option | default | meaning |
|---|---|---|
| `--wet-db` | -4 | hall energy relative to the dry piano; -4 gives C80 of about +8 dB, clear enough for counterpoint with the hall audible. -7 is drier, -2 more distant |
| `--transpose VOICE=N` | | shift one voice (name matched case-insensitively) |
| `--dyn-db` | 0 | global dynamic offset, realised as hammer velocity, so timbre follows |
| `--velocity-scale` | auto | `perform` for perform.py files (see below), else `raw` |
| `--cc-dynamics` | auto | `velocity`, `gain`, `off`; `off` for perform.py strings-target files |
| `--stems DIR` | | write each voice's dry stem |
| `--json PATH` | | render report: per-voice velocities and levels, key sharing, C80, LUFS, LRA, true peak of WAV and M4A |
| `--no-reverb`, `--no-m4a`, `--peak-db`, `--lead-in`, `--quality`, `--keep-temp` | | |

## MIDI contract (summary; full text in the `render_piano.py` docstring)

* **Voices.** One voice per track (or per channel), named by the track name.
  perform.py writes a `tempo` track and then `soprano`, `alto`, `tenor`,
  `bass`/`pedal` on channels 1-4. Tempo maps and tick timing are honoured.
* **Velocity = hammer velocity.** It picks one of 16 recorded layers (timbre)
  and the level on a calibrated, monotonic curve: pp 29, p 42, mp 64, mf 86,
  f 103, ff 115 (-27, -21, -15, -10, -6, -3 dB re 127).
* **perform.py's velocity scale.** perform.py writes pp 32, p 44, mp 56,
  mf 68, f 82, ff 98. Played raw, its f would be this piano's mf- and pp-ff
  would shrink to about 16 dB. `--velocity-scale perform` maps its anchors
  piecewise-linearly onto the calibrated ones. perform.py now tags its files
  with a text meta event `perform.py target=piano|strings`, so `auto` does
  this by itself. (This one-line marker is the only change the piano renderer
  needed in perform.py; other consumers ignore it.)
* **CC1 / CC11** = dynamics envelope: the lower of the two at each note-on
  becomes a different hammer velocity (40·log10(cc/127) dB), not a fader
  (unless `--cc-dynamics gain`), so the timbre follows. perform.py's `--target strings` files carry the
  dynamic in the velocities *and* in CC1/CC11; `auto` ignores the CCs there so
  it is not applied twice. For the piano, use `--target piano`.
* **CC7** = static per-voice fader (100 = 0 dB). **CC64** = the one sustain
  pedal (any track). **One keyboard**: a key struck by two voices is re-struck,
  and unisons become one hammer blow.

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
| direct | pp (vel 29) | -39.5 | 265 | -42.3 | -24.1 dB |
| direct | mf (vel 86) | -23.8 | 339 | -24.0 | -3.2 dB |
| direct | ff (vel 115) | -16.7 | 374 | -20.3 | 0 |
| chain | pp (plan pp) | -38.1 | 259 | -40.1 | -21.1 dB |
| chain | mf (plan mf) | -23.7 | 325 | -24.4 | -3.3 dB |
| chain | ff (plan ff) | -16.5 | 362 | -20.8 | 0 |

Brought up to the ff level, the pp phrase is still 21-24 dB darker at 4 kHz
and 27-29 dB darker at 8 kHz. A pure gain change would leave every band at 0.

Crescendo / diminuendo, constant pitch so that pitch does not affect timbre:

| ramp | control | level span | HF-ratio span | corr(level, control) | monotonic |
|---|---|---|---|---|---|
| direct, repeated chord, 29 hits | velocity 18-120-18 | 27.9 dB | 30.5 dB | 0.993 | yes, no step against the ramp |
| direct, same chord at velocity 120 | CC11 36-127-36 | 22.1 dB | 11.3 dB | 0.984 | yes |
| chain, repeated bar of eighths, per half bar | plan pp-ff-pp hairpin | 22.4 dB | 19.1 dB | 0.988 | yes |

The CC11 ramp keeps the note velocity at 120 throughout and still moves the HF
ratio by 10.4 dB between the softest and loudest chord, so expression is
realised as hammer velocity rather than as a fader. Voicing: raising the tenor
from 60 to 80 while the others drop to 56 moves it from +1.7 dB to +7.3 dB
above the other voices, and its centroid from 405 to 432 Hz.

With `--velocity-scale raw` the chain test spans only 16.1 dB from pp to ff
(-32.6 to -16.5 dBFS), instead of 21.6 dB.

## Demo

`out/fugue_jp_piano.{wav,m4a}` (not in git): the four-voice organ fugue on the
Jurassic Park theme (`fugue-jp/fugue.ly`), plan `plans/fugue_jp.plan.json`.
It opens pp with the alto subject alone and grows as the voices enter. The
episodes ease back, Episode 4 (bars 22-25, pedal returns) crescendos to f at
the three-voice stretto (bar 26), and the final pedal entry rises to ff. There
is a rit. into the last bar and a fermata. Subject and answer entries are
voiced +9 (perform.py units), countersubjects +3, the theme quotation in
Episode 3 +5, free voices -4. Quarter = 66, 141 s.

Measured (`out/fugue_jp_piano.render.json`): -18.2 LUFS integrated, loudness
range 22 LU (the pp opening sits near -39 LUFS, the close near -14),
true peak -1.0 dBTP in both WAV and M4A, C80 +8.4 dB. The four stems sit
within 1 dB of each other in RMS.

`out/fugue_organmidi.json` is the earlier render of LilyPond's own flat MIDI
(every note velocity 90, no plan), kept for comparison.

## Files

| file | role |
|---|---|
| `render_piano.py` | the renderer |
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
  Renders must credit Alexander Holm.
* **Open Database of Spatial Room Impulse Responses at Detmold University of
  Music**, S. V. Amengual Gari, B. Sahin, D. Eddy, M. Kob, AES 149th
  Convention (2020), CC-BY 4.0, <https://zenodo.org/records/4116247>
  (`DetmoldSRIR_v01.zip`, md5 `dce94799dbab211b72f537395b3b4e47`).
* **sfizz**, BSD-2-Clause, <https://github.com/sfztools/sfizz>, commit
  `f5c6e29f23b8057867c08e88f5f6ac6738baa30b`, patched locally for float output.
