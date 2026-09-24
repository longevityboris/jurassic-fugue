# Proposal 1: "Ricercar a 4 sopra il tema di Jurassic Park" (Bach-strict)

A double fugue in B-flat minor, alla breve, 84 bars, about 3'44".

All proofs are reproducible:
- `python3 lab/build_core.py` builds the material proofs (P01-P13).
- `python3 lab/sections.py` builds the fully written passages: the exposition (bars
  1-19), the climax exit (65-69) and the end of the apotheosis with the coda (75-84).
- `python3 lab/skeleton.py --table` builds the whole-piece thematic skeleton.

A lab counts as VERIFIED when `tools/check.py` reports 0 PAR!, 0 BEAT, 0 DIS! and 0 D4?.
Each lab is also run through a stricter alla-breve filter, `ricer.strict()`. It lists
every dissonance on a half-note beat (beat 1 or 3) that is not a suspension or a
retardation. Every item it reports is explained by ear in this document.

## 0. Concept

**Subjects.** Subject I is the first half of the theme at its real rhythm. Subject II
is the second half. The theme is broken in two and put back together three times:
- in D-flat major, as one voice's melody (bars 33-41);
- as the two halves sounding at once (bars 49-58);
- whole and transfigured in B-flat major (bars 69-77).

**Learned devices, as in the Ricercar a 6 and the Art of Fugue:**
- triple invertible counterpoint in all six orders;
- invertible counterpoint at the 12th;
- a mirror inversion of the entire three-voice complex;
- a four-voice stretto chain that is itself the modulation;
- the combination of the two subjects;
- a stretto *per arsin et thesin*;
- the augmented answer in the bass as the dominant pedal, with rectus, inversus and
  Subject II sounding over it at the same time.

**Large-scale shape, after late Beethoven.**

| model | what it gives this piece |
|---|---|
| Op. 131 No. 1 | voices enter from the top down |
| Op. 110 | an inversion section |
| Hammerklavier | a new, lyrical subject in a remote major key, later combined with the first |
| Op. 131 No. 1 | augmentation in the bass near the end |

After a general pause, the theme returns transfigured in B-flat major. A deceptive
cadence follows, then a plagal close on the minor iv, so the major carries a memory
of the minor.

**The key plan follows the subject.** Its main stations are b-flat, c, e-flat,
D-flat, b-flat, then V with c on top. These are the subject's own structural notes:
bes, c, ees, des, bes, c.

## A. Materials (tonic level, B-flat minor, 2/2)

All material is kept in `lab/mats.py`. The LilyPond text is quoted exactly below.

### Subject I (S1): theme bars 1-4 at real rhythm, minor, with its landing note
```
bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' | c''2
```
- **Rhythm.** Unchanged from the theme. In alla breve the dotted halves carry the
  beat, so the tune keeps its breadth. This fixes flaw 1, the halved note values.
- **Landing.** The subject ends on c'' on the downbeat of theme bar 5. That note is
  2^ over V, a half cadence. The landing always elides into the next event (a
  countersubject, a new entry, or a tied suspension), so the voice never stops on a
  pickup.
- **Implied harmony.** i (a tonic pedal with the leading-tone sigh) | i | i-iiø7-iv
  | iv-i6-i | V.
- **Tune tweaks.** None, apart from the minor third (des'') given in THEME.md. The
  melody is used at its original pitch and rhythm, so it is recognised at once.

### Answer (A1): real, at the upper fifth, F minor
```
f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f'' | g''2
```
The answer is real because the subject starts on 1^ and does not touch 5^ before its
cadence. There is no early dominant for a tonal answer to adjust. The answer's
landing, g over G major (V of C), is used on purpose: it becomes the pivot into C
minor (section II).

### Countersubject 1 (CS1): the lament
```
f'2 ges'2 | g'4. aes'8 bes'4. c''8 | bes'2. aes'4~ | aes'4 g'4 ges'4 f'4 | e'2
```
- CS1 holds 5^ and then rises chromatically: f-ges-g-aes-bes-c (passus duriusculus).
- Against the subject's climb it forms a 2-3 bass suspension (bar 3) and a 4-3
  suspension (bar 4).
- It then falls chromatically, aes-g-ges-f-e. This is the descending tetrachord of
  the royal theme in the Musical Offering.
- Its rhythm complements the subject's: it moves on beats 1 and 3 while the subject
  holds.
- Invertible at the octave: P01 and P02.
- Invertible at the 12th: P04 and P05. At the 12th below, CS1 becomes a rising
  chromatic bass (bes ces c des ees f) under the held subject.
- Not invertible at the 10th, because the sixths of bar 4 would become octaves. The
  10th is not used.
- Its landing is flexible. It is e' before an answer. When the following voice needs
  the downbeat, it stops on f' or becomes a tie; bar 14 and bar 18 show both.

