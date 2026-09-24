#!/usr/bin/env python3
"""Derive a calibrated SFZ instrument from Salamander Grand Piano V3.

Usage::

    python3 make_sfz.py            # analyse all samples, write the derived SFZs + calibration JSON
    python3 make_sfz.py --report   # also print the per-note analysis tables

Salamander (Yamaha C5, 16 velocity layers, CC-BY 3.0, Alexander Holm) is an
excellent library, but three things in its stock SFZ matter for expressive
counterpoint. This script fixes them without touching the audio files:

1. **Onset jitter.** The attack sits 5-31 ms into the file and the delay
   differs between layers of the same note. For example, A5 is 11 ms late at
   v1 and 31 ms late at v16. A crescendo that crosses layers would drag, and a
   voice brought out with higher velocity would sound late. Each region gets an
   ``offset=`` so playback starts 2.5 ms before the -20 dB point of the attack
   (``ampeg_attack=0.001`` hides the cut).

2. **Loudness steps between layers.** The stock SFZ selects a layer by velocity
   and adds ``amp_veltrack=73``. The recorded layers are not evenly spaced
   (C4 v14 is louder than v16), so velocity-to-loudness has jumps of up to
   4 dB and some inversions. We measure every sample (K-weighted RMS of the
   first 400 ms after the attack), make the layer loudness monotonic, and build
   a continuous target curve L(v) through the layer anchors plus the author's
   veltrack contribution. Each region then gets ``volume=`` and a per-velocity
   ``amp_velcurve_N`` with ``amp_veltrack=100``, so that inside the region the
   sample is scaled onto L(v). The timbre still changes layer by layer, which is
   the point of 16 layers, while loudness is continuous and monotonic. Below
   the softest layer's anchor the curve continues down 10 dB, so velocities
   1-26 are not all equally loud.

3. **Keyboard evenness and intonation.** The sampled notes are spaced a minor
   third apart, so every sample serves three keys, and one uneven sample affects
   all three. At each of 13 velocities (10, 20 ... 120, 127) the per-note
   loudness is fitted with a smooth keyboard trend and the deviation corrected
   (clipped to +/-4 dB), then interpolated between those velocities: the soft
   layers of a sample can be 3-5 dB off their neighbours while the loud ones are
   even. Tuning is measured from the samples (partial 1 from C4 up, partials 2-3
   below, as a tuner sets the bass octaves; median of three layers). A smooth
   stretch curve is fitted, each sample gets ``tune=`` toward it (clipped to
   +/-8 cents), and ``pitch_keytrack`` = 100 + the local slope of the curve, so
   the two neighbouring keys a sample also serves follow the curve instead of
   sharing its offset (which left 8-12 cent steps in the top octave). The
   piano's natural stretch tuning is kept (bass flat, treble sharp), but single
   notes that are a few cents off their neighbours are corrected.

4. **Damper release.** The stock SFZ fades every lifted key A0-E6 over the same
   1 s, so in a fast passage the previous note still sounds only 8-10 dB under the
   next one, and the bass blurs. The release now runs from 0.5 s in the bottom
   octave to 0.35 s from F2 upwards (per region), which separates successive 16ths
   by about 17 dB. The undamped keys F6-C8 keep their 5 s.

5. **Stereo.** The samples were recorded with a spaced pair, and for many notes
   one channel arrives up to 3 ms after the other. Summed to mono such notes
   partly cancel (C5: L/R correlation -0.82, 8 dB lost in mono; A3, A4, D#5,
   D#6, A6, D#7 also negative), and in the hall's L-to-L / R-to-R convolution
   the image of a line jumps with the phase of each sample. Every note gets one
   inter-channel delay, the same for its 16 layers, from the L/R
   cross-correlation of the first 400 ms averaged over the layers (the smallest
   lag within 0.03 of the best one, up to 3 ms), and aligned copies are written
   to ``samples-aligned/`` (FLAC, lossless shift). The level difference between
   the channels, which carries the low-left/high-right image, is untouched.
   Correlation per note and mono loss before and after are in the calibration
   JSON. Copies are only rewritten when a note's lag changes.

The release groups (string-resonance releases harmL/harmS/harmV3, hammer-noise
releases rel1..88) and the pedal-noise group are copied verbatim. Both derived
files start with ``<control> hint_ram_based=1``: sfizz then holds every sample in
RAM. Streamed from disk, ``sfizz_render`` (which renders about 30 times faster
than real time) can overrun the 8192-frame preload, and the note stops dead
160-180 ms after its onset while the key is still held. Note regions
also get ``note_polyphony=2`` so that re-struck keys under the pedal do not
pile up. A second SFZ without the pedal-noise group is written for the extra
stems of a multi-stem render, so that the noise sounds once and not once per
voice.

Outputs (next to the original SFZ, see piano_paths.py):
    samples-aligned/*.flac, samples-aligned/alignment.json
    SalamanderGrandPiano-Ricercar.sfz
    SalamanderGrandPiano-Ricercar-nopedalnoise.sfz
    SalamanderGrandPiano-Ricercar.calibration.json   (velocity -> dB curve used by render_piano.py)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import scipy.signal as ss
import soundfile as sf

from piano_paths import (
    CALIBRATION_JSON,
    DERIVED_SFZ,
    DERIVED_SFZ_NO_PEDAL_NOISE,
    SALAMANDER_DIR,
    SALAMANDER_SFZ,
    SR,
)

PREROLL = int(0.0025 * SR)  # samples kept before the -20 dB attack point
LOUD_WIN = int(0.400 * SR)  # loudness window after the attack
EXTRA_PP_DB = 10.0  # how far below the softest layer's anchor velocity 1 sits
VELTRACK = 0.73  # the author's amp_veltrack, reproduced as a continuous curve
EVEN_VELS = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 127)  # evenness smoothed at each
EVEN_CLIP_DB = 4.0
TUNE_CLIP_CENTS = 8.0
TUNE_LAYERS = (8, 10, 12)  # median over three layers
P1_FROM_KEY = 60  # below C4 a note's pitch is judged by partials 2-3, as a tuner sets octaves
ALIGNED_DIR = SALAMANDER_DIR / "samples-aligned"  # L/R time-aligned copies of the 480 note samples
ALIGN_MAX_MS = 3.0  # largest inter-channel delay corrected
ALIGN_TOL = 0.03  # correlation tolerance when preferring the smallest lag
ALIGN_WIN = int(0.400 * SR)
ALIGN_METHOD = "xcorr400ms-mean16-max3ms-tol0.03-v1"  # change when the alignment rule changes
# Damper release (ampeg_release, s) of the damped keys A0-E6. The stock 1 s lets the
# previous note of a fast passage sound only 8-10 dB under the current one. Real dampers
# stop the treble within a few tenths of a second and the heavy bass strings more slowly,
# so the release runs from 0.5 s (A0-C#1) down to 0.35 s (from F2), per sample region.
# The recorded string-resonance and hammer release samples still sound on top. The
# undamped keys F6-C8 keep the stock 5 s.
DAMPED_RELEASE = ((24, 0.50), (42, 0.35))  # (sample root key, release s), linear between

NOTE_RE = re.compile(r"samples/([A-G]#?)(\d)v(\d+)\.flac")
PC = {"C": 0, "D#": 3, "F#": 6, "A": 9}

# ITU-R BS.1770 K-weighting at 48 kHz.
K1_B = [1.53512485958697, -2.69169618940638, 1.19839281085285]
K1_A = [1.0, -1.69065929318241, 0.73248077421585]
K2_B = [1.0, -2.0, 1.0]
K2_A = [1.0, -1.99004745483398, 0.99007225036621]


@dataclass
class Region:
    sample: str
    opcodes: dict
    group_opcodes: dict
    root: str = ""
    layer: int = 0
    key: int = 0
    lovel: int = 1
    hivel: int = 127
    onset: int = 0
    attack20: int = 0
    loud_db: float = 0.0
    extra: dict = field(default_factory=dict)


GENERATOR_TAG = "generator make_sfz.py sha256="


def generator_sha256() -> str:
    """SHA-256 of this script. It is written into the derived SFZ header, so that
    setup_piano.sh and render_piano.py can tell a stale instrument from a current one."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + f".tmp{os.getpid()}")
    tmp.write_text(text)
    os.replace(tmp, path)


