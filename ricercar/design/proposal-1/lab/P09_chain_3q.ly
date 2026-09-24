\version "2.24.0"
%% proposal-1 lab: P09 chain of four at 3 quarters (stretto maestrale, reserve)
\header { title = "P09 chain of four at 3 quarters (stretto maestrale, reserve)" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'2. bes'8 a'8 |
  bes'2. bes'8 a'8 |
  bes'4. c''8 c''4. ees''8 |
  ees''2. des''8 bes'8 |
  c''2 r2 |
  r1 |
  r1 |
}

alto = \absolute {
  r2. ees'4~ |
  ees'2 ees'8 d'8 ees'4~ |
  ees'2 ees'8 d'8 ees'4~ |
  ees'8 f'8 f'4. aes'8 aes'4~ |
  aes'2 ges'8 ees'8 f'4~ |
  f'4 r2. |
  r1 |
}

tenor = \absolute {
  r1 |
  r2 aes2~ |
  aes4 aes8 g8 aes2~ |
  aes4 aes8 g8 aes4. bes8 |
  bes4. des'8 des'2~ |
  des'4 ces'8 aes8 bes2 |
  r1 |
}

bass = \absolute {
  r1 |
  r1 |
  r4 des2. |
  des8 c8 des2. |
  des8 c8 des4. ees8 ees4~ |
  ees8 ges8 ges2. |
  fes8 des8 ees2 r4 |
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
