\version "2.24.0"
% bars 20-29
% Section 3: Stretto in the relative major (false dawn), liquidation, Climax I. Composed from the verified
% starter design/final-lab/sections/sec03_stretto_liquidation.ly; LOCKED, CS and KEEP spans unchanged,
% every boundary entry kept. Revised after review (findings 1-9 cited by number); whole-piece review round 1:
% finding 4 done (alto 20-21, below); findings 1-3 need piece.py (see REPORTS at the end of this header).
%
% FREE ALTO 20-26:2, the inner voice between the tenor leader (S1 in D-flat) and the soprano follower:
%   20  Ab (boundary) F Bb in quarters, then Ab: the alto moves only where the soprano's silence needs a
%       chord tone, so the leader's head (S1 in D-flat major, the tune's major shape heard for the first
%       time) is heard as the entry. The F at 20:2 takes over the soprano's third as she falls silent, so
%       the D-flat dawn keeps its third under the leader's held Db (8); it is also the A-flat7's seventh
%       (alto Gb4, 19:3) resolving late by way of the boundary Ab (Gb Ab F). The Bb (a 6th over the pedal)
%       is held into 20:4, where it and the tenor's Db are suspended together over the lament's Ab2 (9/4)
%       and resolve together at 20:4.5 (8/3; sixths Bb/Db to Ab/C), the double suspension on V (2). So
%       21:1 is a clean I6 (F3 Db4 Ab4), not b-flat 6/4.
%   21  Ab held through the I6 while the leader's second head sounds (the skeleton's bar), then Gb for ii7
%       and vii dim 6 (21:4). Whole-piece review, finding 4: the previous eighths (Ab Gb F Ab Bb | Ab Bb
%       Ab G Gb, ten attacks in two bars) circled Ab4-Bb4 above the leader as the top line while the
%       soprano rests; in the piano render the tenor's held Db4 (velocity 67-73) decayed under them
%       (50-60), so the head Db Db C Db read as an inner pedal under a new melody and the stretto was heard
%       only when the soprano entered at 22. Now five attacks (53-59) and the eighth motion starts at 22
%       with the follower. This reverses round 1's (5) (attacks at 21:2.5 and 21:3); the hairpin audit
%       still finds an attack in every half bar (tenor and bass at 21:1; alto, tenor and bass at 21:4).
%   22  Bb held under the follower's entry (the third of G-flat), a 7th over the lament's C-flat at 22:3,
%       resolving to Ab on 22:3.5, the eighth where S, T and B all hold; Cb on 22:4 completes C-flat major
%       under the soprano's Gb and holds through her F, then steps to Db (6). The free voice no longer
%       moves with the follower's Gb-F motto.
%   23  the mirror of CS2's head, x x+1 x x-1 x (Db Eb Db Cb Db), in eighths where the other three voices
%       hold (Db/Eb on the beats: G-flat/B-flat never sounds as two pitch classes only); then Ab at 23:4,
%       held as a common tone over the lament's Ab-C (1): 23:4.5 is a 6/4 that doubles its bass (Ab2 Db4
%       Ab4 F5), 24:1 a complete A-flat7 over C (V6/5 of D-flat, the soprano's Gb its seventh).
%   24  Ab C Eb: the line rises through the A-flat chord into the kept Eb5 (24:3), its peak, under the
%       soprano's C-flat 6. 24:2 C dim (vii dim of D-flat, Gb held), 24:2.5 A-flat over E-flat, C doubled.
%   25  Eb5 held over the Neapolitan (C-flat major over E-flat, the N6 of b-flat, its bass doubled as the
%       N6 wants) while the tenor moves; it leaves at 25:3.5, the one eighth where S, T and B all hold:
%       Db5, the seventh of E-flat minor 7 (25:4) and a 7th under the soprano's suspended Cb6 that becomes
%       a 6th as she resolves; then Cb5 at 25:4.5 (C-flat over G-flat, the passing 6/4 of 25:3 again; a
%       5th against her Gb5, so no parallel sixths with her Bb-Gb) and Ab4 at 26:1 by a falling third (7).
%       The line sinks Eb Db Cb Ab into the kept G against the soprano's S1 tail instead of shadowing it.
%       Cb rather than the reviewer's held Db at 25:4.5: with Db held, the tenor's Eb4 would sit a 7th
%       under it in the last sonority before its 7-6 at 26:1; with Cb it is a 6th under it (consonant).
%   26  Ab (not Db) at 26:1, so no resolution note of the tenor's 7-6 sounds above it; then the kept G.
% FREE TENOR 25-26:2 (unchanged): the mirror sigh Gb Ab Gb, then the line sinks Gb F Eb Db C Bb into the
%   E dim7 (the lament's descent; "sinks through F"), with a 7-6 over the bass F at 26:1 (Eb held from
%   25:3). "26:1 D-flat/F" arrives on 26:1.5 as that 7-6's resolution (26:1 is F Eb Ab Ab); 26:2 F minor.
% FREE BASS 20:1-20:4: the tonic pedal Db2 is kept (3, weighed): the lament's Ab2 at 20:4 is an entry and
%   reads as one when it rises out of a held pedal, not out of a walking I-IV-V bass. With the soprano's
%   rest (a deliberately thin place) 20:2-20:3.5 are three voices over the pedal: 20:2 the alto's F
%   (major third), 20:3 a Db-Bb sixth (the alto's arpeggio F Ab Bb over Db), not "I add6".
% FREE BASS 24:3-26:3: the skeleton's line restored (9): Eb3 held under the N6 (25:1-25:3), a falling
%   sixth to Gb2 under the soprano's 4-3, then the chromatic fall Gb F E Eb into Climax I. The octave drop
%   Eb3-Eb2 at 25:2 is gone: it added no attack and stretched the left hand to 26-27 semitones.
% Deliberately thin places kept: soprano silent 20:2-21:4; nothing added 26:3-29 (the liquidation).
%
% Suspensions (suspensions.py): strong beats 22:3 A 7-6, 25:3 S 4-3 (skeleton), 26:1 T 7-6 = 3. All three
%   are also consonant in the last sonority before the agent: at 22:2-22:3 the alto's Bb clashes only
%   with the lament's passing C3, at 25:2.5 the soprano's Cb6 only with the tenor's passing F4, and at
%   25:4.5 the tenor's Eb4 is a 6th under the alto's Cb5. Weak beats: 20:4 A 9-8 with T 4-3 (the double
%   suspension), 21:4 T 7-6, 23:4 S 7-6 (now against the alto's Ab4). The previous header's 5 is withdrawn
%   (1, 2, 4): 21:1 A "4-3" was V's 9th carried over a change of bass (Bb4 a 9th over Ab2 and a 7th over
%   the tenor's C4 just before the agent); 24:1 A "9-8" was a 6/4's fourth (Db5 over Ab2) carried into a
%   b9 by the bass's leap. suspensions.py credits both because it tests the preparation only where the
%   held note is attacked; its owner is asked to also test the last onset before the agent (licensing a
%   clash with a stepwise passing note in the other voice) and to re-count the piece.
% Flags: no new D4?, DIR, MEL, XREL, CLASH or ACC2 (strict ACC2 in 19-30 unchanged: 19:3 section 2's
%   seventh (twice against SK_final's tenor, once in the assembled score), 22:1 and 24:1 soprano S1 over
%   the lament, 26:3 and 29:1 the dim7 keeps). splice_check PASS against SK_final and against the
%   assembled score (delivered sec02/sec04). New strict ACC
%   24:1 soprano Gb5 / alto Ab4: the seventh of A-flat7/C (rule 4, a chord seventh). check.py DIS, all
%   changes against the previous version: strong DIS down from 3 (21:1 Bb4/F3; 24:1 Db5/Eb4, Db5/C3) to
%   1 (24:1 Gb5/Ab4, the same chord seventh). New weak DIS, all of them (the 20:1.5 Gb4, 21:2.5 Bb4 and
%   21:3.5 G4 of the earlier alto are gone with finding 4): 22:3.5 Gb5/Ab4 m7, the 7-6's resolution under the
%   soprano's held Gb (A-flat minor 7 = IV add6); 23:4 Gb5/Ab4 m7, A-flat7; 25:3.5 alto Db5 (m7 under
%   the soprano's suspended Cb6, m7 over the tenor's Eb4), the seventh of E-flat minor 7 arriving early;
%   25:4.5 alto Cb5 (4th over Gb2), the passing 6/4 C-flat over G-flat.
% Idiom (9): 25:1-25:2.5 lies in one left hand (Eb3 under the tenor's Gb4 F4, 14-15 semitones) except the
%   tenor's Ab4 at 25:1.5 (17), which the right hand takes under its held Cb6/Eb5 (a tenth). 25:3-26:2.5:
%   the tenor's Eb4 over Gb2/F2 needs 19-22 semitones in the left hand and 17-20 in the right, so on the
%   piano roll the left hand Gb2-Eb4 at 25:3 and catch the bass in the pedal; the 7-6 at 26:1 then lives
%   in the pedal (which also sustains its resolution Db4: half-change at 26:1). It is fully idiomatic only
%   on the quartet (viola over cello).
%
% REPORTS for the design owner (whole-piece review round 1; piece.py items this file may not change).
% R1 (findings 1 and 3): the liquidation is not heard as heads accumulating one chord. The alto KEEP G4
%   (26:3-27:3) completes E dim7 at 26:3, so no head adds a pitch class, 27:1-27:3 is a hollow E2 G3 G4
%   (the tenor's head doubles the held G) and the alto's B-flat head is a sounding voice changing pitch.
%   Tested on copies of the assembled score:
%   (a) finding 1, alto `aes'2 r2 | r2 bes'2 ~`: 26:3 E2 Bb3 Db5 (the follower's last note still lands on
%       a diminished sonority), 27:1 E-G, 27:3 E-G-B-flat (the blueprint's own "27 E-G, E-G-B-flat"),
%       28:1 E dim7 complete; alto and soprano heads enter from silence. check.py 0/0/0/0, strict
%       unchanged (clash 0, xrel 8, acc 7, acc2 31), suspensions unchanged (21 + 11), every hairpin half
%       bar attacked; splice_check fails only on the alto keep.
%   (b) finding 3, alto `aes'2 g'2 | des''2 bes'2 ~`: adds MEL G4-Db5 (dim5) at 27:1, sounds Db5 in the
%       alto a bar before the soprano's Db5 head (the last entry pre-empted at its own pitch), and the
%       alto's head is still a sounding voice changing pitch.
%   Recommended (a): in piece.py section 3 change keep ('alto', '7:3', '8:3') to the rest ("alto silent
%   until its head: E, E-G, E-G-B-flat, E dim7"), drop "E dim7 complete at 26:3" from the tenor keep's
%   text, run build_sk.py, then set this file's alto 26-27 to (a); BLUEPRINT 4.3 and the section-3
%   spec then read 26:3 "E dim (E B-flat D-flat), the first head".
% R2 (finding 2): the false dawn is as loud as the apotheosis peak. Measured with this file on the
%   assembled score, bar maxima for bars 24/25/26 against bar 60: piano velocity 86/92/93 vs 93 (soprano
%   Cb6 92 at 25:1, Ab5 93 at 26:1), strings CC1 105/113/117 vs 113. In piece.py section 3, dynamics
%   {'at': '1:1', 'until': '7:1', 'to': 'f'} -> 'to': 'mf' gives piano 78/81/79, strings 94/101/108
%   (bar 26's 108 is the bass head inside the < ff from 26:3; the soprano's maximum is 100). Adding the
%   optional > (1:1-5:3 < mf, 5:3-6:3 > mp) gives piano 80/77/67, strings 97/92/98, so the dawn fades as
%   the A-flat fifth turns minor and the crescendo from 26:3 belongs to the crush. Both variants measure
%   232.1 s. This file cannot fix it: the C-flat 6 and A-flat 5 are the LOCKED follower.
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
  aes'4 f'4 bes'4. aes'8 ~ | aes'2. ges'4 | bes'2 ~ bes'8 aes'8 ces''4 | des''8 ees''8 des''8 ces''8 des''4 aes'4 ~ |
  % 24
  aes'4 c''4 ees''2 | ees''2 ~ ees''8 des''4 ces''8 | aes'2 g'2 ~ | g'2 bes'2 ~ |
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
