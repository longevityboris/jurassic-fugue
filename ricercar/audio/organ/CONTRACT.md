# Pipe organ renderer: input contract

`render_organ.py IN.mid [--registration REG.json] -o OUT [--stems DIR] [--no-reverb] [--lead-in SEC]`

This contract is fixed. The instrument behind it (sample set and church) is described in
`README.md`. What a caller writes is: a MIDI file with one voice per track, and optionally a
registration sidecar JSON. Registration can also travel inside the MIDI as text events (section 4).

## 1. Time base

* Standard MIDI file, type 0 or 1, any `ticks_per_beat`. The tempo map is the `set_tempo` meta
  events (any track, usually track 0). Rubato can be written as a tempo map or as note timing.
* Time zero is tick 0. The output begins with `--lead-in` seconds of silence (default 0.5 s)
  and ends when the church's reverberation has decayed to about -60 dB (at most 6 s after the
  last release).
* **Bar:beat positions** in the sidecar are converted with the file's own tick grid:
  quarter-note position `q = (bar - 1) * measure * 4 + (beat - 1)`, tick `= q * ticks_per_beat`.
  `beat` is a 1-based quarter-note beat and can be fractional (`"12:2.5"`); `measure` is the bar
  length in whole notes (default `"1"` = 4/4, as in perform.py plans). perform.py writes every
  note at the tick of its score position (tempo is carried by the tempo map), so bar:beat is
  exact for its files. Alternatives to `"at"`: `"at_tick"` (integer tick) or `"at_sec"`
  (seconds from time zero, after the tempo map).

## 2. Voices, manuals, keys

* **One voice per track or per channel.** Every (track, channel) pair holding notes is a voice,
  named by the track's `track_name` (trimmed, lower-cased). Several channels in one track get
  `.chN` appended. A repeated name becomes `name.2`, `name.3` (warning). No name: `track3`.
  perform.py's `soprano`, `alto`, `tenor`, `bass` are the usual names.
* **A MIDI note number is a KEY, not a sounding pitch.** As on a real organ, the stop's footage
  decides the octave: an 8' stop sounds as written, 16' an octave lower, 4' an octave higher,
  2 2/3' an octave and a fifth higher, mixtures several ranks. Write the bass line at its
  notated pitch and give the pedal a 16' registration to get the 16' octave.
