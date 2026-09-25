#!/usr/bin/env python3
"""Render an orchestrated piece group by group and mix the groups in one hall.

usage:
  python3 mix.py MANIFEST.json                 render (cached), align, verify, place, master
  python3 mix.py MANIFEST.json --rerender      render every group again even if its cache is fresh
  python3 mix.py MANIFEST.json --recalibrate   measure the renderer calibration again
  options: --out PATH (overrides the manifest's "out"), --keep-stems (keep the aligned stems),
           --max-lag-ms 5 (inter-group alignment tolerance; the mix fails above it)

MANIFEST.json is written by orchestrate.py (OUTDIR/manifest.json) from the spec's "mix" section and
can be edited; paths in it are relative to its own directory. Format: tools/ORCHESTRATION.md.

What it does
  1. Render: each group's MIDI goes to its renderer's own command line (piano render_piano.py,
     quartet render_quartet.py, orchestra render_orchestra.py, organ render_organ.py) with dry
     stems and no reverb, one group at a time, into MANIFEST_DIR/render/<group>/. A render is
     reused while the MIDI, the sidecar, the renderer script and the arguments are unchanged.
  2. Align: every stem is put on one timeline whose sample 0 is MIDI time -lead_in, from what
     each renderer reports about its own output (piano and organ: sample 0 = MIDI -lead_in;
     quartet and orchestra: offset_s in their report). All groups share orchestrate.py's tempo map.
  3. Level: stems are brought to each renderer's raw (pre-normalisation) scale (the quartet's
     stems are normalised by its render; the gain is recovered from its report's pre-normalisation
     stem levels), then renderers are levelled against each other with a calibration chorale
     (orchestration/calibration/: the same four-part mf chorale through orchestrate.py and each
     renderer; equal K-weighted loudness; cached per renderer script hash), then the manifest's
     gain_db per group.
  4. Verify: an onset-strength envelope (1 ms frames, four bands) of each group is cross-correlated
     with an impulse train at that group's MIDI note-ons; the difference between the groups' lags
     must be under --max-lag-ms (5 ms). Where two groups play the same onsets (doublings), their
     onset envelopes are also cross-correlated directly. With "latency_ms" in a group ("auto" or a
     number) a measured offset can be compensated; by default nothing is shifted.
  5. Place and reverberate: each stem is panned to its seat (audio/strings/hall.py place_dry:
     azimuth, width, depth delay and -1 dB/m), and each group feeds the same measured Detmold
     Konzerthaus response (hall.Hall, unit energy, tail continued; right-hand sources get the
     mirrored response) at its own wet level. Orchestra stems arrive already seated by their
     renderer and are only reverberated.
  6. Master: 18 Hz high-pass, silent tail trimmed, true peak (4x oversampled) normalised to
     peak_dbtp (-1 dBTP), 48 kHz 24-bit WAV with credits in its INFO chunk, AAC 256 kb/s m4a by
     afconvert (its decoded true peak is measured and the encode repeated lower if it overshoots).
  7. Report (OUT.mix.json): alignment lags, calibration and gains, per-group loudness where each
     plays, integrated loudness, loudness range, true peak of WAV and m4a, C80 per group,
     stereo correlation, a click scan and a loudness curve per bar range.
Nothing is played through the speakers.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import mido
import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

TOOLS = Path(__file__).resolve().parent
RICERCAR = TOOLS.parent
AUDIO = RICERCAR / "audio"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(AUDIO / "strings"))
import hall as hallmod  # noqa: E402  (audio/strings/hall.py: the shared Detmold hall and stage placement)

SR = 48000
CAL_DIR = RICERCAR / "orchestration" / "calibration"
CAL_VERSION = 1           # bump when the calibration method (seating, loudness measure) changes
CAL_PARTS = {"piano": ["soprano", "alto", "tenor", "bass"], "quartet": ["vn1", "vn2", "va", "vc"],
             "orchestra": ["vn1", "vn2", "va", "vc"], "organ": ["soprano", "alto", "tenor", "bass"]}
SCRIPTS = {"piano": AUDIO / "piano" / "render_piano.py", "quartet": AUDIO / "strings" / "render_quartet.py",
           "orchestra": AUDIO / "orchestra" / "render_orchestra.py", "organ": AUDIO / "organ" / "render_organ.py"}
DEFAULT_STAGE = {"piano": {"az": 0.0, "depth": 1.2, "width": 0.7},
                 "organ": {"az": 0.0, "depth": 0.0, "width": 0.8}}
CREDITS = ("Salamander Grand Piano V3 by Alexander Holm (CC-BY 3.0); University of Iowa MIS strings; "
           "Detmold Konzerthaus SRIR, Amengual Gari, Sahin, Eddy, Kob, AES 2020 (CC BY 4.0); "
           "rendered with sfizz (BSD-2-Clause)")


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16] if Path(path).exists() else "-"


def db(x: float) -> float:
    return 10 * math.log10(max(x, 1e-30))


def true_peak(x: np.ndarray) -> float:
    return float(np.max(np.abs(resample_poly(x, 4, 1, axis=0))))


# ----------------------------------------------------------------------------- renderer adapters
def quartet_instr() -> dict:
    with contextlib.redirect_stdout(io.StringIO()):
        import render_quartet as rq  # noqa: E402
    return rq.INSTR


def render_group(renderer: str, midi: Path, rdir: Path, lead_in: float, extra: list, force: bool,
                 sidecar: Path | None = None) -> dict:
    """Run the renderer (or reuse a fresh cache). -> {"stems": [(name, path)], "offset_s", "report"}."""
    script = SCRIPTS[renderer]
    if not script.exists():
        raise SystemExit(f"{renderer}: renderer {script} not found (not built yet?)")
    rdir.mkdir(parents=True, exist_ok=True)
    base = rdir / "render"
    stems_dir = rdir / "stems"
    if renderer == "piano":
        report = rdir / "render.json"
        cmd = [sys.executable, str(script), str(midi), "-o", str(base), "--no-reverb", "--no-m4a",
               "--stems", str(stems_dir), "--lead-in", f"{lead_in}", "--json", str(report)]
    elif renderer == "quartet":
        report = rdir / "render.report.json"
        cmd = [sys.executable, str(script), str(midi), "-o", str(base), "--hall", "none", "--stems",
               "--report", str(report), "--lead-in", f"{lead_in}",
               "--map", "Violin I=vn1,Violin II=vn2,Viola=va,Cello=vc,Contrabass=cb"]
    elif renderer == "orchestra":
        report = rdir / "render.json"
        cmd = [sys.executable, str(script), str(midi), "-o", str(base), "--stems", "--no-reverb",
               "--lead-in", f"{lead_in}"]
        if sidecar is not None and sidecar.exists():
            cmd += ["--sidecar", str(sidecar)]
    elif renderer == "organ":
        report = rdir / "render.json"
        cmd = [sys.executable, str(script), str(midi), "-o", str(base), "--stems", str(stems_dir),
               "--no-reverb", "--lead-in", f"{lead_in}", "--json", str(report)]
        if sidecar is not None and sidecar.exists():
            cmd += ["--registration", str(sidecar)]
    else:
        raise SystemExit(f"unknown renderer {renderer!r}")
    cmd += [str(x) for x in extra]
    stamp = {"midi": sha(midi), "sidecar": sha(sidecar) if sidecar else None, "script": sha(script),
             "cmd": cmd[2:]}
    stamp_path = rdir / "stamp.json"
    fresh = (not force and stamp_path.exists() and report.exists()
             and json.loads(stamp_path.read_text()) == stamp)
    if not fresh:
        for p in (stems_dir, rdir / "render.stems"):
            if p.exists():
                shutil.rmtree(p)
        for p in rdir.glob("render_stem_*.wav"):
            p.unlink()
        print(f"  rendering {renderer}: {' '.join(Path(c).name if '/' in c else c for c in cmd[1:])}", flush=True)
        log = rdir / "render.log"
        with open(log, "w") as fh:
            r = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT)
        if r.returncode != 0:
            raise SystemExit(f"{renderer} render failed (exit {r.returncode}); see {log}:\n"
                             + "\n".join(log.read_text().splitlines()[-15:]))
        stamp_path.write_text(json.dumps(stamp, indent=1))
    else:
        print(f"  {renderer}: cached render in {rdir}")
    rep = json.loads(report.read_text())
    if renderer == "piano":
        stems = [(p.stem, p) for p in sorted(stems_dir.glob("*.wav"))]
        offset = -lead_in
    elif renderer == "quartet":
        stems = [(p.stem.split("_stem_")[-1], p) for p in sorted(rdir.glob("render_stem_*.wav"))]
        offset = float(rep["offset_s"])
    elif renderer == "orchestra":
        sd = rdir / "render.stems"
        stems = [(p.stem, p) for p in sorted(sd.glob("*.wav"))]
        offset = float(rep.get("offset_s", -lead_in))
    else:
        stems = [(p.stem, p) for p in sorted(stems_dir.glob("*.wav"))]
        offset = float(rep.get("offset_s", -lead_in))
    if not stems:
        raise SystemExit(f"{renderer}: no stems in {rdir}")
    return {"stems": stems, "offset_s": offset, "report": rep}


def raw_scale_db(renderer: str, rep: dict, stems: dict) -> tuple[float, dict]:
    """Gain (dB) that takes this render's stems back to the renderer's pre-normalisation scale.
    piano: stems are pre-normalisation already; organ and orchestra: stems are at the pre-normalisation
    gain by contract; quartet: its stems carry the mix's normalisation, recovered from the report's
    stem levels (computed before normalisation, on the same signal)."""
    if renderer != "quartet":
        return 0.0, {}
    ref = rep.get("stem_rms_db_when_active", {})
    names = quartet_instr()
    est = {}
    for inst, x in stems.items():
        target = ref.get(names[inst]["name"]) if inst in names else None
        if target is None:
            continue
        mono = x.mean(axis=1)
        g = 0.0
        for _ in range(3):          # the report counts samples above 1e-5 on its own scale
            act = np.abs(mono) > 1e-5 * 10 ** (g / 20)
            g = db(float(np.mean(mono[act] ** 2))) - target
        est[inst] = round(-g, 3)
    if not est:
        raise SystemExit("quartet report has no stem_rms_db_when_active: cannot undo its normalisation")
    vals = list(est.values())
    if max(vals) - min(vals) > 0.1:
        print(f"  warning: quartet normalisation estimates disagree: {est}")
    return float(np.median(vals)), est


def load_stems(stems: list, offset_s: float, lead_in: float, n: int) -> dict:
    """-> {name: (n, 2) float64 on the common timeline (sample 0 = MIDI time -lead_in)}."""
    out = {}
    shift = int(round((offset_s + lead_in) * SR))
    for name, path in stems:
        x, sr = sf.read(str(path), dtype="float64", always_2d=True)
        if sr != SR:
            raise SystemExit(f"{path}: {sr} Hz, expected {SR}")
        if x.shape[1] == 1:
            x = np.repeat(x, 2, axis=1)
        y = np.zeros((n, 2))
        a = max(0, shift)
        b = max(0, -shift)
        m = min(n - a, len(x) - b)
        if m > 0:
            y[a:a + m] = x[b:b + m]
        out[name] = y
    return out


# ----------------------------------------------------------------------------- timing
def midi_onsets(midi: Path) -> list:
    """(seconds, track name, key, velocity) of every note-on, through the file's tempo map."""
    mid = mido.MidiFile(str(midi))
    tempos = sorted((t, m.tempo) for tr in mid.tracks for t, m in _abs(tr) if m.type == "set_tempo")
    pts, s, lt, us = [], 0.0, 0, 500000
    for t, tempo in tempos:
        s += (t - lt) * us / 1e6 / mid.ticks_per_beat
        pts.append((t, s, tempo))
        lt, us = t, tempo
    if not pts or pts[0][0] > 0:
        pts.insert(0, (0, 0.0, 500000))
    ticks = np.array([p[0] for p in pts])

    def sec(tick):
        i = int(np.searchsorted(ticks, tick, side="right")) - 1
        t, s0, u = pts[i]
        return s0 + (tick - t) * u / 1e6 / mid.ticks_per_beat

    out = []
    for tr in mid.tracks:
        name = next((m.name for m in tr if m.type == "track_name"), "")
        for t, m in _abs(tr):
            if m.type == "note_on" and m.velocity > 0:
                out.append((sec(t), name, m.note, m.velocity))
    return sorted(out)