def parse_opcodes(text: str) -> dict:
    out = {}
    for tok in text.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
    return out


def read_sfz_sections(path):
    """Split the stock SFZ into (note regions, verbatim release text, verbatim pedal text)."""
    lines = path.read_text().replace("\r\n", "\n").split("\n")
    regions: list[Region] = []
    group = {}
    rel_start = next(i for i, l in enumerate(lines) if l.startswith("//Release string resonances"))
    ped_start = next(i for i, l in enumerate(lines) if l.startswith("//pedalAction"))
    for line in lines[:rel_start]:
        s = line.strip()
        if s.startswith("<group>"):
            group = parse_opcodes(s[len("<group>"):])
        elif s.startswith("<region>"):
            ops = parse_opcodes(s[len("<region>"):])
            r = Region(sample=ops["sample"], opcodes=ops, group_opcodes=dict(group))
            m = NOTE_RE.search(r.sample)
            r.root = f"{m.group(1)}{m.group(2)}"
            r.layer = int(m.group(3))
            r.key = 12 * (int(m.group(2)) + 1) + PC[m.group(1)]
            r.lovel = int(ops.get("lovel", 1))
            r.hivel = int(ops.get("hivel", 127))
            regions.append(r)
    release_text = "\n".join(lines[rel_start:ped_start]).rstrip() + "\n"
    pedal_text = "\n".join(lines[ped_start:]).rstrip() + "\n"
    return regions, release_text, pedal_text


