\version "2.24.0"
% L07 PART I, bars 17-29 (lab bar 1 = bar 17, the exposition's last bar; joins L02).
% 17:4-19 EPISODE: cell b (rising 2nd + 3rd, C-Db-Db-F) answered by its mirror (Gb-F-F-Eb, the inversion's bar 3,
% foreshadowed), bass circle of fifths F-Bb-Eb-F: f minor -> bb (i) -> iv -> V7 -> 20 i.
% 20-26 STRETTO: bass S1 (bb) 20; soprano S1 (eb, a 4th above + 2 octaves) 22 = 2 bars later, entering exactly
% where the bass subject's harmony reaches iv. Alto CS1 (lament) and tenor CS2 (motor) as in the exposition
% (the [CS1, CS2, S1-bass] permutation proven in L03_perm_C1-C2-S). Tails in the minor dominant (C-Ab-F, F-Db-Bb):
% the dominants lose their leading tones as the music sinks.
% 26:3-29 LIQUIDATION + CLIMAX: the subject's head (neighbour figure) in four voices at half-bar distances on the
% four notes of the diminished seventh E-G-Bb-Db (bass E 26:3, tenor G 27:1, alto Bb 27:3, soprano Db 28:1);
% each slides a semitone down (E-Eb, G-Gb, Bb-A, Db-C) so E dim7 melts into A dim7 (vii7 of B-flat minor),
% complete at 28:4.5; ff fermata 29, then general pause. Harmonic by-products: 27:3 E-flat MAJOR (a glimpse of
% light), 27:4.5 E-flat minor, 28:1 Ebm7.
soprano = \absolute {
  g''4. e''8 c''4 r4 | c''4. des''8 des''4. f''8 | ges''4. f''8 f''4. ees''8 | des''4 r2. | r1 | ees''2. ees''8 d''8 | ees''2. ees''8 d''8 | ees''4. f''8 f''4. aes''8 | aes''2. ges''8 ees''8 | f''4. des''8 bes'4 r4 | r1 | des''2. des''8 c''8 | c''1 |
}
alto = \absolute {
  e'4. g'8 c'4 c'4 | aes'2 bes'2 | bes'2 a'2 | f'1 | des''2. c''4 | bes'4 a'4 aes'2 | ges'2. f'4 | aes'4. c''8 f'4 f'4 | f'2 bes'2 | bes'2 g'2 ~ | g'2 bes'2 ~ | bes'4 bes'8 a'8 ~ a'2 ~ | a'1 |
}
tenor = \absolute {
  c2. e4 | f2 des'2 | ees'2 c'2 | bes4 r2. | bes8 a8 bes8 c'8 des'8 c'8 ees'8 ges8 | des'4 c'8 f'8 ~ f'2 | ees'8 f'8 ees'8 des'8 ces'4 des'4 | ees'2 aes2 | aes2 bes2 | bes1 | g2. g8 ges8 | ges1 ~ | ges1 |
}
bass = \absolute {
  c,2. c4 | f,2 bes,2 | ees,2 f,2 | bes,2. bes,8 a,8 | bes,2. bes,8 a,8 | bes,4. c8 c4. ees8 | ees2. des8 bes,8 | c4. aes,8 f,4 ees,4 | des,2. c,4 | f,2 e,2 ~ | e,4 e,8 ees,8 ~ ees,2 ~ | ees,1 ~ | ees,1 |
}
