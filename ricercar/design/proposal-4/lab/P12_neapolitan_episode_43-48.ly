% P12 episode bars 43-48: the chain's D-flat-major entry (tenor) ends; NEAPOLITAN (C-flat, 44) over the fourth statement of the lament (bass des -> f); soprano echoes the subject head (ges''2. ges''8 f''8); vii(o)7, Italian sixth (46) -> dominant pedal (47-48)
% 47-48 = first two bars of Part IV (S2, lament on the tenor's held bes, augmented answer f,)
\version "2.24.0"
soprano = \absolute {
  f''2 ges''2 |   % 1
  ges''2. ges''8 f''8 |   % 2
  ees''2 c''2 |   % 3
  des''2 bes'2 |   % 4
  c''4. a'8 f'4 des''8 bes'8 |   % 5
  c''2. f''8 bes'8 |   % 6
  ees''2 r2 |   % 7
}
alto = \absolute {
  aes'1 |   % 1
  ces''2 des''2 |   % 2
  c''2 aes'2 |   % 3
  f'2 e'2 |   % 4
  f'1 |   % 5
  f'2 ees'4 des'4 |   % 6
  aes2 r2 |   % 7
}
tenor = \absolute {
  des'4. ees'8 ees'4. ges'8 |   % 1
  ges'2. f'8 des'8 |   % 2
  ees'1 |   % 3
  bes1~ |   % 4
  bes2 a2 |   % 5
  aes2 g4. ges8 |   % 6
  f2 r2 |   % 7
}
bass = \absolute {
  des2 c2 |   % 1
  ces2 bes,2 |   % 2
  a,2 aes,2 |   % 3
  g,2 ges,2 |   % 4
  f,1~ |   % 5
  f,2 f,4 e,4 |   % 6
  f,2 r2 |   % 7
}
\score {
  <<
    \new Staff \with { instrumentName = "S" } { \clef "treble" \key bes \minor \soprano }
    \new Staff \with { instrumentName = "A" } { \clef "treble" \key bes \minor \alto }
    \new Staff \with { instrumentName = "T" } { \clef "treble_8" \key bes \minor \tenor }
    \new Staff \with { instrumentName = "B" } { \clef "bass" \key bes \minor \bass }
  >>
  \layout { }
  \midi { \tempo 4 = 80 }
}