### Countersubject 2 (CS2): the quarter-note motor
```
r4 f''4 ees''4 des''8 c''8 | bes'4 c''4 des''4 ees''4 | des''4 c''4 ees''4. des''8 | c''2 bes'4. aes'8 | g'2
```
- CS2 keeps the quarter-note motion going that the subject lacks.
- Bar 1 falls a tetrachord (f ees des c) and bar 2 climbs it back (bes c des ees), so
  the line contains its own mirror.
- It uses the theme's dotted cell twice.
- It enters after a quarter rest so the subject's head is heard alone first. After a
  cadence, bes' replaces the rest (bar 11).
- **Triple counterpoint S1/CS1/CS2 at the octave is clean in all six orders (P06).**
- When CS2 is the lowest voice, its landing g is changed to c. Otherwise it makes a
  6/4.

### Inversion (I1) and the mirrored complex (IC1, IC2)
The inversion is a diatonic mirror in harmonic minor, on the axis 1^<->5^ (the Art of
Fugue convention). The leading-tone sigh bes-a-bes becomes the lament sigh f-ges-f,
and each inverted entry falls from 5^ to a landing on 4^:
```
I1  = f''2. f''8 ges''8 | f''2. f''8 ges''8 | f''4. ees''8 ees''4. c''8 | c''2. des''8 f''8 | ees''2
IC1 = bes''2 a''2 | aes''4. g''8 f''4. ees''8 | f''2. ges''8 g''8~ | g''4 aes''4 a''4 bes''4 | ces'''2
IC2 = r4 bes'4 c''4 des''8 ees''8 | f''4 ees''4 des''4 c''4 | des''4 ees''4 c''4. des''8 | ees''2 f''4. g''8 | aes''2
```
IC1 is the exact mirror of CS1 except for one added note. A chromatic passing ges''
in bar 3 turns the mirrored suspension into a semitone retardation. The inverted
lament therefore becomes a chromatic ascent of seven semitones: f-ges-g-aes-a-bes-ces.

**The mirrored trio I1/IC1/IC2 is clean in all six orders (P07).** The complex is
triple invertible both rectus and inversus.

**Rectus against inversus at offset 0.** S1 with I1, CS1 with I1, and CS1 with IC1
are clean in both vertical orders (P08). S1 with I1 is the mirror pair used at the
climax.

### Subject II (S2): theme bars 5-8, the same length as S1
```
S2   (minor)   c''4. a'8 f'4 des''8 bes' | c''2. f''8 bes' | ees''4. des''8 des''4. c''8 | c''1 | c''2
S2M  (major)   c''4. a'8 f'4 d''8 bes'   | c''2. f''8 bes' | ees''4. d''8 d''4. c''8   | c''1 | c''2
```
S2 is 4.5 bars, exactly like S1, so the two halves of the theme can start together
and land together. S2 lives on the dominant: it arpeggiates V, touches i, and ends on
a long 2^.

**S2 is used in these forms:**
- D-flat major, starting on ees'' (S2D).
- A-flat major, starting on bes' (the answer).
- B-flat minor at its original pitch.
- F major, starting on g'' (S2Mu, for the combination).
- B-flat major at its original pitch (in the combination in e-flat, and in the
  apotheosis).

### Countersubject 3 (CS3), for S2: the dolce line (D-flat level)
```
CS3  c'2 f'2 | ges'4 f'4 ees'4 f'4 | bes'2 aes'4 ges'4 | aes'4 bes'4 c''4 des''4 | c''2
bass c2 des2 | ges2 aes4 f4 | ees2 f4 ees4 | aes2 c2 | aes2      (harmonic bass of the D-flat entry)
```
- CS3 holds long notes under S2's arpeggio and moves in quarters under S2's long notes.
- Its bar-3 bes'-aes'-ges' passes under S2's 7-6 suspension (f''-ees'' over ges).
- It rises through the long held note of S2's bar 4.
- S2 + CS3 + bass is clean with strict = 0 (P11).
- CS3 is written as a *lower* countersubject. Its double-octave inversion is also
  interval-clean, but it goes above the soprano's range and has one accented 4th
  (P11b), so the design always keeps CS3 below S2.

### Augmentation
```
A1aug (bass)  f,1~ | f,2 f,4 e,4 | f,1~ | f,2 f,4 e,4 | f,2. g,4 | g,2. bes,4 | bes,1~ | bes,2 aes,4 f,4 | g,1
```
The answer in augmentation keeps F for four bars, with the leading tone e as a lower
neighbour. It is literally a dominant pedal made from the subject. Its second half
rises f-g-bes-aes-f-g into the final cadence.

### Apotheosis form
The whole theme in B-flat major (THEMEM), 8.5 bars, S1M and S2M elided on the
shared c'':
```
bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 | c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | c''1 | c''2
```

## B. Proof table

### B1. Material proofs (`lab/build_core.py`, summary lines in `lab/proofs_core.txt`)

