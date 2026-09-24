% Proposal 3, lab 10: crisis and mirror section (piece bars 34-43.1 = lab bars 1-10).
% bar 1 (34): vii7 of B-flat minor over c (c ees ges a), ff -> Neapolitan C-flat major in root position,
%   subito p, fermata. Bass c -> ces (the lament's semitone), soprano a'' -> ces''' (peak of the first
%   wave); alto ees'' and tenor ges' are common tones. The mirror subject then starts on bes, a semitone
%   under the Neapolitan root, and keeps ces as its neighbour.
% bars 2-5 (35-38), E-flat minor, pp, three voices: tenor S1I-sub (bes ces' bes: the Neapolitan as a
%   neighbour), alto CS2I-sub (rising cascade), bass CS1I-sub (rising chromatic des, d, ees, fes,).
% bars 6-9 (39-42), B-flat minor: soprano S1I (f'' ges'' f''), alto CS1I, tenor CS2I, free bass
%   tonic pedal bes, (2 bars) | des, ees, | f, ges, -> F (bar 10 = 43.1, start of the augmentation).
soprano = \absolute {
  a''2 ces'''2 |
  R1 | R1 | R1 | R1 |
  f''2. f''8 ges'' | f''2. f''8 ges'' | f''4. ees''8 ees''4. c''8 | c''2. des''8 ees'' |
  bes''1 |
}
alto = \absolute {
  ees''2 ees''2 |
  r4 des'2 ees'2 f'2 ges'4~ | ges'4 aes'2 bes'4~ | bes'4 ces''2 aes'4~ |
  aes'1 | a'2 bes'2 | ces''2 bes'2 | a'2 bes'2 |
  bes'1 |
}
tenor = \absolute {
  ges'2 ges'2 |
  bes2. bes8 ces' | bes2. bes8 ces' | bes4. aes8 aes4. f8 | f2. ges8 aes |
  bes4 aes2 bes4~ | bes4 c'2 des'4~ | des'4 ees'2 f'4~ | f'4 ges'2 ees'4 |
  f'1 |
}
bass = \absolute {
  c2 ces2 |
  r2 des,2 | d,2 ees,2 | fes,2 ees,2 | d,2 ees,2 |
  bes,1~ | bes,1 | des,2 ees,2 | f,2 ges,2 |
  f,1 |
}
