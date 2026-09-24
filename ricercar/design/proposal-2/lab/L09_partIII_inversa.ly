\version "2.24.0"
% L09 PART III "Fuga inversa" (A minor), lab bar 1 = bar 34 (arioso's last bar: E major), 2-8 = bars 35-41,
% 9 = bar 42 (first bar of Part IV, for the seam).
% 35: the INVERSION alone in the bass, from E (5-b6-5, the Phrygian sigh), pp "poi a poi di nuovo vivente".
% 35:4 alto: CS1 INVERTED = the lament rising (C D E F F# G# A); 36 soprano: CS2 inverted (the motor mirrored).
% Bars 35-39 are the tonal mirror of exposition entry 3 (bars 9-13), transposed to A minor: the proven
% triple counterpoint turned upside down (Bach's rectus/inversus), with local fixes where the tonal mirror
% produced augmented steps.
% 37: tenor INV in E minor, a fifth above the bass, 2 bars later (the inversion's best stretto, mirror of S1's
% fifth-below stretto). 40: B7 (V7 of E) -> 41 C (deceptive, VI of E) -> 41:4 C = V of F -> 42 F pedal.
soprano = \absolute {
  c''2 b'2 | r1 | e''8 f''8 e''8 d''8 c''8 d''8 b'8 g''8 | c''4 d''8 a'8 ~ a'4 b'4 | b'8 a'8 b'8 c''8 d''4 c''4 | f''2 e''4 dis''4 ~ | dis''2. e''4 | e''2 g''2 | r1 |
}
alto = \absolute {
  e'1 | r2. a'4 | c'2. d'4 | e'4 f'4 fis'2 | gis'2. a'4 | f'4. d'8 a'2 | a'2. g'4 | g'2 c''4 e''4 | c''4. a'8 f'4 des''8 bes'8 |
}
tenor = \absolute {
  gis1 | r1 | r1 | b2. b8 c'8 | b2. b8 c'8 | b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4 c'4 | r1 |
}
bass = \absolute {
  e,1 | e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 | d4. f8 a4 fis4 | b,2. e4 | c2. c4 | f,1 |
}
