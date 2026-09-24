\version "2.24.0"
%% proposal-1 lab: M mirror counter-exposition, bars 19-27
\header { title = "M mirror counter-exposition, bars 19-27" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  r4 c''4 d''4 ees''8 f''8 |
  g''4 f''4 ees''4 d''4 |
  ees''4 f''4 d''4. ees''8 |
  f''2 g''4. a''8 |
  aes''2 g''2~ |
  g''2 f''4. e''8 |
  f''2 e''2 |
  f''4 g''4 bes''4 aes''4 |
  f''2 ges''2 |
}

alto = \absolute {
  ees'2 d'2 |
  ees'2. c'4~ |
  c'2 b4. d'8 |
  f'2. ees'4 |
  c''2. c''8 des''8 |
  c''2. c''8 des''8 |
  c''4. bes'8 bes'4. g'8 |
  g'2. aes'8 c''8 |
  bes'2. bes'8 a'8 |
}

tenor = \absolute {
  c'2 b2 |
  bes4. a8 g4. f8 |
  g2. aes8 a8~ |
  a4 bes4 b4 c'4 |
  f'2 e'2 |
  ees'4. d'8 c'4. bes8 |
  c'2. des'8 d'8~ |
  d'4 ees'4 e'4 f'4 |
  r1 |
}

bass = \absolute {
  g2. g8 aes8 |
  g2. g8 aes8 |
  g4. f8 f4. d8 |
  d2. ees8 g8 |
  f4 f,4 g,4 aes,8 bes,8 |
  c4 bes,4 aes,4 g,4 |
  aes,4 bes,4 g,4. aes,8 |
  bes,2 c4. d8 |
  des2 r2 |
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
