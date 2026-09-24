"""Materials of proposal-1 (tonic level, B-flat minor, 2/2, one bar = 1)."""
from ricer import *

# Subject I: theme bars 1-4 at real rhythm + the landing c'' (theme bar 5 downbeat).
S1 = parse("bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' | c''2")
# Real answer (dominant, F minor)
A1 = transpose(S1, 4, 7)
# CS1 (tonic level, written above S1 when S1 is at bes).  Chromatic arch:
# landing 5^ held, rise f-ges-g-aes-bes (+ c neighbour mirroring the subject's a),
# then 7-6 and 4-3 suspensions triggered by the subject's rise, chromatic fall to e.
CS1 = parse("f'2 ges'2 | g'4. aes'8 bes'4. c''8 | bes'2. aes'4~ | aes'4 g'4 ges'4 f'4 | e'2")
# Subject I inverted (mirror 1^<->5^, harmonic minor): f ges f | ... | c des f | ees
I1 = mirror(S1)
# Subject II: theme bars 5-7 + landing (B-flat minor, begins on the dominant)
S2 = parse("c''4. a'8 f'4 des''8 bes' | c''2. f''8 bes' | ees''4. des''8 des''4. c''8 | c''2")

# augmented forms
S1aug = augment(S1)
A1aug = augment(A1)
# full theme (S1 + S2, elided on the shared c''): 8 bars in B-flat minor
THEME = S1[:-1] + shift(S2, 4)
# B-flat MAJOR versions (des -> d) for the apotheosis
def major(line):
    return [(s, d, (p[0], p[1] + 1) if p and p[1] % 12 == 1 else p) for s, d, p in line]
S1M, S2M, THEMEM = major(S1), major(S2), major(THEME)
S1Maug = augment(S1M)
HMAJ = [0, 2, 4, 5, 7, 9, 11]
I1M = mirror(S1M, scale=HMAJ)          # major-mode mirror (f g f ...)
I1Maug = augment(I1M)
S2Maug = augment(S2M)
