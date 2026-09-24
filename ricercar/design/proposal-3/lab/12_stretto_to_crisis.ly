% Proposal 3, lab 12: entry E7 (S2 stretto over the answer), Episode 2 and the crisis chord
% (piece bars 28-34 = lab bars 1-7), 4 voices.
% tenor ANS on f (28.1); alto S2 on c'' (28.3); soprano S2-F on g'' (29.3), its final g'' held as a
% top pedal 32.3-33.3. The bass is TACET for the stretto (28-31: three voices, the proven core of lab 06)
% and re-enters on f, at 32.1 with the chromatic rise f, g, aes, | a, bes, b, | c (it starts the climb
% on g, so that it never sounds ges under the held g'').
% Episode 2 chords (quarter-note harmonic rhythm): Eb/G, Abmaj7, A half-dim7, bbm6, B dim7 -> 34.1
% C dim7 (= vii7 of b-flat over c) with every voice moving by semitone, ff -> 34.3 C-flat major, p.
soprano = \absolute {
  R1 | r2 g''4. e''8 | c''4 aes''8 f'' g''2~ | g''4 c'''8 f'' bes''4. aes''8 | aes''4. g''8 g''2~ |
  g''2 aes''2 | a''2 ces'''2 |
}
alto = \absolute {
  r2 c''4. a'8 | f'4 des''8 bes' c''2~ | c''4 f''8 bes' ees''4. des''8 | des''4. c''8 c''2~ | c''2 ees''2~ |
  ees''4 des''4 d''2 | ees''2 ees''2 |
}
tenor = \absolute {
  f2. f8 e | f2. f8 e | f4. g8 g4. bes8 | bes2. aes8 g | f2 bes4 c'4 |
  c'4 des'4 f'2 | ges'2 ges'2 |
}
bass = \absolute {
  R1 | R1 | R1 | R1 | f,2 g,4 aes,4 |
  a,4 bes,4 b,2 | c2 ces2 |
}
