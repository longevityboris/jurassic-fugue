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
%   B 40       B A# B under V of E while the three upper voices hold: the head neighbour, a semitone above the
%              subject's own B-flat A B-flat. E3 kept for the cadence (E2 is saved for 45:4).
%   A 41       c''4. a'8 gis'4 a'4: voice exchange with the tenor's A-C at 41:2.5 (no hollow A-E at 41:2), the leading
%              tone resolves, and i is complete at 41:4 (it was A2 + E5 alone). 41:3 stays E + G# (only one free voice).
%   T 41:4-44  c' completes i at 41:4; silent 42:1-2 (the third entry begins in three voices, rule 6); re-enters at 42:3
%              with a' (the rising sixth c'-a' = CS1's sigh), completing i6, above the alto's low CS2 inv. (the blueprint's
%              licence: a line above the alto where it lies below A4). Then the lament in its original, falling
%              direction, A G F# E, against its own inversion rising in the bass (E F F# G# A): a mirror wedge, set as a
%              suspension chain over the rising bass:
%                43:1 4-3 (A over E -> G: A minor 6/4 -> C6, the hollow C/E filled),
%                43:3 9-8 (G over F# -> F#),
%                44:1 7-6 (F# over G# -> E: the rootless V6 gets its root at 44:2),
%              then the inversion's neighbour E-F-E in quarters: F = seventh of vii dim 7 (44:3, with the alto's D),
%              resolving to E in the complete i (44:4); then the KEEP A at 45:1.
%   A 44:4     landing kept on c': the vii dim 7's D resolves down; the rising sixth into the KEEP a' is CS1's sigh.
%
% Checker notes: no new D4?, DIR, MEL, XREL or ACC/ACC2 (strict.py counts in 34-46 equal the skeleton's).
%   CROS 42:3-44:4.5  tenor above the alto (the alto's CS2 inv. lies A3-G4 here; the tenor A4-E4). Piano: right hand
%                     S+T (with the alto's G4 at 42:4.5), left hand A+B; quartet: viola above violin II for two bars.
%   Weak-beat dissonances against the held a' (42:4 alto B3, 42:4.5 alto G4) are the CS2 inv.'s own leap figure
%                     under a prepared note (check.py: T:SUS); 42:4.5 becomes G9 over D (the passing G7 plus the held A).
%   HOL 43:4.5 (weak eighth): the inversion's b' leaps in while the tenor holds the F# that prepares the 44:1 7-6.
%   Skeleton flags unchanged: DIR 37:2.5; D4? 42:4.5, 43:4.5; strict ACC2 37:1, ACC 41:1 (the cadential 6/4).
% Suspensions (suspensions.py on the section spliced into SK_final): 3 new on strong beats (43:1, 43:3, 44:1);
% section total 3 strong + 2 weak-beat (37:2 bass 2-3 and 43:2 soprano 7-6, both already in the skeleton).
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
  f'4. d'8 c'4 b4 | fis'2. e'4 | c''4. a'8 gis'4 a'4 | e'8 f'8 e'8 d'8 c'8 d'8 b8 g'8 |
  % 43
  c'4 d'8 a8 ~ a4 b4 | b8 a8 b8 c'8 d'4 c'4 | a'4. f'8 e'4 gis'4 |
}
tenor = \absolute {
  % 35
  r1 | r1 | b2. b8 c'8 | b2. b8 c'8 |
  % 39
  b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4 c'4 | r2 a'2 ~ |
  % 43
  a'8 g'8 ~ g'2 fis'4 ~ | fis'4 e'4 f'4 e'4 | a4. a8 c'4 b4 |
}
bass = \absolute {
  % 35
  e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 |
  % 39
  d4. f8 a,4 b,4 | b,4. ais,8 b,4 e4 ~ | e2. a,4 | c2. d4 |
  % 43
  e4 f4 fis2 | gis2. a4 | f4. d8 a,4 e,4 |
}
