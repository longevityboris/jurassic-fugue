#!/usr/bin/env python3
"""Render a multi-voice MIDI file on a sampled concert grand in a concert hall.

Usage
-----
::

    python3 render_piano.py IN.mid [-o OUT] [options]

    # the chain: LilyPond score + performance plan -> MIDI -> piano
    python3 ../../tools/perform.py SCORE.ly PLAN.json out/x.mid --target piano
    python3 render_piano.py out/x.mid -o out/x
    # the demo (old organ fugue; its pedal part sounds an octave lower, as a 16' stop)
    python3 ../../tools/perform.py ../../../fugue.ly plans/fugue_jp.plan.json out/fugue_jp.mid --target piano
    python3 render_piano.py out/fugue_jp.mid -o out/fugue_jp_piano --transpose pedal=-12

This writes ``OUT.wav`` (48 kHz, 24-bit stereo, true peak normalised to -1 dBFS)
and ``OUT.m4a`` (AAC 256 kb/s via ``afconvert``). It plays nothing through the
speakers. Run ``setup_piano.sh`` once first (samples, impulse response, sfizz).

Options: ``--wet-db`` (reverb energy relative to the dry piano, default
-4 dB, C80 of about +8 dB: clear enough for counterpoint, with the hall
audible), ``--no-reverb``, ``--ir PATH``,
``--peak-db``, ``--lead-in``, ``--dyn-db`` (global dynamic offset realised
through velocity), ``--transpose VOICE=N``, ``--stems DIR``,
``--velocity-scale auto|raw|perform``, ``--cc-dynamics auto|velocity|gain|off``
(both explained under the MIDI contract), ``--no-key-sharing``, ``--quality`` (sfizz
resampler, 10 = sinc72), ``--jobs``, ``--keep-temp``, ``--no-m4a``,
``--json PATH`` (render report).

Instrument
----------
Salamander Grand Piano V3 (Yamaha C5, 48 kHz/24-bit, 16 velocity layers, hammer
noise and string-resonance release samples, pedal noises) by Alexander Holm,
CC-BY 3.0. The SFZ is re-derived by ``make_sfz.py``: attacks aligned to within
0.2 ms across layers, velocity-to-loudness continuous and monotonic over about
40 dB, keyboard evenness and intonation smoothed. It is played by sfizz
(``sfizz_render``, sinc-72 resampling, 32-bit float output). Keys up to
E6 have dampers: a lifted key stops with the recorded release (1 s exponential
envelope plus the string-resonance and hammer release samples). Keys from
F6 up ring on, as on a real grand.

Room: Detmold Konzerthaus, audience seat 163, coincident omni/figure-8 decoded
to stereo (``make_ir.py``; CC-BY 4.0, Amengual Gari et al., AES 2020). Each
dry channel feeds its own side of the IR (L to L, R to R). A mono feed would
cancel partly, because on some notes the close AB pair is out of phase.

MIDI contract (for the performance script)
------------------------------------------
* **One voice per track, or per channel.** Every (track, channel) pair that
  holds notes becomes a voice, named after the track (``Soprano``,
  ``Alto`` ...). With several channels in one track, ``.chN`` is appended.
  Tempo (``set_tempo`` on any track, usually track 0) and ticks are honoured, so
  rubato may be written as a tempo map or as note timing. Both work.
* **Note velocity = hammer velocity.** This is the main expressive control. It
  selects one of 16 recorded layers (timbre: soft notes are dark, loud notes
  bright and percussive) and sets the level along a calibrated curve. Measured
  levels relative to velocity 127, averaged over C2-C6::

      velocity   12   29   42   64   86  103  115  127
      dB        -33  -27  -21  -15  -10   -6   -3    0
      marking   ppp   pp    p   mp   mf    f   ff  fff

  (exact curve: ``velocity_db`` in the calibration JSON). To bring out a
  voice, raise its velocities by about 8-15 (+3 to +5 dB, brighter).
  A piano cannot swell a held note, so a crescendo means successive notes
  struck harder.
* **Velocity scale.** perform.py writes its own scale (VEL_AT: ppp 22, pp 32,
  p 44, mp 56, mf 68, f 82, ff 98, fff 112). Played raw, its "f" would be this
  piano's mf- and its pp->ff span 18 dB instead of 24. ``--velocity-scale
  perform`` maps it piecewise-linearly onto the calibrated markings above
  (22->12, 32->29, 44->42, 56->64, 68->86, 82->103, 98->115, 112->127);
  accents and voicing offsets between anchors scale with the local slope.
  perform.py marks its files with a ``text`` meta event ``perform.py
  target=piano|strings`` in the tempo track, and the default ``auto`` picks
  ``perform`` for such files and ``raw`` for everything else.
* **CC11 (expression) and CC1 (modulation/dynamics) = dynamics envelope.**
  Default 127 = neutral, and a channel that never sends them is neutral. The
  lower of the two values in force at each note-on moves that note's level by
  ``40*log10(cc/127)`` dB, realised as a **different hammer velocity** through
  the inverse of the calibrated curve, so the timbre follows the dynamic as on
  a real piano. Examples: 64 -> -11.9 dB, 90 -> -6 dB, 107 -> -3 dB. Taking
  the lower value means a strings-style file that writes the same envelope to
  CC1 and CC11 (``perform.py --target strings``) is not counted twice, and
  either controller can be used alone. Notes that are already sounding do not
  change. ``--cc-dynamics gain`` keeps CC1 as velocity but makes CC11 a
  continuous fader, ``off`` ignores both. The default ``auto`` is ``velocity``,
  except for ``perform.py --target strings`` files: their velocities already
  carry the dynamic level, and the CC1/CC11 copy of the same envelope would
  count it twice, so ``auto`` ignores CC1/CC11 there. (For the piano, render
  ``--target piano``; a strings file also works, with string-style
  articulation and without the piano voicing boosts.)
* **CC7 (channel volume) = mixing fader** for that voice's stem, in dB
  ``40*log10(cc7/100)``: default 100 = 0 dB, 127 = +4.2 dB, 71 = -6 dB. It
  is applied continuously with 20 ms smoothing and changes only level, not
  timbre. Use it for static balance. For musical dynamics use velocity/CC11.
* **CC64 (sustain)** on any track is the one sustain pedal of the piano.
  Values >= 64 are down, < 64 up. Half-pedalling is not modelled. Pedal-down and
  pedal-up mechanism noises are played once. Bach needs none, but light
  syncopated pedalling works.
* **One keyboard.** Voices share one physical piano. If a voice strikes a key
  that another voice is still holding, the key is re-struck: the earlier note
  is cut 15 ms before, and the key stays down as long as either voice holds it.
  Unisons struck together (within 5 ms) become one note at the higher
  velocity. Without this rule, unisons would be doubled 6 dB loud and
  phase-locked. ``--no-key-sharing`` disables it.
* Anything else (program changes, pitch bend, CC10 pan ...) is ignored. The
  stereo image of a piano comes from the instrument itself, low strings left
  and high strings right, as heard from the keyboard.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from bisect import bisect_right
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import mido
import numpy as np
import scipy.signal as ss
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from piano_paths import (  # noqa: E402
    CALIBRATION_JSON,
    DERIVED_SFZ,
    DERIVED_SFZ_NO_PEDAL_NOISE,
    HALL_IR,
    SALAMANDER_DIR,
    SFIZZ_RENDER,
    SR,
)

STEM_TPB = 9600
STEM_TEMPO = 500_000  # -> one tick = 52 us
RESTRIKE_GAP = 0.015
UNISON_WINDOW = 0.005
MIN_NOTE = 0.010
FADER_SMOOTH = 0.020


# ----------------------------------------------------------------------------------------
# MIDI parsing
# ----------------------------------------------------------------------------------------
@dataclass
class Note:
    voice: str
    key: int
    start: float
    end: float
    velocity: int
    vel_eff: int = 0
    dropped: bool = False


@dataclass
class Voice:
    name: str
    notes: list = field(default_factory=list)
    cc: dict = field(default_factory=dict)  # cc number -> list[(time, value)]


class TempoMap:
    def __init__(self, tpb: int, tempos: list[tuple[int, int]]):
        self.tpb = tpb
        tempos = sorted(tempos)
        if not tempos or tempos[0][0] != 0:
            tempos.insert(0, (0, 500_000))
        self.ticks, self.secs, self.tempo = [], [], []
        sec, last_tick, last_tempo = 0.0, 0, tempos[0][1]
        for tick, tempo in tempos:
            sec += (tick - last_tick) * last_tempo / 1e6 / tpb
            self.ticks.append(tick)
            self.secs.append(sec)
            self.tempo.append(tempo)
            last_tick, last_tempo = tick, tempo

    def seconds(self, tick: int) -> float:
        i = bisect_right(self.ticks, tick) - 1
        return self.secs[i] + (tick - self.ticks[i]) * self.tempo[i] / 1e6 / self.tpb


def load_midi(path: Path) -> dict[str, Voice]:
    mf = mido.MidiFile(path)
    abs_events = []
    tempos = []
    names = {}
    for ti, track in enumerate(mf.tracks):
        tick = 0
        for msg in track:
            tick += msg.time
            if msg.type == "set_tempo":
                tempos.append((tick, msg.tempo))
            elif msg.type == "track_name" and ti not in names:
                names[ti] = msg.name.strip().rstrip(":").strip()
            elif msg.type in ("note_on", "note_off", "control_change"):
                abs_events.append((tick, ti, msg))
    if mf.type == 2:
        raise SystemExit("MIDI type 2 (independent sequences) is not supported")
    tmap = TempoMap(mf.ticks_per_beat, tempos)

    chans_per_track: dict[int, set] = {}
    for _, ti, msg in abs_events:
        if msg.type != "control_change":
            chans_per_track.setdefault(ti, set()).add(msg.channel)

    def vname(ti: int, ch: int) -> str:
        base = names.get(ti) or f"track{ti}"
        return f"{base}.ch{ch + 1}" if len(chans_per_track.get(ti, ())) > 1 else base

    voices: dict[str, Voice] = {}
    pending: dict[tuple, list] = {}
    abs_events.sort(key=lambda e: (e[0], 0 if e[2].type != "note_on" or e[2].velocity == 0 else 1))
    cc_events = []
    for tick, ti, msg in abs_events:
        t = tmap.seconds(tick)
        if msg.type == "control_change":
            cc_events.append((t, ti, msg))
            continue
        name = vname(ti, msg.channel)
        v = voices.setdefault(name, Voice(name))
        k = (name, msg.note)
        if msg.type == "note_on" and msg.velocity > 0:
            pending.setdefault(k, []).append((t, msg.velocity))
        else:
            if pending.get(k):
                st, vel = pending[k].pop(0)
                if t - st > 0:
                    v.notes.append(Note(name, msg.note, st, t, vel))
    for (name, key), lst in pending.items():
        for st, vel in lst:  # unterminated notes: 1 s
            voices[name].notes.append(Note(name, key, st, st + 1.0, vel))
    # Controllers go to every voice that lives on that (track, channel); CCs on
    # note-less channels of a track apply to all voices of that track.
    for t, ti, msg in cc_events:
        targets = [vname(ti, msg.channel)] if msg.channel in chans_per_track.get(ti, ()) else [
            vname(ti, c) for c in chans_per_track.get(ti, ())
        ]
        if not targets:  # e.g. a conductor track with only CC64: apply to the whole piano
            targets = [None]
        for name in targets:
            if name is None:
                voices.setdefault("__global__", Voice("__global__")).cc.setdefault(msg.control, []).append((t, msg.value))
            elif name in voices:
                voices[name].cc.setdefault(msg.control, []).append((t, msg.value))
    for v in voices.values():
        v.notes.sort(key=lambda n: (n.start, n.key))
        for lst in v.cc.values():
            lst.sort(key=lambda e: e[0])
    return voices


def cc_value_at(events: list, t: float, default: int) -> int:
    val = default
    for et, ev in events:
        if et <= t + 1e-9:
            val = ev
        else:
            break
    return val


# ----------------------------------------------------------------------------------------
# Expression -> velocity
# ----------------------------------------------------------------------------------------
class VelocityCurve:
    def __init__(self):
        if CALIBRATION_JSON.exists():
            db = np.array(json.loads(CALIBRATION_JSON.read_text())["velocity_db"], dtype=float)
        else:  # fall back to a plain SFZ-style curve
            v = np.arange(128) / 127.0
            db = 20 * np.log10(0.27 + 0.73 * v**2)
        db = db.copy()
        for i in range(1, len(db)):  # strictly increasing for inversion
            db[i] = max(db[i], db[i - 1] + 1e-4)
        self.db = db

    def shift(self, velocity: int, delta_db: float) -> int:
        if abs(delta_db) < 1e-9:
            return int(velocity)
        target = self.db[int(np.clip(velocity, 1, 127))] + delta_db
        v = np.interp(target, self.db[1:], np.arange(1, 128))
        return int(np.clip(round(float(v)), 1, 127))


def cc_db(value: int) -> float:
    return -120.0 if value <= 0 else 40.0 * math.log10(value / 127.0)


# perform.py (ricercar/tools) maps its dynamic levels ppp..fff to velocities 22..112
# (VEL_AT). The calibrated markings of this instrument are 12..127. "--velocity-scale
# perform" maps one onto the other, piecewise linear between the level anchors, so that
# perform.py's "f" is this piano's f (velocity 103, -6 dB) and not mf- (82, -11 dB).
# Accent and voicing offsets that perform.py adds on top of a level are scaled with the
# local slope, so a voice brought out stays brought out.
PERFORM_VEL_MAP = [(0, 0), (22, 12), (32, 29), (44, 42), (56, 64), (68, 86), (82, 103), (98, 115), (112, 127)]


def perform_velocity(v: int) -> int:
    xs, ys = zip(*PERFORM_VEL_MAP)
    return int(np.clip(round(float(np.interp(v, xs, ys))), 1, 127))


def midi_marker(path: Path) -> dict:
    """Read the ``perform.py target=...`` text event that perform.py writes into the
    tempo track, if present. Returns e.g. {"source": "perform.py", "target": "piano"}."""
    for track in mido.MidiFile(path).tracks:
        for msg in track:
            if msg.type == "text" and msg.text.startswith("perform.py"):
                info = {"source": "perform.py"}
                for tok in msg.text.split()[1:]:
                    if "=" in tok:
                        k, v = tok.split("=", 1)
                        info[k] = v
                return info
    return {}


# ----------------------------------------------------------------------------------------
# One keyboard shared by all voices
# ----------------------------------------------------------------------------------------
def share_keyboard(notes: list[Note]) -> dict:
    stats = {"unisons_merged": 0, "restrikes": 0}
    by_key: dict[int, list[Note]] = {}
    for n in sorted(notes, key=lambda n: (n.start, -n.vel_eff)):
        by_key.setdefault(n.key, []).append(n)
    for key, lst in by_key.items():
        active: Note | None = None
        for n in lst:
            if active is not None and n.start < active.end - 1e-6:
                if n.start - active.start <= UNISON_WINDOW:
                    # struck together: one key, one hammer -> keep the stronger
                    keep, drop = (active, n) if active.vel_eff >= n.vel_eff else (n, active)
                    keep.end = max(keep.end, drop.end)
                    drop.dropped = True
                    stats["unisons_merged"] += 1
                    active = keep
                    continue
                # re-strike of a held key
                held_until = active.end
                active.end = max(active.start + MIN_NOTE, n.start - RESTRIKE_GAP)
                n.end = max(n.end, held_until)
                stats["restrikes"] += 1
            active = n
    return stats


# ----------------------------------------------------------------------------------------
# Stems
# ----------------------------------------------------------------------------------------
def pedal_events(voices: dict[str, Voice]) -> list[tuple[float, int]]:
    ev = []
    for v in voices.values():
        ev += v.cc.get(64, [])
    ev.sort()
    out, state = [], 0
    for t, val in ev:
        s = 127 if val >= 64 else 0
        if s != state:
            out.append((t, s))
            state = s
    return out


def write_stem_midi(path: Path, notes: list[Note], pedal: list, transpose: int, lead_in: float) -> None:
    mf = mido.MidiFile(type=0, ticks_per_beat=STEM_TPB)
    tr = mido.MidiTrack()
    mf.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=STEM_TEMPO, time=0))
    ev = []
    ticks_per_sec = STEM_TPB * 1e6 / STEM_TEMPO
    for n in notes:
        if n.dropped:
            continue
        key = n.key + transpose
        while key < 21:  # fold notes outside the 88 keys back into range
            key += 12
        while key > 108:
            key -= 12
        ev.append((n.start + lead_in, 2, mido.Message("note_on", note=key, velocity=n.vel_eff)))
        ev.append((n.end + lead_in, 1, mido.Message("note_off", note=key, velocity=64)))
    for t, val in pedal:
        # pedal changes sort before notes at the same instant
        ev.append((t + lead_in, 0, mido.Message("control_change", control=64, value=val)))
    ev.sort(key=lambda e: (e[0], e[1]))
    now = 0
    for t, _, msg in ev:
        tick = int(round(t * ticks_per_sec))
        msg.time = max(0, tick - now)
        now = max(now, tick)
        tr.append(msg)
    tr.append(mido.MetaMessage("end_of_track", time=int(ticks_per_sec)))
    mf.save(path)


def check_instrument() -> None:
    """Refuse to render with a derived SFZ written by another version of make_sfz.py."""
    for p in (SFIZZ_RENDER, DERIVED_SFZ, DERIVED_SFZ_NO_PEDAL_NOISE):
        if not Path(p).exists():
            raise SystemExit(f"missing {p} -- run setup_piano.sh first")
    want = hashlib.sha256((Path(__file__).resolve().parent / "make_sfz.py").read_bytes()).hexdigest()
    for p in (DERIVED_SFZ, DERIVED_SFZ_NO_PEDAL_NOISE):
        with open(p) as f:
            head = "".join(f.readline() for _ in range(20))
        if f"sha256={want}" not in head:
            raise SystemExit(f"{p.name} was written by a different make_sfz.py -- run ./setup_piano.sh "
                             "(it regenerates the derived instrument)")


def prune_sfz(src: Path, keys: set[int], dst: Path) -> Path:
    """Copy of the derived SFZ without the regions that no key of this stem can trigger.

    The derived SFZ loads every sample into RAM (hint_ram_based=1: sfizz_render's disk
    streaming drops notes). One voice of a fugue uses a small part of the keyboard, so
    dropping the other regions cuts load time and memory several-fold. Regions without
    a key range (the pedal noises) are kept. The audio is bit-identical to a render with
    the full file. Sample paths stay relative to the library via default_path.
    """
    if any(c.isspace() for c in str(SALAMANDER_DIR)):
        return src  # default_path with blanks is not portable across SFZ parsers
    out, group_lo, group_hi = [], None, None
    for line in src.read_text().split("\n"):
        s = line.strip()
        if s.startswith("<control>"):
            out.append(f"<control> default_path={SALAMANDER_DIR}/ " + s[len("<control>"):].strip())
            continue
        if s.startswith("<group>"):
            ops = dict(t.split("=", 1) for t in s[len("<group>"):].split() if "=" in t)
            group_lo, group_hi = ops.get("lokey"), ops.get("hikey")
        elif s.startswith("<region>"):
            ops = dict(t.split("=", 1) for t in s[len("<region>"):].split() if "=" in t)
            lo = ops.get("lokey", ops.get("key", group_lo))
            hi = ops.get("hikey", ops.get("key", group_hi))
            if lo is not None and hi is not None and int(lo) >= 0:
                if not any(int(lo) <= k <= int(hi) for k in keys):
                    continue
        out.append(line)
    if not any(l.startswith("<control> default_path=") for l in out):
        out.insert(0, f"<control> default_path={SALAMANDER_DIR}/")
    dst.write_text("\n".join(out))
    return dst


def run_sfizz(sfz: Path, mid: Path, wav: Path, quality: int) -> None:
    cmd = [str(SFIZZ_RENDER), "--sfz", str(sfz), "--midi", str(mid), "--wav", str(wav),
           "-s", str(SR), "-q", str(quality), "-p", "512", "-b", "256"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not wav.exists():
        raise RuntimeError(f"sfizz_render failed for {mid}:\n{r.stdout}\n{r.stderr}")


def sounding_intervals(notes: list[Note], pedal: list, lead_in: float) -> list[tuple[float, float]]:
    """(start, end) in stem seconds while each note should sound: key down, extended to the
    next pedal release if the sustain pedal is down at the note-off."""
    downs = [(t, v) for t, v in pedal]
    out = []
    for n in notes:
        if n.dropped:
            continue
        end = n.end
        state = 0
        for t, v in downs:
            if t <= n.end + 1e-9:
                state = v
            else:
                break
        if state:
            ups = [t for t, v in downs if t > n.end and v == 0]
            end = ups[0] if ups else n.end + 5.0
        out.append((n.start + lead_in, end + lead_in))
    return out


def find_truncations(x: np.ndarray, intervals: list[tuple[float, float]]) -> list[dict]:
    """Notes that stop dead while they should sound (a sampler streaming underrun).

    1 ms frames; a truncation is a fall of more than 25 dB from the mean power of the
    10 frames before a frame boundary to the mean of the 10 frames after it (so a single
    quiet frame at a zero crossing of a bass note does not count), from a level within
    50 dB of the stem's loudest frame, at a time some note of the stem is held (or
    sustained by the pedal). A damper release (0.35 s envelope) falls about 2 dB in 10 ms.
    """
    m = x.mean(axis=1) if x.ndim == 2 else x
    fr = SR // 1000
    nf = len(m) // fr
    if nf < 30:
        return []
    p = (m[: nf * fr].reshape(nf, fr) ** 2).mean(axis=1) + 1e-30
    top = 10 * np.log10(p.max())
    k = np.ones(10) / 10
    before = 10 * np.log10(np.convolve(p, k, mode="full")[:nf])
    after = 10 * np.log10(np.convolve(p[::-1], k, mode="full")[:nf][::-1])
    d = after[1:] - before[:-1]
    cand = np.nonzero((d < -25) & (before[:-1] > top - 50))[0]
    out, last = [], -100
    for i in cand:
        t = (i + 1) / 1000
        if i - last > 20 and any(a + 0.003 < t < b + 0.002 for a, b in intervals):
            out.append({"t": round(t, 3), "drop_db": round(float(d[i]), 1),
                        "level_re_stem_max_db": round(float(before[i] - top), 1)})
        last = i
    return out


def fader(events: list, n: int, default: int, to_db, lead_in: float) -> np.ndarray | None:
    if not events:
        return None
    step = np.full(n, to_db(default), dtype=np.float64)
    for t, val in events:
        i = int(round((t + lead_in) * SR))
        if i < n:
            step[max(i, 0):] = to_db(val)
    w = int(FADER_SMOOTH * SR)
    kernel = np.ones(w) / w
    sm = np.convolve(np.concatenate([np.full(w, step[0]), step]), kernel, mode="full")[w : w + n]
    return 10 ** (sm / 20.0)


# ----------------------------------------------------------------------------------------
# Output processing
# ----------------------------------------------------------------------------------------
def true_peak(x: np.ndarray) -> float:
    up = ss.resample_poly(x, 4, 1, axis=0)
    return float(np.abs(up).max())


def c80_of(ir: np.ndarray, g: float) -> float:
    e = np.sum(ir**2, axis=1) / 2
    n80 = int(0.080 * SR)
    early = 1.0 + g * g * e[:n80].sum()
    late = g * g * e[n80:].sum()
    return 10 * math.log10(early / late)


def measure_file(path: Path) -> dict | None:
    """EBU R128 integrated loudness, loudness range and true peak of a written file (ffmpeg)."""
    if shutil.which("ffmpeg") is None:
        return None
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-filter_complex",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    summary = r.stderr[r.stderr.rfind("Summary:"):]
    out = {}
    for key, label in (("integrated_lufs", "I:"), ("lra_lu", "LRA:"), ("true_peak_dbtp", "Peak:")):
        for line in summary.splitlines():
            if line.strip().startswith(label):
                try:
                    out[key] = float(line.split()[1])
                except ValueError:
                    pass
                break
    return out or None


def write_outputs(x: np.ndarray, out: Path, make_m4a: bool) -> dict:
    wav = out.with_suffix(".wav")
    # TPDF dither to 24 bit
    lsb = 2.0 ** -23
    d = (np.random.default_rng(0).random(x.shape) - np.random.default_rng(1).random(x.shape)) * lsb
    sf.write(wav, np.clip(x + d, -1, 1 - lsb), SR, subtype="PCM_24")
    res = {"wav": str(wav)}
    if make_m4a:
        m4a = out.with_suffix(".m4a")
        if m4a.exists():
            m4a.unlink()
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "256000", str(wav), str(m4a)], check=True)
        res["m4a"] = str(m4a)
    return res


def main(argv=None) -> dict:
    ap = argparse.ArgumentParser(description="Render multi-voice MIDI on a sampled concert grand (see docstring).",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("midi", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="output path without extension (default: next to the MIDI)")
    ap.add_argument("--wet-db", type=float, default=-4.0, help="reverb energy relative to dry (default -4 dB, C80 ~ +8 dB)")
    ap.add_argument("--no-reverb", action="store_true")
    ap.add_argument("--ir", type=Path, default=HALL_IR)
    ap.add_argument("--peak-db", type=float, default=-1.0, help="true-peak target (default -1 dBFS)")
    ap.add_argument("--lead-in", type=float, default=0.3, help="silence before the first note (s)")
    ap.add_argument("--dyn-db", type=float, default=0.0, help="global dynamic offset in dB, realised via velocity")
    ap.add_argument("--transpose", action="append", default=[], metavar="VOICE=N",
                    help="transpose one voice by N semitones (repeatable), e.g. pedal=-12")
    ap.add_argument("--stems", type=Path, help="write each voice's dry stem (float WAV) into this directory")
    ap.add_argument("--velocity-scale", choices=["auto", "raw", "perform"], default="auto",
                    help="raw: velocities are this piano's calibrated scale; perform: perform.py's scale "
                    "(pp 32, f 82, ff 98), remapped; auto (default): perform if the file was written by "
                    "perform.py, else raw")
    ap.add_argument("--cc-dynamics", choices=["auto", "velocity", "gain", "off"], default="auto",
                    help="velocity: min(CC1, CC11) at each note-on -> hammer velocity; gain: CC1 -> velocity, "
                    "CC11 -> continuous fader; off: ignore CC1/CC11; auto (default): off for perform.py "
                    "--target strings files (their velocities already carry the dynamics), else velocity")
    ap.add_argument("--cc11-mode", choices=["velocity", "gain"], help=argparse.SUPPRESS)  # old name
    ap.add_argument("--no-key-sharing", action="store_true")
    ap.add_argument("--quality", type=int, default=10, help="sfizz resampling quality 1-10 (10 = sinc72)")
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 4),
                    help="parallel sfizz_render instances (default 4; each holds its voice's samples in RAM)")
    ap.add_argument("--keep-temp", action="store_true")
    ap.add_argument("--no-m4a", action="store_true")
    ap.add_argument("--json", type=Path, help="write a JSON render report here")
    args = ap.parse_args(argv)

    check_instrument()

    out = args.out or args.midi.with_suffix("")
    out.parent.mkdir(parents=True, exist_ok=True)
    transpose_arg = {}
    for t in args.transpose:
        k, v = t.split("=")
        transpose_arg[k.strip()] = int(v)

    marker = midi_marker(args.midi)
    vscale = args.velocity_scale
    if vscale == "auto":
        vscale = "perform" if marker.get("source") == "perform.py" else "raw"
    ccdyn = args.cc_dynamics
    if args.cc11_mode and ccdyn == "auto":
        ccdyn = args.cc11_mode
    if ccdyn == "auto":
        ccdyn = "off" if marker.get("target") == "strings" else "velocity"
    print(f"velocity scale: {vscale}; CC1/CC11 dynamics: {ccdyn}"
          + (f"; written by perform.py --target {marker.get('target')}" if marker else ""))

    voices = load_midi(args.midi)
    glob = voices.pop("__global__", None)
    if glob is not None:  # global CCs (e.g. CC64 on a conductor track)
        for v in voices.values():
            for cc, ev in glob.cc.items():
                v.cc.setdefault(cc, []).extend(ev)
                v.cc[cc].sort()
    voices = {k: v for k, v in voices.items() if v.notes}
    if not voices:
        raise SystemExit("no notes found")
    # Voice names match case-insensitively (perform.py writes "pedal", other files "Pedal").
    transpose = {}
    for name, semis in transpose_arg.items():
        hits = [v for v in voices if v.lower() == name.lower()]
        if not hits:
            raise SystemExit(f"--transpose: no voice named {name!r}; voices are {list(voices)}")
        for h in hits:
            transpose[h] = semis

    curve = VelocityCurve()
    all_notes = []
    for v in voices.values():
        cc1, cc11 = v.cc.get(1, []), v.cc.get(11, [])
        for n in v.notes:
            vel = perform_velocity(n.velocity) if vscale == "perform" else n.velocity
            dyn = 127
            if ccdyn != "off":
                dyn = cc_value_at(cc1, n.start, 127)
                if ccdyn == "velocity":
                    dyn = min(dyn, cc_value_at(cc11, n.start, 127))
            delta = args.dyn_db + cc_db(dyn)
            n.vel_eff = curve.shift(vel, delta)
            all_notes.append(n)

    # Key sharing works on sounding pitches.
    for n in all_notes:
        n.key = n.key + transpose.get(n.voice, 0)
    share = {"unisons_merged": 0, "restrikes": 0} if args.no_key_sharing else share_keyboard(all_notes)
    pedal = pedal_events(voices)

    tmp = Path(tempfile.mkdtemp(prefix="piano_render_"))
    names = list(voices)
    jobs = []
    for i, name in enumerate(names):
        mid = tmp / f"stem{i:02d}.mid"
        wav = tmp / f"stem{i:02d}.wav"
        write_stem_midi(mid, voices[name].notes, pedal, 0, args.lead_in)
        keys = {n.key for n in voices[name].notes if not n.dropped}
        sfz = prune_sfz(DERIVED_SFZ if i == 0 else DERIVED_SFZ_NO_PEDAL_NOISE, keys, tmp / f"stem{i:02d}.sfz")
        jobs.append((sfz, mid, wav))
    print(f"rendering {len(names)} voice stem(s) with sfizz: {', '.join(names)}")
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        list(ex.map(lambda j: run_sfizz(j[0], j[1], j[2], args.quality), jobs))

    # Guard against dropped notes: a stem in which a held note stops dead is rendered again.
    truncation = {"checked_stems": len(jobs), "rerendered": {}, "found": {}}
    for i, (name, j) in enumerate(zip(names, jobs)):
        spans = sounding_intervals(voices[name].notes, pedal, args.lead_in)
        for attempt in range(3):
            x = sf.read(j[2], dtype="float64", always_2d=True)[0]
            hits = find_truncations(x, spans)
            if not hits:
                break
            truncation["found"].setdefault(name, []).append(hits)
            if attempt == 2:
                raise SystemExit(f"{name}: notes stop while held after 3 renders ({hits[:3]}); "
                                 f"stem kept in {tmp}")
            print(f"warning: {name}: {len(hits)} note(s) cut while held at {[h['t'] for h in hits][:5]} s; rendering again",
                  file=sys.stderr)
            truncation["rerendered"][name] = attempt + 1
            run_sfizz(j[0], j[1], j[2], args.quality)

    stems = [sf.read(j[2], dtype="float64", always_2d=True)[0] for j in jobs]
    n = max(len(s) for s in stems)
    ir = None
    if not args.no_reverb:
        ir, ir_sr = sf.read(args.ir, dtype="float64", always_2d=True)
        assert ir_sr == SR, "IR must be 48 kHz"
    tail = 0 if ir is None else len(ir)
    dry = np.zeros((n + tail, 2))
    report_voices = {}
    for name, s in zip(names, stems):
        v = voices[name]
        s = np.pad(s, ((0, n + tail - len(s)), (0, 0)))
        g7 = fader(v.cc.get(7, []), len(s), 100, lambda c: -120.0 if c <= 0 else 40 * math.log10(c / 100), args.lead_in)
        if g7 is not None:
            s *= g7[:, None]
        if ccdyn == "gain":
            g11 = fader(v.cc.get(11, []), len(s), 127, cc_db, args.lead_in)
            if g11 is not None:
                s *= g11[:, None]
        dry += s
        vel = [x.vel_eff for x in v.notes if not x.dropped]
        report_voices[name] = {
            "notes": len(vel),
            "velocity_in_mean": round(float(np.mean([x.velocity for x in v.notes])), 1),
            "velocity_in_range": [int(min(x.velocity for x in v.notes)), int(max(x.velocity for x in v.notes))],
            "velocity_eff_mean": round(float(np.mean(vel)), 1) if vel else None,
            "velocity_eff_range": [int(min(vel)), int(max(vel))] if vel else None,
            "rms_dbfs_prenorm": round(float(10 * np.log10(np.mean(s**2) + 1e-20)), 2),
            "transpose": transpose.get(name, 0),
        }
        if args.stems:
            args.stems.mkdir(parents=True, exist_ok=True)
            sf.write(args.stems / f"{name.replace('/', '_')}.wav", s[:n].astype(np.float32), SR, subtype="FLOAT")

    mix = dry.copy()
    c80 = None
    if ir is not None:
        g = 10 ** (args.wet_db / 20)
        # L->L, R->R: the close AB pair of the samples is partly anti-phase on some
        # notes, so a mono sum would starve those notes of reverb.
        wet = np.stack([ss.fftconvolve(dry[:n, c], ir[:, c]) for c in range(2)], axis=1)
        mix[: len(wet)] += g * wet[: len(mix)]
        c80 = c80_of(ir, g)

    # Remove DC/rumble, trim the silent tail, normalise the true peak.
    mix = ss.sosfilt(ss.butter(2, 18, "high", fs=SR, output="sos"), mix, axis=0)
    env = np.abs(mix).max(axis=1)
    thr = env.max() * 10 ** (-80 / 20)
    last = int(np.nonzero(env > thr)[0][-1]) + int(0.05 * SR)
    mix = mix[: min(last, len(mix))]
    fade = min(int(0.05 * SR), len(mix))
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    tp = true_peak(mix)
    gain = 10 ** (args.peak_db / 20) / tp
    mix *= gain
    files = write_outputs(mix, out, not args.no_m4a)

    if not args.keep_temp:
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        files["temp"] = str(tmp)

    report = {
        "input": str(args.midi),
        **files,
        "midi_marker": marker or None,
        "velocity_scale": vscale,
        "cc_dynamics": ccdyn,
        "duration_s": round(len(mix) / SR, 2),
        "voices": report_voices,
        "key_sharing": share,
        "truncation_check": truncation,
        "pedal_changes": len(pedal),
        "wet_db": None if ir is None else args.wet_db,
        "c80_db": None if c80 is None else round(c80, 1),
        "normalise_gain_db": round(20 * math.log10(gain), 2),
        "true_peak_dbfs": args.peak_db,
        "rms_dbfs": round(float(10 * np.log10(np.mean(mix**2))), 2),
        "measured": {k: measure_file(Path(files[k])) for k in ("wav", "m4a") if k in files},
    }
    print(json.dumps(report, indent=1))
    if args.json:
        args.json.write_text(json.dumps(report, indent=1))
    return report


if __name__ == "__main__":
    main()
