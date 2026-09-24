\version "2.24.0"
%% proposal-1 lab: P08 S1 over I1 (offset 0)
\header { title = "P08 S1 over I1 (offset 0)" tagline = ##f }
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
  f'2. f'8 ges'8 |
  f'2. f'8 ges'8 |
  f'4. ees'8 ees'4. c'8 |
  c'2. des'8 f'8 |
  ees'2 r2 |
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
