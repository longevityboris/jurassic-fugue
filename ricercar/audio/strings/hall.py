"""Stage placement and concert-hall reverb for render_quartet.py.

Halls:
  detmold    (default) the measured Konzerthaus Detmold impulse response that
             the piano renderer uses (ricercar/audio/piano/make_ir.py:
             Detmold SRIR database set C, stage source S1, seat 163, omni +
             figure-8 decoded to L/R, direct sound removed, unit energy;
             T20 about 1.5 s mid-band, a clear chamber-music hall).  Zenodo
             record 4116247, CC BY 4.0 (Amengual Gari, Sahin, Eddy, Kob, AES
             149th Convention, 2020).  Built by setup_piano.sh; setup_strings.sh
             runs that step if the file is missing.
  synthetic  stochastic shoebox hall generated here (image-source early
             reflections + frequency-dependent exponential tail, RT60 ~2 s
             mid), no licence constraints.

Each instrument is fed to the hall as the mono source it is.  Source S1 stood
left of centre, so its early reflections lean 1.5 dB to the left; instruments
on the right of the stage use the mirrored response, so every player gets
the stronger early reflections from its own side.
"""
from __future__ import annotations

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

from iowa_common import IR_ROOT

DETMOLD_IR = IR_ROOT / "Detmold-Konzerthaus-S1R163-MS-48k.wav"


def detmold_available() -> bool:
    return DETMOLD_IR.exists()


def place_dry(y: np.ndarray, az: float, width: float = 0.35, depth: float = 0.0, sr: int = 48000) -> np.ndarray:
    """Constant-power pan of a (stereo, anechoic) stem to azimuth `az`
    (degrees, positive = left), narrowing its own stereo width.  `depth` (m
    behind the front desks) adds the extra travel time and -1 dB/m."""
    m = y.mean(axis=1)
    s = 0.5 * (y[:, 0] - y[:, 1]) * width
    p = float(np.clip(-az / 45.0, -1, 1))          # -1 = hard left
    th = (p + 1) * np.pi / 4
    gl, gr = np.cos(th), np.sin(th)
    out = np.stack([m * gl + s, m * gr - s], axis=1) * np.sqrt(2) * 0.7071
    if depth > 0:
        d = int(round(depth / 343.0 * sr))
        out = np.concatenate([np.zeros((d, 2)), out[: len(out) - d]]) * 10 ** (-1.0 * depth / 20)
    return out


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


def synthetic_ir(sr: int, seed: int = 1) -> np.ndarray:
    """Left-of-centre source, ORTF-like pair, direct sound excluded, unit energy."""
    rng = np.random.default_rng(seed)
    L = int(3.2 * sr)
    ir = np.zeros((L, 2))
    room = np.array([34.0, 22.0, 14.0])
    lis = np.array([13.0, 11.0, 3.0])
    th = np.radians(15.0)
    src = lis + np.array([-9.0 * np.cos(th), 9.0 * np.sin(th), -1.8])
    c = 343.0
    ears = [np.array([0, 0.085, 0]), np.array([0, -0.085, 0])]
    beta = 0.82
    t0 = np.linalg.norm(src - lis) / c
    for ch, e in enumerate(ears):
        for nx in range(-3, 4):
            for ny in range(-3, 4):
                for nz in range(-2, 3):
                    order = abs(nx) + abs(ny) + abs(nz)
                    if order > 4 or order == 0:
                        continue
                    img = np.array([
                        nx * room[0] + (src[0] if nx % 2 == 0 else room[0] - src[0]),
                        ny * room[1] + (src[1] if ny % 2 == 0 else room[1] - src[1]),
                        nz * room[2] + (src[2] if nz % 2 == 0 else room[2] - src[2]),
                    ])
                    v = img - (lis + e)
                    d = np.linalg.norm(v)
                    t = d / c - t0
                    if t * sr >= L - 1:
                        continue
                    ang = np.arctan2(v[1], -v[0])
                    aim = np.radians(55 if ch == 0 else -55)
                    card = 0.5 + 0.5 * np.cos(ang - aim)
                    g = (beta ** order) * card / max(d, 1.0)
                    i = int(t * sr)
                    fr = t * sr - i
                    ir[i, ch] += g * (1 - fr)
                    ir[i + 1, ch] += g * fr
    t = np.arange(L) / sr
    onset = np.clip((t - 0.012) / 0.07, 0, 1) ** 2
    ref = np.max(np.abs(ir))
    for ch in range(2):
        noise = rng.standard_normal(L)
        tail = np.zeros(L)
        for band, rt in zip(_bands(noise, sr), RT60):
            tail += band * np.exp(-6.91 * t / rt)
        tail *= onset
        tail *= ref * 0.35 / (np.sqrt(np.mean(tail[int(0.08 * sr): int(0.2 * sr)] ** 2)) + 1e-12)
        ir[:, ch] += tail
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


# ------------------------------------------------------------------- hall
class Hall:
    def __init__(self, name: str, sr: int):
        self.name = name
        self.sr = sr
        if name == "detmold":
            if not detmold_available():
                raise SystemExit(f"missing {DETMOLD_IR}: run setup_strings.sh (it builds the piano's hall IR)")
            ir, fs = sf.read(str(DETMOLD_IR), dtype="float64", always_2d=True)
            assert fs == sr, "hall IR must be 48 kHz"
        else:
            ir = synthetic_ir(sr)
        self.ir = ir / np.sqrt(np.sum(ir ** 2) / 2)                   # unit energy
        self.mirror = self.ir[:, ::-1].copy()

    def c80(self, g: float) -> float:
        """Clarity of dry (unit impulse) + g * IR, in dB."""
        e = np.sum(self.ir ** 2, axis=1) / 2
        n80 = int(0.080 * self.sr)
        return float(10 * np.log10((1.0 + g * g * e[:n80].sum()) / (g * g * e[n80:].sum())))

    def source(self, mono: np.ndarray, az: float, wet_db: float) -> np.ndarray:
        """Hall response (reflections + tail, no direct sound) of one mono source at azimuth az."""
        g = 10 ** (wet_db / 20)
        h = self.ir if az >= 0 else self.mirror                     # S1 was measured left of centre
        return g * np.stack([fftconvolve(mono, h[:, c])[: len(mono)] for c in range(2)], axis=1)
