% Proposal 3, lab 09: Part VI apotheosis + coda (piece bars 52-62 = lab bars 1-11), B-flat MAJOR.
% soprano: the whole theme, UNTWEAKED (bar 4 ends d''8 bes' and runs into bar 5 as Williams wrote it).
% bars 1-4: alto CS2 in major (cascade g'..a, cut at 4.2 to leap into the answer), tenor free,
%   bass tonic pedal -> IV -> V7 -> I6; Williams's own IV6/4-over-tonic in bar 2.
% bars 4.3-8: the proven combination in major: alto ANS-M (f' ...) from 4.3, bass CS2-M in the answer
%   frame (syncopated descending cascade d c bes a g f e g a) from 4.4, soprano S2-M from 5.1; tenor free.
% bars 9-11 coda: V7 - I; tonic pedal; I - iv6/4 (minor: g-flat, the lament's b6) - dim7 over the pedal
%   (the subject's own leading tone a') - I.
soprano = \absolute {
  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes' |
  c''4. a'8 f'4 d''8 bes' | c''2. f''8 bes' | ees''4. d''8 d''4. c''8 | c''1 |
  c''2 d''2 | bes'2. bes'8 a' | bes'1 |
}
alto = \absolute {
  d'4 g'2 f'4~ | f'4 ees'2 d'4~ | d'4 c'2 bes4~ | bes4 a4 f'2~ |
  f'4 f'8 e' f'2~ | f'4 f'8 e' f'4. g'8 | g'4. bes'8 bes'2~ | bes'4 a'8 g' f'2 |
  ees'2 d'2 | d'2 ees'2 | d'1 |
}
tenor = \absolute {
  f1 | g2. f4 | f1 | g4 f4 a4 bes4 |
  a2. bes4 | f2. g4 | bes2 d'4 c'4~ | c'1 |
  a2 bes2 | f2 ges2 | f1 |
}
bass = \absolute {
  bes,1 | bes,1 | bes,2 f2 | ees2 f4 d4~ |
  d4 c2 bes,4~ | bes,4 a,2 g,4~ | g,4 f,2 e,4~ | e,4 g,4 a,2 |
  f,2 bes,2 | bes,1 | bes,1 |
}
