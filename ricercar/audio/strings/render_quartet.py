#!/usr/bin/env python3
"""Render a multi-voice MIDI file as a solo string quartet in a concert hall.

Engine: sfizz_render (float output) playing the University of Iowa MIS solo
strings (pp / mf / ff recorded layers, built into SFZ by iowa_build.py).  Each
voice is rendered dry, placed on stage, convolved with a measured concert-hall
impulse response, mixed, normalised to a true peak of -1 dBFS and written as
48 kHz / 24-bit WAV plus 256 kb/s AAC (.m4a).

USAGE
  python3 render_quartet.py INPUT.mid [-o OUT_BASENAME] [options]

END TO END (the ricercar pipeline)
  python3 ../../tools/perform.py SCORE.ly PLAN.json OUT.mid --target strings
  python3 render_quartet.py OUT.mid -o out/piece

OPTIONS
  -o, --out PATH         output basename -> PATH.wav, PATH.m4a (default: next to INPUT)
  --lib iowa|vpo3        sample library (default iowa; vpo3 = Virtual Playing Orchestra 3
                         solo strings, kept for comparison, see README/ANALYSIS)
  --map SPEC             voice -> instrument, e.g. "soprano=vn1,alto=vn2,tenor=va,pedal=vc"
                         or by index "0=vn1,1=vn2".  Instruments: vn1 vn2 va vc cb
  --bass-double MODE     off (default) | on | auto: add a double bass an octave below the
                         cello.  auto fades it in only where the cello's dynamic level is
                         at or above --bass-threshold (tutti climaxes); a cello track may
                         also carry CC22 = doubling amount 0-127 (overrides auto)
  --bass-threshold LVL   dynamic level for auto doubling, ppp..fff or 1-8 (default ff)
  --hall NAME            detmold (default: Konzerthaus Detmold, measured, CC BY 4.0, same
                         hall as the piano renders) | synthetic | none
  --wet DB               reverb energy relative to the dry signal (default -2 dB)
  --short-ms MS          notes shorter than this get the short (detache) stroke (default 260)
  --legato-xfade-ms MS   overlap of slurred notes (default 70)
  --cc11-depth X         CC11 gain = X * 20*log10(v/127) dB (default 0.5, see below)
  --stems                also write dry per-instrument stems (float WAV)
  --report PATH.json     write a JSON render report (voices, articulations, levels)
  --peak DB              true-peak target (default -1.0 dBFS)

VOICE MAPPING (first rule that applies)
  --map; perform.py / SATB names (soprano -> Violin I, alto -> Violin II,
  tenor -> Viola, bass or pedal -> Cello); instrument names (violin 1/2, viola,
  cello, contrabass); GM program (40 violin, 41 viola, 42 cello, 43 contrabass);
  otherwise by mean pitch, highest -> Violin I.
  Notes below an instrument's compass are rescued the way an arranger would:
  dropped if another voice doubles them in unison, else the whole connected
  phrase is handed to a lower instrument that is resting at that moment (the
  old fugue's tenor dips to F2 while the pedal rests: the cello takes it),
  else transposed up an octave (reported).

MIDI CONVENTIONS (what perform.py --target strings writes)
  * One track per voice.  Velocity = accent / attack bite (127 = the recorded
    bite, low = softer, slower start; about +-2 dB).
  * CC1 = dynamic level with real timbre change, perform.py's scale:
    ppp 36, pp 49, p 62, mp 75, mf 88, f 101, ff 114, fff 127.  The pp, mf and
    ff recordings play alone at 49, 88 and 114 and are equal-power crossfaded in
    between; loudness moves about 3.5 dB per step.  Linear ramps between CC
    events are reconstructed (perform.py samples every 16th note).
  * CC11 = expression gain without timbre change, X*20*log10(v/127) dB with
    X = --cc11-depth (0.5 default).  perform.py sends CC11 = CC1, so the full
    GM curve would double-count the dynamics: pp -> ff would span ~32 dB.
    With 0.5 the pp -> ff span is ~20 dB, like a real quartet in a hall.
  * CC7 = channel volume, GM curve 40*log10(v/127) dB.  CC10 pan is ignored
    (fixed stage positions).  CC64 is ignored.
  * No CC1 at all (e.g. a --target piano file): the dynamic level is taken from
    note velocities on perform.py's velocity scale.
  * Optional CC20 articulation per note: 0-63 normal bow stroke, 64-95 slurred,
    96-127 short.  If absent it is inferred: a note that starts within 60 ms of
    the previous note's end, on a different pitch, and is not short, is slurred
    (the previous note is held --legato-xfade-ms into it and released over
    0.12 s while the new note enters in its sustain); notes shorter than
    --short-ms get the short stroke; everything else is a new bow.
  * Optional CC21 release per note: 0.03 + 1.2*v/127 s.  If absent: 0.12 s
    into a slur, 0.18-0.22 s between detached notes, 0.5-1.1 s before a rest.
  * Tempo map honoured (all timing is converted to seconds before rendering).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import mido
import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from iowa_common import QUARTET_DIR, SFIZZ_RENDER  # noqa: E402
import hall  # noqa: E402

SR = 48000
LEVELS = {"ppp": 1, "pp": 2, "p": 3, "mp": 4, "mf": 5, "f": 6, "ff": 7, "fff": 8}
VEL_AT = {1: 22, 2: 32, 3: 44, 4: 56, 5: 68, 6: 82, 7: 98, 8: 112}      # perform.py velocity scale


def level_to_cc1(L: float) -> int:
    return int(np.clip(round(36 + 13 * (L - 1)), 0, 127))


# id: sfz, display name, stage azimuth (deg, + = left), depth (m), trim (dB), compass lo/hi
INSTR = {
    "vn1": dict(sfz="violin.sfz", name="Violin I", az=30.0, depth=0.0, trim=0.0, lo=55, hi=100),
    "vn2": dict(sfz="violin2.sfz", name="Violin II", az=10.0, depth=0.4, trim=0.0, lo=55, hi=100),
    "va": dict(sfz="viola.sfz", name="Viola", az=-10.0, depth=0.4, trim=0.0, lo=48, hi=91),
    "vc": dict(sfz="cello.sfz", name="Cello", az=-28.0, depth=0.0, trim=0.0, lo=36, hi=81),
    "cb": dict(sfz="bass.sfz", name="Contrabass", az=-36.0, depth=1.2, trim=0.0, lo=28, hi=67),
}
ORDER = ["vn1", "vn2", "va", "vc", "cb"]
EXT_DOWN = 2            # the SFZ stretches the lowest sample this many semitones down
SATB = {"soprano": "vn1", "descant": "vn1", "alto": "vn2", "mezzo": "vn2", "tenor": "va",
        "baritone": "va", "bass": "vc", "pedal": "vc"}
NAME_KEYS = [
    ("vn1", ["violin 1", "violin i", "vln 1", "vln. 1", "vn1", "vn 1", "violino i", "violin1", "1st violin",
             "first violin"]),
    ("vn2", ["violin 2", "violin ii", "vln 2", "vln. 2", "vn2", "vn 2", "violino ii", "violin2", "2nd violin",
             "second violin"]),
    ("va", ["viola", "vla", "alto viol"]),
    ("vc", ["violoncello", "cello", "vlc", "vc"]),
    ("cb", ["contrabass", "double bass", "doublebass", "kontrabass", "contrabasso", "cb"]),
]
PROGRAM = {40: "vn", 41: "va", 42: "vc", 43: "cb"}


@dataclass
class Note:
    on: float
    off: float
    key: int
    vel: int
    art: int | None = None      # CC20 value
    rel: int | None = None      # CC21 value


@dataclass
class Voice:
    name: str
    track: int
    channel: int
    notes: list = field(default_factory=list)
    cc: dict = field(default_factory=dict)       # num -> [(t, v)]
    bend: list = field(default_factory=list)     # [(t, value -8192..8191)]
    program: int | None = None
    inst: str | None = None

    @property
    def mean_pitch(self):
        return float(np.mean([n.key for n in self.notes])) if self.notes else 0.0


@dataclass
class Job:
    voice: Voice              # CC / bend source
    notes: list               # the notes this job plays
    inst: str                 # instrument id (stage position, trim)
    kind: str = "main"        # main | borrowed | double
    label: str = ""


# ------------------------------------------------------------------ MIDI in
def tempo_map(mid: mido.MidiFile):
    """-> function tick -> seconds (honours every set_tempo in any track)."""
    changes = []
    for tr in mid.tracks:
        t = 0
        for msg in tr:
            t += msg.time
            if msg.type == "set_tempo":
                changes.append((t, msg.tempo))
    changes.sort()
    if not changes or changes[0][0] != 0:
        changes.insert(0, (0, 500000))
    ticks = [c[0] for c in changes]
    secs = [0.0]
    for i in range(1, len(changes)):
        secs.append(secs[-1] + (changes[i][0] - changes[i - 1][0]) * changes[i - 1][1] / 1e6 / mid.ticks_per_beat)
    tpb = mid.ticks_per_beat

    def f(tick):
        i = max(0, int(np.searchsorted(ticks, tick, side="right")) - 1)
        return secs[i] + (tick - ticks[i]) * changes[i][1] / 1e6 / tpb
    return f


def midi_marker(mid: mido.MidiFile) -> dict:
    for tr in mid.tracks:
        for msg in tr:
            if msg.type == "text" and msg.text.startswith("perform.py"):
                info = {"source": "perform.py"}
                for tok in msg.text.split()[1:]:
                    if "=" in tok:
                        k, v = tok.split("=", 1)
                        info[k] = v
                return info
    return {}


def read_voices(path: Path):
    mid = mido.MidiFile(str(path))
    t2s = tempo_map(mid)
    voices: dict[tuple[int, int], Voice] = {}
    for ti, tr in enumerate(mid.tracks):
        name = f"track{ti}"
        tick = 0
        pending: dict[tuple[int, int], list] = {}
        for msg in tr:
            tick += msg.time
            if msg.type == "track_name":
                name = msg.name.strip() or name
                for v in voices.values():
                    if v.track == ti:
                        v.name = name
            if not hasattr(msg, "channel"):
                continue
            key = (ti, msg.channel)
            if key not in voices:
                voices[key] = Voice(name=name, track=ti, channel=msg.channel)
            v = voices[key]
            t = t2s(tick)
            if msg.type == "note_on" and msg.velocity > 0:
                pending.setdefault((msg.channel, msg.note), []).append((t, msg.velocity))
            elif msg.type in ("note_off", "note_on"):
                lst = pending.get((msg.channel, msg.note))
                if lst:
                    on, vel = lst.pop(0)
                    if t > on:
                        v.notes.append(Note(on, t, msg.note, vel))
            elif msg.type == "control_change":
                v.cc.setdefault(msg.control, []).append((t, msg.value))
            elif msg.type == "pitchwheel":
                v.bend.append((t, msg.pitch))
            elif msg.type == "program_change":
                v.program = msg.program
    out = [v for v in voices.values() if v.notes]
    for v in out:
        v.notes.sort(key=lambda n: (n.on, -n.key))
        for c in v.cc.values():
            c.sort(key=lambda e: e[0])
    return out, midi_marker(mid)


def assign(voices: list[Voice], spec: str | None):
    if spec:
        for item in spec.split(","):
            k, inst = (x.strip() for x in item.split("="))
            if inst not in INSTR:
                sys.exit(f"--map: unknown instrument {inst!r} (use {' '.join(INSTR)})")
            for i, v in enumerate(voices):
                if (k.isdigit() and int(k) == i) or (not k.isdigit() and k.lower() in v.name.lower()):
                    v.inst = inst
    taken = {v.inst for v in voices if v.inst}
    for v in voices:                                    # SATB / perform.py voice names
        nm = v.name.lower().strip()
        if not v.inst and nm in SATB and SATB[nm] not in taken:
            v.inst = SATB[nm]
            taken.add(v.inst)
    for v in voices:                                    # instrument names
        if v.inst:
            continue
        nm = v.name.lower()
        for inst, keys in NAME_KEYS:
            if inst not in taken and any(k == nm or k in nm for k in keys):
                v.inst = inst
                taken.add(inst)
                break
    rest = [v for v in voices if not v.inst]            # GM programs / pitch order
    for v in sorted(rest, key=lambda v: -v.mean_pitch):
        fam = PROGRAM.get(v.program if v.program is not None else -1)
        cands = [o for o in ORDER if o not in taken and (fam is None or o.startswith(fam))]
        if not cands:
            cands = [o for o in ORDER if o not in taken] or ["vn1"]
        v.inst = cands[0]
        taken.add(v.inst)
    return voices


# ------------------------------------------------------------ dynamics (CC1)
def ensure_cc1(v: Voice):
    """Files without CC1 (e.g. perform.py --target piano): derive the dynamic
    level from note velocities on perform.py's velocity scale."""
    if 1 in v.cc:
        return False
    lv = sorted(VEL_AT.items())
    vs = [x[1] for x in lv]
    ls = [x[0] for x in lv]
    ev = []
    for n in v.notes:
        L = float(np.interp(n.vel, vs, ls))
        ev.append((max(0.0, n.on - 0.01), level_to_cc1(L)))
    v.cc[1] = ev
    return True


