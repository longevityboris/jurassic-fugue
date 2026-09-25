\version "2.24.0"
% bars 55-66
% Section 7: Apotheosis (the whole tune in B-flat major over the triple counterpoint turned major) and coda.
% Composed from design/final-lab/sections/sec07_apotheosis_coda.ly.
% Verify: python3 design/final-lab/splice_check.py score/sections/sec07_apotheosis_coda.ly  (PASS)
%
% UNCHANGED (map, BLUEPRINT sections 6-7): S 55:1-63:1 the tune, 63:1-65:1 d'' held; B 55:4-58:4 CS1
% major, 59:1-63:1 the answer, 63-66 the tonic pedal; T 56:1-58:4 CS2 major, 61:1-62:4 the answer's
% mirror, 62:4 E-flat, 65:1-66 the subject's head; A 59:1 A, 60:3 A-G, 62:1 E-A. Every boundary entry.
%
% THE FREE VOICES
% * Bar 55 (bass and tenor free until CS1/CS2 enter). Bass bes,2 c4 (was bes,2.): under the tune's held
%   B-flat the harmony moves I (55:1), 5-6 in the tenor (G, 55:2), ii7 (55:3), V7sus4 (55:4, the lament's
%   F), V7 (55:4.5), I6 (56:1). The tune's own B-flat becomes the seventh of ii7 and the fourth of V and
%   resolves to its neighbour A: the subject's head becomes a 7-6 suspension (55:3, against the tenor's C).
%   Tenor F G C leads into CS2's B-flat.
% * Alto 55-58, the minor shadow sung as a chain. D-E-flat-(E-flat)-D is the mirror sigh (x x+1 x) under the
%   tune's lower neighbour; the E-flat is prepared over ii7, held as V's seventh and resolves late as a 9-8
%   over the lament's D (56:1). Then F, G rising; G held over the lament's chromatic fall B-flat A A-flat
%   (sixth, passing seventh, then a 7-6 at 57:3), F held into the G-flat (7-6 at 58:1): a 7-6 chain over the
%   passus duriusculus, the dolente inside the apotheosis. At 58:2 the alto leaps to B-flat to complete
%   iv6 (E-flat minor needs its fifth), holds it as a 7-6 over CS2's C (58:3, ii half-dim 4/2) and turns
%   B-flat A-flat B-flat: the subject's head neighbour in its minor form, under the tune's held E-flat.
% * Bar 59 (tenor and alto free around the KEEP A). Tenor E-flat is the seventh of V7 as the blueprint asks,
%   then C, A (the third on 59:3), B-flat, C (C7/E complete at 59:4.5 with the alto's G). The alto takes the
%   seventh over, F E-flat D, and holds D while the tune leaps to D5: it no longer moves in the tune's rhythm
%   (the skeleton's A-F-C shadowed C-A-F).
% * 60: the alto's G, prepared in C7/E, is held over the answer's F as a 9-8 (60:1) under the tune's long C;
%   the tenor sings A (the third) as the blueprint asks. 61: A on the downbeat keeps V7 complete under the
%   tune's E-flat; the alto rises to C (61:2, its highest note, after the tune's peak), holds it as a 4-3 over
%   the answer's re-struck G (61:3; also a 2-3 under the tune's D) and falls B-flat G into the KEEP E.
% * Coda 63-66: the alto sings the inversion's head in major (F F F G F) under the held d'', then the mirror
%   sigh again in diminution with its G tied over the tenor's F: a 9-8 (64:3); its F is tied into 65 so the
%   tenor's head (65:1) enters under no new inner attack. The tenor keeps its tolling
%   D F | B-flat F arpeggio so that its final head (65) enters as the one moving line. Soprano 65 stays
%   d''2 c''2: the neighbour D C D in augmentation above the tenor's B-flat A B-flat, and the C at 65:3 is the
%   agent of the tenor's 2-3 (65:3), which a held D would cancel. The I at 66:1 is completed by the alto's F
%   at 66:3 (BLUEPRINT risk 11).
%
% SUSPENSIONS (suspensions.py, strong beats, this section): 55:3 S 7-6; 56:1 A 9-8; 57:3 A 7-6; 58:1 A 7-6;
% 58:3 A 7-6; 60:1 A 9-8 (listed against the tenor's A as 7-6); 61:3 A 4-3/2-3; 64:3 A 9-8; 65:3 T 2-3
% (skeleton). 9 in the section, 8 new. Whole piece with only this section composed: 12 strong.
%
% FLAGS (splice_check.py, strict.py -v, check.py on bars 54-66):
% * No new D4?, DIR, MEL, XREL, CLASH, unison or parallel. D4? 54:3 and XREL 60:4.5-61:1 are the skeleton's.
% * New ACC2 59:3 soprano F4 / alto E-flat4: the seventh of V7 (F A E-flat over F2), a passing seventh
%   F E-flat D struck with the tune's F and resolved to D at 59:3.5. Chord seventh.
% * Skeleton ACC2 59:1 (tenor E-flat, the V7 seventh) and 61:1 (the tune's E-flat, the V7 seventh); ACC 65:3
%   (V7 over the tonic pedal: pedal licence). HOL 66:1 as in the skeleton (completed at 66:3).
% * Parallel imperfect consonances: alto/tenor sixths 60:2-60:4.5 (F/A, A/C, G/B-flat) and alto/bass tenths
%   60:4-61:1, two moves each, fixed by the KEEP A-G, the tenor's A (the third) and the answer; the skeleton
%   had the same sixths from 60:1 and three tenth moves; the alto's C at 61:2 now breaks the tenths.
% * No dynamics, tempo or articulation in the voices (plan.json).
soprano = \absolute {
  % 55
  bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 |
  % 59
  c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | c''1 |
  % 63
  d''1~ | d''1 | d''2 c''2 | d''1 |
}
alto = \absolute {
  % 55
  d'2 ees'2~ | ees'8 d'8 f'2 g'4~ | g'2. f'4~ | f'8 ees'8 bes'4~ bes'8 aes'8 bes'8 f'8 |
  % 59
  a'4. f'8 ees'8 d'4 g'8~ | g'4 f'4 a'4. g'8 | a'4 c''4~ c''8 bes'4 g'8 | e'2. a'4 |
  % 63
  f'2. f'8 g'8 | f'4 f'8 g'8~ g'4 f'4~ | f'2 ees'2 | d'2 f'2 |
}
tenor = \absolute {
  % 55
  f4 g4 c'2 | bes8 a8 bes8 c'8 d'8 c'8 ees'8 g8 | d4 c8 f8 ~ f2 | ees8 f8 ees8 d8 c4 d4 |
  % 59
  ees4 c4 a4 bes8 c'8 | a2 c'4. bes8 | f4. e8 e4. c8 | c2. ees4 |
  % 63
  d2 f2 | bes2 f2 | bes2. bes8 a8 | bes1 |
}
bass = \absolute {
  % 55
  bes,2 c4 f,4 | d2. c4 | bes,4 a,4 aes,2 | ges,2. f,4 |
  % 59
  f,2. f,8 e,8 | f,2. f,8 e,8 | f,4. g,8 g,4. bes,8 | bes,2. a,8 f,8 |
  % 63
  bes,1 | bes,1 | bes,1 | bes,1 |
}
