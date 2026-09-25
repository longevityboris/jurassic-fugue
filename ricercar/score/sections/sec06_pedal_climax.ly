\version "2.24.0"
% bars 46-54
% Section 6: Dominant pedal: both subjects over the augmented inversion, Climax II in three speeds, dominant hinge.
% Composed from the verified starter design/final-lab/sections/sec06_pedal_climax.ly (BLUEPRINT.md sections 6 and 7).
% Verify: python3 design/final-lab/splice_check.py score/sections/sec06_pedal_climax.ly  -> PASS
%
% FREE spans here: soprano 46:1-50:3, alto 46:1-48:1. Both stay silent, so the notes equal the starter's:
% * 46-47, alto and soprano: rule 6 ("keep the misterioso pedal 46-47 thin"), the section-6 FREE note ("46-47
%   stay two voices") and critique fix C2-M2 ("alto rests in 46-47; S2 and S1 enter together at 48:1"): the
%   pedal and the tenor's lament lead-in alone, so S2's entry at 48:1 is fresh.
% * 48:1-50:3, soprano: silent so S2 (alto) is the unbroken top line through the whole combination and the first
%   diminution head (F5, 50:3) enters from silence (fix C1-M2(a), whole-piece review findings 4, 6, 7). Round 1
%   of this section had A-flat 5 G5 at 49:2-49:3.5 and G-flat 5 at 50:2; both were removed because
%   (a) with S2's F5 at 49:4 the top line was heard as a descent A-flat G F, so S2's leap C5-F5 (the second
%   half's signature) sounded like the end of the soprano's line; (b) the G-flat 5 covered S2's E-flat 5-D-flat 5
%   step from a third above, anticipated head 2's G-flat a bar early and turned head 1 into the resolution of an
%   appoggiatura; (c) the Climax-II climb F, G-flat, A, C was heard as falling A-flat G G-flat F, then rising.
%   Also tested and rejected in round 1 (do not retry): F5 from 48:3 (hollow F/B-flat chord); F5 held 48:4-49:4
%   (brings back the removed inversion head, C2-M2, and re-strikes S2's peak); G-flat 5 tied 49:4.5-50:1 as a 9-8
%   over F2 (doubles the pedal's G-flat neighbour at three octaves, masks S2's leap F5-B-flat 4); B-flat 5 tied
%   49:4-50:1 as a 4-3 (its resolution A5 or A-flat 5 is a seventh against S1's held B-flat 3, and it takes the
%   fff register of 53:1 early). Against F2, B-flat 3 and E-flat 5 (50:1-50:2.5) no pitch is consonant with all
%   three.
% Flags: none new against the skeleton. Pre-existing: D4? 54:3 (V4/2 tritone); XREL 47:3-47:4 (tenor G3, then
%   the pedal's G-flat 2) and 53:2.75-53:3 (alto D5, then the bass's D-flat 2), both non-simultaneous.
% suspensions.py: the section adds none (0 strong-beat, 1 weak at 50:4, as in the skeleton).
% Density (attacks per bar, 46-54): the skeleton's (49: 9, 50: 13, 51: 12, 52: 12, 53: 13).
%
% For the design owner (KEEP / plan.json, not changeable in this file under splice_check):
% * Finding 1 (major), hinge 54: the V4/2's seventh E-flat never resolves to D at 55:1 (tenor E-flat 3 rises
%   to F3; D arrives from below in the alto), and alto A4-C4 with tenor C4-E-flat 3 leap a major sixth down
%   together at 54:3-54:4. Proposed and tested by the reviewer: alto bar 54 c''2 a'8 f'8 ees'4, tenor bar 54
%   a2 c'2 (E-flat 4 resolves to D4 in the alto; 54:4 stays A dim7 over G-flat, Gb2 C4 Eb4 A4; 55:1 boundary
%   unchanged). Needs piece.py/SK_final.ly, plan.json KEEP (alto 53:3-55:1, tenor 52:3-55:1) and the
%   section-6 boundary table (alto last note Eb4, tenor last note C4) changed together; then this file
%   takes the two bars.
% * Finding 3, Climax II 52:3-53:3: the tenor KEEP (B-flat, G) blocks the proposed eighth climb B-flat 3 C4 D4 E4
%   to G4 at 53:1 (held through the E dim7 at 53:3, then the KEEP C4 at 53:4), which would move the peak bar's
%   inner voice and close the 21-semitone hole G3-E5 in the fff chord; plan.json would reach fff at 52:3.
% * Finding 5: delete the 250 ms breath at 46:1 (piece.py) so E major resolves straight into F.
% * Finding 8: plan.json has no pedal in 46-54. Use a damper span {"at":"46:1","until":"55:1","every":"harmony"}
%   and listen for blur at the bass steps 50:4 (E-flat 2) and 51:4 (C2). Do NOT re-catch the sostenuto at
%   50:4 or 51:4 (round 1 suggested it): F5, D-flat 5 and C4 are still down at 50:4 and would ring into 51:1's
%   G-flat 5 and C5, A5 at 51:4 into 52:1's G5; the tenor lies 18-25 semitones above the bass on every
%   downbeat 51:4-54:1, so the left hand cannot hold both.
soprano = \absolute {
  % 46
  r1 | r1 | r1 | r1 |
  % 50
  r2 f''4. f''16 ees''16 | ges''4. ges''16 f''16 a''4. a''16 aes''16 | g''2 c'''4. c'''16 bes''16 | bes''2. a''4 |
  % 54
  f''4 ees''4 c''4 a'4 |
}
alto = \absolute {
  % 46
  r1 | r1 | c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 |
  % 50
  ees''4. des''8 des''4. c''8 | c''1 | e''4. e''16 dis''16 e''2 | e''4. e''16 d''16 e''4 f''4 |
  % 54
  c''2 a'4 c'4 |
}
tenor = \absolute {
  % 46
  bes2 a2 | aes2 g4 c'4 | bes2. bes8 a8 | bes2. bes8 a8 |
  % 50
  bes4. c'8 c'4. ees'8 | ees'2. des'8 bes8 | c'4. a8 bes2 | g2 g4 c'4 |
  % 54
  a2 c'4 ees4 |
}
bass = \absolute {
  % 46
  f,1 | f,2 f,4 ges,4 | f,1 | f,2 f,4 ges,4 |
  % 50
  f,2. ees,4 | ees,2. c,4 | c,1 | c,2 des,4 f,4 |
  % 54
  ees,2. ges,4 |
}
