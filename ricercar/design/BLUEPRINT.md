# BLUEPRINT: "The Neighbour", ricercar a 4 on the Theme from Jurassic Park

B-flat minor to B-flat major. 4 voices (S A T B), piano and string quartet. 4/4, **66 bars, 232.1 s**
(measured with `tools/perform.py` and `final-lab/plan.json`; piano and strings targets alike).

Revision 2 (after critique round 1, `design/critique_r1.json`; every finding is answered in section 12).
Everything musical here exists as notes in `final-lab/SK_final.ly`, the verified skeleton of the whole
piece: `tools/check.py` **0 errors, 0 PAR!, 0 BEAT, 0 DIS!**, `strict.py` **0 CLASH**, compiles
in LilyPond 2.26 without warnings. Composers enrich it section by section, in parallel, and prove each
section with `final-lab/splice_check.py` (section 7).

**Single source.** `final-lab/piece.py` holds every section's notes together with its roles, "keep" items,
tempo, dynamics, fermatas and breaths, all section-relative; `build_sk.py` writes `SK_final.ly` and `plan.json`
from it, so notes and performance plan cannot drift apart. `verify.py` builds and runs every check in one
call; `timeline.py` measures sections and landmarks; `grid.py` prints the sonority of every attack (all harmony
labels below are read from it); `spanmap.py` prints the LOCKED / CS / KEEP / FREE map of every voice;
`sections.py` writes the starters and boundary tables; `build_labs.py` writes `materials.ly`, the labs and
`proofs.txt`.

---------------------------------------------------------------------------------------------------

## 0. The idea in one paragraph

