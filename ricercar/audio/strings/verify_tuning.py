#!/usr/bin/env python3
"""Independent tuning check of a built string instrument, through the real
playback chain (SFZ -> sfizz -> WAV).

For every key of the instrument's range and for every dynamic layer
(pp / mf / ff, selected with the CC1 value at which that layer plays alone)
a 2 s note is rendered with sfizz; the sounding pitch is measured with a YIN
estimator (a different algorithm from the harmonic-comb estimator that
iowa_analyze.py used to derive the tune= corrections) as the median over the
steady part of the note, so vibrato averages out.  Reports every note whose
pitch error exceeds --tol cents (default 15) or that sounds a wrong note.

Usage:
  python3 verify_tuning.py violin viola cello [--lib iowa|vpo3] [--json OUT]
  exit status 1 if any note fails.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import mido
import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from iowa_common import INSTRUMENTS, QUARTET_DIR, SFIZZ_RENDER, midi_name, midi_to_hz  # noqa: E402

SR = 48000
NOTE_S, STEP_S = 2.0, 2.6


def yin(x: np.ndarray, sr: int, fmin: float, fmax: float, W: int = 2048, hop: int = 512, thr: float = 0.12):
    """YIN (de Cheveigne & Kawahara 2002) -> per-frame f0 (Hz, nan if unvoiced)."""
    tmax = int(sr / fmin) + 2
    tmin = max(2, int(sr / fmax) - 1)
    out = []
    n = len(x)
    for s in range(0, n - W - tmax, hop):
        fr = x[s: s + W + tmax].astype(np.float64)
        # difference function via FFT autocorrelation
        L = 1 << int(np.ceil(np.log2(2 * (W + tmax))))
        F = np.fft.rfft(fr, L)
        a = np.fft.irfft(F * np.conj(np.fft.rfft(fr[:W], L)), L)[: tmax]
        c = np.concatenate([[0.0], np.cumsum(fr ** 2)])
        e0 = c[W] - c[0]
        et = c[np.arange(tmax) + W] - c[np.arange(tmax)]
        d = e0 + et - 2 * a
        d[0] = 0
        cm = np.ones_like(d)
        cs = np.cumsum(d[1:])
        cm[1:] = d[1:] * np.arange(1, tmax) / np.maximum(cs, 1e-20)
        cand = np.flatnonzero(cm[tmin:] < thr)
        if len(cand) == 0:
            out.append(np.nan)
            continue
        t = tmin + cand[0]
        while t + 1 < tmax and cm[t + 1] < cm[t]:
            t += 1
        if 1 <= t < tmax - 1:
            y0, y1, y2 = cm[t - 1], cm[t], cm[t + 1]
            den = y0 - 2 * y1 + y2
            tt = t + (0.5 * (y0 - y2) / den if abs(den) > 1e-12 else 0.0)
        else:
            tt = t
        out.append(sr / tt)
    return np.array(out)


def layer_cc1(lib: str) -> dict:
    if lib == "iowa":
        from iowa_build import LAYER_CC1
        return dict(LAYER_CC1)
    return {"single": 100}


def make_midi(keys, cc1: int, path: Path):
    mid = mido.MidiFile(type=0, ticks_per_beat=960)
    tr = mido.MidiTrack()
    tr.append(mido.MetaMessage("set_tempo", tempo=500000))       # 1920 ticks / s
    tps = 1920
    ev = [(0, mido.Message("control_change", control=1, value=cc1)),
          (0, mido.Message("control_change", control=11, value=127))]
    for i, k in enumerate(keys):
        t0 = int((0.2 + i * STEP_S) * tps)
        ev.append((t0, mido.Message("note_on", note=k, velocity=100)))
        ev.append((t0 + int(NOTE_S * tps), mido.Message("note_off", note=k, velocity=0)))
    ev.sort(key=lambda e: e[0])
    last = 0
    for t, m in ev:
        tr.append(m.copy(time=t - last))
        last = t
    tr.append(mido.MetaMessage("end_of_track", time=tps))
    mid.tracks.append(tr)
    mid.save(str(path))


def check(sfz: Path, keys: list[int], cc1: int, tmp: Path, tag: str):
    mp, wp = tmp / f"{tag}.mid", tmp / f"{tag}.wav"
    make_midi(keys, cc1, mp)
    r = subprocess.run([str(SFIZZ_RENDER), "--sfz", str(sfz), "--midi", str(mp), "--wav", str(wp),
                        "-s", str(SR), "-q", "3"], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    x, _ = sf.read(str(wp), dtype="float64", always_2d=True)
    m = x.mean(axis=1)
    rows = []
    for i, k in enumerate(keys):
        a = int((0.2 + i * STEP_S + 0.45) * SR)
        b = int((0.2 + i * STEP_S + NOTE_S - 0.1) * SR)
        seg = m[a:b]
        lvl = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12)
        f = midi_to_hz(k)
        # wide search: one octave down to a fifth up, catches wrong notes / octave slips
        f0 = yin(seg, SR, f / 2.05, f * 1.55)
        f0 = f0[np.isfinite(f0)]
        if len(f0) < 5:
            rows.append(dict(key=k, name=midi_name(k), cents=None, level_db=round(lvl, 1), voiced=len(f0)))
            continue
        cents = 1200 * np.log2(f0 / f)
        med = float(np.median(cents))
        rows.append(dict(key=k, name=midi_name(k), cents=round(med, 1),
                         spread=round(float(np.percentile(cents, 75) - np.percentile(cents, 25)), 1),
                         level_db=round(lvl, 1), voiced=int(len(f0))))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inst", nargs="+")
    ap.add_argument("--lib", default="iowa", choices=["iowa", "vpo3"])
    ap.add_argument("--tol", type=float, default=15.0)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="tune_"))
    report, fails = {}, 0
    for inst in a.inst:
        if a.lib == "iowa":
            sfz = QUARTET_DIR / f"{inst}.sfz"
            lo, hi = INSTRUMENTS[inst]["lo"], INSTRUMENTS[inst]["hi"]
        else:
            from vpo3 import VPO3_SFZ, VPO3_RANGE
            sfz = VPO3_SFZ[inst]
            lo, hi = VPO3_RANGE[inst]
        keys = list(range(lo, hi + 1))
        report[inst] = {}
        for layer, cc in layer_cc1(a.lib).items():
            rows = check(sfz, keys, cc, tmp, f"{inst}_{layer}")
            report[inst][layer] = rows
            bad = [r for r in rows if r["cents"] is None or abs(r["cents"]) > a.tol]
            fails += len(bad)
            c = np.array([r["cents"] for r in rows if r["cents"] is not None])
            print(f"{inst:7s} {layer:6s} keys {midi_name(lo)}-{midi_name(hi)}: median |err| "
                  f"{np.median(np.abs(c)):.1f} c, max |err| {np.max(np.abs(c)):.1f} c, "
                  f"{len(bad)} over {a.tol:g} c" + ("" if not bad else ": " + ", ".join(
                      f"{r['name']}({r['cents']})" for r in bad)))
    if a.json:
        a.json.write_text(json.dumps(report, indent=1))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
