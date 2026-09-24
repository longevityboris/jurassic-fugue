% P11 complete 4-voice exposition, bars 1-18 (order S-A-B-T): S1 / answer+CSb / codetta / S1 in bass + CSb in alto + soprano descant / answer in tenor + lament in bass + CSb in soprano + free alto; Phrygian half cadence on C at 18
\version "2.24.0"
soprano = \absolute {
  bes'2. bes'8 a'8 |   % 1
  bes'2. bes'8 a'8 |   % 2
  bes'4. c''8 c''4. ees''8 |   % 3
  ees''2. des''8 bes'8 |   % 4
  c''4 des''8 ees''8 f''8 ees''8 des''8 c''8 |   % 5
  aes''4 g''8 f''8 ees''8 des''8 c''8 bes'8 |   % 6
  a'4 bes'4 c''4 des''4~ |   % 7
  des''4 ees''4 f''2 |   % 8
  e''2 ees''2 |   % 9
  f''1 |   % 10
  f''2. ees''4 |   % 11
  f''2 ees''2~ |   % 12
  ees''2 des''4 c''4 |   % 13
  bes'4 des''8 ees''8 f''8 ees''8 des''8 c''8 |   % 14
  aes''4 g''8 f''8 ees''8 des''8 c''8 bes'8 |   % 15
  a'4 bes'4 c''4 des''4~ |   % 16
  des''4 ees''4 f''2 |   % 17
  e''2 r2 |   % 18
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
  g'2 a'2 |   % 9
  f'4 ges'8 aes'8 bes'8 aes'8 ges'8 f'8 |   % 10
  des''4 c''8 bes'8 aes'8 ges'8 f'8 ees'8 |   % 11
  d'4 ees'4 f'4 ges'4~ |   % 12
  ges'4 aes'4 bes'2 |   % 13
  des'2 c'2 |   % 14
  c'2 des'2~ |   % 15
  des'4 c'4 c'4 bes8 des'8~ |   % 16
  des'4 ges'4 f'2 |   % 17
  c''2 r2 |   % 18
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
  r1 |   % 10
  r1 |   % 11
  r1 |   % 12
  r1 |   % 13
  f2. f8 e8 |   % 14
  f2. f8 e8 |   % 15
  f4. g8 g4. bes8 |   % 16
  bes2. aes8 f8 |   % 17
  g2 r2 |   % 18
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
  bes,2. bes,8 a,8 |   % 10
  bes,2. bes,8 a,8 |   % 11
  bes,4. c8 c4. ees8 |   % 12
  ees2. des8 bes,8~ |   % 13
  bes,2 a,2 |   % 14
  aes,2 g,4. ges,8 |   % 15
  f,2 e,2 |   % 16
  ees,2 d,4. des,8 |   % 17
  c,2 r2 |   % 18
}
\score {
  <<
    \new Staff \with { instrumentName = "S" } { \clef "treble" \key bes \minor \soprano }
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "T" } { \clef "treble_8" \key bes \minor \tenor }
    \new Staff \with { instrumentName = "B" } { \clef "bass" \key bes \minor \bass }
  >>
  \layout { }
  \midi { \tempo 4 = 72 }
}
