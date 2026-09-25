\version "2.24.0"
% bars 1-12
% Section 1: Exposition, entries 1-3. Composed from design/final-lab/sections/sec01_expo.ly.
% Verify: python3 design/final-lab/splice_check.py score/sections/sec01_expo.ly  (PASS)
%
% WHAT IS WRITABLE HERE. Everything is thematic or deliberately silent (BLUEPRINT sections 6 and 7):
% S 1:1-5:4 subject, 5:4-9:3 CS1 (answer level), 10:1-13:1 CS2; A 5:1-9:4 answer, 9:4-13:1 CS1;
% B 9:1-13:1 subject. The alto before 5:1, the bass before 9:1 and the whole tenor are FREE on the map
% but stay silent: rule 6 keeps the solo (1-4), the two-voice entry (5-8) and the three-voice entry
% (9-12) thin, and the boundary table has the tenor resting throughout. The only composed span is the
% soprano's CS1 landing and the free beat after it, 9:3-10:1.
%
% THE LANDING (soprano 9:3-10:1): skeleton  e''4. g''8 c''4 r4   ->   e''4. g''8 e''4 r4
% * 9:3 E5 instead of C5, the one changed note. The skeleton landed the soprano on C5, an octave above the
%   alto's C4 (the answer's last note), by similar motion (G5-C5 over E4-C4, a direct octave): C over
%   B-flat, two pitch classes on a strong beat. E5 gives the rootless C7 of 9:1 its third back, so 9:3 is
%   C E B-flat = V4/2 of V (C7 over the bass subject's B-flat), and soprano and alto move in tenths
%   (9:2.5-9:3), not octaves.
% * 9:4 keeps the skeleton's quarter rest. The lament (alto F3, CS1 at subject level) enters alone over
%   the bass's re-struck B-flat: B-flat 2 F3, then A2 F3 at 9:4.5 (V6 implied). The entering voice takes
%   E5's resolution to F, and the bass's B-flat, the seventh of C7, falls to A. In the quartet both violins
%   stop at 9:4 and the viola's first note is heard alone over the cello.
% * The join matches the other CS1-to-CS2 join: in section 2 the alto lands A-C-A (13:1-13:3), rests at
%   13:4 and starts CS2 at 14:1; here the soprano lands E-G-E, rests at 9:4 and starts CS2 at 10:1. Both
%   landings end on the third of the chord under them (E of C7, A of F), and the voice leaves it for a rest.
% * Rejected: f''4 (the previous version) and f''8 r8 put F5 on the lament's first attack, two octaves above
%   the alto's F3, over the B-flat: B-flat F F on the entry beat, the new voice masked by its own pitch class
%   in the top voice, and every attack of bar 9 shared by S and A. c''4 fills 9:4.5 (A2 F3 C5) but gives the
%   outer voices C5-B-flat 4 over A2-B-flat 2 into 10:1, a 2-1 over 7-1 clausula in the middle of entry 3,
%   and it leaves the soprano singing without a break from 1:1 to 20:1.
% * ARTICULATION: the separation before CS2 is the written rest, so perform.py renders it; plan.json needs
%   no breath (its breaths stretch time for all voices and would put a hitch into the bass's B-flat A
%   B-flat). It is the soprano's only rest in bars 1-19. CS2 re-enters after it on B-flat 4, the subject's
%   note, at the level of the subject's neighbour below it, not louder (intent only, rule 8).
%
% FLAGS (splice_check.py, strict.py -v, check.py on bars 1-13):
% * No new D4?, DIR, MEL, XREL, CLASH or unison.
% * UNI 5:3 soprano/alto: skeleton, documented in BLUEPRINT section 1 (S1 ends on F where the answer
%   enters on F).
% * DIR 13:3 S/B: printed only when spliced into SK_final.ly (the skeleton's section 2 descant); against
%   the delivered sec02 it does not occur.
% * ACC2 9:1 soprano E5 / bass B-flat 2 (inherited, locked notes): the tritone of the rootless C7, bass
%   B-flat = the chord seventh, resolving to A at 9:4.5 (chord-seventh licence). strict.py: clash 0,
%   xrel 0, acc 0, acc2 1 (this one).
% * check.py's list of dissonances swaps one line at 9:3: the skeleton's M9 C5/B-flat 2 becomes the tritone
%   E5/B-flat 2 [B:SUS(re)]. E5 is the third of C7, and the bass B-flat is its seventh, held, re-struck and
%   resolved to A at 9:4.5. The count is unchanged, 0 unjustified.
%
% SUSPENSIONS (suspensions.py): prepared 0, weak-beat 2 (6:4 alto F4->E4, 2-3 against the soprano's G5;
% 10:4 bass B-flat 2->A2, 2-3 against the alto's C4), both from the locked counterpoint. No strong-beat
% suspension can be written in this section: the one free strong beat (9:3) could only hold the locked
% g''8 (a tie would change CS1's note length, and G5 is a consonant fifth over the alto's C4 anyway).
%
% HARMONY LABELS (grid.py): only 9:3 changes against BLUEPRINT section 1: C over B-flat -> C7 over B-flat
% (C E B-flat, V4/2 of V). 9:4 B-flat/F and 9:4.5 F3 over A2 (V6 implied) are the skeleton's two voices.
%
% IDIOM, piano. The blueprint's "9-12 the alto belongs to the left hand" cannot start at 9:1: the alto's
% G4, E4 and C4 lie 21, 18 and 14 semitones above the held B-flat 2, and its E4 at 9:2.5 is 15 below the
% soprano's G5. Proposed: sustain pedal down just after 9:1, up at 9:4 (9:1-9:3.5 is one harmony, E dim
% then C7 over B-flat, so the pedal holds only C7's chord tones). The left hand strikes B-flat 2, lets
% the pedal hold it, and takes the alto's E4 (9:2.5) and C4 (9:3); the right hand has the soprano (with
% G4 at 9:1, a sixth). The pedal change at 9:4 clears E5 so the rest is heard; no pedal across B-flat 2 to
% A2, where the left hand has F3 over the bass (7, then 8). 10:1-10:3.5 the right hand takes the alto's
% D-flat 4 under CS2 (8-12 semitones; D-flat 4 over B-flat 2 is 15). At 10:4 the left hand takes C4 over
% the re-struck B-flat 2 (14), and the right thumb takes it over at 10:4.5 under G-flat 4 so the left
% hand is free for A2. From 11:1 the alto stays in the left hand (at most 12 over the bass; S+A in the
% right hand would reach 23 at 12:1.5). For plan.json's owner: {"at": "9:1", "until": "9:4", "every":
% "bar"}. Strings: the viola takes the alto 9:4-12:4 (blueprint).
%
% REVIEW ROUND 1: two whole-piece findings on this section. Notes unchanged: both fixes live outside this
% file, which a section fixer may not edit. They are ready to paste and were tested on copies in /tmp.
% NOT YET APPLIED (for the owners of piece.py/plan.json, make_global.py, perform.py, quartet.ly, piano.ly).
% (1) 5:3-6:1, the tune "goes wrong". S1 ends on F4 (5:3) and the soprano carries straight on into CS1's
%   c''4 | aes''2. in the tune's own slots (the tune would go on des''8 bes'8 | c''2), and it stays the top
%   line to 9:3. The notes are locked (S1, CS1), so the performance has to let the answer (alto, 5:1) hold
%   the ear, with CS1 heard as a new, softer line. plan.json, via piece.py section 1 "dynamics", then
%   build_sk.py (SK_final.ly must come out byte-identical). Order matters: the step comes before the ramp.
%     {"at": "5:4", "level": "pp", "voice": "soprano"},
%     {"at": "5:4", "until": "10:1", "to": 3.625, "voice": "soprano"},
%     {"at": "10:1", "until": "13:1", "to": "mp", "voice": "soprano"}
%   A voice override in perform.py has no release, so after 10:1 the soprano has to follow the global
%   p < mp (5:1-13:1) on its own. 3.625 is the global level at 10:1. Measured on a copy against
%   score/music-voices.ly: soprano/alto level 2.00/3.09 at 5:4, 2.48/3.25 at 7:1, 3.24/3.50 at 9:1, equal
%   from 10:1 (3.625) through 13:1 (4.00) and after. On piano the soprano's 11 notes 5:4-9:3 lose 2-13
%   velocity (C5 at 5:4 47->34; A-flat 5 at 6:1 53->41, against the answer's 58). No other note changes,
%   and the piece still lasts 232.1 s on both targets. make_global.py must then leave "voice" events out
%   of \dynamicsLine: today it prints every event on every staff, and a numeric "to" stops it with
%   "ValueError: 3.625 is not in list". Print "pp <" on the soprano (violin I) only.
%   Strings: render_quartet.py has no portamento (its pitch bend only tunes), but it slurs F4 into C5,
%   because F4 ends 5 ms after C5 starts (it infers a slur for gaps under 60 ms). A new bow at 5:4 needs a
%   gap of at least 60 ms, for example a perform.py plan key "lifts": [{"voice": "soprano", "at": "5:4",
%   "ms": 90}] that shortens the note ending there without stretching time ("breaths" would stop all
%   four voices). One CC20 is not enough: once a channel carries any CC20, render_quartet.py stops
%   inferring and reads CC20 for every note.
% (2) 9:4-12:4, engraving. quartet.ly gives \alto to violin II, so the printed part has F3 (9:4, 12:4) and
%   G-flat 3 (12:1) below the violin's G3, and piano.ly has no cross-staff. Tested in LilyPond 2.26 on
%   copies: no warnings, and nothing else changes. quartet.ly, before \score:
%     altoToViola = { s1*8 s2. \change Staff = "viola" s4 s1*3 \change Staff = "violinII" }
%     violinIIGap = { s1*8 s2. r4 R1*3 }
%     violaGap = { s1*8 r2. s4 }
%     tenorRestsOff = { s1*8 \omit Rest \override Staff.RestCollision.positioning-done = ##t s1*4
%                       \undo \omit Rest \revert Staff.RestCollision.positioning-done }
%   and the two middle staves (\dynamicsLine stays outside the alto's Voice, or the dynamics would move
%   to the viola with it):
%     \new Staff = "violinII" \with { instrumentName = "Violin II" } << \global
%       \new Voice = "alto" << \alto \altoToViola >> \new Voice \violinIIGap \dynamicsLine >>
%     \new Staff = "viola" \with { instrumentName = "Viola" } << \global \clef alto
%       \new Voice = "tenor" << \tenor \tenorRestsOff >> \new Voice \violaGap \dynamicsLine >>
%   piano.ly, with this section's hands as given above: the alto goes to the lower staff for 9:2.5-10:1
%   and 10:4-13:1, stems up.
%     altoHands = { s1*8 s4. \change Staff = "lower" \voiceOne s8 s2 |
%       \change Staff = "upper" \voiceTwo s2. \change Staff = "lower" \voiceOne s4 | s1*2 |
%       \change Staff = "upper" \voiceTwo }
%     tenorRestsOff = { s1*8 \omit Rest s1*4 \undo \omit Rest }
%     \new Voice = "alto" << { \voiceTwo \alto } \altoHands >>   (upper staff)
%     \new Voice = "tenor" << { \voiceOne \tenor } \tenorRestsOff >>   (lower staff)
%   The other documented spans (13, 42-44, 55:4, 59:3-60:3, 63:4-64:1) belong to sections 2, 5 and 7 and
%   go in the same way, as a staff-change skeleton in parallel with the voice that crosses.
soprano = \absolute {
  % 1
  bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 |
  % 5
  c''4. a'8 f'4 c''4 | aes''2. g''4 | f''4 e''4 ees''2 | des''2. c''4 |
  % 9
  e''4. g''8 e''4 r4 | bes'8 a'8 bes'8 c''8 des''8 c''8 ees''8 ges'8 | des''4 c''8 f''8~ f''2 | ees''8 f''8 ees''8 des''8 ces''4 des''4 |
}
alto = \absolute {
  % 1
  r1 | r1 | r1 | r1 |
  % 5
  f'2. f'8 e'8 | f'2. f'8 e'8 | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f'8 |
  % 9
  g'4. e'8 c'4 f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4 |
}
tenor = \absolute {
  % 1
  r1 | r1 | r1 | r1 |
  % 5
  r1 | r1 | r1 | r1 |
  % 9
  r1 | r1 | r1 | r1 |
}
bass = \absolute {
  % 1
  r1 | r1 | r1 | r1 |
  % 5
  r1 | r1 | r1 | r1 |
  % 9
  bes,2. bes,8 a,8 | bes,2. bes,8 a,8 | bes,4. c8 c4. ees8 | ees2. des8 bes,8 |
}
