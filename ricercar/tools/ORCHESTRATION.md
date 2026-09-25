# Orchestration and ensemble mix

Two tools turn the four-voice score into ensemble recordings:

```sh
# score + performance plan + orchestration spec -> one MIDI per renderer group (+ manifest, integrity check)
python3 tools/orchestrate.py SCORE.ly PLAN.json ORCH.json OUTDIR
# render every group, align, place in one hall, master -> WAV + m4a
python3 tools/mix.py OUTDIR/manifest.json
```

The demo (piano quintet on the skeleton):

```sh
python3 tools/orchestrate.py design/final-lab/SK_final.ly design/final-lab/plan.json \
        orchestration/quintet_skeleton.json orchestration/out/skeleton_quintet
python3 tools/mix.py orchestration/out/skeleton_quintet/manifest.json
#   -> orchestration/out/skeleton_quintet.wav, .m4a, .mix.json (report)
```

`python3 tools/orchestrate.py ... OUTDIR --check` re-runs only the integrity check on existing output.
`orchestration/tests/test_orchestrate.py` runs the checker's mutation tests and the contract checks.

## 1. What orchestrate.py does

* It imports `perform.py` and runs it once per renderer target on the same plan: `--target piano`
  velocities for the piano (and the organ), `--target strings` CC1/CC11 envelopes and accent
  velocities for bowed and wind parts. perform.py's timing (tempo map, breaths, fermatas, humanised
  onsets, melody lead) does not depend on the target, and orchestrate.py checks this: every group
  file gets the same tempo track and ticks per quarter (960), and a note doubled in two groups
  starts on the same tick in both.
* Each performed note is matched to its score note (lyparse). The spec's windows route notes to
  parts by their **notated start**: a note belongs to the window `[at, until)` that contains its
  start. A note held across a hand-off stays with the part that started it; if that part's next
  window starts before the note ends, the held note is shortened to the new note (reported).
* Nothing is composed: every part note is a score note of the assigned voice, moved by whole
  octaves only (`octave` -24, -12, 0, +12, +24). Derived pedal points (below) hold a pitch that the
  source voice itself holds.
* Each group's MIDI follows its renderer's own contract (section 4) and keeps perform.py's
  `perform.py target=...` marker in the tempo track (the piano and quartet renderers pick their
  velocity scale and CC meaning from it), plus an `orchestrate.py group=...` text event.

## 2. The spec (ORCH.json)

```json
{
 "title": "...",
 "groups": {
  "quartet": {"renderer": "quartet", "parts": ["vn1", "vn2", "va", "vc"]},
  "piano":   {"renderer": "piano",
              "parts": ["soprano", "alto", "tenor", "bass", "soprano_8va", "bass_8vb", "pedal_8vb"],
              "options": {"pedal": [{"at": "46:1", "until": "50:4", "every": "half"}]}}
 },
 "assignments": [
  {"voice": "soprano", "part": "vn1", "at": "1:1", "until": "35:1"},
  {"voice": "alto", "part": "va", "at": "9:4", "until": "13:1"},
  {"voice": "soprano", "part": "soprano_8va", "at": "48:1", "until": "59:1", "octave": 12, "level": -1}
 ],
 "pedal_points": [
  {"voice": "bass", "part": "pedal_8vb", "at": "42:1", "until": "46:1", "octave": -12, "bridge": 1}
 ],
 "allow_uncovered": [],
 "mix": {"lead_in": 0.5, "reference_group": "quartet",
         "groups": {"quartet": {"wet_db": -4}, "piano": {"wet_db": -3, "stage": {"*": {"az": 0, "depth": 1.2}}}}}
}
```

Positions are perform.py's `"bar:beat"` (quarter-note beats, 1-based, fractions allowed), `"end"`,
or a **mark**: `"MARK"`, `"MARK+N"`, `"MARK-N"`, `"MARK+N:beat"` (N bars after the mark, then the beat
in that bar). `at` defaults to `"1:1"`, `until` to `"end"`. Marks come from the spec:

```json
"marks": {"from": "../design/final-lab/piece.py", "tutti": "50:1"}
```

`from` (relative to the spec) reads section lengths: a Python file with `SECTIONS = [{"id", "bars"},
...]` (the skeleton's `piece.py`), a JSON list of the same, or a JSON `{name: "bar:beat"}`. Each
section's first bar becomes a mark under its id and without its `secNN_` prefix (`sec05_inversa`
and `inversa`). If the sections do not add up to the score's length, orchestrate.py stops: the
score and the section list disagree. Other keys are explicit marks. The demo spec uses marks only,
so its scoring follows the form when the composer inserts bars (the skeleton grew from 62 to 66
bars while the demo was being made, and the spec did not change). Positions in group options (piano
pedal spans, organ registration changes) and in `allow_uncovered` may use marks too; they are
rewritten as `bar:beat` for perform.py and the organ. `orchestration.json` lists every mark with its
bar and time.

