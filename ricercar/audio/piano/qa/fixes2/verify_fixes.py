#!/usr/bin/env python3
"""Re-check the QA round-2 defects after the fixes. Audio goes to /tmp/pianofix2, results to
qa/fixes2/results/*.json. Run make_fix_probes.py first.

    python3 verify_fixes.py contract   # 1, 6: GM CC1 reset, duplicate track names
    python3 verify_fixes.py tail       # 3: ff staccato chord, hall tail per octave band
    python3 verify_fixes.py release    # 5: hammer-noise release timing after key-up (iso probe)
    python3 verify_fixes.py velsweep   # 4: brightness and level across velocity layers
    python3 verify_fixes.py hall       # 2: hall-to-dry and program C80 on the demo; fast16 articulation
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import scipy.signal as ss

HERE = Path(__file__).resolve().parent
PIANO = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "round2"))
from lib2 import SR, read  # noqa: E402

P = Path("/tmp/pianofix2")
RES = HERE / "results"


def render(mid: Path, out: str, *extra: str, stems: bool = False) -> dict:
    cmd = [sys.executable, str(PIANO / "render_piano.py"), str(mid), "-o", str(P / out), "--no-m4a",
           "--json", str(P / f"{out}.render.json"), *extra]
    if stems:
        cmd += ["--stems", str(P / f"{out}_stems")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (P / f"{out}.log").write_text(r.stdout + r.stderr)
    if r.returncode != 0:
        raise SystemExit(f"render {out} failed:\n{r.stderr[-2000:]}")
    return json.loads((P / f"{out}.render.json").read_text())


def save(name: str, res: dict) -> None:
    RES.mkdir(exist_ok=True)
    (RES / f"{name}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1)[:4000])


def contract() -> None:
    def summary(r):
        return {"cc_dynamics": r["cc_dynamics"], "normalise_gain_db": r["normalise_gain_db"],
                "voices": {k: {"notes": v["notes"], "velocity_in": v["velocity_in_range"],
                               "velocity_eff": v["velocity_eff_range"], "rms_dbfs_prenorm": v["rms_dbfs_prenorm"],
                               "cc_dynamics_db_mean": v["cc_dynamics_db_mean"]} for k, v in r["voices"].items()},
                "warnings": r["warnings"]}
    res = {
        "gm_cc1reset_default": summary(render(P / "gm_cc1reset.mid", "gm_default")),
        "gm_cc1reset_--cc-dynamics_velocity": summary(render(P / "gm_cc1reset.mid", "gm_velocity", "--cc-dynamics", "velocity")),
        "gm_cc1reset_--cc-dynamics_off": summary(render(P / "gm_cc1reset.mid", "gm_off", "--cc-dynamics", "off")),
        "odd_names_default": summary(render(P / "odd_names.mid", "odd_names")),
        "odd_names_--transpose_soprano.2=-12": summary(render(P / "odd_names.mid", "odd_names_tr", "--transpose", "soprano.2=-12")),
    }
    save("midi_contract", res)


def band_sos(fc: float):
    return ss.butter(3, [fc / 2 ** 0.5, min(fc * 2 ** 0.5, 23000)], "band", fs=SR, output="sos")


def tail() -> None:
    """ff staccato chord, default render: per-band level after key-up (10 ms frames) and decay
    slopes early (0.5-1.2 s) and late (1.3-2.2 s): a truncated IR shows a cliff after ~1.3 s."""
    rep = render(P / "ffchord_end.mid", "ffchord_end")
    x = read(P / "ffchord_end.wav")
    keyup = 0.3 + 1.0 + 0.4  # lead-in + note-on at 1.0 s (480 ticks at 120 bpm) + 0.4 s held
    out = {"file_duration_s": round(len(x) / SR, 2), "keyup_s": keyup, "render_wet_db": rep["wet_db"]}
    for fc in (63, 125, 250, 500, 1000):
        y = ss.sosfiltfilt(band_sos(fc), x, axis=0)
        e = (y ** 2).sum(axis=1)
        fr = SR // 100
        n = len(e) // fr
        env = 10 * np.log10(e[: n * fr].reshape(n, fr).mean(axis=1) + 1e-30)
        env -= env.max()
        t = np.arange(n) / 100 - keyup

        def slope(a, b):
            s = (t >= a) & (t < b) & (env > -95)
            return round(float(np.polyfit(t[s], env[s], 1)[0]), 1) if s.sum() > 5 else None
        out[f"band_{fc}"] = {
            "level_db_re_band_peak_after_keyup": {f"{a:g}": round(float(env[np.argmin(np.abs(t - a))]), 1)
                                                  for a in (0.3, 0.6, 0.9, 1.2, 1.3, 1.4, 1.5, 1.8, 2.1, 2.4)
                                                  if a + keyup < len(x) / SR},
            "slope_0p5_1p2s_db_per_s": slope(0.5, 1.2),
            "slope_1p3_1p45s_db_per_s": slope(1.3, 1.45),
            "slope_1p3_2p2s_db_per_s": slope(1.3, 2.2),
        }
    bb = (x ** 2).sum(axis=1)
    fr = SR // 100
    n = len(bb) // fr
    env = 10 * np.log10(bb[: n * fr].reshape(n, fr).mean(axis=1) + 1e-30)
    env -= env.max()
    t = np.arange(n) / 100 - keyup
    out["broadband_db_re_peak"] = {f"{a:g}": round(float(env[np.argmin(np.abs(t - a))]), 1)
                                   for a in (0.5, 1.0, 1.25, 1.3, 1.35, 1.4, 1.45, 1.6, 1.8, 2.0, 2.2)
                                   if a + keyup < len(x) / SR}
    steps = np.diff(env[t > 0.2])
    out["largest_10ms_drop_after_keyup_db"] = round(float(-steps.min()), 1)
    save("tail_truncation", out)


def main() -> None:
    P.mkdir(exist_ok=True)
    what = sys.argv[1:] or ["contract"]
    for w in what:
        globals()[w]()


if __name__ == "__main__":
    main()