* **Divisions** (keyboards). Callers use these names; each maps to a keyboard of the real
  instrument (README):
  - `HW` Hauptwerk (manual I, main chorus, the loudest),
  - `POS` Positiv / second manual (lighter, placed apart from HW in the church),
  - `PED` Pedal (keys C to f', MIDI 36-65 at most; see the README for the exact compass).
* **Voice-to-division assignment**, in order of precedence: the sidecar's `manual_changes`
  and `manuals` (section 3), `organ:` text events (section 4), else the default by name:
  `soprano`, `alto` -> `HW`; `tenor` -> `POS`; `bass` -> `PED`; any other name -> `HW`.
  A voice can move to another division during the piece (at a rest, like an organist's hand).
* **Compass.** Manual keys MIDI 36-89 (C-f'''), pedal keys MIDI 36-65 (C-f') unless the
  README gives a smaller compass for the chosen instrument. A key outside its division's compass
  is folded by octaves into it, with a warning and a count in the report (`--no-fold`: error).
* **Key sharing.** Two voices on the same division holding the same key play ONE set of pipes
  (as on the instrument): the key sounds from the first press to the last release. No doubling,
  no comb filtering. In stems the sound goes to the voice that pressed first. Counted in the
  report.
* **Repeated notes.** A note-off and a note-on of the same key on the same division re-attack the
  pipe (a new speech transient). A zero-length note is played as a 30 ms touch (warning); a
  note-on with no note-off is closed after 2 s (warning).

## 3. Registration sidecar (`--registration REG.json`)

```json
{
  "measure": "1",
  "manuals": {"soprano": "HW", "alto": "HW", "tenor": "POS", "bass": "PED"},
  "manual_changes": [{"at": "30:1", "voice": "tenor", "division": "HW"}],
  "changes": [
    {"at": "1:1",  "HW": "flute8",       "POS": "flute8",  "PED": "pedal16+8"},
    {"at": "20:1", "HW": "principal8+4"},
    {"at": "26:3", "HW": "plenum",       "PED": "pedal_plenum_reed"}
  ],
  "custom": {"solo_reed": {"stops": ["Trompete 8"]}},
  "enclosed": ["POS"],
  "gain_db": {"bass": 0.0}
}
```

* `changes`: at each position, each listed division switches to the named registration.
  Divisions not listed keep theirs. Before the first change every division uses its default
  (`HW`, `POS`: `principal8`; `PED`: `pedal16+8`).
* **Held keys follow the stops, as on a real organ**: a stop drawn while a key is held starts
  speaking at the change (with its attack), a stop retired while a key is held releases at the
  change (with its release). Put changes at breaths or section joins for clean joins.
* **Named registrations** (the stop lists behind them are in `registrations.json` and the
  README; every name exists on every division type it is listed for):

  | name | manuals `HW` / `POS` | meaning |
  |---|---|---|
  | `flute8` | yes | stopped flute 8' (Gedackt / Rohrflöte) |
  | `flute8+4` | yes | flute 8' + flute 4' |
  | `principal8` | yes | principal 8' |
  | `principal8+4` | yes | principal 8' + octave 4' |
  | `principal8+4+2` | yes | principal 8' + 4' + 2' |
  | `plenum` | yes | principal chorus 8' 4' 2 2/3' 2' + mixture (+16' on HW if present) |
  | `plenum_reed` | yes | `plenum` + trumpet 8' |
  | `reed8` | yes | trumpet 8' (+ flute 8' for body) |

  | name | pedal `PED` | meaning |
  |---|---|---|
  | `pedal16` | yes | subbass 16' |
  | `pedal16+8` | yes | subbass 16' + octave/flute 8' |
  | `pedal16+8+4` | yes | 16' + 8' + 4' |
  | `pedal_plenum` | yes | pedal principal chorus 16' 8' 4' (+ mixture if present) |
  | `pedal_plenum_reed` | yes | `pedal_plenum` + trombone 16' (+ trumpet 8' if present) |
  | `pedal_reed` | yes | trombone 16' + 8' flue |

  Also accepted: `"off"` (division silent), a `custom` name from the sidecar, or an explicit
  list of stop names of that division, e.g. `["Gedackt 8", "Octave 4"]` (names as printed by
  `render_organ.py --list-stops`). An unknown name is an error, not a silent substitute.
* `manuals`: initial voice -> division map (overrides the defaults by name). `manual_changes`:
  moves a voice from a position on.
* `enclosed`: divisions that sit in a swell box (section 5). Default: none.
* `gain_db`: static per-voice mix gain in dB (default 0). For balance only; the organ's
  dynamics are its registration.
* A registration may also be given without MIDI or sidecar positions: `--registration NAME`
  applies one named preset (`demo/` has examples) to the whole file.

## 4. Registration inside the MIDI (optional)

`text` or `marker` meta events on any track whose text starts with `organ:` are read as commands
at their tick, after the sidecar's events at the same tick:

```
organ: HW=plenum PED=pedal_plenum_reed      registration change
organ: tenor->POS                           voice to division
```

## 5. Controllers and other messages

* **Velocity: ignored** (an organ key does not know how fast it was pressed). Velocity 0 is a
  note-off. perform.py's dynamic velocities therefore have no effect; its dynamics must be
  translated into registration changes (the demo plan shows how).
* **CC11 = swell box**, only for voices on a division listed in `enclosed`: 127 open, 0 closed.
  The box lowers level (to -18 dB at 0) and highs more than lows (a low-pass sweeping from
  open to about 1.5 kHz), smoothed over 60 ms, so a crescendo changes timbre as well as level.
  On divisions that are not enclosed CC11 is ignored.
* Ignored: program change (perform.py writes one per channel), CC1, CC7, CC64, CC10, pitch bend,
  aftertouch, sysex.

## 6. Output

* `OUT.wav`: 48 kHz, 24-bit, stereo, true peak normalised to -1 dBTP (`--peak-db`), church
  reverberation by convolution (`--no-reverb`: dry). `OUT.m4a`: AAC 256 kb/s (afconvert).
  One normalisation gain for the whole file, so registration contrasts are kept.
* `--stems DIR`: one dry 48 kHz 24-bit stereo WAV per voice (`DIR/<voice>.wav`), same time base
  and length as the mix, at the mix's pre-reverb gain (sum of stems = dry mix before the
  common normalisation gain, which is written into the report).
* `--json PATH`: report (voices, divisions, registration timeline in seconds, folded and shared
  keys, per-voice levels, reverb C80, loudness, true peak, warnings).
* Nothing is played through the speakers.
