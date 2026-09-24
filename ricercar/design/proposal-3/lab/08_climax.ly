% Proposal 3, lab 08: Part V, dominant pedal and climax (piece bars 43-51 = lab bars 1-9).
% bass: the answer in augmentation (AUG, last beat tweaked aes-g -> aes-ges) = the dominant pedal.
% bars 1-4: rectus/inversus wedge over the pedal: alto S1 on bes', soprano its mirror on bes'' (leading
%   tone a' against Neapolitan ces''' at every beat 4.5), tenor CS2 (cascade).
% bars 4-8: the alto runs straight on into S2 with the theme's ORIGINAL bar-4 pickup (des''8 bes') -> the
%   whole theme, in minor, under a soprano descant; bar 8 beat 4: French sixth (ges, bes c'' e'')
%   under S2's held c''; bar 9: V (F major).
soprano = \absolute {
  bes''2. bes''8 ces''' | bes''2. bes''8 ces''' | bes''4. aes''8 aes''4. f''8 | f''2. ges''8 aes'' |
  a''2. bes''4~ | bes''2. aes''4 | ges''2 f''2 | g''2 aes''4 c'''4 |
  c'''2 a''4 c''4 |
}
alto = \absolute {
  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' |
  c''4. a'8 f'4 des''8 bes' | c''2. f''8 bes' | ees''4. des''8 des''4. c''8 | c''1 |
  c''2 f'2 |
}
tenor = \absolute {
  r4 g'2 f'4~ | f'4 ees'2 des'4~ | des'4 c'2 bes4~ | bes4 a2 c'4 |
  c'2. e'4~ | e'2. f'4 | ges'2 aes'2 | g'2 f'4 e'4 |
  f'1 |
}
bass = \absolute {
  f,1~ | f,2 f,4 e,4 | f,1~ | f,2 f,4 e,4 |
  f,2. g,4 | g,2. bes,4 | bes,1~ | bes,2 aes,4 ges,4 |
  f,1 |
}
