\version "2.24.0"
%% proposal-1 lab: P10 S2 (F major) over S1
\header { title = "P10 S2 (F major) over S1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

alto = \absolute {
  g'4. e'8 c'4 a'8 f'8 |
  g'2. c''8 f'8 |
  bes'4. a'8 a'4. g'8 |
  g'1 |
  g'2 r2 |
}

tenor = \absolute {
  bes2. bes8 a8 |
  bes2. bes8 a8 |
  bes4. c'8 c'4. ees'8 |
  ees'2. des'8 bes8 |
  c'2 r2 |
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
