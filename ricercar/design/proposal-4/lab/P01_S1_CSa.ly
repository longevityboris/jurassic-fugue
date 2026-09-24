% P01 S1 (alto) + CSa lament (tenor), subject context
% claim: CSa (chromatic descent ees'->f) is clean under S1; answer context = exact transposition
\version "2.24.0"
soprano = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
}
alto = \absolute {
  bes'2. bes'8 a'8 |   % 1
  bes'2. bes'8 a'8 |   % 2
  bes'4. c''8 c''4. ees''8 |   % 3
  ees''2. des''8 bes'8 |   % 4
  c''2 r2 |   % 5
}
tenor = \absolute {
  ees'2 d'2 |   % 1
  des'2 c'4. ces'8 |   % 2
  bes2 a2 |   % 3
  aes2 g4. ges8 |   % 4
  f2 r2 |   % 5
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
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "T" } { \clef "treble_8" \key bes \minor \tenor }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
