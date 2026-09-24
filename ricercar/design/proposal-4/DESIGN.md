# Proposal 4: "Ricercar sopra il canto fermo" (melodic-beauty / cantus-firmus design)

Status: IN PROGRESS. Sections marked (pending) are not yet verified; everything in the proof
table has a lab file in `lab/` that was run through `tools/ck.sh` (= project checker with the four
voice ranges S 60-84, A 53-77, T 48-72, B 36-62).

## 0. Concept in one paragraph

The whole piece is built from the tune's two halves and the idea that the tune, sung whole and
unhurried, is the goal. Part I is a grave B-flat-minor fugue on the antecedent (theme bars 1-4 at
their real rhythm). Part II adds the consequent (bars 5-8) as a second subject and proves that the
two halves of one melody can be sung at the same time. Part III turns the subject upside down and
presses it into stretto while the keys darken (flat side, Neapolitan). Part IV is a dominant pedal
that IS the subject: the answer in augmentation in the bass (a held F with its E-natural neighbour
is exactly what the augmented answer sounds like). Part V is the apotheosis: the complete tune in
B-flat major as a cantus firmus in the soprano, over the subject in augmentation as a tonic pedal
in the bass, with the inner voices weaving the subjects: the theme over itself, at two speeds.

## A. Subjects and materials

All material is written in `tools/mats.py` (single source; every lab imports it). LilyPond
`\absolute`, Dutch names, 4/4. Home key B-flat minor.

