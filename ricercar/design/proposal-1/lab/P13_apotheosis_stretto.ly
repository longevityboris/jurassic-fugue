\version "2.24.0"
%% proposal-1 lab: P13 theme (B-flat major) + S1 at the lower fifth
\header { title = "P13 theme (B-flat major) + S1 at the lower fifth" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'2. bes'8 a'8 |
  bes'2. bes'8 a'8 |
  bes'4. c''8 c''4. ees''8 |
  ees''2. d''8 bes'8 |
  c''4. a'8 f'4 d''8 bes'8 |
  c''2. f''8 bes'8 |
  ees''4. d''8 d''4. c''8 |
  c''1 |
  c''2 r2 |
}

alto = \absolute {
  r1 |
  r1 |
  ees'2. ees'8 d'8 |
  ees'2. ees'8 d'8 |
  ees'4. f'8 f'4. aes'8 |
  aes'2. g'8 ees'8 |
  f'2 r2 |
  r1 |
  r1 |
}

tenor = \absolute {
  R1 | R1 | R1 | R1 | R1 | R1 | R1 | R1 | R1 |
}

bass = \absolute {
  R1 | R1 | R1 | R1 | R1 | R1 | R1 | R1 | R1 |
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
