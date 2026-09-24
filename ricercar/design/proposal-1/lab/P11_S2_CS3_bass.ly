\version "2.24.0"
%% proposal-1 lab: P11 S2 (D-flat) + CS3 + bass
\header { title = "P11 S2 (D-flat) + CS3 + bass" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  ees''4. c''8 aes'4 f''8 des''8 |
  ees''2. aes''8 des''8 |
  ges''4. f''8 f''4. ees''8 |
  ees''1 |
  ees''2 r2 |
}

alto = \absolute {
  c'2 f'2 |
  ges'4 f'4 ees'4 f'4 |
  bes'2 aes'4 ges'4 |
  aes'4 bes'4 c''4 des''4 |
  c''2 r2 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

bass = \absolute {
  c2 des2 |
  ges2 aes4 f4 |
  ees2 f4 ees4 |
  aes2 c2 |
  aes2 r2 |
}

\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "S" } << \global \soprano >>
    \new Staff \with { instrumentName = "A" } << \global \alto >>
    \new Staff \with { instrumentName = "T" } << \global \clef "treble_8" \tenor >>
    \new Staff \with { instrumentName = "B" } << \global \clef bass \bass >>
  >>
  \layout { }
  \midi { \tempo 2 = 46 }
}
