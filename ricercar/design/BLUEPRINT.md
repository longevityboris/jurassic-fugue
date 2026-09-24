# BLUEPRINT: "The Neighbour", ricercar a 4 on the Theme from Jurassic Park

B-flat minor to B-flat major. 4 voices (S A T B), piano and string quartet. 4/4, **62 bars, 227.3 s**
(measured with `tools/perform.py` and `final-lab/plan.json`, piano and strings targets alike).

Everything musical in this document exists as notes in `final-lab/SK_final.ly`, the verified skeleton of
the whole piece: 62 bars, 4 voices, `tools/check.py` **0 errors, 0 PAR!, 0 BEAT, 0 DIS!**, strict.py
**0 CLASH**, compiles in LilyPond 2.26 without warnings. Composers enrich it section by section, in
parallel, and prove each section with `final-lab/splice_check.py` (section 7).

Base: proposal 2 (the complete, measured 62-bar skeleton and the "neighbour" concept). Grafts from
proposals 1, 3 and 4 are listed in section 1 with the reason for each, and so are the ideas rejected.

---------------------------------------------------------------------------------------------------

## 0. The idea in one paragraph

The theme opens with a lower neighbour, B-flat A B-flat (1, #7, 1). The piece is built from that gesture
at five scales. (1) In the subject it is stated twice and harmonised twice. (2) The countersubjects are
neighbour steps chained into a chromatic lament (CS1) and the neighbour cell in diminution (CS2). (3) The
tonal mirror turns the lower semitone B-flat/A into the upper semitone F/G-flat, the Phrygian sigh, so
the subject's i-to-V question becomes the inversion's V-to-i answer. (4) At the first climax the
neighbour is applied to a whole chord: four head entries on E-G-B-flat-D-flat slide down a semitone, E
dim7 into A dim7. (5) The tonal plan is the neighbour writ large: B-flat minor, A minor (reached because
V7 of B-flat is also the German sixth of A minor), F (the subject's own last note, held as a pedal), and
B-flat MAJOR. The frame is Op. 110 (fugue, collapse, arioso dolente, inverted fugue, radiant close); the
pedal combination has the density of the Hammerklavier and Op. 131 No. 1. The tune is withheld whole
until the end: first its halves are heard apart (S1 in the fugue, S2 in the arioso), then S2 and S1
together over the augmented inversion, and only at bar 51 the complete tune, untouched, in B-flat major,
over its own mirror, its open c'' finally rising to d''. The last word is the subject's neighbour
B-flat A B-flat in the tenor, over the tonic pedal.

---------------------------------------------------------------------------------------------------

## 1. Synthesis log: what was kept, grafted and rejected

| decision | source | why |
|---|---|---|
| Base: concept, materials, triple invertible counterpoint, stretto at the 4th, dim7 liquidation, arioso, German-sixth pivot to A minor, fuga inversa with its stretto, INV in augmentation as the pedal, plagal turn into the major | P2 | the only design fully written, checked and measured; the judges' execution winner |
| **Exposition re-ordered S-A-B-T, tune first alone in the soprano at its own pitch (bes')** | P1 (Op. 131 top-down idea), judges of execution and beauty | P2 began in the cello at B-flat2; recognition matters most for a user who heard the melody as "off". Realised with P2's own counterpoint: entry 3 is P2's proven order C2-C1-S at identical registers, entry 4 the proven order C2-S-C1 transposed down a perfect fourth (interval-identical to lab T4) |
| **The full lament in the bass under the last exposition entry** (CS1 at c,: aes, g, f, e, ees, des, c,) | P4 | gives the exposition gravity (P1's and P2's lower registers were thin); here it falls out of the permutation for free |
| Entry tails no longer collapse into four-octave unisons (13:3, 17:3) | beauty judge | CS2 and CS1 landings varied (f'' at 13, c'' at 17; CS1 tail a c' a) |
| **Four thematic forms at once over the pedal (44-45): S2 (A), S1 (T), the INV head (S), INV augmented (B)**, then the double pedal F2/F5 that becomes the climax wedge | P1 P12 and P3 wedge ideas, realised with P2 material | P2's S1+S2 combination was nominal and bars 42-46 were 2-3 voices; P1's quadruple lab had parallel 2nds and a unison. The INV head (not the whole INV) is what fits the C7 "light" at 48 |
| Tenor lament lead-in B-flat A A-flat G G-flat (42-43) into its S1 entry | P4 (lament over the pedal) | fills the pedal's first bars with CS1's chromatic fall, sus4-3 over V |
| **Apotheosis = proposal-4 P06 verbatim**: the whole tune untouched as cantus firmus (S) over its own mirror (B), then over the answer (B) against the answer's mirror (T); c'' rises to d''; minor-iv plagal shadow | P4, judges of beauty and execution | removes P2's unresolved sevenths, G-flat/G false relations and the bar-58 tonic close of the tune; P06 is 4-voice and clean |
| Williams's own IV6/4 over the tonic in the apotheosis (52:3) | P3 | already in P06; instant film recognition at the moment the tune turns major |
| The lament's G-flat to F as the last chromatic step (alto 60) | P3 | already in P06 (minor iv6/4 to I) |
| Coda (61-62): the subject's head B-flat A B-flat in the tenor, V7 over the tonic pedal, I | P1 X2 (head as 4-3 in the Amen), P2 concept | the neighbour that opens the piece closes it |
| Apotheosis tempo raised from quarter 63 to 69 | execution judge | P2's 63 was at the floor for recognising the tune |
| strict.py as a second checker (CLASH, XREL, accented dissonance) | P3 | check.py accepts any stepwise dissonance |
| perform plan with roles, fermatas, breaths, measured duration | P2 | concrete and reproducible |
| REJECTED: P3's reordered S1 ending (des'' c'' / bes') | beauty judge "fatal" | changes the tune's hook |
| REJECTED: P1's D-flat-major S2 exposition and fifths chain (bars 27-48) | time budget | would add about 20 bars (the piece is at 227 s of 240); P1's chain is a resource for Part III enrichment, not used |
| REJECTED: P4's fixed-register countersubjects | rigor judge | no invertibility; P2's triple counterpoint serves both roles |
| REJECTED: P2's apotheosis tenor mirror with G-flat, bar-58 close on B-flat | judges | see above |

---------------------------------------------------------------------------------------------------

## 2. Materials

All in `final-lab/materials.ly` (one `\absolute` variable per material, reference pitch = first
appearance in the piece). LilyPond, c' = middle C, B-flat minor unless stated.

### 2.1 Subject I (S1) = theme bars 1 to 5 beat 3, real rhythm, 19 beats (`subjectOne`)

    bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 | c''4. a'8 f'4

* Not one pitch or rhythm of the tune changes except the minor third (d to d-flat, THEME.md). S1 simply
  runs on through theme bar 5's falling arpeggio C-A-F and ends on F (5) over V. It never stops on the
  pickup notes (flaw 1 of the old piece).
* The tail C-A-F overlaps the next entry, so entries come every 4 bars with no codetta.
* Harmonisation as supplied by the countersubjects in entry 3 (9-13): `V4/2 of f - V6 | i ... vii°7 | i ... v6/4 | iv ... N6 - i | V`;
  entry 4 (13-17, in f): `I (tail) - V | i6 ... vii°4/3 | i V6 v6 v6/5 | iv6 N6/4 cad. 6/4 | V6 V`.
* The first bar is never one static chord: every accompanied statement harmonises bar 1 twice (entry 3:
  C7/B-flat then F/A; entry 4: F then V of f).

### 2.2 Answer (ANS), real, at the fifth, F minor (`answerOne`, first in the alto at f')

    f'2. f'8 e'8 | f'2. f'8 e'8 | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f'8 | g'4. e'8 c'4

Real, not tonal: the head is 1-#7-1 and S1 touches 5 only at its last note, so there is no 1-5
exchange to mutate, and a real answer keeps the leading-tone neighbour F-E-F that is the subject's
identity.

### 2.3 Countersubject 1, "Lament" (`csOne`, `csOneAnswer`)

    subject level (alto 9:4):   r2. f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4 | a4. c'8 f4
    answer level (soprano 5:4): r2. c''4 | aes''2. g''4 | f''4 e''4 ees''2 | des''2. c''4 | e''4. g''8 c''4

A rising sixth (the sigh), then the chromatic fall D-flat C B-flat A A-flat G-flat F: the chromatic
fourth of Bach's Thema Regium. Enters on the subject's beat 4, so the subject's head is heard alone. Its
tail swaps voices with the subject's tail (subject C-A, lament A-C). In stretto the tail takes the minor
dominant `aes4. c'8 f4`. Landing note is free (bar 13: `a4. c'8 a4`).

### 2.4 Countersubject 2, "Motor" (`csTwo`, `csTwoAnswer`)

    subject level (soprano 10):  r1 | bes'8 a'8 bes'8 c''8 des''8 c''8 ees''8 ges'8 | des''4 c''8 f''8~ f''2 | ees''8 f''8 ees''8 des''8 ces''4 des''4 | f'2.
    answer level (alto 14):      r1 | f'8 e'8 f'8 g'8 aes'8 g'8 bes'8 des'8 | aes'4 g'8 c''8~ c''2 | bes'8 c''8 bes'8 aes'8 ges'4 aes'4 | c'2.

The neighbour cell in diminution, rising (bar 2), then its mirror falling through the Phrygian
tetrachord (bar 4), which puts a Neapolitan (C-flat major) under the subject's held E-flat (12:3).
Rhythm complementary to S1: eighths where S1 holds, a held note where S1 moves. Landing note free (13:
f'', 17: c'').

**S1, CS1, CS2 are triple invertible counterpoint at the octave: all six vertical orders are proven**
(labs T1-T6). The exposition uses two of them in real time: C2-C1-S (bars 9-13, identical registers to
T3) and C2-S-C1 (bars 13-17 = T4 transposed down a perfect fourth in all three voices).

### 2.5 Subject II (S2) = theme bars 5-8, 16 beats (`subjectTwo`)

    c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1

Begins with S1's tail and ends open on C over V (the theme's own half cadence). Used as the arioso's
melody (30-33), over the dominant pedal with S1 (42-45), and inside the whole tune (55-58, major).

### 2.6 Inversion (INV), tonal mirror (`inversion`, `inversionA`, `inversionE`)

    reference:            f''2. f''8 ges''8 | f''2. f''8 ges''8 | f''4. ees''8 ees''4. c''8 | c''2. des''8 f''8 | ees''4. ges''8 bes''4
    A minor (bass 35):    e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 | d4. f8 a4
    E minor (tenor 37):   b2. b8 c'8 | b2. b8 c'8 | b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4

Mapping: B-flat and F swap, C and E-flat, A and G-flat, A-flat and G; D-flat fixed. Starts on 5, ends on 1.
The lower neighbour B-flat/A becomes the upper neighbour F/G-flat (5, b6, 5).

### 2.7 Inverted countersubjects (A minor, Part III) (`csOneInv`, `csTwoInv`)

    CS1 inverted (alto 35:4): r2. a'4 | c'2. d'4 | e'4 f'4 fis'2 | gis'2. a'4 | f'4. d'8 a'2      (the lament rising)
    CS2 inverted (sop. 36):   e''8 f''8 e''8 d''8 c''8 d''8 b'8 g''8 | c''4 d''8 a'8~ a'4 b'4 | b'8 a'8 b'8 c''8 d''4 c''4

Three notes of CS2-inverted differ from the strict tonal mirror (G for G-sharp at 36:4.5 and D for
D-sharp at 38:3 to avoid augmented seconds; B at 37:4 to avoid a seventh against the bass).

### 2.8 INV in augmentation = the dominant pedal (`inversionAug`, bass 42-51, 38 beats, exact 2x)

    f,1 | f,2 f,4 ges,4 | f,1 | f,2 f,4 ges,4 | f,2. ees,4 | ees,2. c,4 | c,1 | c,2 des,4 f,4 | ees,2. ges,4 | bes,2

Four bars of F with G-flat neighbours (vii°4/2), then V4/2 (E-flat), the lowest note of the piece (C2,
cello open C) under the climax, D-flat and F, E-flat and G-flat (IV, iv6), and it lands on B-flat exactly
at the first note of the apotheosis. One thematic line prepares the climax and cadences plagally.

### 2.9 Derived forms

| name | LilyPond | use |
|---|---|---|
| `headH` | `x2. x8 (x-1)8`, e.g. `e2. e8 ees8` | liquidation on E (B 26:3), G (T 27:1), B-flat (A 27:3), D-flat (S 28:1) |
| `episodeCell` | `c''4. des''8 des''4. f''8 \| ges''4. f''8 f''4. ees''8 \| des''4` | cell b (S1 bar 3 rhythm) in sequence, episode 18-19 |
| `descantEntryFour` | `f''2. r4 \| r4 c''2 des''4 \| c''2 r2 \| r4 des''2 f''4 \| e''2. d''4` | soprano over entry 4; its c''-des''-c'' is the INV sigh at the answer level |
| `lamentLeadIn` | `bes2 a2 \| aes2 g4 ges4` | tenor 42-43, sus4-3 over the pedal, into its S1 entry |
| `wedge` | `f''2. f''8 ges''8 \| f''1 \| f''1~ \| f''2. ges''4~ \| ges''2 g''2 \| bes''2 bes''4 a''4 \| bes''1` | soprano 44-50: INV head, inverted pedal, chromatic wedge to the fermata on a'' |
| `themeCantusFirmus` | the whole major theme, bars 1-7 as THEME.md, then `c''1 \| d''1~ \| d''1` | soprano 51-60 |
| `mirrorMajor` | `bes,2. bes,8 c8 \| bes,2. bes,8 c8 \| bes,4. a,8 a,4. f,8 \| f,2. d,4` | bass 51-54: melodic mirror of S1 about its first note (upper neighbour c against the tune's lower neighbour a) |
| `answerMajor` | `f,2. f,8 e,8 \| f,2. f,8 e,8 \| f,4. g,8 g,4. bes,8 \| bes,2. a,8 f,8` | bass 55-58 under the tune's second half |
| `answerMirrorMajor` | `f2. f8 g8 \| f2. f8 g8 \| f4. e8 e4. c8 \| c2. d8 f8` | tenor 55-58: the answer's mirror = INV in major with E natural over the F pedal |
| `codaHead` | `bes2. bes8 a8 \| bes1` | tenor 61-62 |

Resource, not in the skeleton: `R1_S2_over_S1_iv.ly`, S2 over S1 in the subdominant, full length,
2 voices, clean (one non-simultaneous D-flat/D false relation). Available to a composer who wants a
further S1+S2 statement in free space (not planned).

### 2.10 Tune tweaks (complete list; everything else is the tune exactly)

| where | tweak | why |
|---|---|---|
| bars 1-50 | d to d-flat (minor mode) | agreed (THEME.md) |
| S1 boundary | S1 = theme bars 1 to 5:3 (C-A-F tail) | ends on 5 over V, elides into the next entry; no note changed |
| 24, 26 | stretto tails take the minor dominant (C-A-flat-F, F-D-flat-B-flat) | the next key already sounds; the dominants lose their leading tones as the music sinks |
| 48 | tenor S1 tail C-A-F becomes C-A-B-flat | the subject breaks off into C7 (V7/V), "the light" |
| 34 | the arioso's final C held over E (b6-5) | the Phrygian sigh that turns B-flat into A minor |
| 36-38 | three notes of CS2-inverted | see 2.7 |
| 54 | the bass mirror's pickup g,-bes, becomes d,4 | avoids fifths on successive beats with the tune (P4) |
| 59 | the tune's final c'' (tied) rises to d'' | the one note that separates minor from major; the theme's question gets its answer |

The complete tune is heard only once, at 51-58, untouched in B-flat major.

---------------------------------------------------------------------------------------------------

## 3. Meter, tempo, duration

4/4 throughout (the tune's own metre; every entry keeps the tune's metric placement). Measured:
`python3 tools/perform.py design/final-lab/SK_final.ly design/final-lab/plan.json OUT.mid --target piano|strings`
gives **227.3 s** for both targets (window 210-240; 12.7 s headroom for reverb tails and a slightly
longer fermata, 17 s above the floor).

| section | bars | tempo (quarter) | measured s | starts at |
|---|---|---|---|---|
| 1 Exposition, entries 1-3 | 1-12 | 74, Grave e sostenuto | 38.9 | 0.0 |
| 2 Entry 4, Episode 1 | 13-19 | 74 | 22.7 | 38.9 |
| 3 Stretto, liquidation, Climax I | 20-29 | 74; rit. to 66 in 28; fermata 29 (+3 beats); GP 1.4 s | 37.1 | 61.6 |
| 4 Arioso dolente | 30-34 | 52 | 23.4 | 98.8 |
| 5 Fuga inversa | 35-41 | 60, poco a poco to 76 ("poi a poi di nuovo vivente") | 25.1 | 122.1 |
| 6 Pedal, combination, Climax II | 42-50 | 76; rit. to 68 in 49; fermata 49:4 (+3); 50 at 56; breath 0.7 s | 33.4 | 147.2 |
| 7 Apotheosis and coda | 51-62 | 69 (Largamente); rit. to 56 from 59; final fermata on the full chord at 62:3 (+3) | 46.6 | 180.6 |
| **total** | **62** | | **227.3** | |

Arithmetic cross-check: 1-27 at 74 = 27 x 4 x 60/74 = 87.6 s; 28-29 with rit., fermata and GP about
11 s; 30-34 at 52 = 23.1 s; 35-41 accelerando (mean about 67) about 25 s; 42-48 at 76 = 22.1 s; 49-50
with fermata and breath about 11 s; 51-58 at 69 = 27.8 s; 59-62 ritardando and fermata about 17 s;
about 225 s plus breaths. The main climax (49:4, about 170 s) falls at 75% of the piece.

---------------------------------------------------------------------------------------------------

## 4. Form

| bars | part | content | key | dynamics |
|---|---|---|---|---|
| 1-4 | I Fuga: exposition, entry 1 | S1 alone, soprano, at the tune's own pitch | b-flat | p dolce, sostenuto |
| 5-8 | entry 2 | alto ANS (f'); soprano CS1 above (two voices) | f | p < |
| 9-12 | entry 3 | bass S1 (B-flat2, entering as the 7th of C7); alto CS1; soprano CS2; Neapolitan 12:3 | b-flat | mp |
| 13-17 | entry 4 | tenor ANS (f); bass CS1 = the full lament to C2; alto CS2; soprano free descant; N6/4, cadential 6/4, half cadence on C | f | mp < mf |
| 18-19 | Episode 1 | cell b in sequence (S), bass fifths F B-flat E-flat F | f to b-flat | mp < |
| 20-26 | Stretto | bass S1 (b-flat, 20); soprano S1 (e-flat, 22) a 4th + 2 octaves above, entering where the leader reaches iv; alto CS1, tenor CS2; minor-dominant tails | b-flat, e-flat, b-flat | < f |
| 26-29 | Liquidation, Climax I | head H on E (B), G (T), B-flat (A), D-flat (S), each sliding a semitone: E dim7 melts into A dim7 over E-flat; fermata ff; general pause | b-flat | < ff, GP |
| 30-33 | II Arioso dolente | soprano S2 over pulsing eighths: V, ii-half-dim 6/5, V6/iv (the one ray of D natural), iv6, V7 | b-flat | subito pp |
| 34 | Pivot | V7 of B-flat = German sixth of A minor; C held over E (b6-5); E major | to a | pp |
| 35-36 | III Fuga inversa | INV alone in the bass (E3); alto CS1 inverted (rising lament); soprano CS2 inverted | a | pp |
| 37-39 | INV stretto | tenor INV in e, a 5th above, 2 bars later | a, e | < |
| 40-41 | Transition | B7 (V7 of e), then C (VI of e = V of F) | e to F | < mf, accel. |
| 42-43 | IV Pedal | INV augmented enters on F2 (dominant pedal); alto S2; tenor lament lead-in | b-flat: V | subito p misterioso |
| 44-45 | Combination | alto S2 (end) + tenor S1 + soprano INV head + bass INV augmented: four thematic forms | b-flat: V | < mp |
| 46-49 | Climax II | double pedal F2/F5 opens into the wedge: soprano F G-flat G B-flat A against the bass F E-flat C; 48:3 C7 = V7/V, "the light"; 49:3 E dim7/D-flat; 49:4 V fermata fff, a'' on top | b-flat | < f < fff |
| 50 | Plagal turn | subito pp IV (E-flat major, the first G natural) to iv6 (G-flat bass); alto E-flat to D (51) | b-flat to B-flat | subito pp |
| 51-58 | V Apotheosis | the whole tune in B-flat major, untouched (S), over its mirror (B 51-54) and the answer (B 55-58), the answer's mirror in the tenor (55-58); Williams's IV6/4 at 52:3 | B-flat | p dolce < mf < f |
| 59-60 | | the tune's c'' rises to d''; minor iv6/4 (G-flat to F in the alto) to I | B-flat | p |
| 61-62 | Coda | the subject's head B-flat A B-flat in the tenor, ii4/2 to V7 over the tonic pedal, I; last soprano note d'', the major third | B-flat | pp, fermata |

### 4.1 Tonal plan and its logic

`b-flat, f (exposition) | b-flat, e-flat, b-flat (stretto) | b-flat dim7 slide | b-flat (arioso) | = Ger6 -> a, e, C | F pedal = V of b-flat | B-flat MAJOR`

* b-flat and f alternate at the fifth (real answers).
* e-flat is the stretto follower's key and the subject's own bar-4 harmony (iv).
* The dim7 slide moves the neighbour into harmony and ends on vii°7 of B-flat over E-flat.
* A minor is the large-scale lower neighbour, reached by the German-sixth reading of V7.
* e and C follow the inversion's own stretto at the 5th above; B7 to C turns E minor's VI into V of F.
* F is the subject's last note, held for nine bars as the augmented inversion.
* B-flat major enters plagally out of the V fermata; the whole-piece motion B-flat, A, B-flat is the
  subject's first three notes, and the coda ends on them.

### 4.2 Entry table

| bar:beat | voice | form | key | first note |
|---|---|---|---|---|
| 1:1 | S | S1 | b-flat | bes' (B-flat4) |
| 5:1 | A | ANS (real) | f | f' (F4) |
| 5:4 | S | CS1 (answer level) | f | c'' |
| 9:1 | B | S1 | b-flat | bes, (B-flat2) |
| 9:4 | A | CS1 | b-flat | f (F3) |
| 10:1 | S | CS2 | b-flat | bes' |
| 13:1 | T | ANS | f | f (F3) |
| 13:4 | B | CS1 (answer level) | f | c, (C2) |
| 14:1 | A | CS2 (answer level) | f | f' |
| 20:1 | B | S1, stretto leader | b-flat | bes, |
| 20:1 / 21:1 | A / T | CS1 (f' held, then des'') / CS2 | b-flat | f' / bes |
| 22:1 | S | S1, stretto follower (4th + 2 octaves above, +2 bars) | e-flat | ees'' |
| 26:3 / 27:1 / 27:3 / 28:1 | B / T / A / S | head H (liquidation) | dim7 E-G-B-flat-D-flat | e, / g / bes' / des'' |
| 30:1 | S | S2 (arioso) | b-flat | c'' |
| 35:1 | B | INV | a | e (E3) |
| 35:4 / 36:1 | A / S | CS1 inverted / CS2 inverted | a | a' / e'' |
| 37:1 | T | INV, stretto 5th above, +2 bars | e | b (B3) |
| 42:1 | B | INV augmented (the pedal, 9.5 bars) | b-flat: V | f, (F2) |
| 42:1 | A | S2 | b-flat over V | c'' |
| 44:1 | T | S1 (tail broken off at 48) | b-flat over V | bes (B-flat3) |
| 44:1 | S | INV head, then inverted pedal and wedge | b-flat over V | f'' |
| 51:1 | S | the whole tune, major (cantus firmus) | B-flat | bes' |
| 51:1 | B | mirror of S1 (major) | B-flat | bes, |
| 55:1 | B | ANS, major | F over B-flat's V | f, |
| 55:1 | T | the answer's mirror (INV major, E natural) | V | f (F3) |
| 61:1 | T | S1 head | B-flat | bes |

### 4.3 Special harmonic events

* Neapolitan: C-flat major at 12:3 and 23:3 (N6 under the subject's held E-flat); G-flat/D-flat (N6/4 of
  f) at 16:3.
* Diminished sevenths: vii°4/3 at 14:4.5; vii°7 at 10:4.5 and 21:4.5; the E°7 to A°7 slide (26-29);
  vii°4/2 neighbours in the pedal (43:4, 45:4.5); A°7/C at 48:2.5; E°7/D-flat at 49:3.
* Augmented sixth: V7 of B-flat heard as the German sixth of A minor (33-34), the pivot of the plan.
* Secondary dominants: C7/B-flat (V4/2 of f, the bass subject entering as the seventh, 9:1); V6/iv
  (31:4); C7 = V7/V at 48:3; C7/B-flat = V4/2 of V at 58.
* Deceptive and interrupted: B7 to C (40-41); V fermata to IV subito pp (49-50).
* Pedal points: dominant pedal 42-50 (INV augmented), with a double pedal F2/F5 at 44-47; tonic pedals
  in the apotheosis (51-52) and the coda (59-62).
* Mixture: minor iv6/4 inside the major close (60); IV then iv6 at the entry into the major (50).

---------------------------------------------------------------------------------------------------

## 5. Section list for composition

Seven sections, each self-contained, each with a verified starter file in `final-lab/sections/`.

| # | bars | file | title | skeleton density (attacks/bar) | composing work |
|---|---|---|---|---|---|
| 1 | 1-12 | `sec01_expo.ly` | Exposition, entries 1-3 | 6.8 (1, 2, 3 voices by design) | light: no free voices; landings, articulation |
| 2 | 13-19 | `sec02_entry4_episode.ly` | Entry 4 and Episode 1 | 11.6 | soprano descant, episode inner voices |
| 3 | 20-29 | `sec03_stretto_liquidation.ly` | Stretto, liquidation, Climax I | 9.0 | free tenor/alto 24-27, bass 25-26 |
| 4 | 30-34 | `sec04_arioso.ly` | Arioso dolente and pivot | 20.4 | accompaniment voicing only |
| 5 | 35-41 | `sec05_inversa.ly` | Fuga inversa and transition | 11.1 | free S/A/B 39-41 |
| 6 | 42-50 | `sec06_pedal_climax.ly` | Pedal, combination, Climax II, plagal turn | 8.6 | free alto 46-50, tenor 49-50 |
| 7 | 51-62 | `sec07_apotheosis_coda.ly` | Apotheosis and coda | 10.2 | free alto 51-60, tenor 51-54 |

Section 4 is 5 bars, under the usual 6: it stays its own section because its tempo (52), texture
(melody over pulsing eighths) and function (the collapse after the general pause, the pivot to A
minor) are unique, and merging it into section 3 or 5 would put a fermata and a general pause, or the
key change to A minor, inside one composer's work.

---------------------------------------------------------------------------------------------------

## 6. Section specifications

Notation: `n:b` = bar n, beat b. LOCKED = thematic span in `plan.json` (roles subject, answer, cf),
checked by `splice_check.py`; CS = countersubject span (only its landing note may change); FREE = may be
rewritten. Harmony per half bar: bass (lowest sounding note) / Roman numeral. Boundary tables are
generated from SK_final.ly by `sections.py`; keep every entry exactly.

### Section 1: bars 1-12, Exposition entries 1-3 (0.0-38.9 s)

* Entries: 1:1 S S1 bes'; 5:1 A ANS f'; 9:1 B S1 bes,.
* Voices: S 1-5:3 S1 LOCKED, 5:4-9:3 CS1 answer level (CS), 10-12 CS2 (CS); A 5-9:3 ANS LOCKED,
  9:4-12 CS1 (CS); B 9-12 S1 LOCKED; T rests (enters at 13). No free voices: the texture grows 1, 2, 3
  voices by design (Op. 131: the theme alone first).
* Texture: solo (1-4), two voices (5-8), three voices (9-12) = proven order C2-C1-S (lab T3, identical registers).
* Harmony (half bars, bass / numeral):
  1-4 solo line implying `i | i (A = vii) | i | i | i | ii°-iv | iv | iv-i`.
  5 `F / V of b-flat = i of f | F / i`; 6 `F / i | F / i-V (g'' over e')`; 7 `F / i | G / v6 (e-flat''/g')`;
  8 `B-flat / iv | B-flat / iv-i6/4`; 9 `B-flat2 / C7/B-flat = V4/2 of f | B-flat2 / V4/2, then A2 = b-flat V6`;
  10 `B-flat2 / i | B-flat2 / i - vii°7 (10:4.5, bass A2)`; 11 `B-flat2 / i | C3 / v6/4 passing (11:4.5 bass E-flat anticipates iv)`;
  12 `E-flat3 / iv | E-flat3 / N6 (C-flat major, 12:3) - i (12:4.5)`.
* Dynamics: p dolce espressivo, sostenuto (1-4); poco a poco cresc. to mp by 13. Bring out each
  entry (roles).
* Flags in the starter: strict ACC2 9:1 (the bass subject enters as the seventh of C7, resolving down
  at 9:4.5: intended).
* Idiom: alto CS1 at the f level (9:4-13:3) touches F3/G-flat3, below violin II's G3 (renderer stretches
  2 semitones; a live quartet may give 9:4-13:3 to the viola, which rests until 13). Piano: bars 9-12 need
  the alto split between the hands (tenor rests).

#### Section 1 boundary (bars 1-12)

| voice | first attack at 1:1 | last note |
|---|---|---|
| S | Bb4 | Db5 at 12:4 |
| A | rest (first note F4 at 5:1) | F3 at 12:4 |
| T | rest throughout | rest |
| B | rest (first note Bb2 at 9:1) | Bb2 at 12:4.5 |

First sonority (1:1): Bb4 alone. Last sonority (12:4.5): Bb2 F3 Db5 = B-flat minor.

### Section 2: bars 13-19, Entry 4 and Episode 1 (38.9-61.6 s)

* Entries: 13:1 T ANS f; 13:4 B CS1 answer level (c,, the lament to C2); 14:1 A CS2 answer level (f').
* Voices: T 13-17:3 LOCKED; B 13:4-17:3 CS; A 13:1-3 CS1 tail (CS), 14-17 CS2 (CS); S 13-17 FREE
  descant; 17:4-19 all FREE (episode). Order in 13-17: proven C2-S-C1 = lab T4 transposed down a perfect fourth in all three voices (interval-identical), + free soprano.
* FREE work: (a) soprano 13-17: keep the sighing descant's shape (entries on weak beats, c''-des''-c''
  = the INV sigh at the answer level, des''-f''-e'' to the half cadence) and its boundary; it may be
  enriched with suspensions over the lament bass (e.g. prepare 16:1 and 17:1 as 7-6 / 4-3), but avoid
  doubling the alto's CS2 at the octave (the tested failures in `search_E4_descant.py`: parallels with
  the tenor's neighbour at 13:4-14:1 and with the alto at 15:3-16:1). (b) Episode 18-19: the soprano's
  cell b (`episodeCell`) is the leading line; answer it in the alto with its mirror
  `ges'4. f'8 f'4. ees'8` (INV bar 3, foreshadowing Part III) or with CS1 fragments; give the tenor
  quarter motion instead of halves. Keep the bass fifths F B-flat E-flat F.
* Harmony: 13 `C3-F2 / V of b-flat (tail) = f: I | C2 / V of f`; 14 `A-flat2 / i6 | A-flat2 - G2 / i6 - vii°4/3`;
  15 `F2 / i - V6 (E2) | E-flat2 / v6 - v6/5`; 16 `D-flat2 / iv6 | D-flat2 - C2 / N6/4 (16:3) - cad. 6/4 (16:4)`;
  17 `E2 / V6 | C2 / V`; 18 `F2 / f: i | B-flat2 / b-flat: i (= f: iv)`; 19 `E-flat2 / iv | F2 / V - V7 (19:4.5)`.
* Dynamics: mp < mf to the half cadence (17:3), mp at the episode (18), cresc. into the stretto.
* Flags in the starter: D4? 17:2.5 (alto c'' over the bass's arpeggiated G2 inside the V chord
  E2-G2-C2: an arpeggiated 6/4, weak eighth); strict ACC2 13:1 (the tenor's answer and the soprano's F
  over the bass's C: the subject's own arpeggiated tail C-A-F, a passing 6/4).
* Idiom: soprano to f'' only. Lower staff wide in 13-19 (tenor answer over the low lament): piano takes
  the tenor in the right hand where the alto allows.

#### Section 2 boundary (bars 13-19)

| voice | first attack at 13:1 | last note |
|---|---|---|
| S | F5 | Eb5 at 19:4.5 |
| A | A3 | A4 at 19:3 (held to the section end) |
| T | F3 | C4 at 19:3 (held to the section end) |
| B | C3 | F2 at 19:3 (held to the section end) |

First sonority (13:1): C3 F3 A3 F5 = F major (6/4, the subject's arpeggiated tail). Last sonority
(19:4.5): F2 C4 A4 Eb5 = F7 (V7 of b-flat).

### Section 3: bars 20-29, Stretto, liquidation, Climax I (61.6-98.8 s)

* Entries: 20:1 B S1 bes,; 22:1 S S1 ees'' (e-flat, a 4th + 2 octaves above, 2 bars later); 26:3 B head
  on e,; 27:1 T head on g; 27:3 A head on bes'; 28:1 S head on des''.
* Voices: B 20-24 LOCKED, 26:3-29 LOCKED (head); S 22-26 LOCKED, 28-29 LOCKED; A 20:1-24 CS1 (CS),
  27:3-29 LOCKED; T 21-23 CS2 (CS), 27-29 LOCKED. FREE: S 20:1 (end of episode, des''), T 24-26,
  A 25-27:2, B 25-26:2.
* FREE work: T 24-26 and A 25-26 are half notes: give them CS2 fragments (the neighbour cell in eighths)
  and suspensions leading into the i6/4 at 26:1; B 25-26:2 may carry a lament fragment (des, c, then f,).
  Keep the soprano's rest in 20-21 (the follower must enter fresh). Do not add notes between 26:3 and
  29: the liquidation must be heard as four heads and a sliding chord.
* Harmony: 20 `B-flat2 / i | i`; 21 `i | i - vii°7 (21:4.5, bass A2)`; 22 `B-flat2 / i with the entering
  e-flat'' (the leader reaches iv) | C3 / v7 (F minor 7 over C) - iv`; 23 `E-flat3 / iv = e-flat: i | E-flat3 / N6 (C-flat) - i`;
  24 `C3 / VII6 | F2 / v - v7 (E-flat2)`; 25 `D-flat2 / III | D-flat2 / i6/5 - ii°7 (25:4)`;
  26 `F2 / i6/4 | E2 / E°7 (head on E)`; 27 `E2 / E°7 | E-flat2 / E-flat major (glimpse of light) - E-flat7`;
  28 `E-flat2 / e-flat minor 7 | E-flat2 / A°7 over E-flat (complete 28:4.5)`; 29 `A°7/E-flat, fermata`.
* Dynamics: mp at 20 < f by 26; 26:3-28:4 < ff; 29 ff, fermata (+3 beats), then a general pause of 1.4 s.
  Shade 27:3 (the E-flat major chord) as a glimpse of light inside the crescendo.
* Flags: XREL 23:4 (bass D-flat, soprano's e-flat-minor D natural on the next eighth: the stretto's two
  keys overlap; non-simultaneous, standard minor-mode stretto).

#### Section 3 boundary (bars 20-29)

| voice | first attack at 20:1 | last note |
|---|---|---|
| S | Db5 | C5 at 29:1 (held to the section end) |
| A | F4 | A4 at 28:2.5 (held to the section end) |
| T | Bb3 | Gb3 at 28:1 (held to the section end) |
| B | Bb2 | Eb2 at 27:2.5 (held to the section end) |

First sonority (20:1): Bb2 Bb3 F4 Db5 = B-flat minor. Last sonority (29:1): Eb2 Gb3 A4 C5 = A°7 over E-flat.

### Section 4: bars 30-34, Arioso dolente and the German-sixth pivot (98.8-122.1 s)

* Entry: 30:1 S S2 c'' (LOCKED 30-33); 34 soprano c''2 b'2 (the b6-5 sigh, FREE but keep).
* Voices: A and T pulsing repeated eighths (FREE accompaniment, keep the harmony and the pulse); B
  half/whole notes (FREE).
* FREE work: voicing of the eighth-note chords only; one expressive suspension per bar is welcome
  (e.g. alto 31:3 held into 32:1). Keep the bass's diminished-fourth fall D2-G-flat2 at 32:1 (lament
  figure). Keep 34 exactly (the pivot).
* Harmony: 30 `F2 / V | F2 / V - i6/4 (30:4)`; 31 `E-flat2 / ii-half-dim 6/5 | E-flat2 / ii°6/5 - V6/iv
  (31:4, the only D natural)`; 32 `G-flat2 / iv6 | F2 / V7 (d-flat''-c'' = b6-5)`; 33 `F2 / V7 | V7 (= German
  sixth of A minor)`; 34 `E2 / a: V+ (C held over E) | E2 / V (E major)`.
* Dynamics: subito pp (tempo 52, after the general pause), swell to p in 31, back to pp by 34. Piano:
  una corda, pedal each harmony. Strings: pulsing, non tremolo, each eighth lightly separated.
* Flags: MEL 32:1 (bass diminished fourth, deliberate); XREL 33:4-34:1 (alto E-flat, bass E natural:
  the enharmonic pivot itself, D-sharp spelled E-flat).

#### Section 4 boundary (bars 30-34)

| voice | first attack at 30:1 | last note |
|---|---|---|
| S | C5 | B4 at 34:3 (held to the section end) |
| A | C4 | E4 at 34:4.5 |
| T | F3 | G#3 at 34:4.5 |
| B | F2 | E2 at 34:1 (held to the section end) |

First sonority (30:1): F2 F3 C4 C5 = V (open fifth, the 3rd arrives at 30:2.5). Last sonority (34:4.5): E2 G#3 E4 B4 = E major.

### Section 5: bars 35-41, Fuga inversa and transition (122.1-147.2 s)

* Entries: 35:1 B INV e (A minor); 35:4 A CS1 inverted a'; 36:1 S CS2 inverted e''; 37:1 T INV b (E minor).
* Voices: B 35-39 LOCKED; T 37-41 LOCKED; A 35:4-39 CS; S 36-38 CS. FREE: S 39-41, A 40-41, B 39:4-41.
* FREE work: the transition (39-41) may gain eighth-note motion (accelerando "poi a poi di nuovo
  vivente"); the soprano's d-sharp'' 39:4-40 is the leading tone of e held across the bar: keep it as a
  suspension. Bar 35 stays a solo bass (the inversion alone, the answer to the subject's solo opening).
* Harmony: 35 `E3 / V (INV alone, F = b6 neighbour) | V`; 36 `E3 / i6/4 | i6/4`; 37 `E3 / VI over the
  INV's E | D3 / e: v6/5 (B minor 7)`; 38 `B2 / a: V6/4 over the tenor's B | B2 / V4/3`; 39 `D3 / ii°6 |
  A3 / i`; 40 `B2 / e: V7 (B7) | V7`; 41 `C3 / e: iv7/C (A minor 7) | C3 / VI = V of F`.
* Dynamics: pp (35) < mf (41), accelerando 60 to 76.
* Flags: DIR 37:2.5 (a hidden fifth inside the motor figure on a weak eighth, soprano leap within the line).

#### Section 5 boundary (bars 35-41)

| voice | first attack at 35:1 | last note |
|---|---|---|
| S | rest (first note E5 at 36:1) | G5 at 41:3 (held to the section end) |
| A | rest (first note A4 at 35:4) | E5 at 41:4 |
| T | rest (first note B3 at 37:1) | C4 at 41:4 |
| B | E3 | C3 at 41:4 |

First sonority (35:1): E3 alone. Last sonority (41:4): C3 C4 E5 G5 = C major (V of F).

### Section 6: bars 42-50, Dominant pedal, combination, Climax II, plagal turn (147.2-180.6 s)

* Entries: 42:1 B INV augmented f, (LOCKED 42-51:1); 42:1 A S2 c'' (LOCKED 42-45); 44:1 T S1 bes
  (LOCKED 44-48, tail broken off into C7); 44:1 S INV head f'' (LOCKED 44).
* Voices: T 42-43 lament lead-in (FREE but keep: sus4-3, then the chromatic fall into its S1 entry);
  S 45-50 wedge (FREE but keep its pitches: inverted pedal f'' 45-47, then G-flat, G, B-flat, A); A 46-50
  FREE; T 49-50 FREE.
* FREE work: the alto 46-49 (des'' c'' | a' c'' ees'' | ees'' e'' | e'' c'') is the chord-filler of the
  wedge; it may move in quarters and eighths but must keep the harmonic events 47:4 (ii°7), 48:2.5
  (A°7/C), 48:3 (C7 with E natural in the alto) and 49:3 (E°7/D-flat). Do not add a fifth part to the
  pedal bars; 42-43 stay three voices (subito p misterioso).
* Harmony: 42 `F2 / Vsus4 (tenor b-flat) | F2 / V`; 43 `F2 / v (tenor a-flat) | F2 / V (passing g),
  vii°4/2 on the bass G-flat (43:4)`; 44 `F2 / V7sus4 (F B-flat E-flat F) | F2 / i6/4 - V(b9) (44:4.5)`;
  45 `F2 / Vsus4 | F2 / Vsus4 - vii°4/2 (45:4.5)`; 46 `F2 / i6/4 | F2 / V - V4/2 (E-flat2, 46:4)`;
  47 `E-flat2 / V4/2 | E-flat2 - C2 / V4/2 - ii°7 (47:4)`; 48 `C2 / ii-half-dim 7 | C2 / A°7/C (48:2.5) -
  C7 = V7/V (48:3), "the light"`; 49 `C2 / C7 | D-flat2 - F2 / E°7/D-flat - V (49:4, fermata)`;
  50 `E-flat2 / IV (E-flat major) | E-flat2 - G-flat2 / IV - iv6 (50:4)`.
* Dynamics: subito p misterioso (42); < mp (44-46); < f (46-48); < fff (48-49:4); fermata on V with a''
  (+3 beats), breath 0.7 s; subito pp at 50 (tempo 56).
* Flags: D4? 47:1 (alto A over the bass E-flat inside V4/2: the chord's own tritone); XREL 43:3-43:4
  (tenor G then G-flat against the bass G-flat: the tenor's own chromatic step, doubled by the bass).
* Idiom: F2 is a nine-bar pedal. Piano: sostenuto pedal on F2 (42-46) so the left hand can take the
  tenor; strings: cello long bows, no accent on the G-flat neighbours. C2 (47:4-49:2) is the cello's open C.
  Soprano peak B-flat5 (49-50), violin I.

#### Section 6 boundary (bars 42-50)

| voice | first attack at 42:1 | last note |
|---|---|---|
| S | rest (first note F5 at 44:1) | Bb5 at 50:1 (held to the section end) |
| A | C5 | Eb4 at 50:4 |
| T | Bb3 | Gb3 at 50:4 |
| B | F2 | Gb2 at 50:4 |

First sonority (42:1): F2 Bb3 C5 = Vsus4. Last sonority (50:4): Gb2 Gb3 Eb4 Bb5 = iv6 (E-flat minor over G-flat).

### Section 7: bars 51-62, Apotheosis and coda (180.6-227.3 s)

* Entries: 51:1 S the whole tune, major, bes' (LOCKED 51-58); 51:1 B mirror of S1 bes, (CS 51-54);
  55:1 B ANS major f, (CS 55-58); 55:1 T answer's mirror f (CS 55-58); 61:1 T S1 head bes (LOCKED).
* Voices: A 51-62 FREE; T 51-54 FREE; all voices 59-60 FREE except the soprano's d'' (keep);
  61-62 S, A, B FREE (keep the boundary).
* FREE work: the alto (proposal-4 P06's free line) and the tenor 51-54 may be made more cantabile
  (suspensions under the tune's long notes: e.g. at 53:1 and 57:1) but must stay below the tune and
  must not double its neighbour notes at the octave. Keep 52:3 (IV6/4 over the tonic: Williams's own
  plagal colour), 56:1 (the alto's E natural over the F pedal, resolving chromatically E to E-flat) and
  60 (alto G-flat to F, the minor iv6/4: the last shadow of the minor). The tenor's final head (61-62)
  must be audible (viola, piano left hand).
* Harmony: 51 `B-flat2 / I | I (vi7/B-flat neighbour)`; 52 `B-flat2 / I | IV6/4 - I`; 53 `B-flat2 / I |
  A2 / V6/5`; 54 `F2 / V7 | F2 / V9 (no 3rd) - I6`; 55 `F2 / V (the answer enters) | F2 / V (D-minor
  colour, passing)`; 56 `F2 / V with E natural (V of V colour) | V`; 57 `F2 / V7 (the tune's e-flat'') |
  G2 / V/V 6/4 (C over G, the tenor's E natural)`; 58 `B-flat2 / C7/B-flat = V4/2 of V | B-flat2 - A2 - F2 /
  V6 - V (58:4)`; 59 `B-flat2 / I (c'' rises to d'') | I`; 60 `B-flat2 / iv6/4 (G-flat, under the held d'') |
  I`; 61 `B-flat2 / I | ii4/2 - V7 over the pedal (61:4.5, the tenor's A)`; 62 `B-flat2 / I | I`.
* Dynamics: p dolce cantabile (51) < mf (55) < f (57, the tune's peak), > mp (58), p at 59 (the rise to
  d''), > pp (62), fermata. Tempo 69, ritardando to 56 from 59. Piano: pedal each harmony; strings:
  violin I sings the tune, the others sotto voce except the tenor's mirror (55-58) and head (61-62).
* Flags: XREL 56:4.5-57:1 (the bass answer's E natural, then the tune's E-flat on the next beat:
  non-simultaneous, the tune's own note).

#### Section 7 boundary (bars 51-62)

| voice | first attack at 51:1 | last note |
|---|---|---|
| S | Bb4 | D5 at 62:1 (held to the section end) |
| A | D4 | F4 at 62:3 (held to the section end) |
| T | F3 | Bb3 at 62:1 (held to the section end) |
| B | Bb2 | Bb2 at 61:1 (held to the section end) |

First sonority (51:1): Bb2 F3 D4 Bb4 = B-flat major. Last sonority (62:3): Bb2 Bb3 F4 D5 = B-flat major, D on top.

---------------------------------------------------------------------------------------------------

## 7. Global rules for composers

1. Start from your starter `design/final-lab/sections/secNN_*.ly` (the verified skeleton). Deliver the
   finished section as `score/sections/secNN_*.ly` (same name; keep the `% bars A-B` line; one 4/4 bar
   per `|`; voices contain only notes, rests, ties and bar checks).
2. Never change LOCKED spans (subjects, answers, INV, the augmentation, the cantus firmus, the heads).
   Countersubjects keep their notes; only a landing note may change, and only if a boundary or a doubling
   requires it.
3. Keep every boundary entry of your section's table: first attack at the first downbeat (pitch, rest
   or tie-in) and the last note of every voice (pitch, tie-out). Then any two sections join as proven.
4. Verify: `python3 design/final-lab/splice_check.py score/sections/secNN_*.ly` must print PASS
   (0 PAR!, 0 BEAT, 0 DIS!, 0 CLASH, boundaries and locks intact, joins included). Every new D4?, DIR,
   MEL or XREL gets a one-line explanation in a comment at the top of the file. Also look at
   `python3 design/final-lab/strict.py FILE -v`: a new ACC2 must be a suspension, a pedal-point licence or
   a chord seventh.
5. Enrichment targets: free voices move in the rhythmic gaps of the thematic lines (eighths where the
   subject holds, held notes where it moves). Prefer prepared suspensions (7-6, 4-3, 9-8, 2-3 in the
   bass): the skeleton has 12 (`python3 design/final-lab/suspensions.py FILE`); the finished piece should
   have at least 30. Motives for free voices: the head neighbour (x x x-1), its mirror sigh (x x x+1),
   cell b (dotted quarter + eighth), CS1's chromatic tetrachord, CS2's eighth-note turns. No chordal
   padding; no parallel thirds or sixths for more than two beats; never more than four real voices.
6. Keep the deliberately thin places thin: the solo openings (1-4, 35), the two-voice entry 2 (5-8), the
   three-voice entry 3 (9-12), the soprano's silence before its stretto entry (20-21), the liquidation
   (26:3-29), the misterioso pedal (42-43), the V fermata and the pp turn (49:4-50).
7. Ranges: S 60-84, A 53-77 (below G3 only where the skeleton already goes), T 48-72, B 36-62. Where you
   add notes, keep the piano's lower staff (T+B) within a tenth unless the skeleton is already wider there.
8. Do not write dynamics, tempo or articulation into the voices. They live in `design/final-lab/plan.json`
   (performance) and will go into `score/music-global.ly` (print) when the sections are assembled. Put
   expressive intent in comments.
9. Assemble with `python3 tools/assemble.py`; then run `tools/check.py` on `score/music-voices.ly` (the
   whole piece) and re-measure the duration with `tools/perform.py` (must stay in 210-240 s).

---------------------------------------------------------------------------------------------------

## 8. Performance sketch (`final-lab/plan.json`)

* Tempo map: 74 (1-27), rit. to 66 (28), fermata 29 and general pause 1.4 s; 52 arioso (30-34); 60
  accelerando to 76 (35-41); 76 (42-48), rit. to 68 (49), fermata on V at 49:4, breath 0.7 s; 56 (50);
  69 (51-58), rit. to 56 (59-62), final fermata on the complete B-flat chord (62:3, after the alto's d' rises to f').
* Dynamics arc: p (the tune alone) to mf at the first half cadence (17); mp to f through the stretto, ff
  at the liquidation, fermata and silence (29); subito pp arioso, swelling only to p; pp to mf through
  the inverted fugue; subito p misterioso on the pedal; mp, f, fff at the V fermata (49:4, about 170 s,
  75% of the piece); subito pp IV-iv6; p dolce apotheosis to f at the tune's peak (57), then down to pp.
  Three subito-piano cuts (30, 42, 50) break the three rising spans.
* Bring out (roles in plan.json; piano +9 velocity, strings +0.7 dynamic level): S 1-5 (S1 alone), A 5-9
  (ANS), B 9-13 (S1 in the bass), T 13-17 (ANS), B 20-24 and S 22-26 (the stretto pair), the four heads
  26-29, S 30-34 (S2), B 35-39 and T 37-41 (INV and its stretto), B 42-51 (augmentation, cf level), A
  42-45 (S2), T 44-48 (S1), S 44 (INV head), S 51-58 (the tune), T 61-62 (the last head). Countersubjects
  +2 (cs), free voices -4.
* Piano: pedal each harmony in 30-34 and 51-62; sostenuto on F2 in 42-46 and on B-flat2 in 59-62; una corda
  in the arioso. Strings: arioso eighths lightly separated; the pedal F2 in long bows; violin I cantabile
  for the tune at 51.

---------------------------------------------------------------------------------------------------

## 9. Proof table (reproduce: `cd design/final-lab && python3 build_sk.py && python3 build_labs.py`)

All results are in `final-lab/proofs.txt`. Checker = `tools/check.py` with the four ranges (`ck.sh`);
strict = `strict.py` (from proposal 3).

| lab | claim | check.py (errors/PAR!/BEAT/DIS!) | remaining flags, explained |
|---|---|---|---|
| T1_C1-C2-S | triple counterpoint, CS1 top, CS2 middle, S1 bass | 0/0/0/0 | none |
| T2_C1-S-C2 | CS1 top, S1 middle, CS2 bass | 0/0/0/0 | none |
| T3_C2-C1-S | CS2 top, CS1 middle, S1 bass (= bars 9-13) | 0/0/0/0 | none |
| T4_C2-S-C1 | CS2 top, S1 middle, CS1 bass (bars 13-17 = this lab down a perfect fourth) | 0/0/0/0 | D4? 5:2.5: passing 6/4 in the tail as the next entry starts |
| T5_S-C2-C1 | S1 top, CS2 middle, CS1 bass | 0/0/0/0 | same tail 6/4 |
| T6_S-C1-C2 | S1 top, CS1 middle, CS2 bass | 0/0/0/0 | none. **All six orders pass** |
| X1_E2_cs1_over_answer | entry 2: CS1 over the answer, two voices (5-9) | 0/0/0/0 | DIR 5:3 (lab bar = 9:3): the two tails land in octaves; not outer voices once the bass enters at 9:1 |
| X2_stretto_S1_4th | S1 stretto at the 4th + 2 octaves, 2 bars (20-26) | 0/0/0/0 | XREL D-flat/D (23:4), non-simultaneous |
| X3_liquidation | four heads on a dim7, sliding (26-29) | 0/0/0/0 | none |
| X4_mirror_trio | INV + CS1-inv + CS2-inv (35-39) | 0/0/0/0 | DIR 37:2.5, weak eighth inside the motor |
| X5_stretto_INV_5th | INV stretto at the 5th, 2 bars (35-41) | 0/0/0/0 | none |
| X6_S2_then_S1 | S2 then S1 two bars later, the pair alone (42-48) | 0/0/0/0 | none |
| X7_combination_pedal | S2 + S1 + INV head + INV augmented + wedge (42-50) | 0/0/0/0 | D4? 47:1 chord tritone of V4/2; XREL 43:3 the tenor's own chromatic step |
| X8_tune_over_mirror | the whole tune over its mirror and the answer (51-59) | 0/0/0/0 | XREL 56:4.5 (E then the tune's E-flat) |
| X9_answer_vs_mirror | the answer against its own mirror (55-58) | 0/0/0/0 | none |
| R1_S2_over_S1_iv | resource: S2 over S1 in iv, full length | 0/0/0/0 | DIR 3:1 (the tune's own leap); XREL D-flat/D, non-simultaneous |
| R2_P06_apotheosis_frame | source of 51-60 (proposal-4 P06 as written) | 0/0/0/0 | as X8 |
| sections/sec01-sec07 | each starter spliced into the skeleton and checked with its joins (bars A-1..B+1) | all PASS, 0/0/0/0 | as listed per section above |
| **SK_final** | **the whole piece, 62 bars** | **0/0/0/0** | D4? 17:2.5, 47:1; DIR 37:2.5; MEL 32:1; XREL 23:4, 33:4 (x2), 43:3, 56:4.5 (none simultaneous); strict: clash 0, acc 7, acc2 26 (the tail 6/4s, pedal-point 4ths and sevenths, the V4/2 entries, the V9 and ii4/2 over pedals) |
| compile_test.ly | SK_final compiles in LilyPond 2.26 | no warnings | |
| plan.json + perform.py | duration | 227.3 s (piano and strings) | |

Harmony x-ray (`tools/harmony.py --stats`): 301 attacks, 54% chromatic to the local key, 151 distinct
harmony labels (proposal 2's skeleton: 294, 51%, 133; the old piece: mostly diatonic major triads).

Search records (not proofs): `search_E4_descant.py` (why the descant is sparse), `part4_variants.py`
(the Part IV enrichment options x1-x4; x1 adopted).

---------------------------------------------------------------------------------------------------

## 10. How the old piece's five flaws are answered

1. **Rushed subject that stopped mid-phrase**: S1 at real rhythm (4.75 bars), ends on 5 over V and
   elides; its first bar is harmonised twice in every accompanied statement.
2. **Filler countersubject, padded free voices**: a chromatic lament and a neighbour-cell motor,
   triple invertible in all six orders; free voices are lament lead-ins, a sighing descant, a wedge, a
   mirror and the answer's mirror.
3. **Diatonic harmony**: 54% chromatic attacks; Neapolitans, dim7 chains and slides, the German-sixth
   pivot, V7/V, V(b9), pedal points, deceptive and plagal cadences, mixture.
4. **No devices beyond an octave stretto**: triple counterpoint (6 orders), stretto at the 4th + 2 octaves,
   head stretto at half-bar distances on a dim7, a mirrored three-voice texture, inversion stretto at the
   5th, the inversion in augmentation as a nine-bar pedal and cantus firmus, four thematic forms at once,
   the tune over its own mirror, the answer against its own mirror.
5. **Block form, flat dynamics**: five parts after Op. 110, two climaxes (29 ff, 49 fff at 75% of the
   duration), three subito-piano cuts, a neighbour-shaped tonal plan, a major close reached through the
   minor iv, ending pp on the subject's own neighbour.

---------------------------------------------------------------------------------------------------

## 11. Open risks

1. **Tempo and recognition.** Part I runs at quarter 74 (68% of the film's 108) for gravity; the tune is
   at its own pitch in the soprano, which carries recognition. The apotheosis at 69 is above the floor of
   about 60 where the dotted halves stop sounding like the tune. Do not slow either further.
2. **Part III is short** (7 bars, 25 s). The A-minor "neighbour key" is a passage; its weight comes from
   the German-sixth pivot and the silence before it. There is no time budget for a third inverted entry
   (227 s of 240).
3. **Violin II below its compass**: the alto's CS1 at 9:4-13:3 touches F3 and G-flat3. The renderer
   stretches samples two semitones; for a live quartet give those bars to the viola (it rests until 13).
4. **Keyboard spans.** The lower staff is wider than a ninth in many bars (tenor answer over the low
   lament 13-19, stretto 21-29, the arioso bass, the pedal 42-50, 53-56). The upper staff reaches 23
   semitones at 12:1.5 (tenor resting: the alto belongs to the left hand there). MIDI rendering is
   unaffected; a printed piano score needs cross-staff distribution and the sostenuto pedal (42-46,
   59-62).
5. **Pedal harshness.** Bars 44-46 (Vsus4 with root and seventh a second apart at 44:1, the tenor's B-flat as
   a 4th over F2) and 49 (B-flat5 over C2) are dissonant by design; strict.py lists them as ACC2. On the
   piano voice the top lighter than the bass.
6. **Non-simultaneous false relations** remain at 23:4 (the stretto's two keys), 33:4 (the enharmonic
   pivot), 43:3 and 56:4.5. strict.py finds no simultaneous clash anywhere.
7. **Checker leniency.** check.py accepts accented passing dissonance; every lab was also run through
   strict.py and each remaining item is listed above. Composers must keep that standard (rule 4).
8. **The descant over entry 4 is sparse** (entries on weak beats) because fuller descants doubled the
   alto's CS2 or moved in octaves with the tenor's neighbour (see `search_E4_descant.py`). A composer may
   fill it, under the same checks.
9. **Enrichment could thicken the texture past taste**, especially at the pedal and in the apotheosis.
   Rule 6 lists the places that must stay thin; the composer of section 7 must keep the tune on top and
   clear.
10. **The INV head may mask S2 at 44-45.** At 44:1 the soprano's F5 (INV head, then the inverted pedal)
    sits a major second above the alto's S2 at its most recognisable bar (theme bar 7, e-flat'' d-flat''
    d-flat'' c''). Voice the soprano lighter there (plan roles already favour S2 and S1). If the render
    confirms masking, variant x2 of `part4_variants.py` (soprano silent until 46:3, as in proposal 2,
    then the same wedge) is checked clean and keeps the section's boundaries; using it means deleting the
    soprano's 44:1-45:1 role from plan.json (otherwise splice_check reports a LOCK).
11. **Duration headroom is 12.7 s.** Longer fermatas, slower ritardandi or long reverb tails in rendering
    must stay inside it.
