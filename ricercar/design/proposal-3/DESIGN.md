# Proposal 3: "Ricercar cromatico" on the Theme from Jurassic Park

Designer #3 (chromatic depth). Double fugue a 4, B-flat minor to B-flat major, 62 bars, about 3'50".
Every contrapuntal claim below is backed by a lab file in `lab/` that passes `tools/check.py`
(0 PAR!, 0 BEAT, 0 DIS!) and a stricter second opinion (`lab/strict.py`).

## 0. Concept

The theme's first phrase barely moves: a held tonic circled by its leading tone. So the piece treats it
as Bach treats the Royal Theme and the C-sharp minor subject, as a slow cantus with chromatic lines
moving round it. All the chromaticism grows from one cell, **the semitone neighbour of a held note**:

- S1 circles B-flat from below (a).
- The lament countersubject circles the dominant F from above and below (g-ges-f-e-f-ges-f).
- The mirror of S1 circles F from above (ges, the Phrygian b6), and on B-flat it circles from above with
  c-flat, the Neapolitan.
- The mirror lament circles B-flat from both sides (a below, c-flat above).

The large form is a descent and a return, and the tonal plan is itself a mirror. The first half sinks
flatward (B-flat minor, E-flat minor) to a crisis on the Neapolitan C-flat chord. The mirror section
climbs back note by note, like the inverted fugue of Op. 110 ("nach und nach wieder auflebend"). The
augmented answer in the bass then becomes the dominant pedal; the augmented sixth on its G-flat is the
climax; and the theme returns whole and untweaked, in B-flat major, over the combination proven
earlier. The last melodic motion of the piece is the lament's ges-f, sounded under a B-flat major chord.

## A. Subjects and materials

LilyPond `\absolute`, c' = middle C. All materials are defined once, in `lab/mats.py`.

| name | role | LilyPond (B-flat minor unless noted) |
|---|---|---|
| **S1** | Subject I: theme bars 1-4, real rhythm | `bes'2. bes'8 a' \| bes'2. bes'8 a' \| bes'4. c''8 c''4. ees''8 \| ees''2. des''8 c'' \| bes'2` |
| **ANS** | real answer, F minor | `f''2. f''8 e'' \| f''2. f''8 e'' \| f''4. g''8 g''4. bes''8 \| bes''2. aes''8 g'' \| f''2` |
| **CS1** | countersubject 1, "lament": chromatic 6-b6-5-#4, then the Phrygian turn 5-b6-5 | `r2 g2 \| ges2 f2 \| e2 f2 \| ges2 f2` (first half-bar is free) |
| CS1-F | CS1 against the answer | `r2 d'2 \| des'2 c'2 \| b2 c'2 \| des'2 c'2` |
| **CS2** | countersubject 2, "cascade": a scale falling a ninth in syncopation (7-6 and 4/2-6 chains) | `r4 g'2 f'2 ees'2 des'2 c'2 bes2 a2 c'4 \| des'2` |
| CS2-F | CS2 against the answer | `r4 d'2 c'2 bes2 aes2 g2 f2 e2 g4 \| aes2` |
| **S2** | Subject II: theme bars 5-8 in minor, no tweak | `c''4. a'8 f'4 des''8 bes' \| c''2. f''8 bes' \| ees''4. des''8 des''4. c''8 \| c''1` |
| S2-sub | S2 in E-flat minor (entry E6) | `f''4. d''8 bes'4 ges''8 ees'' \| f''2. bes''8 ees'' \| aes''4. ges''8 ges''4. f''8 \| f''1` |
| S2-F | S2 at the fifth (entry E7, stretto) | `g''4. e''8 c''4 aes''8 f'' \| g''2. c'''8 f'' \| bes''4. aes''8 aes''4. g''8 \| g''1` |
| **S1I** | tonal mirror of S1 about D-flat (bes<->f, c<->ees, des<->des, a<->ges) | `f'2. f'8 ges' \| f'2. f'8 ges' \| f'4. ees'8 ees'4. c'8 \| c'2. des'8 ees' \| f'2` |
| S1I-sub | mirror in E-flat minor (entry E8) | `bes2. bes8 ces' \| bes2. bes8 ces' \| bes4. aes8 aes4. f8 \| f2. ges8 aes \| bes2` |
| S1I on bes | the mirror placed on B-flat, for the rectus/inversus wedge | `bes''2. bes''8 ces''' \| bes''2. bes''8 ces''' \| bes''4. aes''8 aes''4. f''8 \| f''2. ges''8 aes'' \| bes''2` |
| **CS1I** | mirror of CS1: rising chromatic 7-#7-1-b2, then a turn round the tonic | `r2 aes'2 \| a'2 bes'2 \| ces''2 bes'2 \| a'2 bes'2` |
| **CS2I** | mirror of CS2: a rising cascade (retardations) | `r4 aes2 bes2 c'2 des'2 ees'2 f'2 ges'2 ees'4 \| des'2` |
| **AUG** | the answer in augmentation (bass) = the dominant pedal; last beat tweaked | `f,1~ \| f,2 f,4 e,4 \| f,1~ \| f,2 f,4 e,4 \| f,2. g,4 \| g,2. bes,4 \| bes,1~ \| bes,2 aes,4 ges,4 \| f,1` |
| **S1M / S2M** | major forms (apotheosis) | S1 and S2 with d for des |
| **THEME-M** | the whole theme, untweaked, B-flat major (apotheosis soprano) | `bes'2. bes'8 a' \| bes'2. bes'8 a' \| bes'4. c''8 c''4. ees''8 \| ees''2. d''8 bes' \| c''4. a'8 f'4 d''8 bes' \| c''2. f''8 bes' \| ees''4. d''8 d''4. c''8 \| c''1` |
| ANS-M, CS2-M | answer and cascade in major | `f'2. f'8 e' \| f'2. f'8 e' \| f'4. g'8 g'4. bes'8 \| bes'2. a'8 g' \| f'2`; `r4 g'2 f'2 ees'2 d'2 c'2 bes2 a2 c'4 \| d'2` |

