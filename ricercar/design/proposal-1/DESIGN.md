# Proposal 1: "Ricercar a 4 sopra il tema di Jurassic Park" (Bach-strict)

Status: IN PROGRESS. Sections marked VERIFIED have lab files that pass
`tools/check.py` with 0 PAR!, 0 BEAT, 0 DIS!, 0 D4?, 0 DIR, 0 CROS.

## 0. Concept in one paragraph

A double fugue in the stile antico, alla breve, in B-flat minor. Subject I is the
first half of the theme at its real rhythm. Subject II is the second half. The piece
works through the learned devices of the Ricercar a 6 and the Art of Fugue: triple
invertible counterpoint, invertible counterpoint at the 12th, mirror inversion of
the whole contrapuntal complex, stretto at several intervals, and the combination
of the two halves of the theme. The augmented answer in the bass becomes the
dominant pedal of the climax. The large-scale shape follows late Beethoven: a lyrical
major-key episode in the middle (Hammerklavier), an inversion section (Op. 110),
augmentation in the bass near the end (Op. 131 No. 1), then a general pause and the
theme's transfiguration in B-flat major.

Working files: `lab/mats.py` (all materials), `lab/build_core.py` (core proofs),
`lab/sections.py` (section drafts), `lab/ricer.py` (toolkit plus the strict filter),
and the search tools `lab/search.py`, `lab/matrix.py` and `lab/augsearch.py`.

**Strict filter.** `tools/check.py` accepts accented passing notes on the half-note
beats. The alla-breve style of this proposal does not, so every lab is also run
through `ricer.strict()`. It lists each dissonance on beat 1 or 3 that is not a
suspension or retardation. Each item it reports is explained by ear below.

## A. Materials (tonic level, B-flat minor, 2/2)

### Subject I (S1): theme bars 1-4, real rhythm, minor mode, with a landing note
```
bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' | c''2
```
- **Rhythm.** The theme is unchanged. In alla breve the dotted halves carry the
  pulse, so the tune keeps its breadth. This fixes the previous piece's halved values.
- **Landing.** The subject ends on c'' on the downbeat of theme bar 5. That note is
  2^ over V, a half cadence, so no entry stops on the pickup. The landing c'' is
  elided into the countersubject: the voice goes straight on.
- **Implied harmony.** i (bes pedal with a leading-tone sigh) | i | i–iiø7–iv |
  iv–i6–i | V. It is a tonic prolongation followed by a half cadence.
- **Tune tweaks.** None in S1 apart from the minor third (des''), which is
  already in THEME.md.

### Answer (A1): real, at the upper fifth, F minor
```
f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f'' | g''2
```
The answer is real because the subject begins on 1^ and does not touch 5^ until its
cadence. There is no early dominant that would call for a tonal answer. The answer's
landing, g over G major (V of C), is used on purpose: the exposition ends on G7 and
the tonal plan's second station is C minor.

### Countersubject 1 (CS1): the lament
```
f'2 ges'2 | g'4. aes'8 bes'4. c''8 | bes'2. aes'4~ | aes'4 g'4 ges'4 f'4 | e'2
```
CS1 holds 5^, rises chromatically f-ges-g-aes-bes-c (passus duriusculus), and turns
at the subject's climb. From there come a 2-3 bass suspension (bar 3) and a 4-3
suspension (bar 4), then the chromatic fall aes-g-ges-f-e. That fall is the
descending tetrachord of the royal theme in the Musical Offering. Its rhythm
complements the subject's: CS1 moves on beats 1 and 3 while the subject holds, and
it takes the dotted cell in bar 2, one bar before the subject does.
- Invertible at the octave: P01 and P02.
- Invertible at the 12th: P04 and P05. At the 12th below the subject, CS1 becomes
  a rising chromatic bass under the held tonic (bes ces c des ees f), which is used
  at the return (section F).
- Not invertible at the 10th. The parallel sixths of bar 4, beats 3-4, would become
  octaves, so the 10th is not used.
- Its landing is flexible. It is e' (V of F) before an answer entry in two voices.
  When the next entry is in the bass, CS1 stops on f' (bar 14 of the exposition).

### Countersubject 2 (CS2): the quarter-note motor
```
r4 f''4 ees''4 des''8 c''8 | bes'4 c''4 des''4 ees''4 | des''4 c''4 ees''4. des''8 | c''2 bes'4. aes'8 | g'2
```
CS2 keeps the quarter-note motion going that the subject lacks. Bar 1 falls a
tetrachord (f ees des c) and bar 2 climbs it back (bes c des ees), so the line
contains its own mirror. It uses the theme's dotted cell twice. It enters after a
quarter rest so the subject's head is heard alone first; when it follows a cadence,
bes' replaces the rest (bar 11).
- **Triple invertible counterpoint S1/CS1/CS2 at the octave.** All six vertical
  orders are clean (P06).
