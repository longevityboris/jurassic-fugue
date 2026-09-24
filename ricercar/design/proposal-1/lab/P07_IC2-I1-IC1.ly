\version "2.24.0"
%% proposal-1 lab: P07 mirrored trio: IC2 / I1 / IC1
\header { title = "P07 mirrored trio: IC2 / I1 / IC1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  r4 bes'4 c''4 des''8 ees''8 |
  f''4 ees''4 des''4 c''4 |
  des''4 ees''4 c''4. des''8 |
  ees''2 f''4. g''8 |
  aes''2 r2 |
}

alto = \absolute {
  f'2. f'8 ges'8 |
  f'2. f'8 ges'8 |
  f'4. ees'8 ees'4. c'8 |
  c'2. des'8 f'8 |
  ees'2 r2 |
}

tenor = \absolute {
  bes2 a2 |
  aes4. g8 f4. ees8 |
  f2. ges8 g8~ |
  g4 aes4 a4 bes4 |
  ces'2 r2 |
}

bass = \absolute {
  R1 | R1 | R1 | R1 | R1 |
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