def cc1_curve(events, t_end: float, step: float = 0.02, max_ramp: float = 0.6):
    """Reconstruct the continuous CC1 curve: perform.py samples a hairpin every
    16th note, so consecutive events closer than max_ramp are joined by linear
    ramps (each event is the value reached at its time); longer gaps hold the
    value and ramp over the last 60 ms.  Returns [(t, value)] at <= step spacing."""
    if not events:
        return []
    out = [(0.0, events[0][1])] if events[0][0] > 0 else []
    for (t0, v0), (t1, v1) in zip(events, events[1:]):
        out.append((t0, v0))
        if v1 == v0 or t1 <= t0:
            continue
        a = t0 if t1 - t0 <= max_ramp else max(t0, t1 - 0.06)
        n = max(1, int((t1 - a) / step))
        for i in range(1, n):
            x = a + (t1 - a) * i / n
            val = v0 + (v1 - v0) * i / n
            out.append((x, int(round(val))))
    out.append(events[-1])
    ded = []
    for t, val in out:
        if not ded or val != ded[-1][1]:
            ded.append((t, val))
    return ded


def cc_value_at(events, t: float, default: int) -> int:
    val = default
    for te, v in events or []:
        if te > t:
            break
        val = v
    return val


# ------------------------------------------------------ compass (range) rescue
def rescue_range(voices: list[Voice], jobs_out: list, log: list):
    """Notes below an instrument's compass: drop unison doublings, hand connected
    phrases to a resting lower instrument, else transpose up an octave."""
    by_inst = {v.inst: v for v in voices}
    all_notes = [(v, n) for v in voices for n in v.notes]
    for v in voices:
        lo = INSTR[v.inst]["lo"] - EXT_DOWN
        low = [n for n in v.notes if n.key < lo]
        if not low:
            continue
        moved = set()
        for n in low:
            if id(n) in moved:
                continue
            twin = [m for (w, m) in all_notes if w is not v and m.key == n.key and m.on < n.off - 0.05
                    and m.off > n.on + 0.05]
            if twin:
                v.notes.remove(n)
                log.append(f"{v.name}: {n.key} at {n.on:.2f}s below {INSTR[v.inst]['name']} compass, "
                           f"doubled in unison by another voice -> dropped")
                continue
            # a lower instrument of the ensemble that is resting around this phrase
            lower = [i for i in ORDER[ORDER.index(v.inst) + 1:] if i in by_inst]
            done = False
            for li in lower:
                other = by_inst[li]
                if n.key < INSTR[li]["lo"] - EXT_DOWN:
                    continue

                def free(a, b, other=other):
                    # the lower player may still be finishing a note as the phrase begins (hand-off)
                    return not any(m.on < b + 0.15 and m.off > a + 0.04 for m in other.notes)
                if not free(n.on, n.off):
                    continue
                # grow the phrase through connected notes while the lower instrument rests
                i = v.notes.index(n)
                j0 = i
                while j0 > 0 and v.notes[j0].on - v.notes[j0 - 1].off < 0.35 and free(v.notes[j0 - 1].on,
                                                                                       v.notes[j0 - 1].off):
                    j0 -= 1
                j1 = i
                while j1 + 1 < len(v.notes) and v.notes[j1 + 1].on - v.notes[j1].off < 0.35 and \
                        free(v.notes[j1 + 1].on, v.notes[j1 + 1].off):
                    j1 += 1
                phrase = v.notes[j0: j1 + 1]
                if any(m.key > INSTR[li]["hi"] for m in phrase):
                    continue
                for m in phrase:
                    moved.add(id(m))
                    v.notes.remove(m)
                jobs_out.append(Job(voice=v, notes=phrase, inst=li, kind="borrowed",
                                    label=f"{v.name} on {INSTR[li]['name']}"))
                log.append(f"{v.name}: {len(phrase)} notes {phrase[0].on:.2f}-{phrase[-1].off:.2f}s "
                           f"(down to {min(m.key for m in phrase)}) handed to the resting {INSTR[li]['name']}")
                done = True
                break
            if not done:
                while n.key < lo:
                    n.key += 12
                log.append(f"{v.name}: note at {n.on:.2f}s below compass, no free lower instrument -> "
                           f"transposed up to {n.key}")


