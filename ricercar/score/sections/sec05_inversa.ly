\version "2.24.0"
% bars 35-45
% Section 5: Fuga inversa: three inverted entries, A minor established with a cadence, deceptive link to F.
% Composed from the verified starter (design/final-lab/sections/sec05_inversa.ly); LOCKED, CS and KEEP spans unchanged.
%
% What the free voices do:
%   35, 36     S/A/T stay silent in 35 (the inversion alone, rule 6); the tenor rests in 36 so its stretto entry is fresh.
%   S 39:1-2   f'' e'' f'' then the KEEP e'': the subject's semitone neighbour (F E F) in diminution turning into the
%              inversion's sigh F-E as root-position A minor arrives (39:3). Moves in the gap 39:1.5-2, holds when the
%              others move at 39:2.5. (d'' at 39:1 would make octaves C-D with the bass on successive beats.)
%   B 40       B A# B: the head neighbour a semitone above the subject's own B-flat A B-flat, under V of E, where the
%              three upper voices hold.
%   A 41       c''4. a'8 gis'4 a'4: voice exchange with the tenor's A-C (41:2.5), no hollow A-E at 41:2; the leading
%              tone resolves and i is complete at 41:4 (it was A2 + E5 alone).
%   T 41:4-44  c' completes i at 41:4; rests through 42 (the third entry in three voices, rule 6); re-enters at 43:1 on
%              g' above the alto's low CS2 inv. (licensed by the blueprint where the alto lies below A4), filling the
%              hollow C/E into a complete III6. The subject's head in its own rhythm (G2. then the semitone below),
%              made into a suspension chain over the rising lament in the bass: 9-8 at 43:3 (G over F#), 7-6 at 44:1
%              (F# over G#) -> V6 complete at 44:2; then the inversion's neighbour E-F-E in quarters: F = seventh of
%              vii dim 7 (44:3, completed by the alto's D), resolving to E in the complete i (44:4); then the KEEP A.
%   A 44:4     landing kept on c' (the vii dim 7's D resolves down; the rising sixth into the KEEP a' is CS1's sigh).
%
% Checker notes (none new except the crossings):
%   CROS 43:1-44:4.5  tenor above the alto (the alto's CS2 inv. lies A3-D4 here): piano right hand takes S+T, left
%                     hand A+B; in the quartet the viola sits above violin II for two bars.
%   HOL 43:4.5 (weak eighth) the inversion's b' leaps in while the tenor holds the prepared F# of the 44:1 suspension.
%   Skeleton flags kept: DIR 37:2.5; D4? 42:4.5, 43:4.5; strict ACC2 37:1, ACC 41:1 (cadential 6/4).
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
  b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4 c'4 | r1 |
  % 43
  g'2. fis'4 ~ | fis'4 e'4 f'4 e'4 | a4. a8 c'4 b4 |
}
bass = \absolute {
  % 35
  e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 |
  % 39
  d4. f8 a,4 b,4 | b,4. ais,8 b,4 e4 ~ | e2. a,4 | c2. d4 |
  % 43
  e4 f4 fis2 | gis2. a4 | f4. d8 a,4 e,4 |
}
