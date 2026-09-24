% Proposal 3, lab 01: the whole exposition, bars 1-18 (4 voices), B-flat minor.
% E1 1-4 bass S1 | E2 5-8 tenor ANS, bass CS1-F | 9 codetta | E3 10-13 alto S1, tenor CS1, bass CS2
% E4 14-17 soprano ANS, alto CS1-F, tenor CS2-F, bass free | 18 arrival in F minor.
soprano = \absolute {
  R1 | R1 | R1 | R1 |
  R1 | R1 | R1 | R1 |
  R1 |
  R1 | R1 | R1 | R1 |
  % E4: answer
  f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 g'' |
  f''1 |
}
alto = \absolute {
  R1 | R1 | R1 | R1 |
  R1 | R1 | R1 | R1 |
  R1 |
  % E3: subject
  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 c'' |
  % E4: CS1-F (first half-bar = the subject's last note)
  bes'2 d''2 | des''2 c''2 | b'2 c''2 | des''2 c''2 |
  c''1 |
}
tenor = \absolute {
  R1 | R1 | R1 | R1 |
  % E2: answer
  f'2. f'8 e' | f'2. f'8 e' | f'4. g'8 g'4. bes'8 | bes'2. aes'8 g' |
  % codetta
  f'4 ees'4 des'4 c'4 |
  % E3: CS1 (first half-bar held from the codetta)
  f'2 g'2 | ges'2 f'2 | e'2 f'2 | ges'2 f'2 |
  % E4: CS2-F
  f'4 d'2 c'4~ | c'4 bes2 aes4~ | aes4 g2 f4~ | f4 e2 g4 |
  aes1 |
}
bass = \absolute {
  % E1: subject
  bes,2. bes,8 a, | bes,2. bes,8 a, | bes,4. c8 c4. ees8 | ees2. des8 c |
  % E2: subject's last note, then CS1-F
  bes,2 d2 | des2 c2 | b,2 c2 | des2 c2 |
  % codetta: F minor -> V6 -> i
  f4 c4 bes,4 a,4 |
  % E3: CS2 in the bass (cascade: 4/2 -> 6 chain)
  bes,4 g2 f4~ | f4 ees2 des4~ | des4 c2 bes,4~ | bes,4 a,2 f,4 |
  % E4: free bass
  bes,1 | des2 f2 | d2 c2 | bes,2 c2 |
  f,1 |
}