def _abs(tr):
    t = 0
    for m in tr:
        t += m.time
        yield t, m


def onset_envelope(x: np.ndarray) -> np.ndarray:
    """Onset strength at 1 ms frames: rises of log energy in four bands (5 ms smoothing), summed."""
    mono = x.mean(axis=1) if x.ndim == 2 else x
    hop, win = SR // 1000, SR // 200
    edges = [(80, 400), (400, 1600), (1600, 6400), (6400, 16000)]
    total = None
    for lo, hi in edges:
        sos = butter(2, [lo, hi], "bandpass", fs=SR, output="sos")
        e = sosfilt(sos, mono) ** 2
        c = np.concatenate([[0.0], np.cumsum(e)])
        idx = np.arange(0, len(mono) - win, hop)
        en = (c[idx + win] - c[idx]) / win
        le = 10 * np.log10(en + 1e-12 + 1e-4 * en.mean())
        d = np.zeros_like(le)
        d[2:] = le[2:] - le[:-2]
        d = np.maximum(d, 0)
        total = d if total is None else total + d
    # frame k covers samples [k*hop, k*hop + win) and d[k] compares it with frame k-2, so a step at
    # time T peaks at k = T - 1.5 ms: two leading frames put the peak on T (within 0.5 ms)
    return np.concatenate([np.zeros(2), total])


