\version "2.24.0"
% bars 35-45
% Section 5: Fuga inversa, with S2 answered and inverted against the locked S1 inversions.
% All S1, CS and KEEP spans, eleven-bar length, and complete first/last beats are unchanged.
%
% S2 entries (only the tenor's previously free spans have new notes):
%   T 35:2-36:4: tonal answer a fourth below the reference C5, on G4, in F major,
%     in 1:2 diminution. G-E-C retains the head; the fourth attack is G rather than
%     A, a tonal adjustment avoiding an unresolved fourth above the locked E3.
%     The major-mode third is A in the descending tail (36:2.75 and 36:3).
%     At 36:1.75 the weak F resolves upward through an added G32 before B-flat;
%     B-flat then falls to A and G. The final held note is curtailed for a beat
%     of silence before the locked E-minor S1 inversion on B3 at 37:1. This also
%     avoids completing E minor 7 beneath the alto's fixed D-E. Bar 35:1 remains solo.
%     The full S2 pitch sequence is present with those adjustments; kapell's
%     interval-only matcher recognizes 8/11 collapsed notes, stopping at the ornament.
%   T 42:2.5-43:4.5: tonal inversion of S2 on E4 in A minor, in adjusted 1:2
%     diminution: E-G-B-D-F-E-B-F-C-D-D-E. This is the diatonic mirror of the
%     A-natural-minor form about the midpoint C4/D4; G stays natural.
%     The G is lengthened to put B over the bass D at 42:4. D and F follow at
%     42:4.5 and 42:4.75. E anticipates the bar line at 42:4.875 and is tied,
%     so the soprano's F-E neighbour resolves above a stationary E, without
%     parallel octaves. The tail's C arrives weakly at 43:2.875 and rises to D
%     as the bass raises F to F-sharp; E then passes upwards into F-sharp at
%     43:4.5. The final E is shortened. kapell recognizes all 11 collapsed notes.
%     The late F-sharp is consonantly prepared over F-sharp in the bass, held
%     over G-sharp at 44:1, and resolves to E at 44:2: the existing 7-6 survives.
%     The former G-F-sharp 9-8 at 43:3 is replaced by the inverted S2 tail.
%   These are successive treatments, not an S2 stretto: the locks leave no two
%     simultaneous four-bar windows for proposal-4's original-speed combination.
%
% The remaining free counterpoint is retained:
%   S 39:1-2 F-E-F in diminution; B 40 B-C-sharp-B-A-sharp-B-G drives the static
%     upper parts, then E at 41:1; A 41 C-B-A-G-sharp-A completes the A-minor
%     cadence. T 41:4 C and 42:1 A still exchange with the bass A-C, filling i6.
%   T 44 F-sharp-E-F-E restores the seventh of vii dim 7 and its tonic resolution;
%     A 44:4 C still resolves the diminished seventh's D and leads into KEEP A4.
%
% Review notes:
%   splice_check: PASS; no new parallels, beat-parallels, unjustified dissonances,
%     unisons or CLASH. Strict accented counts remain acc 0, acc2 3 in 34-46.
%   The inversion's B3-F4 at 43:2.5 is a diminished-fifth leap; it turns inward
%     to C4, then rises by step. F4 leaves before the bass's F-sharp at 43:3:
%     strict reports that successive cross relation, not a simultaneous clash.
%   The tenor crosses above the locked low alto at 36 and again from 42:2.5;
%     the two subjects need distinct colours there. No instrument/plan files are
%     changed in this section-only revision. All four voices remain in range.
%   Existing skeleton warnings remain: DIR 37:2.5; D4? 42:4.5 and 43:4.5;
%     ACC2 37:1 and the cadential 6/4 at 41:1 (including its upper A-C exchange).
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
  r4 g'8. e'16 c'8 g'16 f'16 g'4 ~ | g'8 c''16 f'32 g'32 bes'8. a'16 a'8. g'16 r4 | b2. b8 c'8 | b2. b8 c'8 |
  % 39
  b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4 c'4 | a4. e'8. g'8. b'8 d'16 f'32 e'32 ~ |
  % 43
  e'4 b8 f'16. c'32 d'16 d'16 e'4 fis'8 ~ | fis'4 e'4 f'4 e'4 | a4. a8 c'4 b4 |
}
bass = \absolute {
  % 35
  e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 |
  % 39
  d4. f8 a,4 b,4 | b,8 cis8 b,8 ais,8 b,4 g,4 | e2. a,4 | c2. d4 |
  % 43
  e4 f4 fis2 | gis2. a4 | f4. d8 a,4 e,4 |
}
