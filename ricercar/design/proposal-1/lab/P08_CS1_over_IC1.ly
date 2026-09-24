\version "2.24.0"
%% proposal-1 lab: P08 CS1 over IC1
\header { title = "P08 CS1 over IC1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

alto = \absolute {
  f'2 ges'2 |
  g'4. aes'8 bes'4. c''8 |
  bes'2. aes'4~ |
  aes'4 g'4 ges'4 f'4 |
  e'2 r2 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

bass = \absolute {
  bes2 a2 |
  aes4. g8 f4. ees8 |
  f2. ges8 g8~ |
  g4 aes4 a4 bes4 |
  ces'2 r2 |
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