def fit(x: np.ndarray, n: int) -> np.ndarray:
    return x[:n] if len(x) >= n else np.concatenate([x, np.zeros(n - len(x))])


def onset_train(times_s: list, n: int, sigma_ms: float = 2.0) -> np.ndarray:
    tr = np.zeros(n)
    for t in times_s:
        k = int(round(t * 1000))
        if 0 <= k < n:
            tr[k] += 1.0
    r = int(4 * sigma_ms)
    ker = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_ms) ** 2)
    return np.convolve(tr, ker, mode="same")


def xcorr_lag(a: np.ndarray, b: np.ndarray, max_lag: int = 80, mask: np.ndarray | None = None) -> tuple:
    """Lag (ms, parabolic peak) that best aligns a to b: a(t) ~ b(t - lag); lag > 0 = a is late."""
    n = min(len(a), len(b))
    a, b = a[:n].copy(), b[:n].copy()
    if mask is not None:
        a *= mask[:n]
    a = (a - a.mean()) / (a.std() + 1e-12)
    b = (b - b.mean()) / (b.std() + 1e-12)
    lags = np.arange(-max_lag, max_lag + 1)
    c = np.array([np.dot(a[max(0, L):n + min(0, L)], b[max(0, -L):n - max(0, L)]) for L in lags]) / n
    i = int(np.argmax(c))
    frac = 0.0
    if 0 < i < len(c) - 1:
        den = c[i - 1] - 2 * c[i] + c[i + 1]
        frac = 0.5 * (c[i - 1] - c[i + 1]) / den if den != 0 else 0.0
    others = np.concatenate([c[:max(0, i - 10)], c[i + 11:]])
    return float(lags[i] + frac), float(c[i]), float(c[i] / (np.max(others) + 1e-12)) if len(others) else 0.0


def xcorr_curve(a: np.ndarray, b: np.ndarray, max_lag: int = 80) -> np.ndarray:
    """c[L + max_lag] = sum_t z(a)[t + L] z(b)[t] / n: peak at L > 0 means a is late."""
    n = min(len(a), len(b))
    a = (a[:n] - a[:n].mean()) / (a[:n].std() + 1e-12)
    b = (b[:n] - b[:n].mean()) / (b[:n].std() + 1e-12)
    return np.array([np.dot(a[max(0, L):n + min(0, L)], b[max(0, -L):n - max(0, L)])
                     for L in range(-max_lag, max_lag + 1)]) / n


def peak_of(c: np.ndarray) -> float:
    max_lag = (len(c) - 1) // 2
    i = int(np.argmax(c))
    frac = 0.0
    if 0 < i < len(c) - 1:
        den = c[i - 1] - 2 * c[i] + c[i + 1]
        frac = 0.5 * (c[i - 1] - c[i + 1]) / den if den != 0 else 0.0
    return float(i - max_lag + frac)


