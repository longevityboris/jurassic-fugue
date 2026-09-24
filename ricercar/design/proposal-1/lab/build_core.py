"""Regenerate the core proof labs of proposal-1 and record checker summaries.

python3 build_core.py  -> writes lab/P*.ly and prints one summary line per lab
(also written to lab/proofs_core.txt).  Materials come from mats.py.
"""
import io, contextlib, itertools
from fractions import Fraction as F
from ricer import *
from mats import *
from perm import place, pick_voices

RESULTS = []


def record(name, voices, title, bars=None):
    lab(name, voices, title)
    out = check(name, bars)
    cnt, strong, tot = summary(out)
    st = strict(out)
    line = (f"{name:34s} PAR!={cnt['PAR!']} BEAT={cnt['BEAT']} DIS!={cnt['DIS!']} D4?={cnt['D4?']} "
            f"DIR={cnt['DIR']} CROS={cnt['CROS']} MEL={cnt['MEL']} ERR={cnt['ERR']} strict={len(st)}")
    RESULTS.append(line)
    print(line)
    for l in out.splitlines():
        if l[:4] in ('PAR!', 'BEAT', 'DIS!', 'D4? ', 'ERR ', 'DIR ', 'CROS', 'MEL '):
            print('      ' + l)
    for l in st:
        print('      strict: ' + l)
    return out


def perm_labs(prefix, lines, title):
    for order in itertools.permutations(lines):
        b = place(order, lines)
        cost, octs, ls = b
        vs = pick_voices(ls)
        record(f"{prefix}_{'-'.join(order)}.ly", dict(zip(vs, ls)), f"{title}: {' / '.join(order)}")


if __name__ == '__main__':
    # P01-P02: S1 / CS1 double counterpoint at the octave (both positions)
    record('P01_S1_over_CS1.ly', dict(alto=S1, tenor=octave(CS1, -1)), 'P01 S1 over CS1 (8ve)')
    record('P02_CS1_over_S1.ly', dict(alto=CS1, tenor=octave(S1, -1)), 'P02 CS1 over S1 (8ve)')
    # P03: answer + CS1 (exposition bars 5-9 texture)
    record('P03_CS1_over_A1.ly', dict(soprano=transpose(CS1, 4, 7), alto=octave(A1, -1)), 'P03 CS1 over answer')
    # P04: CS1 at the 12th below the subject (bass), and above the answer
    record('P04_S1_over_CS1at12.ly', dict(alto=S1, bass=transpose(CS1, -11, -19)), 'P04 CS1 inverted at the 12th (bass)')
    record('P05_A1_over_CS1at12.ly', dict(soprano=A1, alto=CS1), 'P05 answer over CS1 (12th)')
    # P06: triple counterpoint S1 / CS1 / CS2, all six permutations
    perm_labs('P06', {'S1': S1, 'CS1': CS1, 'CS2': CS2}, 'P06 triple counterpoint')
    # P07: the same trio in mirror inversion
    perm_labs('P07', {'I1': I1, 'IC1': IC1, 'IC2': IC2}, 'P07 mirrored trio')
    open('proofs_core.txt', 'w').write('\n'.join(RESULTS) + '\n')