# ------------------------------------------------------- articulation logic
def rel_cc(seconds: float) -> int:
    return int(np.clip(round((seconds - 0.03) / 1.2 * 127), 0, 127))


SHORT_REL = float(os.environ.get("QUARTET_SHORT_REL", "0.09"))   # release of a short note into the next


def shape_articulation(notes: list[Note], short_s: float, xfade_s: float, has_art: bool, has_rel: bool):
    """Infer CC20 (articulation) and CC21 (release) per note; extend slurred
    notes so the previous note fades out under the next one."""
    counts = {"normal": 0, "legato": 0, "short": 0}
    for i, n in enumerate(notes):
        prev = notes[i - 1] if i else None
        nxt = notes[i + 1] if i + 1 < len(notes) else None
        dur = n.off - n.on
        chord_prev = prev is not None and abs(n.on - prev.on) < 0.03
        connected_in = (prev is not None and not chord_prev and n.on - prev.off < 0.06
                        and prev.key != n.key)
        if not has_art:
            if dur < short_s:
                n.art = 112
            elif connected_in:
                n.art = 80
            else:
                n.art = 0
        counts["short" if n.art >= 96 else "legato" if n.art >= 64 else "normal"] += 1
    for i, n in enumerate(notes):
        nxt = notes[i + 1] if i + 1 < len(notes) else None
        dur = n.off - n.on
        chord_next = nxt is not None and abs(nxt.on - n.on) < 0.03
        slur_out = nxt is not None and not chord_next and 64 <= (nxt.art or 0) < 96 and nxt.on - n.off < 0.06
        gap = (nxt.on - n.off) if nxt is not None and not chord_next else 99.0
        if slur_out:
            n.off = max(n.off, nxt.on + xfade_s)
            rel = 0.12
        elif gap < 0.08 and dur >= short_s and nxt is not None and (nxt.art or 0) >= 96:
            # into a detached short note (a dotted figure, a run): lift the bow a
            # moment early so the short note speaks instead of drowning in a release
            n.off = max(n.on + 0.6 * dur, min(n.off, nxt.on - 0.025))
            rel = SHORT_REL
        elif gap < 0.08:
            rel = SHORT_REL if dur < short_s else 0.22
        elif dur < short_s:
            rel = 0.25
        else:
            rel = float(np.clip(0.45 + 0.25 * dur, 0.5, 1.1))
        if not has_rel:
            n.rel = rel_cc(rel)
    return counts


