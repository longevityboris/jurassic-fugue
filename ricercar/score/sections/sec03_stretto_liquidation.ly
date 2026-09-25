\version "2.24.0"
% bars 20-29
% Section 3: Stretto in the relative major (false dawn), liquidation, Climax I. Composed from the verified
% starter design/final-lab/sections/sec03_stretto_liquidation.ly; LOCKED, CS and KEEP spans unchanged.
%
% FREE ALTO 20-24:2 (the inner voice between the tenor leader and the soprano follower):
%   20-21  the neighbour cell x, x-1, x, x+1 (CS2's first four notes) on A-flat: Ab (Gb Ab) Bb. The Bb is
%          the mirror's upper neighbour held over the subject's lower one (tenor Db C Db): 6th over Db,
%          9th over the V at 20:4, then a 4-3 over the lament's F (21:1) resolving to Ab. Then CS1's
%          chromatic core Ab G Gb (21:3-21:4), a pre-echo of the lament's C-Cb in the bass at 22:2-22:3.
%   22     Bb held under the follower's entry, 7-6 over the lament's C-flat (22:3), rising Ab Cb into 23.
%   23     CS2's turn Db Eb Db Cb Db in eighths where the other three voices hold (Gb/Bb), no doubled bass.
%   24     the Db tied over the bar: 9th/7th against the lament's C and the tenor's Eb (24:1), resolving
%          to C; the kept Eb5 at 24:3.
% FREE TENOR 25-26:2: the mirror sigh Gb Ab Gb, then the line sinks Gb F Eb Db C Bb into the E dim7
%   (the lament's descent, the "sinks to F" of the blueprint), with a 7-6 over the bass F at 26:1.
% FREE BASS 24:3-26:3 and 20:1-20:4 unchanged (Eb N6, Gb, F, E, Eb: the chromatic fall into Climax I);
% FREE ALTO 25-26:2 holds the Neapolitan's doubled third under the soprano's C-flat (the tenor moves).
% Deliberately thin places kept: soprano silent 20:2-21:4; nothing added 26:3-29 (the liquidation).
%
% Prepared suspensions (suspensions.py): 21:1 A 4-3, 22:3 A 7-6, 24:1 A 7-6 (9-8 over the bass),
%   25:3 S 4-3 (skeleton), 26:1 T 7-6 = 5 on strong beats (skeleton: 1); weak 20:4, 21:4, 23:4 T/S kept.
% Flags: no new D4?, DIR, MEL, XREL or ACC2. The skeleton's D4? 24:1 (alto Gb4 over C3) is gone: the alto
%   now holds Db5 there as a suspension. strict ACC2 left in bars 19-30 are all thematic/kept notes:
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
  aes'4 ges'8 aes'8 bes'2 ~ | bes'4 aes'4. g'8 ges'4 | bes'2 ~ bes'4 aes'8 ces''8 | des''8 ees''8 des''8 ces''8 des''2 ~ |
  % 24
  des''4 c''4 ees''2 | ees''2. des''4 ~ | des''4 aes'4 g'2 ~ | g'2 bes'2 ~ |
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
  c4. ees8 aes,2 | ees2 ges,2 | f,2 e,2 ~ | e,1 ~ |
  % 28
  e,2. e,8 ees,8 | ees,1 |
}