def kweight(x: np.ndarray) -> np.ndarray:
    return ss.lfilter(K2_B, K2_A, ss.lfilter(K1_B, K1_A, x, axis=0), axis=0)


def analyse_audio(r: Region, x: np.ndarray) -> None:
    """Attack position, playback offset and K-weighted loudness of one (aligned) sample."""
    a = np.abs(x).max(axis=1)
    peak = a.max()
    t20 = int(np.argmax(a > peak * 0.1))
    r.attack20 = t20
    r.onset = max(0, t20 - PREROLL)
    y = kweight(x[r.onset : r.onset + PREROLL + LOUD_WIN])
    r.loud_db = float(10 * np.log10(np.mean(np.sum(y**2, axis=1)) + 1e-20))
    r.extra["peak_db"] = float(20 * np.log10(peak))


def partial_cents(m: np.ndarray, key: int, k: int) -> float | None:
    """Cents deviation of partial k from k times the 12-TET fundamental (A4 = 440 Hz).

    The strongest spectral peak (prominence >= 6 dB) within +/-60 cents is taken: the
    band edge can sit on the skirt of a stronger neighbouring component (C8 has one
    about 100 cents up), and a plain arg-max would pick the edge. Its frequency is the
    power-weighted mean of the bins within 15 cents of it that are no more than 10 dB
    down, so that the slightly detuned strings of a unison (two peaks a few cents apart,
    as on A6) count together.
    """
    n = 1 << 20
    spec = np.abs(np.fft.rfft(m * np.hanning(len(m)), n))
    freqs = np.fft.rfftfreq(n, 1 / SR)
    fk = k * 440.0 * 2 ** ((key - 69) / 12)
    if fk * 2 ** (60 / 1200) > 0.45 * SR:
        return None
    idx = np.nonzero((freqs > fk * 2 ** (-60 / 1200)) & (freqs < fk * 2 ** (60 / 1200)))[0]
    s = spec[idx]
    peaks, _ = ss.find_peaks(20 * np.log10(s + 1e-30), prominence=6.0)
    if len(peaks) == 0:
        return None
    i = idx[peaks[np.argmax(s[peaks])]]
    near = np.nonzero((np.abs(1200 * np.log2(freqs[idx] / freqs[i])) < 15) & (s > spec[i] * 10 ** (-10 / 20)))[0]
    w = spec[idx[near]] ** 2
    f = float(np.sum(freqs[idx[near]] * w) / np.sum(w))
    return float(1200 * np.log2(f / fk))


def measure_tuning(layers: dict[int, np.ndarray], key: int) -> float:
    """Cents deviation of the sampled note from 12-TET (A4 = 440 Hz): partial 1 from C4
    up, the mean of partials 2 and 3 below (the fundamental of a wound bass string is
    weak and pulled by the soundboard; a tuner sets those octaves by the partials).
    Median over layers 8, 10, 12 (aligned audio), 0.3-2.3 s after the attack."""
    vals = []
    for layer in TUNE_LAYERS:
        m = layers[layer].mean(axis=1)
        on = int(np.argmax(np.abs(m) > 0.1 * np.abs(m).max()))
        seg = m[on + int(0.3 * SR) : on + int(2.3 * SR)]
        parts = [1] if key >= P1_FROM_KEY else [2, 3]
        c = [partial_cents(seg, key, k) for k in parts]
        c = [v for v in c if v is not None]
        if c:
            vals.append(float(np.mean(c)))
    return float(np.median(vals))


