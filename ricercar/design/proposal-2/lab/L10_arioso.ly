\version "2.24.0"
% L10 ARIOSO DOLENTE (Adagio, quarter = 52), lab bar 1 = bar 29 (the A dim7 fermata that ends Part I),
% 2-6 = bars 30-34, 7 = bar 35 (Part III begins: the inversion alone in the bass).
% Soprano: S2 (theme bars 5-8) as a lament over pulsing eighths: V | i6/4 | ii-half-dim6/5 | V6/iv | iv6 - V7 with
% the b6 appoggiatura D-flat-C | V7. Bar 34: the V7 of B-flat is re-read as the GERMAN SIXTH of A minor (E-flat = D#):
% F->E, A->G#, D#->E, and the soprano's C is held as a b6 suspension over E (C-B, the Phrygian sigh) -> E major,
% the dominant of A minor. The whole piece's tonal neighbour (B-flat -> A) happens through this one chord.
soprano = \absolute {
  c''1 | c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1 | c''2 b'2 | r1 |
}
alto = \absolute {
  a'1 | c'8 c'8 c'8 c'8 c'8 c'8 des'8 des'8 | ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 f'8 f'8 | ges'8 ges'8 ges'8 ges'8 ees'8 ees'8 ees'8 ees'8 | ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 | e'8 e'8 e'8 e'8 e'8 e'8 e'8 e'8 | r2. a'4 |
}
tenor = \absolute {
  ges1 | f8 f8 f8 f8 a8 a8 bes8 bes8 | ges8 ges8 ges8 ges8 ges8 ges8 f8 f8 | bes8 bes8 bes8 bes8 a8 a8 a8 a8 | a8 a8 a8 a8 a8 a8 a8 a8 | gis8 gis8 gis8 gis8 gis8 gis8 gis8 gis8 | r1 |
}
bass = \absolute {
  ees,1 | f,1 | ees,2. d,4 | ges,2 f,2 | f,1 | e,1 | e2. e8 f8 |
}