| lab | claim | result (PAR!/BEAT/DIS!/D4?) | strict (explained) |
|---|---|---|---|
| P01_S1_over_CS1 | S1 over CS1, octave | 0/0/0/0 | 1: 1:1 is a 4th in two voices only; a lower voice is always present in use |
| P02_CS1_over_S1 | CS1 over S1, octave | 0/0/0/0 | 0 |
| P03_CS1_over_A1 | CS1 over the answer (exposition bars 5-9) | 0/0/0/0 | 0 |
| P04_S1_over_CS1at12 | CS1 at the 12th, as bass | 0/0/0/0 | 1: 2:1, chromatic bass c under the held bes (inverted pedal) |
| P05_A1_over_CS1at12 | answer over CS1 at the 12th | 0/0/0/0 | 1: same spot |
| P06_* (6 files) | triple counterpoint S1/CS1/CS2, all orders | 0/0/0/0 in all six | at most 2 per file: 4ths at the entry and the CS2-bass landing |
| P07_* (6 files) | mirrored trio I1/IC1/IC2, all orders | 0/0/0/0 in all six | at most 2 per file, same kind |

(Rows P08-P13: see B3.)

### B2. The whole-piece thematic skeleton (`lab/SK_skeleton.ly`, `lab/proofs_skeleton.txt`)
Every statement in the entry table (section C3) is placed at its real bar, voice,
key and octave. The exposition is included complete, free counterpoint is left as
rests, and the whole file is checked at once. The joints between sections are
therefore proven too.

`-- totals: 84 bars; errors 0, parallels 0, beat-par 0, unjustified 0`

The checker reports two remaining flags, both harmless:
- `CROS 20:4.5`: the tenor's IC1 f dips one eighth below the bass's I1 aes (the
  mirror section). It is a momentary exchange that sounds fine on strings and piano.
- `DIR 74:4.5`: a direct fifth between soprano and alto. It exists only because the
  bass is still a rest in the skeleton, and disappears once the bass is composed.

Strict items in the skeleton, all deliberate:

| position | what it is |
|---|---|
| 19:1 (exposition lab) | the cadential 6/4 of C minor over G |
| 23:3 | a passing 6/4 |
| 33:1 | soprano entry on des'' over a passing aes |
| 49:1 | c' over bes,: the C7/B-flat that opens the combination |
| 55:3, 57:1, 58:1 | the tenor's S2 is the lowest voice only because the bass is still a rest there |
| 59:1, 61:1, 63:3 | S1's bes over the F pedal: the subject's head *is* the 4-3 over the dominant |
| 61:1, 63:1 | the free seventh of V7 over the pedal |
| 67:3 | the landing c'' over ges: it is the third of the French sixth (X1) |
| 75:1 | the alto's landing f' under the theme's ees'' |

### B3. Device proofs (`lab/build_core.py`, rows P08-P13 of `lab/proofs_core.txt`)

