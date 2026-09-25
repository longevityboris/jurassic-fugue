\version "2.24.0"
% bars 13-19
% Section 2: Entry 4 (tenor answer, bass the full lament to C2, alto CS2) and the Episode (cell b over the
% falling fifths F B-flat E-flat A-flat into D-flat). Composed from design/final-lab/sections/sec02_entry4_episode.ly.
%
% Soprano descant (13-17), free. One line: C5 held as a reciting tone while the answer enters (13:2.5-14:2), a
% short fall E-flat D-flat C (14), then a rise C5-G-flat 5 (15-16) against the falling lament. The descant's
% highest note is the Neapolitan's G-flat 5 (16:3.5); it no longer sings G5.
%   13  F4. C8 C2~: cell b's opening and its repeated note. The boundary F5 (13:1, fixed by the section table)
%       doubles the answer's F3 two octaves up; the descant leaves it at 13:2.5 and then holds. C5 is re-struck
%       at 13:3 as the bass lands on F2 and held through 14:1 (review round 1, finding 2), so the answer's
%       F-E-F (13:4-14:1) and the lament's entry on C2 (13:4) are the only moving lines at 13:4-14:1.
%       Before this fix, the descant leapt to G5 at 13:4.5 with the answer's E3 and tied it into 14:1 as a
%       major 7th over A-flat 2 and a major 9th over CS2's F4: three new events in one beat.
%   14  C5 held to beat 2, so 14:1 is a clean i6 (A-flat 2 F3 F4 C5) under CS2's first notes; then E-flat 5
%       (half), D-flat, C. C is anticipated at 14:4.5 over G2 (C E G D-flat: V with a flat ninth) and held
%       while the bass steps G-F. This avoids D-flat 5/G2 to C5/F2 (a diminished fifth to a fifth in the
%       outer voices) and an octave D-flat 5/D-flat 4 with CS2 at 14:4.5.
%   15  C D E-flat, then F (16:1): the descant rises by step while the lament falls F E E-flat D-flat, a wedge
%       that meets on E-flat at 15:3, three octaves apart. D natural rises here, D-flat fell in 14 (melodic
%       minor). D5 is a passing quarter held across 15:2.5, so CS2's leap to its peak C5 sounds alone under it:
%       no simultaneous leaps and no direct fifth or octave into 15:2.5.
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
%   19:2.5.
%   Tenor, a chain of suspensions over the falling fifths: G3 held over F (18:1, 9-8); A-flat held over B-flat
%   (18:3, 7-6), G-flat, F (7-6-5); F3 held across the bar line over E-flat (19:1, 9-8), resolving to E-flat 3
%   at 19:2 together with the alto's 7-6: a double suspension, 9 and 7 over E-flat 2 resolving to 8 and 6. So
%   CS1's falling tetrachord A-flat G-flat F E-flat now runs 18:2-19:2. Then B-flat 3 (19:2.5) held over A-flat
%   (19:3, 9-8), C4. The tenor meets the bass's octave only at 19:2, as the 9-8's resolution, for an eighth
%   (the previous version held E-flat 3 over E-flat 2 for 1.5 beats). Alto and tenor still lie 20-21
%   semitones apart in 19:1-19:2.5 (F3/D-flat 5, then E-flat 3/C5): the price of completing the tetrachord.
%   19:3 is deliberately thick: the tenor's 9th, the alto's seventh and the soprano's 13th over A-flat resolve
%   one at a time (9-8 at 19:3.5, the third C4 at 19:4, 13-12 at 19:4.5) into the complete A-flat7.
% Suspensions: suspensions.py -v counts 6 on strong beats (17:1 A, 18:1 T, 18:3 T, 19:1 A, 19:1 T, 19:3 T) and 1
%   on a weak beat (14:4 T F3-E3 over G2: the answer's own 7-6, listed now that its 14:1 preparation is
%   consonant with the held C5). By kind, applying the tests the review asks for (tied, not re-struck; held
%   note dissonant with the bass; the dissonance begins on the strong beat, where the bass attacks):
%   Bach-grade (4):
%     18:1 T G-F, 9-8 over F2, prepared at 17:4 for a quarter (the fifth of C7). The tool prints "2-3 against
%       alto A-flat 4" only because it tests the alto before the bass.
%     18:3 T A-flat-G-flat, 7-6 over B-flat 2, prepared at 18:2 for a quarter; the dissonance lasts an eighth
%       and the line goes on to F (7-6-5).
%     19:1 A D-flat-C, 7-6 over E-flat 2, tied from the answer's D-flat (18:4.5, cell b's upbeat: an eighth
%       reached by a third) and dissonant for a quarter.
%     19:1 T F-E-flat, 9-8 over E-flat 2 (new, round 1). Prepared at 18:4 for a quarter, reached by step
%       (G-flat 3-F3), consonant with every voice (a fifth over B-flat 2, a fourth under B-flat 4, a sixth under
%       D-flat 5). Tied; dissonant with the bass (a major 9th) from the bass's attack at 19:1; resolves at 19:2
%       to E-flat 3 while E-flat 2 still sounds. The tool prints "2-3 against soprano G-flat 5" only because it
%       tests the soprano first; against the bass it is a 9-8.
%   Eighth-note syncopation (1): 19:3 T B-flat-A-flat, 9-8 over A-flat 2, prepared by an eighth reached by a
%     leap of a fifth (E-flat 3-B-flat 3). Not lengthened: B-flat 3 struck at 19:2 meets the alto's C5 (the
%     7-6's resolution) a ninth apart, so the preparation is no longer consonant and the tool drops the
%     suspension (tested); and the tenor cannot take B-flat earlier: it holds the 19:1 9-8 until 19:2.
%   Not a suspension (1): 17:1 A A-flat is a re-struck b6-5 appoggiatura over E2 (a tie out of CS2's 16:4 note
%     changes a countersubject note: splice_check LOCK), and its resolution G already sounds in the tenor's
%     locked G3 a minor ninth below. The tool counts it by its re-strike rule. It is not offered toward rule 5's
%     strong-beat quota: under the locked tenor and CS2 no voice can prepare 17:1. (The soprano's F held into
%     17:1 would resolve to E5 over the bass's E2, doubling the leading tone.)
%   Removed in round 1: 14:1 S G-F, an eighth-note syncopation prepared by a leap of a fifth (finding 2 above).
%     The new 19:1 T replaces it, so this section still offers 5 strong-beat suspensions against the bass, now
%     with one eighth-note syncopation instead of two.
%   Not counted: the 16:3 retardation (it resolves upward).
%   No other strong beat in 13-17 can take a prepared suspension against the bass: only the soprano is free
%   there (A 14:1-17:1 CS, T locked to 17:4, B CS to 17:3). 15:1: the tenor's locked E3 at 14:4.5 forbids a
%   prepared E-flat, and G5 would be prepared by the octave G5/G2. 15:3: a D or D-flat over E-flat 2 would
%   resolve to the alto's C5 (a unison), and F or A-flat cannot be prepared over E2. 16:1: E-flat 5 is
%   prepared only by the octave E-flat 5/E-flat 2 (octaves by suspension in the outer voices); G-flat 5
%   prepared at 15:4.5 makes a cross relation with the tenor's G3; C6 would take the piece's top note from
%   Climax II. 17:3: F (4-3) cannot be prepared over E2 or G2, and a D (9-8) would leave the half cadence's
%   V7 without its third.
% Piece-wide (all current sections assembled on a copy, with this file): suspensions.py 21 strong, 12 weak (was
%   21 and 11); check.py 0/0/0/0; strict.py clash 0, xrel 7, acc 6, acc2 31, unchanged.
% Flags (splice_check PASS against SK_final.ly and against the assembled sections):
%   D4?  17:2.5 soprano C5 over G2: the fourth of V4/3 (G2 E3 B-flat 4 C5), held from 17:1 and cleared when the
%        bass reaches C2 at 17:3.
%   MEL  19:2.5 alto C5-G-flat 4: a falling diminished fifth (check.py counts semitones and calls it aug4),
%        recovered inside the interval by step at 20:1 (A-flat 4, sec03's boundary). G-flat is re-struck at
%        19:3, not tied: with a tie, check.py reports the seventh as DIS! unjustified, because the boundary
%        makes it rise.
%   XREL 14:1.5-14:2 alto E4 (CS2's rising lower neighbour), then the soprano's falling E-flat 5: the two
%        sevenths of f minor in contrary directions, never sounding together. The alto moves by step; the
%        soprano now reaches E-flat 5 by a leap of a third from the held C5 and leaves it by step.
%   XREL 15:2-15:3 bass E2, then the soprano's E-flat 5. At that moment the bass itself steps E-E-flat (the
%        lament's chromatic step), and the soprano reaches the same E-flat by step from D; the two never sound
%        together. The skeleton had the same pair reversed (soprano E5, then bass E-flat 2).
%   ACC2 13:1 (the F/C 6/4 of the section's first downbeat) and 19:3 (alto G-flat 4, the seventh of A-flat7,
%        prepared at 19:2.5) come from the skeleton. There is no new ACC2: the 16:3 retardation is tied.
%   The BLUEPRINT's DIR 13:3 does not occur (check.py): the soprano's leap F5-C5 comes at 13:2.5 over A2, and at
%        13:3 it re-strikes C5 (oblique motion) as the bass lands on F2.
% Spec exception (declared): at 16:3.5 the soprano's G-flat 5 doubles CS2's G-flat 4 at the octave for one weak
%   eighth, as the retardation's resolution. G-flat 5 on beat 3 (an earlier version) doubled CS2 for a whole
%   strong beat. The other notes the descant could take there are worse: D-flat 5 would make octaves with the
%   bass into 16:4 (D-flat-C), B-flat 5 would double the answer's B-flat 3.
% Harmony labels that now differ from BLUEPRINT section 6 (for the blueprint owner):
%   14:4.5 is V with a flat ninth (C E G D-flat), not vii dim 6.
%   16:3 is the N6/4 with the soprano's F as a 7-8 retardation; the soprano's G-flat arrives at 16:3.5.
%   17:4 is V7 complete; 17:4.5 is vii half-dim 7 over E2 with the passing D. The blueprint has "17:4 V7 with
%   passing D".
%   19:1 is E-flat minor with a double suspension (the tenor's F as a 9th, the alto's D-flat as a 7th),
%   resolving to 8 and 6 at 19:2 (E-flat 2 E-flat 3 C5 G-flat 5); the alto's G-flat 4 at 19:2.5 is the third.
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
%   (c) BLUEPRINT section 6 and the SK_final flag list name DIR 13:3; it no longer occurs (see Flags).
% NOT YET APPLIED (for the owners of suspensions.py and piano.ly; review round 1, findings 1 and 3):
%   suspensions.py: apply the tests the composers ran by hand. (1) Reject a re-struck preparation (today a
%     same-pitch note ending at t counts as a preparation; that is how 17:1 A is counted). (2) Require the held
%     note to be dissonant with the lowest sounding voice at t, not only with the attacking agent. (3) Require
%     the dissonance to begin at t: the held note is consonant with the bass immediately before t. With these
%     tests, this section counts 5 (18:1 T, 18:3 T, 19:1 A, 19:1 T, 19:3 T).
%   piano.ly: at 13:4, 16:1 and 16:4 (and 45:3 in section 5) the notes struck together fit no two-hand split.
%     13:4: C2 with the tenor's F3 while the right hand holds C5 (left hand 17 semitones; right hand C5-F3
%     19). 16:1: D-flat 2 B-flat 3 B-flat 4 F5 (left hand 21, right hand F5-B-flat 3 19). 16:4: C2 A-flat 3
%     A-flat 4 F5 (left hand 20, right hand F5-A-flat 3 21). Print them spread, bass first as an anticipation
%     (no note change), and catch the bass with the sostenuto: C2 at 13:4 (lift at 14:1), D-flat 2 at 16:1,
%     changed to C2 at 16:4 (lift at 17:1); and E-flat 2 at 19:2 (lift at 19:3). Tested on copies of piano.ly
%     with the assembled score in LilyPond 2.26: no warnings; the spread lines join across the staves at 16:1,
%     16:4 and 45:3.
%       spreadUpper = { s1*15 s2.\arpeggio s4\arpeggio | s1*28 s2 s4\arpeggio }
%       spreadLower = { s1*12 s2. s4\arpeggio | s1*2 | s2.\arpeggio s4\arpeggio | s1*28 s2 s4\arpeggio }
%       sostLower = { s1*12 s2. s4\sostenutoOn | s1\sostenutoOff | s1 |
%         s2.\sostenutoOn s4\sostenutoOff\sostenutoOn | s1\sostenutoOff | s1 | s4 s4\sostenutoOn s2\sostenutoOff }
%       (with the default mixed style the 19:2-19:3 catch prints as text only; \set Staff.pedalSostenutoStyle =
%       #'bracket at the start of sostLower draws all three catches as brackets, also tested without warnings)
%       \new PianoStaff \with { connectArpeggios = ##t } << ...
%         \new Voice = "soprano" << { \voiceOne \soprano } \spreadUpper >>   (the alto likewise, \voiceTwo)
%         \new Voice = "tenor" << { \voiceOne \tenor } \spreadLower >>
%         \new Voice = "bass" << { \voiceTwo \bass } \spreadLower \sostLower >>
% Idiom, piano (S+A right hand, T+B left):
%   13:3: roll or split the alto's A3 and the soprano's C5 (a minor tenth in the right hand; F2-A3 is too wide
%     for the left).
%   13:4, 16:1, 16:4: spread, bass first, with the sostenuto as above, so the left hand takes the tenor dry: the
%     4-3 at 13:4.5 and the tenor's B-flat 3 and A-flat 3-F3 under CS2's eighths stay clean. The sostenuto
%     catches every key that is down, and every key if the damper pedal is down: press it with the damper up,
%     after the bass is struck and before the tenor (at 13:4 the left hand lets go of the tenor's F3, strikes
%     C2, catches it, then re-strikes F3; at 16:1 the damper of 15:3 is lifted first).
%   19:1-19:2: the left hand holds the tied F3 and strikes E-flat 2 under it, a major ninth (14 semitones) held
%     for one beat, for large hands. Nothing can relieve it: the right hand's D-flat 5/G-flat 5 lie 20-25
%     semitones away, the damper from 18:4 would drag B-flat 2 into E-flat minor, and a sostenuto pressed at
%     19:1 would catch F3 and let it ring through its own resolution. It is the price of the tied 9-8 (the old
%     version had an octave, E-flat 2/E-flat 3, here). For small hands, re-strike F3 with the bass at 19:1: that
%     turns the 9-8 into the re-struck kind the review rejects, so it is a performance fallback only.
%   19:2: after the 9-8 has resolved (E-flat 2 E-flat 3 C5 G-flat 5, nothing left to resolve), catch E-flat 2 with the
%     sostenuto (lift at 19:3), so the left hand can take B-flat 3 and the 9-8 at 19:3.5 stays clean.
%   Damper pedal on one harmony at a time: 15:3-16:1 (C minor 7 over E-flat 2; the right hand holds), and
%     17:3-17:4.5 (C7, all chord tones), changed at 17:4.5.
%   The left hand then holds G3 over E2 (a minor tenth) and F2 (a ninth).
%   19:4: roll the A-flat 2-C4 tenth.
% Quartet: violin II from A3 (13:1), as the blueprint states; C2 is the cello's open string; no other problems.
soprano = \absolute {
  % 13
  f''4. c''8 c''2~ | c''4 ees''2 des''8 c''8~ | c''4 d''4 ees''2 | f''2~ f''8 ges''8 f''4 |
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
  g4. e8 c4 g4~ | g8 f8 aes4~ aes8 ges8 f4~ | f4 ees8 bes8~ bes8 aes8 c'4 |
}
bass = \absolute {
  % 13
  c4. a,8 f,4 c,4 | aes,2. g,4 | f,4 e,4 ees,2 | des,2. c,4 |
  % 17
  e,4. g,8 c,4. e,8 | f,2 bes,2 | ees,2 aes,2 |
}
