\version "2.24.0"
% bars 46-54
% Section 6: Dominant pedal: both subjects over the augmented inversion, Climax II in three speeds, dominant hinge.
% Composed from the verified starter design/final-lab/sections/sec06_pedal_climax.ly (BLUEPRINT.md sections 6 and 7).
% Verify: python3 design/final-lab/splice_check.py score/sections/sec06_pedal_climax.ly  -> PASS
%
% FREE spans here: soprano 46:1-50:3, alto 46:1-48:1. What was done with them, and why:
% * 46-47, alto and soprano: silent on purpose. Rule 6 ("keep the misterioso pedal 46-47 thin"), the section-6
%   FREE note ("46-47 stay two voices") and critique fix C2-M2 ("alto rests in 46-47; S2 and S1 enter together
%   at 48:1") all require the pedal and the tenor's lament lead-in alone, so that S2's entry at 48:1 is fresh.
% * 48:1-50:2, soprano: silent on purpose (fix C1-M2: S2 must be the top thematic voice). Tested alternatives:
%   over F2 and S1's held B-flat 3 only F5 is consonant above S2; F5 from 48:3 makes a hollow F/B-flat chord
%   (HOL at 48:3); F5 held 48:4-49:4 brings back the removed soprano inversion head (C2-M2) and makes S2's leap to
%   its peak F5 at 49:4 sound like a re-strike. The window can hold only two counted suspensions, both tested and
%   rejected: (a) G-flat 5 from 49:4.5 tied into 50:1 (9-8 over F2) doubles the pedal's G-flat neighbour at three
%   octaves while it sounds (49:4.5-50:1), accenting it, and its 9-8 only decorates octaves Gb2/Gb5 -> F2/F5 in the
%   outer voices; it enters the instant S2 leaves its peak F5, so F5-G-flat 5 is heard as one line and S2's leap
%   F5-B-flat 4 is lost; and its F5 at 50:2 states the head's pitch a beat before the head. (b) B-flat 5 from 49:4
%   tied into 50:1 (4-3 over F2) sits a fourth above S2's peak F5, doubles S2's B-flat 4 at the octave at 49:4.5,
%   resolves at 50:2 onto A-flat 5 (a seventh over the tenor's held B-flat 3), then leaps to F5, and takes the
%   Climax-II register (B-flat 5 is the fff note of 53:1) four bars early.
% * 50:2, soprano g-flat''4 (the only new note): the pedal's upper neighbour (the inversion's G-flat, bass 49:4)
%   taken up by the soprano and resolved onto the first diminution head: G-flat F | F E-flat = the mirror's
%   upper neighbour and the subject's lower neighbour around one F, as Climax II begins. It moves in the one
%   rhythmic gap of bar 50 (alto and tenor hold 50:1-50:2.5) and holds while they move. 50:2: B-flat 3, E-flat 5,
%   G-flat 5 = E-flat minor (iv) over the F pedal (pedal licence); 50:2.5: the held G-flat over S1's C and S2's
%   D-flat, resolving by step to F at 50:3 (b9-8 over the pedal). Soprano stays a third or more above S2.
% New flags against the skeleton: none (no new D4?, DIR, MEL, XREL, ACC, ACC2, HOL, unison or crossing).
% Pre-existing, unchanged: D4? 54:3 (V4/2 tritone), XREL 47:3-47:4 and 53:2.75-53:3 (non-simultaneous).
% suspensions.py: 0 strong-beat (the free window cannot hold one without the faults above), 1 weak (50:4, skeleton).
% Density: bar 50 now has 14 attacks (blueprint section 6 lists the skeleton's 13).
soprano = \absolute {
  % 46
  r1 | r1 | r1 | r1 |
  % 50
  r4 ges''4 f''4. f''16 ees''16 | ges''4. ges''16 f''16 a''4. a''16 aes''16 | g''2 c'''4. c'''16 bes''16 | bes''2. a''4 |
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