# ------------------------------------------------------------- per job MIDI
TPB_OUT = 960
TEMPO_OUT = 500000                      # 120 bpm -> 1920 ticks per second


def sec2tick(t: float) -> int:
    return int(round(max(0.0, t) * TPB_OUT * 1e6 / TEMPO_OUT))


def job_midi(job: Job, transpose: int = 0) -> mido.MidiFile:
    v = job.voice
    ev = []   # (tick, prio, msg)
    t_end = max(n.off for n in job.notes) + 2.0
    cc1 = cc1_curve(v.cc.get(1, []), t_end)
    ev.append((0, 0, mido.Message("control_change", control=1, value=cc1[0][1] if cc1 else 88)))
    for t, val in cc1:
        ev.append((sec2tick(t), 1, mido.Message("control_change", control=1, value=int(val))))
    for num in (20, 21):
        for t, val in v.cc.get(num, []):
            ev.append((sec2tick(t), 1, mido.Message("control_change", control=num, value=val)))
    for t, val in v.bend:
        ev.append((sec2tick(t), 1, mido.Message("pitchwheel", pitch=val)))
    for n in job.notes:
        k = n.key + transpose
        if not 0 <= k <= 127:
            continue
        ton, toff = sec2tick(n.on), sec2tick(n.off)
        if n.art is not None:
            ev.append((ton, 2, mido.Message("control_change", control=20, value=n.art)))
        if n.rel is not None:
            ev.append((ton, 2, mido.Message("control_change", control=21, value=n.rel)))
        ev.append((ton, 4, mido.Message("note_on", note=k, velocity=int(np.clip(n.vel, 1, 127)))))
        ev.append((max(toff, ton + 1), 3, mido.Message("note_off", note=k, velocity=0)))
    ev.sort(key=lambda e: (e[0], e[1]))
    mid = mido.MidiFile(type=0, ticks_per_beat=TPB_OUT)
    tr = mido.MidiTrack()
    tr.append(mido.MetaMessage("set_tempo", tempo=TEMPO_OUT))
    last = 0
    for tick, _, msg in ev:
        tr.append(msg.copy(time=tick - last))
        last = tick
    tr.append(mido.MetaMessage("end_of_track", time=TPB_OUT))
    mid.tracks.append(tr)
    return mid


