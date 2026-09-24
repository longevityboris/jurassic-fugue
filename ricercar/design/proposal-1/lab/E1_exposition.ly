\version "2.24.0"
%% proposal-1 lab: E1 exposition bars 1-19
\header { title = "E1 exposition bars 1-19" tagline = ##f }
global = { \key bes \minor \time 2/2 }

soprano = \absolute {
  bes'2. bes'8 a'8 |
  bes'2. bes'8 a'8 |
  bes'4. c''8 c''4. ees''8 |
  ees''2. des''8 bes'8 |
  c''2 des''2 |
  d''4. ees''8 f''4. g''8 |
  f''2. ees''4~ |
  ees''4 d''4 des''4 c''4 |
  b'2 c''2~ |
  c''4 bes'4 a'2 |
  bes'4 f''4 ees''4 des''8 c''8 |
  bes'4 c''4 des''4 ees''4 |
  des''4 c''4 ees''4. des''8 |
  c''2 bes'4. aes'8~ |
  aes'4 r4 r2 |
  r2 c''2~ |
  c''4 bes'4 ees''2~ |
  ees''2 des''4 f''4 |
  r2 r2 |
}

alto = \absolute {
  r1 |
  r1 |
  r1 |
  r1 |
  f'2. f'8 e'8 |
  f'2. f'8 e'8 |
  f'4. g'8 g'4. bes'8 |
  bes'2. aes'8 f'8 |
  g'2 e'2 |
  f'2 c'2 |
  f'2 ges'2 |
  g'4. aes'8 bes'4. c''8 |
  bes'2. aes'4~ |
  aes'4 g'4 ges'4 f'4 |
  r4 c''4 bes'4 aes'8 g'8 |
  f'4 g'4 aes'4 bes'4 |
  aes'4 g'4 bes'4. aes'8 |
  g'2 f'4. ees'8~ |
  ees'2 r2 |
}

tenor = \absolute {
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  bes2. bes8 a8 |
  bes2. bes8 a8 |
  bes4. c'8 c'4. ees'8 |
  ees'2. des'8 bes8 |
  c'2 des'2 |
  d'4. ees'8 f'4. g'8 |
  f'2. ees'4~ |
  ees'4 d'4 des'4 c'4~ |
  c'2 r2 |
}

bass = \absolute {
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  r1 |
  f2. f8 e8 |
  f2. f8 e8 |
  f4. g8 g4. bes8 |
  bes2. aes8 f8 |
  g2 r2 |
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
