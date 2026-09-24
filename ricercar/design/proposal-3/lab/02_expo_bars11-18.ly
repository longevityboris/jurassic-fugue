% Proposal 3, lab 02: exposition bars 11-18 (3 then 4 voices), continuing lab 01.
% Bar 11: alto S1 (B-flat minor) over tenor CS1 (lament from 4^) and a free bass; opens on iv.
% Bar 15: soprano answer (F minor), alto CS1 (F frame), tenor CS2 (running eighths), free bass.
soprano = \absolute {
  R1*4 |
  f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 g'' |
}
alto = \absolute {
  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 c'' |
  bes'2 a' | aes' g' | f' ees' | des' c' |
}
tenor = \absolute {
  ees'2 d' | des' c' | bes aes | ges f |
  % CS2 (motor), F frame
  r8 f bes des' c' a f g | aes c' f' c' bes g c' bes |
  aes des' f' des' bes g ees aes | f bes aes bes g e f e |
}
bass = \absolute {
  ees,4 ges, bes,2 | ees4 ges, ees2 | des2 f4 f, | ees, c a,2 |
  bes,2 f, | f, c | des c | bes, c |
}
