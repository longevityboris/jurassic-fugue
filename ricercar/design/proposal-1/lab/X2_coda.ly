\version "2.24.0"
%% proposal-1 lab: X2 apotheosis end and coda, bars 75-84
\header { title = "X2 apotheosis end and coda, bars 75-84" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  ees''4. d''8 d''4. c''8 |
  c''1 |
  c''1 |
  bes'1 |
  c''1 |
  d''2 ees''2 |
  d''2 ees''2 |
  bes'2. bes'8 a'8 |
  bes'1 |
  bes'1 |
}

alto = \absolute {
  ges'2 f'2 |
  f'2 ees'2 |
  ees'1 |
  des'1 |
  f'1 |
  f'2 ges'2 |
  f'2 g'2 |
  f'2 g'4 f'4 |
  f'2 ges'2 |
  f'1 |
}

tenor = \absolute {
  bes2 bes2 |
  a2 a2 |
  a1 |
  bes1 |
  a1 |
  bes1 |
  bes1 |
  d'2 ees'4 ees'4 |
  d'2 ees'2 |
  d'1 |
}

bass = \absolute {
  ees2 bes,2 |
  f,1 |
  f,1 |
  ges,1 |
  f,1 |
  bes,1 |
  bes,1 |
  bes,2 ees4 f4 |
  bes,1 |
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
