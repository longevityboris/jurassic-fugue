#!/usr/bin/env python3
"""Full orchestral score (one staff per instrument, concert pitch) from an orchestration spec.

usage: python3 tools/full_score.py [SPEC.json] [-o score/out/orchestra-full.ly]
Defaults: performance/symphonic/symphonic.json. Run from ricercar/. Reads score/music-voices.ly
and design/final-lab/plan.json, gives each part exactly the notes the renderer plays (line windows
with their octave, sustained pedal points, timpani rolls as tremolo), re-spells the rhythm
bar by bar, and writes a LilyPond file that \\includes score/music-global.ly for key, tempo,
rehearsal marks and dynamics. Empty staves are hidden after the first system.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(HERE))
import perform  # noqa: E402
import orchestrate  # noqa: E402
from lyparse import parse_voice  # noqa: E402

NAMES = {
    'fl': ('Flute', 'Fl.', 'treble'), 'ob': ('Oboe', 'Ob.', 'treble'),
    'cl': ('Clarinet I', 'Cl. I', 'treble'), 'cl.2': ('Clarinet II', 'Cl. II', 'treble'),
    'bn': ('Bassoon', 'Bn.', 'bass'), 'hn.1': ('Horn I', 'Hn. I', 'treble'),
    'hn.2': ('Horn II', 'Hn. II', 'treble'), 'tpt': ('Trumpet I', 'Tpt. I', 'treble'),
    'tpt.2': ('Trumpet II', 'Tpt. II', 'treble'), 'tbn': ('Trombone', 'Tbn.', 'bass'),
    'btbn': ('Bass Trombone', 'B. Tbn.', 'bass'), 'tba': ('Tuba', 'Tba.', 'bass'),
    'timp': ('Timpani', 'Timp.', 'bass'), 'vn1': ('Violin I', 'Vn. I', 'treble'),
    'vn2': ('Violin II', 'Vn. II', 'treble'), 'va': ('Viola', 'Va.', 'alto'),
    'vc': ('Violoncello', 'Vc.', 'bass'), 'cb': ('Contrabass', 'Cb.', 'bass_8'),
}
GROUPS = [('Woodwinds', ['fl', 'ob', 'cl', 'cl.2', 'bn']),
          ('Brass', ['hn.1', 'hn.2', 'tpt', 'tpt.2', 'tbn', 'btbn', 'tba']),
          ('Percussion', ['timp']),
          ('Strings', ['vn1', 'vn2', 'va', 'vc', 'cb'])]
LETTER_PC = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)


def ly_pitch(name, midi):
    """spelled name like 'Bb4' / 'F#3' plus the sounding MIDI number -> LilyPond absolute pitch."""
    letter = name[0]
    acc = name[1:].rstrip('0123456789-')
    alter = acc.count('#') - acc.count('b')
    octv = (midi - alter - LETTER_PC[letter]) // 12 - 1
    s = letter.lower() + ('is' * alter if alter > 0 else 'es' * -alter)
    return s + ("'" * (octv - 3) if octv >= 3 else "," * (3 - octv))


NOTE_VALUES = [(F(1), '1'), (F(3, 4), '2.'), (F(1, 2), '2'), (F(3, 8), '4.'), (F(1, 4), '4'),
               (F(3, 16), '8.'), (F(1, 8), '8'), (F(1, 16), '16'), (F(1, 32), '32')]


def allowed(pos, d, rest):
    if d == 1:
        return pos == 0
    if d == F(3, 4):
        return not rest and pos % F(1, 4) == 0
    if d == F(1, 2):
        return pos % (F(1, 2) if rest else F(1, 4)) == 0
    if d == F(3, 8):
        return not rest and pos % F(1, 4) == 0
    if d == F(1, 4):
        return pos % (F(1, 4) if rest else F(1, 8)) == 0
    if d == F(3, 16):
        return not rest and pos % F(1, 8) == 0
    if d == F(1, 8):
        return pos % (F(1, 8) if rest else F(1, 16)) == 0
    return True


def spell(pos, dur, measure=F(1), rest=False):
    """split a span starting at pos (within the piece) into notated durations, barline-aware."""
    out = []
    while dur > 0:
        inbar = pos % measure
        room = min(dur, measure - inbar)
        for d, tok in NOTE_VALUES:
            if d <= room and allowed(inbar, d, rest):
                out.append((pos, d, tok))
                pos += d
                dur -= d
                break
        else:
            raise ValueError(f'cannot spell {dur} at {pos}')
    return out


def part_events(part, spec, voices, plan):
    ev = []  # (start, end, midi, name, roll)
    for w in spec.part_windows(part):
        src = voices[w.voice]
        if w.kind == 'line':
            for n in src:
                if n.midi is not None and w.a <= n.start < w.u:
                    ev.append((n.start, n.end, n.midi + w.octave, n.name, False))
        else:
            class P:  # adapter for orchestrate.pedal_notes (expects .pitch)
                pass
            adapted = []
            for n in src:
                if n.midi is None:
                    continue
                p = P()
                p.start, p.end, p.pitch, p.name, p.dur = n.start, n.end, n.midi, n.name, n.dur
                adapted.append(p)
            for first, last, pitch in orchestrate.pedal_notes(w, adapted, plan):
                roll = w.pedal.get('mode') == 'repeat'
                ev.append((first.start, last.end, pitch + w.octave, first.name, roll))
    ev.sort()
    # trim overlaps (a held note handed off early)
    for i in range(len(ev) - 1):
        if ev[i][1] > ev[i + 1][0]:
            ev[i] = (ev[i][0], ev[i + 1][0]) + ev[i][2:]
    return ev


def engrave_part(events, end, measure):
    toks, t = [], F(0)

    def rest_to(x):
        nonlocal t
        while t < x:
            bar_end = (t // measure + 1) * measure
            if t % measure == 0 and x >= bar_end:
                toks.append('R1')
                t = bar_end
                toks.append('|')
                continue
            seg_end = min(x, bar_end)
            for _, d, tok in spell(t, seg_end - t, measure, rest=True):
                toks.append('r' + tok)
            t = seg_end
            if t % measure == 0:
                toks.append('|')

    for s, e, midi, name, roll in events:
        rest_to(s)
        # octave shift keeps the spelled letter: derive from name letter/accidental, octave from midi
        base = name[:-1] if name[-1].isdigit() else name
        p = ly_pitch(base + '0', midi)
        pieces = spell(s, e - s, measure)
        for i, (pos, d, tok) in enumerate(pieces):
            trem = ':32' if roll else ''
            toks.append(p + tok + trem + (' ~' if i < len(pieces) - 1 else ''))
            if (pos + d) % measure == 0:
                toks.append('|')
        t = e
    rest_to(end)
    # join, one bar per line
    lines, cur = [], []
    for x in toks:
        cur.append(x)
        if x == '|':
            lines.append('  ' + ' '.join(cur))
            cur = []
    if cur:
        lines.append('  ' + ' '.join(cur))
    return '\n'.join(lines)


def main():
    args = sys.argv[1:]
    spec_path = Path(args[0]) if args and not args[0].startswith('-') else R / 'performance/symphonic/symphonic.json'
    out = Path(args[args.index('-o') + 1]) if '-o' in args else R / 'score/out/orchestra-full.ly'
    plan = perform.Plan(json.loads((R / 'design/final-lab/plan.json').read_text()))
    src = (R / 'score/music-voices.ly').read_text()
    voices = {v: parse_voice(src, v, plan.measure) for v in plan.voices}
    end = max(n[-1].end for n in voices.values())
    spec = orchestrate.load_spec(spec_path, plan, end)
    parts = list(spec.groups['orchestra']['parts'].keys())
    body, staves = [], []
    for gname, members in GROUPS:
        members = [m for m in members if m in parts]
        if not members:
            continue
        st = []
        for m in members:
            var = 'part' + ''.join(ch for ch in m.title() if ch.isalpha())
            music = engrave_part(part_events(m, spec, voices, plan), end, plan.measure)
            body.append(f'{var} = \\absolute {{\n{music}\n}}\n')
            full, short, clef = NAMES[m]
            extra = ' \\marks' if m == members[0] and gname == GROUPS[0][0] else ''
            st.append(f'      \\new Staff \\with {{ instrumentName = "{full}" shortInstrumentName = "{short}" }}'
                      f' << \\global{extra} \\clef "{clef}" \\{var} >>')
        dyn = '      \\new Dynamics \\dynamicsLine\n' if gname in ('Woodwinds', 'Strings') else ''
        staves.append(f'    \\new StaffGroup \\with {{ systemStartDelimiter = #\'SystemStartBracket }} <<\n'
                      + dyn + '\n'.join(st) + '\n    >>')
    ly = f'''\\version "2.24.0"
% GENERATED by tools/full_score.py from {spec_path.name} -- the notes each instrument plays in the render.
\\include "music-global.ly"
{''.join(body)}
\\header {{
  title = "The Neighbour"
  subtitle = "Ricercar a 4 on the Theme from Jurassic Park, for orchestra"
  subsubtitle = "Full score in C (all instruments at sounding pitch; contrabass sounds an octave below)"
  composer = "Theme: John Williams (1993)"
  tagline = ##f
}}
\\paper {{ #(set-paper-size "a4") ragged-last-bottom = ##f
  system-system-spacing.basic-distance = #14 }}
\\score {{
  <<
{chr(10).join(staves)}
  >>
  \\layout {{
    #(layout-set-staff-size 15)
    \\context {{ \\Staff \\RemoveEmptyStaves }}
    \\context {{ \\Score
      barNumberVisibility = #all-bar-numbers-visible
      \\override BarNumber.break-visibility = #end-of-line-invisible
      \\override BarNumber.font-size = #-2 }}
  }}
}}
'''
    out.write_text(ly)
    print(f'wrote {out} ({len(parts)} parts, {float(end / plan.measure):g} bars)')


if __name__ == '__main__':
    main()
