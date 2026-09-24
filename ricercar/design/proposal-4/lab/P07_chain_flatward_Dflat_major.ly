% P07 Part III stretto chain (bars 37-46): S1 e-flat (S), a-flat (A), then D-flat MAJOR (T), each a fifth lower, 2 bars apart
\version "2.24.0"
soprano = \absolute {
  ees''2. ees''8 d''8 |   % 1
  ees''2. ees''8 d''8 |   % 2
  ees''4. f''8 f''4. aes''8 |   % 3
  aes''2. ges''8 ees''8 |   % 4
  f''2 r2 |   % 5
  r1 |   % 6
  r1 |   % 7
  r1 |   % 8
  r1 |   % 9
  r1 |   % 10
}
alto = \absolute {
  r1 |   % 1
  r1 |   % 2
  aes'2. aes'8 g'8 |   % 3
  aes'2. aes'8 g'8 |   % 4
  aes'4. bes'8 bes'4. des''8 |   % 5
  des''2. ces''8 aes'8 |   % 6
  bes'2 r2 |   % 7
  r1 |   % 8
  r1 |   % 9
  r1 |   % 10
}
tenor = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  des'2. des'8 c'8 |   % 5
  des'2. des'8 c'8 |   % 6
  des'4. ees'8 ees'4. ges'8 |   % 7
  ges'2. f'8 des'8 |   % 8
  ees'2 r2 |   % 9
  r1 |   % 10
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
  r1 |   % 10
}
\score {
  <<
    \new Staff \with { instrumentName = "S" } { \clef "treble" \key bes \minor \soprano }
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "T" } { \clef "treble_8" \key bes \minor \tenor }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
