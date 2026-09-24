\version "2.24.0"
% L02 EXPOSITION v2, bars 1-17 (B-flat minor -> F minor). Entries every 4 bars, no codetta:
% b1 bass S1 (bb) | b5 tenor ANS (f) + bass CS1 lament | b9 alto S1 (bb, head over C7) + tenor CS1 + bass CS2 motor |
% b13 soprano ANS (f) + alto CS1 + tenor CS2 + bass free (tonic pedal, N6, cadential 6/4). Ends 17:3 on V of F minor.
soprano = \absolute {
  R1*12 |
  f''2. f''8 e''8 | f''2. f''8 e''8 | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f''8 | g''4. e''8 c''4 r4 |
}
alto = \absolute {
  R1*8 |
  bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 | c''4. a'8 f'4 c'4 |
  aes'2. g'4 | f'4 e'4 ees'2 | des'2. c'4 | e'4. g'8 c'4 r4 |
}
tenor = \absolute {
  R1*4 |
  f'2. f'8 e'8 | f'2. f'8 e'8 | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f'8 | g'4. e'8 c'4 f4 |
  des'2. c'4 | bes4 a4 aes2 | ges2. f4 | a4. c'8 f4 r4 |
  f8 e8 f8 g8 aes8 g8 bes8 des8 | aes4 g8 c'8 ~ c'2 | bes8 c'8 bes8 aes8 ges4 aes4 | c2. r4 |
}
bass = \absolute {
  bes,2. bes,8 a,8 | bes,2. bes,8 a,8 | bes,4. c8 c4. ees8 | ees2. des8 bes,8 | c4. a,8 f,4 c4 |
  aes2. g4 | f4 e4 ees2 | des2. c4 | e4. g8 c4 r4 |
  bes,8 a,8 bes,8 c8 des8 c8 ees8 ges,8 | des4 c8 f8 ~ f2 | ees8 f8 ees8 des8 ces4 des4 | f,2. r4 |
  f,2. g,4 | aes,4. e,8 c,2 | des,2 bes,4 c4 | c,2. r4 |
}
