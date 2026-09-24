\version "2.24.0"
%% proposal-1 lab: X1 climax exit, bars 65-69
\header { title = "X1 climax exit, bars 65-69" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'4 bes'8 a'8 bes'4. c''8 |
  c''4. ees''8 ees''2~ |
  ees''4 des''8 bes'8 c''2~ |
  c''1 |
  bes'1 |
}

alto = \absolute {
  f'2 f'2 |
  a'2 aes'2 |
  bes'2 bes'2 |
  bes'4 a'4 a'2 |
  f'1 |
}

tenor = \absolute {
  des'2 des'2 |
  ges'2 f'4 ees'4 |
  ees'2 e'2 |
  f'2 ees'2 |
  d'1 |
}

bass = \absolute {
  bes,1 |
  bes,2 aes,4 f,4 |
  g,2 ges,2 |
  f,2 f,2 |
  bes,1 |
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
