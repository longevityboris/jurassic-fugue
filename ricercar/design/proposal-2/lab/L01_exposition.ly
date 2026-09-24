\version "2.24.0"
% L01 EXPOSITION, bars 1-18 (B-flat minor -> F minor). Order B, T, A, S (ascending).
% Entry 1 b.1 bass S1 | entry 2 b.5 tenor ANS (F minor) over CS1 in bass |
% codetta b.9 beat 4 (V7 of B-flat) | entry 3 b.10 alto S1 + tenor CS1 + bass CS-L (lament) |
% entry 4 b.14 soprano ANS + alto CS1 + bass CS-L (F minor) + free tenor.
soprano = \absolute {
  R1*13 |
  % 14-18 ANS (F minor)
  f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f'' | g''4. e''8 c''4 r4 |
}
alto = \absolute {
  R1*9 |
  % 10-14 S1 (B-flat minor)
  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' |
  % 14 S1 tail, then CS1 (F minor) under the soprano answer
  c''4. a'8 f'4 aes'8 bes'8 |
  des''8 c''8 bes'4 aes'4. g'8 | aes'4. c''8 bes'2 ~ | bes'4 g'2 f'8 d'8 | e'4. c'8 ~ c'4 r4 |
}
tenor = \absolute {
  R1*4 |
  % 5-9 ANS (F minor), bar 9 beat 4 = codetta (7th of V7/B-flat)
  f2. f8 e | f2. f8 e | f4. g8 g4. bes8 | bes2. aes8 f | g4. e8 c4 ees4 |
  % 10-14 CS1 (B-flat minor) under alto S1
  des4 r2 des'8 ees'8 | ges'8 f'8 ees'4 des'4. c'8 | des'4. f'8 ees'2 ~ | ees'4 c'2 bes8 g8 |
  % 14 CS1 end, then free voice
  a4. f8 ~ f4 c'4 | des'2 c'2 | c'4 aes8 g8 g4 f4 | f2 g4 d4 | g2. r4 |
}
bass = \absolute {
  % 1-5 S1 (B-flat minor)
  bes,2. bes,8 a, | bes,2. bes,8 a, | bes,4. c8 c4. ees8 | ees2. des8 bes, |
  % 5 tail, then CS1 (F minor, 2-voice form) under tenor answer
  c4. a,8 f,4 aes,8 bes,8 | des8 c8 bes,4 aes,4. g,8 | aes,4. c8 bes,2 ~ | bes,4 g,2 f,8 ees,8 |
  e,4. c,8 ~ c,4 f,4 |
  % 10-14 CS-L lament (B-flat minor)
  bes,2 aes,4 ges,4 | ees,2 f,2 | bes,4. a,8 aes,4 g,4 | ges,2 f,4 e,4 |
  % 14 lament ends on F; 15-18 CS-L (F minor)
  f,1 | bes,2 c2 | f4. e8 ees4 d4 | des2 c4 b,4 | c2. r4 |
}