### Tune tweaks (each one justified)

1. **S1, bar 4: `des''8 bes'` becomes `des''8 c''`, then `bes'` on the next downbeat.** The theme's
   own bar 5 starts on c'', so no new note is added; the two notes are simply reordered. The subject now
   closes 4-3-2-1 on the tonic instead of stopping on a pickup (flaw 1 of the old piece). Twice the
   original is restored as a structural event: at the climax the alto runs S1 straight into S2 with
   Williams's own pickup (bar 46), and the apotheosis soprano plays the theme untweaked.
2. **Minor mode** (d -> des) everywhere before bar 52, including S2. Its a'-f'-des'' then outlines the
   augmented triad F-A-D-flat (III+ of the harmonic minor): the darkest colour the tune can take without
   changing a single rhythm.
3. **AUG, last beat: `aes,4 g,4` becomes `aes,4 ges,4`.** The augmented answer's final descent becomes
   the Phrygian tetrachord bes-aes-ges-f, so the climax sounds an augmented sixth (French type, ges-c-e,
   third omitted) resolving to the
   dominant. This is one note of an eight-bar bass. The ear follows the augmentation by its long F
   pedal, not by that beat.

Nothing else in the theme is changed.

### Why a real answer

S1 never touches the fifth degree (bes-a-c-ees-des), so there is no 5^->1^ head to mutate. A real
answer at the fifth keeps the leading-tone neighbour (f-e-f), which is the subject's identity.

### Why these countersubjects

| line | rhythm | intervals | function |
|---|---|---|---|
| S1 | dotted halves, 8th-note neighbour pickup | static tonic, a rising fourth | cantus |
| CS1 | halves on beats 1 and 3 | chromatic semitones round the dominant | harmonic lament; the "passus duriusculus" |
| CS2 | halves on beats 2 and 4 (syncopated) | diatonic scale falling a ninth | suspension chain |
| S2 | dotted quarter + 8th, leaps of a sixth | arpeggio, augmented triad | lyrical second subject |

In S1+CS1+CS2 no two lines move together except at cadences: S1 moves at 4.5, CS1 on 1 and 3, CS2 on 2
and 4. The composite is a steady quarter pulse. Continuous 8ths first appear in Episode 1 (bar 18);
Part II brings S2's dotted 8th rhythms; the climax brings the widest leaps and the densest chromatic
harmony. The surface therefore accelerates with the form, which the old two-bar blocks never did.

