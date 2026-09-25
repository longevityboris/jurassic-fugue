\version "2.24.0"
% bars 13-19
% Section 2: Entry 4 (tenor answer, bass the full lament to C2, alto CS2) and the Episode (cell b over the
% falling fifths F B-flat E-flat A-flat into D-flat). Composed from design/final-lab/sections/sec02_entry4_episode.ly.
%
% Soprano descant (13-17), free. One line, not three arches: a fall G5-C5 (bar 14) and its mirror, a rise
% C5-G-flat 5 (15-16) against the falling lament. The rise's top is the first peak's G darkened to G-flat by the
% Neapolitan. G5 is sounded once (13:4.5-14:1).
%   13  F4. C8 C4. G8: cell b's rhythm with its repeated note, over the tenor's held entry note; C stays on top
%       while the tenor's F-E (4-3) resolves; the leap up to G (13:4.5) starts the fall.
%   14  G held over the bar line, then F, E-flat (half), D-flat, C: a stepwise fall of a fifth, contrary to CS2's
%       rise. C is anticipated at 14:4.5 over G2 (C E G D-flat: V with a flat ninth) and held while the bass
%       steps G-F. This removes D-flat 5/G2 to C5/F2 (a diminished fifth to a fifth in the outer voices) and
%       the old octave D-flat 5/D-flat 4 with CS2 at 14:4.5.
%   15  C D E-flat, then F (16:1): the descant rises by step while the lament falls F E E-flat D-flat, a wedge
%       that meets on E-flat at 15:3, three octaves apart. D natural rises here, D-flat fell in 14 (melodic
%       minor). D5 is a passing quarter held across 15:2.5, so CS2's leap to its peak C5 sounds alone under it:
%       no simultaneous leaps and no direct fifth or octave into 15:2.5, and 13:3-14:2 is no longer repeated.
%   16  F5 held across the alto's G-flat 4 at 16:3 is a 7-8 retardation prepared at 16:1 (the fifth of iv6).
%       It rises to G-flat 5 on the weak eighth, then returns to F. CS2 strikes the Neapolitan's root alone and
%       the descant takes it an eighth later.
%   17  C5 (half) E5 (dotted quarter) D5 (eighth). C holds while the tenor and bass play their dotted tails
%       (17:2.5 is a complete C7, G2 E3 B-flat 4 C5). E5 lands on the C7 at the mf peak (17:3) and holds
%       through the tenor's G3 (17:4, C7 complete in root position). D5 falls into the episode's C and fills the
%       gap after the 17:4 attack. (The old "cell-b rhythm" claim for this bar was wrong: 4. 8 4 4 was the
%       answer tail's rhythm.)
% Bass 17:3-18:1 (free): C2 is held for a dotted quarter, then E2 sounds at 17:4.5: V7, then vii half-dim 7 (E G
%   B-flat with the passing D), then i. The leading tone E resolves to F in the bass, and the tritone E2/B-flat 4
%   resolves inward to F2/A-flat 4. The bass holds while the tenor leaps C3-G3, so there is no tenor/bass hidden
%   fifth. The soprano's E5-D5 hands the E to the bass; the two E's never sound together, so the leading tone is
%   not doubled. The reviewer's tenor fix (E3 at 17:4) was not taken: under the held E5 it doubles the leading
%   tone (C3 E3 B-flat 4 E5, no fifth).
% Episode (18-19): the soprano's cell b as designed. The alto answers at the half bar (bes'4. des''8, 18:3); its
%   D-flat is tied into a 7-6 over E-flat (19:1). It then falls a diminished fifth, C5-G-flat 4 (19:2.5), which
%   gives E-flat minor its third on the half beat, and re-strikes G-flat 4 as the prepared seventh of A-flat7 at
%   19:3. This removes the unequal fifths G-flat 5/C5 to F5/B-flat 4 between soprano and alto and the thirdless
%   19:2.5. Tenor: G3 held over F (18:1); A-flat G-flat F E-flat (18:2-19:1), CS1's falling tetrachord; B-flat
%   held over A-flat (19:3); C4. At 19:1 alto and tenor lie 22 semitones apart, with the tenor on the bass's
%   octave, for 1.5 beats: the price of completing the tetrachord. 19:3 is deliberately thick: the tenor's 9th,
%   the alto's seventh and the soprano's 13th over A-flat resolve one at a time (9-8 at 19:3.5, the third C4 at
%   19:4, 13-12 at 19:4.5) into the complete A-flat7.
% Suspensions: suspensions.py -v counts 6 on strong beats. By kind:
%   Bach-grade (3): 18:1 T G-F, 9-8 over F2 (prepared at 17:4 as the fifth of C7); 18:3 T A-flat-G-flat, 7-6
%     over B-flat 2; 19:1 A D-flat-C, 7-6 over E-flat 2 (tied from the answer's 18:4.5).
%   Eighth-note syncopations (2): 14:1 S G-F is prepared by an eighth reached by a leap of a fifth; its F5 lands
%     a minor ninth over CS2's E4 and is followed at once by the XREL below, so it never lands on a clean
%     consonance. 19:3 T B-flat-A-flat, 9-8, is prepared by an eighth reached by a leap of a fifth from E-flat 3.
%   Not a suspension (1): 17:1 A A-flat is a re-struck b6-5 appoggiatura over E2 (a tie out of CS2's 16:4 note
%     would change a countersubject note), and its resolution G already sounds in the tenor's locked G3 a minor
%     ninth below. The tool counts it by its re-strike rule. It is not offered toward rule 5's strong-beat quota
%     and does not meet the spec's "prepare 17:1": under the locked tenor and CS2 no voice can prepare 17:1.
%     (The soprano's F held into 17:1 would resolve to E5 over the bass's E2.)
%   Not counted: the 16:3 retardation (it resolves upward).
%   16:1 has no suspension: with CS2 on B-flat/C and the tenor locked, the only dissonance that can be prepared
%   there is the soprano's E-flat as a 9-8 over D-flat, prepared by the octave E-flat 5/E-flat 2, which gives
%   octaves by suspension in the outer voices.
% Flags (splice_check PASS against SK_final.ly and against the assembled sections):
%   D4?  17:2.5 soprano C5 over G2: the fourth of V4/3 (G2 E3 B-flat 4 C5), held from 17:1 and cleared when the
%        bass reaches C2 at 17:3.
%   MEL  19:2.5 alto C5-G-flat 4: a falling diminished fifth (check.py counts semitones and calls it aug4),
%        recovered inside the interval by step at 20:1 (A-flat 4, sec03's boundary). G-flat is re-struck at
%        19:3, not tied: with a tie, check.py reports the seventh as DIS! unjustified, because the boundary
%        makes it rise.
%   XREL 14:1.5-14:2 alto E4 (CS2's rising lower neighbour), then the soprano's falling E-flat 5: the two
%        sevenths of f minor in contrary directions, never sounding together; each voice moves by step.
%   XREL 15:2-15:3 bass E2, then the soprano's E-flat 5. At that moment the bass itself steps E-E-flat (the
%        lament's chromatic step), and the soprano reaches the same E-flat by step from D; the two never sound
%        together. The skeleton had the same pair reversed (soprano E5, then bass E-flat 2).
%   ACC2 13:1 (the F/C 6/4 of the section's first downbeat) and 19:3 (alto G-flat 4, the seventh of A-flat7,
%        prepared at 19:2.5) come from the skeleton. There is no new ACC2: the 16:3 retardation is tied.
% Spec exception (declared): at 16:3.5 the soprano's G-flat 5 doubles CS2's G-flat 4 at the octave for one weak
%   eighth, as the retardation's resolution. G-flat 5 on beat 3 (the previous version) doubled CS2 for a whole
%   strong beat. D-flat 5 makes octaves with the bass into 16:4 (D-flat-C). B-flat 5 doubles the answer's B-flat 3.
% Harmony labels that now differ from BLUEPRINT section 6 (for the blueprint owner):
%   14:4.5 is V with a flat ninth (C E G D-flat), not vii dim 6.
%   16:3 is the N6/4 with the soprano's F as a 7-8 retardation; the soprano's G-flat arrives at 16:3.5.
%   17:4 is V7 complete; 17:4.5 is vii half-dim 7 over E2 with the passing D. The blueprint has "17:4 V7 with
%   passing D".
% Reports for the blueprint owner (outside this section's scope):
%   (a) sec02/sec03 join, 19:4.5-20:1. The seventh of V7 of D-flat (alto G-flat 4) rises to A-flat 4 at 20:1, and
%       alto/tenor move from G-flat 4/C4 (d5) to A-flat 4/D-flat 4 (P5). The seventh's F is in the soprano (F5,
%       20:1); the alto reaches F4 only at 20:2 (A-flat G-flat F). Both notes are boundary-locked and come from
%       the skeleton. Fix: sec03's alto starts on F4 at 20:1, or sec02's alto ends on G-flat 4 and falls to F4
%       inside bar 19. Otherwise list it among the known licences in BLUEPRINT section 9.
%   (b) The episode's answer at the half bar coincides with the leader's next cell b. From 17:4.5 to 18:4.5 the
%       soprano and alto therefore move mostly in thirds: the ear hears a harmonisation, not imitation.
%       Starting the answer where the leader holds (18:2 or 18:4) would make it audible as imitation. The
%       reviewer's local option, re-striking the alto's D-flat at 19:1, was not taken: it conflicts with the
%       19:2.5 fix above and turns the Bach-grade 19:1 7-6 into a re-struck seventh.
% Idiom, piano (S+A right hand, T+B left):
%   13:3: roll or split the alto's A3 and the soprano's C5 (a minor tenth in the right hand; F2-A3 is too wide
%     for the left).
%   Sostenuto pedal on C2 at 13:4 (lift at 14:1), on D-flat 2 at 16:1 (lift at 16:4) and on E-flat 2 at 19:1
%     (lift at 19:3), so the left hand takes the tenor dry: the 4-3 at 13:4.5, CS2's eighths over the tenor's
%     B-flat 3 and the 9-8 at 19:3.5 stay clean.
%   Damper pedal on one harmony at a time: 15:3-16:1 (C minor 7 over E-flat 2; the right hand holds), and
%     17:3-17:4.5 (C7, all chord tones), changed at 17:4.5.
%   The left hand then holds G3 over E2 (a minor tenth) and F2 (a ninth).
%   19:4: roll the A-flat 2-C4 tenth.
% Quartet: violin II from A3 (13:1), as the blueprint states; C2 is the cello's open string; no other problems.
soprano = \absolute {
  % 13
  f''4. c''8 c''4. g''8~ | g''8 f''8 ees''2 des''8 c''8~ | c''4 d''4 ees''2 | f''2~ f''8 ges''8 f''4 |
  % 17
  c''2 e''4. d''8 | c''4. des''8 des''4. f''8 | ges''4. f''8 f''4. ees''8 |
}
alto = \absolute {
  % 13
  a4. c'8 a4 r4 | f'8 e'8 f'8 g'8 aes'8 g'8 bes'8 des'8 | aes'4 g'8 c''8~ c''2 | bes'8 c''8 bes'8 aes'8 ges'4 aes'4 |
  % 17
  aes'4 g'8 bes'8~ bes'2 | aes'2 bes'4. des''8~ | des''4 c''8 ges'8 ges'2 |
}
tenor = \absolute {
  % 13
  f2. f8 e8 | f2. f8 e8 | f4. g8 g4. bes8 | bes2. aes8 f8 |
  % 17
  g4. e8 c4 g4~ | g8 f8 aes4~ aes4 ges8 f8 | ees4. bes8~ bes8 aes8 c'4 |
}
bass = \absolute {
  % 13
  c4. a,8 f,4 c,4 | aes,2. g,4 | f,4 e,4 ees,2 | des,2. c,4 |
  % 17
  e,4. g,8 c,4. e,8 | f,2 bes,2 | ees,2 aes,2 |
}
