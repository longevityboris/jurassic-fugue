% L01 - Exposition of Subject I, bars 1-18 (B-flat minor), top-down entries S, A, T, B.
% Claims: S1 alone; real answer + CS1 (lament) in 2 voices; codetta; S1 in tenor (lowest) +
% CS1 (tonic form) + free soprano; answer in bass + CS1 (tenor) + free alto/soprano.
\version "2.24.0"
soprano = \absolute {
  % E1 bars 1-4: Subject I (S1)
  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' |
  % E2 bars 5-8: S1 end (c'') then CS1 over the alto's answer
  c''2 aes''4 g''4 | f''4 ees''4 des''4 c''8 des''8 ~ | des''4 f''4 ees''4 d''4 | des''2 c''2 |
  % 9 codetta (C -> F7 -> b-flat), lament continues e'' ees'' -> des''
  e''2 ees''2 |
  % E3 bars 10-13: free descant over tenor S1
  des''2 f''2 | f''2 ees''4 des''8 c''8 | des''4. c''8 ees''2 ~ | ees''2 c''4 des''4 |
  % E4 bars 14-17: CS1 at its E2 pitch over the bass answer (outer voices = the verified E2 duet)
  c''2 aes''4 g''4 | f''4 ees''4 des''4 c''8 des''8 ~ | des''4 f''4 ees''4 d''4 | des''2 c''2 |
  % 18
  e''2 r2 |
}
alto = \absolute {
  R1*4 |
  % E2 bars 5-8: real answer (F minor)
  f'2. f'8 e' | f'2. f'8 e' | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f' |
  % 9 answer end + codetta
  g'2 a'2 |
  % E3 bars 10-13: CS1 tonic form (first note replaced by b-flat': leading tone resolves)
  bes'4 f'4 des''4 c''4 | bes'4 aes'4 ges'4 f'8 ges'8 ~ | ges'4 bes'4 aes'4 g'4 | ges'2 f'2 |
  % E4 bars 14-17: free inner voice
  a'2 aes'4 aes'8 g'8 | aes'2 aes'4 aes'8 g'8 | aes'4 aes'8 bes'8 c''4 bes'4 | bes'2 g'4 aes'4 |
  % 18
  c''2 r2 |
}
tenor = \absolute {
  R1*9 |
  % E3 bars 10-13: Subject I in the tenor (lowest voice)
  bes2. bes8 a | bes2. bes8 a | bes4. c'8 c'4. ees'8 | ees'2. des'8 bes |
  % E4 bars 14-17: S1 end (c') then free inner voice
  c'2 c'4 c'4 | c'2 bes4 c'8 bes8 | des'4 c'8 des'8 c'4 d'4 | f'2 e'4 f'4 |
  % 18
  e'2 r2 |
}
bass = \absolute {
  R1*13 |
  % E4 bars 14-17: real answer in the bass (F2)
  f,2. f,8 e, | f,2. f,8 e, | f,4. g,8 g,4. bes,8 | bes,2. aes,8 f, |
  % 18
  g,2 r2 |
}
\score {
  <<
    \new Staff { \clef treble \key bes \minor \soprano }
    \new Staff { \clef treble \key bes \minor \alto }
    \new Staff { \clef "treble_8" \key bes \minor \tenor }
    \new Staff { \clef bass \key bes \minor \bass }
  >>
  \layout { }
  \midi { \tempo 4 = 88 }
}