def lr_xcorr(x: np.ndarray, maxlag: int) -> np.ndarray:
    """Normalised L/R cross-correlation over the first ALIGN_WIN after the attack, for
    lags -maxlag..maxlag (positive: the right channel arrives later)."""
    a = np.abs(x).max(axis=1)
    on = int(np.argmax(a > 0.1 * a.max()))
    seg = x[on : on + ALIGN_WIN]
    L, R = seg[:, 0], seg[:, 1]
    n = len(L)
    xc = np.fft.irfft(np.conj(np.fft.rfft(L, 2 * n)) * np.fft.rfft(R, 2 * n), 2 * n)
    return np.concatenate([xc[-maxlag:], xc[: maxlag + 1]]) / np.sqrt(np.sum(L * L) * np.sum(R * R) + 1e-30)


def shift_lr(x: np.ndarray, lag: int) -> np.ndarray:
    """Advance the later channel by |lag| samples (the file gets |lag| samples shorter)."""
    if lag > 0:
        return np.stack([x[: len(x) - lag, 0], x[lag:, 1]], axis=1)
    if lag < 0:
        return np.stack([x[-lag:, 0], x[: len(x) + lag, 1]], axis=1)
    return x


def corr_mono(x: np.ndarray) -> tuple[float, float]:
    """L/R correlation and mono fold-down level re stereo (dB) over the first ALIGN_WIN."""
    a = np.abs(x).max(axis=1)
    on = int(np.argmax(a > 0.1 * a.max()))
    L, R = x[on : on + ALIGN_WIN, 0], x[on : on + ALIGN_WIN, 1]
    c = float(np.sum(L * R) / np.sqrt(np.sum(L * L) * np.sum(R * R) + 1e-30))
    mono = 10 * np.log10(np.mean(((L + R) / 2) ** 2) / np.mean((L * L + R * R) / 2) + 1e-30)
    return c, float(mono)


def align_root(layers: list[Region], sidecar: dict) -> dict:
    """Time-align the two channels of every layer of one sampled note, write the aligned
    copies (unless the sidecar says they exist with this lag), analyse the aligned audio.

    Salamander was recorded with a spaced pair, so for many notes the right channel
    arrives up to a few ms after the left (or before it). Summed to mono, and in the
    L/R correlation, such notes partly cancel: C5 had correlation -0.82 and lost 8 dB in
    mono. One lag per note (the same for all 16 layers, so the image does not jump with
    velocity) is chosen from the L/R cross-correlation averaged over the layers, within
    +/-ALIGN_MAX_MS; among lags within ALIGN_TOL of the best correlation the smallest is
    taken, because on a periodic tone every period gives an equally good match.
    """
    root = layers[0].root
    raw = {}
    for r in layers:
        data, sr = sf.read(SALAMANDER_DIR / r.sample, dtype="int32", always_2d=True)
        assert sr == SR, f"{r.sample}: expected {SR} Hz, got {sr}"
        raw[r.layer] = data
    maxlag = int(ALIGN_MAX_MS / 1000 * SR)
    acc = np.mean([lr_xcorr(d / 2.0**31, maxlag) for d in raw.values()], axis=0)
    lags = np.arange(-maxlag, maxlag + 1)
    ok = np.nonzero(acc >= acc.max() - ALIGN_TOL)[0]
    lag = int(lags[ok[np.argmin(np.abs(lags[ok]))]])
    reuse = sidecar.get(root) == lag
    before, after, aligned = [], [], {}
    for r in layers:
        name = Path(r.sample).name
        dst = ALIGNED_DIR / name
        y = shift_lr(raw[r.layer], lag)
        if not (reuse and dst.exists()):
            tmp = dst.with_name(f".{name}.tmp{os.getpid()}.flac")
            sf.write(tmp, y, SR, subtype="PCM_24", format="FLAC")
            os.replace(tmp, dst)
        x0 = raw[r.layer] / 2.0**31
        yf = y / 2.0**31
        before.append(corr_mono(x0))
        after.append(corr_mono(yf))
        r.sample = f"{ALIGNED_DIR.name}/{name}"
        analyse_audio(r, yf)
        aligned[r.layer] = yf
    tuning = measure_tuning(aligned, layers[0].key)
    return {
        "lag_samples": lag,
        "lag_ms": round(lag / SR * 1000, 3),
        "corr_before": round(float(np.median([b[0] for b in before])), 3),
        "corr_after": round(float(np.median([a[0] for a in after])), 3),
        "mono_db_before": round(float(np.median([b[1] for b in before])), 2),
        "mono_db_after": round(float(np.median([a[1] for a in after])), 2),
        "tuning_cents": tuning,
        "rewritten": not reuse,
    }


