\version "2.24.0"
%% proposal-1 lab: cs1_answer
\header { title = "cs1_answer" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  c''2 des''2 |
  d''4. ees''8 f''4. g''8 |
  f''2. ees''4~ |
  ees''4 d''4 des''4 c''4 |
  b'2 r2 |
}

alto = \absolute {
  f'2. f'8 e'8 |
  f'2. f'8 e'8 |
  f'4. g'8 g'4. bes'8 |
  bes'2. aes'8 f'8 |
  g'2 r2 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 |
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
