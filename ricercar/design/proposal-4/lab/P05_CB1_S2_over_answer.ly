% P05 combination CB1: S2 (theme bars 5-8, soprano) over the real answer (alto), simultaneous; free bass
% both halves of the tune at once: S2 lives on the dominant, the answer lives in the dominant key
\version "2.24.0"
soprano = \absolute {
  c''4. a'8 f'4 des''8 bes'8 |   % 1
  c''2. f''8 bes'8 |   % 2
  ees''4. des''8 des''4. c''8 |   % 3
  c''1 |   % 4
  r1 |   % 5
}
alto = \absolute {
  f'2. f'8 e'8 |   % 1
  f'2. f'8 e'8 |   % 2
  f'4. g'8 g'4. bes'8 |   % 3
  bes'2. aes'8 f'8 |   % 4
  g'2 r2 |   % 5
}
tenor = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
}
bass = \absolute {
  f,2. bes,4 |   % 1
  a,2. g,4 |   % 2
  f,2 e,2 |   % 3
  f,1 |   % 4
  c,2 r2 |   % 5
}
\score {
  <<
    \new Staff \with { instrumentName = "S" } { \clef "treble" \key bes \minor \soprano }
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "B" } { \clef "bass" \key bes \minor \bass }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
