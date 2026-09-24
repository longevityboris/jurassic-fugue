% t_e2
\version "2.24.0"
soprano = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  c''2 aes''4 g''4 |   % 5
  f''4 ees''4 des''4 c''8 des''8~ |   % 6
  des''4 f''4 ees''4 d''4 |   % 7
  des''2 c''2 |   % 8
  e''2 r2 |   % 9
}
alto = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  f'2. f'8 e'8 |   % 5
  f'2. f'8 e'8 |   % 6
  f'4. g'8 g'4. bes'8 |   % 7
  bes'2. aes'8 f'8 |   % 8
  g'2 r2 |   % 9
}
tenor = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
  r1 |   % 6
  r1 |   % 7
  r1 |   % 8
  r1 |   % 9
}
bass = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
  r1 |   % 6
  r1 |   % 7
  r1 |   % 8
  r1 |   % 9
}
\score {
  <<
    \new Staff \with { instrumentName = "S" } { \clef "treble" \key bes \minor \soprano }
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
