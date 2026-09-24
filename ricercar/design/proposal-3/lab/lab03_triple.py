"""Lab 03: triple invertible counterpoint S1 / CS1 / CS2 -- all six vertical orders.
Writes lab/03_triple_<order>.ly for each order and checks it."""
import itertools
from p3 import *
from mats import S1, CS1, CS2

lines = {'S1': S1, 'CS1': CS1, 'CS2': mel("r4 g'2 f'2 ees'2 des'2 c'2 bes2 a2 c'4 | des'2")}
res = perms3(lines, ['S1', 'CS1', 'CS2'], 5)
for order, pl, r in res:
    b_, d4, vs, sh, s, _ = r
    k1, k2, _sp = pl
    parts = {vs[0]: [octs(lines[order[0]], sh)], vs[1]: [octs(octs(lines[order[1]], k1), sh)],
             vs[2]: [octs(octs(lines[order[2]], k2), sh)]}
    fn = f"03_triple_{'-'.join(order)}.ly"
    write_lab(fn, f"Proposal 3, lab 03: triple counterpoint, order (top->bottom) {' > '.join(order)}\n"
              f"voices {', '.join(vs)}; B-flat minor frame; 5 bars.", parts, 5)
    s2, _ = check(fn)
    print(fn, s2)