- When CS2 is the lowest voice, its landing g is changed to c. Otherwise the
  landing makes a 6/4 (strict flag in P06_S1-CS1-CS2 and P06_CS1-S1-CS2).

### Inversion (I1), mirror inversion of the whole complex
Diatonic mirror in harmonic minor, axis 1^<->5^ (the Art of Fugue convention). The
leading-tone sigh bes-a-bes becomes the lament sigh f-ges-f:
```
I1  = f''2. f''8 ges''8 | f''2. f''8 ges''8 | f''4. ees''8 ees''4. c''8 | c''2. des''8 f''8 | ees''2
IC1 = bes''2 a''2 | aes''4. g''8 f''4. ees''8 | f''2. ges''8 g''8~ | g''4 aes''4 a''4 bes''4 | ces'''2
IC2 = r4 bes'4 c''4 des''8 ees''8 | f''4 ees''4 des''4 c''4 | des''4 ees''4 c''4. des''8 | ees''2 f''4. g''8 | aes''2
```
IC1 is the exact mirror of CS1 except for one note. A chromatic passing ges'' in
bar 3 turns the mirrored 2-3 suspension into a semitone retardation. As a result
the inverted lament becomes a chromatic ascent of seven semitones
(f-ges-g-aes-a-bes-ces). The mirrored trio I1/IC1/IC2 is clean in all six orders
(P07). So the complex is triple invertible both rectus and inversus.

### Subject II (S2): theme bars 5-8
```
c''4. a'8 f'4 des''8 bes' | c''2. f''8 bes' | ees''4. des''8 des''4. c''8 | c''1 | c''2
```
S2 is 4.5 bars, the same length as S1, so the two halves of the theme can sound
together and land together. The short form S2s ends on `c''2` after 3.5 bars.
(Combination proofs: section B.)

## B. Proof table (core)

Summaries from `python3 lab/build_core.py` (full lines in `lab/proofs_core.txt`):

| lab | claim | PAR! | BEAT | DIS! | D4? | strict (by ear) |
|---|---|---|---|---|---|---|
| P01_S1_over_CS1 | S1 over CS1, 8ve | 0 | 0 | 0 | 0 | 1: 1:1 bes/f 4th in two voices only; a lower voice is always present in use |
| P02_CS1_over_S1 | CS1 over S1, 8ve | 0 | 0 | 0 | 0 | 0 |
| P03_CS1_over_A1 | CS1 over answer (bars 5-9) | 0 | 0 | 0 | 0 | 0 |
| P04_S1_over_CS1at12 | CS1 at the 12th, as bass | 0 | 0 | 0 | 0 | 1: 2:1 chromatic bass c under held bes (inverted pedal) |
| P05_A1_over_CS1at12 | answer over CS1 at the 12th | 0 | 0 | 0 | 0 | 1: same spot, same reason |
| P06_* (6 files) | triple counterpoint S1/CS1/CS2, all orders | 0 | 0 | 0 | 0 | at most 2 per file: entry 4ths and the CS2-bass landing (see above) |
| P07_* (6 files) | mirrored trio I1/IC1/IC2, all orders | 0 | 0 | 0 | 0 | at most 2 per file, same kind |

## C. Architecture

(in progress; see section C below when complete)

### VERIFIED: Exposition, bars 1-18 (+ joint bar 19:1), lab `E1_exposition.ly`
Checker: `errors 0, parallels 0, beat-par 0, unjustified 0`. Strict: one item, 19:1
f''/g. That is the prepared seventh of G7 (tied from 18:4), which resolves to ees''
in bar 19.

| bars | S | A | T | B | harmony / key |
|---|---|---|---|---|---|
| 1-4 | S1 (bes') | - | - | - | b-flat: i ... V |
| 5-8 | CS1 (answer level, elided from c'') | A1 (f') | - | - | f: i ... V/V |
| 9-10 | codetta | codetta | - | - | G - C/E - F - F/C (circle of fifths) |
| 11-14 | CS2 | CS1 | S1 (bes) | - | b-flat, S1 as bass = tonic pedal |
| 15-18 | rest, then free from 16:3 | CS2 (answer) | CS1 (answer) | A1 (f) | f minor; bass entry heard in 3 voices |
| 19:1 | f'' (7th) | d' | b | g | G7 = V7 of C minor |

Voices enter top-down, as in Op. 131 No. 1. The theme is first heard alone in the
soprano at its original pitch (violin I in the quartet), so it is recognised at once.
Keyboard: upper staff = S+A, lower = T+B. The widest lower-staff span is 14
semitones (bar 16).
