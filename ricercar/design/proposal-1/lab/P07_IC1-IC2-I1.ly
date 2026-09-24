\version "2.24.0"
%% proposal-1 lab: P07 mirrored trio: IC1 / IC2 / I1
\header { title = "P07 mirrored trio: IC1 / IC2 / I1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'2 a'2 |
  aes'4. g'8 f'4. ees'8 |
  f'2. ges'8 g'8~ |
  g'4 aes'4 a'4 bes'4 |
  ces''2 r2 |
}

alto = \absolute {
  r4 bes4 c'4 des'8 ees'8 |
  f'4 ees'4 des'4 c'4 |
  des'4 ees'4 c'4. des'8 |
  ees'2 f'4. g'8 |
  aes'2 r2 |
}

tenor = \absolute {
  f2. f8 ges8 |
  f2. f8 ges8 |
  f4. ees8 ees4. c8 |
  c2. des8 f8 |
  ees2 r2 |
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
