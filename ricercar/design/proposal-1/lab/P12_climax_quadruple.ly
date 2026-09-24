\version "2.24.0"
%% proposal-1 lab: P12 I1 / S2 / S1 over A1 augmented
\header { title = "P12 I1 / S2 / S1 over A1 augmented" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  f''2. f''8 ges''8 |
  f''2. f''8 ges''8 |
  f''4. ees''8 ees''4. c''8 |
  c''2. des''8 f''8 |
  ees''2 r2 |
  r1 |
  r1 |
  r1 |
  r1 |
}

alto = \absolute {
  c''4. a'8 f'4 des''8 bes'8 |
  c''2. f''8 bes'8 |
  ees''4. des''8 des''4. c''8 |
  c''1 |
  c''2 r2 |
  r1 |
  r1 |
  r1 |
  r1 |
}

tenor = \absolute {
  bes2. bes8 a8 |
  bes2. bes8 a8 |
  bes4. c'8 c'4. ees'8 |
  ees'2. des'8 bes8 |
  c'2 r2 |
  r1 |
  r1 |
  r1 |
  r1 |
}

bass = \absolute {
  f,1~ |
  f,2 f,4 e,4 |
  f,1~ |
  f,2 f,4 e,4 |
  f,2. g,4 |
  g,2. bes,4 |
  bes,1~ |
  bes,2 aes,4 f,4 |
  g,1 |
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
