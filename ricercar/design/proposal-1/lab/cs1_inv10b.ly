\version "2.24.0"
%% proposal-1 lab: cs1_inv10b
\header { title = "cs1_inv10b" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

alto = \absolute {
  bes'2. bes'8 a'8 |
  bes'2. bes'8 a'8 |
  bes'4. c''8 c''4. ees''8 |
  ees''2. des''8 bes'8 |
  c''2 r2 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

bass = \absolute {
  des,2 ees,2 |
  e,4. f,8 ges,4. aes,8 |
  ges,2. f,4~ |
  f,4 e,4 ees,4 des,4 |
  cis,2 r2 |
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
