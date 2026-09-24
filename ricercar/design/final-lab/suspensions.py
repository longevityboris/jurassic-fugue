#!/usr/bin/env python3
"""Count prepared suspensions in a score: a note sounding before a strong beat (1 or 3), dissonant
there against another voice (2nd, 7th, 9th, or a 4th against the lowest voice), resolving down by step.
usage: python3 suspensions.py FILE.ly [-v]"""
import os, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
from lyparse import parse_voice
src = open(sys.argv[1]).read()
V = ['soprano', 'alto', 'tenor', 'bass']
data = {v: [n for n in parse_voice(src, v) if n.midi is not None] for v in V}
end = max(n.end for v in V for n in data[v])
def snd(v, t):
    for n in data[v]:
        if n.start <= t < n.end:
            return n
count, out = 0, []
t = F(0)
while t < end:
    s = {v: snd(v, t) for v in V}
    s = {v: n for v, n in s.items() if n}
    if s:
        low = min(n.midi for n in s.values())
        for v, n in s.items():
            if n.start >= t:
                continue
            i = data[v].index(n)
            nx = data[v][i + 1] if i + 1 < len(data[v]) else None
            if not nx or not (1 <= n.midi - nx.midi <= 2):
                continue
            dis = False
            for w, m in s.items():
                if w == v:
                    continue
                iv = abs(n.midi - m.midi) % 12
                if iv in (1, 2, 10, 11) or (iv == 5 and min(n.midi, m.midi) == low):
                    dis = True
            if dis:
                count += 1
                b = int(t) + 1
                out.append(f"{b}:{float((t - b + 1) * 4 + 1):g} {v} {n.name}->{nx.name}")
    t += F(1, 2)
if '-v' in sys.argv:
    print("\n".join(out))
print(f"prepared suspensions: {count}")