### groups

| key | meaning |
|---|---|
| `renderer` | `piano`, `quartet`, `orchestra` or `organ` (default: the group's name) |
| `parts` | list of part names, or `{part: {options}}`. Part names are unique across groups; an assignment may also say `"group.part"` |
| `options` | per-renderer options (below) |
| `plan_overrides` | plan keys replaced for this group's perform.py run (`dynamics`, `role_boost`, `role_level`, `pedal`, ...). Timing keys (`tempo`, `fermatas`, `breaths`, `measure`, `voices`, `humanize`) are refused: all groups share one time base |

Part options and group options by renderer:

| renderer | part name / part options | group options |
|---|---|---|
| `piano` | the track (voice) name the piano renders as a stem; `track`, `program` | `pedal`: `"plan"` (default: the plan's pedal), `"none"`, or a list of perform.py pedal spans `{"at", "until", "every": "bar" \| "half"}`. Pedal changes where the piano rests are dropped (no pedal noise while it is silent) |
| `quartet` | an instrument id `vn1 vn2 va vc cb`, or `{"instrument": id}`; tracks are named "Violin I", "Violin II", "Viola", "Cello", "Contrabass" | |
| `orchestra` | the track name: a part id with an optional tag (`fl`, `hn.1`, `vc.div`, `fl:oct`); `{"part": id}` for other names; `divisi: true` allows chords; `gain_db`, `players` (`solo`, `a2`, `a4`), `pan`, `depth_m`, `width` go into the sidecar | `sidecar`: the base of `<group>.orchestra.json` (`hall`, `seating`, `tracks`) |
| `organ` | the track name (lower-cased); `division` `HW`, `POS` or `PED` (default by name: soprano, alto: HW, tenor: POS, bass: PED) | `registration`: the sidecar of `audio/organ/CONTRACT.md` section 3 (`changes`, `manual_changes`, `custom`, `enclosed`, `gain_db`); `manuals` and `measure` are filled in. `swell: true`: the plan's dynamic envelope drives the swell box (CC11; `enclosed` defaults to `["POS"]`) |

### assignments (lines)

| key | default | meaning |
|---|---|---|
| `voice` | | `soprano`, `alto`, `tenor`, `bass` (the plan's voices) |
| `part` | | who plays it |
| `at`, `until` | `1:1`, `end` | the window, by notated start |
| `octave` | 0 | -24, -12, 0, +12, +24 semitones: an octave doubling or a transposed hand-off |
| `level` | 0 | dynamic steps added to the plan's level (1 = p to mp). Piano: a different hammer velocity through perform.py's level curve (so timbre follows); bowed and wind parts: CC1/CC11 + 13 per step (layer and brightness follow); organ: none (use registration) |
| `accent` | 0 | velocity offset in perform.py units (piano: level; bowed: attack bite) |
| `articulation` | `auto` | `legato`/`slur`, `detache`/`normal`/`tenuto`, `short`/`staccato`/`spiccato`, and `roll`/`stroke` (timpani). Quartet and orchestra: CC20 per note (once a part has a hint, every note of it gets a CC20 value, with the renderers' own inference for `auto` notes, because the renderers stop inferring when a track carries CC20). Piano: `short` halves the sounding length, `legato` overlaps the next note by 40 ticks |
| `players` | | orchestra winds and brass: `solo`, `a2`, `a4` (CC16 at each note) |

Rules: one part plays one window at a time (overlapping windows on a part are an error; split
them). A voice may be played by any number of parts at once (doubling), by none (a rest: it must
then be listed in `allow_uncovered`, see below), and may move from part to part at any beat
(hand-offs, Klangfarben). Single-line parts (quartet, orchestra without `divisi`) may not receive
two notes starting together.

### pedal_points (derived sustained parts)

`{"voice", "part", "at", "until", "octave", "level", "articulation", "mode", "bridge", "min_beats", "pitch", "rate"}`

The part holds the pitch the voice sustains in the window (`pitch`: `"auto"` = the pitch held
longest, or a MIDI number the voice sounds there), from the first note of that pitch to the end
of the last one, merged over repeated notes and bridged over other notes no longer than `bridge`
beats (default 1: neighbour notes). Runs shorter than `min_beats` (default 2) are dropped. `mode`:
`sustain` (one held note; on `timp` a roll by the orchestra renderer's rule, or say
`"articulation": "roll"`), or `repeat` (re-struck `rate` times per second). The demo holds the
bass's dominant pedal F an octave down in the piano (42-45) under the cello's line with its
G-flat neighbours.

### allow_uncovered

`[{"voice": "tenor", "at": "44:1", "until": "46:1"}]`: score notes deliberately played by no part.
Without it, a score note that no part plays fails the integrity check.

## 3. Integrity check

Written to `OUTDIR/integrity.json`; the exit code is 1 if it fails. It re-reads the score with
lyparse and the written MIDI files with mido (independently of the routing code) and checks:

* every note of every part is a note of its assigned voice, at the same notated onset (within
  the humanising tolerance, 60 ticks or a third of the shortest note) and at pitch + the declared
  octave; nothing is missing and nothing is extra; no note lasts past its notated end;
* every score note is played by some part (unless allowed);
* pedal-point notes sound a pitch the voice holds, start on one of its notes, end with its last
  note of that pitch, and bridge only stretches no longer than `bridge`;
* no hanging note-ons, no re-struck held keys, single-line parts stay single lines (perform.py's
  own legato overlap of a few ms is allowed);
* all group files have the same tempo map and ticks per quarter;
* notes outside an instrument's compass (from the renderers' tables) are warnings.

`orchestration/tests/test_orchestrate.py` plants errors in clean output (a semitone, an undeclared
octave, a dropped note, an added note, a hanging note, a tempo change, an uncovered window, a
pedal held past its pedal, bad specs) and checks that each one is caught, and checks the contract
details (markers, track names, pedal only where the piano plays, CC20 on every note once hinted,
the viola's CC1 following the alto and then the tenor across a hand-off, a level of -1 lowering
piano velocities by one dynamic step, shared onset ticks in doublings): 24/24 pass
(`tests/results/orchestrate_tests.json`).

## 4. Renderer contracts used

| group | perform.py target | tracks | controllers written | sidecar |
|---|---|---|---|---|
| piano (`audio/piano/README.md`) | piano | one per part (stems by track name) | velocity; CC64 on the first track | |
| quartet (`audio/strings/README.md`) | strings | Violin I, Violin II, Viola, Cello, Contrabass | CC1 = CC11 envelope of the voice being played (+13 x level); velocity = accent; CC20 when hinted | |
| orchestra (`audio/orchestra/CONTRACT.md`) | strings | part ids (`fl`, `hn.1`, `vn1`, `timp`, ...), concert pitch | CC1/CC11 as above; CC16 players; CC20 (timpani: roll/stroke) | `<group>.orchestra.json` |
| organ (`audio/organ/CONTRACT.md`) | piano (strings with `swell`) | lower-cased part names | CC11 swell only with `swell` | `<group>.registration.json` |

While a bowed or wind part rests, its envelope follows its next window, so the right dynamic
layer is already in place at its entry.

## 5. The manifest and mix.py

orchestrate.py writes `OUTDIR/manifest.json` from the spec's `mix` section:

```json
{"title": "...", "out": "../skeleton_quintet", "lead_in": 0.5, "peak_dbtp": -1.0, "hall": "detmold",
 "reference_group": "quartet",
 "groups": {"quartet": {"renderer": "quartet", "midi": "quartet.mid", "parts": {...},
                        "gain_db": 0, "wet_db": -4, "stage": {"vn1": {"az": 30, "depth": 0}}},
            "piano": {"renderer": "piano", "midi": "piano.mid", "parts": {...}, "gain_db": 0, "wet_db": -3,
                      "stage": {"*": {"az": 0, "depth": 1.2, "width": 0.7}}, "render_args": ["--jobs", "2"]}}}
```

| key | meaning |
|---|---|
| `out` | output path without extension, relative to the manifest (`.wav`, `.m4a`, `.mix.json`) |
| `lead_in` | seconds of silence before MIDI time 0 in the mix (and passed to every renderer) |
| `reference_group` | the group whose calibration level the others are levelled to |
| `groups.<g>.gain_db` | balance trim after calibration |
| `groups.<g>.hall_re_dry_db` | hall energy re this group's dry sound, **measured on this music** (the reverb is computed at unit gain, measured, and scaled). Portable between instruments: at the same impulse-referenced level the piano's hall is about 2.5 dB stronger than the quartet's, because its energy sits where the hall rings longest. The quartet renderer's own default (`--wet -4`) is +4.2 dB on this piece; the demo gives both groups +4 dB |
| `groups.<g>.wet_db` | used when `hall_re_dry_db` is absent: hall energy re the dry sound for an impulse (`hall.py` convention, default -4) |
| `groups.<g>.stage` | per stem seat: keys part, track, instrument or `"*"`; `az` (degrees, + = left), `depth` (m behind the front; adds 1/343 s per m and -1 dB/m), `width` (share of the stem's own stereo width). Quartet defaults: its renderer's seats; piano: centre, 1.2 m back. Orchestra stems come seated by their renderer |
| `groups.<g>.render_args` | extra arguments for that renderer |
| `groups.<g>.latency_ms` | shift the group earlier by this many ms, or `"auto"` (its measured lag re the reference group). Default 0: nothing is shifted |

**Rendering.** One group at a time, dry stems and no reverb, into `OUTDIR/render/<group>/`; a
render is reused while its MIDI, sidecar, renderer script and arguments are unchanged
(`--rerender` forces it).

**Time base.** Every stem is placed so that its sample 0 is MIDI time `-lead_in`: the piano and
the organ start their output at MIDI time `-lead_in`; the quartet and the orchestra report
`offset_s` (MIDI time of their first sample). No stretch or resampling: offsets are whole samples.

**Levels.** The quartet normalises its stems with its mix; mix.py undoes that from the report's
pre-normalisation stem levels (the four instruments give the same gain within 0.01 dB). The piano
and organ stems and the orchestra's are pre-normalisation by contract. The renderers are then
levelled against each other with a **calibration chorale**: `orchestration/calibration/chorale.ly`
(eight bars of four-part B-flat major at mf, `chorale.plan.json`) goes through orchestrate.py and
each renderer, seated as in the mix; the K-weighted loudness of each (`calibration.json`, cached
per renderer script, orchestrate.py and mix.py hash) sets a gain so that an mf chorale is equally
loud on every renderer. `gain_db` is applied on top. So the scoring changes the balance the way
it would on stage (a doubled line is louder, a solo softer), and nothing depends on how loud a
group happens to be where it plays.

**Alignment check.** Before placement (depth delays are physical), mix.py computes an onset
envelope (1 ms frames, log-energy rises in four bands) of every stem and cross-correlates it with
an impulse train at the times at which that stem's renderer starts an attack; the curves of a
group's stems are summed and the peak is the group's lag. The difference between groups must be
under `--max-lag-ms` (5 ms) or the mix stops. Attack times per renderer:

* piano: every note-on (its samples are onset-aligned to 0.2 ms);
* quartet: new-bow and short strokes at their note-on (the renderer starts a stroke's bow pre-roll
  15 ms early so that the stroke lands on the note-on); slurred notes are left out, because they
  enter by a crossfade whose envelope peak depends on register (the cello's slurs peak up to 17 ms
  late, the violins' within 2 ms), which is articulation, not time base;
* orchestra, organ: notes after at least 100 ms of silence in their part (until their reports
  give articulation).

Reported alongside, for information: the lag per quarter of the piece, the lag over every note of
the group's summed envelope, notes after silence, and where groups play the same onsets
(doublings) the direct cross-correlation of their two envelopes, masked to +-60 ms around the
shared onsets. Numbers: `groups.<g>.alignment`, `inter_group`.

**Hall.** `audio/strings/hall.py` (shared with the quartet renderer): `place_dry` seats each stem
(constant-power pan, width, depth delay and attenuation) and `Hall("detmold")` is the measured
Detmold Konzerthaus response (the piano's `make_ir.py` output, tail continued to 3.5 s, unit
energy; sources on the right use the mirrored response). Each group's stems are summed per side
and convolved once at the group's wet level.

**Master and report.** 18 Hz high-pass, tail trimmed at -80 dB with a 0.3 s fade, true peak
(4x oversampled) to `peak_dbtp`, 48 kHz 24-bit WAV with the credits in its INFO chunk, AAC
256 kb/s m4a via `afconvert` (decoded and measured; encoded again lower if it overshoots by more
than 0.1 dB). `OUT.mix.json`: per group offsets, gains, calibration, lags, level while playing,
seats, C80; the balance where all groups play; integrated loudness, loudness range, true peak of
WAV and m4a, stereo correlation, mono fold-down, hall re dry, a click scan (1 ms bursts above
12 kHz, 15 dB over their surroundings, away from onsets) and a 5 s loudness curve.