| lab | claim | result (PAR!/BEAT/DIS!/D4?) | strict (explained) |
|---|---|---|---|
| P08_S1_over_I1, P08_I1_over_S1 | rectus against inversus at offset 0 (the climax pair), both orders | 0/0/0/0 | 3: bes over f is the 4th of the mirror axis. At the climax the pedal F sits under it, so it is the sus4 of V |
| P08_CS1_/IC1_* (4 files) | CS1 against I1 and IC1 at offset 0, both orders | 0/0/0/0 | 2-5: accented chromatic passing notes where the two laments cross. Harsh, so NOT used in the form (reserve) |
| P09_stretto5_3q | S1 stretto at the lower 5th, 3 quarters apart | 0/0/0/0 | 0 |
| P09_stretto5_2bars | S1 stretto at the lower 5th, 2 bars apart | 0/0/0/0 | 0 |
| P09_chain_of_fifths | the four-voice chain exactly as in bars 27-37 (bes' A, ees' T, aes B, des'' S major) | 0/0/0/0 | 1: soprano entry des'' over the bass's passing aes (33:1) |
| P09_chain_3q | four entries at 3 quarters (stretto maestrale, reserve) | 0/0/0/0 | 2: at the landings |
| P10_S1_over_S2Mu, P10_S2Mu_over_S1 | S1 + S2 (F major, a 5th/12th above) at offset 0: double counterpoint at the octave | 0/0/0/0 | 1 / 0: landing 6/4 when S2 is the bass |
| P10_CS2_S2Mu_S1 | the combination trio of bars 49-53 | 0/0/0/0 | **0** |
| P11_S2_CS3_bass | S2 in D-flat + CS3 + its bass (bars 37-41) | 0/0/0/0 | **0** |
| P11b_CS3_over_S2_15th | CS3 inverted at two octaves | 0/0/0/0 (ERR: des''' above the soprano's range) | 1: so CS3 stays below S2 |
| P12_climax_quadruple | I1 (S) + S2 (A) + S1 (T) over A1 augmented (B), bars 59-63 | 0/0/0/0 | 7: all are pedal events. S1's bes = sus4 over F; S2's c against it = the fifth of Fsus4; the free seventh ees'' of V7 (61:1, 63:1); f''/ees'' at 61:1 = root and seventh of V7 |
| P13_apotheosis_stretto | the whole theme (B-flat major) + S1M at the lower 5th, 2 bars later | 0/0/0/0 | 1: the alto's landing f' under ees'' (flexible; X2 turns it into ges') |
| X1_climax_exit | bars 65-69 fully voiced: dim7 over the tonic bass → v7 → IV6 → Fr+6 → V4-3 → V7 → I | 0/0/0/0 | 3: the French sixth's own tritone and seventh; the seventh of V7 |
| X2_coda | bars 75-84 fully voiced: minor iv inside the theme, V7 → bVI deceptive, plagal Amen over the tonic pedal | 0/0/0/0 | 4: the passing seventh of V7 (76:3); iv6/4 and IV6/4 over the pedal (80:3, 81:3, 83:3) |

**Stretto grid, VERIFIED cell by cell (`python3 lab/stretto_grid.py`, table in
`lab/stretto_grid.txt`).** Each cell is a two-voice lab in `lab/stretto/`
(regenerated by the script, not committed).
- `#` = 0 PAR!/BEAT/DIS!/D4? and strict 0.
- `+` = checker-clean, with accented dissonance to review.
- `.` = fails.
- "above/below" intervals are octave-equivalent (compound intervals included).
- Columns = entry distance in quarter notes.

```
S1 leader, S1 follower
             1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
8ve below    .  +  #  .  #  +  +  +  #  +  #  +  #  #  #  +
5th below    +  #  #  .  #  #  #  #  #  #  #  #  #  #  #  #
4th below    .  #  #  +  +  +  .  +  #  #  #  #  #  #  #  #
5th above    .  +  #  .  #  +  +  +  #  +  #  +  #  #  #  +

I1 leader, I1 follower
8ve below    +  +  #  .  .  +  #  .  .  .  .  +  #  +  +  +
5th below    #  +  #  .  .  .  .  .  .  .  .  +  #  +  +  +
4th below    .  .  +  +  .  .  .  +  #  #  #  #  #  #  #  #
5th above    .  #  #  .  #  #  #  #  #  #  #  #  #  #  #  #

S1 leader, I1 follower (mirror stretto)
8ve below    +  +  +  +  #  +  +  +  .  #  #  #  #  #  #  #
4th above    +  +  #  .  .  .  #  .  .  .  .  +  #  +  +  +
5th above    .  +  +  +  +  +  .  +  .  #  #  #  #  #  #  #

I1 leader, S1 follower (mirror stretto)
5th below    .  +  #  +  +  +  .  +  #  #  #  #  #  #  #  #
4th below    .  +  #  #  #  +  +  +  #  +  #  +  #  #  #  +
8ve above    +  +  .  +  #  +  #  +  #  #  #  #  #  #  #  #
```
The subject is unusually stretto-friendly. At the lower 5th every distance from 2
quarters to 4 bars is clean except 1 bar. The inversion strettos at the upper 5th
from 5 quarters on. Mirror strettos work at the octave from 10 quarters and at the
lower 4th from 3 quarters.

**Stretto choices for a composer who wants more learned density.** None of these
change the form:
- I1 × I1 at the upper 5th, 5 quarters apart, in the mirror section (bars 23-26)
  instead of the free soprano;
- the 3-quarter chain (P09_chain_3q) instead of bars 63-67;
- I1 → S1 at the lower 4th, 3 quarters apart, in the coda.

## C. Architecture

### C1. Meter, tempo, duration
Grave, alla breve (2/2), **half = 46** (quarter = 92). That is 85% of the theme's
quarter = 108, which gives gravity without dragging. Bar = 2.609 s.

| bars | tempo | seconds |
|---|---|---|
| 1-48 | half = 46 | 48 × 2.609 = 125.2 |
| 49-58 | poco a poco animando 46 → 50 (mean 48) | 10 × 2.50 = 25.0 |
| 59-67 | half = 50 | 9 × 2.40 = 21.6 |
| 68 | half = 50; fermata on V7 (+2 beats ≈ 1.2 s); general pause 1.5 s | 2.4 + 1.2 + 1.5 = 5.1 |
| 69-77 | Maestoso, half = 44 | 9 × 2.727 = 24.5 |
| 78-84 | 44 → 38 ritardando (mean 41); final fermata 2.5 s | 7 × 2.927 + 2.5 = 23.0 |
| **total** | | **224.4 s ≈ 3'44"** (inside 210-240) |

With `perform.py`, write the general pause as `"breaths": [{"at": "69:1", "ms": 1500}]`
and the fermatas as `{"at": "68:3", "extra_beats": 2}` and
`{"at": "84:1", "extra_beats": 4}`.

### C2. Form table (84 bars)

| § | bars | name | keys | content | dynamics |
|---|---|---|---|---|---|
| I | 1-18 (+19:1) | Exposition (VERIFIED, fully written) | b-flat, f, b-flat, f → c: i6/4 | S1 S · A1 A · codetta 9-10 · S1 T · A1 B, with CS1 and CS2 | p, growing to mp |
| II | 19-26 (+27:1) | Counter-exposition by mirror inversion | c → f → b-flat | M1 19-22: I1 in the bass (c), IC1 T, IC2 S, free A. M2 23-26: I1 in the alto (f), IC1 T, IC2 B, free S | pp sotto voce |
| III | 27-36 (+37:1) | Stretto I: chain in descending fifths | b-flat → e-flat → a-flat → D-flat | S1 in A (27), T (29), B (31), then S (33, major form), each 2 bars apart | mp, cresc. to f at 35 |
| IV | 37-48 (+49:1) | Second exposition (S2), dolce | D-flat → A-flat → b-flat | S 37: S2 in D-flat (the soprano's S1 from 33 continues, so the whole theme sounds in D-flat); A 41: answer in A-flat; T 45: S2 in minor at its original pitch; CS3 below each | subito p dolce, mp |
| V | 49-58 | Combination | b-flat → e-flat → V | C1 49-53: B S1 (tonic pedal), A S2 in F major, S CS2, T free. C2 54-58: S S1 in e-flat, A CS2, T S2 at its original B-flat-major pitch, B free; 58:3 Neapolitan 6th | mf → f, animando |
| VI | 59-68 | Climax on the augmented answer | V pedal | 59-63: B A1aug, T S1, A S2, S I1 (quadruple combination). 63:3-67:3: S S1 per arsin et thesin over the rising augmented bass. 66:1 vii°7 over the tonic bass (fff); 67:1 IV6 → 67:3 French sixth; 68 V4-3 → V7, fermata, general pause (written: X1) | ff at 59, fff at 66 |
| VII | 69-77 | Apotheosis: the whole theme in B-flat major | B-flat | S THEMEM · A S1M at the lower fifth (71) · T, B free chorale foundation | pp, cresc. to ff at 74 |
| Coda | 78-84 | Deceptive cadence and plagal Amen (written: X2, from bar 75) | B-flat | 77 V7 → 78 bVI (G-flat), soprano c''→bes'; 79 V; 80-81 tonic pedal with iv6/4 then IV6/4; 82 S1 head resolved as 4-3; 83 I · iv6/4; 84 I | subito p, down to ppp |

### C3. Entry table (the skeleton; every row is proven in `SK_skeleton.ly`)

| bar | voice | form | key | first note |
|---|---|---|---|---|
| 1 | S | S1 | b-flat | bes' |
| 5 | A | A1 (real answer) | f | f' |
| 5 | S | CS1, answer level (elided from S1's c'') | f | c'' |
| 11 | T | S1 | b-flat | bes |
| 11 | A | CS1 | b-flat | f' |
| 11 | S | CS2 (bes' replaces the rest) | b-flat | bes' |
| 15 | B | A1 | f | f |
| 15 | T | CS1, answer level (elided) | f | c' |
| 15 | A | CS2, answer level | f | (rest) c'' |
| 19 | B | I1 (elided from A1's landing g) | c | g |
| 19 | T | IC1 (tied from CS1's c') | c | c' |
| 19 | S | IC2 | c | (rest) c'' |
| 23 | A | I1 | f | c'' |
| 23 | T | IC1 | f | f' |
| 23 | B | IC2 (its rest taken by I1's landing f) | f | f → F, |
| 27 | A | S1 (elided from I1's landing bes') | b-flat | bes' |
| 29 | T | S1 | e-flat | ees' |
| 31 | B | S1 | a-flat | aes |
| 33 | S | S1, MAJOR form | D-flat | des'' |
| 37 | S | S2 (continues the S1 above: whole theme in D-flat) | D-flat | ees'' |
| 37 | A | CS3 | D-flat | c' |
| 37 | B | CS3's harmonic bass | D-flat | c |
| 41 | A | S2 answer | A-flat | bes' |
| 41 | T | CS3 | A-flat | g |
| 45 | T | S2, minor, original pitch | b-flat | c' |
| 45 | B | harmonic bass for S2 | b-flat | a, |
| 49 | B | S1 (tonic pedal) | b-flat | bes, |
| 49 | A | S2 in F major (S2Mu) | V | g' |
| 49 | S | CS2 | b-flat | (rest) f'' |
| 54 | S | S1 | e-flat | ees'' |
| 54 | A | CS2 | e-flat | (rest) bes' |
| 54 | T | S2M at its original B-flat-major pitch (= V of e-flat) | e-flat | c' |
| 59 | B | A1 augmented | V pedal | f, |
| 59 | T | S1 | b-flat over V | bes |
| 59 | A | S2 minor, original pitch | V | c'' |
| 59 | S | I1 | b-flat over V | f'' |
| 63:3 | S | S1 per arsin et thesin (enters on beat 3) | b-flat | bes' |
| 69 | S | THEMEM, the whole theme | B-flat | bes' |
| 71 | A | S1M at the lower fifth (stretto, 2 bars) | E-flat/B-flat | ees' |

Stretto intervals and distances used in the form:
- lower fifth at 2 bars: the chain in III and the apotheosis;
- simultaneous mirror (offset 0): S1 with I1 at the climax;
- S2 against S1 at the fifth/12th: the combination;
- metrical displacement by half a bar: 63:3.

The full grid of proven options is in B3.

### C4. Tonal plan and the logic of each modulation

1. **b-flat → f (bars 1-18).** Real answers. The last answer lands on g over G major.
2. **→ c (bar 19).** That G is V of C. The exposition ends on the cadential 6/4 of C
   minor over G, and the bass's g *is* the first note of the inverted subject. So
   the inversion begins as a dominant pedal with its own b9 sigh (aes-g).
3. **c → f → b-flat (bars 19-27).** The inverted subject runs from 5^ down to 4^, so
   each inverted entry lands on the tonic of the key a fifth lower. The mirror
   section walks home by descending fifths without any modulating episode: the entry
   in C lands on f, the entry in F lands on bes.
4. **b-flat → e-flat → a-flat → D-flat (bars 27-37).** The stretto chain keeps the
   same descending fifths. Each entry enters a fifth below the last, two bars apart,
   so the stretto *is* the modulation. The last entry is in D-flat MAJOR (S1M). Its
   landing ees'' is the first note of S2, so the soprano sings the whole theme in
   D-flat (bars 33-41). It is the first time the theme is heard complete, and in the
   "wrong" key.
5. **D-flat → A-flat → b-flat (bars 37-49).** S2 is answered in A-flat. The answer's
   landing bes' becomes a 4-3 suspension over F major (V of b-flat), and the third
   entry is S2 in its original minor. D-flat was the relative major; the light dims
   back to minor.
6. **b-flat → e-flat → V (bars 49-59).** The combination over S1 in the bass
   (a tonic pedal). Then S1 moves to e-flat (iv), while S2 is heard at its ORIGINAL
   major pitch (c'' a' f' d'' bes'), which here is V of e-flat. iv prepares V: the
   Neapolitan sixth (58:3) resolves to i6/4 over the pedal F.
7. **V (bars 59-68).** The dominant pedal. The augmented answer rises to bes, where
   the diminished seventh sounds over the tonic bass (66:1, fff). The bass then
   descends chromatically g-ges-f: IV6 (the Dorian E-flat/G) → French sixth (the
   subject's landing c'' is its third) → V with 4-3 → V7, then a fermata and silence.
   At 69 the soprano's c'' falls to bes', the first note of the transfigured theme,
   and the minor third becomes d' in the tenor.
8. **I (B-flat major, bars 69-84).** The deceptive V7 → bVI (G-flat) at 78, then the
   plagal close through the minor iv.

The main stations (b-flat, c, e-flat, D-flat, b-flat, V with c on top) are S1's
structural notes (bes, c, ees, des, bes, c). The ricercar's key plan is the subject
writ large; passing keys (f, a-flat, A-flat) connect them. Compare the Hammerklavier,
whose key plan descends in the thirds of its subject.

### C5. Harmonic outline (half-bar level at entries, cadences and the climax)

**Exposition** (from the written lab `E1_exposition.ly`):

| bars | harmony |
|---|---|
| 1-4 | S1 alone implies i | i | i iiø7-iv | iv-i6 | V |
| 5-8 (f) | i · VI6-vii°7 | IV6/4(melodic)-iiø7-V6/5 | i-iiø7 · v | iv-i6 |
| 9-10 codetta | G (V/V of f) · C/E (V6 of f) | F · F/C (V of b-flat) |
| 11-14 | S1 in the tenor is the bass: a tonic pedal. i · iv6/4-vii°7 | IV6/4 (Dorian g) · i-V6/5 | i · ii7-VII6 | iv (4-3) · iv-i6-i7 |
| 15-18 (f) | i · iv6/4-vii°7 | IV6/4 · i-V6/5 | i · iiø7-VII6 with 9-8 | Ebmaj7/Bb · iv-i6-i7 |
| 19:1 | c: i6/4 over G |

**Mirror (19-26):**

| bars | harmony |
|---|---|
| 19-20 | G pedal (I1 head in the bass): i6/4-V, then V with aes-g (b9-8) |
| 21 | V4/2-V6/5 (bass g-f-d) |
| 22 | vii°6-i6 (d-ees) · V-iv (g-f) |
| 23-26 (f) | the same shape a fifth lower. The alto's I1 lands on bes' at 27:1, now i of b-flat |

**Stretto chain (27-36):** each two-bar block is i (pedal-like S1 head) → V/next.
Bars 33-36 are D-flat: I6/4 (33:1) · ... · V (36).

**S2 exposition (37-48):**

| bars | harmony |
|---|---|
| 37 | V6 · I |
| 38 | ii6/5 · V (I6 under the pickup) |
| 39 | ii · I6-IV with 7-6 |
| 40 | V · V6 |
| 41 | = V of A-flat (the answer starts over E-flat) |
| 45 | F sus4 → F (V of b-flat) |

**Combination (49-58):**

| bars | harmony |
|---|---|
| 49-50 | V4/2 of V (C7/Bb) → V6 (F/A), twice over the tonic pedal |
| 51 | i · V/V |
| 52 | ii-V/V · V/V |
| 53 | V/V → |
| 54-58 | the same, a fifth lower (e-flat), landing on F (V of b-flat) at 58:1 |
| 58:3 | N6 (ees-ges-ces) |

**Climax (59-68):**

| bars | harmony |
|---|---|
| 59-62 | pedal F: sus4-3 (S1's bes-a) and 8-b9-8 (I1's f-ges-f) together, with S2 arpeggiating V; V7 at 61 and 63 |
| 63-64 | bass f-g-g-bes: V · V/V7 · (S1 enters above at 63:3, displaced) |
| 65 | i over bes (the augmented answer's bes = tonic) |
| 66 | vii°7 over the tonic bass (fff) · v6/5-v7 (bass aes-f) |
| 67 | IV6 (E-flat/G, Dorian) · French sixth over ges |
| 68 | V with 4-3 · V7 (fermata), general pause |
| 69 | I, B-flat major |

**Apotheosis (69-77):**

| bars | harmony |
|---|---|
| 69-70 | I over a tonic pedal |
| 71-72 | I · IV (the alto's S1M in E-flat) |
| 73 | I-ii6 · V |
| 74 | V · I6 (theme peak f'') |
| 75 | iv (minor, e-flat-g-flat) · I6 (d'') |
| 76 | V7 |
| 76-77 | V · V7 · V7 (the theme's long c'') |

**Coda (78-84), as written in X2:**

| bars | harmony |
|---|---|
| 78 | bVI (G-flat), deceptive; the theme's c'' falls to bes' (1^) over it |
| 79 | V |
| 80 | I · iv6/4 over the tonic pedal; the alto sings f'-ges'-f', the inverted sigh |
| 81 | I · IV6/4; ges' becomes g', minor turns major |
| 82 | the soprano sings S1's head bes'2. bes'8 a'8: I · IV · V7 with bes'-a' as 4-3 |
| 83 | I · iv6/4, the last lament sigh (tenor ees') |
| 84 | I, ppp, fermata |

### C6. Special harmonic events (where and why)

| bar | event | purpose |
|---|---|---|
| 1:4.5 and passim | vii°7 on the subject's leading-tone sigh | the subject's a against CS1's ges' forms the diminished seventh; the lament is built in |
| 13:3, 14:1, 17:3 | 7-6, 4-3 and 9-8 suspension chains in CS1 | stile antico dissonance, replacing the old piece's 3rds/6ths filler |
| 18-19 | cadential 6/4 of c over G | the exposition opens onto the mirror instead of closing |
| 19-21 | G pedal = the inverted subject in the bass, b9 sigh aes-g | the inversion is heard as a pedal before it is heard as a melody |
| 23-26, 27-37 | descending-fifths sequence carried by entries alone | modulation made of subjects, not episodes |
| 36-37 | first major-key cadence (D-flat) | the first light in the piece |
| 45 | 4-3 suspension bes'-a' pivots A-flat → b-flat | the light dims |
| 49-51 | tonic pedal (S1 in the bass) under C7/B-flat → F/A | the combination begins as dominant against tonic |
| 58:3 | Neapolitan 6th → i6/4 | prepares the climax pedal |
| 59-62 | dominant pedal = A1 augmented; sus4-3 and b9-8 at once | rectus and inversus heads are the two classic dominant appoggiaturas |
| 66-67 | diminished 7th over the tonic bass (fff) → v7 → IV6 → French sixth, with a chromatic bass slide g-ges-f | the peak; the subject's own landing is the third of the augmented sixth |
| 68 | V4-3 → V7, fermata, general pause | the Beethoven silence |
| 75 | minor iv inside the major theme (theme bar 7) | the major carries the memory of the minor |
| 78 | deceptive cadence V7 → bVI | withholds the final tonic once more |
| 79-81 | plagal iv(minor) → I over a tonic pedal, with the inverted sigh f-ges-f in an inner voice | "Amen" with a lament in it |

### C7. Dynamics arc
- **I:** p. The subject alone, sostenuto. Growing to mp by bar 15, with the bass
  entry heard in three voices.
- **II:** subito pp, sotto voce, a veiled mirror section.
- **III:** mp, with a steady crescendo as the entries pile up. f at 35-36, the
  arrival in D-flat.
- **IV:** subito p dolce. The lyrical plateau, never above mp.
- **V:** mf → f, poco a poco animando.
- **VI:** ff at 59, where all four voices are thematic. fff at 66 on the dim7; the
  French sixth at 67:3 is the harshest chord. Fermata, then silence.
- **VII:** pp; the theme begins sotto voce in B-flat major. Crescendo to ff at 74
  (the theme's high f'').
- **Coda:** subito p at the deceptive cadence (78), diminuendo to ppp.

The climax sits at bars 59-68, at 78% of the duration. The apotheosis's ff (bar 74)
is a second, brighter peak. The piece ends quietly and transfigured rather than
triumphant, which answers the complaint "too happy".

### C8. Free-voice plan (what fills the rests of the skeleton)

The skeleton fixes every thematic statement. The free counterpoint below has to be
composed, and each passage checked in a lab, following the E1 exposition as the
model:

| bars | voice | material | notes |
|---|---|---|---|
| 19-22 | A | from the tied ees' (third of the 6/4) → d' (V), then a descending half-note lament c'-bes-aes-g over the G pedal | the fourth voice of the mirror trio; pp |
| 23-26 | S | CS2's tetrachord cell in F minor, high and light (c''' bes'' aes'' g'' / f'' g'' aes'' bes'') | ppp; or the I1 × I1 stretto from B3 |
| 27-31 | S | CS1 above the alto's S1 (CS1 over S1 is P02), at the f'' level: f'' ges'' g'' aes'' bes'' c''' ... | the lament returns with the chain |
| 31-36 | A (from 31:3), T (from 33:3), B (from 35:3) | each voice leaving its subject continues with CS1's chromatic fall or CS2's tetrachords, one per voice, so the texture thickens | crescendo to f at 35 |
| 37-40 | T | quarter-note motion under CS3 (CS2's cell, now in D-flat major) | keep below CS3 |
| 41-48 | S (from 41:3) | a descant built on S2's leap figure (f''8 bes' → aes''8 des'') | mp at most |
| 45 | A | the answer's landing bes' held as a 4-3 suspension → a' over F | the pivot back to b-flat |
| 49-53 | T | from c' (the seventh of C7/B-flat) a slow lament: c'-b-bes-a-aes-g in halves | the CS1 fall at half speed |
| 54-58 | B | bass of the e-flat combination: ees ... ending f (58:1) - ees (58:3, N6 bass) - f (59:1) | N6 → i6/4 over the pedal |
| 63-64 | A, T | CS1 and IC1 as a chromatic wedge in contrary motion, reaching the written X1 voicing at 65 | cresc. to fff |
| 65-69 | all | WRITTEN: lab `X1_climax_exit.ly` | checker clean |
| 69-77 | T, B | chorale foundation: tonic pedal bes (69-70), ees (IV, 71-72), then half-note root motion per C5; the tenor in CS1-shaped steps | the bass may double in octaves on the piano at ff |
| 75-84 | all | WRITTEN: lab `X2_coda.ly` (the theme's last bars, the deceptive cadence, the plagal Amen) | checker clean |

## D. Risks and honest caveats

1. **About 35% of the voice-bars are free counterpoint** (C8) and are not yet
   written or checked. The skeleton proves only that the thematic statements and
   their joints are clean. The exposition (fully written, clean) shows the standard
   those passages must meet.
2. **Bimodality at 49-53.** S2 in F major (a, e natural) sounds over S1 in B-flat
   minor (des''). It is clean on paper (P10_CS2_S2Mu_S1, strict 0) and is meant as a
   foretaste of the major. The e''/bes' tritone at 49:2.5 and the des''/a'
   neighbourhood at 52:4 must be confirmed by ear.
3. **The climax (P12) is dense by design:** 7 accented dissonances in 4 bars, all
   pedal-based. If it sounds congested on the piano, thin the alto's S2 to its
   first 2 bars and continue it freely.
4. **Keyboard spans, bars 59-63.** Tenor bes-ees' over the bass F, spans up to 22
   semitones. On the piano, sustain F, (octave F,/F) with the sostenuto pedal and
   take the tenor in the left hand. In bars 11-18 the lower-staff span is 14
   semitones or less. On the quartet, the cello's F2 is comfortable.
5. **Register limits.** The soprano reaches c''' (84) in the free CS1 at bar 28 and
   bes'' in IC2 (bar 22). The apotheosis theme stays at bes' (its top note f'' = 77),
   so the ff at bar 74 must come from the full texture below, not from register.
6. **Exposition length.** The exposition is 18 bars (47 s). The four solo bars (10 s)
   are deliberate: the theme is heard at its original pitch before anything else.
7. **Checker leniency.** tools/check.py accepts accented passing dissonance and
   "ESC?" figures. That is why every lab here was also run through the stricter
   filter and every remaining item is explained above. The CS1/IC1 crossings (P08)
   fail that standard and are deliberately kept out of the form.
8. **Tone.** B-flat minor, the lament CS1, the mirror section at pp and the quiet
   plagal ending answer "too happy". The only extended major passages are the
   D-flat S2 exposition (dolce) and the apotheosis, and even there the minor iv
   returns (bars 75 and 79-81).
