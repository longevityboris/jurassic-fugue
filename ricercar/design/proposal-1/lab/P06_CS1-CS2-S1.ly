\version "2.24.0"
%% proposal-1 lab: P06 triple counterpoint: CS1 / CS2 / S1
\header { title = "P06 triple counterpoint: CS1 / CS2 / S1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  f'2 ges'2 |
  g'4. aes'8 bes'4. c''8 |
  bes'2. aes'4~ |
  aes'4 g'4 ges'4 f'4 |
  e'2 r2 |
}

alto = \absolute {
  r4 f'4 ees'4 des'8 c'8 |
  bes4 c'4 des'4 ees'4 |
  des'4 c'4 ees'4. des'8 |
  c'2 bes4. aes8 |
  g2 r2 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

bass = \absolute {
  bes,2. bes,8 a,8 |
  bes,2. bes,8 a,8 |
  bes,4. c8 c4. ees8 |
  ees2. des8 bes,8 |
  c2 r2 |
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
