#!/usr/bin/env python3
"""Render a multi-voice MIDI file as a solo string quartet (+ optional double bass).

Engine: sfizz (sfizz_render, patched for 32-bit float output) playing the
Iowa MIS quartet SFZ instruments built by iowa_build.py.  Every voice is
rendered separately, then placed on a virtual stage and convolved with
measured concert-hall impulse responses (3D-MARCo, St Paul's Hall,
Huddersfield) or a synthetic hall, mixed, normalised and exported.

USAGE
  python3 render_quartet.py INPUT.mid [-o OUT_BASENAME] [options]

  -o, --out PATH        output basename (default: INPUT without suffix);
                        writes PATH.wav (48 kHz / 24-bit stereo) and PATH.m4a
                        (AAC 256 kb/s via afconvert)
  --map SPEC            explicit voice -> instrument map, comma separated, e.g.
                        "Soprano=vn1,Alto=vn2,Tenor=va,Bass=vc" (keys match a
                        track name substring, case-insensitive) or by voice
                        index "0=vn1,1=vn2,2=va,3=vc".  Instruments: vn1 vn2 va vc cb
  --bass MODE           octave doubling of the cello by a double bass:
                        off | on | auto (default auto: fades in where the cello's
                        CC1 is above --bass-threshold, i.e. forte/tutti climaxes).
                        A cello track may also carry CC22 (0-127) = explicit
                        doubling amount, which overrides auto.
  --bass-threshold N    CC1 value where auto doubling reaches full level (default 100;
                        it starts fading in 16 below)
  --bass-level DB       level of the doubling bass relative to its own
                        calibration (default -4)
  --hall NAME           marco (measured, default if installed) | synthetic | none
  --wet DB / --dry DB   reverb and direct (spot) levels (defaults -1 / -6 dB)
  --short-ms MS         notes shorter than this get the 'short' articulation
                        unless the voice carries its own CC20 (default 190)
  --legato-xfade-ms MS  crossfade length for overlapping (slurred) notes (default 70)
  --stems               also write the dry per-voice stems next to the output
  --keep-temp           keep the per-voice MIDI/WAV temp files
  --peak DB             normalisation peak (default -1.0 dBFS)

INPUT MIDI CONVENTIONS (what a performance script should emit)
  * One voice per track (type 1), or per channel in a type-0 file.  Voices
    are mapped by --map, else by track name (violin 1/I, violin 2/II, viola,
    cello/violoncello, contrabass/double bass), else by GM program (40 violin,
    41 viola, 42 cello, 43 contrabass), else by mean pitch (highest -> vn1).
  * Note velocity = attack/accent: 127 = full recorded bow bite, ~60 = gentle
    start, ~20 = very soft swell-in.  It changes level only slightly (30 %).
  * CC1  (mod wheel) = dynamics with real timbre change: crossfades the
    recorded pp / mf / ff layers.  0 ppp, 16 pp, 40 p, 52 mp, 64 mf, 88 f,
    112 ff, 127 fff.  Continuous: use it for crescendo/diminuendo and phrase
    shaping inside held notes.
  * CC11 (expression) = extra per-voice gain, GM curve 40*log10(v/127) dB
    (default 127).  Use for fine balance / hairpins that should not change timbre.
  * CC7  (channel volume) = static balance, same curve (default 127 = 0 dB;
    note GM files often send 100 = -4.2 dB).
  * CC10 (pan) is ignored: the stage position of each instrument is fixed.
  * CC20 (articulation, optional): 0-63 normal, 64-95 legato (slurred), 96-127
    short.  If absent it is inferred: overlapping notes (next note-on before
    the previous note-off) are slurred with a --legato-xfade-ms crossfade,
    notes shorter than --short-ms are short, everything else is a new bow.
  * CC21 (release, optional): release time = 0.03 + 2.0*v/127 s to -78 dB.  If
    absent it is inferred from context (slur 0.12 s, re-bow 0.2 s, short note
    0.18 s, before a rest 0.5-1.0 s depending on note length).
  * Pitch bend: +-2 semitones.  Tempo map: honoured (all timing is converted
    to seconds before rendering, so rubato via tempo events works).

EXAMPLES
  python3 render_quartet.py ../../score/ricercar_performance.mid -o out/ricercar
  python3 render_quartet.py demo.mid --bass on --hall synthetic --stems
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
from scipy.signal import resample_poly

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from iowa_common import QUARTET_DIR, SFIZZ_RENDER  # noqa: E402
import hall  # noqa: E402

SR = 48000
INSTR = {
    # id: (sfz file, display name, stage azimuth deg (ITU: + = left), depth m, gain dB)
    "vn1": ("violin.sfz", "Violin I", 38.0, 0.0, 0.0),
    "vn2": ("violin.sfz", "Violin II", 13.0, 0.3, -0.5),
    "va": ("viola.sfz", "Viola", -13.0, 0.3, 0.5),
    "vc": ("cello.sfz", "Cello", -36.0, 0.0, 0.5),
    "cb": ("bass.sfz", "Contrabass", -45.0, 1.2, 0.0),
}
NAME_KEYS = [
    ("vn1", ["violin 1", "violin i", "vln 1", "vln. 1", "vn1", "vn 1", "violino i", "violin1", "1st violin", "first violin"]),
    ("vn2", ["violin 2", "violin ii", "vln 2", "vln. 2", "vn2", "vn 2", "violino ii", "violin2", "2nd violin", "second violin"]),
    ("va", ["viola", "vla", "alto viol"]),
    ("vc", ["cello", "violoncello", "vlc", "vc"]),
    ("cb", ["contrabass", "double bass", "doublebass", "kontrabass", "cb", "bass"]),
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
        i = max(0, np.searchsorted(ticks, tick, side="right") - 1)
        return secs[i] + (tick - ticks[i]) * changes[i][1] / 1e6 / tpb
    return f


def read_voices(path: Path) -> list[Voice]:
    mid = mido.MidiFile(str(path))
    t2s = tempo_map(mid)
    voices: dict[tuple[int, int], Voice] = {}
    for ti, tr in enumerate(mid.tracks):
        name = f"track{ti}"
        tick = 0
        pending: dict[tuple[int, int], list] = {}
        prog = {}
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
                prog[msg.channel] = msg.program
    out = [v for v in voices.values() if v.notes]
    for v in out:
        v.notes.sort(key=lambda n: (n.on, -n.key))
    return out


def assign(voices: list[Voice], spec: str | None):
    if spec:
        for item in spec.split(","):
            k, inst = item.split("=")
            k, inst = k.strip(), inst.strip()
            for i, v in enumerate(voices):
                if (k.isdigit() and int(k) == i) or (not k.isdigit() and k.lower() in v.name.lower()):
                    v.inst = inst
    for v in voices:
        if v.inst:
            continue
        nm = v.name.lower()
        for inst, keys in NAME_KEYS:
            if any(k == nm or k in nm for k in keys):
                v.inst = inst
                break
    # GM programs / pitch order for the rest
    rest = [v for v in voices if not v.inst]
    taken = {v.inst for v in voices if v.inst}
    order = ["vn1", "vn2", "va", "vc", "cb"]
    for v in sorted(rest, key=lambda v: -v.mean_pitch):
        fam = PROGRAM.get(v.program or -1)
        cands = [o for o in order if o not in taken and (fam is None or o.startswith(fam))]
        if not cands:
            cands = [o for o in order if o not in taken] or ["vn1"]
        v.inst = cands[0]
        taken.add(v.inst)
    return voices


# ------------------------------------------------------- articulation logic
def rel_cc(seconds: float) -> int:
    return int(np.clip(round((seconds - 0.03) / 2.0 * 127), 0, 127))


def shape_articulation(v: Voice, short_s: float, xfade_s: float):
    """Infer CC20 (articulation) and CC21 (release) per note; trim slurred
    notes so the previous note fades out under the next one."""
    has_art = 20 in v.cc
    has_rel = 21 in v.cc
    notes = v.notes
    for i, n in enumerate(notes):
        prev = notes[i - 1] if i else None
        nxt = notes[i + 1] if i + 1 < len(notes) else None
        dur = n.off - n.on
        chord_prev = prev is not None and abs(n.on - prev.on) < 0.03
        slur_in = prev is not None and not chord_prev and prev.off > n.on + 0.005
        if not has_art:
            n.art = 80 if slur_in else (112 if dur < short_s else 0)
        chord_next = nxt is not None and abs(nxt.on - n.on) < 0.03
        slur_out = nxt is not None and not chord_next and n.off > nxt.on + 0.005
        gap = (nxt.on - n.off) if nxt is not None else 99.0
        if slur_out:
            n.off = min(n.off, nxt.on + xfade_s)
            rel = 0.12
        elif gap < 0.04:
            rel = 0.18 if dur < short_s else 0.22
        elif dur < short_s:
            rel = 0.22
        else:
            rel = float(np.clip(0.45 + 0.25 * dur, 0.5, 1.1))
        if not has_rel:
            n.rel = rel_cc(rel)


# ------------------------------------------------------------- per voice MIDI
TPB_OUT = 960
TEMPO_OUT = 500000                      # 120 bpm -> 1920 ticks per second


def sec2tick(t: float) -> int:
    return int(round(t * TPB_OUT * 1e6 / TEMPO_OUT))


def voice_midi(v: Voice, transpose: int = 0, extra_cc: dict | None = None) -> mido.MidiFile:
    ev = []   # (tick, prio, msg)
    cc = dict(v.cc)
    if extra_cc:
        cc.update(extra_cc)
    first_cc1 = cc.get(1, [(0, 64)])[0][1]
    ev.append((0, 0, mido.Message("control_change", control=1, value=first_cc1)))
    for num in (1, 20, 21, 64):
        for t, val in cc.get(num, []):
            if num == 64:
                continue            # sustain pedal is meaningless for bowed strings
            ev.append((sec2tick(t), 1, mido.Message("control_change", control=num, value=val)))
    for t, val in v.bend:
        ev.append((sec2tick(t), 1, mido.Message("pitchwheel", pitch=val)))
    for n in v.notes:
        k = n.key + transpose
        if not 0 <= k <= 127:
            continue
        ton, toff = sec2tick(n.on), sec2tick(n.off)
        if n.art is not None:
            ev.append((ton, 2, mido.Message("control_change", control=20, value=n.art)))
        if n.rel is not None:
            ev.append((ton, 2, mido.Message("control_change", control=21, value=n.rel)))
        ev.append((ton, 4, mido.Message("note_on", note=k, velocity=max(1, n.vel))))
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
def cc_envelope(events, n: int, default: int, smooth_s: float = 0.012):
    """Sample-and-hold CC curve -> per-sample gain (GM: (v/127)^2), smoothed."""
    vals = np.full(n, default / 127.0, dtype=np.float64)
    for t, val in sorted(events or []):
        i = int(t * SR)
        if i < n:
            vals[i:] = val / 127.0
    g = vals ** 2
    w = max(1, int(smooth_s * SR))
    k = np.ones(w) / w
    g = np.convolve(np.concatenate([np.full(w, g[0]), g]), k, mode="same")[w:]
    return g


def bass_envelope(cello: Voice, n: int, mode: str, threshold: int):
    if mode == "off":
        return None
    if mode == "on":
        return np.ones(n)
    if 22 in cello.cc:                               # explicit doubling amount
        ev = cello.cc[22]
        g = np.zeros(n)
        for t, val in sorted(ev):
            g[int(t * SR):] = val / 127.0
    else:
        ev = cello.cc.get(1, [(0.0, 64)])
        g = np.zeros(n)
        lo = threshold - 16
        for t, val in sorted(ev):
            g[int(t * SR):] = np.clip((val - lo) / 16.0, 0, 1)
    # smooth over 0.6 s so the bass never pops in
    w = int(0.6 * SR)
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
    if shutil.which("afconvert"):
        if m4a.exists():
            m4a.unlink()
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "256000", str(wav), str(m4a)], check=True)
    else:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "256k",
                        str(m4a)], check=True)
    return wav, m4a, 20 * math.log10(tp)


# --------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="See the module docstring (python3 -c 'import render_quartet; "
                                        "help(render_quartet)') for MIDI conventions.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("midi", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    ap.add_argument("--map")
    ap.add_argument("--bass", choices=["off", "on", "auto"], default="auto")
    ap.add_argument("--bass-threshold", type=int, default=100)
    ap.add_argument("--bass-level", type=float, default=-4.0)
    ap.add_argument("--hall", choices=["marco", "synthetic", "none"], default=None)
    ap.add_argument("--wet", type=float, default=-1.0)
    ap.add_argument("--dry", type=float, default=-6.0)
    ap.add_argument("--short-ms", type=float, default=190.0)
    ap.add_argument("--legato-xfade-ms", type=float, default=70.0)
    ap.add_argument("--stems", action="store_true")
    ap.add_argument("--keep-temp", action="store_true")
    ap.add_argument("--peak", type=float, default=-1.0)
    ap.add_argument("--sfz-dir", type=Path, default=QUARTET_DIR)
    a = ap.parse_args(argv)

    out = a.out or a.midi.with_suffix("")
    voices = assign(read_voices(a.midi), a.map)
    if not voices:
        sys.exit("no notes found")
    for v in voices:
        shape_articulation(v, a.short_ms / 1000.0, a.legato_xfade_ms / 1000.0)
    tmp = Path(tempfile.mkdtemp(prefix="quartet_"))
    jobs = []
    for i, v in enumerate(voices):
        sfz = a.sfz_dir / INSTR[v.inst][0]
        mp = tmp / f"v{i}_{v.inst}.mid"
        voice_midi(v).save(str(mp))
        jobs.append((v, v.inst, sfz, mp, tmp / f"v{i}_{v.inst}.wav", None))
    cello = next((v for v in voices if v.inst == "vc"), None)
    has_cb = any(v.inst == "cb" for v in voices)
    if cello is not None and not has_cb and a.bass != "off":
        mp = tmp / "double_cb.mid"
        voice_midi(cello, transpose=-12).save(str(mp))
        jobs.append((cello, "cb", a.sfz_dir / INSTR["cb"][0], mp, tmp / "double_cb.wav", "double"))

    print(f"{a.midi.name}: {len(voices)} voices")
    for v in voices:
        print(f"  {v.name!r:28s} ch{v.channel:<2d} -> {INSTR[v.inst][1]:11s} {len(v.notes):4d} notes, "
              f"range {min(n.key for n in v.notes)}-{max(n.key for n in v.notes)}")
    with ThreadPoolExecutor(min(6, os.cpu_count() or 4)) as ex:
        stems = list(ex.map(lambda j: run_sfizz(j[2], j[3], j[4]), jobs))

    n = max(len(s) for s in stems) + int(4.5 * SR)
    hall_name = a.hall or ("marco" if hall.marco_available() else "synthetic")
    reverb = None if hall_name == "none" else hall.Hall(hall_name, SR)
    mix = np.zeros((n, 2))
    dry_g = 10 ** (a.dry / 20)
    wet_g = 10 ** (a.wet / 20)
    stem_out = {}
    for (v, inst, sfz, mp, wav, kind), x in zip(jobs, stems):
        y = np.zeros((n, 2))
        y[: len(x)] = x
        g = cc_envelope(v.cc.get(7), n, 127) * cc_envelope(v.cc.get(11), n, 127)
        g *= 10 ** (INSTR[inst][4] / 20)
        if kind == "double":
            env = bass_envelope(v, n, a.bass, a.bass_threshold)
            if env is None:
                continue
            g = g * env * 10 ** (a.bass_level / 20)
        y *= g[:, None]
        label = INSTR[inst][1] if kind is None else "Contrabass (8vb doubling)"
        stem_out[label] = y
        az = INSTR[inst][2]
        mix += dry_g * hall.place_dry(y, az)
        if reverb is not None:
            mix += wet_g * reverb.convolve(y.mean(axis=1), az, INSTR[inst][3])
    # trim trailing silence (keep 0.5 s after the tail falls below -90 dBFS)
    env = np.max(np.abs(mix), axis=1)
    thr = env.max() * 10 ** (-90 / 20)
    last = int(np.flatnonzero(env > thr)[-1]) if np.any(env > thr) else len(mix)
    mix = mix[: min(len(mix), last + int(0.5 * SR))]
    fade = int(0.3 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    wav, m4a, tp = export(mix, out, a.peak)
    print(f"hall={hall_name}  pre-normalisation true peak {tp:+.1f} dBFS  -> {wav.name}, {m4a.name}  "
          f"({len(mix) / SR:.1f} s)")
    if a.stems:
        for label, y in stem_out.items():
            p = out.parent / f"{out.name}_stem_{label.split()[0].lower()}{'2' if label.endswith('II') else ''}.wav"
            sf.write(str(p), y[: len(mix)].astype(np.float32), SR, subtype="FLOAT")
    if a.keep_temp:
        print("temp:", tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    return wav, m4a


if __name__ == "__main__":
    main()
