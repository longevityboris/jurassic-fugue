\version "2.24.0"
% bars 35-45
% Section 5: Fuga inversa: three inverted entries, A minor established with a cadence, deceptive link to F.
% Composed from the verified starter (design/final-lab/sections/sec05_inversa.ly); LOCKED, CS and KEEP spans unchanged.
%
% What the free voices do:
%   35, 36     S/A/T stay silent in 35 (the inversion alone: rule 6 names 35 a solo opening); the tenor rests in 36 so
%              its stretto entry at 37 is fresh.
%   S 39:1-2   f'' e'' f'' then the KEEP e'': the subject's semitone neighbour (F E F) in diminution, turning into the
%              inversion's sigh F-E as root-position A minor arrives (39:3). It moves in the gap 39:1.5-2 and holds when
%              the others move at 39:2.5. (d'' at 39:1 would give octaves C-D with the bass on successive beats; b'
%              parallel octaves with the tenor; f'' is the only consonant choice.)
%   B 40       b,8 cis8 b,8 ais,8 b,4 under V of E: bar 40 is the accelerando's one bar where S, A and T all hold (KEEP
%              and LOCKED), so the free bass carries the motor: CS2 inv.'s head shape (x x+1 x x-1), ending on the
%              subject's neighbour figure x8 (x-1)8 x, B A# B = B-flat A B-flat a semitone higher. C#3 (40:1.5) is an
%              upper neighbour on a weak eighth (a compound second under D#5, a fourth under both F#s). E3 kept for the
%              cadence (E2 is saved for 45:4).
%   A 41       c''4 b'8 a'8 gis'4 a'4: over the bass E the line sings 6-5-4-3 (C B A G#), the cadential 6/4 resolved in
%              one voice and the lament's stepwise descent in miniature. The passing B4 gives beat 2 an attack (E3 A3
%              B4 E5: a fifth over the bass, a ninth over the 6/4's A3); the voice exchange with the tenor's A-C at
%              41:2.5 stays (no hollow A-E), the leading tone resolves, and i is complete at 41:4. 41:3 stays E + G#
%              (the alto is the only free voice there and must carry the third).
%   T 41:4-44  c' completes i at 41:4; silent through 42 (the third entry's first bar in three voices, rule 6); re-enters
%              at 43:1 on g', the one note missing from C over E (E3 C4 G4 E5), a full beat of consonant preparation. It
%              catches the G4 the alto leaves by leap (42:4.5 -> C4), so the G carries across the bar line in another
%              voice. Then the lament in its original, falling direction, G F# E, against its own inversion rising in
%              the bass (E F F# G# A): a mirror wedge, set as a suspension chain over the rising bass:
%                43:3 9-8, a change-of-bass suspension: G held over F (43:2, under the soprano's 7-6, a 9/7 double
%                     suspension over the lament's F) and still a ninth when the bass rises to F# (43:3); resolves to
%                     F# at 43:4. Two beats of dissonance on one of preparation, the price of the rising bass.
%                44:1 7-6 (F# over G# -> E: the rootless V6 gets its root at 44:2),
%              then the inversion's neighbour E-F-E in quarters: F = seventh of vii dim 7 (44:3, with the alto's D),
%              resolving to E in the complete i (44:4); then the KEEP A at 45:1. Tenor and alto sound thirds on three
%              attacks (E-F-E over C-D-C at 44:2.5, 44:3, 44:4, the last held to 45:1): the vii dim 7's fifth and
%              seventh resolving together, two parallel moves, then the leap apart at 45:1.
%   A 44:4     landing kept on c': the vii dim 7's D resolves down; the rising sixth into the KEEP a' is CS1's sigh.
%
% Checker notes: no new D4?, DIR, MEL, XREL or ACC/ACC2 (strict.py counts in 34-46 equal the skeleton's).
%   CROS 43:1-44:4.5  tenor above the alto (the alto's CS2 inv. lies A3-D4 here; the tenor G4-E4). It uncrosses at
%                     45:1 by leaping past the alto into the KEEP cadence chord (tenor E4 -> A3, alto C4 -> A4); the
%                     move is forced: 45:1 is KEEP in both voices, and no tenor eighth at 44:4.5 that would shorten the
%                     leap (D4, C4, B3, A3) avoids a second or a unison against the alto's held C4 or the bass's A3.
%   Piano: 42:1-2.5 alto in RH (E4/F4 against the bass's C3 is out of LH reach), 42:3-4 in LH (C4 D4 B3 over C3/D3),
%                     its G4 at 42:4.5 in RH; 43:1-44:4.5 RH S+T, LH A+B; from 45:1 back to RH S+A, LH T+B.
%   Quartet: violin II's CS2 inv. 'sul G, marcato' and the viola 'dolce, sotto voce' for 43:1-44:4 (the free viola
%                     lies above the countersubject; do not swap the two instruments: that would split the alto's
%                     44:4 c' -> 45:1 a' sigh). Violin II re-attacks the A4 at 45:1 clearly so the lines re-sort.
%                     For plan.json's owner: keep the tenor at the free level with no long-note swell 43:1-44:4
%                     (a tenor voice override slightly below the hairpin, rejoining it at 45:1), or raise the alto's
%                     cs level 42:1-44:4.
%   HOL 43:4.5 (weak eighth): S B4, A B3, B F#3 are all skeleton notes and the tenor must hold the F# that prepares
%                     the 44:1 7-6 (a re-struck preparation would also need F# there); A4 instead would put a HOL on
%                     the strong beat 44:2; D4 is a chord tone of G# dim and makes no suspension. Kept. The F#4 doubles
%                     the bass's raised sixth at 43:4-43:4.5 and the two leave it in opposite directions (tenor F#-E,
%                     bass F#-G#), as melodic minor allows.
% Judgement calls: (1) soprano 35 stays a full rest although the section list calls it free (rule 6 and the section
%   map: the inversion alone). (2) The tenor re-enters at 43:1, a bar before the blueprint's preferred 44: the register
%   licence holds there (alto at most D4 in 43-44), and the entry buys the 9-8 / 7-6 chain; the third entry is in three
%   voices for its whole first bar with the countersubjects (42), as rule 6's "unless a composer finds room" allows.
%   Skeleton flags unchanged: DIR 37:2.5; D4? 42:4.5 (the skeleton's passing G7 over D, three voices), 43:4.5;
%   strict ACC2 37:1, ACC 41:1 (the cadential 6/4).
% Suspensions (suspensions.py on the section spliced into SK_final): 2 new on strong beats (43:3, 44:1);
% section total 2 strong + 2 weak-beat (37:2 bass 2-3 and 43:2 soprano 7-6, both already in the skeleton).
soprano = \absolute {
  % 35
  r1 | e''8 f''8 e''8 d''8 c''8 d''8 b'8 g''8 | c''4 d''8 a'8 ~ a'4 b'4 | b'8 a'8 b'8 c''8 d''4 c''4 |
  % 39
  f''8 e''8 f''4 e''4 d''4 | dis''2. r4 | e''2. e''8 f''8 | e''2. e''8 f''8 |
  % 43
  e''4. d''8 d''4. b'8 | b'2. c''8 e''8 | d''4. f''8 a''4 r4 |
}
alto = \absolute {
  % 35
  r2. a'4 | c'2. d'4 | e'4 f'4 fis'2 | gis'2. a'4 |
  % 39
  f'4. d'8 c'4 b4 | fis'2. e'4 | c''4 b'8 a'8 gis'4 a'4 | e'8 f'8 e'8 d'8 c'8 d'8 b8 g'8 |
  % 43
  c'4 d'8 a8 ~ a4 b4 | b8 a8 b8 c'8 d'4 c'4 | a'4. f'8 e'4 gis'4 |
}
tenor = \absolute {
  % 35
  r1 | r1 | b2. b8 c'8 | b2. b8 c'8 |
  % 39
  b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4 c'4 | r1 |
  % 43
  g'2. fis'4 ~ | fis'4 e'4 f'4 e'4 | a4. a8 c'4 b4 |
}
bass = \absolute {
  % 35
  e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 |
  % 39
  d4. f8 a,4 b,4 | b,8 cis8 b,8 ais,8 b,4 e4 ~ | e2. a,4 | c2. d4 |
  % 43
  e4 f4 fis2 | gis2. a4 | f4. d8 a,4 e,4 |
}
