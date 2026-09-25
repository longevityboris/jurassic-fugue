\version "2.24.0"
% bars 30-34
% Section 4: Arioso dolente and the German-sixth pivot. S2 (soprano, locked) over pulsing eighths.
% Composed from design/final-lab/sections/sec04_arioso.ly; LOCKED/KEEP notes and all boundary entries unchanged.
%
% What the free voices do (all inside the pulse; section 4 is exempt from "no chordal padding"):
% * 30: the inner voices mirror S2's falling arpeggio C-A-F: alto A3-C4 against the soprano's C5-A4
%   (voice exchange at 30:2.5), tenor F3-A3 against the soprano's A4-F4 (30:3); soprano and tenor swap
%   D-flat and B-flat at 30:4 (i6/4 over the F pedal).
% * 30:4.5-32:1 tenor: CS1's chromatic core at its own pitch, one note a beat (D-flat C B-flat A A-flat
%   G-flat): the lament accompanies S2 as it accompanied S1 in the exposition. Its A at 31:3 makes A dim7
%   over E-flat with the same outer notes as the Climax I chord (29:1), recalled pp.
% * alto: the head neighbour and its mirror around F (F E-flat G-flat F), twice: 31:1 F held over the
%   bass E-flat (9-8) and 32:3 G-flat held over the bass F (b9-8). With the kept 7-6 (32:1) and 4-3 (tenor
%   32:3-33:3) the dominant becomes a chain of resolutions: b9-8 (32:3.5), b6-5 (soprano, 32:4.5), 8-7 (the
%   seventh E-flat enters by step, 33:1), 4-3 (33:3). The alto then holds E-flat, the German sixth's D-sharp,
%   and resolves it to E (34:1); its last-beat F-E (34:4) is the inversion's neighbour, heard just before
%   the bass states it at 35.
% Prepared suspensions (suspensions.py): 31:1 alto 9-8, 32:1 alto 7-6 (kept), 32:3 alto 9-8 (b9 over V),
%   32:3 tenor 4-3 (kept): 4 on strong beats, 2 of them new.
% Flags (check.py/strict.py, bars 29-35): no new D4?, DIR, MEL, XREL, ACC or ACC2. Kept from the skeleton:
%   MEL 32:1 bass D-G-flat (the lament's diminished fourth); XREL 33:4 and 33:4.5 alto E-flat then bass E
%   (the enharmonic pivot itself). ACC2 in the window: 6, all the skeleton's (it had 7; 32:3 alto E-flat
%   over F is gone). Spelled dissonances check.py cannot see, all intended: 31:3 tenor A3 / alto G-flat4
%   (inside A dim7), 32:3 alto G-flat4 over bass F2 (the b9 suspension), 34:1 tenor G-sharp3 / soprano C5
%   (the pivot's augmented triad, skeleton), 34:4 tenor G-sharp3 / alto F4 (upper neighbour, weak eighth).
soprano = \absolute {
  % 30
  c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1 |
  % 34
  c''2 b'2 |
}
alto = \absolute {
  % 30
  a8 a8 a8 c'8 c'8 c'8 f'8 f'8 ~ | f'8 f'8 ees'8 ges'8 ges'8 ges'8 f'4 | f'8 f'8 ees'8 ges'8 ges'8 f'8 f'8 f'8 | ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 |
  % 34
  e'8 e'8 e'8 e'8 e'8 e'8 f'8 e'8 |
}
tenor = \absolute {
  % 30
  f8 f8 f8 f8 a8 a8 bes8 des'8 | c'8 c'8 bes8 bes8 a8 a8 aes8 aes8 | ges8 ges8 bes8 bes8 bes8 bes8 bes8 bes8 | bes8 bes8 bes8 bes8 a8 a8 a8 a8 |
  % 34
  gis8 gis8 a8 a8 gis8 gis8 gis8 gis8 |
}
bass = \absolute {
  % 30
  f,1 | ees,2. d,4 | ges,2 f,2 | f,1 |
  % 34
  e,1 |
}
