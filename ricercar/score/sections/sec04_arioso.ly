\version "2.24.0"
% bars 30-34
% Section 4: Arioso dolente and the German-sixth pivot. S2 (soprano, locked) over pulsing eighths.
% Composed from design/final-lab/sections/sec04_arioso.ly; LOCKED/KEEP notes and all boundary entries unchanged.
%
% What the free voices do (all inside the pulse; section 4 is exempt from "no chordal padding"):
% * 30:2-30:4 bass: S2's head in stretto. C3 (30:2) A2 (30:3.5) F2 (30:4), dotted quarter, eighth, quarter:
%   the soprano's C5 A4 F4 one beat later and two octaves lower, like a continuo taking up the voice's
%   head in a Bach aria. It is the only imitation of S2 in the piece, and it can only be the head: bar 30
%   is the arioso's one bar with all three lower voices free, and the bass's KEEP E-flat at 31:1 stops it
%   after the third note (S2 goes on D-flat B-flat C). The head is the F-major arpeggio, so the bass only
%   arpeggiates the V it was holding (F C A F): V throughout 30:1-30:3.5 (6/4 at 30:2-30:3, 6/3 at 30:3.5),
%   i6/4 at 30:4 as before.
%   What it is not: an answer. S2 is still never answered in full, inverted or combined in the second
%   invertible position with S1; that is a blueprint question (see "For the design owner").
% * 30: the inner voices mirror S2's falling arpeggio C-A-F: alto A3-C4 against the soprano's C5-A4
%   (voice exchange at 30:2.5), tenor F3-A3 against the soprano's A4-F4 (30:3); soprano and tenor swap
%   D-flat and B-flat at 30:4 (i6/4 over F). The alto takes D-flat4 at 30:4 (i6/4 with its third doubled
%   at the octave, one eighth) and F4 only at 30:4.5: an alto F4 on 30:4 would make octaves with the bass
%   on successive beats (C4/C3 at 30:3, F4/F2 at 30:4) now that the bass moves.
% * 30:4.5-32:1 tenor: CS1's chromatic core at its own pitch, one note a beat (D-flat C B-flat A A-flat
%   G-flat): the lament accompanies S2 as it accompanied S1 in the exposition. Over the held E-flat bass it
%   makes ii dim 6 (31:1), ii half-dim 6/5 (31:2, its B-flat a passing chord seventh), vii dim 4/3 = A dim7
%   over E-flat (31:3: the Climax I chord of 29:1 with the same outer notes, recalled pp) and, with A-flat,
%   the rootless V7/iv (31:4).
% * alto: the tonal mirror's upper neighbour F G-flat F at bar scale. F4 (30:4.5) rises to G-flat4 on the
%   downbeat of 31, in contrary motion to the bass F-E-flat, completing ii dim 6; it holds G-flat as the
%   common tone of the three chords of bar 31, so the alto stands still exactly where the tenor's lament
%   moves every beat (rule 5: held notes where the other line moves). Back to the kept F (31:4), which
%   becomes the arioso's peak, the 7-6 over G-flat (32:1); its E-flat (32:2) stays as the seventh of V,
%   prepared as a common tone of the iv6, and is re-read as the German sixth's D-sharp rising to E (34:1).
%   33:2.5: the mirror sigh at eighth scale (E-flat F E-flat), F B-flat C over F2 for one eighth, so that at
%   33:3 the V7's third (tenor A) and seventh (alto E-flat) are struck together. The alto's last-beat F-E
%   (34:4) is the inversion's neighbour, heard just before the bass states it at 35.
% * Bar 32's alto is the skeleton's. An earlier version tied F4 from 30:4 into 31:1 (9-8 over E-flat)
%   and set G-flat4 at 32:2.5-32:3 (b9-8 over F). Both were the bass's own step shadowed two octaves up and
%   delayed by the syncopation (F4/F2 -> E-flat4/E-flat2; G-flat4/G-flat2 -> F4/F2), i.e. double octaves,
%   not suspensions. The first also left 31:1 without G-flat and the second made 32:2.5 root-position
%   G-flat major. Both were removed.
% Dominant chain: 7-6 (alto, 32:1), b6-5 (soprano, 32:4.5), 4-3 (tenor, 33:3).
% Prepared suspensions (suspensions.py): 32:1 alto 7-6, 32:3 tenor 4-3: 2 on strong beats, both the skeleton's
%   (whole score with this section spliced: 21 strong + 11 weak, unchanged by the bass imitation).
% Harmony against the blueprint's section-4 labels: 30:1 V and 30:4 i6/4 as given, with the bass arpeggiating
%   V in between (above); 31:1, 31:4 and 32-34 as given (bar 32 as in the skeleton: 32:2 iv6, 32:2.5 iv6/5
%   with S2's passing D-flat, 32:3 cadential 6/4 with E-flat). Added inside bar 31 (the skeleton held C dim
%   over E-flat all bar): 31:2 ii half-dim 6/5 (C E-flat G-flat B-flat), 31:3 vii dim 4/3 (A dim7 over
%   E-flat). Added at 33:2.5: F B-flat C (sus4, one eighth).
% Flags (check.py/strict.py, bars 29-35), against the skeleton's: MEL 32:1 bass D-G-flat (the lament's
%   diminished fourth); XREL 33:4 and 33:4.5 alto E-flat then bass E (the enharmonic pivot itself); both
%   the skeleton's. New, all from the bass imitation, all the same arpeggiated 6/4 of an unchanged V (the
%   kind the blueprint labels at 13:1, "the subject's arpeggiated tail, a 6/4"): D4? 30:2 and 30:2.5
%   tenor F3 over bass C3; D4? 30:3 and strict ACC 30:3 soprano F4 over bass C3 (S2's own F, a consonant
%   fourth above the bass's arpeggiated fifth; not a suspension, resolved by the bass moving to A2 at 30:3.5).
%   ACC2: 7, the skeleton's: 29:1 alto A4/bass E-flat2 (section 3's A dim7); 32:1 alto F4 against soprano
%   E-flat5, tenor G-flat3 and bass G-flat2 (the 7-6); 32:3 alto E-flat4/bass F2 (the chord seventh of V,
%   prepared as a common tone from 32:2) and tenor B-flat3/bass F2 (the 4-3); 33:1 soprano C5/tenor
%   B-flat3 (the held fourth under the fifth).
% Spelled dissonances check.py cannot see (it measures semitones), all intended: 31:3 tenor A3/alto G-flat4
%   (diminished seventh inside A dim7), 34:1 tenor G-sharp3/soprano C5 (the pivot's diminished fourth,
%   skeleton), 34:4 tenor G-sharp3/alto F4 (diminished seventh, upper neighbour on a weak eighth).
% For the design owner (outside this file):
% * The double-fugue layer (review round 1): this head stretto is all the arioso can give S2. A full answer,
%   S2 inverted, or S1 over S2 (the second invertible position) needs a slot outside bars 30-34; otherwise
%   the blueprint should describe the form as a fugue, a counter-fugue on the inversion and a combination
%   of the tune's halves. The entry table (4.2) and section 2.5 can list the bass's head at 30:2.
% * Piano idiom (for the blueprint's section-4 notes): in 30:1-30:3.5 the left hand plays bass and tenor
%   together (F2-F3, C3-F3, C3-A3, A2-A3), no pedal trick needed. From 30:4 the tenor lies 16-21
%   semitones above the bass, so the left hand cannot hold the bass under the tenor's pulse: strike each
%   new bass note alone and catch it with the sostenuto pedal (30:4, 31:1, 31:4, 32:1, 32:3, 33:1, 34:1),
%   let the left hand take the tenor pulse, change the damper per harmony. At 30:4 the right hand has the
%   octave D-flat4-D-flat5 but F2-B-flat3 is a twelfth for the left; 31:4 (D2 A-flat3 F4 F5) and 32:3 (F2
%   B-flat3 E-flat4 D-flat5) fit neither hand: spread all three, bass slightly before the beat. At 31:1 the right hand takes the tenor's C4 (C4 G-flat4 C5, an
%   octave). 34:1 needs a major tenth (E2-G-sharp3): sostenuto as above. The quartet has no problem, and
%   MIDI is unaffected.
% * plan.json: the tenor 30:4.5-32:1 (the lament) is the section's moving inner line but has the free role
%   (-4/-0.2), the same level as the alto's pulse. Give it a role of its own, e.g. "lament", about +2 piano
%   / +0.2 strings. perform.py applies any role name listed in role_boost/role_level (boost.get(role, 0));
%   splice_check only compares notes under subject, answer, cf, cs and keep, so a new name costs no check
%   (a 'cs' role would fail it). plan.json is written by build_sk.py from piece.py (GLOBAL and the
%   section's roles), so the change belongs there.
soprano = \absolute {
  % 30
  c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1 |
  % 34
  c''2 b'2 |
}
alto = \absolute {
  % 30
  a8 a8 a8 c'8 c'8 c'8 des'8 f'8 | ges'8 ges'8 ges'8 ges'8 ges'8 ges'8 f'4 | f'8 f'8 ees'8 ees'8 ees'8 ees'8 ees'8 ees'8 | ees'8 ees'8 ees'8 f'8 ees'8 ees'8 ees'8 ees'8 |
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
  f,4 c4. a,8 f,4 | ees,2. d,4 | ges,2 f,2 | f,1 |
  % 34
  e,1 |
}
