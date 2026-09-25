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
%   tied into 50:1 (4-3 over F2): at 50:2 its resolution, A5 (or A-flat 5), is a seventh against S1's B-flat 3,
%   which is still held until 50:2.5, and A5 is also a tritone over S2's E-flat 5. The line also sits a fourth
%   above S2's peak F5, doubles S2's B-flat 4 at 49:4.5 and takes the Climax-II register early (B-flat 5 is the
%   fff note of 53:1).
% * 50:2, soprano g-flat''4 (the only new note): the pedal's upper neighbour (the inversion's G-flat, bass 49:4)
%   taken up by the soprano and resolved onto the first diminution head: G-flat F | F E-flat = the mirror's
%   upper neighbour and the subject's lower neighbour around one F, as Climax II begins. It moves in the one
%   rhythmic gap of bar 50 (alto and tenor hold 50:1-50:2.5) and holds while they move. 50:2: the G-flat enters
%   from rest as a struck minor ninth over F2 (check.py S:APP); with B-flat 3 and E-flat 5 it makes E-flat minor
%   (iv) over the F pedal (pedal licence). 50:2.5: F2 C4 Db5 Gb5 = the 50:3 chord (V with b6), anticipated by S1
%   and S2 under the held G-flat; the G-flat is a d5 over S1's C and a b9 over the pedal, and resolves to F at
%   50:3 (an upper-neighbour appoggiatura licensed by the pedal, not a counted suspension). Soprano stays a third
%   or more above S2.
%   Judgement call, kept: the G-flat sounds head 2's first pitch (51:1) a bar early, the head at 50:3 is heard as a
%   resolution rather than an attack out of silence, and S2's E-flat 5-D-flat 5 step (50:2.5) is covered from
%   above for one beat. No other upbeat pitch fits: against F2, B-flat 3 and E-flat 5 (50:1-50:2.5) no pitch class
%   is consonant with all three; those dissonant with the pedal alone are G-flat, G and B-flat (a fourth over the
%   bass), and G would bring the bright raised sixth (E-flat major) and a cross relation with the pedal's G-flat 2,
%   B-flat 5 the Climax-II register. The only alternative is the starter's r2 at 50:1-50:3. Performance: 50:2 lies
%   outside the soprano's subject role (from 50:3), so perform.py plays it at free level (-4, the head +9); no
%   accent.
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
