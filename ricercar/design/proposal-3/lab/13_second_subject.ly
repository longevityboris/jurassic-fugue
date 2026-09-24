% Proposal 3, lab 13: entries E5 and E6 (piece bars 20-27 = lab bars 1-8, plus 28.1).
% E5 (20-23), three voices (soprano tacet): alto S2 from 20.3, tenor ANS on f' from 20.1, bass CS2-F
%   from 20.2 (cadence changed to f, e, f,); S2's last c'' resolves 9-8 onto bes' at 24.2.
% E6 (24-27): soprano S2-sub from 24.3 (its first entry after four bars' rest), bass S1 from 24.1, tenor
%   CS2 from 24.2; alto tacet 24.3-25, then free in 26-27 (bbm, Cm, Ab/C, e-flat, dim7, F7/E-flat, RET
%   c''-des'' into 28.1).
soprano = \absolute {
  R1 | R1 | R1 | R1 |
  r2 f''4. d''8 | bes'4 ges''8 ees'' f''2~ | f''4 bes''8 ees'' aes''4. ges''8 | ges''4. f''8 f''2~ |
  f''2 r2 |
}
alto = \absolute {
  r2 c''4. a'8 | f'4 des''8 bes' c''2~ | c''4 f''8 bes' ees''4. des''8 | des''4. c''8 c''2~ |
  c''4 bes'4 r2 | R1 | f'4 g'4 ees'2 | ees'4 c''2 c''4 |
  des''2 r2 |
}
tenor = \absolute {
  f'2. f'8 e' | f'2. f'8 e' | f'4. g'8 g'4. bes'8 | bes'2. aes'8 g' |
  f'4 g'2 f'4~ | f'4 ees'2 des'4~ | des'4 c'2 bes4~ | bes4 a2 c'4 |
  f2 r2 |
}
bass = \absolute {
  f4 d2 c4~ | c4 bes,2 aes,4~ | aes,4 g,2 f,4~ | f,4 e,2 f,4 |
  bes,2. bes,8 a, | bes,2. bes,8 a, | bes,4. c8 c4. ees8 | ees2. des8 c |
  bes,2 r2 |
}
