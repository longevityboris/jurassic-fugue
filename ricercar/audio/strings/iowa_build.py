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
     (ff = 0 dB, mf = -8 dB, pp = -18 dB) so CC1 behaves predictably;
  5. writes <inst>.sfz with:
       CC1   dynamics: equal-power crossfade pp (<=16) -> mf (64) -> ff (>=112),
             plus a volume curve so loudness moves ~linearly in dB with CC1
             (cc1 0 = ppp, 16 = pp, 40 = p, 64 = mf, 88 = f, 112 = ff, 127 = fff)
       CC20  articulation (set by render_quartet.py before each note-on):
             0-63 normal bow attack, 64-95 legato (slurred: starts after the
             attack, 60 ms fade-in), 96-127 short (crisp onset for fast notes)
       CC21  release time: 0.03 s + 1.2 s * cc21/127
       vel   attack softness (vel 127 = the recorded bite, vel 1 = 150 ms swell)
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
LAYER_DB = {"pp": -18.0, "mf": -8.0, "ff": 0.0}
REF_DB = -20.0          # A-weighted steady level of the ff layer mid-range (dBFS, before volume=-6)
# CC1 anchor points -> target loudness (dB, relative to the ff layer)
CC1_TARGET = [(0, -26.0), (16, -18.0), (40, -12.5), (64, -8.0), (88, -3.5), (112, 0.0), (127, 1.5)]
XF = {"pp": (0, 16, 16, 64), "mf": (16, 64, 64, 112), "ff": (64, 112, 112, 127)}


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
    return dict(inst=inst, dyn=dyn, midi=midi, file=c["file"], string=c["string"], cents=c["cents"],
                path=str(out_path.relative_to(QUARTET_DIR)), level_db=level - 20 * np.log10(1.0),
                norm_gain_db=20 * np.log10(gain), attack_s=att, legato_offset=int(min(max(s0, int(0.08 * fs)), int(0.6 * fs))),
                short_offset=int(min(att * 0.5, 0.05) * fs), loop_start=int(loop_start), loop_end=int(loop_end),
                s0=s0, s1=s1, frames=len(y))


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
    for m in meta:
        k = m["midi"]
        # keep the instrument's natural register slope (clamped to +-6 dB), but pin
        # the ff curve at the middle of the range to REF_DB for every instrument
        slope = float(np.clip(np.polyval(ref, k) - np.polyval(ref, k_mid), -6, 6))
        target = REF_DB + slope + LAYER_DB[m["dyn"]]
        smooth_own = np.polyval(curves[m["dyn"]], k)
        # pull 80 % of the way from the note's own level toward the smooth curve
        own = m["level_db"]
        corrected = own + 0.8 * (smooth_own - own)
        corrected = own + np.clip(corrected - own, -8, 8)
        out[(m["dyn"], k)] = float(target - corrected)
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


def write_sfz(inst: str, meta: list[dict]):
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
        "set_cc1=64",
        "set_cc20=0",
        "set_cc21=30",
        "<curve>curve_index=17 " + " ".join(f"v{v:03d}={comp[v] / depth:.4f}" for v in range(128)),
        "<global>",
        "loop_mode=loop_continuous loop_crossfade=0.12",
        "xf_cccurve=power",
        f"volume_oncc1={depth:g} volume_curvecc1=17",
        "amp_veltrack=30",
        "ampeg_attack=0.15 ampeg_vel2attack=-0.15",
        "ampeg_release=0.03 ampeg_release_oncc21=1.2",
        "bend_up=200 bend_down=-200",
        "pitch_random=3",
        "volume=-6",
    ]
    arts = [  # (locc20, hicc20, offset key, attack override)
        (0, 63, None, None),
        (64, 95, "legato_offset", "ampeg_attack=0.06 ampeg_vel2attack=0"),
        (96, 127, "short_offset", "ampeg_attack=0.003 ampeg_vel2attack=0"),
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
                tune = -m["cents"]
                reg = (f"<region> sample={m['path']} lokey={lo} hikey={hi} pitch_keycenter={k} "
                       f"tune={tune:.0f} volume={vol:.2f} loop_start={m['loop_start']} loop_end={m['loop_end']}")
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
    a = ap.parse_args()
    only = set(a.only.split(",")) - {""}
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
