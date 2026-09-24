\version "2.24.0"
%% proposal-1 lab: P08 IC1 over CS1
\header { title = "P08 IC1 over CS1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

alto = \absolute {
  bes'2 a'2 |
  aes'4. g'8 f'4. ees'8 |
  f'2. ges'8 g'8~ |
  g'4 aes'4 a'4 bes'4 |
  ces''2 r2 |
}

tenor = \absolute {
  f2 ges2 |
  g4. aes8 bes4. c'8 |
  bes2. aes4~ |
  aes4 g4 ges4 f4 |
  e2 r2 |
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
