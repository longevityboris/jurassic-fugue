% Proposal 3, lab 01: exposition bars 1-10 (2 voices).
% Claim: S1 alone (bass), real answer in F minor (tenor) against CS1 (lament) in the bass,
% then a 2-bar codetta returning to B-flat minor (ends on B-flat/F = V/iv, so bar 11 opens on iv).
soprano = \absolute {
  R1*10 |
}
alto = \absolute {
  R1*10 |
}
tenor = \absolute {
  R1*4 |
  % 5-8 answer (F minor, real)
  f2. f8 e | f2. f8 e | f4. g8 g4. bes8 | bes2. aes8 g |
  % 9-10 codetta
  f4 aes4 des'2 ~ | des'4 c'8 bes c'4 d'4 |
}
bass = \absolute {
  % 1-4 subject I (B-flat minor)
  bes,2. bes,8 a, | bes,2. bes,8 a, | bes,4. c8 c4. ees8 | ees2. des8 c |
  % 5-8 CS1 = lament, F-minor frame: 4^ down the chromatic tetrachord, then the Phrygian tetrachord
  bes,2 a, | aes, g, | f, ees, | des, c, |
  % 9-10 codetta
  f,2 bes, | ges, f, |
}
