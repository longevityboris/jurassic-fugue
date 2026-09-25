\version "2.24.0"
% bars 1-12
% Section 1: Exposition, entries 1-3. Composed from design/final-lab/sections/sec01_expo.ly.
% Verify: python3 design/final-lab/splice_check.py score/sections/sec01_expo.ly  (PASS)
%
% WHAT IS WRITABLE HERE. Everything is thematic or deliberately silent (BLUEPRINT sections 6 and 7):
% S 1:1-5:4 subject, 5:4-9:3 CS1 (answer level), 10:1-13:1 CS2; A 5:1-9:4 answer, 9:4-13:1 CS1;
% B 9:1-13:1 subject. The alto before 5:1, the bass before 9:1 and the whole tenor are FREE on the map
% but stay silent: rule 6 keeps the solo (1-4), the two-voice entry (5-8) and the three-voice entry
% (9-12) thin, and the boundary table has the tenor resting throughout. The only composed span is the
% soprano's CS1 landing and the free beat after it, 9:3-10:1.
%
% THE LANDING (soprano 9:3-10:1): skeleton  e''4. g''8 c''4 r4   ->   e''4. g''8 e''4 f''4
% * 9:3 E5 instead of C5. The skeleton landed the soprano on C5 an octave above the alto's C4 (the
%   answer's last note): a two-pitch-class sonority (C over B-flat) on a strong beat, reached by
%   similar motion. E5 gives the rootless C7 of 9:1 its third back: 9:3 is C E B-flat = V4/2 of V
%   (C7 over the bass subject's B-flat), with G heard at 9:2.5. Soprano and alto move in tenths
%   (9:2.5-9:3), not octaves.
% * The tail E-G-E turns back instead of falling to a cadence note, because the exposition must not
%   close here: the bass subject has just entered. It is the same landing shape the skeleton gives the
%   other CS1 landing (alto 13:1-13:3, A-C-A), so the two CS1 tails match.
% * 9:4 F5: the leading tone of F resolves in its own voice, arriving together with the alto's F3
%   (CS1's first note at subject level) and the bass's re-struck B-flat (contrary motion to the alto,
%   oblique to the bass). The E does not hang over the alto's entry note. At 9:4.5 the bass steps to A:
%   F5 A2 F3 = V6 of b-flat (three voices, fifth omitted, root doubled), so the bar reads
%   V4/2 of V -> V6 -> i (10:1) under the subject's opening neighbour B-flat A B-flat.
% * E-F is the inversion's own neighbour (the E-to-F hinge at 45:4-46:1 that returns the piece to
%   B-flat). The answer already sings it as its leading-tone neighbour (5:4.5-6:1, 6:4.5-7:1); here it
%   moves to the top voice and becomes the fugue's first cadential resolution.
% * ARTICULATION (intent only; nothing in the voices, rule 8). The skeleton breathed on 9:4 (quarter
%   rest). Here the soprano ends its long CS1 phrase on F, the note on which the answer entered at 5:1,
%   and CS2 starts a fifth lower on B-flat, the subject's note: the leap and the change from quarter
%   notes to running eighths mark the entrance, and CS2 is still the first eighth-note motion in the
%   upper voice. Play F5 legato, lift slightly before 10:1 (no written rest); CS2 enters at the same
%   level as the subject's neighbour below it, not louder.
%
% FLAGS (splice_check.py, strict.py -v, check.py on bars 1-13):
% * No new D4?, DIR, MEL, XREL, CLASH or unison.
% * UNI 5:3 soprano/alto: skeleton, documented in BLUEPRINT section 1 (S1 ends on F where the answer
%   enters on F).
% * DIR 13:3 S/B: belongs to section 2's descant (the join bar), BLUEPRINT section 2.
% * ACC2 9:1 soprano E5 / bass B-flat 2 (inherited, locked notes): the tritone of the rootless C7, bass
%   B-flat = the chord seventh, resolving to A at 9:4.5 (chord-seventh licence).
% * No new ACC or ACC2. check.py's informational DIS list gains one line, 9:3 S/B tritone E5/B-flat 2
%   [S:APP]: E5 is a chord tone (the third of C7), the bass B-flat its seventh, held and re-struck,
%   resolving to A at 9:4.5 (unjustified 0).
%
% SUSPENSIONS (suspensions.py): prepared 0, weak-beat 2 (6:4 alto F4->E4, 2-3 against the soprano's G5;
% 10:4 bass B-flat 2->A2, 2-3 against the alto's C4), both from the locked counterpoint. No strong-beat
% suspension can be written in this section: the one free strong beat (9:3) could only hold the locked
% g''8 (a tie would change CS1's note length, and G5 is a consonant fifth over the alto's C4 anyway).
%
% HARMONY LABELS that change against BLUEPRINT section 1 (grid.py): 9:3 C over B-flat -> C7 over B-flat
% (C E B-flat, V4/2 of V); 9:4 open fifth B-flat/F (F doubled); 9:4.5 F over A (V6). Everything else
% as in the blueprint.
soprano = \absolute {
  % 1
  bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 |
  % 5
  c''4. a'8 f'4 c''4 | aes''2. g''4 | f''4 e''4 ees''2 | des''2. c''4 |
  % 9
  e''4. g''8 e''4 f''4 | bes'8 a'8 bes'8 c''8 des''8 c''8 ees''8 ges'8 | des''4 c''8 f''8~ f''2 | ees''8 f''8 ees''8 des''8 ces''4 des''4 |
}
alto = \absolute {
  % 1
  r1 | r1 | r1 | r1 |
  % 5
  f'2. f'8 e'8 | f'2. f'8 e'8 | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f'8 |
  % 9
  g'4. e'8 c'4 f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4 |
}
tenor = \absolute {
  % 1
  r1 | r1 | r1 | r1 |
  % 5
  r1 | r1 | r1 | r1 |
  % 9
  r1 | r1 | r1 | r1 |
}
bass = \absolute {
  % 1
  r1 | r1 | r1 | r1 |
  % 5
  r1 | r1 | r1 | r1 |
  % 9
  bes,2. bes,8 a,8 | bes,2. bes,8 a,8 | bes,4. c8 c4. ees8 | ees2. des8 bes,8 |
}
