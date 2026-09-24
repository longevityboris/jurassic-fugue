"""Proposal-3 materials (B-flat minor frame unless noted). Single source of truth for the labs."""
from p3 import mel, tr, inv, aug, at, octs, S1

# Subject I: theme bars 1-4, real rhythm, tweak: bar 4 "des''8 bes'" -> "des''8 c''", then bes' (4-3-2-1 close)
S1 = S1
# Real answer (F minor)
ANS = tr(S1, '5')
# CS1 "lament": chromatic 6-b6-5-#4, then Phrygian turn 5-b6-5; first half-bar free (held/cadence note)
CS1 = mel("r2 g2 | ges2 f2 | e2 f2 | ges2 f2")
# CS2 "cascade": syncopated descending scale g'..a (7-6 / 4-2 suspension chain), cadence a-c'-des'
CS2 = mel("r4 g'2 f'2 ees'2 des'2 c'2 bes2 a2 c'4 | des'2")
# Subject II: theme bars 5-8 (minor), open ending on 2^ over V
S2 = mel("c''4. a'8 f'4 des''8 bes' | c''2. f''8 bes' | ees''4. des''8 des''4. c''8 | c''1")
# Inversion of S1: diatonic mirror about des (1<->5, 2<->4, 3<->3, #7<->b6)
S1I = mel("f'2. f'8 ges' | f'2. f'8 ges' | f'4. ees'8 ees'4. c'8 | c'2. des'8 ees' | f'2")
# Major forms for the apotheosis (B-flat major)
S1M = mel("bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. d''8 c'' | bes'2")
S2M = mel("c''4. a'8 f'4 d''8 bes' | c''2. f''8 bes' | ees''4. d''8 d''4. c''8 | c''1")
THEME_M = mel("bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes' | "
              "c''4. a'8 f'4 d''8 bes' | c''2. f''8 bes' | ees''4. d''8 d''4. c''8 | c''1")
