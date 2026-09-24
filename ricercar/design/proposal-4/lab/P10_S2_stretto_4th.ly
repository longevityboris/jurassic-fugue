% P10 Part II (bars 19-24): S2 on g' (alto, f minor) and S2 at the lower 4th on d' (tenor, c minor) 2 bars later
\version "2.24.0"
soprano = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
  r1 |   % 6
}
alto = \absolute {
  g'4. e'8 c'4 aes'8 f'8 |   % 1
  g'2. c''8 f'8 |   % 2
  bes'4. aes'8 aes'4. g'8 |   % 3
  g'1 |   % 4
  r1 |   % 5
  r1 |   % 6
}
tenor = \absolute {
  r1 |   % 1
  r1 |   % 2
  d'4. b8 g4 ees'8 c'8 |   % 3
  d'2. g'8 c'8 |   % 4
  f'4. ees'8 ees'4. d'8 |   % 5
  d'1 |   % 6
}
bass = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
  r1 |   % 6
}
\score {
  <<
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "T" } { \clef "treble_8" \key bes \minor \tenor }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
