\version "2.24.0"
%% proposal-1 lab: P07 mirrored trio: IC1 / I1 / IC2
\header { title = "P07 mirrored trio: IC1 / I1 / IC2" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'2 a'2 |
  aes'4. g'8 f'4. ees'8 |
  f'2. ges'8 g'8~ |
  g'4 aes'4 a'4 bes'4 |
  ces''2 r2 |
}

alto = \absolute {
  f'2. f'8 ges'8 |
  f'2. f'8 ges'8 |
  f'4. ees'8 ees'4. c'8 |
  c'2. des'8 f'8 |
  ees'2 r2 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

bass = \absolute {
  r4 bes,4 c4 des8 ees8 |
  f4 ees4 des4 c4 |
  des4 ees4 c4. des8 |
  ees2 f4. g8 |
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
