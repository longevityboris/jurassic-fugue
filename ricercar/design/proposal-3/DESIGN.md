# Proposal 3: "Ricercar cromatico" on the Theme from Jurassic Park

Designer #3 (chromatic depth). Status: materials and core proofs verified; architecture in progress
(sections marked DRAFT are not yet backed by a lab).

## 0. Concept in one paragraph

The theme's first phrase is almost motionless (a held tonic circled by its leading tone), so the piece
treats it the way Bach treats the Royal Theme and the C-sharp minor subject: as a slow cantus around
which chromatic lines move. Everything chromatic grows out of one idea, the **semitone neighbour of a
held note**: S1 circles B-flat from below (a); the lament countersubject circles the dominant F from
above and below (g-ges-f-e-f-ges-f); the mirror form of S1 circles F from above (ges, the Phrygian
b6); the mirror lament circles B-flat from both sides (a and c-flat, leading tone and Neapolitan). The
large form is a descent and a return: the first half sinks flatward (B-flat minor, E-flat minor, the
Neapolitan C-flat chord at the crisis), the mirror section rises again note by note ("nach und nach
wieder auflebend", Op. 110), the augmented answer in the bass becomes the dominant pedal, the German
sixth on its G-flat is the climax, and the theme returns whole, in B-flat major, over the combination
that has been proven all along.

## A. Subjects and materials

All LilyPond `\absolute`, c' = middle C. Material file: `lab/mats.py` (single source for every lab).

| name | role | LilyPond (B-flat minor frame unless noted) |
|---|---|---|
| **S1** | Subject I (theme bars 1-4, real rhythm) | `bes'2. bes'8 a' \| bes'2. bes'8 a' \| bes'4. c''8 c''4. ees''8 \| ees''2. des''8 c'' \| bes'2` |
| **ANS** | real answer, F minor | `f''2. f''8 e'' \| f''2. f''8 e'' \| f''4. g''8 g''4. bes''8 \| bes''2. aes''8 g'' \| f''2` |
| **CS1** | countersubject 1, "lament" (chromatic 6-b6-5-#4, Phrygian turn 5-b6-5) | `r2 g2 \| ges2 f2 \| e2 f2 \| ges2 f2` (first half-bar free) |
| CS1-F | CS1 in the answer | `r2 d'2 \| des'2 c'2 \| b2 c'2 \| des'2 c'2` |
| **CS2** | countersubject 2, "cascade" (syncopated descending scale, 7-6 / 4-2 suspension chain) | `r4 g'2 f'2 ees'2 des'2 c'2 bes2 a2 c'4 \| des'2` |
| CS2-F | CS2 in the answer | `r4 d'2 c'2 bes2 aes2 g2 f2 e2 g4 \| aes2` |
| **S2** | Subject II (theme bars 5-8, minor, no tweak) | `c''4. a'8 f'4 des''8 bes' \| c''2. f''8 bes' \| ees''4. des''8 des''4. c''8 \| c''1` |
| S2-sub | S2 in E-flat minor (subdominant answer, used with S1 in B-flat minor) | `f''4. d''8 bes'4 ges''8 ees'' \| f''2. bes''8 ees'' \| aes''4. ges''8 ges''4. f''8 \| f''1` |
| S2-F | S2 at the fifth (used in the S2 stretto) | `g''4. e''8 c''4 aes''8 f'' \| g''2. c'''8 f'' \| bes''4. aes''8 aes''4. g''8 \| g''1` |
| **S1I** | tonal mirror of S1 (about D-flat: bes<->f, c<->ees, a<->ges) | `f'2. f'8 ges' \| f'2. f'8 ges' \| f'4. ees'8 ees'4. c'8 \| c'2. des'8 ees' \| f'2` |
| S1I on bes | the same mirror placed on B-flat (for the rectus/inversus wedge) | `bes''2. bes''8 ces''' \| bes''2. bes''8 ces''' \| bes''4. aes''8 aes''4. f''8 \| f''2. ges''8 aes'' \| bes''2` |
| **CS1I** | mirror of CS1: rising chromatic 7-#7-1-b2 and a turn round the tonic | `r2 aes2 \| a2 bes2 \| ces'2 bes2 \| a2 bes2` |
| **CS2I** | mirror of CS2: rising cascade (retardations) | `r4 aes'2 bes'2 c''2 des''2 ees''2 f''2 ges''2 ees''4 \| des''2` |
| **AUG** | answer in augmentation, bass, = the dominant pedal (last beat tweaked) | `f,1~ \| f,2 f,4 e,4 \| f,1~ \| f,2 f,4 e,4 \| f,2. g,4 \| g,2. bes,4 \| bes,1~ \| bes,2 aes,4 ges,4 \| f,1` |
| **S1M, S2M** | major forms for the apotheosis | `bes'2. bes'8 a' \| bes'2. bes'8 a' \| bes'4. c''8 c''4. ees''8 \| ees''2. d''8 c'' \| bes'2` and `c''4. a'8 f'4 d''8 bes' \| c''2. f''8 bes' \| ees''4. d''8 d''4. c''8 \| c''1` |
| ANS-M | answer form of S1M (F major), combined with S2M | `f'2. f'8 e' \| f'2. f'8 e' \| f'4. g'8 g'4. bes'8 \| bes'2. a'8 g' \| f'2` |

### Tune tweaks (each one justified)

1. **S1 bar 4: `des''8 bes'` becomes `des''8 c''`, then `bes'` on the next downbeat.** The theme's own bar 5
   begins on c'', so the notes are the same, only reordered: the subject now closes 4-3-2-1 on the tonic
   instead of stopping on a pickup (flaw 1 of the old piece). In the apotheosis the soprano plays the
   theme *untweaked* (`d''8 bes' | c''4.` ...), so the listener finally hears the original line.
2. **Minor mode** (d -> des) everywhere before the apotheosis, including S2 (a'-f'-des'' then outlines
   the augmented triad F-A-D-flat, III+ of the harmonic minor: the darkest colour the tune can take
   without changing a rhythm).
3. **AUG last beat: `aes,4 g,4` becomes `aes,4 ges,4`.** The augmented answer's final descent becomes
   the Phrygian tetrachord bes-aes-ges-f, so the climax chord on the bass G-flat is a German sixth
   (ges-bes-des-e) resolving to the dominant. This is a tonal adjustment of one note in a bass line
   that is eight bars long; the ear follows the augmentation by its long F pedal, not by this beat.

No other pitch or rhythm of the theme is changed.

### Why a real answer

S1 never touches the fifth degree (bes-a-c-ees-des), so there is no 5^->1^ head to mutate; a real
answer at the fifth keeps the leading-tone neighbour (f-e-f) which is the subject's identity.

### Character of the lines (why the countersubjects are independent)

| line | rhythm | interval world | function |
|---|---|---|---|
| S1 | dotted halves with an 8th-note neighbour pickup | static tonic, rising 4th | cantus |
| CS1 | half notes on beats 1 and 3 | chromatic semitones round the dominant | harmonic bass-line, "passus duriusculus" |
| CS2 | half notes on beats 2 and 4 (syncopated) | diatonic scale falling a ninth | suspension chain (7-6, 4/2-6) |
| S2 | dotted quarter + 8th, leaps of a sixth | arpeggio, augmented triad | lyrical second subject |

The composite rhythm of S1+CS1+CS2 is a steady quarter pulse in which no two lines move together
except at cadences: S1 moves at 4.5, CS1 on 1 and 3, CS2 on 2 and 4. Eighth-note motion is held back
for Part II (free voices round S2), sixteenths for the climax, so the surface accelerates with the form.

## B. Proof table

Checker = `tools/check.py` with the ricercar ranges (`lab/run.sh`). Strict = `lab/strict.py`, a second
opinion that flags what check.py lets through: CLASH (augmented unison/octave such as g against ges),
XREL (cross relation within a quarter), ACC/ACC2 (dissonance on beat 1 or 3 that is not a prepared
suspension; ACC2 = both notes struck together). ACC2 against a *pedal* (P4 over a held bass) is the
normal pedal-point exemption and is noted as such.

| claim | lab file(s) | check.py summary | strict |
|---|---|---|---|
| S1/CS1/CS2 triple invertible counterpoint at the octave: all 6 vertical orders | `lab/03_triple_*.ly` (6 files) | all 6: errors 0, parallels 0, beat-par 0, unjustified 0 | clash 0, xrel 0 in all; ACC2 0/1/0/2/1/2 (only when S1 or CS1 is the lowest line: the 4/2 passing chord on 3:1, a passing 6/4 on 3:3) |
| Mirror texture S1I/CS1I/CS2I, all 6 orders (rectus/inversus like Contrapunctus 12) | `lab/04_mirror_*.ly` (6 files) | all 6: 0 / 0 / 0 / 0 | clash 0, xrel 0; ACC2 0/2/0/1/2/1 |

(continued in later commits: answer + S2 combination, S2 stretto, augmentation, apotheosis, exposition)

## C. Architecture (DRAFT, being verified section by section)

See section C below once filled.

## D. Risks

(pending)
