\version "2.24.0"
% bars 20-29
% Section 3: Stretto in the relative major (false dawn), liquidation, Climax I. Composed from the verified
% starter design/final-lab/sections/sec03_stretto_liquidation.ly; LOCKED, CS and KEEP spans unchanged,
% every boundary entry kept.
%
% FREE ALTO 20-24:2, the inner voice between the tenor leader (S1 in D-flat) and the soprano follower:
%   20-21  CS2's head cell x, x-1, x, x+1 on A-flat: Ab (Gb Ab) Bb. The Bb is the mirror's upper neighbour
%          held against the subject's lower one (tenor Db C Db): a 6th over Db, a 9th over the V at 20:4,
%          then a 4-3 over the lament's F at 21:1 resolving to Ab. Then CS1's chromatic core Ab G Gb
%          (21:3-21:4), a pre-echo of the lament's own C-Cb at 22:2-22:3; Gb gives ii7 and vii dim 6.
%          This replaces the skeleton's held G-flat at 20:3 (the C2-M3 "suspended fourth"): bar 20 still
%          moves I, neighbour (Gb, 20:2), I add6 (20:3), V with the tenor's 4-3 and the alto's 9th (20:4),
%          I6 with the alto's 4-3 (21:1), so the critique's point (bar 20 not static) stays answered.
%   22     Bb held under the follower's entry (the third of G-flat), 7-6 over the lament's C-flat at 22:3,
%          resolving on beat 4, then rising Ab Cb into 23.
%   23     the mirror of CS2's head, x x+1 x x-1 x (Db Eb Db Cb Db), in eighths where the other three voices
%          hold; it keeps Db/Eb on the beats so G-flat/B-flat never sounds with two pitch classes only.
%   24     that Db tied over the bar: 9-8 against the lament's C (7th against the tenor's Eb) at 24:1,
%          resolving to C; the kept Eb5 at 24:3 is the line's peak, with the soprano's C-flat 6.
%          Label change: 24:2.5 is now A-flat 6/4 over E-flat (the skeleton's A-flat7 had its seventh in
%          the alto's Gb4, which is gone); the held C moves to the bare A-flat fifth at 24:3 as before.
% FREE ALTO 25-26:2 holds the Neapolitan's doubled third (Eb5) under the soprano's C-flat while the tenor
%   moves, then falls Db Bb Ab into the kept G. Ab (not Db) at 26:1 so that the tenor's 7-6 has no
%   resolution note sounding above it.
% FREE TENOR 25-26:2: the mirror sigh Gb Ab Gb, then the line sinks Gb F Eb Db C Bb into the E dim7 (the
%   lament's descent; "sinks through F"), with a 7-6 over the bass F at 26:1 (Eb held from 25:3).
%   Keep "26:1 D-flat/F": D-flat/F arrives on the second eighth (26:1.5) as that 7-6's resolution
%   (26:1 itself is F Eb Ab Ab); 26:2 F minor kept.
% FREE BASS 24:3-26:3: kept as the skeleton's line on purpose (Eb under the N6, Gb under the soprano's 4-3,
%   then the chromatic fall Gb F E Eb into Climax I); the only change is the octave drop Eb3-Eb2 at 25:2,
%   which moves under the held C-flat 6 and reaches Gb2 by a rising third instead of a falling sixth.
%   FREE BASS 20:1-20:4 kept: the tonic pedal under the leader's entry.
% Deliberately thin places kept: soprano silent 20:2-21:4; nothing added 26:3-29 (the liquidation).
%
% Prepared suspensions (suspensions.py): 21:1 A 4-3, 22:3 A 7-6, 24:1 A 9-8/7-6, 25:3 S 4-3 (skeleton),
%   26:1 T 7-6 = 5 on strong beats in this section (skeleton: 1); weak-beat 20:4 T, 21:4 T, 23:4 S kept.
%   No resolution note sounds above a suspension (24:1 has the C in the bass: the 9-8 licence).
% Flags: no new D4?, DIR, MEL, XREL, CLASH or ACC2. The skeleton's D4? 24:1 (alto Gb4 over C3) and its
%   ACC 20:3 (alto Gb4 over Db2) are gone. strict ACC2 left in bars 19-30 are all thematic or kept notes:
%   19:3 (section 2), 22:1 and 24:1 (soprano S1 over the lament), 26:3 (E dim7 keep), 29:1 (A dim7 keep).
soprano = \absolute {
  % 20
  f''4 r2. | r1 | ges''2. ges''8 f''8 | ges''2. ges''8 f''8 |
  % 24
  ges''4. aes''8 aes''4. ces'''8 | ces'''2. bes''8 ges''8 | aes''4. f''8 des''4 r4 | r1 |
  % 28
  des''2. des''8 c''8 | c''1 |
}
alto = \absolute {
  % 20
  aes'4 ges'8 aes'8 bes'2 ~ | bes'4 aes'4. g'8 ges'4 | bes'2. aes'8 ces''8 | des''8 ees''8 des''8 ces''8 des''2 ~ |
  % 24
  des''4 c''4 ees''2 | ees''2. des''8 bes'8 | aes'2 g'2 ~ | g'2 bes'2 ~ |
  % 28
  bes'2. bes'8 a'8 | a'1 |
}
tenor = \absolute {
  % 20
  des'2. des'8 c'8 | des'2. des'8 c'8 | des'4. ees'8 ees'4. ges'8 | ges'2. f'8 des'8 |
  % 24
  ees'4. c'8 aes4 ces'4 | ges'8 aes'8 ges'8 f'8 ees'2 ~ | ees'8 des'8 c'4 bes2 | g1 ~ |
  % 28
  g2. g8 ges8 | ges1 |
}
bass = \absolute {
  % 20
  des,2. aes,4 | f2. ees4 | des4 c4 ces2 | bes,2. aes,4 |
  % 24
  c4. ees8 aes,2 | ees4 ees,4 ges,2 | f,2 e,2 ~ | e,1 ~ |
  % 28
  e,2. e,8 ees,8 | ees,1 |
}
