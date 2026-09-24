#!/usr/bin/env python3
"""Stage 3 of the Iowa quartet build: turn the analysed Iowa MIS arco notes into
playable, expressive SFZ instruments for sfizz.

For every instrument (violin, viola, cello, bass) and every chromatic note it
  1. picks one string per note (the normal fingering: the highest string whose
     open pitch is below the note; open-string pitches prefer the stopped note
     on the next lower string so vibrato stays continuous), the same string for
     pp, mf and ff so the dynamic crossfade stays within one timbre family;
  2. high-passes the note just below its fundamental (the recordings carry
     building rumble below 60 Hz), trims it to the bow onset, resamples to 48 kHz;
  3. extends the sustain to SUSTAIN_S seconds by pitch-synchronous grain
     splicing (cross-correlation matched splice points, 70 ms crossfades, random
     grain order, slow level normalisation) so long notes never loop audibly;
  4. measures the A-weighted steady level of each note, smooths the level across
     the range, and calibrates the three layers to fixed loudness steps
     (ff = 0 dB, mf = -6.5 dB, pp = -16 dB) so CC1 behaves predictably;
  5. writes <inst>.sfz with:
       CC1   dynamics on the perform.py scale (ppp 36, pp 49, p 62, mp 75, mf 88,
             f 101, ff 114, fff 127): equal-power crossfade of the recorded layers
             pp (<=49) -> mf (88) -> ff (>=114) plus a volume curve so loudness
             moves about 3.5 dB per dynamic step (CC1_TARGET)
       CC20  articulation (set by render_quartet.py before each note-on):
             0-63 normal bow stroke (recorded attack, slow swells shortened),
             64-95 legato (slurred: starts in the sustain, 40-70 ms fade-in),
             96-127 short (crisp onset, small accent decay, for fast notes)
       CC21  release time: 0.03 s + 1.2 s * cc21/127
       vel   attack softness (vel 127 = the recorded bite, vel 1 = 100 ms fade-in)
             and a gentle accent (amp_veltrack 30 %)
       pitch bend +-2 semitones.
     CC11/CC7 are applied by render_quartet.py as post-gain on each voice.

Usage:  python3 iowa_build.py [--only violin,viola] [--jobs 10] [--sustain 10]
Outputs: IowaMIS/quartet/{violin,viola,cello,bass}.sfz and samples/<inst>/*.wav
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from fractions import Fraction
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import bilinear, butter, lfilter, resample_poly, sosfiltfilt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from iowa_common import (DYNAMICS, INSTRUMENTS, QUARTET_DIR, RAW_DIR, load_audio, load_iowa,  # noqa: E402
                         midi_name, midi_to_hz)

SR = 48000
SUSTAIN_S = 10.0
# CC1 scale = the one ricercar/tools/perform.py writes for --target strings:
#   value = 36 + 13 * (level - 1), level ppp=1 pp=2 p=3 mp=4 mf=5 f=6 ff=7 fff=8
#   -> ppp 36, pp 49, p 62, mp 75, mf 88, f 101, ff 114, fff 127
# Each recorded layer plays alone at its anchor and is crossfaded (equal power)
# with its neighbour in between: pp <= 49, pp->mf 49..88, mf->ff 88..114, ff >= 114.
LAYER_CC1 = {"pp": 49, "mf": 88, "ff": 114}
XF = {"pp": (0, 49, 49, 88), "mf": (49, 88, 88, 114), "ff": (88, 114, 114, 127)}
# loudness of each layer at its anchor (dB re ff) = the CC1 target there, so the
# compensation curve is 0 dB at the anchors and only evens out the crossfades
LAYER_DB = {"pp": -16.0, "mf": -6.5, "ff": 0.0}
REF_DB = -20.0          # A-weighted steady level of the ff layer mid-range (dBFS, before volume=-6)
# CC1 -> target loudness (dB, relative to the ff layer); about 3.5 dB per dynamic step
CC1_TARGET = [(0, -30.0), (20, -24.5), (36, -20.0), (49, -16.0), (62, -12.5), (75, -9.5), (88, -6.5),
              (101, -3.2), (114, 0.0), (127, 1.5)]
# articulation timing (s): 'normal' notes keep at most NORMAL_RISE of the recorded
# rise before the note reaches steady-3 dB (Iowa players often swell into pp/mf
# notes for 0.3-0.6 s, far too slow for eighth notes); 'short' notes keep SHORT_RISE
NORMAL_RISE = 0.14
SHORT_RISE = 0.035


# --------------------------------------------------------------------------- DSP
def a_weighting(fs: int):
    f1, f2, f3, f4, a1000 = 20.598997, 107.65265, 737.86223, 12194.217, 1.9997
    nums = [(2 * np.pi * f4) ** 2 * (10 ** (a1000 / 20)), 0, 0, 0, 0]
    dens = np.polymul([1, 4 * np.pi * f4, (2 * np.pi * f4) ** 2], [1, 4 * np.pi * f1, (2 * np.pi * f1) ** 2])
    dens = np.polymul(np.polymul(dens, [1, 2 * np.pi * f3]), [1, 2 * np.pi * f2])
    return bilinear(nums, dens, fs)


AW_B, AW_A = a_weighting(SR)


def a_level_db(x: np.ndarray) -> float:
    y = lfilter(AW_B, AW_A, x.mean(axis=1) if x.ndim == 2 else x)
    return float(10 * np.log10(np.mean(y.astype(np.float64) ** 2) + 1e-20))


def hpf(x, sr, fc, order=4):
    sos = butter(order, fc, btype="highpass", fs=sr, output="sos")
    return sosfiltfilt(sos, x, axis=0)


def rms_track(mono, win):
    k = np.ones(win) / win
    return np.sqrt(np.convolve(mono.astype(np.float64) ** 2, k, mode="same") + 1e-20)


def best_align(mono, ref_end, q_center, W, search):
    """Return q (near q_center) maximising the normalised cross-correlation of
    mono[q-W:q] with mono[ref_end-W:ref_end]."""
    ref = mono[ref_end - W: ref_end]
    lo = max(W, q_center - search)
    hi = min(len(mono), q_center + search)
    if hi <= lo:
        return q_center, -1.0
    seg = mono[lo - W: hi]
    # correlation of ref with every window ending in [lo, hi)
    c = np.correlate(seg, ref, mode="valid")[: hi - lo]
    e = np.sqrt(np.convolve(seg ** 2, np.ones(W), mode="valid")[: hi - lo] * np.dot(ref, ref) + 1e-20)
    ncc = c / e
    i = int(np.argmax(ncc))
    return lo + i, float(ncc[i])


def extend_sustain(x: np.ndarray, sr: int, f0: float, s0: int, s1: int, total: int, seed: int,
                   cut: int | None = None):
    """Grow x to `total` samples by splicing grains from the steady region [s0, s1).

    Output = x[:cut] (attack + natural steady part) followed by grains taken
    from the steady region in random order; every splice point is aligned by
    normalised cross-correlation (waveform + vibrato phase) and crossfaded."""
    rng = np.random.default_rng(seed)
    mono = x.mean(axis=1).astype(np.float64)
    period = sr / f0
    W = int(max(0.035 * sr, 3 * period))
    XFL = int(0.07 * sr)
    s0 = max(s0, W + 1)
    s1 = min(s1, len(x) - XFL - 1)
    if s1 - s0 < int(0.25 * sr):
        s0 = max(W + 1, s1 - int(0.25 * sr))
    cut = min(cut if cut is not None else s1 - XFL, s1 - XFL)
    out = [x[:cut]]
    n = cut
    cur = cut                           # next source sample of the current grain
    fade_in = np.sin(0.5 * np.pi * (np.arange(XFL) + 0.5) / XFL) ** 2
    fade_out = 1.0 - fade_in
    last_q = -10 ** 9
    min_grain = int(0.18 * sr)
    avail = s1 - XFL - s0
    while n < total:
        # pick a new grain start among random candidates, keep the best-aligned
        best = None
        for _ in range(24):
            hi_q = s1 - XFL - min_grain
            if hi_q <= s0:
                q0 = s0
            else:
                q0 = int(rng.integers(s0, hi_q))
            if abs(q0 - cur) < 0.12 * sr or abs(q0 - last_q) < 0.1 * sr:
                if avail > 0.6 * sr:
                    continue
            q, ncc = best_align(mono, cur, q0, W, int(period) + 2)
            if best is None or ncc > best[1]:
                best = (q, ncc)
        q = best[0] if best else s0
        q = int(np.clip(q, s0, s1 - XFL - 1))
        a = x[cur: cur + XFL]
        b = x[q: q + XFL]
        m = min(len(a), len(b))
        out.append(a[:m] * fade_out[:m, None] + b[:m] * fade_in[:m, None])
        n += m
        g_len = int(rng.uniform(0.25, 0.7) * sr)
        start = q + m
        stop = min(start + g_len, s1 - XFL)
        if stop <= start:
            stop = min(start + min_grain, len(x) - XFL - 1)
        out.append(x[start:stop])
        n += stop - start
        cur = stop
        last_q = q
    y = np.concatenate(out, axis=0)[:total]
    # slow level normalisation toward the level of the stable window, from the
    # end of the attack onward (keeps the recorded bow attack untouched)
    steady = np.sqrt(np.mean(mono[s0:s1] ** 2) + 1e-20)
    r = rms_track(y.mean(axis=1), int(0.3 * sr))
    g = np.clip(steady / r, 10 ** (-6 / 20), 10 ** (6 / 20))
    ramp = np.clip((np.arange(len(y)) - (s0 - int(0.05 * sr))) / (0.25 * sr), 0, 1)
    g = 1.0 + (g - 1.0) * ramp
    return (y * g[:, None]).astype(np.float32)


def stable_window(x: np.ndarray, sr: int, att_s: float, sus_end_s: float):
    """Most stable stretch of the sustained note (flat envelope, early preferred)
    -> (start, end) in samples.  Protects against notes that were recorded with
    a swell or a fading bow."""
    db, hop = rms_db_track(x.mean(axis=1), sr)
    a = int((att_s + 0.04) * sr / hop)
    e = max(a + 5, int(sus_end_s * sr / hop))
    length = float(np.clip(0.45 * (e - a) * hop / sr, 0.35, 1.2))
    w = int(length * sr / hop)
    if e - a <= w:
        return a * hop, e * hop
    best, arg = 1e9, a
    for i in range(a, e - w + 1, 2):
        seg = db[i:i + w]
        slope = abs(np.polyfit(np.arange(w) * hop / sr, seg, 1)[0])
        score = np.std(seg) + 0.5 * slope + 0.4 * (i - a) * hop / sr
        if score < best:
            best, arg = score, i
    return arg * hop, (arg + w) * hop


def rms_db_track(mono, sr, win_s=0.02):
    hop = int(win_s * sr)
    n = len(mono) // hop
    fr = mono[: n * hop].reshape(n, hop).astype(np.float64)
    return 10 * np.log10(np.mean(fr ** 2, axis=1) + 1e-20), hop


def find_loop(mono: np.ndarray, sr: int, f0: float):
    """Loop points inside the (already extended) sustain tail, for notes longer
    than SUSTAIN_S; aligned by cross-correlation."""
    end = len(mono) - int(0.25 * sr)
    W = int(max(0.035 * sr, 3 * sr / f0))
    q, _ = best_align(mono, end, end - int(2.5 * sr), W, int(sr / f0) + 2)
    return q, end


# ------------------------------------------------------------------ selection
def load_analysis():
    data = json.loads((QUARTET_DIR / "analysis.json").read_text())
    table = defaultdict(list)       # (inst, dyn, midi) -> [candidates]
    for r in data:
        for n in r["notes"]:
            if n.get("junk"):
                continue
            table[(r["inst"], r["dyn"], n["midi"])].append(dict(file=r["file"], string=r["string"], hpf=r["hpf"], **n))
    return table


def string_pref(inst: str, midi: int) -> list[str]:
    strings = INSTRUMENTS[inst]["strings"]
    order = sorted(strings, key=lambda s: strings[s])              # low -> high
    below = [s for s in order if strings[s] < midi]
    first = below[-1] if below else order[0]
    rest = sorted(order, key=lambda s: (s != first, abs(strings[s] - strings[first]), -strings[s]))
    return rest


def choose(inst: str, table) -> dict:
    """-> {(dyn, midi): candidate}."""
    keys = sorted({m for (i, d, m) in table if i == inst})
    picks = {}
    for midi in keys:
        pref = string_pref(inst, midi)

        def ok(c):
            return c["body_s"] >= 0.45 and abs(c["cents"]) < 60

        # string that has all three dynamics (in preference order), else most
        best_s, best_cov = None, -1
        for s in pref:
            cov = sum(any(c["string"] == s and ok(c) for c in table.get((inst, d, midi), [])) for d in DYNAMICS)
            if cov > best_cov:
                best_s, best_cov = s, cov
        for d in DYNAMICS:
            cands = [c for c in table.get((inst, d, midi), []) if ok(c)]
            if not cands:
                continue
            same = [c for c in cands if c["string"] == best_s]
            if same:
                picks[(d, midi)] = max(same, key=lambda c: c["body_s"])
            else:
                picks[(d, midi)] = sorted(cands, key=lambda c: pref.index(c["string"]))[0]
    return picks


# ----------------------------------------------------------------- processing
def process_one(job):
    inst, dyn, midi, c, out_path, sustain_s = job
    x, sr = load_iowa(inst, RAW_DIR / inst / c["file"])
    a = c["a"] + c["onset"]
    b = c["a"] + c["end"]
    seg = x[max(0, a - int(0.002 * sr)): b].astype(np.float64)
    f0 = midi_to_hz(midi + c["cents"] / 100.0)
    seg = hpf(seg, sr, max(c["hpf"], 0.6 * f0), order=4)
    if sr != SR:
        fr = Fraction(SR, sr).limit_denominator(1000)
        seg = resample_poly(seg, fr.numerator, fr.denominator, axis=0)
    fs = SR
    att = c["attack_s"]
    sus_end = min(c["sus_end_s"] - c["onset"] / sr - 0.06, len(seg) / fs - 0.1)
    s0, s1 = stable_window(seg, fs, att, max(sus_end, att + 0.4))
    cut = s0 + int(min(0.3 * fs, (s1 - s0) / 2))
    total = int(sustain_s * fs)
    y = extend_sustain(seg, fs, f0, s0, s1, total, seed=midi * 7 + DYNAMICS.index(dyn), cut=cut)
    # fade the last 20 ms (the loop region never reaches it)
    fl = int(0.02 * fs)
    y[-fl:] *= np.linspace(1, 0, fl)[:, None]
    # onset fade-in of 2 ms (the pre-roll)
    fi = int(0.002 * fs)
    y[:fi] *= np.linspace(0, 1, fi)[:, None]
    steady = y[s0: max(s0 + int(0.3 * fs), s1)]
    level = a_level_db(steady)
    peak = float(np.max(np.abs(y)))
    gain = 10 ** (-1.0 / 20) / peak                         # peak-normalise to -1 dBFS
    y *= gain
    loop_start, loop_end = find_loop(y.mean(axis=1), fs, f0)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), y, fs, subtype="PCM_24")
    # rise times of the recorded attack (10 ms RMS frames, re the steady level)
    t6, t3 = rise_times(y, fs, s0, s1)
    normal_off = max(0.0, t3 - NORMAL_RISE)
    short_off = max(0.0, t3 - SHORT_RISE) if t3 > 0.1 else 0.3 * t3
    legato_off = float(np.clip(max(t3 + 0.05, 0.12), 0.12, max(0.12, s1 / fs - 0.2)))
    return dict(inst=inst, dyn=dyn, midi=midi, file=c["file"], string=c["string"], cents=c["cents"],
                path=str(out_path.relative_to(QUARTET_DIR)), level_db=level - 20 * np.log10(1.0),
                norm_gain_db=20 * np.log10(gain), attack_s=att, rise6_s=t6, rise3_s=t3,
                normal_offset=int(normal_off * fs), legato_offset=int(legato_off * fs),
                short_offset=int(short_off * fs), loop_start=int(loop_start), loop_end=int(loop_end),
                s0=s0, s1=s1, frames=len(y))


def rise_times(y: np.ndarray, fs: int, s0: int, s1: int) -> tuple[float, float]:
    mono = y.mean(axis=1).astype(np.float64)
    hop = int(0.01 * fs)
    n = min(len(mono), int(2.0 * fs)) // hop
    db = 10 * np.log10(np.mean(mono[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-20)
    st = 10 * np.log10(np.mean(mono[s0:s1] ** 2) + 1e-20)

    def first(th):
        i = np.flatnonzero(db > st + th)
        return float(i[0] * hop / fs) if len(i) else s0 / fs
    return first(-6.0), first(-3.0)


# ------------------------------------------------------------------- SFZ
def smooth_levels(meta: list[dict]) -> dict:
    """Per-note calibration offsets (dB) so that each layer follows a smooth
    register curve and sits at LAYER_DB relative to the ff curve."""
    by_dyn = defaultdict(dict)
    for m in meta:
        # level of the note as it will sound = measured level + normalisation gain
        by_dyn[m["dyn"]][m["midi"]] = m["level_db"]
    out = {}
    curves = {}
    for d, lv in by_dyn.items():
        ks = np.array(sorted(lv))
        vs = np.array([lv[k] for k in ks])
        # robust smooth: rolling median (+-3 semitones) then quadratic fit
        med = np.array([np.median(vs[np.abs(ks - k) <= 3]) for k in ks])
        coef = np.polyfit(ks, med, 2 if len(ks) > 6 else 1)
        curves[d] = coef
    ref = curves.get("ff") if "ff" in curves else next(iter(curves.values()))
    keys = sorted({m["midi"] for m in meta})
    k_mid = keys[len(keys) // 2]
    dev = defaultdict(list)                  # each note's deviation from its layer's smooth curve
    for m in meta:
        dev[m["midi"]].append(m["level_db"] - float(np.polyval(curves[m["dyn"]], m["midi"])))
    for m in meta:
        k = m["midi"]
        # keep the instrument's natural register slope (clamped to +-6 dB), but pin
        # the ff curve at the middle of the range to REF_DB for every instrument
        slope = float(np.clip(np.polyval(ref, k) - np.polyval(ref, k_mid), -6, 6))
        target = REF_DB + slope + LAYER_DB[m["dyn"]]
        # all layers of a key keep the same 30 % of that key's natural unevenness,
        # so the pp/mf/ff crossfade of one key never bulges or dips
        keep = 0.3 * float(np.clip(np.mean(dev[k]), -3, 3))
        out[(m["dyn"], k)] = float(target + keep - m["level_db"])
    return out


def cc1_curve() -> list[float]:
    """Volume (dB) to add at each CC1 value so loudness follows CC1_TARGET given
    equal-power crossfades between layers calibrated to LAYER_DB."""
    tx = [p[0] for p in CC1_TARGET]
    ty = [p[1] for p in CC1_TARGET]
    comp = []
    for v in range(128):
        p = 0.0
        for d, (i0, i1, o0, o1) in XF.items():
            # same maths as sfizz crossfadeIn/crossfadeOut (power curve -> linear power)
            pin = 1.0 if (d == "pp" or v >= i1) else (0.0 if v < i0 else min(1.0, (v - i0) / (i1 - i0 - 1)))
            if d == "ff" or v <= o0:
                pout = 1.0
            else:
                pos = (v - o0) / (o1 - o0 - 1)
                pout = 0.0 if pos > 1 else 1.0 - pos
            p += pin * pout * 10 ** (LAYER_DB[d] / 10)
        comp.append(float(np.interp(v, tx, ty) - 10 * np.log10(p)))
    return comp


CORR_PATH = QUARTET_DIR / "tuning_corrections.json"


def load_corrections() -> dict:
    return json.loads(CORR_PATH.read_text()) if CORR_PATH.exists() else {}


def retune(verify_json: Path, only: set):
    """Closed-loop tuning: fold the pitch errors measured by verify_tuning.py
    (YIN through sfizz, per layer and sample key) into tuning_corrections.json."""
    rep = json.loads(Path(verify_json).read_text())
    corr = load_corrections()
    meta = json.loads((QUARTET_DIR / "samples" / "meta.json").read_text())
    n = 0
    for inst, layers in rep.items():
        if only and inst not in only:
            continue
        centres = {(m["dyn"], m["midi"]) for m in meta.get(inst, [])}
        for dyn, rows in layers.items():
            for r in rows:
                if (dyn, r["key"]) in centres and r["cents"] is not None and abs(r["cents"]) < 60:
                    key = f"{inst}/{dyn}/{r['key']}"
                    corr[key] = round(corr.get(key, 0.0) - r["cents"], 1)
                    n += 1
    CORR_PATH.write_text(json.dumps(corr, indent=0, sort_keys=True))
    print(f"retune: updated {n} corrections -> {CORR_PATH}")


def write_sfz(inst: str, meta: list[dict]):
    corr = load_corrections()
    cal = smooth_levels(meta)
    comp = cc1_curve()
    depth = 30.0
    by = defaultdict(dict)
    for m in meta:
        by[m["dyn"]][m["midi"]] = m
    lo_all = INSTRUMENTS[inst]["lo"]
    hi_all = INSTRUMENTS[inst]["hi"]
    lines = [
        f"// {inst.capitalize()} (solo) - University of Iowa MIS 2012 arco samples, pp/mf/ff",
        "// generated by ricercar/audio/strings/iowa_build.py - do not edit by hand",
        "// CC1 = dynamics (timbre crossfade + loudness), CC20 = articulation, CC21 = release,",
        "// velocity = attack softness / accent.  CC7/CC11 are applied by render_quartet.py.",
        "<control>",
        "hint_ram_based=1",      # load every sample into RAM: sfizz_render's disk streaming drops notes
        "set_cc1=88",
        "set_cc20=0",
        "set_cc21=30",
        "<curve>curve_index=17 " + " ".join(f"v{v:03d}={comp[v] / depth:.4f}" for v in range(128)),
        "<global>",
        "loop_mode=loop_continuous loop_crossfade=0.12",
        "xf_cccurve=power",
        f"volume_oncc1={depth:g} volume_curvecc1=17",
        "amp_veltrack=30",
        "ampeg_attack=0.10 ampeg_vel2attack=-0.09",
        "ampeg_release=0.03 ampeg_release_oncc21=1.2",
        "bend_up=200 bend_down=-200",
        "pitch_random=3",
        "volume=-6",
    ]
    arts = [  # (locc20, hicc20, offset key, envelope override)
        # normal bow stroke: recorded attack, slow swells shortened to NORMAL_RISE;
        # velocity 127 = the recorded bite, low velocity = up to 90 ms softer start
        (0, 63, "normal_offset", None),
        # slurred: enters in the sustain, fades in under the previous note's release
        (64, 95, "legato_offset", "ampeg_attack=0.07 ampeg_vel2attack=-0.03"),
        # short (detache / spiccato-like): crisp start and a small accent decay
        (96, 127, "short_offset", "ampeg_attack=0.004 ampeg_vel2attack=0 ampeg_hold=0.03 "
                                   "ampeg_decay=0.16 ampeg_sustain=72"),
    ]
    for d in DYNAMICS:
        notes = by.get(d, {})
        if not notes:
            continue
        i0, i1, o0, o1 = XF[d]
        xf = []
        if d != "pp":
            xf.append(f"xfin_locc1={i0} xfin_hicc1={i1}")
        if d != "ff":
            xf.append(f"xfout_locc1={o0} xfout_hicc1={o1}")
        ks = sorted(notes)
        # key ranges: each sample covers up to half-way to its neighbours; extend
        # the ends by up to 3 semitones (pitch-shifted) to reach the full range
        bounds = []
        for j, k in enumerate(ks):
            lo = lo_all - 2 if j == 0 else (ks[j - 1] + k) // 2 + 1
            hi = hi_all if j == len(ks) - 1 else (k + ks[j + 1]) // 2
            lo = max(lo, k - 3) if j == 0 else lo
            hi = min(hi, k + 3) if j == len(ks) - 1 else hi
            bounds.append((lo, hi))
        for (lc, hc, offk, att) in arts:
            lines.append(f"<group> // {d} art cc20 {lc}-{hc}")
            lines.append(" ".join(xf + [f"locc20={lc} hicc20={hc}"] + ([att] if att else [])))
            for k, (lo, hi) in zip(ks, bounds):
                m = notes[k]
                vol = cal[(d, k)] - m["norm_gain_db"]
                tune = -m["cents"] + corr.get(f"{inst}/{d}/{k}", 0.0)
                reg = (f"<region> sample={m['path']} lokey={lo} hikey={hi} pitch_keycenter={k} "
                       f"tune={tune:.1f} volume={vol:.2f} loop_start={m['loop_start']} loop_end={m['loop_end']}")
                if offk:
                    reg += f" offset={m[offk]}"
                reg += f"  // {midi_name(k)} {m['string']} {m['file']}"
                lines.append(reg)
    out = QUARTET_DIR / f"{inst}.sfz"
    out.write_text("\n".join(lines) + "\n")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--sustain", type=float, default=SUSTAIN_S)
    ap.add_argument("--sfz-only", action="store_true", help="rewrite SFZ from samples/meta.json")
    ap.add_argument("--retune", type=Path, metavar="VERIFY_JSON",
                    help="fold the errors measured by verify_tuning.py --json into the tune corrections, "
                         "then rewrite the SFZ files (implies --sfz-only)")
    a = ap.parse_args()
    only = set(a.only.split(",")) - {""}
    if a.retune:
        retune(a.retune, only)
        a.sfz_only = True
    table = load_analysis()
    meta_path = QUARTET_DIR / "samples" / "meta.json"
    all_meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    for inst in INSTRUMENTS:
        if only and inst not in only:
            continue
        if not any(k[0] == inst for k in table):
            print(f"{inst}: no analysed notes, skipped")
            continue
        if not a.sfz_only:
            picks = choose(inst, table)
            jobs = []
            for (d, midi), c in sorted(picks.items(), key=lambda t: (t[0][1], t[0][0])):
                out = QUARTET_DIR / "samples" / inst / f"{inst}_{d}_{midi:03d}_{midi_name(midi)}.wav"
                jobs.append((inst, d, midi, c, out, a.sustain))
            with ProcessPoolExecutor(a.jobs) as ex:
                meta = list(ex.map(process_one, jobs))
            all_meta[inst] = meta
            meta_path.parent.mkdir(parents=True, exist_ok=True)
            meta_path.write_text(json.dumps(all_meta, indent=1))
        meta = all_meta[inst]
        path = write_sfz(inst, meta)
        cov = {d: len([m for m in meta if m["dyn"] == d]) for d in DYNAMICS}
        print(f"{inst}: {len(meta)} samples {cov} -> {path}")


if __name__ == "__main__":
    main()