def midi_notes(midi: Path) -> dict:
    """{track name: [(on_s, off_s, key, velocity)]} through the file's tempo map."""
    mid = mido.MidiFile(str(midi))
    tempos = sorted((t, m.tempo) for tr in mid.tracks for t, m in _abs(tr) if m.type == "set_tempo")
    pts, s, lt, us = [], 0.0, 0, 500000
    for t, tempo in tempos:
        s += (t - lt) * us / 1e6 / mid.ticks_per_beat
        pts.append((t, s, tempo))
        lt, us = t, tempo
    if not pts or pts[0][0] > 0:
        pts.insert(0, (0, 0.0, 500000))
    ticks = np.array([p[0] for p in pts])

    def sec(tick):
        i = int(np.searchsorted(ticks, tick, side="right")) - 1
        t, s0, u = pts[i]
        return s0 + (tick - t) * u / 1e6 / mid.ticks_per_beat

    out = {}
    for tr in mid.tracks:
        name = next((m.name for m in tr if m.type == "track_name"), "")
        pend, lst = {}, []
        for t, m in _abs(tr):
            if m.type == "note_on" and m.velocity > 0:
                pend.setdefault(m.note, []).append((sec(t), m.velocity))
            elif m.type in ("note_off", "note_on") and pend.get(m.note):
                on, vel = pend[m.note].pop(0)
                lst.append((on, sec(t), m.note, vel))
        if lst:
            out[name] = sorted(lst)
    return out


ATTACK_RULE = {
    "piano": "every note-on (the samples are onset-aligned to 0.2 ms)",
    "quartet": "new-bow and short strokes at their note-on (the renderer starts the bow's pre-roll early "
               "so that the stroke lands on the note-on); slurred notes, which enter by crossfade, are left out "
               "(articulation from its report)",
    "default": "notes after at least 100 ms of silence in their part",
}


def attack_starts(renderer: str, rep: dict, by_track: dict, track_of: dict) -> dict:
    """{stem name: [MIDI seconds]} at which the renderer starts a note's attack."""
    stem_of = {t: s for s, t in track_of.items()}
    if renderer == "piano":
        return {stem_of[t]: [on for on, *_ in v] for t, v in by_track.items() if t in stem_of}
    if renderer == "quartet":
        out = {}
        for j in rep.get("jobs", []):
            if j.get("kind") != "main":
                continue
            ts = [on for (on, off, key, vel, art) in j["note_list"] if art is None or art < 64 or art >= 96]
            out.setdefault(j["inst"], []).extend(ts)
        return {k: sorted(v) for k, v in out.items()}
    return {stem_of[t]: entry_onsets(v) for t, v in by_track.items() if t in stem_of}


def entry_onsets(notes: list, gap_s: float = 0.1) -> list:
    """Onsets of notes that follow at least gap_s of silence in their own part (or start it):
    their attack is unambiguous on every instrument (a bowed slur's is not)."""
    out, last_off = [], -1e9
    for on, off, *_ in sorted(notes):
        if on - last_off >= gap_s:
            out.append(on)
        last_off = max(last_off, off)
    return out


def stem_track_map(gm: dict, stems: dict) -> dict:
    """stem name -> the MIDI track it renders (quartet stems are named by instrument id)."""
    parts = gm.get("parts", {})
    by_inst = {v.get("instrument"): v.get("track") for v in parts.values() if v.get("instrument")}
    tracks = {v.get("track"): v.get("track") for v in parts.values()}
    low = {str(t).lower(): t for t in tracks}
    out = {}
    for name in stems:
        if gm["renderer"] == "quartet" and name in by_inst:
            out[name] = by_inst[name]
        elif name in tracks:
            out[name] = name
        elif name.lower() in low:
            out[name] = low[name.lower()]
    return out


def per_note_lags(env: np.ndarray, times_s: list, pre_ms=30, post_ms=60) -> np.ndarray:
    out = []
    for t in times_s:
        k = int(round(t * 1000))
        a, b = k - pre_ms, k + post_ms
        if a < 0 or b >= len(env):
            continue
        seg = env[a:b]
        if seg.max() <= 0:
            continue
        out.append(int(np.argmax(seg)) - pre_ms)
    return np.array(out)


# ----------------------------------------------------------------------------- calibration
def calibrate(renderers: set, lead_in: float, force: bool) -> dict:
    """K-weighted loudness (LUFS, raw scale, placed dry sum) of the calibration chorale per renderer."""
    import orchestrate
    import pyloudnorm as pyln
    cal_path = CAL_DIR / "calibration.json"
    cal = json.loads(cal_path.read_text()) if cal_path.exists() else {}
    score, plan = CAL_DIR / "chorale.ly", CAL_DIR / "chorale.plan.json"
    for r in sorted(renderers):
        key = f"v{CAL_VERSION}:{sha(SCRIPTS[r])}:{sha(score)}:{sha(plan)}:{sha(Path(orchestrate.__file__))}"
        if not force and cal.get(r, {}).get("key") == key:
            continue
        print(f"  calibrating {r} (four-part mf chorale)", flush=True)
        work = CAL_DIR / "render" / r
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        parts = CAL_PARTS[r]
        spec = {"groups": {"cal": {"renderer": r, "parts": parts}},
                "assignments": [{"voice": v, "part": p} for v, p in zip(["soprano", "alto", "tenor", "bass"], parts)]}
        sp = work / "spec.json"
        sp.write_text(json.dumps(spec))
        with contextlib.redirect_stdout(io.StringIO()):
            rep = orchestrate.build(score, plan, sp, work / "orch", quiet=True)
        if not rep["ok"]:
            raise SystemExit(f"calibration orchestration failed: {rep['errors']}")
        side = work / "orch" / ("cal.orchestra.json" if r == "orchestra" else "cal.registration.json")
        res = render_group(r, work / "orch" / "cal.mid", work / "render", lead_in, [], True,
                           side if side.exists() else None)
        n = max(sf.info(str(p)).frames for _, p in res["stems"]) + SR
        stems = load_stems(res["stems"], res["offset_s"], lead_in, n)
        g_db, est = raw_scale_db(r, res["report"], stems)
        dry = np.zeros((n, 2))
        for name, x in stems.items():
            dry += place(x * 10 ** (g_db / 20), stage_for(r, name, name, name, {}), r)
        lufs = pyln.Meter(SR).integrated_loudness(dry)
        cal[r] = {"key": key, "lufs_raw": round(float(lufs), 3), "raw_scale_db": round(g_db, 3),
                  "stems": len(stems), "note": "four-part mf chorale, placed dry sum, pre-normalisation scale"}
        cal_path.write_text(json.dumps(cal, indent=1))
        shutil.rmtree(work / "render" / "stems", ignore_errors=True)
        for p in (work / "render").glob("*.wav"):
            p.unlink()
    return cal


