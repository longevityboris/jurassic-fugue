% P09 Part IV (bars 47-58): answer in 2x AUGMENTATION as the dominant pedal (bass); S2 (47-50) and the answer at the top (51-54, peak bes''); lament over the pedal (tenor 47-50); climax It6 - V (4-3: the subject head bes''-a'') - VI deceptive; general pause
% alto 47-54 left free in the lab (to be composed; must avoid the aug bass e,-f, neighbour octaves)
\version "2.24.0"
soprano = \absolute {
  c''4. a'8 f'4 des''8 bes'8 |   % 1
  c''2. f''8 bes'8 |   % 2
  ees''4. des''8 des''4. c''8 |   % 3
  c''2. r4 |   % 4
  f''2. f''8 e''8 |   % 5
  f''2. f''8 e''8 |   % 6
  f''4. g''8 g''4. bes''8 |   % 7
  bes''2. aes''8 f''8 |   % 8
  bes''1~ |   % 9
  bes''2. bes''8 a''8 |   % 10
  bes''1 |   % 11
  r1 |   % 12
}
alto = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
  r1 |   % 6
  r1 |   % 7
  r1 |   % 8
  bes'1 |   % 9
  c''1 |   % 10
  bes'1 |   % 11
  r1 |   % 12
}
tenor = \absolute {
  bes2 a2 |   % 1
  aes2 g4. ges8 |   % 2
  f2 e2 |   % 3
  ees2 d4. des8 |   % 4
  c2 c'2 |   % 5
  bes2. des'4 |   % 6
  des'2 ees'2 |   % 7
  des'2 c'2 |   % 8
  e'1 |   % 9
  f'1 |   % 10
  des'1 |   % 11
  r1 |   % 12
}
bass = \absolute {
  f,1~ |   % 1
  f,2 f,4 e,4 |   % 2
  f,1~ |   % 3
  f,2 f,4 e,4 |   % 4
  f,2. g,4 |   % 5
  g,2. bes,4 |   % 6
  bes,1~ |   % 7
  bes,2 aes,4 f,4 |   % 8
  ges,1 |   % 9
  f,1 |   % 10
  ges,1 |   % 11
  r1 |   % 12
}
\score {
  <<
    \new Staff \with { instrumentName = "S" } { \clef "treble" \key bes \minor \soprano }
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "T" } { \clef "treble_8" \key bes \minor \tenor }
    \new Staff \with { instrumentName = "B" } { \clef "bass" \key bes \minor \bass }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
