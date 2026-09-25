\version "2.24.0"
% bars 13-19
% Section 2: Entry 4 (tenor answer, bass the full lament to C2, alto CS2) and the Episode (cell b over the
% falling fifths F B-flat E-flat A-flat into D-flat). Composed from design/final-lab/sections/sec02_entry4_episode.ly.
%
% Soprano descant (13-17), free:
%   13  F4. C8 C4. G8: cell b's own shape (repeated note, then a leap) over the tenor's held entry note; C stays
%       on top while the tenor's F-E (4-3) resolves, and the leap up to G (13:4.5) prepares the suspension
%       (the skeleton's DIR 13:3 is gone).
%   14  the G is held over the lament's A-flat: 9-8 against the tenor's F (7-6 over the bass), then a stepwise
%       fall F E-flat D-flat C (half notes against the alto's CS2 eighths, contrary to its rise). Leap up a
%       fifth, then a stepwise fall of a fifth: CS1's sigh (rising sixth, falling line) in the descant.
%   15  C, then G over the V6 and a CS2-like turn G F E-flat into F (no E5 over the bass's E2: the doubled
%       leading tone and the skeleton's XREL 15:2.5 are gone).
%   16  F G-flat F: the mirror sigh, G-flat doubling the alto's root on the N6/4 by contrary motion.
%   17  C4. D8 E4 D4: cell-b rhythm again, under which the alto sings its b6-5 (A-flat G) over the V6; C7 at 17:3.
% Episode (18-19): the soprano's cell b as designed; the alto answers at the half bar (bes'4. des''8) and its
%   D-flat becomes a 7-6 over E-flat (19:1); the tenor carries a chain of suspensions under the imitation:
%   9-8 over F (18:1), 7-6 over B-flat (18:3), 9-8 over A-flat (19:3), stepping to C4 as the leader's leading tone.
%   The alto's B-flat (17:2.5) is prepared before the half cadence and resolves to A-flat at 18:1; the tenor's
%   A-flat G-flat F E-flat (18:2-19:1) is CS1's falling tetrachord.
% Strong-beat suspensions (suspensions.py): 14:1 S G-F, 17:1 A A-flat-G, 18:1 T G-F, 18:3 T A-flat-G-flat,
%   19:1 A D-flat-C, 19:3 T B-flat-A-flat (6). The tenor's weak-beat 7-6 at 14:4 is no longer counted: its
%   preparation at 14:1 now sounds against the soprano's suspended G.
% Flags:
%   XREL 14:1.5-14:2 (alto E4, CS2's rising lower neighbour, then the soprano's falling passing E-flat 5: the
%        two sevenths of f minor in contrary directions, never sounding together; each voice moves by step).
%   ACC2 13:1 (the F/C 6/4 of the section's first downbeat) and 19:3 (alto G-flat 4, the seventh of A-flat7)
%        are the skeleton's; no new ACC2.
% Idiom: piano, the soprano's G5 over the alto's F4-E4 at 14:1 is a ninth-tenth stretch for one eighth (or the
%   left hand takes the tenor's F3 with the bass). Quartet: violin II from A3 (13:1), as the blueprint states.
soprano = \absolute {
  % 13
  f''4. c''8 c''4. g''8~ | g''8 f''8 ees''2 des''4 | c''4. g''8~ g''8 f''8 ees''4 | f''2 ges''4 f''4 |
  % 17
  c''4. d''8 e''4 d''4 | c''4. des''8 des''4. f''8 | ges''4. f''8 f''4. ees''8 |
}
alto = \absolute {
  % 13
  a4. c'8 a4 r4 | f'8 e'8 f'8 g'8 aes'8 g'8 bes'8 des'8 | aes'4 g'8 c''8~ c''2 | bes'8 c''8 bes'8 aes'8 ges'4 aes'4 |
  % 17
  aes'4 g'8 bes'8~ bes'2 | aes'2 bes'4. des''8~ | des''4 c''8 bes'8 ges'2 |
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
  e,4. g,8 c,4 c4 | f,2 bes,2 | ees,2 aes,2 |
}
