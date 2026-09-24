\version "2.24.0"
%% proposal-1 lab: P11b CS3 two octaves up
\header { title = "P11b CS3 two octaves up" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  c''2 f''2 |
  ges''4 f''4 ees''4 f''4 |
  bes''2 aes''4 ges''4 |
  aes''4 bes''4 c'''4 des'''4 |
  c'''2 r2 |
}

alto = \absolute {
  R1 | R1 | R1 | R1 | R1 |
}

tenor = \absolute {
  ees'4. c'8 aes4 f'8 des'8 |
  ees'2. aes'8 des'8 |
  ges'4. f'8 f'4. ees'8 |
  ees'1 |
  ees'2 r2 |
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
