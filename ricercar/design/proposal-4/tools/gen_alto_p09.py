import sys, time
sys.path.insert(0, '.')
from p4 import *; from mats import *
from solve import Solver, show
from fractions import Fraction as F
S1e = cat(S1_CORE, ly("c''2"))
bass = real(aug(A1_CORE, 2), -14, -24)
sop = S2 + real(S1_CORE, 0, 0)
ten = cat(CSA_ANS[:-1], ly("c2 r2 | r1 | r1 | r1"))   # lament bars 1-4 then c at bar 5 half, rests
tot = F(8)
fixed = {'soprano': fill(sop, tot), 'tenor': fill(ten, tot), 'bass': fill(bass, tot)}
PAL = "f g aes a bes b c' des' d' ees' e' f' ges' g' aes' a' bes' c'' des''"
KEY = {10, 0, 1, 3, 5, 6, 8, 9, 7, 4}
S = Solver(fixed, 'alto', palette=PAL, patterns=["4 4 4 4", "8 4 4", "4 4 8", "8 8", "t4 4 4 4", "t4 4 8", "t8 4 4", "6 2 4 4", "4 4 6 2", "t8 8", "12 4"],
           width=500, keep=10, key_pcs=KEY, lo=55, hi=74, inner=30, still_pen=(8, 0.4, 12, 1.0))
t0 = time.time()
sols = S.solve()
print(len(sols), round(time.time() - t0))
for c, ns in sols[:6]:
    print(f'{c:6.1f} ' + show(ns, S.total))