The theme opens with a lower neighbour, B-flat A B-flat (1, #7, 1). The piece is built from that gesture at
several scales. (1) In the subject it is stated twice. (2) The countersubjects are the neighbour chained into
a lament (CS1) and the neighbour cell in diminution (CS2). (3) The tonal mirror turns the lower semitone
B-flat/A into the upper semitone F/G-flat, so the subject's i-to-V question becomes the inversion's V-to-i
answer. (4) At the first climax the neighbour is applied to a whole chord: four heads build a complete E
diminished seventh, and all four voices slide down a semitone together into A dim7. (5) The tonal plan is the
neighbour writ large: B-flat minor; a false dawn in the relative major (D-flat, G-flat) that darkens and
collapses; the arioso in B-flat minor, whose V7 is re-read as the German sixth of A minor; A minor, the
large-scale lower neighbour, established by three inverted entries and a cadence; its dominant E resolves
deceptively to F (E-F, the inversion's own neighbour), which is B-flat's dominant; and B-flat MAJOR. The frame
is Op. 110 (fugue, collapse, arioso dolente, inverted fugue, the pedal where augmentation and diminution meet,
radiant close). The tune is withheld whole until the end: its halves are heard apart (S1 in the fugue, S2 in
the arioso), then together over the augmented inversion, and only at bar 55 the complete tune, untouched, in
B-flat major, over the fugue's own triple counterpoint turned major, the lament still falling in the bass; its
open c'' rises to d'' at 63 through a real V7-I. The last word is the subject's neighbour B-flat A B-flat in the
tenor, over a tolling tonic pedal.

---------------------------------------------------------------------------------------------------

## 1. Synthesis log

| decision | source | why |
|---|---|---|
| Base: concept, materials, triple invertible counterpoint, dim7 liquidation, arioso, German-sixth pivot to A minor, fuga inversa with its stretto at the 5th, INV in augmentation as the dominant pedal | proposal 2 | the only design fully written, checked and measured |
| Exposition S-A-B-T, tune first alone in the soprano at its own pitch | proposal 1, judges | recognition first |
| The full lament in the bass under the last exposition entry | proposal 4 | gravity; falls out of the permutation |
| Williams's tune untouched as the apotheosis cantus firmus, c'' rising to d'' | proposal 4 (P06), judges | the one note that separates minor from major |
| strict.py as a second checker | proposal 3 | check.py accepts any stepwise dissonance |
| **Revision 2 (critique round 1)**: stretto moved to the relative major; A minor established by a third inverted entry and a cadence; liquidation sounds its complete dim7; S1 and S2 enter together over the pedal; Climax II built from diminution heads; dominant hinge instead of V-IV; apotheosis over the triple counterpoint in major; entry-4 descant, episode, arioso and coda recomposed; splice_check enforces countersubjects and "keep" items | critics 1 and 2 | section 12 maps every finding |
| REJECTED: P3's reordered S1 ending, P1's D-flat-major S2 exposition and fifths chain, P4's fixed-register countersubjects | judges | unchanged from revision 1 |

---------------------------------------------------------------------------------------------------

## 2. Materials

All in `final-lab/materials.ly` (35 `\absolute` variables at their reference pitch = first appearance, all
parsed by `tools/lyparse.py`). LilyPond, c' = middle C, B-flat minor unless stated.

### 2.1 Subject I (S1) = theme bars 1 to 5 beat 3, 19 beats (`subjectOne`)

    bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'8 | c''4. a'8 f'4

* Only the third degree changes (d to d-flat). S1 ends on F (5) and elides into the next entry.
* The tune's bars 1-3 contain no third degree: S1 in major and in minor differ in one eighth (4:4). This is
  why S1 can stand in D-flat major (stretto leader), G-flat major (follower) and B-flat major (apotheosis)
  without changing its identity.
* First bars: entries 3 (9), 4 (13) and the stretto leader (20) are harmonised with at least two harmonies in
  their first bar. Entry 2 (5-8) is two voices only (CS1 above the answer) by design, and its first bar is one
  F-minor arpeggio. Bar 9:1-9:2.5 is E dim over B-flat (a rootless C7 = V4/2 of f); the C arrives at 9:3.

### 2.2 Answer (ANS), real, at the fifth (`answerOne`, alto 5:1)

    f'2. f'8 e'8 | f'2. f'8 e'8 | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f'8 | g'4. e'8 c'4

Real, not tonal: S1 touches 5 only at its last note; a real answer keeps the leading-tone neighbour F-E-F.

### 2.3 Countersubject 1, "Lament" (`csOne`, `csOneAnswer`)

    subject level (alto 9:4):   r2. f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4 | a4. c'8 f4
    answer level (soprano 5:4): r2. c''4 | aes''2. g''4 | f''4 e''4 ees''2 | des''2. c''4 | e''4. g''8 c''4

A rising sixth (the sigh), then a descent from the minor third to the fifth, D-flat C B-flat A A-flat
G-flat F, a minor sixth with two chromatic steps (D-flat-C is diatonic; B-flat-A-A-flat is the chromatic core).
It is not Bach's chromatic fourth; it is a lamento line in the same family. Enters on the subject's beat 4.

### 2.4 Countersubject 2, "Motor" (`csTwo`, `csTwoAnswer`)

    subject level (soprano 10): r1 | bes'8 a'8 bes'8 c''8 des''8 c''8 ees''8 ges'8 | des''4 c''8 f''8~ f''2 | ees''8 f''8 ees''8 des''8 ces''4 des''4 | f'2.
    answer level (alto 14):     r1 | f'8 e'8 f'8 g'8 aes'8 g'8 bes'8 des'8 | aes'4 g'8 c''8~ c''2 | bes'8 c''8 bes'8 aes'8 ges'4 aes'4 | c'2.

The neighbour cell in diminution, rising, then falling through the Phrygian tetrachord (the Neapolitan
C-flat under the subject's held E-flat, 12:3). **S1, CS1, CS2 are triple invertible counterpoint at the octave:
all six orders proven** (labs T1-T6).

### 2.5 Subject II (S2) = theme bars 5-8, 16 beats (`subjectTwo`)

    c''4. a'8 f'4 des''8 bes'8 | c''2. f''8 bes'8 | ees''4. des''8 des''4. c''8 | c''1

Used as the arioso's melody (30-33), with S1 over the dominant pedal (alto 48-51), and inside the whole tune
(59-62, major). It keeps its own pitch (c'' over F) at all three, on purpose (section 12, C1-M3).

### 2.6 Inversion (INV), tonal mirror (`inversion`, `inversionA`, `inversionE`, `inversionAthird`)

    reference:             f''2. f''8 ges''8 | f''2. f''8 ges''8 | f''4. ees''8 ees''4. c''8 | c''2. des''8 f''8 | ees''4. ges''8 bes''4
    A minor (bass 35):     e2. e8 f8 | e2. e8 f8 | e4. d8 d4. b,8 | b,2. c8 e8 | d4. f8 a4
    E minor (tenor 37):    b2. b8 c'8 | b2. b8 c'8 | b4. a8 a4. fis8 | fis2. g8 b8 | a4. c'8 e'4
    A minor (soprano 41):  e''2. e''8 f''8 | e''2. e''8 f''8 | e''4. d''8 d''4. b'8 | b'2. c''8 e''8 | d''4. f''8 a''4

Diatonic mirror (B-flat/F, C/E-flat, A/G-flat, A-flat/G swap; D-flat fixed). Starts on 5, ends on 1; its tail
is a iv arpeggio, so the inversion cadences plagally by nature (the mirror of S1's V tail).

### 2.7 Inverted countersubjects (`csOneInv`, `csTwoInv`, `csOneInvBass`, `csTwoInvLow`)

    CS1 inv. (alto 35:4):   r2. a'4 | c'2. d'4 | e'4 f'4 fis'2 | gis'2. a'4 | f'4. d'8 [landing]
    CS2 inv. (sop. 36):     e''8 f''8 e''8 d''8 c''8 d''8 b'8 g''8 | c''4 d''8 a'8~ a'4 b'4 | b'8 a'8 b'8 c''8 d''4 c''4
    CS1 inv. (bass 41:4):   r2. a,4 | c2. d4 | e4 f4 fis2 | gis2. a4 | f4. d8 a,4 e,4   (the lament rising in the bass; cadence tail)
    CS2 inv. (alto 42):     e'8 f'8 e'8 d'8 c'8 d'8 b8 g'8 | c'4 d'8 a8~ a4 b4 | b8 a8 b8 c'8 d'4 c'4

The mirrored triple counterpoint appears in two orders: CS2inv / CS1inv / INV (35-39, lab X4) and INV / CS2inv /
CS1inv (41-45, lab X10).

### 2.8 INV in augmentation = the dominant pedal (`inversionAug`, bass 46-55:1, exact 2x)

    f,1 | f,2 f,4 ges,4 | f,1 | f,2 f,4 ges,4 | f,2. ees,4 | ees,2. c,4 | c,1 | c,2 des,4 f,4 | ees,2. ges,4 | bes,2

F is held 46:1-50:3 (with G-flat neighbours at 47:4 and 49:4); then the augmentation moves: E-flat (50:4),
C (51:4, the cello's open C under the climax), D-flat (53:3), F (53:4, the V fermata), E-flat (54:1), G-flat
(54:4), B-flat (55:1, the first note of the apotheosis).

### 2.9 Derived forms

| name | LilyPond | use |
|---|---|---|
| `subjectOneDflat` | `des'2. des'8 c'8 \| ... \| ees'4. c'8 aes4` | S1 in D-flat major, stretto leader, tenor 20 |
| `subjectOneGflat` | `ges''2. ges''8 f''8 \| ... \| aes''4. f''8 des''4` | S1 in G-flat major, follower a 4th + octave above, soprano 22 |
| `csOneDflat` | `r2. aes,4 \| f2. ees4 \| des4 c4 ces2 \| bes,2. aes,4 \| c4. ees8 aes,4` | the lament in D-flat major under the leader, bass 20:4 |
| `headH` | `x2. x8 (x-1)8` | liquidation heads on E (B 26:3), G (T 27:1), B-flat (A 27:3), D-flat (S 28:1), each held until all sound, then `x8 (x-1)8` in all four voices at 28:4 |
| `episodeCell` | `c''4. des''8 des''4. f''8 \| ges''4. f''8 f''4. ees''8 \| f''4` | cell b in sequence, soprano 18-20:1 |
| `descantEntryFour` | `f''2 c''2~ \| c''2. des''4 \| c''4. e''8 g''4 ees''4 \| f''2 ges''4 f''4 \| e''2. d''4` | free soprano over entry 4 |
| `lamentLeadIn` | `bes2 a2 \| aes2 g4 c'4` | tenor 46-47 over the pedal, into its S1 entry |
| `headDiminution` | `x4. x16 (x-1)16` | S1's head in diminution: soprano on F (50:3, diatonic E-flat neighbour against the E-flat bass), G-flat (51:1), A (51:3), C (52:3, neighbour B-flat); alto on E (52:1, 53:1) |
| `hingeDescent` | `a''4 \| f''4 ees''4 c''4 a'4 \| bes'2.` | soprano 53:4-55:1: V7 falling to the leading tone, which resolves to the tune's first note |
| `themeCantusFirmus` | the whole major theme, then `c''1 \| d''1~ \| d''1` | soprano 55-64 |
| `csOneMajor` | `bes,2. f,4 \| d2. c4 \| bes,4 a,4 aes,2 \| ges,2. f,4` | the lament in B-flat major, bass 55-58 |
| `csTwoMajor` | `bes8 a8 bes8 c'8 d'8 c'8 ees'8 g8 \| d4 c8 f8~ f2 \| ees8 f8 ees8 d8 c4 d4` | CS2 in major, tenor 56-58 (bars 2-3 an octave lower to leave the alto room) |
| `answerMajor` | `f,2. f,8 e,8 \| f,2. f,8 e,8 \| f,4. g,8 g,4. bes,8 \| bes,2. a,8 f,8` | bass 59-62 under the tune's second half |
| `answerMirrorTail` | `f4. e8 e4. c8 \| c2. ees4` | the answer's mirror bars 3-4, tenor 61-62, landing on the seventh of V7 |
| `inversionHeadMajor` | `f'2. f'8 g'8 \| f'4` | the inversion's head in major (G natural for the old G-flat), alto 63 |
| `codaHead` | `bes2. bes8 a8 \| bes1` | tenor 65-66 |

Resource, not in the skeleton: `R1_S2_over_S1_iv.ly` (S2 over S1 in the subdominant, 2 voices, clean).

### 2.10 Tune tweaks (complete list)

| where | tweak | why |
|---|---|---|
| bars 1-54 | d to d-flat (minor) | agreed (THEME.md) |
| S1 boundary | S1 = theme bars 1 to 5:3 | ends on 5, elides |
| 20-26 | S1 in D-flat and G-flat major (the tune's own major shape, transposed) | the false dawn; bars 1-3 of the tune have no third degree |
| 52 | tenor S1 tail C-A-F becomes C-A-B-flat | the subject breaks off into C7, "the light" |
| 34 | the arioso's final C held over E (b6-5) | the Phrygian sigh into A minor |
| 36-38 | three notes of CS2-inverted | augmented seconds avoided |
| 63 | the tune's final c'' rises to d'' | the question answered |

The complete tune is heard once, at 55-62, untouched in B-flat major.

---------------------------------------------------------------------------------------------------

## 3. Meter, tempo, duration

4/4 throughout. Measured with `python3 tools/perform.py design/final-lab/SK_final.ly design/final-lab/plan.json OUT.mid --target piano|strings`:
**232.1 s** for both targets (window 210-240; 7.9 s headroom). `python3 design/final-lab/timeline.py`:

| section | bars | tempo (quarter) | start s | measured s | share |
|---|---|---|---|---|---|
| 1 Exposition, entries 1-3 | 1-12 | 78, Grave e sostenuto | 0.0 | 36.9 | 15.9% |
| 2 Entry 4, Episode | 13-19 | 78 | 36.9 | 21.5 | 9.3% |
| 3 Stretto (false dawn), liquidation, Climax I | 20-29 | 78; rit. to 66 in 28; fermata 29:1 (+3); general pause 1.4 s | 58.5 | 35.7 | 15.4% |
| 4 Arioso dolente | 30-34 | 52 | 94.2 | 23.4 | 10.1% |
| 5 Fuga inversa | 35-45 | 64, poco a poco to 76 | 117.5 | 38.1 | 16.4% |
| 6 Pedal, combination, Climax II, hinge | 46-54 | 76; rit. to 68 in 53; fermata 53:4 (+2); 54 at 62 to 56 | 155.6 | 31.3 | 13.5% |
| 7 Apotheosis and coda | 55-66 | 72 (Largamente); rit. to 56 from 63; fermata 66:3 (+3) | 186.9 | 45.2 | 19.5% |
| **total** | **66** | | | **232.1** | |

Landmarks: Climax I fermata 29:1 at 86.4 s (37%); A-minor cadence 45:3 at 153.8 s (66%); Climax II peak 53:1
at 177.7 s (77%); V fermata 53:4 at 180.2 s; the tune in major 55:1 at 186.9 s (81%); c''-d'' 63:1 at 213.6 s
(92%); final chord 66:3 at 226.7 s.

---------------------------------------------------------------------------------------------------

## 4. Form

| bars | part | content | key | dynamics |
|---|---|---|---|---|
| 1-4 | I Fuga: entry 1 | S1 alone, soprano, at the tune's own pitch | b-flat | p |
| 5-8 | entry 2 | alto ANS; soprano CS1 above (two voices) | f | < |
| 9-12 | entry 3 | bass S1 (entering under E dim = rootless C7); alto CS1; soprano CS2; N6 at 12:3 | b-flat | mp |
| 13-17 | entry 4 | tenor ANS; bass the full lament to C2; alto CS2; soprano descant; half cadence on C7 | f | < mf |
| 18-19 | Episode | cell b in sequence over bass fifths F-B-flat-E-flat-A-flat; alto answers cell b at the half bar | f, b-flat, e-flat, to D-flat | mp |
| 20-26 | Stretto, false dawn | tenor S1 in D-flat major over the lament in the bass; soprano S1 in G-flat major (22); C-flat (IV of G-flat); 24:3 a bare A-flat fifth that turns minor; 25 C-flat = the Neapolitan of b-flat; sinks to F | D-flat, G-flat, back to b-flat | < f |
| 26-29 | Liquidation, Climax I | heads on E, G, B-flat, D-flat accumulate the complete E dim7 (28:1-4, ff); all four slide a semitone together into A dim7 over E-flat (28:4.5), re-struck ff, fermata; general pause | b-flat | < ff, GP |
| 30-33 | II Arioso dolente | soprano S2 over pulsing eighths: V, i6/4, ii dim 6, V7/iv, iv6 with the alto's 7-6 (the peak, 32:1), cadential 6/4, V7 (4-3 at 33:3) | b-flat | subito pp < mp > pp |
| 34 | Pivot | V7 of B-flat = German sixth of A minor: E with C held (b6), a touch of A-minor 6/4, E major | to a | pp |
| 35-39 | III Fuga inversa | INV alone in the bass (E); CS1 inv. (alto), CS2 inv. (soprano); tenor INV in e a 5th above (37); root-position A minor at 39:3 | a | pp < |
| 40 | | B major (V of e) to E minor: the tenor's answer closes | e | |
| 41-45 | third entry, cadence | soprano INV in A minor over the lament rising in the bass (CS1 inv.) and CS2 inv. (alto): i6/4-V-i (41), V6-vii dim-i (44:4), iv-i with a'' on top (45:3); E major (45:4) | a | < mf |
| 46-47 | IV Pedal | INV augmented enters on F2; tenor lament lead-in alone above it (two voices, misterioso) | b-flat: V | subito p |
| 48-51 | Combination | S2 (alto) and S1 (tenor) enter together over the augmentation: both halves of the tune for 16 beats | b-flat: V | < mp < f |
| 50-53 | Climax II | S1 heads in diminution (the first sixteenths: soprano F, G-flat, A, C; alto E) over S1 (tenor) and the augmentation (bass): three speeds; C major (52:1, "the light") to complete C7 with B-flat 6 on top (53:1, fff), E dim7/D-flat, V fermata with the root doubled | b-flat | < fff |
| 54 | Hinge | the dominant continues: V4/2 (E-flat bass), vii dim 4/2 (G-flat bass); soprano A F E-flat C A, the leading tone resolving to the tune's first note | to B-flat | f > p |
| 55-58 | V Apotheosis | the whole tune untouched in B-flat major (S) over CS1 major (the lament, B) and CS2 major (T): the exposition's triple counterpoint in major; A-flat and G-flat of the lament are the one minor shadow | B-flat | p < mf |
| 59-62 | | the tune's second half over the answer (B); the answer's mirror in contrary motion (T 61-62); peak f at 60:4; C7/B-flat, V7 complete | B-flat | < f > mp |
| 63-64 | | c'' rises to d'' over a real V7-I; the inversion's head in major (alto) under the held d'' | B-flat | p |
| 65-66 | Coda | the subject's head B-flat A B-flat in the tenor, V7 over the tolling tonic pedal, I; d'' on top | B-flat | pp, fermata |

### 4.1 Tonal plan and its logic

`b-flat, f (exposition) | episode fifths | D-flat, G-flat, C-flat (false dawn) | b-flat: dim7 slide | b-flat arioso | V7 = Ger6 -> a, e, a (cadence) | E -> F deceptive | F pedal = V of b-flat | B-flat MAJOR`

* b-flat and f alternate at the fifth (real answers).
* The stretto moves to the relative major and its subdominant: the tune's major shape appears for the first
  time, in stretto, over the lament; it darkens (A-flat: bare fifth to minor; C-flat, the Neapolitan of b-flat)
  and sinks through F to the E dim7 that crushes it. The dawn is false; the true one is 55.
* A minor is the large-scale lower neighbour of B-flat. It is entered through the German-sixth reading of V7
  (33-34) and left through its own dominant resolving deceptively onto F (45:4-46:1): F-E, then E-F.
* A minor is established, not passed through: root-position i at 39:3 (after ii dim 6 and iv6), a cadential
  6/4-V-i at 41:1-4 (bass E-A), V6-vii dim-i at 44 (bass G-sharp-A), iv-i at 45:3 with the tonic on top.
* The nine-bar dominant function (46-54) resolves to I through V4/2 and vii dim 4/2, not by retrogression.
* The whole-piece motion B-flat, A, B-flat is the subject's first three notes; the coda ends on them.

### 4.2 Entry table (all thematic spans in `plan.json`)

| bar:beat | voice | form | key | first note |
|---|---|---|---|---|
| 1:1 | S | S1 | b-flat | bes' |
| 5:1 | A | ANS (real) | f | f' |
| 5:4 | S | CS1 (answer level) | f | c'' |
| 9:1 | B | S1 | b-flat | bes, |
| 9:4 | A | CS1 | b-flat | f |
| 10:1 | S | CS2 | b-flat | bes' |
| 13:1 | T | ANS | f | f |
| 13:4 | B | CS1 (answer level, to C2) | f | c, |
| 14:1 | A | CS2 (answer level) | f | f' |
| 20:1 | T | S1, stretto leader | D-flat | des' |
| 20:4 | B | CS1 (lament) in D-flat | D-flat | aes, |
| 22:1 | S | S1, stretto follower (4th + octave above, 2 bars later) | G-flat | ges'' |
| 26:3 / 27:1 / 27:3 / 28:1 | B / T / A / S | head H (liquidation) | E dim7 | e, / g / bes' / des'' |
| 30:1 | S | S2 (arioso) | b-flat | c'' |
| 35:1 | B | INV | a | e |
| 35:4 / 36:1 | A / S | CS1 inv. / CS2 inv. | a | a' / e'' |
| 37:1 | T | INV, stretto at the 5th above, 2 bars | e | b |
| 41:1 | S | INV, third entry | a | e'' |
| 41:4 / 42:1 | B / A | CS1 inv. (rising lament) / CS2 inv. | a | a, / e' |
| 46:1 | B | INV augmented (the pedal) | b-flat: V | f, |
| 48:1 | A | S2 | over V | c'' |
| 48:1 | T | S1 (breaks off into C7 at 52:3) | over V | bes |
| 50:3 | S | S1 heads in diminution (F, G-flat, A, C) | over V | f'' |
| 52:1 | A | S1 heads in diminution (E) | V/V | e'' |
| 55:1 | S | the whole tune, major (cantus firmus) | B-flat | bes' |
| 55:4 | B | CS1 (lament) in B-flat major | B-flat | f, |
| 56:1 | T | CS2 in B-flat major | B-flat | bes |
| 59:1 | B | ANS, major | V | f, |
| 61:1 | T | the answer's mirror, bars 3-4 | V | f |
| 65:1 | T | S1 head | B-flat | bes |

### 4.3 Special harmonic events (read from `grid.py`)

* Neapolitan: C-flat major at 12:3 (N6 under the subject's held E-flat), G-flat major over D-flat at 16:3 (N6/4
  of f), and C-flat major as a region at 25 (IV of G-flat = the Neapolitan of b-flat).
* Diminished sevenths: vii dim 4/3 of f at 14:4; E dim7 (26:3, complete 28:1-4) sliding into A dim7 over
  E-flat (28:4.5-29); A dim7 over E-flat arpeggiated across 51 (51:1 C-E-flat-G-flat, 51:3 A: vii dim 4/2 in the
  pedal); E dim7 over D-flat at 53:3;
  A dim7 over G-flat at 54:4 (the hinge).
* Augmented sixth: V7 of B-flat heard as the German sixth of A minor (33-34).
* Secondary dominants: rootless C7 over B-flat (9:1); C7 half cadence of f (17:3); B7/D = V7/iv (31:4);
  B major = V of e (40); C major then C7 = V/V (52-53); C7/B-flat = V4/2 of V (62:1).
* Deceptive: E major (V of a) to F (45:4-46:1).
* Pedal points: dominant pedal F2 46:1-50:3; tonic pedal 63-66 re-struck every bar.
* Mixture: the lament's A-flat (57:3, v6) and G-flat (58:1, iv6) under the major tune: the one minor shadow.
* Suspensions in the skeleton (strict count): 25:3 soprano 4-3 over G-flat; 32:1 alto 7-6 over G-flat (the
  arioso peak); 32:3-33:3 tenor 4-3 (cadential 6/4); 65:3 tenor 2-3 in the coda; plus 12 on weak beats.

---------------------------------------------------------------------------------------------------

## 5. Section list for composition

Seven sections, each with a verified starter in `final-lab/sections/` (same file names as before; bar ranges
changed from bar 35 on).

| # | bars | file | title | attacks/bar (skeleton) | composing work |
|---|---|---|---|---|---|
| 1 | 1-12 | `sec01_expo.ly` | Exposition, entries 1-3 | 6.8 (1, 2, 3 voices by design) | light: landings, articulation |
| 2 | 13-19 | `sec02_entry4_episode.ly` | Entry 4 and Episode | 12.3 | main task: the soprano descant; episode inner voices |
| 3 | 20-29 | `sec03_stretto_liquidation.ly` | Stretto in the relative major, liquidation, Climax I | 10.2 | the free alto 20-27:2 and tenor/bass 24-26 |
| 4 | 30-34 | `sec04_arioso.ly` | Arioso dolente and the German-sixth pivot | 20.0 | voicing and motion of the accompaniment |
| 5 | 35-45 | `sec05_inversa.ly` | Fuga inversa: three entries, A minor established, deceptive link to F | 9.5 | free tenor 41:4-44, free soprano 35 and 39:1-2, cadence inner voices |
| 6 | 46-54 | `sec06_pedal_climax.ly` | Dominant pedal: S1 and S2 together, Climax II in three speeds, dominant hinge | 10.6 | soprano 46-50:2 (silent in the skeleton), alto 46-47 |
| 7 | 55-66 | `sec07_apotheosis_coda.ly` | Apotheosis over the triple counterpoint in major; coda | 10.8 | the free alto 55-66, tenor 59-60 and 63-64, soprano 65-66 |

Section 4 stays a 5-bar section (unique tempo, texture and function). It is exempt from global rule 5's
"no chordal padding": its pulsing repeated eighths are the Op. 110 arioso model; enrichment there means
voice-leading inside the pulse (suspensions, the moving inner line), not added figuration.

---------------------------------------------------------------------------------------------------

## 6. Section specifications

Notation: `n:b` = bar n, beat b. LOCKED = thematic span in `plan.json` (roles subject, answer, cf): unchanged
notes. CS = countersubject span: unchanged notes except from its `landing_from` position (the landing note).
KEEP = a non-thematic note the design depends on (`plan.json` "keep"): unchanged. FREE = may be rewritten.
The per-voice maps below are printed by `spanmap.py` from `plan.json`; splice_check enforces them. Harmony per
half bar is read from `grid.py`. Boundary tables are generated by `sections.py`; keep every entry exactly.

### Section 1: bars 1-12, Exposition entries 1-3 (0.0-36.9 s)

* Entries: 1:1 S S1 bes'; 5:1 A ANS f'; 5:4 S CS1 (answer level); 9:1 B S1 bes,; 9:4 A CS1; 10:1 S CS2.
* Map: S 1:1-5:4 LOCKED; 5:4-9:3 CS (landing 9:3); 9:4-10:1 FREE; 10:1-13:1 CS. A 5:1-9:4 LOCKED; 9:4-13:1 CS
  (continues to its landing 13:3 in section 2). T FREE (rests; enters at 13). B 9:1-13:1 LOCKED.
* Texture: solo (1-4), two voices (5-8), three voices (9-12) = proven order C2-C1-S (lab T3). No free voices.
* Harmony: 1-4 the solo line; 5 f: i (F-C, then the unison F at 5:3, below); 6 f: i (F, A-flat); 7 F, then E-flat
  over G (v6 colour); 8 b-flat: i (B-flat, D-flat); 9:1 E dim over B-flat (rootless C7 = V4/2 of f), 9:3 C over
  B-flat (V4/2); 10 i; 11:1 i, 11:3 F minor over C (a passing 6/4 of the minor v); 12:1 iv (E-flat minor),
  12:3 C-flat major over E-flat (N6), 12:4.5 i.
* Unison 5:3 (the one in the skeleton): S1's final F4 meets the answer's held F4. Kept on purpose: the subject
  must end on F and the answer must enter on F; the voices meet where one ends. Piano: one key, the soprano
  part ends there; quartet: violins I and II in unison for one beat.
* Dynamics: p (1-4), poco a poco to mp by 13.
* Idiom: violin II would go below its compass at 9:4-12:4 (F3, G-flat3): give the alto's 9:4-12:4 to the
  viola, which rests until 13; violin II resumes the CS1 tail at 13:1 (A3). Piano: 9-12 the alto belongs to
  the left hand (upper-staff span 23 semitones at 12:1.5 otherwise).

#### Section 1 boundary (bars 1-12)

| voice | first attack at 1:1 | last note |
|---|---|---|
| S | Bb4 | Db5 at 12:4 |
| A | rest (first note F4 at 5:1) | F3 at 12:4 |
| T | rest throughout | rest |
| B | rest (first note Bb2 at 9:1) | Bb2 at 12:4.5 |

First sonority (1:1): Bb4 alone. Last sonority (12:4.5): Bb2 F3 Db5 = B-flat minor.

### Section 2: bars 13-19, Entry 4 and Episode (36.9-58.5 s)

* Entries: 13:1 T ANS f; 13:4 B CS1 (answer level, the lament to C2); 14:1 A CS2 (answer level).
* Map: S 13:1-20:1 FREE. A 13:1-13:3 CS, landing 13:3; 13:4-14:1 FREE; 14:1-17:1 CS; 17:1-20:1 FREE.
  T 13:1-17:4 LOCKED; 17:4-20:1 FREE. B 13:1-13:4 LOCKED (S1 tail); 13:4-17:3 CS; 17:3-18:1 FREE; 18:1-20:1
  KEEP (the episode bass F-B-flat-E-flat-A-flat: the fifths into D-flat).
* FREE work (the main task of this section, critique C1-m6): the soprano descant over entry 4 is the first
  four-voice music; the skeleton's descant (`descantEntryFour`) completes every chord (13:3 C, 15:2.5 E, G-flat
  on the N6/4, E-D into the half cadence). Enrich it with suspensions over the lament bass (e.g. prepare 16:1
  and 17:1) without doubling the alto's CS2 at the octave or the unison. Episode (18-19): the soprano's cell b
  leads; the alto answers it at the half bar (`bes'4. des''8`, 18:3); the tenor moves in quarters (F G F |
  E-flat G-flat A-flat C) into the leader's D-flat at 20:1. Keep the bass.
* Harmony: 13:1 F over C (the subject's arpeggiated tail, a 6/4), 13:3 F major (V of b-flat), 13:4 the
  tenor's F over C resolving to E (4-3); 14 f: i6, 14:4 vii dim 4/3; 15:1 i, 15:2.5 V6, 15:3 v6 (C minor over
  E-flat), 15:4.5 v6/5; 16:1 iv6, 16:3 N6/4 (G-flat over D-flat), 16:4 cadential 6/4; 17:1 V6, 17:3 V7 (C7:
  the alto's B-flat), 17:4 V7 with passing D; 18:1 f: i; 18:3 b-flat: i (B-flat minor 7 at 18:4.5); 19:1 e-flat
  minor (= D-flat: ii); 19:3 A-flat7 with the soprano's F as a 13th resolving to E-flat (19:4.5) = V7 of D-flat.
* Dynamics: < mf to the half cadence (17:3), mp at 18, < into the stretto.
* Flags: DIR 13:3 (the soprano leaps F5-C5 onto the root while the bass moves A-F: a hidden fifth softened by
  the bass's step of a third; kept to complete the F chord); XREL 15:2.5-15:3 (soprano E5, then the bass's
  E-flat: the lament's own chromatic step).
* Idiom: lower staff wider than a ninth in 13, 15-17, 19 (tenor answer over the low lament): the piano takes
  the tenor in the right hand where the alto allows.

#### Section 2 boundary (bars 13-19)

| voice | first attack at 13:1 | last note |
|---|---|---|
| S | F5 | Eb5 at 19:4.5 |
| A | A3 | Gb4 at 19:3 (held to the section end) |
| T | F3 | C4 at 19:4 |
| B | C3 | Ab2 at 19:3 (held to the section end) |

First sonority (13:1): C3 F3 A3 F5 = F major. Last sonority (19:4.5): Ab2 C4 Gb4 Eb5 = A-flat7 (V7 of D-flat).

### Section 3: bars 20-29, Stretto in the relative major, liquidation, Climax I (58.5-94.2 s)

* Entries: 20:1 T S1 in D-flat major (des'); 20:4 B CS1 in D-flat; 22:1 S S1 in G-flat major (ges''), a 4th +
  octave above, 2 bars later; heads 26:3 B e,; 27:1 T g; 27:3 A bes'; 28:1 S des''.
* Map: S 20:1-22:1 FREE (20:1 F5, then silence: the follower enters fresh); 22:1-26:4 LOCKED; 26:4-28:1
  FREE (rest); 28:1-29:1 LOCKED; 29:1-30:1 KEEP. A 20:1-24:3 FREE; 24:3-25:1 KEEP (E-flat: the bare fifth);
  25:1-26:3 FREE; 26:3-27:3 KEEP (G: E dim7 complete at 26:3); 27:3-29:1 LOCKED; 29:1-30:1 KEEP.
  T 20:1-24:4 LOCKED; 24:4-25:1 KEEP (C-flat: A-flat minor); 25:1-26:3 FREE; 26:3-27:1 KEEP (B-flat);
  27:1-29:1 LOCKED; 29:1-30:1 KEEP. B 20:1-20:4 FREE; 20:4-24:3 CS; 24:3-26:3 FREE; 26:3-29:1 LOCKED;
  29:1-30:1 KEEP.
* FREE work: the alto 20-24:2 (between the tenor's subject and the soprano) is the section's inner voice: give
  it suspensions and CS2-like eighths (the neighbour cell) against the leader's held notes; tenor/bass 25-26:2
  may move more (keep 26:1 D-flat/F and 26:2 F minor). Do not add notes between 26:3 and 29 except the
  written ones: the liquidation must be heard as heads accumulating one chord, then one slide.
* Harmony: 20:1 D-flat: I, 20:3 IV6/4 (neighbour), 20:4.5 V (A-flat), 21:1 I6, 21:4 ii7, 21:4.5 vii dim 6;
  22:1 G-flat over D-flat (the follower enters on I6/4 of G-flat), 22:2.5 C half-dim 7 (the lament passing),
  22:3 C-flat major (IV of G-flat); 23:1 G-flat: I6, 23:4 A-flat7 with passing F, 23:4.5 D-flat over A-flat;
  24:1 C dim, 24:2.5 A-flat7 over E-flat, 24:3 the three thematic lines land on A-flat: a bare fifth
  (A-flat, E-flat), 24:4 A-flat minor (C-flat): the major is never confirmed; 25:1 C-flat major over E-flat
  (= the Neapolitan of b-flat), 25:3 C-flat over G-flat (passing 6/4), 25:4 E-flat minor 7 over G-flat;
  26:1 D-flat over F, 26:2 F minor (v of b-flat), 26:3 E dim7 (the first head); 27 E-G, E-G-B-flat; 28:1-28:4
  E dim7 complete (ff); 28:4.5 all four slide: A dim7 over E-flat; 29:1 the same chord re-struck, fermata.
* Dynamics: < f by 26:1; < ff by 28:1 (the dim7 complete), ff through the re-strikes, fermata (+3 beats at 66),
  general pause 1.4 s.
* Flags: D4? 24:1 (C dim in root position, the lament's leading tone under G-flat: vii dim of D-flat, a
  passing sonority on the way to the A-flat7).
* Idiom: soprano C-flat6 at 24:4.5-25:3 (violin I, E string; piano right hand). Lower staff wider than a ninth
  in 20, 22-29 (tenor leader over the low lament): the piano gives the tenor to the right hand when the alto
  lies above C5, else the pedal sustains the bass.

#### Section 3 boundary (bars 20-29)

| voice | first attack at 20:1 | last note |
|---|---|---|
| S | F5 | C5 at 29:1 (held to the section end) |
| A | Ab4 | A4 at 29:1 (held to the section end) |
| T | Db4 | Gb3 at 29:1 (held to the section end) |
| B | Db2 | Eb2 at 29:1 (held to the section end) |

First sonority (20:1): Db2 Db4 Ab4 F5 = D-flat major. Last sonority (29:1): Eb2 Gb3 A4 C5 = A dim7 over E-flat.

### Section 4: bars 30-34, Arioso dolente and the German-sixth pivot (94.2-117.5 s)

* Entry: 30:1 S S2 c'' (LOCKED 30-33); 34 soprano c''2 b'2 KEEP (the b6-5 sigh).
* Map: S 30:1-34:1 LOCKED; 34:1-35:1 KEEP. A 30:1-31:4 FREE; 31:4-32:2 KEEP (F held over G-flat: the 7-6);
  32:2-35:1 FREE. T 30:1-32:1 FREE; 32:1-33:4 KEEP (B-flat held, the cadential 6/4's 4-3 at 33:3); 33:4-34:1
  FREE; 34:1-35:1 KEEP (G-sharp, A, G-sharp). B 30:1-31:1 FREE; 31:1-33:1 KEEP (E-flat D, then the
  diminished-fourth fall to G-flat, F); 33:1-35:1 FREE.
* FREE work: voicing inside the pulse only (rule 5 exemption above); one more suspension per bar is welcome.
* Harmony: 30:1 V (F major, third present from the downbeat), 30:4 i6/4; 31:1 ii dim 6 (C dim over E-flat),
  31:4 V7/iv (B-flat7 over D: the tenor's A-flat resolves down); 32:1 iv6 with the alto's F as a 7-6 over
  G-flat (the arioso's peak), 32:2 iv6; 32:3 cadential 6/4 with E-flat (D-flat in the soprano = b6), 32:4.5
  6-5; 33:1 V7 sus4, 33:3 V7 (4-3); 34:1 E with C held (the German sixth's C over E: an augmented triad, b6),
  34:2 A minor 6/4 (the tenor's A: the new key glimpsed), 34:3 E major (V of a).
* Dynamics: subito pp at 52, < mp to the 7-6 at 32:1, > pp by 34. Piano: una corda, pedal each harmony.
* Flags: MEL 32:1 (bass diminished fourth D-G-flat, the lament figure); XREL 33:4-34:1 (alto E-flat, bass E:
  the enharmonic pivot itself); the diminished fourth G-sharp3/C5 at 34:1 is the pivot sonority, intended.

#### Section 4 boundary (bars 30-34)

| voice | first attack at 30:1 | last note |
|---|---|---|
| S | C5 | B4 at 34:3 (held to the section end) |
| A | A3 | E4 at 34:4.5 |
| T | F3 | G#3 at 34:4.5 |
| B | F2 | E2 at 34:1 (held to the section end) |

First sonority (30:1): F2 F3 A3 C5 = F major. Last sonority (34:4.5): E2 G#3 E4 B4 = E major.

### Section 5: bars 35-45, Fuga inversa: three entries, A minor established, deceptive link (117.5-155.6 s)

* Entries: 35:1 B INV (a) e; 35:4 A CS1 inv.; 36:1 S CS2 inv.; 37:1 T INV (e) b, a 5th above, 2 bars later;
  41:1 S INV (a) e'', the third entry; 41:4 B CS1 inv. (the lament rising); 42:1 A CS2 inv. (lower octave).
* Map: S 35:1-36:1 FREE (rest: the inversion alone); 36:1-39:1 CS; 39:1-39:3 FREE; 39:3-41:1 KEEP (E5 over
  the root-position A minor, D, the leading tone D-sharp held, rest); 41:1-45:4 LOCKED; 45:4-46:1 FREE (rest).
  A 35:4-39:3 CS, landing 39:3; 39:4-41:1 KEEP (C, B, F-sharp, E); 41:1-42:1 FREE; 42:1-44:4 CS, landing 44:4;
  45:1-46:1 KEEP (cadence and the G-sharp of the link). T 37:1-41:4 LOCKED; 41:4-45:1 FREE (rests in the
  skeleton); 45:1-46:1 KEEP. B 35:1-39:4 LOCKED; 39:4-41:4 FREE; 41:4-45:1 CS; 45:1-46:1 KEEP (F-D-A, then E).
* FREE work: the tenor rests 41:4-44 in the skeleton (the third entry in three voices, as entry 3 of the
  exposition); a composer may bring it back earlier with a free line, but the alto's CS2 inv. and the rising
  bass leave little room (A3-D4 in 43-44): prefer a late re-entry (44) or a line above the alto's CS2 only
  where it lies below A4. The accelerando "poi a poi di nuovo vivente" may gain eighth motion in 39:4-41.
* Harmony: 35 E alone (V of a, F = b6 neighbour); 36 E under C (i6/4 of a); 37:1 E with the tenor's B entering
  under CS2 inv.'s C (a minor ninth that the line resolves), 37:3 B minor 7 over D; 38:1 E major over B
  without its root (V), 38:3 G-sharp dim (vii dim), 38:4.5 A minor over E; 39:1 ii dim 6 (B dim over D), 39:2.5
  iv6, **39:3 i in root position, complete (A2 A3 C4 E5)**; 39:4 B minor 7, 40:1 B major (V of e), 40:4 e: i;
  **41:1 a: cadential 6/4, 41:3 V (E, no fifth), 41:4 i (bass E-A)**; 42:1 i6; 42:4.5 G7 over D (passing);
  43:1 i6/4 passing, 43:2.5 iv6, 43:3 IV6 (D major over F-sharp, melodic minor); **44:1 V6 (E over G-sharp),
  44:3 vii dim, 44:4 i (bass G-sharp-A)**; **45:1 iv6, 45:2.5 iv, 45:3 i with a'' on top (iv-i)**; 45:4 E major
  (V of a, no seventh), resolving deceptively to F at 46:1 (VI of a = V of b-flat).
* Dynamics: pp (35) < mf (45:3), accelerando 64 to 76.
* Flags: DIR 37:2.5 (a hidden fifth inside the motor on a weak eighth); D4? 42:4.5 (CS2 inv.'s leap figure G
  over D, weak eighth, passing G7) and 43:4.5 (the INV's B over the rising bass's F-sharp, weak eighth).
* Idiom: the alto's CS2 inv. at 42-44 goes down to A3 (violin II is fine; piano: left hand may take it).

#### Section 5 boundary (bars 35-45)

| voice | first attack at 35:1 | last note |
|---|---|---|
| S | rest (first note E5 at 36:1) | rest (last note A5 at 45:3) |
| A | rest (first note A4 at 35:4) | G#4 at 45:4 |
| T | rest (first note B3 at 37:1) | B3 at 45:4 |
| B | E3 | E2 at 45:4 |

First sonority (35:1): E3 alone. Last sonority (45:4): E2 B3 G#4 = E major (V of A minor), resolving to F.

### Section 6: bars 46-54, Dominant pedal, combination, Climax II, dominant hinge (155.6-186.9 s)

* Entries: 46:1 B INV augmented f, (LOCKED 46-55:1); 48:1 A S2 c'' and T S1 bes together; 50:3 S S1 heads in
  diminution (F, G-flat, A, C); 52:1 A heads in diminution (E).
* Map: S 46:1-50:3 FREE (silent in the skeleton); 50:3-53:4 LOCKED; 53:4-55:1 KEEP (A at the fermata, then F
  E-flat C A into the tune). A 46:1-48:1 FREE (silent); 48:1-53:3 LOCKED (S2, then its heads); 53:3-55:1 KEEP
  (E, F doubling the root at the fermata, then C A C). T 46:1-48:1 KEEP (the lament lead-in); 48:1-52:3 LOCKED
  (S1, broken off into C7); 52:3-55:1 KEEP (B-flat, G, C, then A C E-flat). B LOCKED throughout.
* FREE work: the soprano may enter before 50:3 (e.g. a sustained line from 48 above S2), but S2 must stay the
  top thematic voice in 48-49 (do not sit a second above it) and 46-47 stay two voices (misterioso).
* Harmony: 46:1 F with B-flat (Vsus4, two voices), 46:3 V, 47:1 v (A-flat), 47:3 V with G, 47:4 the pedal's
  G-flat under C (A dim7 implied); 48:1 Vsus4 (S1 and S2 enter), 48:3 i6/4 over V, 49:4 the G-flat neighbour
  again; 50:1 V7sus4, 50:3 V with the b6 (D-flat to C) as the first head sounds; 51:1 C dim over E-flat, 51:3
  A dim over E-flat (with 51:1's G-flat: vii dim 4/2 arpeggiated); 52:1 C major (V/V, "the light": the alto's E), 52:3 C7 (the tenor's
  B-flat), **53:1 C7 complete, B-flat 6 on top (fff)**, 53:3 E dim7 over D-flat (vii dim 7 of V), **53:4 V
  (F2 C4 F5 A5, root doubled), fermata**; 54:1 V4/2 (E-flat bass), 54:4 vii dim 4/2 (G-flat bass); 55:1 I.
* Density: 13, 12, 12, 13 attacks in bars 50-53 (revision 1: 9, 9, 7, 9); the sixteenths are the piece's first.
* Dynamics: subito p misterioso (46); < mp (48-50); < f (50-52); < fff (52-53:4); fermata (+2 beats); f at
  54:1 diminuendo to p at 55 through the dominant (no breath, no subito).
* Flags: XREL 47:3-47:4 (tenor G, then the pedal's G-flat neighbour: the lament's chromatic step against the
  augmentation); XREL 53:2.75-53:3 (the alto head's D, then the bass's D-flat: a sixteenth neighbour); D4? 54:3
  (A over E-flat: the tritone of V4/2).
* Idiom: the pedal F2 is held 46:1-50:3: piano sostenuto pedal on F2 so the left hand can take the tenor;
  cello long bows, no accent on the G-flat neighbours. C2 (51:4-53:2) is the cello's open C. Soprano C6
  (52:3) and B-flat 5 (53:1), violin I. Lower staff wider than a ninth throughout (pedal under the tenor).

#### Section 6 boundary (bars 46-54)

| voice | first attack at 46:1 | last note |
|---|---|---|
| S | rest (first note F5 at 50:3) | A4 at 54:4 |
| A | rest (first note C5 at 48:1) | C4 at 54:4 |
| T | Bb3 | Eb3 at 54:4 |
| B | F2 | Gb2 at 54:4 |

First sonority (46:1): F2 Bb3 (Vsus4, two voices). Last sonority (54:4): Gb2 Eb3 C4 A4 = A dim7 over G-flat
(vii dim 4/2), resolving to I at 55:1.

### Section 7: bars 55-66, Apotheosis and coda (186.9-232.1 s)

* Entries: 55:1 S the whole tune, major (LOCKED 55-63:1); 55:4 B CS1 in major (the lament); 56:1 T CS2 in
  major; 59:1 B ANS major (LOCKED 59-63:1); 61:1 T the answer's mirror, bars 3-4; 65:1 T S1 head (LOCKED).
* Map: S 55:1-63:1 LOCKED; 63:1-65:1 KEEP (d'' held); 65:1-67:1 FREE. A 55:1-59:1 FREE; 59:1-59:2.5 KEEP (A,
  the third of V7); 59:2.5-60:3 FREE; 60:3-61:1 KEEP (A under the tune's peak, then G); 61:1-62:1 FREE;
  62:1-63:1 KEEP (E: C7/B-flat complete, then A); 63:1-67:1 FREE. T 55:1-56:1 FREE; 56:1-58:4 CS, landing 58:4;
  59:1-61:1 FREE; 61:1-62:4 CS, landing 62:4 (E-flat, also KEEP 62:4-63:1: V7 complete); 63:1-65:1 FREE;
  65:1-66:4 LOCKED. B 55:1-55:4 FREE; 55:4-58:4 CS; 59:1-63:1 LOCKED; 63:1-67:1 KEEP (tonic pedal re-struck
  every bar).
* FREE work: the alto (55-66) is the section's free voice: make it cantabile, with suspensions under the tune's
  long notes (55, 56, 58, 60), always below the tune and never doubling its neighbour notes at the octave;
  never F where the keep asks for the third. The tenor 59-60 carries A and E-flat of V7 (not the answer's F).
  The coda alto (63-64) sings the inversion's head in major under the held d''; keep the tenor's final head
  audible (viola, piano left hand).
* Harmony: 55:1 I, 55:4 I6/4 (the lament enters), 55:4.5 vi6 passing; 56:1 I6, 56:4 ii7; 57:1 vi6 (G minor
  over B-flat), 57:2 V6 with the tune's B-flat as a retardation, 57:3 v6 (F minor over A-flat: the minor
  shadow), 57:4.5 v6/5; 58:1 iv6 (E-flat minor over G-flat), 58:3 ii dim (C dim over G-flat), 58:4 I6/4;
  59:1 V7 complete (the answer enters), 59:4 I6/4, 59:4.5 V6/5 of V; 60:1-60:4 V (the tune's peak f'' over F A C
  F at 60:4), 60:4.5 C7 over E; 61:1 V7 (the tune's e-flat''), 61:2.5 vii half-dim 7 of V over G; 61:4.5-62:1
  C7 over B-flat (V4/2 of V); 62:4 V6/5 (A C E-flat), 62:4.5 V7 complete; **63:1 I (c''-d'')**; 63:4.5 I with
  the inversion head's G; 64 I; 65:1 I, 65:3 V7 over the tonic pedal (65:4.5 the tenor's A), 66:1 I, 66:3 I
  complete (fermata, d'' on top).
* Dynamics: p dolce (55) < mf (59) < f (60:4, the tune's peak) > mp (63) > pp (66), fermata. Tempo 72,
  ritardando to 56 from 63. Piano: pedal each harmony; strings: violin I sings the tune, the others sotto voce
  except the lament (cello), the answer (cello) and the last head (viola).
* Flags: XREL 60:4.5-61:1 (the answer's E natural, then the tune's E-flat: non-simultaneous, the tune's own
  note); the augmented fifth G-flat2/D3 at 58:2.5 (the lament's G-flat under CS2's passing D: a passing eighth,
  the bittersweet point of the minor shadow, intended).

#### Section 7 boundary (bars 55-66)

| voice | first attack at 55:1 | last note |
|---|---|---|
| S | Bb4 | D5 at 66:1 (held to the section end) |
| A | D4 | F4 at 66:3 (held to the section end) |
| T | F3 | Bb3 at 66:1 (held to the section end) |
| B | Bb2 | Bb2 at 66:1 (held to the section end) |

First sonority (55:1): Bb2 F3 D4 Bb4 = B-flat major. Last sonority (66:3): Bb2 Bb3 F4 D5 = B-flat major.

---------------------------------------------------------------------------------------------------

## 7. Global rules for composers

1. Start from your starter `design/final-lab/sections/secNN_*.ly`. Deliver `score/sections/secNN_*.ly` (same
   name; keep the `% bars A-B` line; one 4/4 bar per `|`; voices contain only notes, rests, ties, bar checks).
2. Never change LOCKED spans. Countersubjects keep their notes; only the landing window may change. KEEP items
   stay. `python3 design/final-lab/spanmap.py` prints the map of your section.
3. Keep every boundary entry of your section's table (first attack at the first downbeat and the last note of
   every voice, with ties in or out). Then any two sections join as proven.
4. Verify: `python3 design/final-lab/splice_check.py score/sections/secNN_*.ly` must print PASS. It FAILS on:
   a changed boundary; a changed LOCKED, CS (outside its landing window) or KEEP note; a new unison (two voices
   on one pitch); any PAR!, BEAT, DIS! or CLASH in the section and its joins. Every new D4?, DIR, MEL or XREL
   gets a one-line explanation in a comment at the top of the file. Also read `strict.py FILE -v`: a new ACC2
   must be a suspension, a pedal-point licence or a chord seventh.
5. Enrichment: free voices move in the rhythmic gaps of the thematic lines (eighths where the subject holds,
   held notes where it moves). Prefer prepared suspensions. `suspensions.py` now counts only real ones
   (consonant preparation, dissonance against a voice that attacks, stepwise resolution while that voice still
   sounds); the skeleton has 4 on strong beats and 12 on weak beats (revision 1 claimed 12; the old counter
   credited held chord tones). Target for the finished piece: **at least 30 in total (both lines of
   suspensions.py), at least 20 of them on strong beats**. Motives for free voices: the head neighbour
   (x x x-1), its mirror sigh (x x x+1), cell b, CS1's chromatic core, CS2's eighth-note turns. No chordal
   padding (section 4 excepted, see section 5); no parallel thirds or sixths for more than two beats; never
   more than four real voices.
6. Keep the deliberately thin places thin: the solo openings (1-4, 35), the two-voice entry 2 (5-8), the
   three-voice entry 3 (9-12), the soprano's silence before its stretto entry (20:2-21), the liquidation
   (26:3-29), the three-voice third inverted entry (42-44, unless a composer finds room), the misterioso pedal
   (46-47).
7. Ranges: S 60-84, A 53-77 (below G3 only at 9:4-12:4, which the viola takes), T 48-72, B 36-62.
8. No dynamics, tempo or articulation in the voices: they live in `plan.json`. Put intent in comments.
9. Assemble with `python3 tools/assemble.py`; check `score/music-voices.ly` with `check.py` and `strict.py`;
   re-measure with `perform.py` (210-240 s).

---------------------------------------------------------------------------------------------------

## 8. Performance sketch (`final-lab/plan.json`)

* Tempo map: 78 (1-27), rit. to 66 (28), fermata 29:1 (+3 beats) and general pause 1.4 s; 52 arioso (30-34);
  breath 0.3 s, 64 accelerando to 76 (35-45); breath 0.25 s, 76 (46-52), rit. to 68 (53), fermata on V at 53:4
  (+2 beats), 62 slowing to 56 through the hinge (54); 72 (55-62), rit. to 56 (63-66:3), final fermata on the
  complete B-flat chord (66:3, +3 beats).
* Dynamics arc: p (the tune alone) to mf at the half cadence (17); mp at the episode; < f through the false
  dawn, < ff as the dim7 completes (28:1), ff through the slide and the re-struck fermata chord (29); subito pp
  arioso, swelling to mp at its 7-6 (32:1); pp to mf through the fuga inversa (cadence 45:3); subito p
  misterioso on the pedal; mp, f, fff at the peak (53:1-4); f at the hinge diminuendo to p at the tune (no
  subito, no breath); f at the tune's peak (60:4); down to pp. Two subito cuts (30, 46); Climax II flows into
  the apotheosis instead of breaking off.
* Every hairpin has attacks in every half bar (`verify.py` audits this; the piano sets loudness at note-on).
  The fermata chord at 29:1 and the tonic pedal 63-66 are re-struck.
* Bring out (roles; piano +9 velocity, strings +0.7 level): every LOCKED span (subject, answer; cf +7/+0.5 for
  the augmentation). Countersubjects +2/+0.2, free voices -4/-0.2.
* Piano: una corda and pedal each harmony in 30-34; sostenuto on F2 in 46-50; pedal each harmony in 55-66.
  Strings: arioso eighths lightly separated; the pedal F2 in long bows; violin I cantabile for the tune at 55;
  viola takes the alto 9:4-12:4.

---------------------------------------------------------------------------------------------------

## 9. Proof table (reproduce: `cd design/final-lab && python3 build_sk.py && python3 sections.py && python3 build_labs.py`)

All results in `final-lab/proofs.txt`. check = `tools/check.py` with the four ranges (`ck.sh`); strict =
`strict.py`. Lab bar numbers inside `proofs.txt` are relative to the lab window.

| lab | claim | check (errors/PAR!/BEAT/DIS!) | strict clash | remaining flags, explained |
|---|---|---|---|---|
| T1-T6 | triple counterpoint S1/CS1/CS2, all six orders | 0/0/0/0 each | 0 | T4, T5: D4? at the tail (a passing 6/4 as the next entry starts) |
| X1_E2_cs1_over_answer | CS1 over the answer, two voices (5-9) | 0/0/0/0 | 0 | DIR 9:3 (tails in octaves; not outer voices once the bass enters) |
| X2_stretto_Db_Gb | S1 stretto in D-flat/G-flat, 4th + octave, 2 bars (20-26) | 0/0/0/0 | 0 | none |
| X2b_stretto_over_lament | the pair over CS1 in D-flat (20-26) | 0/0/0/0 | 0 | none |
| X3_liquidation | heads accumulate E dim7, all slide into A dim7 (26-29) | 0/0/0/0 | 0 | D4? 29:1 (A over E-flat: the dim7's tritone) |
| X4_mirror_trio | INV + CS1 inv. + CS2 inv. (35-39) | 0/0/0/0 | 0 | DIR 37:2.5 (weak eighth in the motor) |
| X5_stretto_INV_5th | INV stretto at the 5th, 2 bars (35-41) | 0/0/0/0 | 0 | none |
| X10_inv_third_entry | INV (S) over CS2 inv. (A) and CS1 inv. (B), cadence in A minor (41-45) | 0/0/0/0 | 0 | D4? 42:4.5, 43:4.5 (weak eighths, passing) |
| X6_S2_with_S1 | S2 and S1 entering together, the pair alone (48-52) | 0/0/0/0 | 0 | none |
| X11_three_speeds | diminution heads + S1 + INV augmented (50-53) | 0/0/0/0 | 0 | none |
| X7_combination_pedal | the whole pedal section (46-54) | 0/0/0/0 | 0 | D4? 54:3-4 (V4/2, vii dim 4/2 tritones); XREL 47:3, 53:2.75 (non-simultaneous) |
| X8_tune_over_triple_major | the tune over CS1 and CS2 in major, then over the answer, into the cadence (55-63) | 0/0/0/0 | 0 | XREL 60:4.5 (E then the tune's E-flat) |
| X9_answer_vs_mirror | the answer against its mirror, into the cadence (61-63) | 0/0/0/0 | 0 | none |
| R1_S2_over_S1_iv | resource: S2 over S1 in iv | 0/0/0/0 | 0 | DIR, XREL as before |
| sections/sec01-sec07 | each starter spliced into the skeleton with its joins, all checks of rule 4 | **all PASS**, 0/0/0/0 | 0 | as listed per section |
| **SK_final** | **the whole piece, 66 bars** | **0/0/0/0** | **0** | MEL 32:1; DIR 13:3, 37:2.5; D4? 24:1, 42:4.5, 43:4.5, 54:3; XREL 15:2.5, 33:4 (x2), 47:3, 53:2.75, 60:4.5 (none simultaneous); strict: xrel 6, acc 7, acc2 34 (pedal licences, chord sevenths, the suspensions, the tail 6/4s) |
| compile_test.ly | SK_final compiles in LilyPond 2.26 | no warnings | | |
| plan.json + perform.py | duration | 232.1 s (piano and strings) | | hairpins: every half bar has an attack |

Spelled dissonances that `check.py` cannot see (semitone arithmetic), all heard and intended: augmented
seconds and diminished fourths inside diminished sevenths (28:4.5-29:1 G-flat/A, 53:3 D-flat/E, 54:4
G-flat/A); the pivot's diminished fourth G-sharp/C (34:1); passing or neighbour eighths and sixteenths at
10:1.5, 14:1.5, 38:2.5, 44:2.5, 49:4.5 (the augmentation's G-flat against S1's A), 51:4, 52:2.75 and 58:2.5
(the lament's G-flat under CS2's D in major).

---------------------------------------------------------------------------------------------------

## 10. How the old piece's five flaws are answered

1. **Rushed subject that stopped mid-phrase**: S1 at real rhythm (4.75 bars), ends on 5 and elides; entries
   3, 4 and the stretto leader are harmonised at least twice in their first bar.
2. **Filler countersubject, padded free voices**: a lament and a neighbour-cell motor, triple invertible in all
   six orders, and turned major under the apotheosis; free voices are the descant, the episode's imitation of
   cell b, suspensions (the arioso's 7-6 and 4-3), the dominant hinge and the inversion's head in major.
3. **Diatonic harmony**: Neapolitans (as chords and as a region), dim7 accumulation and slide, the
   German-sixth pivot, a real A-minor cadence and a deceptive exit, V/V, mixture in the major apotheosis.
4. **No devices beyond an octave stretto**: triple counterpoint (6 orders) and its mirror (2 orders), stretto
   at the 4th in the relative major, head stretto building one chord, inversion stretto at the 5th, a third
   inverted entry, the two subjects combined over the inversion in augmentation, augmentation and diminution
   at once (three speeds), the tune over the triple counterpoint in major, the answer against its mirror.
5. **Block form, flat dynamics**: five parts after Op. 110; the tonal arc false dawn, collapse, neighbour key,
   dominant, true dawn; Climax I (37%) and Climax II (77%) with different gestures (collapse and general pause
   against a continuous dominant descent into the tune).

---------------------------------------------------------------------------------------------------

## 11. Open risks

1. **Tempo and recognition.** Part I at 78 (72% of the film's 108) keeps gravity; the apotheosis at 72 is well
   above the floor where dotted halves stop sounding like the tune. Do not slow either.
2. **The false dawn could read as the tune "arriving" early.** It is in stretto, in D-flat and G-flat, over
   the lament, and it darkens within four bars; keep it at mp < f, never broader, so the apotheosis stays the
   first full statement.
3. **Violin II compass**: the viola must take the alto 9:4-12:4 in the quartet; violin II resumes at 13:1.
4. **Keyboard spans.** The lower staff (T+B) is wider than a ninth in 13, 15-17, 19, 20, 22-34, 45, 46-54, 56,
   59, 60 (widest 25 semitones at 51:4, tenor over the pedal); the upper staff reaches 23 semitones at 12:1.5.
   MIDI rendering is unaffected; a printed piano score needs cross-staff distribution and the sostenuto pedal
   (46-50) as given in the section idiom notes.
5. **Pedal and climax harshness.** 48-50 hold S1's B-flat as a 4th over the F pedal (Vsus4); 50:3 has the b6
   (D-flat) over V; 53:1 is fff at the top of the range. Voice the top lighter than the bass on the piano.
6. **The one skeleton unison (5:3)** is kept on purpose (section 1). splice_check lists it as known and fails
   any new one.
7. **Three-voice third entry (42-44).** Thin by design; a composer may add a fourth voice only where the alto's
   low CS2 inv. leaves room.
8. **Duration headroom is 7.9 s** (232.1 of 240). Longer fermatas, slower ritardandi or long reverb tails must
   stay inside it; the final reverb tail is not in the 232.1 s.
9. **Suspension target** (rule 5) is now counted strictly; composers who meet it with weak-beat figures only
   will miss the strong-beat quota.
10. **Checker leniency.** check.py measures semitones and accepts any stepwise dissonance; strict.py and the
    spelled-dissonance list above cover the gaps. Composers keep that standard (rule 4).

---------------------------------------------------------------------------------------------------

## 12. Critique responses (round 1, `design/critique_r1.json`)

Bar numbers are revision-2 bars unless marked "old". Everything marked changed is in the notes (SK_final.ly),
proved (proofs.txt) and enforced (splice_check).

### Critic 1 (musical), major

| # | finding | response |
|---|---|---|
| C1-M1 | Apotheosis thin and static: hollow unisons (four-octave F at the tune's peak), 58:1 not C7, V without A/E-flat, "mirror" = a pedal, the film's I-IV6/4-I | **Changed.** 55-58: the tune over the exposition's triple counterpoint in B-flat major (CS1 the lament in the bass from 55:4, CS2 in the tenor from 56), the critic's order T5 in major; the alto carries the thirds (A at 59:1, 60:3-4; KEEP); 62:1 is C7/B-flat with E; 62:4.5 a complete V7 (A, E-flat; KEEP), so 62-63 is a real V7-I under c''-d''; the mirror survives only in 61-62 where it moves against the answer; no IV6/4 over the tonic. Hollow four-voice chords in 55-62: none (grid). |
| C1-M2 | Climax II unearned: slowing surface, drones, soprano masking S2, fff chord with doubled fifth, doubled seventh at the C7 | **Changed.** (a) soprano silent until 50:3; S2 is the top thematic voice. (b) The climax is built from S1 heads in diminution (the first sixteenths), rising F, G-flat, A, C, passed to the alto (E) in stretto, over S1 in normal values and the INV in augmentation: three speeds (lab X11); 13/12/12/13 attacks per bar in 50-53. (c) 53:1 C7 complete (C G E B-flat, no doubled seventh; the tenor leaves B-flat for G); 53:4 V with the root doubled (F2 C4 F5 A5). |
| C1-M3 | Bars 1-29 never leave B-flat/F/E-flat minor; bar 21 replays bar 10; Neapolitan twice at the same CS2 point; S1 five times on B-flat; S2 always c'' over F | **Changed (preferred fix).** The episode's bass falls in fifths into D-flat; the stretto is in D-flat (tenor leader, new voice and register) and G-flat (soprano follower), over the lament in D-flat in the bass; it darkens through A-flat minor and C-flat (the Neapolitan of b-flat as a region) and sinks through F into the dim7. Bar 21 is no longer entry 3; CS2's Neapolitan occurs once (12:3). S1 on B-flat: 1, 9, 48 (combined with S2), 55 (major). **S2 kept at c'' over F (rejected part)**: its three statements have three functions (alone, lamenting; combined with S1 over the augmentation; inside the whole tune in major), and the tune's own pitch is the recognition anchor for a listener who found the melody "off"; the travel is given to S1 and the inversion instead. |
| C1-M4 | A minor never established; 39:3 without third, tenor/bass unisons | **Changed (both fixes).** (a) 39:3 root-position complete A minor (A2 A3 C4 E5), no unisons (the bass lands on A2; the free notes avoid the tenor). (b) A third inverted entry (soprano, 41) over the lament rising in the bass and CS2 inv., with a cadential 6/4-V-i (41), V6-vii dim-i (44:4) and iv-i with the tonic on top (45:3); E major then resolves deceptively to F, the home dominant. Paid for by Part I at 78 (the critic's suggestion), the inversa at 64-76 and the apotheosis at 72: 232.1 s. |
| C1-M5 | Piano: the ff fermata barely struck; ties through crescendi | **Changed.** All four voices re-strike the fermata chord at 29:1 (and all re-strike the dim7 at 28:4); the crescendo reaches ff when the dim7 completes (28:1); the tonic pedal is re-struck every bar in 63-66; the old soprano tie f'' (old 46-47) no longer exists. verify.py audits every hairpin: no half bar without an attack. |
| C1-M6 | Hinge one bar, deflation, V-IV retrogression, three plagal/minor-iv colours | **Changed, with a different means than proposed.** No subito pp and no breath: the V fermata (53:4) continues as dominant function, V4/2 (54:1) and vii dim 4/2 (54:4), then I (55:1); the soprano falls A F E-flat C A and its leading tone resolves to the tune's first note. The locked augmentation (E-flat, G-flat, B-flat) makes this reading possible; a bVI chord would have needed a G-flat bass on the downbeat and added a fourth plagal/modal colour, which the critic's own point argues against. One minor shadow remains (the lament's A-flat and G-flat, 57-58); IV6/4 at old 52:3 and the minor iv6/4 at old 60 are gone. The hinge stays one bar, but it is 6.7 s of continuous dominant after the fermata, not a 4-second drop. |

### Critic 1, minor

| # | finding | response |
|---|---|---|
| C1-m1 | 33-34 identical repeated chords | **Changed.** 33: V7 sus4 resolving 4-3 at 33:3 (the tenor's B-flat from the cadential 6/4); 34:2 the tenor's A (an A-minor 6/4 over the E). |
| C1-m2 | Arioso without a dolente peak; 31:4 bare D-F | **Changed.** 31:4 V7/iv complete (the tenor's A-flat resolving down); the alto's F held over the G-flat bass as a 7-6 at 32:1 is the peak (< mp). |
| C1-m3 | Violin II below compass 9:4-13:3 | **Changed (with C2-m7's correction).** The viola takes 9:4-12:4; violin II resumes at 13:1. |
| C1-m4 | Unisons 5:3, 15:2.5; add a unison scan | **Changed.** splice_check fails any new unison; 15:2.5 removed (soprano E5); 5:3 kept on purpose (section 1). |
| C1-m5 | 9:1-9:2.5 is E dim, not C7 | **Label corrected** (sections 2.1 and 6.1). |
| C1-m6 | Entry 4 descant thin; hollow 13:3, 17:3 | **Changed.** New descant completes every chord; 17:3 is C7 (the alto's B-flat); declared the section's main task. |
| C1-m7 | Two climaxes with the same gesture | **Changed.** Climax I keeps fermata, general pause and subito pp; Climax II has a shorter fermata (+2), no breath, no subito, and diminuendo through the dominant into the tune. |
| C1-m8 | Apotheosis dynamics misaligned | **Changed.** f arrives at 60:4 (the tune's f'') and holds to 61:3. |
| C1-m9 | Hollow 46:3 (old) inside the crescendo | **Changed.** 50:3 is F2 C4 D-flat5 F5 with the first head; no hollow four-voice chord in 46-54 except the sixteenth 50:4.75. |
| C1-m10 | Coda: d'' held 8 beats with nothing moving | **Changed.** Under the held d'' the alto sings the inversion's head in major and descends; the tenor moves; the tonic pedal is re-struck each bar. (The lament in the alto was the critic's alternative if C1-M1 was not adopted; C1-M1 was adopted.) |
| C1-m11 | "54% chromatic" is not evidence | **Removed** from the blueprint. |
| C1-m12 | 13:1 upper-staff span; decide print distribution now | **Done** in the idiom notes of sections 1-7 and risk 4 (measured with `sections.py --spans`). |
| C1-m13 | Mirror claims inaudible where the head is a repeated note | **Changed.** The tune is no longer set over its mirror; the answer's mirror is kept only in 61-62, where it moves in contrary motion. |

### Critic 2 (contrapuntal), major

| # | finding | response |
|---|---|---|
| C2-M1 | Liquidation never sounds the E dim7 | **Changed (the critic's voicing).** Each head holds until all four sound; E dim7 complete 28:1-4 (ff); all four voices strike x8 (x-1)8 together at 28:4-4.5 into A dim7 over E-flat; re-struck at 29:1. Claims in sections 0, 4 and 6 now describe exactly this (lab X3). |
| C2-M2 | Combination of subjects nominal | **Changed.** Alto rests in 46-47; S2 (alto) and S1 (tenor) enter together at 48:1 over the augmentation (16 beats, lab X6); the soprano's INV head is gone. |
| C2-M3 | Bar 20 static; tenor rest not declared FREE; section-2.1 claim false for bar 5 | **Changed.** Bar 20 (now the tenor leader in D-flat) moves I, IV6/4, V, I6; claim 2.1 now covers entries 3, 4 and 20 and says entry 2 is two voices by design. |
| C2-M4 | Episode instruction not executable | **Changed.** The skeleton's episode contains the proven line (the alto answers cell b at 18:3 with B-flat-D-flat; the tenor moves in quarters) and the spec names bar, beat and pitch. |
| C2-M5 | splice_check only warns on countersubjects; "keep" items unchecked; T 49-50 FREE inside a lock | **Changed.** splice_check fails on countersubject changes outside `landing_from`, on 30 KEEP items, and on new unisons; the tenor's S1 lock ends at 52:3 where the subject breaks off, and the held B-flat after it is a KEEP item; `spanmap.py` prints every voice's map, and the section specs quote it. |

### Critic 2, minor

| # | finding | response |
|---|---|---|
| C2-m1 | INV stretto unisons 39:3, 39:4.5 | **Changed.** Bass lands on A2; the free bass goes to B2; no unisons (verify). |
| C2-m2 | Harmony labels not matching the notes | **Changed.** All labels are read from `grid.py`; e.g. 37:1 is described as the tenor's B entering under CS2 inv.'s C, 38:1 as V without its root, 45:4 as E major (no seventh). |
| C2-m3 | "IV, the first G natural" false | **Removed** (the bar no longer exists). |
| C2-m4 | "Nine-bar pedal" wording | **Corrected**: F is held 46:1-50:3; the augmentation's dominant function runs 46-54. |
| C2-m5 | Checker leniency; spelled dissonances (old 60, 34) | **Answered.** A letter-aware scan lists every spelled dissonance (section 9); old 60 no longer exists; 34:1 is the pivot, intended. |
| C2-m6 | suspensions.py over-counts | **Changed.** Real preparation, an attacking agent, resolution over it, re-strikes skipped, one count per suspension; the skeleton has 4 (+12 on weak beats), not 12. Rule 5's target restated. |
| C2-m7 | Viola cannot take 9:4-13:3 | **Accepted**: viola 9:4-12:4 only. |
| C2-m8 | Unisons 5:3, 15:2.5; overlap at old 57:1 | 15:2.5 removed; 5:3 kept (section 1); the old 57:1 overlap no longer exists (the apotheosis alto is new). |
| C2-m9 | Keyboard spans worse than stated; hole between alto and tenor in the pedal | **Measured and stated** (risk 4, idiom notes). In 50-53 the alto (E5) and tenor (G3-C4) are an octave+ apart around the climax, with the soprano's heads above; on the piano the right hand takes soprano and alto, the left the tenor, the sostenuto the bass. |
| C2-m10 | Tenor lead-in's G-flat doubling the bass; doubled seventh of C7 | **Changed.** The lead-in ends on C (47:4), stepping into S1's B-flat; C7 at 53:1 has one B-flat. |
| C2-m11 | Old 42:4.5 alto B-flat vs tenor A | The same meeting of S2's B-flat and S1's neighbour A recurs at 49:4.5 now that the subjects enter together: it is the two subjects' own notes on a weak eighth, and the proof of the combination (X6) passes. Kept. |
| C2-m12 | Rule 5 contradicts section 4 | **Changed.** Section 4 is exempt, with the reason (section 5). |
| C2-m13 | plan.json roles (alto 20:1, soprano cs to 39:4) | **Changed.** All roles rebuilt from piece.py; the soprano's CS2 inv. role ends at 39:1; bar 20's alto is FREE by design. |
| C2-m14 | CS1 is not Bach's chromatic fourth | **Reworded** (section 2.3). |
| C2-m15 | Head treatment inconsistent (tie vs re-strike) | **Changed.** All four heads re-strike together at 28:4 and slide together at 28:4.5; all four re-strike at 29:1. |
| C2-m16 | (verified correct: duration arithmetic, entry lengths, answer, mirrors, entry 4 = T4 down a 4th) | Unchanged items stay verified; duration re-measured (232.1 s). |

### Removed with the superseded design

`part4_variants.py` and `search_E4_descant.py` (search records for Part IV variant x1 and descant h, both
replaced), `R2_P06_apotheosis_frame.ly` (proposal 4's apotheosis, no longer the source), labs X2 (old stretto),
X6 (old S2-then-S1), X8 (old tune-over-mirror), and old risk 10 (the INV head masking S2). All are in git
history.
