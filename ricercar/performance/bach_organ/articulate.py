#!/usr/bin/env python3
"""Baroque organ articulation for a perform.py / orchestrate.py organ MIDI: move key-ups only.

usage: python3 articulate.py SCORE.ly PLAN.json IN.mid OUT.mid [--json REPORT]

An organ key has no dynamics, so the touch is all an organist has: the length of each note
against the next. perform.py's piano target releases every note 12 ms (40 ms under a quarter)
before its notated end and a repeated note 60 ms before. This script replaces that with an
"articulated legato" read from the score, voice by voice:

* step (1-2 semitones) into the next note of the voice: legato, the key comes up 8 ms before
  the next key goes down (the organ renderer plays that key early by half its pipes' speech,
  so the two pipes overlap by a few ms, as under the fingers);
* repeated note (same key): detached, gap = 25 % of the note, 70-150 ms, so the pipe
  re-speaks clearly (the arioso's pulsing eighths come out lightly separated, the tolling
  tonic pedal is re-struck);
* leap of a third: slight detachment, gap = 10 % of the note, 30-60 ms;
* leap of a fourth or more: gap = 14 % of the note, 40-90 ms;
* a note before a notated rest and the last note of a voice keep perform.py's release (the rest
  is the articulation).

Key-downs are never moved and no key-up goes past the note's notated end or the next key-down,
so orchestrate.py's integrity check (every note at its notated onset, none past its notated end)
holds. The notes are matched to the score in order per voice (pitch checked note by note).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import mido

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools"))
from lyparse import parse_voice  # noqa: E402
import perform  # noqa: E402

LEGATO_GAP_S = 0.008
MIN_SOUNDING_TICKS = 40


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def gap_for(interval: int, dur_s: float) -> tuple[str, float]:
    if interval == 0:
        return "repeat", clamp(0.25 * dur_s, 0.070, 0.150)
    if interval <= 2:
        return "step", LEGATO_GAP_S
    if interval <= 4:
        return "third", clamp(0.10 * dur_s, 0.030, 0.060)
    return "leap", clamp(0.14 * dur_s, 0.040, 0.090)


class TempoMap:
    def __init__(self, mid: mido.MidiFile):
        pts, t = [], 0
        for msg in mido.merge_tracks([mid.tracks[0]]):
            t += msg.time
            if msg.type == "set_tempo":
                pts.append((t, msg.tempo))
        if not pts or pts[0][0] != 0:
            pts.insert(0, (0, 500000))
        self.tpq = mid.ticks_per_beat
        self.pts = []          # (tick, sec, us per quarter)
        s = 0.0
        for i, (tk, us) in enumerate(pts):
            if i:
                ptk, pus = pts[i - 1]
                s += (tk - ptk) * pus / 1e6 / self.tpq
            self.pts.append((tk, s, us))

    def _seg_tick(self, tick):
        lo = 0
        for i, p in enumerate(self.pts):
            if p[0] <= tick:
                lo = i
        return self.pts[lo]

    def sec(self, tick):
        tk, s, us = self._seg_tick(tick)
        return s + (tick - tk) * us / 1e6 / self.tpq

    def tick(self, sec):
        lo = 0
        for i, p in enumerate(self.pts):
            if p[1] <= sec:
                lo = i
        tk, s, us = self.pts[lo]
        return int(round(tk + (sec - s) * 1e6 / us * self.tpq))


def read_notes(track):
    """absolute (on, off, pitch, vel, channel) per note, and the non-note messages with ticks."""
    t, pend, notes, other = 0, {}, [], []
    for msg in track:
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            pend.setdefault(msg.note, []).append((t, msg.velocity, msg.channel))
        elif msg.type in ("note_off", "note_on"):
            on, vel, ch = pend[msg.note].pop(0)
            notes.append([on, t, msg.note, vel, ch])
        elif msg.type != "end_of_track":
            other.append((t, msg))
    if any(pend.values()):
        raise SystemExit(f"{track.name}: hanging note-on")
    notes.sort(key=lambda n: (n[0], n[2]))
    return notes, other


def write_track(name, notes, other):
    evs = [(t, 0, m) for t, m in other]
    for on, off, p, vel, ch in notes:
        evs.append((off, 1, mido.Message("note_off", channel=ch, note=p, velocity=0)))
        evs.append((on, 2, mido.Message("note_on", channel=ch, note=p, velocity=vel)))
    evs.sort(key=lambda e: (e[0], e[1]))
    tr, last = mido.MidiTrack(), 0
    for t, _, m in evs:
        tr.append(m.copy(time=t - last))
        last = t
    tr.append(mido.MetaMessage("end_of_track", time=0))
    return tr


def articulate(score, plan_path, mid_in, mid_out, report=None):
    plan = perform.Plan(json.loads(Path(plan_path).read_text()))
    src = Path(score).read_text()
    mid = mido.MidiFile(mid_in)
    tpq = mid.ticks_per_beat
    tm = TempoMap(mid)
    rep = {"input": str(mid_in), "rules": {"legato_gap_ms": LEGATO_GAP_S * 1000,
                                            "repeat": "25% of the note, 70-150 ms",
                                            "third": "10%, 30-60 ms", "leap": "14%, 40-90 ms"},
           "voices": {}}
    out = mido.MidiFile(type=1, ticks_per_beat=tpq)
    out.tracks.append(mid.tracks[0])
    for tr in mid.tracks[1:]:
        name = tr.name.strip().lower()
        notes, other = read_notes(tr)
        if name not in plan.voices:
            out.tracks.append(tr)
            continue
        score_notes = [n for n in parse_voice(src, name, plan.measure) if n.midi is not None]
        if len(score_notes) != len(notes):
            raise SystemExit(f"{name}: {len(notes)} MIDI notes, {len(score_notes)} score notes")
        counts = {"step": 0, "repeat": 0, "third": 0, "leap": 0, "rest": 0, "last": 0}
        changed_ms = []
        for i, (x, n) in enumerate(zip(notes, score_notes)):
            if x[2] != n.midi:
                raise SystemExit(f"{name}: note {i} is {x[2]} in the MIDI, {n.midi} ({n.name}) in the score")
            s_tick = int(n.start * 4 * tpq)
            e_tick = int(n.end * 4 * tpq)
            if i + 1 == len(notes):
                counts["last"] += 1
                continue
            nxt, xn = score_notes[i + 1], notes[i + 1]
            if nxt.start != n.end:
                counts["rest"] += 1
                continue
            dur_s = tm.sec(e_tick) - tm.sec(s_tick)
            kind, gap = gap_for(abs(nxt.midi - n.midi), dur_s)
            counts[kind] += 1
            limit = min(xn[0], e_tick)
            off = tm.tick(tm.sec(limit) - gap)
            off = max(off, x[0] + MIN_SOUNDING_TICKS)
            off = min(off, limit)
            changed_ms.append((tm.sec(off) - tm.sec(x[1])) * 1000)
            x[1] = off
        # guard: same key never re-pressed while still down
        for a, b in zip(notes, notes[1:]):
            if a[2] == b[2] and b[0] < a[1]:
                raise SystemExit(f"{name}: key {a[2]} re-pressed at tick {b[0]} while held to {a[1]}")
        out.tracks.append(write_track(tr.name, notes, other))
        changed_ms.sort()
        rep["voices"][name] = {"notes": len(notes), **counts,
                               "release_moved_ms_median": round(changed_ms[len(changed_ms) // 2], 1) if changed_ms else 0,
                               "release_moved_ms_min": round(changed_ms[0], 1) if changed_ms else 0,
                               "release_moved_ms_max": round(changed_ms[-1], 1) if changed_ms else 0}
    out.save(mid_out)
    if report:
        Path(report).write_text(json.dumps(rep, indent=1))
    for v, r in rep["voices"].items():
        print(f"{v:8s} {r['notes']:4d} notes: step {r['step']}, repeat {r['repeat']}, third {r['third']}, "
              f"leap {r['leap']}, before rest {r['rest']}; key-up moved {r['release_moved_ms_min']:+.0f}.."
              f"{r['release_moved_ms_max']:+.0f} ms (median {r['release_moved_ms_median']:+.0f})")
    return rep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("score")
    ap.add_argument("plan")
    ap.add_argument("mid_in")
    ap.add_argument("mid_out")
    ap.add_argument("--json")
    a = ap.parse_args()
    articulate(a.score, a.plan, a.mid_in, a.mid_out, a.json)
