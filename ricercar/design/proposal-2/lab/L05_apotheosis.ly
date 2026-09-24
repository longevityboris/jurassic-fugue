\version "2.24.0"
% L05 APOTHEOSIS + CODA, lab bar 1 = bar 50 (subito pp IV - iv6, joins L04), 2-9 = bars 51-58, 10-13 = bars 59-62.
% Soprano: the complete theme in B-flat MAJOR (bars 51-58; bar 58 closes on B-flat instead of the open C).
% Tenor 51-55: the INVERSION as a mirror against the tune (S1 in major above, its tonal mirror below, starting
% together): the mirror keeps G-flat (b6) as its neighbour, so each neighbour moment becomes V7b9 / vii7 over the
% major tonic (the minor remembered inside the major). Bass: I-V7b9 | vi7-vii7/Eb | I6-V6/5 | V7-I | V7-I6 |
% ii6/5-V4/2 of IV | IV6-I6/4-V7 | I. Coda 58-62: alto sings the inversion (major body, G-flat neighbours) over a
% tonic pedal; soprano sings the subject's contour in augmentation (B-flat, A, B-flat, C ... ) and ends on D, the
% major third that replaced the minor D-flat; final plagal IV(add6)/I6-4 - I.
soprano = \absolute {
  bes''1 | bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 | c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | bes'1 | bes'2. a'4 | bes'2 c''2 | c''2. bes'4 | c''2 d''2 |
}
alto = \absolute {
  ees'2. ees'4 | d'2. ees'4 | d'2. c'4 | d'2 c'2 | c'2. bes4 | a2 bes2 | ees'2. d'4 | bes'4. bes'8 bes'4. a'8 | f'2. f'8 ges'8 | f'2. f'8 ges'8 | f'4. ees'8 ees'4. c'8 | c'2. d'8 f'8 | ees'4. g'8 bes'4 r4 |
}
tenor = \absolute {
  g2. ges4 | f2. f8 ges8 | f2. f8 ges8 | f4. ees8 ees4. c8 | c2. d8 f8 | ees4. ges8 bes4 bes4 | g2. f4 | bes4. bes8 bes4. c'8 | d'1 | d'2. c'4 | bes4. g8 ~ g4. a8 | a2. bes4 | g2 f2 |
}
bass = \absolute {
  ees,2. ges,4 | bes,2. f,4 | g,2. ees4 | d2 a,2 | f,2. bes,4 | f,4. a,8 d2 | ees2. aes,4 | g,4. f,8 ~ f,2 | bes,1 | bes,1 | bes,4. ees8 ~ ees4. f8 | f2. bes,4 | bes,1 |
}
