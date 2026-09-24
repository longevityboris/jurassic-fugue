% P03 triple complex: CSb (S) / answer (A) / CSa (T), answer context
\version "2.24.0"
soprano = \absolute {
  c''4 des''8 ees''8 f''8 ees''8 des''8 c''8 |   % 1
  aes''4 g''8 f''8 ees''8 des''8 c''8 bes'8 |   % 2
  a'4 bes'4 c''4 des''4~ |   % 3
  des''4 ees''4 f''2 |   % 4
  e''2 r2 |   % 5
}
alto = \absolute {
  f'2. f'8 e'8 |   % 1
  f'2. f'8 e'8 |   % 2
  f'4. g'8 g'4. bes'8 |   % 3
  bes'2. aes'8 f'8 |   % 4
  g'2 r2 |   % 5
}
tenor = \absolute {
  bes2 a2 |   % 1
  aes2 g4. ges8 |   % 2
  f2 e2 |   % 3
  ees2 d4. des8 |   % 4
  c2 r2 |   % 5
}
bass = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
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
