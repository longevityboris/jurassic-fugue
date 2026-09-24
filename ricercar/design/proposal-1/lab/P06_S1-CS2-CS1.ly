\version "2.24.0"
%% proposal-1 lab: P06 triple counterpoint: S1 / CS2 / CS1
\header { title = "P06 triple counterpoint: S1 / CS2 / CS1" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'2. bes'8 a'8 |
  bes'2. bes'8 a'8 |
  bes'4. c''8 c''4. ees''8 |
  ees''2. des''8 bes'8 |
  c''2 r2 |
}

alto = \absolute {
  r4 f'4 ees'4 des'8 c'8 |
  bes4 c'4 des'4 ees'4 |
  des'4 c'4 ees'4. des'8 |
  c'2 bes4. aes8 |
  g2 r2 |
}

tenor = \absolute {
  f2 ges2 |
  g4. aes8 bes4. c'8 |
  bes2. aes4~ |
  aes4 g4 ges4 f4 |
  e2 r2 |
}

bass = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "S" } << \global \soprano >>
    \new Staff \with { instrumentName = "A" } << \global \alto >>
    \new Staff \with { instrumentName = "T" } << \global \clef "treble_8" \tenor >>
    \new Staff \with { instrumentName = "B" } << \global \clef bass \bass >>
  >>
  \layout { }
  \midi { \tempo 2 = 46 }
}