The two countersubjects are opposite in character: CS1 is chromatic and on the beat, CS2 diatonic and
off the beat. Together they sound what the old piece's "3rds/6ths filler" never had: real 7-6 and 4/2-6
suspensions (bars 11-13), and chromatic harmony (Dorian IV turning to iv, vii7/V, Phrygian iv6-V7).

## B. Proof table

`check.py` = `tools/check.py` with the ricercar ranges (run with `lab/run.sh FILE`). `strict.py` =
`lab/strict.py FILE -v`, a second opinion that flags what check.py accepts as "PT/NT":

- CLASH: augmented unison or octave, e.g. g against ges.
- XREL: cross relation within a quarter.
- ACC: dissonance on beat 1 or 3 that is not a prepared suspension.
- ACC2: the same, with both notes struck together.

Every remaining ACC/ACC2 is listed and explained. "6/4 over pedal" means a fourth above a held pedal
note; that is the normal pedal-point licence.

| # | claim | lab file(s) | check.py | strict (explained) |
|---|---|---|---|---|
| 1 | S1/CS1/CS2 triple invertible counterpoint at the octave, **all 6 vertical orders** | `03_triple_*.ly` (6) | 0/0/0/0 in all six | clash 0, xrel 0 in all; ACC2 0,1,0,2,1,2: only where S1 or CS1 is the lowest line (4/2 passing chord on 3:1, passing 6/4 on 3:3) |
| 2 | Mirror texture S1I/CS1I/CS2I (Contrapunctus-12 style rectus/inversus), **all 6 orders** | `04_mirror_*.ly` (6) | 0/0/0/0 in all six | clash 0, xrel 0; ACC2 0,2,0,1,2,1 |
| 3 | Whole exposition, 4 voices, bars 1-18 (answer, CS1, CS2, codetta, free bass) | `01_exposition.ly` | errors 0, parallels 0, beat-par 0, unjustified 0 | clash 0, xrel 0, acc 0, acc2 1 (7:1, tritone f'/b in two voices = vii7/V of F minor) |
| 4 | S1 (answer form, f') + S2 entering two beats later a fifth above it (c'') + CS2: **triple counterpoint, all 6 orders** (the S1+S2 combination) | `05_combo_*.ly` (6) | 0/0/0/0 in all six | clash 0, xrel 0; ACC 0,2,0,0,2,0 (a 4th over S2 only when S2 is the lowest line) |
| 5 | The same combination in B-flat major (apotheosis) and S1M/CS1/CS2-M in major, all 12 orders | `09_combomaj_*.ly`, `09_triplemaj_*.ly` | 0/0/0/0 in all twelve | clash 0, xrel 0; max ACC2 2 |
| 6 | S2 stretto at the upper fifth, one bar apart, over the answer in the bass (entry E7) | `06_stretto_S2.ly` | 0/0/0/0 | ACC2 1 (4:3: S2's final c' against S2-F's bes', a 9th over the bass b-flat; it becomes consonant when the bass moves to a-flat on the next beat) |
| 7 | S1 half-bar stretto (answer a fourth below, two beats later) | `07_stretto_S1.ly` | 0/0/0/0 | 0 / 0 / 0 / 0 |
| 8 | Crisis (vii7 -> Neapolitan) and mirror section in 4 voices, bars 34-43 | `10_crisis_mirror.ly` | 0/0/0/0 | acc 1, acc2 6, all explained in C.6 (dim7 over its bass, Gb7/Fb = V4/2 of the Neapolitan, a passing 6/4, leading tone over tonic pedal, Db7 upper-neighbour seventh, 6/4 over the dominant pedal) |
| 9 | Climax bars 43-51: augmented answer (= dominant pedal) + S1 + its mirror on the same B-flat (rectus/inversus wedge) + CS2; then the whole theme in the alto under a descant; augmented sixth on the bass g-flat | `08_climax.ly` | 0/0/0/0 | acc2 5: four are the i6/4 over the F pedal, one is a passing 6/4 over the bass g, (bar 48.1) |
| 10 | Apotheosis + coda, 4 voices, B-flat major, bars 52-62 | `09_apotheosis.ly` | 0/0/0/0 | acc 1 (iv6/4 over the tonic pedal), acc2 1 (passing seventh f'-ees'-d' of V7) |
| 11 | E7 (S2 stretto over the answer, bass tacet) + Episode 2 (bass re-enters f, and climbs g, aes, a, bes, b, c under the held g'') + the crisis chord, 4 voices, bars 28-34 | `12_stretto_to_crisis.ly` | errors 0, parallels 0, beat-par 0, unjustified 0 (one DIR: S2-F's leap g''-e'' against the answer's f-e, a hidden octave between two subject statements on a weak 8th) | clash 0; xrel 1 (tenor des' then alto d'', covered by the alto's own des''-d''); acc2 3 (bes''/c'' = the two subjects' 7-6 at 31.3; the tritones of the two diminished sevenths at 33.3 and 34.1) |
| 14 | E5-E6: S2 with the answer (three voices) and S2-sub with S1 and the cascade plus a free alto, bars 20-28 | `13_second_subject.ly` | errors 0, parallels 0, beat-par 0, unjustified 0 | clash 0, xrel 0, acc 0, acc2 0 |
| 15 | Episode 1 on the dominant pedal, in context (bars 17-20) | `14_episode1.ly` | errors 0, parallels 0, beat-par 0, unjustified 0 (one D4?: alto bes' over the F pedal at 19.1 = i6/4 over the pedal) | acc 5, all against the held F pedal (IV/V, i6/4, the seventh of V7) |
| 16 | **The whole design spliced into one 62-bar file** (labs 01, 14, 13, 12, 10, 08, 09 joined by time; joins at 18, 20, 28, 34, 43, 52 checked) | `99_assembled.ly` (made by `assemble_check.py`) | **errors 0, parallels 0, beat-par 0, unjustified 0**; one D4? (19.1, 6/4 over the dominant pedal), one DIR (29.4.5, the hidden octave of row 11) | clash 0, xrel 1, acc 7, acc2 13: every item is one already explained in rows 3-15 |
| 12 | Double counterpoint at the 10th and 12th: **CS1 against CS2 is invertible at the 8ve, 10th and 12th** | `11_cs1cs2_10th.ly`, `11_cs1cs2_12th.ly` (8ve: lab 03) | 0/0/0/0 both | clash 0, xrel 0, acc 0, acc2 0 both |
| 13 | Negative result, kept on purpose: S1 against CS1 or CS2 is invertible **only at the octave**. Moved a 10th or 12th, each countersubject lands in another key and makes augmented-octave clashes (b' against bes', g against ges) | `11_s1cs1_*_fails.ly`, `11_s1cs2_*_fails.ly` | check.py passes 3 of 4 (it cannot see clashes); the 12th/CS2 case has a range error | clash 1-2 in all four: **not used** |

Additional verified facts, from searches run through the real checker (reproduce with `lab/p3.py`,
`pair_search2`):
- S1 fits S1 in stretto at 2 beats a 4th or 5th below, and at 2 or 4 beats a 6th above (strict-clean).
- S1 + its mirror started on the same B-flat is clean at distance 0, mirror above or below (the wedge).
- S2 + S2-F at 3 beats is clean with S2-F above; S2 + S2 at the octave below after one bar is clean.

## C. Architecture

### C.1 Meter, tempo, duration

4/4 throughout (the theme's own meter and rhythm; S1 is never halved or doubled except for AUG).

| bars | marking | quarter | beats | seconds |
|---|---|---|---|---|
| 1-33 | Grave, ma non troppo | 69 | 132 | 114.8 |
| 34 | fermata on the Neapolitan + short G.P. | 69 | 4+3 | 6.1 |
| 35-42 | Più lento, dolente (mirror) | 63 | 32 | 30.5 |
| 43-50 | Tempo I, pesante | 69 | 32 | 27.8 |
| 51 | fermata on V | 69 | 4+2 | 5.2 |
| 52-59 | Maestoso, luminoso | 63 | 32 | 30.5 |
| 60-62 | coda, ritardando to about 52, final fermata | ~57 | 12+2 | 14.7 |
| **total** | | | | **229.6 s = 3'50"** |

Checked by rendering: `tools/perform.py lab/99_assembled.ly lab/plan_sketch.json` (tempo map above, with a
ritardando in 33 and 50, fermatas at 34.3, 51.1 and 62.1, breaths before 20, 35, 43 and 52) gives
**231.3 s** of MIDI.

Bar count 62. Proportions: the first crisis falls at bar 34 (0.55 of the bars), the climax at bar 50.4
(0.81), the apotheosis starts at 0.84: the late-Beethoven placement.

### C.2 Form table

| bars | section | content | key |
|---|---|---|---|
| 1-4 | **I. Exposition** E1 | bass S1, alone | b-flat |
| 5-8 | E2 | tenor ANS; bass CS1-F (after S1's last note) | f |
| 9 | codetta | f -> V6 -> i (bass f c bes, a,) | f -> b-flat |
| 10-13 | E3 | alto S1, tenor CS1, bass CS2 (order S1>CS1>CS2) | b-flat |
| 14-17 | E4 | soprano ANS, alto CS1-F, tenor CS2-F, free bass | f |
| 18-19 | Episode 1 | two bars on a dominant pedal (bass f,): soprano runs S1's 4-3-2-1 tail in 8ths, sequenced down by step (f''-c'', ees''-bes', des''-a'), the first continuous 8ths of the piece; alto and tenor in half and quarter notes: fm, Eb/F, bbm6/4, F, F7 | f -> V of b-flat |
| 20-23 | **II. Second subject** E5 | alto S2 from 20.3; tenor ANS from 20.1; bass CS2-F from 20.2 (cadence f, e, f,); **soprano tacet** (three voices); S2's last c'' resolves 9-8 to bes' at 24.2 | b-flat (on its dominant) |
| 24-27 | E6 | soprano S2-sub from 24.3 (re-entering after four bars' rest); bass S1 from 24.1; tenor CS2 from 24.2; alto tacet 24.3-25, then free (f' g' ees' \| ees' c'' c'' -> des'' at 28.1) | e-flat (on its dominant) |
| 28-31 | E7 = S2 stretto | tenor ANS on f from 28.1; alto S2 from 28.3; soprano S2-F from 29.3 (one bar later, upper fifth; its last note g'' is held 32.3-33.3); **bass tacet** (three voices) | b-flat / f |
| 32-33 | Episode 2 | the bass re-enters on f, (32.1) and climbs in quarters g, aes, a, bes, b, to c (34.1), under the soprano's held g'' (starting on g, so that no ges sounds against it); quarter-note chords Eb/G, Ab maj7, A half-dim7, b-flat m6, B dim7; cresc. molto | -> |
| 34 | **Crisis** | 34.1 vii7 over c (c ees ges a), ff; 34.3 C-flat major in root position (the Neapolitan), subito p, fermata, G.P. | b-flat: N |
| 35-38 | **III. Mirror** E8 | tenor S1I-sub (bes-ces-bes), alto CS2I-sub, bass CS1I-sub (des, d, ees, fes, ...); soprano tacet | e-flat |
| 39-42 | E9 | soprano S1I (f''-ges''-f''), alto CS1I, tenor CS2I; bass tonic pedal, then des, ees, f, ges, -> f, | b-flat |
| 43-46 | **IV. Dominant pedal** | bass AUG (F pedal); alto S1 on bes' + soprano S1I on bes'' (rectus and inversus from one note); tenor CS2 | V of b-flat |
| 47-50 | climax | bass AUG rises f g bes then falls bes aes ges; alto S2 with the theme's original pickup (the whole theme, minor); soprano descant peaking on c''' at 50.4 | V -> aug. 6th |
| 51 | | V (F major), fermata | V |
| 52-55 | **V. Apotheosis** | soprano THEME-M bars 1-4; alto CS2-M (cascade) cut at 55.2; bass tonic pedal, IV, V7, I6 | **B-flat major** |
| 55-59 | | soprano THEME-M bars 5-8 (= S2M, from 56.1); alto ANS-M from 55.3; bass CS2-M in the answer frame (d c bes a g f e g a) from 55.4; tenor free | B-flat |
| 60-62 | **Coda** | V7-I; tonic pedal; soprano S1 head; I - iv6/4 (minor, ges) - vii7 over the pedal - I | B-flat |

### C.3 Tonal plan and its logic

`b-flat -> f` (exposition) `-> b-flat -> e-flat` (S2 entries on the dominants of i and iv) `-> b-flat/f`
(stretto) `-> C-flat` (Neapolitan crisis) `|| e-flat -> b-flat` (mirror) `-> F` (pedal) `-> B-flat`.

- The first half goes flatward by fifths (i, iv, then bII, the flattest point) and the second half comes
  back by fifths (iv, i, V, I). The tonal plan is a mirror, like the counterpoint of its middle section.
- The Neapolitan is prepared motivically, not only harmonically. The mirror subject on B-flat has c-flat
  as its neighbour, so C-flat is the one chord that literally "is" the inverted subject. The tenor's
  c-flat falls to b-flat and so begins the mirror section.
- C-flat is VI of E-flat minor, which is why the mirror section can begin in e-flat with no modulation.
- The climax chord (an augmented sixth over g-flat) is the same b6-5 as the lament's turn and the S1 mirror's
  neighbour. Its G-flat7 colour is enharmonically the dominant of C-flat, so the climax reinterprets
  the crisis.
- The B-flat major triad is never a goal before bar 52. D natural appears only as a passing Dorian
  colour (E2, E4, CS2-F) or as the leading tone of E-flat minor (E6, E8), so the major third of the
  apotheosis sounds new.

### C.4 Entry table

| entry | bar.beat | voice | form | key | first pitch |
|---|---|---|---|---|---|
| E1 | 1.1 | B | S1 | b-flat | bes, |
| E2 | 5.1 | T | ANS | f | f' |
| E3 | 10.1 | A | S1 | b-flat | bes' |
| E4 | 14.1 | S | ANS | f | f'' |
| E5 | 20.1 / 20.3 | T / A | ANS + S2 | b-flat | f' / c'' |
| E6 | 24.1 / 24.3 | B / S | S1 + S2-sub | e-flat | bes, / f'' |
| E7 | 28.1 / 28.3 / 29.3 | T / A / S | ANS + S2 + S2-F (stretto) | b-flat, f | f / c'' / g'' |
| E8 | 35.1 | T | S1I-sub | e-flat | bes |
| E9 | 39.1 | S | S1I | b-flat | f'' |
| E10 | 43.1 | B / A / S | AUG + S1 + S1I on bes | V pedal | f, / bes' / bes'' |
| E11 | 47.1 | A | S2 (after S1's original pickup) | b-flat | c'' |
| E12 | 52.1 | S | THEME-M (S1M + S2M) | B-flat | bes' |
| E13 | 55.3 | A | ANS-M (combined with S2M) | B-flat | f' |

Complete subject statements: S1 family 14 (including mirror, augmentation and major forms); S2 family 6.

### C.5 Harmonic outline (half-bar, at entries, cadences, climax)

- **E1** (1-4), solo: implied i | i (a = V) | i ii6/5 V | iv V7 | i.
- **E2** (5-8), bass CS1-F: i(b-flat) IV-Dorian (d) | VI iv... the lament d-des-c: `F: IV(maj) iv6 | V6/4 V | vii7/V V | iv6 V7 | i`.
- **Codetta** (9): f, V6 (a,), i at 10.1.
- **E3** (10-13), bass CS2 = chain of bass suspensions: `i | vi6-ish (g) 4/2->5/3 (f -> ees) iv | i6 4/2 (c) V/V (e in tenor) | V 4/3 ... iv6 V7 | i`.
- **E4** (14-17): `i(b-flat) IV(Bb, Dorian of f) V4/2 | VI7 (c suspended) iv6 V-sus4 v(4-3) | vii7/V (d) V/V V | iv V4/2 V7 | i (f)`.
- **E5-E6**: S2's bar 1 = V with the augmented triad (a-f-des) resolving to i/VI; bar 3 = iv -> i6 -> V; each S2 entry ends on V (half cadence) as the theme does. E6 = the same a fifth lower (e-flat).
- **E7** (28-31, three voices, ANS lowest): `V (4-3 in the answer's f-e) | i6 V/V(sus4-3) | v(f) iv | Eb7 (V7/iv) F-sus4 v`.
- **Episode 2** (32-33): `v | Eb/G Abmaj7 | A half-dim7 b-flat-m6 | B dim7` -> 34.1 C dim7: every voice rises a semitone into the crisis.
- **34**: `vii7 (c ees ges a) -> bII (ces ees ges, root position)`; the fermata sits on bII.
- **E8** (35-38, e-flat): the mirror's harmony is the lament's harmony read upward. At 37.1 comes Gb7/F-flat (V4/2 of C-flat, the crisis chord's own dominant), resolving fes -> ees.
- **E9** (39-42): i pedal (leading tone over the pedal) | Db7 (V7 of VI) -> iv | V (42.1) -> ges,-bes-c-ees (augmented-sixth colour) -> V pedal at 43.
- **43-46**: over the F pedal: i6/4 | IV/V (the "eleventh") | the wedge sounds V7 with lowered fifth at every 4.5 (a' against ces'''); vii7/V over the pedal's e,; F7 at 46.2.
- **47-51**: `V | vii7/V (bass g) | V/V 6/4 (C/G) | i (bass bes) | iv6/4 i | V4/2/V (C7/B-flat) | F-minor 6 (aes) | aug. 6th, French type without its third (ges c e) | V`.
- **52-55**: `I | vi6/5 IV6/4 (Williams) | I sus2 V | IV V4/2 V7 I6`.
- **56-59**: the descending cascade bass under S2M: `iii7 V6/4 | I V6 | ii IV6 I6/4 V/V6/5 | V6`.
- **60-62**: `V7 I | I iv6/4(minor) vii7-over-I | I`.

### C.6 Special harmonic events (and why each sits where it does)

| bar | event | why there |
|---|---|---|
| 2-4 of every S1 entry | Phrygian iv6 -> V7 -> i (CS1's turn f-ges-f) | the subject's 4-3-2-1 ending always lands through the b6 |
| 5-6, 14-15 | Dorian IV (major) turning to iv inside one lament step (d -> des) | the answer is coloured by mixture; the ear learns early that major and minor are neighbours |
| 11-13 | suspension chain 4/2 -> 5/3, 7-6 (CS2 in the bass) | first real counterpoint density, still pp |
| 20-27 | augmented triad III+ (a-f-des) inside S2 | the lyrical subject is made strange, not happy |
| 34 | vii7 ff -> Neapolitan subito p, fermata | end of the first wave; the flattest point of the tonal mirror |
| 37 | Gb7/F-flat, V4/2 of the Neapolitan | the crisis chord is recalled inside the mirror |
| 39-40 | leading tone over the tonic pedal | rebirth from the tonic: the mirror texture starts on a pedal as the exposition started on a held note |
| 43-46 | rectus and inversus from one B-flat over the augmented answer: V7 with lowered fifth at each 4.5 | four forms of the subject at once (rectus, inversus, augmentation, plus CS2) |
| 50.4 | augmented sixth over g-flat (French type, third omitted), soprano c''' (apex of the piece) | the climax; ges = the lament's b6 in the bass |
| 51 | V with fermata, caesura | Beethovenian breath before the major |
| 52-53 | Williams's own IV6/4 over the tonic pedal | the film harmony, once, at the moment the tune becomes itself |
| 61 | minor iv6/4 over the tonic pedal, then vii7 over the pedal | the minor's shadow; the tenor's ges -> f is the last melodic step of the piece |

### C.7 Dynamics arc

| bars | level |
|---|---|
| 1-4 | pp (one voice) |
| 5-13 | p, poco cresc. with each entry |
| 14-19 | mp |
| 20-27 | mf, espressivo (S2) |
| 28-31 | f |
| 32-33 | cresc. molto |
| 34.1 | ff (dim7) -> 34.3 subito p (Neapolitan), fermata, G.P. |
| 35-38 | pp, dolente, three voices |
| 39-42 | p, poco a poco cresc. |
| 43-46 | mp -> f |
| 47-50 | f -> ff; 50.4 fff (augmented sixth) |
| 51 | ff, dim. on the fermata |
| 52-55 | **subito p**, dolce luminoso, cresc. |
| 56-58 | f -> ff (S2M's f'' and ees'' peaks) |
| 59 | dim. |
| 60-62 | p -> pp, final chord pp |

Two waves: the first peaks at the crisis (34), the second at the augmented sixth (50.4). The apotheosis
starts quietly and grows, so the brightest major sonority (57-58) is also the loudest.

### C.8 Notes for the composer (free parts)

- **Episode 1 (18-19)**: written out and proven in `14_episode1.ly` (in context with bars 17 and 20).
- **Textures of Part II**: E5 and E7 are deliberately three-voice (soprano tacet, then bass tacet); this
  thins the middle of the piece and makes the re-entries (soprano S2-sub at 24.3, bass chromatic climb
  at 32.1) into events. If the composer adds a free fourth voice, it must avoid `g` against `ges`: S2
  and CS1 must never sound together, because CS1's ges clashes with S2-F's g (verified CLASH). Use CS2
  with S2, never CS1. A trial soprano descant over E5 produced parallels with the cascade bass at every
  attempt, which is why the rest is written into the design.
- **Episode 2 (32-33)**: written out and proven in `12_stretto_to_crisis.ly`; the composer may add
  inner-voice 8ths (S1's neighbour cell) as long as the lab stays clean.
- **Keyboard**: upper staff S+A, lower T+B, except in 10-13 where the soprano rests and the right hand
  takes alto and tenor. In 43-46, 39-40, 52-53 and 61-62 the pedal notes are caught with the sostenuto
  pedal, so that the left hand is free for the tenor line. In the quartet everything is literal: violin
  I = S, violin II = A, viola = T, cello = B. Every lab respects the ranges; the lowest viola note used
  is e (bar 17), the cello goes down to des, (bar 35), the first violin up to c''' (bar 50).
- **Performance roles** for `tools/perform.py`: role `subject` for every S1/S2/ANS/mirror/AUG
  statement in the entry table, `cs` for CS1/CS2 and their mirrors, `free` otherwise. Breaths before 20,
  35, 43 and 52. Fermatas at 34.3 (+3 beats) and 51.1 (+2 beats); pedal (piano) re-taken each half bar
  in 52-62.

## D. Risks (honest)

1. **Coverage.** Every bar exists in a checked lab, and the spliced whole (`99_assembled.ly`, row 16)
   passes the checker. It is a proof that the design closes, not a finished score. The inner voices
   of 20-33 and 52-59 are plain, and the composer should enrich them (8th-note motion from S1's
   neighbour cell) and re-run `lab/run.sh` and `lab/strict.py` after every change.
2. **Three-voice stretches** (E5, E7, E8) are a deliberate choice. If a fuller sound is wanted, the fourth
   voice is the composer's to add and to re-check.
3. **The checker is lenient.** check.py accepts any stepwise dissonance, even struck on the beat. The
   strict script catches that, and every residual ACC2 is explained above. Its cross-relation test is
   heuristic, so the ear should still review 20-33.
4. **Pedal-point sonorities** (43-46) are deliberately harsh: V7 with a lowered fifth and a' against
   ces'''. On piano they need the sostenuto pedal and careful voicing; on strings, clean intonation of
   the ces''' (= b'') against a'.
5. **Hand spans**: E4 bar 14 (tenor d' against bass bes,, a tenth). Either roll it, or play the bass an
   octave higher on the piano only.
6. **Tempo sensitivity**: the 229.6 s total assumes the tempo map above. At q = 72 throughout (no
   slower sections) the piece would last 207 s, under the minimum, so the slower mirror and apotheosis
   tempi are part of the design, not decoration.
7. **The mirror tweak des <-> des** makes the inversion tonal, not exact. This is standard practice, but
   the chromatic mirror (with d natural) would sound wrong in minor, so the mirror table in A is the rule.
8. **Invertibility is at the octave only for S1 with its countersubjects** (row 13). The 10th/12th
   devices of the Art of Fugue are therefore confined to the pair CS1/CS2 (row 12). If the composer
   wants a 12th inversion in an episode, use CS1 over CS2 raised a twelfth (lab 11), not S1.
