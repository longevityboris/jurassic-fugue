% P06 apotheosis (B-flat major): the complete tune as cantus firmus (S) over its own mirror (B, bars 1-4) and the answer (B, bars 5-8); free inner voices; c'' rises to d''
% plagal close bar 10 with the minor subdominant (ges) as the last shadow of the minor
\version "2.24.0"
soprano = \absolute {
  bes'2. bes'8 a'8 |   % 1
  bes'2. bes'8 a'8 |   % 2
  bes'4. c''8 c''4. ees''8 |   % 3
  ees''2. d''8 bes'8 |   % 4
  c''4. a'8 f'4 d''8 bes'8 |   % 5
  c''2. f''8 bes'8 |   % 6
  ees''4. d''8 d''4. c''8 |   % 7
  c''1 |   % 8
  d''1~ |   % 9
  d''1 |   % 10
}
alto = \absolute {
  d'4. ees'8 f'4 ees'4 |   % 1
  d'4 f'4 ees'4 f'8 ees'8 |   % 2
  f'4. ees'8 ees'4. f'8 |   % 3
  a'2 g'4 f'4 |   % 4
  f'4. f'8 d'4 f'8 g'8 |   % 5
  a'2. a'8 g'8 |   % 6
  a'4. bes'8 bes'4. g'8 |   % 7
  g'2. f'4 |   % 8
  f'1 |   % 9
  ges'2 f'2 |   % 10
}
tenor = \absolute {
  f2 g4 f4 |   % 1
  bes4 aes4 g4 f4 |   % 2
  f4 d'4 c'4. c'8 |   % 3
  c'2. f4 |   % 4
  c'2 bes4 c'4 |   % 5
  c'2 d'4 c'8 bes8 |   % 6
  c'4. bes8 bes4. ees'8 |   % 7
  ees'2. ees'4 |   % 8
  d'1 |   % 9
  ees'2 d'2 |   % 10
}
bass = \absolute {
  bes,2. bes,8 c8 |   % 1
  bes,2. bes,8 c8 |   % 2
  bes,4. a,8 a,4. f,8 |   % 3
  f,2. d,4 |   % 4
  f,2. f,8 e,8 |   % 5
  f,2. f,8 e,8 |   % 6
  f,4. g,8 g,4. bes,8 |   % 7
  bes,2. a,8 f,8 |   % 8
  bes,1~ |   % 9
  bes,1 |   % 10
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
