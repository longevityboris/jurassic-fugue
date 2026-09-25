\version "2.24.0"
% bars 55-66
% Section 7: Apotheosis (the whole tune in B-flat major over the triple counterpoint turned major) and coda.
% Composed from design/final-lab/sections/sec07_apotheosis_coda.ly; revised after the sec07 review (1-13).
% Verify: python3 design/final-lab/splice_check.py score/sections/sec07_apotheosis_coda.ly  (PASS)
%
% UNCHANGED (map, BLUEPRINT sections 6-7): S 55:1-63:1 the tune, 63:1-65:1 d'' held; B 55:4-58:4 CS1
% major, 59:1-63:1 the answer, 63-66 the tonic pedal; T 56:1-58:4 CS2 major, 61:1-62:4 the answer's
% mirror, 62:4 E-flat, 65:1-66 the subject's head; A 59:1 A, 60:3 A-G, 62:1 E-A. Every boundary entry.
% FREE: A 55-58, 59:2.5-60:3, 61, 63-66; T 55, 59:1-61:1, 63-64; S 65-66; B 55:1-55:4.
%
% THE FREE VOICES
% * Bar 55 (bass and tenor free until CS1/CS2 enter). Bass bes,2 c4 (was bes,2.): under the tune's held
%   B-flat the harmony moves I (55:1), 5-6 in the tenor (G, 55:2), ii7 (55:3), V7sus4 (55:4, the lament's
%   F), V7 (55:4.5), I6 (56:1). The tune's own B-flat becomes the seventh over C and the fourth of V and
%   resolves to its neighbour A: the subject's head becomes a 7-6 suspension (55:3, against the tenor's C).
%   Tenor F G C leads into CS2's B-flat.
% * Alto 55-58, the minor shadow sung as a chain. D-E-flat-(E-flat)-D is the mirror sigh (x x+1 x) under
%   the tune's lower neighbour; the E-flat is prepared over ii7, held as V's seventh and resolves late as
%   a 9-8 over the lament's D (56:1). Then F, G rising. The G (from 56:4) is a seventh over the lament's
%   passing A (57:2, with the tune's B-flat a ninth over it) and both resolve on 57:2.5, the G falling to
%   F: a weak-beat 7-6, and V6 (57:2.5) and v6 (57:3) sound clean. F is re-struck at 57:4 and held into
%   the G-flat: 7-6 at 58:1. At 58:2 the alto leaps to B-flat to complete iv6 (E-flat minor needs its
%   fifth); at 58:3 CS2's C makes the chord ii half-dim 4/3 (C E-flat G-flat B-flat over G-flat), and the
%   alto turns B-flat A B-flat, the subject's own semitone head: its A makes 58:3.5 A dim7 over G-flat
%   (vii dim 4/2), the hinge chord of 54:4, so the minor shadow closes on the chord that first opened onto
%   the major and resolves the same way, into the I6/4 at 58:4 (A up to B-flat, the tune's E-flat5 down
%   to D5: the diminished fifth resolves inward). The whole-tone A-flat (A-flat7 over G-flat) is gone.
% * Bar 59 (alto free after the KEEP A; tenor free). The tenor keeps E-flat, the seventh of V7, as the
%   blueprint asks, then C, A (the third on 59:3), B-flat, C (C7/E complete at 59:4.5 with the alto's G).
%   The KEEP A has the tune's dotted rhythm a third below (forced); then the alto falls a sixth to C4
%   (59:2.5) and holds it through the tune's F4, so 59:3 is a clean F2 A3 C4 F4 and the tune's falling
%   arpeggio C-A-F is heard alone on top. (The old a'4. f'8 ees'8 shadowed it in thirds, struck its F4 half
%   a beat early and rubbed E-flat4 a second under it: ACC2 59:3.) The alto still attacks with the tune at
%   58:4, 58:4.5, 59:1 and 59:2.5 (a B-flat held at 58:4.5 would be a unison with the tune). Then D4
%   rises to G4, preparing the 9-8 at 60:1. Trade-off: the tenor's E-flat3 (59:1) leaves by leap inside
%   the V7 arpeggio, as in the skeleton, and D arrives only as the 6/4's third at 59:4 (S D5, A D4); the
%   old alto F4-E-flat4-D4 was the one version tested that re-sounded and resolved that seventh without a
%   cross relation (a'4. c'8~ c'8 ees'8 d'8 g'8~ gives XREL alto E-flat4 59:3.5, bass E2 59:4.5), but it
%   cost the tune its arpeggio. Not f'8 at 59:4: F4-G4 against the tenor's B-flat3-C4 are parallel fifths.
% * 60: the alto's G, prepared in C7/E, is held over the answer's F as a 9-8 (60:1) under the tune's long
%   C; the tenor sings A (the third) as the blueprint asks, then C4, then G3 at 60:4.5 (was B-flat3): E dim
%   (vii dim of V) with its third doubled, the alto's KEEP G4 reached in contrary motion, and G3 steps
%   into the mirror's F3 (61:1). The alto/tenor sixths stop after one move (F4/A3 to A4/C4); gone are the
%   tenor's B-flat3 doubling the tune's B-flat4 by similar motion (a direct octave under F5-B-flat4), its
%   tritone over E2 and the four-voice block attacks at 60:4.5 and 61:1. Not a2 c'2 (complete C7/E):
%   DIS! 60:4.5, the tune's B-flat4 an unresolved seventh against a held C4.
% * 61: V7 without the fifth under the tune's E-flat (F2 F3 A4 E-flat5). The alto rises to C (61:2, its
%   highest note, after the tune's peak), so for half a beat the V7 lacks its third (F2 F3 C5 E-flat5); the
%   answer's G and the tune's D arrive against the C on the weak eighth 61:2.5 and re-strike at 61:3; the
%   alto falls B-flat (61:3.5, vii half-dim 7 of V) G into the KEEP E.
% * Coda 63-66. The alto sings the inversion's head in major (F F F G F) under the held d'', then the
%   mirror sigh in diminution, its G tied over the tenor's F (64:3, see SUSPENSIONS), its F tied into 65.
%   The tenor resolves the seventh E-flat3 to D3 (63:1), then sings the lament's head in major as the bass
%   sang it at 55:4-57:1: F rising a sixth to D (63:3-63:4), D C B-flat (64:1-64:2.5), where it turns away
%   from the chromatic fall onto F, the subject's own last note, and rests an eighth (64:4.5); B-flat A
%   B-flat (65:1) then enters as a real entry, by a leap out of silence, instead of continuing a tolling
%   half-note arpeggio (was D F | B-flat F). The inversion's head (alto) and the lament's head (tenor)
%   sound together over the pedal. Soprano 65-66 d''2 ees''2 | d''1: D E-flat D, the mirror sigh (upper
%   neighbour) against the tenor's B-flat A B-flat (lower neighbour) in contrary motion, the piece's two
%   neighbours in its last bar; the soprano no longer sings the tenor's own shape above it, earlier, in
%   parallel tenths. Alto 65 f'2 c'2: the tenor's B-flat3 is a 2-3 against the alto's C4 (65:3); 65:4.5 is
%   the rootless V7 A C E-flat over the pedal (no G sounds: not IV6/4), and its seventh E-flat5 resolves
%   in the top voice at 66:1. (Alto E-flat4 under the soprano's E-flat5 would make parallel octaves
%   E-flat/D at 65:3-66:1.) The I at 66:1 is completed by the alto's F at 66:3 (BLUEPRINT risk 11). Cost:
%   the soprano's C-D echo of 62-63 is no longer repeated in the coda.
%
% SUSPENSIONS. suspensions.py credits 8 strong in this section: 55:3 S 7-6; 56:1 A 9-8; 58:1 A 7-6; 58:3 A
% 7-6; 60:1 A 9-8 (listed as 7-6 against the tenor's A); 61:3 A 4-3/2-3; 64:3 A 9-8; 65:3 T 2-3 (skeleton;
% agent now the alto's C4); 7 new. Weak: 56:4 S (skeleton), 57:2 A 7-6 over the passing A2 (new).
% To the ear, strong-beat suspensions against the bass are 55:3, 56:1, 58:1, 60:1 (prepared by one eighth)
% and 65:3 (over the pedal the tenor is the real bass) = 5, 4 new. The tool also credits three that are not:
% 58:3 is a prepared chord seventh of ii half-dim 4/3 (B-flat a major third over G-flat2, a 7-6 against
% the tenor's C3 only); 61:3 is a syncopation (the dissonance starts on the weak eighth 61:2.5 after one
% eighth of preparation; the locked lines only re-strike at 61:3); 64:3 is a 6-5 over the pedal (G4 a
% sixth over B-flat2, a ninth only against the tenor's F3). The old 57:3 was never consonantly prepared
% (the G was dissonant from 57:2) and is now the weak 57:2. Whole piece (tool): SK_final with this section
% 11 strong; all seven score sections spliced as of this revision 21 strong, 11 weak.
%
% FLAGS (splice_check.py, strict.py -v, check.py on bars 54-66, plus a scan of every voice pair):
% * No new D4?, DIR, MEL, XREL, CLASH, unison or parallel. D4? 54:3 and XREL 60:4.5-61:1 are the skeleton's.
% * strict: ACC2 59:1 (the tenor's E-flat3 over F2) and 61:1 (the tune's E-flat5 over F2 and F3), both V7
%   sevenths from the skeleton; ACC 65:3 (V7 over the tonic pedal: pedal licence). HOL 66:1 as in the
%   skeleton (completed at 66:3).
% * Direct octaves off the outer pair (check.py tests only soprano/bass): 59:4 S/A (the tune leaps F4-D5,
%   the alto steps C4-D4: the 6/4's third doubled for one eighth) and 60:4.5 A/T (the alto steps A4-G4, the
%   tenor C4-G3).
% * Parallel imperfect consonances: alto/tenor sixths one move (60:2-60:3); alto/bass tenths 60:3-61:1
%   (A/F, G/E, A/F: two moves, the KEEP A-G against the locked answer); tenor/bass sixths 57:2.5-58:1
%   (CS2 against CS1, locked, skeleton).
% * Idiom. Strings: every part in its instrument's compass. Piano (pedal each harmony): the right hand
%   takes the tenor at 55:4-55:4.5 (C4-B-flat4), 59:3-60:3 and 63:4-64:1 (D4-D5). 60:1-60:4 is one F
%   harmony under the pedal, so the hands strike only new attacks, and the peak at 60:4 is F2 (left) and F5
%   (right) over the sustained C4 and A4. Three tenths remain (risk 4 lists bars 59 and 60): right hand
%   B-flat3-D5 at 59:4; A3 at 60:1, a minor tenth under C5 in the right hand or over F2 in the left; left
%   hand E2-G3 at 60:4.5 (roll if needed). 65:3-65:4.5: the left hand holds B-flat2 and takes the tenor
%   and the alto's C4 (B-flat2 B-flat3/A3 C4, a ninth), so the damper can change at 65:3 and the right
%   hand's E-flat5 stands alone; at 66:1 the right hand takes the alto's D4 under D5.
% * No dynamics, tempo or articulation in the voices (plan.json).
soprano = \absolute {
  % 55
  bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 |
  % 59
  c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | c''1 |
  % 63
  d''1~ | d''1 | d''2 ees''2 | d''1 |
}
alto = \absolute {
  % 55
  d'2 ees'2~ | ees'8 d'8 f'2 g'4~ | g'4. f'8~ f'4 f'4~ | f'8 ees'8 bes'4~ bes'8 a'8 bes'8 f'8 |
  % 59
  a'4. c'8~ c'4 d'8 g'8~ | g'4 f'4 a'4. g'8 | a'4 c''4~ c''8 bes'4 g'8 | e'2. a'4 |
  % 63
  f'2. f'8 g'8 | f'4 f'8 g'8~ g'4 f'4~ | f'2 c'2 | d'2 f'2 |
}
tenor = \absolute {
  % 55
  f4 g4 c'2 | bes8 a8 bes8 c'8 d'8 c'8 ees'8 g8 | d4 c8 f8 ~ f2 | ees8 f8 ees8 d8 c4 d4 |
  % 59
  ees4 c4 a4 bes8 c'8 | a2 c'4. g8 | f4. e8 e4. c8 | c2. ees4 |
  % 63
  d2 f4 d'4~ | d'4 c'8 bes8 f4~ f8 r8 | bes2. bes8 a8 | bes1 |
}
bass = \absolute {
  % 55
  bes,2 c4 f,4 | d2. c4 | bes,4 a,4 aes,2 | ges,2. f,4 |
  % 59
  f,2. f,8 e,8 | f,2. f,8 e,8 | f,4. g,8 g,4. bes,8 | bes,2. a,8 f,8 |
  % 63
  bes,1 | bes,1 | bes,1 | bes,1 |
}
