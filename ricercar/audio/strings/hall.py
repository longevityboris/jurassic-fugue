"""Concert-hall placement and reverb for render_quartet.py.

Two halls:
  marco      measured impulse responses of St Paul's Hall, Huddersfield
             (RT60 about 2.1 s) from the 3D-MARCo database (Lee & Johnson,
             University of Huddersfield, 2019; Zenodo record 3477602).  The
             13 loudspeaker positions (azimuth -90..+90 deg in 15 deg steps, 3 m
             or 4 m from the array) are captured by an ORTF pair (main stereo
             image) and the rear-facing cardioids of the PCMA-3D cube (hall
             bloom).  Licence stated in the database documentation:
             CC BY-NC 3.0 (the Zenodo landing page says CC BY 3.0) - fine for
             personal/educational renders; use --hall synthetic for anything
             commercial.
  synthetic  stochastic hall IR generated here (image-source early
             reflections of a 34 x 22 x 14 m shoebox + frequency-dependent
             exponential late tail, RT60 2.0 s mid), no licence constraints.

Each voice is convolved with the IR of its own stage position, so the
instruments sit at different places in the same room.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

from iowa_common import IR_ROOT

MARCO_DIR = IR_ROOT / "3D-MARCo" / "irs48k"
MARCO_POS = [90, 75, 60, 45, 30, 15, 0, -15, -30, -45, -60, -75, -90]


def marco_available() -> bool:
    return MARCO_DIR.exists() and any(MARCO_DIR.glob("pos*_front.wav"))


def place_dry(y: np.ndarray, az: float, width: float = 0.35) -> np.ndarray:
    """Constant-power pan of a (stereo, anechoic) stem to azimuth `az`
    (ITU: positive = left), narrowing its own stereo width."""
    m = y.mean(axis=1)
    s = 0.5 * (y[:, 0] - y[:, 1]) * width
    p = float(np.clip(-az / 50.0, -1, 1))          # -1 = hard left
    th = (p + 1) * np.pi / 4
    gl, gr = np.cos(th), np.sin(th)
    return np.stack([m * gl + s, m * gr - s], axis=1) * np.sqrt(2) * 0.7071


# ------------------------------------------------------------ synthetic hall
def _bands(x, sr):
    edges = [0, 180, 360, 720, 1440, 2880, 5760, 11520, sr / 2]
    out = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        if lo == 0:
            sos = butter(4, hi, "lowpass", fs=sr, output="sos")
        elif hi >= sr / 2:
            sos = butter(4, lo, "highpass", fs=sr, output="sos")
        else:
            sos = butter(4, [lo, hi], "bandpass", fs=sr, output="sos")
        out.append(sosfilt(sos, x))
    return out


RT60 = [2.5, 2.4, 2.2, 2.0, 1.85, 1.55, 1.1, 0.7]          # per band above


def synthetic_ir(sr: int, az: float, dist: float, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    L = int(3.2 * sr)
    ir = np.zeros((L, 2))
    room = np.array([34.0, 22.0, 14.0])
    # listener (the "main pair") 9 m from the stage front, 3 m up; stage near x = 4
    lis = np.array([13.0, 11.0, 3.0])
    th = np.radians(az)
    src = lis + np.array([-dist * np.cos(th) - 0.0, dist * np.sin(th), -1.8])
    c = 343.0
    ears = [np.array([0, 0.085, 0]), np.array([0, -0.085, 0])]
    beta = 0.82                                       # wall reflection coefficient
    for ch, e in enumerate(ears):
        for nx in range(-3, 4):
            for ny in range(-3, 4):
                for nz in range(-2, 3):
                    order = abs(nx) + abs(ny) + abs(nz)
                    if order > 4:
                        continue
                    img = np.array([
                        nx * room[0] + (src[0] if nx % 2 == 0 else room[0] - src[0]),
                        ny * room[1] + (src[1] if ny % 2 == 0 else room[1] - src[1]),
                        nz * room[2] + (src[2] if nz % 2 == 0 else room[2] - src[2]),
                    ])
                    v = img - (lis + e)
                    d = np.linalg.norm(v)
                    t = d / c
                    if t * sr >= L - 1:
                        continue
                    # cardioid-ish ORTF capsule pointing +-55 deg
                    ang = np.arctan2(v[1], -v[0])
                    aim = np.radians(55 if ch == 0 else -55)
                    card = 0.5 + 0.5 * np.cos(ang - aim)
                    g = (beta ** order) * card / max(d, 1.0)
                    i = int(t * sr)
                    fr = t * sr - i
                    ir[i, ch] += g * (1 - fr)
                    ir[i + 1, ch] += g * fr
    # late diffuse tail, independent per channel, from 25 ms after the direct sound
    t0 = np.linalg.norm(src - lis) / c
    t = np.arange(L) / sr
    onset = np.clip((t - t0 - 0.012) / 0.07, 0, 1) ** 2
    direct_level = np.max(np.abs(ir))
    for ch in range(2):
        noise = rng.standard_normal(L)
        tail = np.zeros(L)
        for band, rt in zip(_bands(noise, sr), RT60):
            tail += band * np.exp(-6.91 * np.maximum(t - t0, 0) / rt)
        tail *= onset
        tail *= direct_level * 0.09 / (np.sqrt(np.mean(tail[int((t0 + 0.08) * sr): int((t0 + 0.2) * sr)] ** 2)) + 1e-12)
        ir[:, ch] += tail
    # gentle air absorption on everything after the direct sound
    return ir


# ------------------------------------------------------------------- hall
class Hall:
    def __init__(self, name: str, sr: int):
        self.name = name
        self.sr = sr

    @lru_cache(maxsize=32)
    def ir(self, az: float, dist: float) -> np.ndarray:
        if self.name == "marco":
            pos = min(MARCO_POS, key=lambda p: abs(p - az))
            front, _ = sf.read(str(MARCO_DIR / f"pos{pos:+03d}_front.wav"), dtype="float64", always_2d=True)
            return front
        return synthetic_ir(self.sr, az, 3.0 + dist, seed=int(az) & 0xFFFF)

    def convolve(self, mono: np.ndarray, az: float, dist: float) -> np.ndarray:
        h = self.ir(float(az), float(dist))
        y = np.stack([fftconvolve(mono, h[:, c])[: len(mono)] for c in range(2)], axis=1)
        return y