def isotonic(y: np.ndarray) -> np.ndarray:
    """Pool-adjacent-violators, non-decreasing."""
    blocks = [[v, 1] for v in y]
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] > blocks[i + 1][0]:
            v = (blocks[i][0] * blocks[i][1] + blocks[i + 1][0] * blocks[i + 1][1]) / (blocks[i][1] + blocks[i + 1][1])
            blocks[i] = [v, blocks[i][1] + blocks[i + 1][1]]
            del blocks[i + 1]
            i = max(i - 1, 0)
        else:
            i += 1
    return np.concatenate([[v] * n for v, n in blocks])


def veltrack_db(v: np.ndarray | float) -> np.ndarray:
    return 20 * np.log10((1 - VELTRACK) + VELTRACK * (np.asarray(v, dtype=float) / 127.0) ** 2)


def loudness_curve(layers: list[Region]) -> np.ndarray:
    """Target loudness (dB) for velocities 0..127 for one sampled note."""
    layers = sorted(layers, key=lambda r: r.layer)
    raw = np.array([r.loud_db for r in layers])
    mono = isotonic(raw)
    for i in range(1, len(mono)):
        mono[i] = max(mono[i], mono[i - 1] + 0.25)
    centres = np.array([(r.lovel + r.hivel) / 2 for r in layers])
    anchors_v = np.concatenate([[1.0], centres, [127.0]])
    anchors_db = np.concatenate(
        [
            [mono[0] + veltrack_db(centres[0]) - EXTRA_PP_DB],
            mono + veltrack_db(centres),
            [mono[-1] + veltrack_db(127.0)],
        ]
    )
    v = np.arange(128, dtype=float)
    curve = np.interp(v, anchors_v, anchors_db)
    curve[0] = curve[1]
    return curve


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report", action="store_true", help="print per-note analysis tables")
    args = ap.parse_args()

    regions, release_text, pedal_text = read_sfz_sections(SALAMANDER_SFZ)
    roots = {}
    for r in regions:
        roots.setdefault(r.root, []).append(r)
    root_keys = sorted({(r.key, r.root) for r in regions})

    # --- stereo alignment + per-sample analysis ---------------------------------------------
    ALIGNED_DIR.mkdir(exist_ok=True)
    side_path = ALIGNED_DIR / "alignment.json"
    side = json.loads(side_path.read_text()) if side_path.exists() else {}
    known = side.get("lags", {}) if side.get("method") == ALIGN_METHOD else {}
    print(f"aligning and analysing {len(regions)} note samples ...")
    align = {root: align_root(sorted(roots[root], key=lambda r: r.layer), known) for _, root in root_keys}
    write_atomic(side_path, json.dumps({"method": ALIGN_METHOD,
                                        "lags": {root: a["lag_samples"] for root, a in align.items()}}, indent=1))
    rewritten = sum(a["rewritten"] for a in align.values())
    print(f"aligned copies in {ALIGNED_DIR} ({rewritten} of {len(align)} notes rewritten)")

    # --- tuning ---------------------------------------------------------------------------
    keys = np.array([k for k, _ in root_keys], dtype=float)
    cents = np.array([align[root]["tuning_cents"] for k, root in root_keys])
    coef = np.polyfit(keys, cents, 4)
    smooth = np.polyval(coef, keys)
    slope = np.polyval(np.polyder(coef), keys)  # cents per key of the stretch curve
    tune = {root: round(float(np.clip(s - c, -TUNE_CLIP_CENTS, TUNE_CLIP_CENTS)), 1)
            for (k, root), c, s in zip(root_keys, cents, smooth)}
    # Each sample serves up to three keys. pitch_keytrack = 100 + the local slope of the
    # stretch curve, so the neighbours follow the curve too instead of sharing the root's
    # offset (which left 8-12 cent steps between sample groups in the top octave).
    keytrack = {root: round(100.0 + float(np.clip(d, -2.0, 8.0)), 2) for (k, root), d in zip(root_keys, slope)}

    # --- loudness -------------------------------------------------------------------------
    curves = {root: loudness_curve(roots[root]) for _, root in root_keys}
    # Keyboard evenness at every dynamic, not just one: at each anchor velocity the
    # per-note levels are fitted with a smooth keyboard trend (cubic in key), the
    # deviation is corrected (clipped to +/-EVEN_CLIP_DB), and the correction is
    # interpolated between anchor velocities. Soft layers of one sample can sit 3-5 dB
    # off their neighbours while the loud layers are even.
    fix_at = np.zeros((len(EVEN_VELS), len(root_keys)))
    for i, v in enumerate(EVEN_VELS):
        lv = np.array([curves[root][v] for _, root in root_keys])
        fit = np.polyval(np.polyfit(keys, lv, 3), keys)
        fix_at[i] = np.clip(fit - lv, -EVEN_CLIP_DB, EVEN_CLIP_DB)
    level_fix = {}
    for j, (_, root) in enumerate(root_keys):
        fix = np.interp(np.arange(128), EVEN_VELS, fix_at[:, j])
        level_fix[root] = {v: float(f) for v, f in zip(EVEN_VELS, fix_at[:, j])}
        c = isotonic(curves[root] + fix)  # a velocity-dependent fix must not break monotonicity
        curves[root] = c + np.arange(128) * 1e-4  # and strictly increasing, for the inverse curve
    # Global trim: loudest target equals loudest raw sample (keeps float headroom sane).
    top = max(c[127] for c in curves.values())
    raw_top = max(r.loud_db for r in regions)
    for root in curves:
        curves[root] = curves[root] - (top - raw_top)

    # --- write SFZ ------------------------------------------------------------------------
    header = [
        "//=====================================================================",
        "// Salamander Grand Piano V3 (Yamaha C5) -- Alexander Holm, CC-BY 3.0",
        "// FLAC/SFZ packaging: FreePats (roberto@zenvoid.org), V3+20200602",
        "// Derived by ricercar/audio/piano/make_sfz.py: onset-aligned offsets,",
        "// continuous velocity->loudness calibration, keyboard evenness, tuning",
        "// smoothing. DO NOT EDIT -- regenerate with make_sfz.py.",
        f"// {GENERATOR_TAG}{generator_sha256()}",
        "//=====================================================================",
        "",
        # Load every sample into RAM. sfizz_render renders far faster than real time, and
        # its disk streaming can fall behind the 8192-frame preload: the voice then stops
        # 160-180 ms after note-on with a click while the key is still held (a dropped note).
        "<control> hint_ram_based=1",
        "",
    ]
    body = []
    groups_seen = []
    for r in regions:
        g = r.group_opcodes
        gkey = tuple(sorted(g.items()))
        damped = float(g.get("ampeg_release", "1")) < 2
        if not groups_seen or groups_seen[-1] != gkey:
            groups_seen.append(gkey)
            release = f"{DAMPED_RELEASE[-1][1]:g}" if damped else g.get("ampeg_release", "5")
            body.append("")
            body.append(f"<group> amp_veltrack=100 ampeg_attack=0.001 ampeg_release={release} note_polyphony=2")
        curve = curves[r.root]
        vels = np.arange(r.lovel, r.hivel + 1)
        gain_db = curve[vels] - r.loud_db
        vol = float(gain_db.max())
        lin = 10 ** ((gain_db - vol) / 20)
        ops = [
            f"sample={r.sample}",
            f"lokey={r.opcodes['lokey']}",
            f"hikey={r.opcodes['hikey']}",
            f"lovel={r.lovel}",
            f"hivel={r.hivel}",
            f"pitch_keycenter={r.key}",
            f"offset={r.onset}",
            f"tune={tune[r.root]:g}",
            f"pitch_keytrack={keytrack[r.root]:g}",
            f"volume={vol:.2f}",
        ]
        if damped and r.key < DAMPED_RELEASE[-1][0]:
            (k0, r0), (k1, r1) = DAMPED_RELEASE
            ops.append(f"ampeg_release={np.interp(r.key, [k0, k1], [r0, r1]):.3f}")
        ops += [f"amp_velcurve_{v}={g_:.5f}" for v, g_ in zip(vels, lin)]
        body.append("<region> " + " ".join(ops))

    common = "\n".join(header + body) + "\n\n" + release_text
    # Atomic writes: a render that starts while this runs sees the old or the new file,
    # never a half-written instrument.
    write_atomic(DERIVED_SFZ, common + "\n" + pedal_text)
    write_atomic(DERIVED_SFZ_NO_PEDAL_NOISE, common)
    print(f"wrote {DERIVED_SFZ}")
    print(f"wrote {DERIVED_SFZ_NO_PEDAL_NOISE}")

    # --- calibration JSON -----------------------------------------------------------------
    # Average velocity->dB curve (relative to velocity 127) over the keys a
    # four-voice keyboard piece actually uses (C2..C6).
    use = [root for k, root in root_keys if 36 <= k <= 84]
    rel = np.mean([curves[r] - curves[r][127] for r in use], axis=0)
    marks = {}
    for name, db in [("ppp", -33), ("pp", -27), ("p", -21), ("mp", -15), ("mf", -10), ("f", -6), ("ff", -3), ("fff", 0)]:
        marks[name] = int(np.clip(np.searchsorted(rel, db), 1, 127))
    calib = {
        "description": "Mean velocity->loudness curve of the derived SFZ, dB relative to velocity 127, "
        "averaged over sampled notes C2..C6 (K-weighted RMS of the first 400 ms).",
        "velocity_db": [round(float(x), 3) for x in rel],
        "suggested_velocities": marks,
        "tuning_cents_measured": {root: round(float(c), 1) for (_, root), c in zip(root_keys, cents)},
        "tuning_cents_applied": tune,
        "pitch_keytrack_applied": keytrack,
        "stereo_alignment": {root: {k: v for k, v in a.items() if k not in ("tuning_cents", "rewritten")}
                             for root, a in align.items()},
        "level_fix_db": {k: {str(v): round(f, 2) for v, f in d.items()} for k, d in level_fix.items()},
        "onset_ms": {f"{r.root}v{r.layer}": round(r.attack20 / SR * 1000, 2) for r in regions},
        "layer_loudness_db": {f"{r.root}v{r.layer}": round(r.loud_db, 2) for r in regions},
    }
    write_atomic(CALIBRATION_JSON, json.dumps(calib, indent=1))
    print(f"wrote {CALIBRATION_JSON}")

    on = np.array([r.attack20 for r in regions]) / SR * 1000
    print(f"attack (-20 dB) position in the raw files: {on.min():.1f}..{on.max():.1f} ms "
          f"(spread {on.max() - on.min():.1f} ms) -> aligned to {PREROLL / SR * 1000:.1f} ms by offset=")
    print("suggested velocities:", marks)
    if args.report:
        print("\nnote  key  tune(meas->applied) keytrack  level_fix v20/v50/v80/v110  layer loudness v1..v16 (dB)")
        for k, root in root_keys:
            ls = " ".join(f"{r.loud_db:6.1f}" for r in sorted(roots[root], key=lambda r: r.layer))
            lf = "/".join(f"{level_fix[root][v]:+.1f}" for v in (20, 50, 80, 110))
            print(f"{root:4s} {k:4d}  {calib['tuning_cents_measured'][root]:+6.1f} -> {tune[root]:+5.1f} "
                  f"{keytrack[root]:7.2f}  {lf:>22s}   {ls}")
        print("\nstereo alignment: note  lag(ms)  corr before -> after  mono dB before -> after")
        for k, root in root_keys:
            a = align[root]
            print(f"  {root:4s} {a['lag_ms']:+6.2f}  {a['corr_before']:+.2f} -> {a['corr_after']:+.2f}   "
                  f"{a['mono_db_before']:+5.1f} -> {a['mono_db_after']:+5.1f}")
        print("\nvelocity -> dB (rel. v127):")
        print(" ".join(f"{v}:{rel[v]:.1f}" for v in range(1, 128, 6)))


if __name__ == "__main__":
    main()
