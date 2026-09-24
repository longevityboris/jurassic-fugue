% P08 Part III opening (bars 33-36): S1 on ees' (alto) and its diatonic MIRROR on ees (bass), simultaneously, two voices alone
% the neighbour notes meet as i6-vii(o) / the voices open from the octave into a wedge; (b-flat version: S1 bes' / mirror bes)
\version "2.24.0"
soprano = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
}
alto = \absolute {
  ees'2. ees'8 d'8 |   % 1
  ees'2. ees'8 d'8 |   % 2
  ees'4. f'8 f'4. aes'8 |   % 3
  aes'2. ges'8 ees'8 |   % 4
  f'2 r2 |   % 5
}
tenor = \absolute {
  r1 |   % 1
  r1 |   % 2
  r1 |   % 3
  r1 |   % 4
  r1 |   % 5
}
bass = \absolute {
  ees2. ees8 f8 |   % 1
  ees2. ees8 f8 |   % 2
  ees4. d8 d4. bes,8 |   % 3
  bes,2. ces8 ees8 |   % 4
  d2 r2 |   % 5
}
\score {
  <<
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "B" } { \clef "bass" \key bes \minor \bass }
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