def run_sfizz(sfz: Path, midi_path: Path, wav: Path):
    cmd = [str(SFIZZ_RENDER), "--sfz", str(sfz), "--midi", str(midi_path), "--wav", str(wav),
           "-s", str(SR), "-p", "256", "-q", "3"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not wav.exists():
        raise RuntimeError(f"sfizz_render failed for {midi_path.name}: {r.stdout}\n{r.stderr}")
    x, fs = sf.read(str(wav), dtype="float32", always_2d=True)
    assert fs == SR
    return x


# --------------------------------------------------------- CC gain envelopes
def gain_envelope(events, n: int, default: int, to_db, smooth_s: float = 0.03):
    """Piecewise-linear (between events <= 0.6 s apart) CC curve -> linear gain per sample."""
    pts = cc1_curve(sorted(events or []), n / SR)
    db = np.full(n, to_db(default), dtype=np.float64)
    for t, val in pts:
        i = int(t * SR)
        if i < n:
            db[i:] = to_db(val)
    w = max(1, int(smooth_s * SR))
    k = np.ones(w) / w
    db = np.convolve(np.concatenate([np.full(w, db[0]), db, np.full(w, db[-1])]), k, mode="same")[w:-w]
    return 10 ** (db / 20)


def bass_envelope(cello: Voice, n: int, mode: str, threshold_cc1: int):
    if mode == "off":
        return None
    if mode == "on":
        return np.ones(n)
    g = np.zeros(n)
    if 22 in cello.cc:                               # explicit doubling amount
        for t, val in sorted(cello.cc[22]):
            g[int(t * SR):] = val / 127.0
    else:
        lo = threshold_cc1 - 10
        for t, val in cc1_curve(cello.cc.get(1, []), n / SR):
            g[int(t * SR):] = np.clip((val - lo) / 10.0, 0, 1)
    w = int(0.6 * SR)                                # never pops in
    k = np.hanning(w)
    k /= k.sum()
    g = np.convolve(np.concatenate([np.full(w, g[0]), g, np.full(w, g[-1])]), k, mode="same")[w:-w]
    return g if g.max() > 1e-3 else None


# ------------------------------------------------------------------- output
def true_peak(x: np.ndarray) -> float:
    up = resample_poly(x, 4, 1, axis=0)
    return float(np.max(np.abs(up)))


def export(y: np.ndarray, out: Path, peak_db: float):
    tp = true_peak(y)
    y = y * (10 ** (peak_db / 20) / tp)
    wav = out.with_suffix(".wav")
    m4a = out.with_suffix(".m4a")
    wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(wav), y.astype(np.float32), SR, subtype="PCM_24")
    if m4a.exists():
        m4a.unlink()
    if shutil.which("afconvert"):
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "256000", str(wav), str(m4a)], check=True)
    else:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "256k",
                        str(m4a)], check=True)
    return wav, m4a, 20 * math.log10(tp), 20 * math.log10(true_peak(y))


