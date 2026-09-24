% P04 stretto chain at the lower fifth, 2 bars apart: S1 Bb minor (S), Eb minor (A), Ab minor (T)
% pairwise: S/A = lower 5th +8 beats; A/T = same; S/T = only the elision chord at bar 5
\version "2.24.0"
soprano = \absolute {
  bes'2. bes'8 a'8 |   % 1
  bes'2. bes'8 a'8 |   % 2
  bes'4. c''8 c''4. ees''8 |   % 3
  ees''2. des''8 bes'8 |   % 4
  c''2 r2 |   % 5
  r1 |   % 6
  r1 |   % 7
  r1 |   % 8
  r1 |   % 9
  r1 |   % 10
}
alto = \absolute {
  r1 |   % 1
  r1 |   % 2
  ees'2. ees'8 d'8 |   % 3
  ees'2. ees'8 d'8 |   % 4
  ees'4. f'8 f'4. aes'8 |   % 5
  aes'2. ges'8 ees'8 |   % 6
  f'2 r2 |   % 7
  r1 |   % 8
  r1 |   % 9
  r1 |   % 10
}
tenor = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  aes2. aes8 g8 |   % 5
  aes2. aes8 g8 |   % 6
  aes4. bes8 bes4. des'8 |   % 7
  des'2. ces'8 aes8 |   % 8
  bes2 r2 |   % 9
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
