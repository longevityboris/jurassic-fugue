\version "2.24.0"
% bars 55-66
% Section 7: Apotheosis (the whole tune in B-flat major over the triple counterpoint turned major) and coda.
% Composed from design/final-lab/sections/sec07_apotheosis_coda.ly; revised after the sec07 review (1-13) and
% after the whole-piece review, round 1 (this section's fixer list, findings 1-12: see WHOLE-PIECE REVIEW).
% Verify: python3 design/final-lab/splice_check.py score/sections/sec07_apotheosis_coda.ly  (PASS)
%
% UNCHANGED (map, BLUEPRINT sections 6-7): S 55:1-63:1 the tune, 63:1-65:1 d'' held; B 55:4-58:4 CS1
% major, 59:1-63:1 the answer, 63-66 the tonic pedal; T 56:1-58:4 CS2 major, 61:1-62:4 the answer's
% mirror, 62:4 E-flat, 65:1-66 the subject's head; A 59:1 A, 60:3 A-G, 62:1 E-A. Every boundary entry.
% FREE: A 55-58, 59:2.5-60:3, 61, 63-66; T 55, 59:1-61:1, 63-64; S 65-66; B 55:1-55:4.
%
% WHOLE-PIECE REVIEW, ROUND 1 (what changed in this file, and why)
% * 8, 9 (bar 55): the tonic is back under the tune's head. The bass holds B-flat2 until the lament's F (55:4),
%   as in the skeleton; alto and tenor move only inside the B-flat triad. The tune's B-flat stays the root
%   until the lament makes it the 6/4's fourth. The old bar (I, vi6, ii7, V7sus4 under the held B-flat) made
%   the head lean on its A, and its alto E-flat was a minor ninth over the lament's D at 56:1. Both are gone.
% * 5 and 4 (60:4): tenor c'4 des'8 c'8 (was c'4. g8). The tune's peak f'' now sounds over D-flat4, the b6-5
%   sigh of 34:1 and 50:3 on the major dominant, so the minor is remembered at the peak.
% * 6 and 4 (64:2.5): alto f'4 f'8 ges'8~ ges'4 f'4~ (was g'). The head's diminution recalls its minor form,
%   and a real prepared suspension joins the coda's only borrowed colour.
% * 10, 11 (bar 61): the skeleton's alto a'4. bes'8 bes'4. g'8 (was a'4 c''4~ c''8 bes'4 g'8). The alto stays
%   a third under the tune's bar-7 cadence and leaves C5 to the tune.
% * 12 (65-66): alto f'2 c''2 | bes'2 f'2 (was f'2 c'2 | d'2 f'2). The last head B-flat A B-flat is no longer
%   inside a cluster.
% * Not in the list, same aim as 4 and 5 (59): tenor ees4. d8 (was ees4 c4). The V7's seventh resolves by
%   step instead of leaving by leap, and V7 lasts a beat and a half instead of one.
% * 2 (suspensions): the strong-beat count in this file falls from 8 to 5 (tool). No real one against the bass
%   can be added inside this section's locks (see SUSPENSIONS for the bar-by-bar reason).
% * 1, 3, 7 and the tempo half of 8 need sec06, plan.json/piece.py or the blueprint: FOR THE DESIGN OWNER.
%
% THE FREE VOICES
% * 55 (bass and tenor free until CS1/CS2 enter). Alto D4, E-flat4 (passing, weak eighth 55:2.5), F4; tenor
%   F3 rising a sixth to D4 (55:3). The two exchange D and F (a voice exchange inside I), so 55:1-55:3.5 is
%   B-flat major with the tune's B-flat as its root, and bar 55 still moves (C1-M1). 55:4 I6/4 (the lament's
%   F), 55:4.5 iii6 passing (D F A over F; the blueprint's "vi6" for the same sonority is a mislabel), 56:1 I6. The tenor's F-D sixth anticipates the lament's sigh (bass F2-D3,
%   55:4-56:1), an octave above and a beat and a half early, and falls a third into CS2's B-flat against the
%   bass's rise (not D3: a rising sixth in parallel with the bass's, and 15 semitones under the alto). The
%   alto holds F4 across 56:1, a consonance on the tune's second downbeat, then G4 at 56:4 (ii7).
% * 57-58, the minor shadow as a chain. The G (from 56:4) is a seventh over the lament's passing A (57:2, with
%   the tune's B-flat a ninth over it), and both resolve on 57:2.5, the G falling to F: a weak-beat 7-6, and
%   V6 (57:2.5) and v6 (57:3) sound clean. F is re-struck at 57:4 and held into the G-flat: 7-6 at 58:1. At
%   58:2 the alto leaps to B-flat to complete iv6 (E-flat minor needs its fifth). At 58:3 CS2's C makes the
%   chord ii half-dim 4/3 (C E-flat G-flat B-flat over G-flat), and the alto turns B-flat A B-flat, the
%   subject's own semitone head. Its A makes 58:3.5 A dim7 over G-flat (vii dim 4/2), the hinge chord of
%   54:4, so the minor shadow closes on the chord that first opened onto the major and resolves the same way,
%   into the I6/4 at 58:4 (A up to B-flat, the tune's E-flat5 down to D5).
% * 59 (alto free after the KEEP A; tenor free). The tenor holds E-flat, the seventh of V7, for a beat and a
%   half (V7 complete with the alto's A and the tune's C), and resolves it by step to D3 (59:2.5, 7-6 over the
%   answer's held F, under the tune's A4). Then A3 (the third, 59:3), B-flat3, C4 (C7/E complete at 59:4.5
%   with the alto's G). The KEEP A has the tune's dotted rhythm a third below (forced); then the alto falls a
%   sixth to C4 (59:2.5) and holds it through the tune's F4, so 59:3 is a clean F2 A3 C4 F4 and the tune's
%   falling arpeggio C-A-F is heard alone on top. D4 then rises to G4, preparing the 9-8 at 60:1. Not f'8 at
%   59:4: F4-G4 against the tenor's B-flat3-C4 are parallel fifths.
% * 60: the alto's G, prepared in C7/E, is held over the answer's F as a 9-8 (60:1) under the tune's long C.
%   The tenor sings A (the third) as the blueprint asks, then C4 (60:3). Under the tune's f'' it adds D-flat4
%   (60:4: F2 D-flat4 A4 F5, V with its b6, the augmented triad). The D-flat falls to C4 at 60:4.5, making
%   C7/E (V6/5 of V) with the alto's KEEP G4 and the tune's B-flat4, and C4 leaps to the mirror's F3 (61:1).
%   Rejected: c'4 ees'8 d'8 (V7, then E half-dim 7), because its E-flat4 is followed an eighth later by the
%   bass's E2 (XREL). Also rejected: a2 c'2 (C4 held), which is DIS!, the tune's B-flat4 an unresolved
%   seventh over a held C4; re-struck after the D-flat, check.py lists that seventh as a weak DIS only.
% * 61: V7 without the fifth under the tune's E-flat (F2 F3 A4 E-flat5). The alto stays a third under the
%   tune: A4, then B-flat4 with the answer's G and the tune's D (61:2.5, vii half-dim 6/5 of V: G2 E3
%   B-flat4 D5), re-struck with everyone at 61:3, then G4 (61:4.5) into the KEEP E. The tune's C5 arrives only
%   in the tune (61:4.5, 62).
% * Coda 63-66. The alto sings the inversion's head in major (F F F G F) under the held d''. It then sings
%   that head in diminution in its minor form, F F G-flat F. G-flat4 enters at 64:2.5 consonant with the pedal
%   and the tenor's B-flat3, is held as a minor ninth over the tenor's F3 (64:3), resolves to F (64:4) and is
%   tied into 65. Against the held d'' it is the G-flat/D augmented fifth of 58:2.5, the one chromatic note of
%   63-66. The alto's G (63:4.5) and G-flat (64:2.5) are in one voice: no cross relation. The tenor resolves
%   the seventh E-flat3 to D3 (63:1), then sings the lament's head in major as the bass sang it at
%   55:4-57:1: F rising a sixth to D (63:3-63:4), D C B-flat (64:1-64:2.5). There it turns away from the
%   chromatic fall onto F, the subject's own last note, and rests an eighth (64:4.5). B-flat A B-flat (65:1)
%   then enters as a real entry, by a leap out of silence. Soprano 65-66 d''2 ees''2 | d''1: D E-flat D, the
%   mirror sigh (upper neighbour) against the tenor's B-flat A B-flat (lower neighbour) in contrary motion.
%   Alto 65-66 f'2 c''2 | bes'2 f'2: the alto leaps to C5, a third under the soprano's E-flat5, so the tenor's
%   B-flat3 is a 9-10 against it (65:3) as in the skeleton, and the last head sounds alone in its octave.
%   65:4.5 is the rootless V7 A3 C5 E-flat5 over the pedal (no G sounds: not IV6/4). Its seventh E-flat5
%   resolves in the top voice at 66:1, with C5 falling to B-flat4 a third below it. The alto's F at 66:3
%   completes the I (BLUEPRINT risk 11).
%
% SUSPENSIONS. suspensions.py credits 5 strong-beat suspensions in this section (was 8): 58:1 A 7-6 over
% G-flat2; 60:1 A 9-8 over F2 (the tool lists it against the tenor's A3); 58:3 A 7-6 against the tenor's C3
% only; 64:3 A G-flat4-F4, a minor ninth over the tenor's F3 (a minor sixth over the pedal); 65:3 T 9-10 under
% the alto's C5. It also credits 3 weak ones (was 2): 56:4 S (skeleton), 57:2 A 7-6 over the passing A2, and
% 55:4 S. 55:4 is the tune's re-struck B-flat over the lament's F, resolving to A. The tool used to merge it
% into the old 55:3 suspension; it is a 6/4 figure, not a real suspension. Gone: 55:3 S and 56:1 A (the
% reharmonised head, review 9) and 61:3 A (a syncopation, review 11).
% Real ones against the bass: 58:1 and 60:1, plus 64:3 and 65:3 over the pedal, where the tenor is the
% harmonic bass. A new one would need the bass to strike a new pitch on beat 1 or 3. In this section it does
% so only at 56:1, 57:1, 57:3, 58:1, 60:1, 61:1 and 63:1; 59:1, 61:3 and 62:1 re-strike the same pitch, and
% the pedal (63-66) keeps any note consonant that was consonant at its preparation. 56:1 is the tune's head
% (review 9). At 57:1 the alto must lie above CS2's E-flat4 at 56:4, so it can hold only G4, a sixth over
% B-flat2. C4 there would be reached by a leap at 56:4.5 with one eighth of preparation, the kind the review
% discounts at 14:1 and 19:3. At 57:3 the alto's only consonant notes at 57:2.5 (A, C, F) stay consonant
% with A-flat2. 58:1 and 60:1 are taken. A second held note at 60:1 is not possible: the tenor's G3 would
% double the alto's 9-8 in octaves, and its other candidates are dissonant at 59:4.5. At 61:1 the V7 needs the
% alto's A, which a tritone under E-flat5 cannot prepare. At 63:1 only the V7's seventh (tenor E-flat3,
% KEEP) or the alto's A4 could be held over the tonic; either would suspend the cadence the tonal plan
% leads to, with the tune's D5 doubling the note of resolution. Rule 5's strong quota has to come from finding
% 2's other slots (sec03 free alto 20-25, sec04 inner voices).
%
% FLAGS (splice_check.py, strict.py -v, check.py on bars 54-66, plus a scan of every voice pair):
% * Counts: splice_check PASS against SK_final and against all seven score sections spliced (with joins:
%   strict clash 0, xrel 1, acc 3, acc2 5, as before); check.py: 0 errors, 0 parallels, 0 beat-par,
%   0 unjustified.
% * No new D4?, DIR, MEL, XREL, CLASH, unison or parallel. D4? 54:3 and XREL 60:4.5-61:1 are the skeleton's.
%   Review 5 asked to watch D-flat4 (tenor, 60:4, one eighth) against the tune's D5 (61:2.5): two and a half
%   beats apart, with the tenor's C4 and F3 and the tune's E-flat5 between, and D5 is the tune's own locked
%   note; strict.py (a quarter's window) does not flag it.
% * strict: ACC2 59:1 (the tenor's E-flat3 over F2) and 61:1 (the tune's E-flat5 over F2 and F3), both V7
%   sevenths from the skeleton; ACC 65:3 (V7 over the tonic pedal: pedal licence; the alto's note is now C5).
%   HOL 66:1 as in the skeleton (completed at 66:3).
% * Spelled dissonances that check.py counts as sixths: 60:4 D-flat4/A4 and 64:2.5-64:4 G-flat4/D5,
%   augmented fifths, both intended (b6 over V; the G-flat/D of 58:2.5).
% * Hidden fifths and octaves off the outer pair (check.py tests only soprano/bass). New: fifths at 59:2.5 S/T
%   (the tune falls C5-A4 while the tenor's seventh resolves E-flat3-D3 by step, to a twelfth) and 60:4.5
%   A/T (A4/D-flat4 to G4/C4, an augmented fifth to a fifth, both stepping down as the D-flat resolves). As
%   before: octaves 59:4 S/A (the 6/4's third doubled for one eighth) and 61:4.5 S/T, fifths 59:4.5 A/T and
%   61:4.5 A/T; 57:2.5 and 60:1 are between locked lines. The old octave 60:4.5 A/T (C4-G3) is gone.
% * Parallel imperfect consonances: alto/bass tenths 60:3-61:4.5 (A/F, G/E, A/F, B-flat/G: three moves, the KEEP
%   A-G against the locked answer, then review 11's skeleton B-flat, as in SK_final); tenor/bass sixths
%   57:2.5-58:1 (CS2 against CS1, locked, skeleton).
% * Idiom. Strings: every part in its instrument's compass; violin II's C5 at 65:3 is an octave above the
%   viola's B-flat3 A3. Piano (pedal each harmony): the right hand takes the tenor at 55:3-56:1 (D4 F4
%   B-flat4), 59:3-60:4.5 and 63:4-64:1 (D4-D5). At 60:4 the right hand holds D-flat4 A4 F5, a tenth (roll if
%   needed), while the left hand strikes F2 then E2. Remaining tenths: right hand B-flat3-D5 at 59:4; A3 at
%   60:1, a minor tenth under C5 in the right hand or over F2 in the left (risk 4 lists bars 59 and 60).
%   65:3-66:1: the left hand has only B-flat2 and the tenor's B-flat3/A3; the right hand has C5 E-flat5, then
%   B-flat4 D5.
% * No dynamics, tempo or articulation in the voices (plan.json).
%
% FOR THE DESIGN OWNER (not applied: they change sec06, plan.json via piece.py, or the blueprint)
% * Finding 1 (sec06 KEEP notes, alto 54 c''2 a'8 f'8 ees'4, tenor 54 a2 c'2). Tested on a copy of all
%   score sections with this file: the hinge's seventh then resolves E-flat4-D4 into this file's 55:1 (alto
%   D4, tenor F3; no boundary change here). check.py 0/0/0/0; strict and suspension counts unchanged; the
%   only new flag is D4? 54:4 (C4 over G-flat2, the dim7's tritone). It also removes the alto/tenor sixths
%   54:3-55:1. After it: plan.json KEEP alto 53:3-55:1 and tenor 52:3-55:1, and sec06's boundary table
%   (alto last note E-flat4, tenor C4, both at 54:4).
% * Findings 7 and 8, tempo half. piece.py sec07 (section-relative), tested with perform.py on a copy of
%   plan.json and all score sections with this file:
%     tempo=[{'at': '1:1', 'bpm': 72}, {'at': '8:1', 'until': '9:1', 'to_bpm': 60},
%            {'at': '9:1', 'until': '12:3', 'to_bpm': 56}]
%     dynamics: replace {'at': '7:3', 'until': '9:1', 'to': 'mp'} by {'at': '7:3', 'level': 'mf'}
%       (mf held through the cadence; the existing 9:1-12:3 > pp starts at the arrival)
%     roles: ('soprano', '1:1', '11:1', 'subject')  (the d'' plays as the tune's last note, not as a free one)
%   sec06: drop {'at': '9:1', 'until': '10:1', 'to_bpm': 56}, so the hinge stays at 62 and 72 at 55:1 is a
%   gentle a tempo, not a 29% jump.
%   Measured: 232.1 s now; 233.7 s with the sec07 changes; 233.5 s with both (inside 240). Piano velocities:
%   the V7 root F2 at 62:4.5 goes from 65 to 75, and the d'' at 63:1 from 57 to 82, above the other voices
%   (67-70; they were 55-58). The peak at 60:4 is unchanged (92/80/91).
% * Finding 3 (S2 never imitated) has no slot here. At 59-62 S2 is in the tune, with the answer below it,
%   the mirror in the tenor and the KEEP A/E-flat of V7 in the free voices. In 63-66 its head (C A F) would
%   outline F major over the tonic pedal.
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
  d'4. ees'8 f'2~ | f'2. g'4~ | g'4. f'8~ f'4 f'4~ | f'8 ees'8 bes'4~ bes'8 a'8 bes'8 f'8 |
  % 59
  a'4. c'8~ c'4 d'8 g'8~ | g'4 f'4 a'4. g'8 | a'4. bes'8 bes'4. g'8 | e'2. a'4 |
  % 63
  f'2. f'8 g'8 | f'4 f'8 ges'8~ ges'4 f'4~ | f'2 c''2 | bes'2 f'2 |
}
tenor = \absolute {
  % 55
  f2 d'2 | bes8 a8 bes8 c'8 d'8 c'8 ees'8 g8 | d4 c8 f8 ~ f2 | ees8 f8 ees8 d8 c4 d4 |
  % 59
  ees4. d8 a4 bes8 c'8 | a2 c'4 des'8 c'8 | f4. e8 e4. c8 | c2. ees4 |
  % 63
  d2 f4 d'4~ | d'4 c'8 bes8 f4~ f8 r8 | bes2. bes8 a8 | bes1 |
}
bass = \absolute {
  % 55
  bes,2. f,4 | d2. c4 | bes,4 a,4 aes,2 | ges,2. f,4 |
  % 59
  f,2. f,8 e,8 | f,2. f,8 e,8 | f,4. g,8 g,4. bes,8 | bes,2. a,8 f,8 |
  % 63
  bes,1 | bes,1 | bes,1 | bes,1 |
}