### A1. Subject I (S1) = theme bars 1-4 at the REAL rhythm, no halving

    S1:  bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes'
         + one TERMINATION, chosen per entry:
           (e) elision   -> c''   (bar 5 beat 1; the fifth over the next entry's f: answer enters BELOW)
           (t) tonic     -> bes'~ (the pickup bes' is tied on and becomes the first note of CSa)
           (c) cadence   -> c''4. a'8 bes'2   ("closed" form: the theme's own bar-5 figure turned home, 2-7-1)
           (s) the tune  -> S2    (the theme continues; this is how the cantus firmus is built)

Why this fixes flaw 1: the subject is the tune exactly as the listener knows it (dotted halves,
eighth-note pickups), four full bars, and it never stops on the pickup: the pickup `des'' bes'` always
lands on a strong note (c'' = 5th of the next entry's tonic, or the tonic bes, or the 2-7-1 cadence).
The static first bar is no longer a "static tonic chord": S1's first two bars are a pedal on the
tonic, and every countersubject below is designed to move harmonically underneath that pedal
(CSa: a chromatic lament; CSb: an eighth-note arch; the mirror: tonic/dominant oscillation).
Implied harmony of S1 alone: i (bars 1-2, V at each a') | i - ii(o) - iv (bar 3) | iv - (VI) | V (c'').

### A2. Answer: REAL, in the dominant (F minor), entering a fourth below

    A:   f'2. f'8 e' | f'2. f'8 e' | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f' | + g' (elision) or f'~ (tonic)

Justification: S1 contains no scale degree 5 at all (its pitch set is bes, a, c, ees, des), so there
is no 1<->5 exchange to adjust and a tonal answer would be identical to the real one at the head; the
real answer keeps the tune's exact intervals (bes-a neighbour becomes f-e, the leading tone of F).
The answer enters BELOW the voice that just finished S1, so the elision c'' sits a perfect fifth
above the answer's f' (checked in P02).

### A3. Countersubject a, "Lamento" (always BELOW the subject; a bass-type countersubject)

    CSa (subject context):  ees'2 d'2 | des'2 c'4. ces'8 | bes2 a2 | aes2 g4. ges8 | f2
    CSa (answer context):   bes2 a2 | aes2 g4. ges8 | f2 e2 | ees2 d4. des8 | c2

The complete chromatic descent from the 4th of the key to the 5th below (ees' ... f): a two-bar
chromatic cell (iv -> i) followed by its exact transposition a fifth lower (i -> V). Rhythm
2 2 | 2 4. 8 twice: the slow half notes move under the subject's pedal, and each cell ends with an
eighth-note chromatic slide that forms an AUGMENTED SIXTH with the subject's lower-neighbour a'
(ces'/a' in the subject context, ges/e' in the answer context) resolving outward to the octave
(bes/bes', f/f'). The second cell ends with the lament's classic close VI -> V (ges -> f). Implied
harmony (subject context, per half bar): iv | V/iv(6) | i6 | ii(o)7 - N/aug6 | i | V6 | VII - IV6 | VI - V.
Why not invertible: over a pedal the lament's first interval is a fifth (a fourth when inverted).
Instead of forcing invertibility this design gives the subject TWO countersubjects with fixed
registral roles (lament below, descant above), like a chorale setting; their mirror relation is
used later (Part III).

### A4. Countersubject b, "Sospiri" (descant, always ABOVE the subject)

    CSb (answer context, over f'):
      c''4 des''8 ees''8 f''8 ees''8 des''8 c''8 | aes''4 g''8 f''8 ees''8 des''8 c''8 bes'8 |
      a'4 bes'4 c''4 des''4~ | des''4 ees''4 f''2 | e''2
    CSb (subject context) = the same a fifth lower (f'4 ges'8 aes'8 ...).

The first quarter is the elision note of the preceding subject (c''), so CSb proper starts on beat 2.
Character: continuous eighths exactly where the subject holds its pedal (bars 1-2), a rising
sixth (c''-aes'') and a long falling scale that lands, on the last eighth of bar 2, on the German
sixth (ges-bes-e') and resolves bes'->a' (bar 3); then slow quarters rising (a'-bes'-c''-des''-ees''-f'')
in contrary motion to the lament, a 7th (des'' over ees) and the Phrygian close f''->e'' over des->c.
Checked alone with the answer (answer = bass: P02) and in the full triple complex (P03).

### A5. The triple complex (the "Grundgestalt" of the piece)

    S : CSb        c''4 des''8 ees''8 f''8 ees''8 des''8 c''8 | aes''4 g''8 f''8 ees''8 des''8 c''8 bes'8 | a'4 bes'4 c''4 des''4~ | des''4 ees''4 f''2 | e''2
    A : answer     f'2. f'8 e' | f'2. f'8 e' | f'4. g'8 g'4. bes'8 | bes'2. aes'8 f' | g'2
    T : CSa        bes2 a2 | aes2 g4. ges8 | f2 e2 | ees2 d4. des8 | c2

## B. Proof table

Checker = `tools/ck.sh` (project check.py with the four ranges). "0/0/0" = 0 PAR!, 0 BEAT, 0 DIS!.

| lab | claim | checker summary | dissonances to hear (all explained) |
|---|---|---|---|
| P01_S1_CSa.ly | S1 + CSa (lament) below it; answer context is the exact transposition | errors 0, parallels 0, beat-par 0, unjustified 0 | 2:3 accented passing c'; 2:4.5 aug-6th ces'/a' -> 8ve; 3:4.5 vii(o) over a (lament); 4:4 escape tone des'' over g |
| P02_answer_CSb.ly | answer + CSb as a duet (answer is the bass: 4ths count) | errors 0, parallels 0, beat-par 0, unjustified 0 | only passing tones and the answer's own e' neighbour |
| P03_answer_CSb_CSa.ly | triple complex CSb / answer / CSa | errors 0, parallels 0, beat-par 0, unjustified 0 | 1:1 c''/bes = elision note (replaced by des'' when the soprano is not coming off S1); 4:1 des'' 7th over ees (lament passing) |

## C. Architecture
(pending: meter 4/4, quarter = 76-84 with a tempo map; target ~72-76 bars)

## D. Risks
(pending)

## E. Inherited work from the interrupted session
- `lab/L01_exposition.ly` (4-voice exposition draft): checker 3 BEAT (13:4-14:1 S/T 8ve,
  15:4-16:1 S/T 8ve, 16:4-17:1 T/B 5th) and a CS1 whose last note is an unresolved accented 2nd
  (8:3 c''/bes'). Superseded by the new materials below; kept only as history.
- `lab/t_e2.ly` (answer + old CS1, 2 voices): clean (0/0/0) but uses the superseded CS1.
- `tools/p4.py` (pitch-exact transformations, lab writer, checker runner), `strict2.py` (strict
  two-voice evaluator used for ranking), `search_combo.py`, `combo_real.py`, `combo_rank.py`,
  `stretto.py`: kept and used.
