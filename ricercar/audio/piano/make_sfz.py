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
   third apart, so every sample serves three keys, and one uneven sample
   affects all three. The per-note loudness at velocity 80 is smoothed across
   the keyboard (correction clipped to +/-3 dB). Tuning is measured from the
   samples (fundamental from A2 up, partials 2-3 below). A smooth stretch
   curve is fitted and each note gets ``tune=`` toward that curve (clipped to
   +/-8 cents). The piano's natural stretch tuning is kept (bass flat, treble
   sharp), but single notes that are a few cents off their neighbours are
   corrected. F#4, which also serves F4 and G4, was 5 cents flat.

The release groups (string-resonance releases harmL/harmS/harmV3, hammer-noise
releases rel1..88) and the pedal-noise group are copied verbatim. Note regions
also get ``note_polyphony=2`` so that re-struck keys under the pedal do not
pile up. A second SFZ without the pedal-noise group is written for the extra
stems of a multi-stem render, so that the noise sounds once and not once per
voice.

Outputs (next to the original SFZ, see piano_paths.py):
    SalamanderGrandPiano-Ricercar.sfz
    SalamanderGrandPiano-Ricercar-nopedalnoise.sfz
    SalamanderGrandPiano-Ricercar.calibration.json   (velocity -> dB curve used by render_piano.py)
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field

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
EVEN_VEL = 80  # velocity at which keyboard evenness is smoothed
EVEN_CLIP_DB = 3.0
TUNE_CLIP_CENTS = 8.0

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


def analyse_region(r: Region) -> None:
    x, sr = sf.read(SALAMANDER_DIR / r.sample, dtype="float64", always_2d=True)
    assert sr == SR, f"{r.sample}: expected {SR} Hz, got {sr}"
    a = np.abs(x).max(axis=1)
    peak = a.max()
    t20 = int(np.argmax(a > peak * 0.1))
    r.attack20 = t20
    r.onset = max(0, t20 - PREROLL)
    y = kweight(x[r.onset : r.onset + PREROLL + LOUD_WIN])
    r.loud_db = float(10 * np.log10(np.mean(np.sum(y**2, axis=1)) + 1e-20))
    r.extra["peak_db"] = float(20 * np.log10(peak))


def measure_tuning(root: str, key: int) -> float:
    """Cents deviation of the sampled note from 12-TET (A4 = 440 Hz), layer 10."""
    x, sr = sf.read(SALAMANDER_DIR / "samples" / f"{root}v10.flac", dtype="float64", always_2d=True)
    m = x.mean(axis=1)
    on = int(np.argmax(np.abs(m) > 0.1 * np.abs(m).max()))
    seg = m[on + int(0.3 * sr) : on + int(2.3 * sr)]
    n = 1 << 20
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    freqs = np.fft.rfftfreq(n, 1 / sr)
    f0 = 440.0 * 2 ** ((key - 69) / 12)
    partials = [1] if key >= 45 else [2, 3]
    devs = []
    for k in partials:
        fk = k * f0
        band = (freqs > fk * 2 ** (-60 / 1200)) & (freqs < fk * 2 ** (60 / 1200))
        i = int(np.argmax(np.where(band, spec, 0)))
        a, b, c = np.log(spec[i - 1 : i + 2] + 1e-30)
        p = 0.5 * (a - c) / (a - 2 * b + c)
        devs.append(1200 * np.log2(((i + p) * sr / n) / fk))
    return float(np.mean(devs))


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
    print(f"analysing {len(regions)} note samples ...")
    for r in regions:
        analyse_region(r)

    roots = {}
    for r in regions:
        roots.setdefault(r.root, []).append(r)
    root_keys = sorted({(r.key, r.root) for r in regions})

    # --- tuning ---------------------------------------------------------------------------
    keys = np.array([k for k, _ in root_keys], dtype=float)
    cents = np.array([measure_tuning(root, k) for k, root in root_keys])
    coef = np.polyfit(keys, cents, 4)
    smooth = np.polyval(coef, keys)
    tune = {root: int(round(np.clip(s - c, -TUNE_CLIP_CENTS, TUNE_CLIP_CENTS)))
            for (k, root), c, s in zip(root_keys, cents, smooth)}

    # --- loudness -------------------------------------------------------------------------
    curves = {root: loudness_curve(roots[root]) for _, root in root_keys}
    mid = np.array([curves[root][EVEN_VEL] for _, root in root_keys])
    mid_fit = np.polyval(np.polyfit(keys, mid, 3), keys)
    level_fix = {root: float(np.clip(f - m, -EVEN_CLIP_DB, EVEN_CLIP_DB))
                 for (_, root), m, f in zip(root_keys, mid, mid_fit)}
    for root in curves:
        curves[root] = curves[root] + level_fix[root]
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
        "//=====================================================================",
        "",
    ]
    body = []
    groups_seen = []
    for r in regions:
        g = r.group_opcodes
        gkey = tuple(sorted(g.items()))
        if not groups_seen or groups_seen[-1] != gkey:
            groups_seen.append(gkey)
            release = g.get("ampeg_release", "1")
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
            f"tune={tune[r.root]}",
            f"volume={vol:.2f}",
        ]
        ops += [f"amp_velcurve_{v}={g_:.5f}" for v, g_ in zip(vels, lin)]
        body.append("<region> " + " ".join(ops))

    common = "\n".join(header + body) + "\n\n" + release_text
    DERIVED_SFZ.write_text(common + "\n" + pedal_text)
    DERIVED_SFZ_NO_PEDAL_NOISE.write_text(common)
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
        "level_fix_db": {k: round(v, 2) for k, v in level_fix.items()},
        "onset_ms": {f"{r.root}v{r.layer}": round(r.attack20 / SR * 1000, 2) for r in regions},
        "layer_loudness_db": {f"{r.root}v{r.layer}": round(r.loud_db, 2) for r in regions},
    }
    CALIBRATION_JSON.write_text(json.dumps(calib, indent=1))
    print(f"wrote {CALIBRATION_JSON}")

    on = np.array([r.attack20 for r in regions]) / SR * 1000
    print(f"attack (-20 dB) position in the raw files: {on.min():.1f}..{on.max():.1f} ms "
          f"(spread {on.max() - on.min():.1f} ms) -> aligned to {PREROLL / SR * 1000:.1f} ms by offset=")
    print("suggested velocities:", marks)
    if args.report:
        print("\nnote  key  tune(meas->applied)  level_fix  layer loudness v1..v16 (dB)")
        for k, root in root_keys:
            ls = " ".join(f"{r.loud_db:6.1f}" for r in sorted(roots[root], key=lambda r: r.layer))
            print(f"{root:4s} {k:4d}  {calib['tuning_cents_measured'][root]:+6.1f} -> {tune[root]:+3d}   "
                  f"{level_fix[root]:+5.2f}   {ls}")
        print("\nvelocity -> dB (rel. v127):")
        print(" ".join(f"{v}:{rel[v]:.1f}" for v in range(1, 128, 6)))


if __name__ == "__main__":
    main()