# ----------------------------------------------------------------------------- placement
def stage_for(renderer: str, part: str | None, track: str | None, inst: str | None, stage: dict) -> dict:
    st = {}
    if renderer == "quartet":
        q = quartet_instr().get(inst or "", {})
        st = {"az": q.get("az", 0.0), "depth": q.get("depth", 0.0), "width": 0.35}
    else:
        st = dict(DEFAULT_STAGE.get(renderer, {"az": 0.0, "depth": 0.0, "width": 0.35}))
    for k in ("*", inst, track, part):
        if k and k in stage:
            st.update(stage[k])
    return st


def place(x: np.ndarray, st: dict, renderer: str) -> np.ndarray:
    if renderer == "orchestra":        # its stems arrive seated (pan, width, depth) by the renderer
        return x
    return hallmod.place_dry(x, float(st.get("az", 0.0)), float(st.get("width", 0.35)),
                             float(st.get("depth", 0.0)))


def side_of(x: np.ndarray, st: dict, renderer: str) -> float:
    """Azimuth sign for the hall (only the side matters: hall.Hall mirrors the IR for the right)."""
    if renderer == "orchestra":
        el, er = float(np.sum(x[:, 0] ** 2)), float(np.sum(x[:, 1] ** 2))
        return 1.0 if el >= er else -1.0
    return 1.0 if float(st.get("az", 0.0)) >= 0 else -1.0


# ----------------------------------------------------------------------------- measurements
def loudness_stats(x: np.ndarray) -> dict:
    import pyloudnorm as pyln
    meter = pyln.Meter(SR)
    I = meter.integrated_loudness(x)
    # short-term (3 s, 1 s hop) for the loudness range, EBU 3342 style (relative gate -20 LU)
    st = []
    for a in range(0, max(1, len(x) - 3 * SR), SR):
        seg = x[a:a + 3 * SR]
        if len(seg) < 3 * SR:
            break
        z = np.mean(sosfilt_k(seg) ** 2, axis=0).sum()
        st.append(-0.691 + 10 * math.log10(max(z, 1e-20)))
    st = np.array(st)
    g = st[st > -70]
    g = g[g > (10 * math.log10(np.mean(10 ** (g / 10))) - 20)] if len(g) else g
    lra = float(np.percentile(g, 95) - np.percentile(g, 10)) if len(g) > 2 else 0.0
    return {"integrated_lufs": round(float(I), 2), "loudness_range_lu": round(lra, 2),
            "short_term_max_lufs": round(float(st.max()), 2) if len(st) else None}


_KW = None


def sosfilt_k(x: np.ndarray) -> np.ndarray:
    """BS.1770 K-weighting (pre-filter + RLB) at 48 kHz."""
    global _KW
    if _KW is None:
        b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
        b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
        from scipy.signal import tf2sos
        _KW = np.vstack([tf2sos(b1, a1), tf2sos(b2, a2)])
    return sosfilt(_KW, x, axis=0)


def kw_level(x: np.ndarray) -> float:
    return -0.691 + db(float(np.mean(sosfilt_k(x) ** 2, axis=0).sum()))


def click_scan(x: np.ndarray, onsets_s: list, lead_in: float) -> dict:
    """Clicks: 1 ms blocks whose energy above 12 kHz is more than 15 dB over the median of the
    surrounding +-20 ms and above -90 dBFS, further than 30 ms from any note onset."""
    from scipy.ndimage import median_filter
    mono = x.mean(axis=1)
    hp = sosfilt(butter(4, 12000, "high", fs=SR, output="sos"), mono)
    b = SR // 1000
    nb = len(hp) // b
    e = (hp[: nb * b] ** 2).reshape(nb, b).mean(axis=1)
    bg = median_filter(e, size=41, mode="nearest") + 1e-14
    cand = np.nonzero((e / bg > 10 ** 1.5) & (e > 1e-9))[0]
    ons = np.array(sorted(onsets_s)) + lead_in
    hits = [round(k / 1000, 3) for k in cand if not (len(ons) and np.min(np.abs(ons - k / 1000)) < 0.03)]
    return {"clicks_away_from_onsets": len(hits), "click_times_s": hits[:20]}