# --------------------------------------------------------------------- main
def parse_level(s: str) -> float:
    return float(LEVELS.get(s, s))


def sfz_for(lib: str, inst: str, sfz_dir: Path) -> Path:
    if lib == "vpo3":
        import vpo3
        return vpo3.VPO3_SFZ[vpo3.INST_PATCH[inst]]
    p = sfz_dir / INSTR[inst]["sfz"]
    return p if p.exists() else sfz_dir / "violin.sfz" if inst == "vn2" else p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Full MIDI conventions: python3 -c 'import render_quartet as r; print(r.__doc__)'",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("midi", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--lib", choices=["iowa", "vpo3"], default="iowa")
    ap.add_argument("--map")
    ap.add_argument("--bass-double", choices=["off", "on", "auto"], default="off")
    ap.add_argument("--bass-threshold", default="ff")
    ap.add_argument("--bass-level", type=float, default=-5.0, help="doubling bass trim in dB (default -5)")
    ap.add_argument("--hall", choices=["detmold", "synthetic", "none"], default="detmold")
    ap.add_argument("--wet", type=float, default=-2.0)
    ap.add_argument("--short-ms", type=float, default=260.0)
    ap.add_argument("--legato-xfade-ms", type=float, default=70.0)
    ap.add_argument("--cc11-depth", type=float, default=0.5)
    ap.add_argument("--stems", action="store_true")
    ap.add_argument("--report", type=Path)
    ap.add_argument("--keep-temp", action="store_true")
    ap.add_argument("--keep-start", action="store_true", help="do not trim leading silence (for measurements)")
    ap.add_argument("--peak", type=float, default=-1.0)
    ap.add_argument("--sfz-dir", type=Path, default=QUARTET_DIR)
    a = ap.parse_args(argv)

    if not SFIZZ_RENDER.exists():
        sys.exit(f"missing {SFIZZ_RENDER}: run setup_strings.sh")
    out = a.out or a.midi.with_suffix("")
    voices, marker = read_voices(a.midi)
    if not voices:
        sys.exit("no notes found")
    assign(voices, a.map)
    log = []
    if marker:
        log.append(f"MIDI written by perform.py (target={marker.get('target')})")
    for v in voices:
        if ensure_cc1(v):
            log.append(f"{v.name}: no CC1, dynamic level taken from note velocities")
    jobs: list[Job] = []
    rescue_range(voices, jobs, log)
    for v in voices:
        if v.notes:
            jobs.insert(0, Job(voice=v, notes=v.notes, inst=v.inst, kind="main", label=v.name))
    art_counts = {}
    for j in jobs:
        c = shape_articulation(j.notes, a.short_ms / 1000.0, a.legato_xfade_ms / 1000.0,
                               20 in j.voice.cc, 21 in j.voice.cc)
        art_counts[j.label] = c
    for j in jobs:                                    # compass check for what is left
        lo = INSTR[j.inst]["lo"] - EXT_DOWN
        hi = INSTR[j.inst]["hi"]
        bad = [n for n in j.notes if not lo <= n.key <= hi]
        for n in bad:
            while n.key < lo:
                n.key += 12
            while n.key > hi:
                n.key -= 12
        if bad:
            log.append(f"{j.label}: {len(bad)} notes outside the {INSTR[j.inst]['name']} compass octave-shifted")
    cello = next((v for v in voices if v.inst == "vc"), None)
    if cello is not None and not any(v.inst == "cb" for v in voices) and a.bass_double != "off":
        cn = [Note(n.on, n.off, n.key, n.vel, n.art, n.rel) for j in jobs if j.inst == "vc" for n in j.notes]
        cn.sort(key=lambda n: n.on)
        cn = [n for n in cn if n.key - 12 >= INSTR["cb"]["lo"] - EXT_DOWN]
        if cn:
            jobs.append(Job(voice=cello, notes=cn, inst="cb", kind="double", label="Contrabass 8vb (doubling)"))

    tmp = Path(tempfile.mkdtemp(prefix="quartet_"))
    tasks = []
    for i, j in enumerate(jobs):
        mp = tmp / f"j{i}_{j.inst}.mid"
        job_midi(j, transpose=-12 if j.kind == "double" else 0).save(str(mp))
        tasks.append((sfz_for(a.lib, j.inst, a.sfz_dir), mp, tmp / f"j{i}_{j.inst}.wav"))

    print(f"{a.midi.name}: {len(voices)} voices, library {a.lib}")
    for j in jobs:
        ks = [n.key for n in j.notes]
        c = art_counts.get(j.label, {})
        print(f"  {j.label:28s} -> {INSTR[j.inst]['name']:11s} {len(ks):4d} notes, keys {min(ks)}-{max(ks)}"
              + (f"  (normal {c.get('normal', 0)}, legato {c.get('legato', 0)}, short {c.get('short', 0)})"
                 if c else ""))
    for line in log:
        print("  note:", line)
    with ThreadPoolExecutor(min(6, os.cpu_count() or 4)) as ex:
        stems = list(ex.map(lambda t: run_sfizz(*t), tasks))

    n = max(len(s) for s in stems) + int(4.0 * SR)
    reverb = None if a.hall == "none" else hall.Hall(a.hall, SR)
    dry = np.zeros((n, 2))
    wet = np.zeros((n, 2))
    stem_out = {}
    level_report = {}
    thr_cc1 = level_to_cc1(parse_level(a.bass_threshold))
    for j, x in zip(jobs, stems):
        y = np.zeros((n, 2))
        y[: len(x)] = x
        g = gain_envelope(j.voice.cc.get(7), n, 127, lambda v: 40 * math.log10(max(v, 1) / 127))
        g *= gain_envelope(j.voice.cc.get(11), n, 127, lambda v: a.cc11_depth * 20 * math.log10(max(v, 1) / 127))
        g *= 10 ** (INSTR[j.inst]["trim"] / 20)
        if j.kind == "double":
            env = bass_envelope(j.voice, n, a.bass_double, thr_cc1)
            if env is None:
                log.append("bass doubling: cello never reaches the threshold, nothing added")
                continue
            g = g * env * 10 ** (a.bass_level / 20)
        y *= g[:, None]
        stem_out.setdefault(j.inst, np.zeros((n, 2)))
        stem_out[j.inst] += y
        dry += hall.place_dry(y, INSTR[j.inst]["az"], depth=INSTR[j.inst]["depth"])
        if reverb is not None:
            wet += reverb.source(y.mean(axis=1), INSTR[j.inst]["az"], a.wet)
    mix = dry + wet
    c80 = reverb.c80(10 ** (a.wet / 20)) if reverb is not None else None
    for inst, y in stem_out.items():
        mono = y.mean(axis=1)
        act = np.abs(mono) > 1e-5
        level_report[INSTR[inst]["name"]] = round(10 * math.log10(np.mean(mono[act] ** 2) + 1e-20), 2) \
            if act.any() else None
    env = np.max(np.abs(mix), axis=1)
    thr = env.max() * 10 ** (-80 / 20)
    idx = np.flatnonzero(env > thr)
    first = max(0, int(idx[0]) - int(0.25 * SR)) if len(idx) and not a.keep_start else 0
    last = int(idx[-1]) if len(idx) else len(mix)
    mix = mix[first: min(len(mix), last + int(0.3 * SR))]
    fade = int(0.3 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    wav, m4a, tp_pre, tp_post = export(mix, out, a.peak)
    print(f"hall={a.hall} wet={a.wet:+.1f} dB" + (f" (C80 {c80:+.1f} dB)" if c80 is not None else "")
          + f"  true peak {tp_post:+.2f} dBTP  -> {wav}, {m4a.name}  ({len(mix) / SR:.1f} s)")
    if a.stems:
        norm = 10 ** (a.peak / 20) / 10 ** (tp_pre / 20)
        for inst, y in stem_out.items():
            p = out.parent / f"{out.name}_stem_{inst}.wav"
            sf.write(str(p), (y[first: first + len(mix)] * norm).astype(np.float32), SR, subtype="FLOAT")
    if a.report:
        rep = dict(midi=str(a.midi), lib=a.lib, hall=a.hall, wet_db=a.wet, c80_db=c80, duration_s=len(mix) / SR,
                   true_peak_dbtp=tp_post, offset_s=first / SR,
                   jobs=[dict(label=j.label, inst=j.inst, kind=j.kind, notes=len(j.notes),
                              articulation=art_counts.get(j.label),
                              note_list=[(round(n.on, 4), round(n.off, 4), n.key, n.vel, n.art)
                                         for n in j.notes]) for j in jobs],
                   cc1={v.inst: [(round(t, 3), val) for t, val in v.cc.get(1, [])] for v in voices},
                   stem_rms_db_when_active=level_report, notes=log)
        a.report.write_text(json.dumps(rep, indent=1))
    if a.keep_temp:
        print("temp:", tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    return wav, m4a


if __name__ == "__main__":
    main()
