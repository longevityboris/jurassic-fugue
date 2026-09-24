#!/usr/bin/env python3
"""Build the stereo concert-hall impulse response used by render_piano.py.

Usage::

    python3 make_ir.py [--width 1.0] [--out PATH]

Source: *Open Database of Spatial Room Impulse Responses at Detmold University
of Music*, set C ("Dense KH"), Detmold Konzerthaus (a concert hall of about
600 seats), stage source S1, audience seat 163 (row 7, centre block).
Amengual Gari, Sahin, Eddy and Kob, AES 149th Convention (2020).
Zenodo record 4116247, licence CC-BY 4.0. ``setup_piano.sh`` extracts the
files.

At that seat the database has an omni (``Omni/S1R163.wav``) and a lateral
figure-8 (``Fig8/S1R163.wav``, a Schoeps CCM8) measured together. Together
they form a coincident Mid/Side pair, which this script decodes to L/R:

* **Polarity.** Band-passed to 200-1500 Hz, the direct sound in the figure-8
  correlates with the omni at +0.98. The dummy head at the same seat hears
  the direct sound 9.7 dB louder in the left ear, so S1 is on the listener's
  left and the figure-8's positive lobe points left. S = +fig8.
* **Side gain.** In a diffuse field a figure-8 captures 1/3 of an omni's
  energy (-4.8 dB). The side gain is set so that the late tail (0.4-1.4 s)
  of S sits 4.8 dB below M, which gives matched sensitivities without trusting
  the dataset's mic gains. ``--width`` scales S further. L = M + S, R = M - S.
* **Direct sound removed.** The dry close-miked piano supplies the direct
  sound, so the IR starts 1 ms before the direct peak and the first 2.5 ms
  after it are faded out. What remains is the hall's own reflections and
  tail, keeping their natural delay relative to the direct sound.
* **Clean-up.** 25 Hz high-pass for rumble and measurement noise, a 150 ms
  raised-cosine fade at the end (the file is 1.5 s long and the tail is
  already 68 dB below the direct sound there), and scaling to unit energy, so
  that ``--wet-db`` in render_piano.py is the reverb-to-dry energy ratio.

Measured on the source (Schroeder T20 of the omni): about 1.7 s at 125 Hz,
1.5 s at 500 Hz-2 kHz and 1.3 s at 4 kHz. This is a warm, clear chamber-music
hall acoustic, suitable for Bach on a grand piano.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import scipy.signal as ss
import soundfile as sf

from piano_paths import DETMOLD_DIR, HALL_IR, SR

OMNI = DETMOLD_DIR / "SetC_DenseKH_LSOrchestra/Data/Omni/S1R163.wav"
FIG8 = DETMOLD_DIR / "SetC_DenseKH_LSOrchestra/Data/Fig8/S1R163.wav"
DUMMY = DETMOLD_DIR / "SetC_DenseKH_LSOrchestra/Data/DummyHead/S1R163.wav"


def band(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return ss.sosfiltfilt(ss.butter(4, [lo, hi], "band", fs=SR, output="sos"), x, axis=0)


def t20(x: np.ndarray) -> float:
    """Broadband-ish Schroeder T20 (500 Hz-2 kHz) in seconds."""
    y = band(x, 500, 2000)
    e = y**2
    edc = np.cumsum(e[::-1])[::-1]
    edc_db = 10 * np.log10(edc / edc.max() + 1e-30)
    i5 = int(np.argmax(edc_db < -5))
    i25 = int(np.argmax(edc_db < -25))
    return 3 * (i25 - i5) / SR


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the M/S hall IR (see module docstring).")
    ap.add_argument("--width", type=float, default=1.0, help="extra side gain (1.0 = matched M/S)")
    ap.add_argument("--out", default=str(HALL_IR))
    args = ap.parse_args()

    m, sr_m = sf.read(OMNI, dtype="float64")
    f, sr_f = sf.read(FIG8, dtype="float64")
    d, sr_d = sf.read(DUMMY, dtype="float64")
    assert sr_m == sr_f == sr_d == SR

    p = int(np.argmax(np.abs(m)))

    # Which side is the source on? (dummy head, direct sound)
    pd = int(np.argmax(np.abs(d).max(axis=1)))
    w = slice(pd - 48, pd + 96)
    lr_db = 10 * np.log10(np.sum(d[w, 0] ** 2) / np.sum(d[w, 1] ** 2))
    source_left = lr_db > 0
    # Polarity of the figure-8 relative to the omni for the direct sound.
    mb, fb = band(m, 200, 1500), band(f, 200, 1500)
    w = slice(p - 50, p + 100)
    lags = range(-8, 9)
    corr = [np.sum(mb[w] * np.roll(fb, k)[w]) / np.sqrt(np.sum(mb[w] ** 2) * np.sum(np.roll(fb, k)[w] ** 2)) for k in lags]
    c = corr[int(np.argmax(np.abs(corr)))]
    pos_lobe_left = (c > 0) == source_left
    s = f if pos_lobe_left else -f

    tail = slice(int(0.4 * SR), int(1.4 * SR))
    g = np.sqrt(np.sum(m[tail] ** 2) / (3.0 * np.sum(s[tail] ** 2))) * args.width

    left = m + g * s
    right = m - g * s
    ir = np.stack([left, right], axis=1)

    # Start 1 ms before the direct sound; fade the direct sound itself out.
    ir = ir[p - 48 :]
    n = np.arange(len(ir))
    t0, t1 = 48 + int(0.0005 * SR), 48 + int(0.0025 * SR)
    win = np.clip((n - t0) / (t1 - t0), 0, 1)
    win = 0.5 - 0.5 * np.cos(np.pi * win)
    ir *= win[:, None]

    ir = ss.sosfilt(ss.butter(2, 25, "high", fs=SR, output="sos"), ir, axis=0)
    nf = int(0.150 * SR)
    ir[-nf:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, nf)))[:, None]
    ir /= np.sqrt(np.sum(ir**2) / 2)

    sf.write(args.out, ir.astype(np.float32), SR, subtype="FLOAT")
    corr_lr = np.corrcoef(ir[int(0.3 * SR) : int(1.2 * SR), 0], ir[int(0.3 * SR) : int(1.2 * SR), 1])[0, 1]
    info = {
        "source": "Detmold SRIR database, set C, Konzerthaus, S1R163 (Omni + Fig8 -> M/S)",
        "zenodo": "https://zenodo.org/records/4116247",
        "licence": "CC-BY 4.0",
        "citation": "Amengual Gari, S. V.; Sahin, B.; Eddy, D.; Kob, M.: Open Database of Spatial Room Impulse "
        "Responses at Detmold University of Music, AES 149th Convention, 2020.",
        "source_side_db_dummy_head": round(float(lr_db), 2),
        "fig8_vs_omni_direct_corr": round(float(c), 3),
        "fig8_positive_lobe": "left" if pos_lobe_left else "right",
        "side_gain": round(float(g), 4),
        "t20_500_2k_s": round(t20(m[p:]), 2),
        "tail_lr_correlation": round(float(corr_lr), 3),
        "length_s": round(len(ir) / SR, 3),
    }
    with open(str(args.out).rsplit(".", 1)[0] + ".json", "w") as fh:
        json.dump(info, fh, indent=1)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