# ----------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--rerender", action="store_true")
    ap.add_argument("--recalibrate", action="store_true")
    ap.add_argument("--keep-stems", action="store_true")
    ap.add_argument("--max-lag-ms", type=float, default=5.0)
    a = ap.parse_args(argv)

    man_path = a.manifest.resolve()
    base = man_path.parent
    man = json.loads(man_path.read_text())
    lead_in = float(man.get("lead_in", 0.5))
    peak_db = float(man.get("peak_dbtp", -1.0))
    out = (a.out or (base / man.get("out", f"../{base.name}"))).resolve()
    groups = man["groups"]
    ref_group = man.get("reference_group") or next(iter(groups))
    if man.get("hall", "detmold") not in ("detmold", "synthetic"):
        raise SystemExit(f"hall {man.get('hall')!r}: detmold | synthetic")
    report = {"manifest": str(man_path), "out": str(out), "lead_in_s": lead_in, "groups": {}}

    # 1. render
    print(f"{man.get('title', man_path.name)}: {len(groups)} group(s)")
    renders = {}
    for g, gm in groups.items():
        side = None
        if gm["renderer"] == "orchestra":
            side = base / f"{g}.orchestra.json"
        elif gm["renderer"] == "organ":
            side = base / f"{g}.registration.json"
        renders[g] = render_group(gm["renderer"], base / gm["midi"], base / "render" / g, lead_in,
                                  gm.get("render_args", []), a.rerender, side)
    n = 0
    for g, r in renders.items():
        for _, p in r["stems"]:
            n = max(n, sf.info(str(p)).frames + int(round((r["offset_s"] + lead_in) * SR)))
    n += int(0.5 * SR)

    # 3. levels: raw scale, renderer calibration, manifest gain
    rset = {gm["renderer"] for gm in groups.values()}
    cal = calibrate(rset, lead_in, a.recalibrate) if len(groups) > 1 else {}
    ref_lufs = cal.get(groups[ref_group]["renderer"], {}).get("lufs_raw")
    aligned = {}
    for g, gm in groups.items():
        r = renders[g]
        stems = load_stems(r["stems"], r["offset_s"], lead_in, n)
        raw_db, est = raw_scale_db(gm["renderer"], r["report"], stems)
        cal_db = 0.0 if ref_lufs is None else ref_lufs - cal[gm["renderer"]]["lufs_raw"]
        gain_db = raw_db + cal_db + float(gm.get("gain_db", 0.0))
        for k in stems:
            stems[k] *= 10 ** (gain_db / 20)
        aligned[g] = stems
        report["groups"][g] = {"renderer": gm["renderer"], "midi": gm["midi"], "stems": sorted(stems),
                               "offset_s": r["offset_s"], "raw_scale_db": round(raw_db, 3),
                               "raw_scale_estimates": est, "calibration_db": round(cal_db, 3),
                               "gain_db": float(gm.get("gain_db", 0.0)), "total_gain_db": round(gain_db, 3)}
    report["calibration"] = {k: v for k, v in cal.items() if k in rset}

    # 4. verify alignment (before placement: the stage's depth delays are physical, not errors)
    print("  verifying alignment", flush=True)
    nframes = n // (SR // 1000)
    ons, env_group, env_stem, entries, attacks = {}, {}, {}, {}, {}
    for g, gm in groups.items():
        ons[g] = midi_onsets(base / gm["midi"])
        by_track = midi_notes(base / gm["midi"])
        track_of = stem_track_map(gm, aligned[g])
        env_group[g] = fit(onset_envelope(sum(aligned[g].values())), nframes)
        env_stem[g], entries[g] = {}, {}
        for name, x in aligned[g].items():
            tr = track_of.get(name)
            if tr is None or tr not in by_track:
                continue
            env_stem[g][name] = fit(onset_envelope(x), nframes)
            entries[g][name] = [t + lead_in for t in entry_onsets(by_track[tr])]
        attacks[g] = {k: [t + lead_in for t in v]
                      for k, v in attack_starts(gm["renderer"], renders[g]["report"], by_track, track_of).items()
                      if k in env_stem[g]}

    def entry_lag(g, shift_ms=0.0, window=None, which=None):
        """cross-correlation of each stem's onset envelope with the times at which its renderer
        starts an attack (attack_starts), curves summed over the group's stems -> peak"""
        which = attacks if which is None else which
        tot, cnt, pn = None, 0, []
        for name, env in env_stem[g].items():
            ts = [t - shift_ms / 1000 for t in which[g].get(name, [])]
            if window is not None:
                ts = [t for t in ts if window[0] <= t * 1000 < window[1]]
            if len(ts) < 3:
                continue
            m = None
            if window is not None:
                m = np.zeros(nframes)
                m[int(window[0]):int(window[1])] = 1.0
            c = xcorr_curve(env if m is None else env * m, onset_train(ts, nframes))
            tot = c * len(ts) if tot is None else tot + c * len(ts)
            cnt += len(ts)
            pn += list(per_note_lags(env, ts))
        if tot is None:
            return None, 0, []
        return peak_of(tot), cnt, pn

    lags, report_align = {}, {}
    q_edges = np.linspace(0, nframes, 5)
    for g, gm in groups.items():
        lat = gm.get("latency_ms", 0)
        lag, cnt, pn = entry_lag(g)
        if lag is None:
            raise SystemExit(f"{g}: no attacks to verify its alignment")
        lags[g] = lag
        el, ecnt, _ = entry_lag(g, which=entries)
        report_align[g] = {
            "attack_rule": ATTACK_RULE.get(gm["renderer"], ATTACK_RULE["default"]),
            "entry_xcorr_lag_ms": round(lag, 2), "entries": cnt,
            "after_silence_xcorr_lag_ms": None if el is None else round(el, 2), "after_silence_notes": ecnt,
            "entry_lag_ms_by_quarter": [None if x[0] is None or x[1] < 10 else round(x[0], 2) for x in
                                        (entry_lag(g, window=(q0, q1)) for q0, q1 in zip(q_edges[:-1], q_edges[1:]))],
            "entry_per_note_lag_ms_median": float(np.median(pn)) if pn else None,
            "entry_per_note_lag_ms_p10_p90": [float(np.percentile(pn, 10)), float(np.percentile(pn, 90))] if pn else None,
            "requested_latency_ms": lat}
        # every note, the group's summed envelope: shows articulation (bowed slurs lead or trail)
        times = [t + lead_in for t, *_ in ons[g]]
        all_lag = xcorr_lag(env_group[g], onset_train(times, nframes))[0]
        pa = per_note_lags(env_group[g], times)
        report_align[g].update({"all_notes_xcorr_lag_ms": round(all_lag, 2), "all_notes": len(times),
                                "all_notes_per_note_lag_ms_median": float(np.median(pa)) if len(pa) else None})
    # optional latency compensation (default none): shift a group earlier by latency_ms, or by its
    # measured entry lag re the reference group ("auto")
    for g, gm in groups.items():
        lat = gm.get("latency_ms", 0)
        comp = (lags[g] - lags[ref_group]) if lat == "auto" else float(lat)
        report_align[g]["compensation_ms"] = round(comp, 2)
        if comp:
            k = int(round(comp / 1000 * SR))
            for s_ in aligned[g]:
                aligned[g][s_] = np.roll(aligned[g][s_], -k, axis=0)
                if k > 0:
                    aligned[g][s_][-k:] = 0
                else:
                    aligned[g][s_][:-k] = 0
            for name in env_stem[g]:          # measured again on the shifted stems
                env_stem[g][name] = fit(onset_envelope(aligned[g][name]), nframes)
            lags[g] = entry_lag(g)[0]
        report_align[g]["entry_lag_after_ms"] = round(lags[g], 2)
        report["groups"][g]["alignment"] = report_align[g]
    inter = {}
    names = list(groups)
    for i, g in enumerate(names):
        for h in names[i + 1:]:
            e = {"entry_lag_difference_ms": round(lags[g] - lags[h], 2)}
            qa, qb = report_align[g]["entry_lag_ms_by_quarter"], report_align[h]["entry_lag_ms_by_quarter"]
            e["entry_lag_difference_ms_by_quarter"] = [None if x is None or y is None else round(x - y, 2)
                                                       for x, y in zip(qa, qb)]
            # direct: the two groups' onset envelopes around the onsets they share (doublings)
            tg = {int(round((t + lead_in) * 1000)) for t, *_ in ons[g]}
            th = {int(round((t + lead_in) * 1000)) for t, *_ in ons[h]}
            shared = sorted(k for k in tg if any(k + d in th for d in range(-3, 4)))
            e["shared_onsets"] = len(shared)
            if len(shared) >= 20:
                mask = np.zeros(nframes)
                for k in shared:
                    mask[max(0, k - 60):k + 60] = 1.0
                e["direct_xcorr_lag_ms"] = round(xcorr_lag(env_group[g] * mask, env_group[h] * mask)[0], 2)
            inter[f"{g}-{h}"] = e
    report["inter_group"] = inter
    worst = max((abs(v["entry_lag_difference_ms"]) for v in inter.values()), default=0.0)
    report["alignment_ok"] = worst < a.max_lag_ms
    report["alignment_worst_ms"] = round(worst, 2)
    for k, v in inter.items():
        print(f"  {k}: attack lag difference {v['entry_lag_difference_ms']:+.2f} ms "
              f"(by quarter {v['entry_lag_difference_ms_by_quarter']})"
              + (f", direct {v['direct_xcorr_lag_ms']:+.2f} ms over {v['shared_onsets']} shared onsets"
                 if "direct_xcorr_lag_ms" in v else ""))
    if not report["alignment_ok"]:
        (out.parent / f"{out.name}.mix.json").write_text(json.dumps(report, indent=1))
        raise SystemExit(f"alignment error {worst:.2f} ms exceeds {a.max_lag_ms} ms (report written)")

    # 5. place and reverberate
    print("  placing and reverberating", flush=True)
    hall = hallmod.Hall(man.get("hall", "detmold"), SR)
    tail = len(hall.ir)
    dry = np.zeros((n + tail, 2))
    wet = np.zeros((n + tail, 2))
    per_group_dry = {}
    for g, gm in groups.items():
        rname = gm["renderer"]
        parts = gm.get("parts", {})
        by_track = {v.get("track"): p for p, v in parts.items()}
        by_inst = {v.get("instrument"): p for p, v in parts.items() if v.get("instrument")}
        wet_db = float(gm.get("wet_db", -4.0))
        feeds = {1.0: np.zeros(n), -1.0: np.zeros(n)}
        gdry = np.zeros((n, 2))
        seats = {}
        for name, x in aligned[g].items():
            part = by_track.get(name) or by_inst.get(name) or next(
                (p for t, p in by_track.items() if t and t.lower() == name.lower()), None)
            inst = parts.get(part, {}).get("instrument") if part else name
            st = stage_for(rname, part, name, inst, gm.get("stage", {}))
            y = place(x, st, rname)
            gdry += y
            feeds[side_of(x, st, rname)] += x.mean(axis=1)
            seats[name] = {k: st.get(k) for k in ("az", "depth", "width")} if rname != "orchestra" else "renderer"
        dry[:n] += gdry
        # the group's hall at unit gain, then scaled: by wet_db (impulse-referenced, hall.py's
        # convention), or so that the hall's energy re the group's dry sound, measured on this
        # music, is hall_re_dry_db (portable between instruments whose spectra excite the hall
        # differently: at the same wet_db the piano's hall is about 2.5 dB stronger than the quartet's)
        gwet = np.zeros((n + tail, 2))
        for sgn, mono in feeds.items():
            if np.any(mono):
                h = hall.ir if sgn > 0 else hall.mirror
                for c in range(2):
                    conv = fftconvolve(mono, h[:, c])[: n + tail]
                    gwet[: len(conv), c] += conv
        unit_ratio = db(float(np.sum(gwet ** 2))) - db(float(np.sum(gdry ** 2)))
        if gm.get("hall_re_dry_db") is not None:
            wet_db = float(gm["hall_re_dry_db"]) - unit_ratio
        wet += gwet * 10 ** (wet_db / 20)
        del gwet
        report["groups"][g]["hall_re_dry_db_program"] = round(unit_ratio + wet_db, 2)
        per_group_dry[g] = gdry
        report["groups"][g]["wet_db"] = round(wet_db, 2)
        report["groups"][g]["c80_db_impulse"] = round(hall.c80(10 ** (wet_db / 20)), 2)
        report["groups"][g]["seats"] = seats
    mix = dry + wet
    del aligned

    # 6. master
    print("  mastering", flush=True)
    mix = sosfilt(butter(2, 18, "high", fs=SR, output="sos"), mix, axis=0)
    env = np.abs(mix).max(axis=1)
    last = int(np.nonzero(env > env.max() * 10 ** (-80 / 20))[0][-1]) + int(0.05 * SR)
    mix = mix[: min(last, len(mix))]
    fade = int(0.3 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    tp = true_peak(mix)
    gnorm = 10 ** (peak_db / 20) / tp
    mix *= gnorm
    out.parent.mkdir(parents=True, exist_ok=True)
    wav, m4a = out.with_suffix(".wav"), out.with_suffix(".m4a")
    with sf.SoundFile(str(wav), "w", SR, 2, subtype="PCM_24") as f:
        f.title = str(man.get("title", out.stem))[:250]
        f.software = "ricercar tools/mix.py"
        f.comment = CREDITS
        f.write(mix.astype(np.float32))
    m4a_tp = encode_m4a(wav, m4a, peak_db)

    # 7. measurements
    print("  measuring", flush=True)
    wav_x = sf.read(str(wav), dtype="float64", always_2d=True)[0]
    all_on = [t for g in groups for t, *_ in ons[g]]
    report["output"] = {
        "wav": str(wav), "m4a": str(m4a), "duration_s": round(len(wav_x) / SR, 2),
        "format": f"{sf.info(str(wav)).samplerate} Hz, {sf.info(str(wav)).channels} ch, {sf.info(str(wav)).subtype}",
        "true_peak_dbtp_wav": round(20 * math.log10(true_peak(wav_x)), 2),
        "true_peak_dbtp_m4a": m4a_tp, "normalise_gain_db": round(20 * math.log10(gnorm), 2),
        **loudness_stats(wav_x),
        "stereo_correlation": round(float(np.corrcoef(wav_x[:, 0], wav_x[:, 1])[0, 1]), 3),
        "mono_fold_down_db": round(db(float(np.mean(wav_x.mean(axis=1) ** 2)))
                                   - db(float(np.mean(wav_x ** 2))), 2),
        "hall_re_dry_db": round(db(float(np.sum(wet[:len(mix)] ** 2))) - db(float(np.sum(dry[:len(mix)] ** 2))), 2),
        **click_scan(wav_x, all_on, lead_in),
    }
    # balance: each group's K-weighted level (dry, after all gains) while it plays, and the levels
    # of the groups relative to each other where they play together
    act = {}
    for g in groups:
        m = np.zeros(len(mix), bool)
        ts = sorted(t for t, *_ in ons[g])
        for t in ts:
            a0 = int((t + lead_in) * SR)
            m[a0:a0 + int(1.0 * SR)] = True
        act[g] = m
        x = per_group_dry[g][: len(mix)] * gnorm
        report["groups"][g]["level_when_playing_lufs"] = round(kw_level(x[m]), 2) if m.any() else None
    if len(groups) > 1:
        both = np.all(np.stack([act[g] for g in groups]), axis=0)
        report["balance_where_all_play"] = {
            "seconds": round(float(both.sum()) / SR, 1),
            **{g: round(kw_level(per_group_dry[g][: len(mix)][both] * gnorm), 2) for g in groups}} \
            if both.any() else None
    curve = []
    for k in range(0, len(wav_x) - 5 * SR, 5 * SR):
        curve.append(round(kw_level(wav_x[k:k + 5 * SR]), 1))
    report["loudness_curve_5s_lufs"] = curve
    rp = out.parent / f"{out.name}.mix.json"
    rp.write_text(json.dumps(report, indent=1))
    o = report["output"]
    print(f"  -> {wav.name}, {m4a.name}: {o['duration_s']} s, {o['integrated_lufs']} LUFS, LRA {o['loudness_range_lu']} LU, "
          f"true peak {o['true_peak_dbtp_wav']} dBTP (m4a {o['true_peak_dbtp_m4a']}), report {rp.name}")
    return report


def encode_m4a(wav: Path, m4a: Path, peak_db: float) -> float:
    """AAC 256 kb/s with afconvert; if the decoded true peak overshoots by more than 0.1 dB, encode
    again from a copy lowered by the overshoot."""
    src = wav
    tmp = None
    tp = None
    for _ in range(3):
        if m4a.exists():
            m4a.unlink()
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "256000", str(src), str(m4a)], check=True)
        with tempfile.TemporaryDirectory() as td:
            dec = Path(td) / "dec.wav"
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEF32", str(m4a), str(dec)], check=True)
            x = sf.read(str(dec), dtype="float64", always_2d=True)[0]
        tp = 20 * math.log10(true_peak(x))
        if tp <= peak_db + 0.1:
            break
        y = sf.read(str(wav), dtype="float64", always_2d=True)[0] * 10 ** ((peak_db - tp - 0.05) / 20)
        tmp = Path(tempfile.mkdtemp()) / "lower.wav"
        sf.write(str(tmp), y.astype(np.float32), SR, subtype="FLOAT")
        src = tmp
    if tmp is not None:
        shutil.rmtree(tmp.parent, ignore_errors=True)
    return round(tp, 2)


if __name__ == "__main__":
    main()
