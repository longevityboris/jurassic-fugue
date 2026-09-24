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
| P04_stretto_chain_5ths.ly | stretto chain at the lower 5th, 2 bars apart, 3 voices: S1 b-flat (S), e-flat (A), a-flat (T) | errors 0, parallels 0, beat-par 0, unjustified 0 | only the followers' leading-tone neighbours (d, g) and the leader's escape tone |
| P05_CB1_S2_over_answer.ly | S1+S2 combination: S2 (soprano) over the real answer (alto), simultaneous, with a free bass | errors 0, parallels 0, beat-par 0, unjustified 0 | 3:1 V7 (ees'' over f, resolves to des''); 4:1 4-3 suspension bes'->aes' over f under S2's c'' |
| P06_apotheosis_frame.ly | B-flat major apotheosis, 4 voices, 10 bars: complete tune (S) over its mirror (B 1-4) and the answer (B 5-8), c'' -> d'', plagal minor-iv close | errors 0, parallels 0, beat-par 0, unjustified 0 | 3:3 V6/5 7th; 4:1, 7:1 V7; 8:1 ii4/2 (bass bes, is the 7th, resolves to a,); 10:1 minor iv6/4 neighbour chord |

## C. Architecture

### C1. Meter, tempo, duration

4/4 throughout (the tune's own metre; every entry keeps the tune's metric placement: dotted half on
beat 1, pickup eighths on beat 4). 70 bars.

| span | tempo | bars | seconds |
|---|---|---|---|
| Part I, bars 1-18 | Grave e sostenuto, quarter = 72 | 18 | 18 x 4 x 60/72 = 60.0 |
| Parts II-IV, bars 19-58 | Poco piu mosso, quarter = 80 | 40 | 40 x 4 x 60/80 = 120.0 |
| allargando 55-57 + fermata/general pause 58 | | | + 4.0 |
| Part V, bars 59-70 | Largamente, quarter = 66 | 12 | 12 x 4 x 60/66 = 43.6 |
| final ritardando + fermata | | | + 4.0 |
| **total** | | **70** | **231.6 s (3'52")** |

Slack: 210 s is reached even without the fermatas at a uniform quarter = 80; 240 s is not exceeded
unless Part V is taken below quarter = 60.

### C2. Form table

| bars | part | what happens | key | dynamics |
|---|---|---|---|---|
| 1-4 | I Esposizione | S1 alone, soprano | b-flat | p, dolce |
| 5-8 | | answer (alto) + CSb (soprano) = P02 | f / b-flat | p < |
| 9 | | codetta: C -> F7 -> i (link, 1 bar) | | mp |
| 10-13 | | S1 in the BASS (bes,), CSb in alto (subject form), soprano free descant (held notes, suspensions) | b-flat | mp |
| 14-17 | | answer in TENOR (f), CSa lament in bass (bes, -> c,), CSb in soprano, alto free = P03 + alto | f / b-flat | mf < f |
| 18 | | Phrygian half cadence on C (des -> c), the lament's goal | f: V | f > p |
| 19-22 | II Il conseguente | S2 (theme bars 5-8) enters, ALTO on g' (f-minor form), motor bass in eighths | f | p, poco piu mosso |
| 21-24 | | S2 stretto at the lower 4th: TENOR on d' (c-minor form), 2 bars after the alto | c | mp |
| 25-28 | | FIRST COMBINATION CB1 = P05: S2 (soprano, c'') over the answer (alto, f'); both halves of the tune at once | b-flat (on V) | mf |
| 29-32 | | episode: CSb head in sequence down by fifths, lament fragments in bass -> e-flat minor | -> e-flat | mf > p |
| 33-36 | III Inversio | S1 (alto, ees') with its MIRROR (tenor, ees) simultaneously, CSb above | e-flat | p subito, misterioso |
| 37-42 | | STRETTO CHAIN at the lower fifth, 2 bars apart = P04 transposed: S ees'' (e-flat), A aes' (a-flat), T des' (D-FLAT MAJOR: the tune's first, false, glimpse of major) | e-flat -> a-flat -> D-flat | p < f |
| 43-46 | | bass lament in half notes on the flat side: G-flat -> C-flat (NEAPOLITAN region) -> German sixth ges-bes-des-e | G-flat -> C-flat -> (b-flat: Ger6) | f > mp < |
| 47-54 | IV Pedale | ANSWER IN AUGMENTATION in the bass: F pedal 47-50 (f... f-e ...), rising f-g-bes 51-53, bes-aes-f 54. Above: S2 (soprano, c'') 47-50; lament CSa over the pedal (tenor: bes-a-aes-g-ges-f = sus4-3, then chromatic prolongation of V); S1 (soprano) 51-54 | b-flat: V | mf < ff |
| 55-57 | | CLIMAX: 55 German sixth fff (ges in bass); 56 V (F major) with the subject's head bes''-a'' in the soprano as the 4-3 suspension of the dominant; 57 DECEPTIVE cadence to G-flat (VI) | | fff, allargando |
| 58 | | general pause (fermata), then the lament's first two notes alone, pp | | pp |
| 59-68 | V Apoteosi | = P06: the COMPLETE TUNE in B-flat major as cantus firmus (soprano), over its own mirror (bass 59-62) and the answer (bass 63-66); c'' (the tune's open ending) rises to d'' (bar 67), the one note that separates minor from major | B-flat major | f, largamente, cantabile |
| 67-68 | | plagal close with the MINOR subdominant (ges) as the last shadow | B-flat | f > mp |
| 69-70 | | final B-flat major chord, d'' on top | B-flat | p < mf (fermata) |

### C3. Tonal plan and its logic

b-flat (i) -> f (v, the answer's key; exposition ends on its dominant C) -> Part II climbs the SHARP
side by S2's stretto at the lower 4th (f, c: tension) -> back to b-flat for the first combination ->
Part III falls the FLAT side by the stretto chain at the lower 5th (e-flat, a-flat, D-flat,
G-flat, C-flat = darkness, the Neapolitan region) -> the German sixth on G-flat pivots to the dominant
pedal (Part IV) -> climax on V, deceptive cadence to VI (G-flat, the last flat-side key) -> B-flat MAJOR.
The two strettos are mirror images of each other (up-by-fourths vs down-by-fifths), and the whole
piece balances sharp-side tension (II) against flat-side darkness (III) around the dominant.

### C4. Entry table

| bar | voice | form | key | first note |
|---|---|---|---|---|
| 1 | S | S1 | b-flat | bes' |
| 5 | A | answer (real) | f | f' |
| 10 | B | S1 | b-flat | bes, |
| 14 | T | answer | f | f |
| 19 | A | S2 (f-minor form) | f | g' |
| 21 | T | S2 stretto, lower 4th | c | d' |
| 25 | S + A | S2 + answer (CB1) | b-flat on V | c'' + f' |
| 33 | A + T | S1 + mirror (simultaneous, octave) | e-flat | ees' + ees |
| 37 | S | S1 (chain 1) | e-flat | ees'' |
| 39 | A | S1 (chain 2, lower 5th) | a-flat | aes' |
| 41 | T | S1 major form (chain 3, lower 5th) | D-flat | des' |
| 47 | B | answer in 2x augmentation (pedal) | b-flat: V | f, |
| 47 | S | S2 over the pedal | b-flat: V | c'' |
| 51 | S | S1 over the moving augmentation | b-flat | bes' |
| 59 | S | cantus firmus: complete tune (S1M + S2M) | B-flat | bes' |
| 59 | B | mirror of S1M (2 octaves below) | B-flat | bes, |
| 63 | B | answer (F major, real) | B-flat: V | f, |

### C5. Harmonic outline (per half bar; subject context numerals in b-flat unless noted)

- 1-4 (S1 alone, implied): i | i (V on a') | i ii(o) | iv | (V at 5)
- 5-8 (= P03 without bass: answer + CSb): i V6 | v6 vi(o)7->Ger6 | (f:) i V6 | iv IV6 -> iv6 | (f:) V
- 10-13 (bass S1, alto CSb, soprano descant): i (pedal) ... | VI6/4 - vii(o)7 | i - ii(o)6/5 - iv | iv - VI | V
- 14-17 (= P03 + alto): i V6 | v6 vi(o)7 - Ger6 | V(=f: I) V6/5 of f | iv of f (Eb/D) | f: Phrygian HC (des -> c) at 18
- 25-28 (= P05): V | V6 vii(o)7/V | V7 vii(o)7/V | v with 4-3 | (f: V) 
- 43-46: G-flat (VI) | C-flat (N, root position) | N6 (ees bass) | Ger6 (ges bass)
- 47-50: V pedal: V(sus4) V v V9 V(b9) V ... | (lament over the pedal)
- 55-58: Ger6 | V (4-3 = bes''-a'') | VI (deceptive) | fermata
- 59-68 (= P06, B-flat major): I | I (IV6/4 neighbour) | I V6 V6/5 V7 | V7 I6 | V (C7/E = V6/5 of V) | V | V7 vi | ii4/2 V6/5 V | I | iv6/4 (minor) I

### C6. Special harmonic events (where they sit and why)

- AUGMENTED SIXTHS built into the countersubject: every CSa cell ends with the lament's chromatic
  eighth forming an augmented sixth with the subject's leading-tone neighbour (2:4.5 of every entry
  that has CSa); the big German sixth returns structurally at 46 and 55.
- NEAPOLITAN: implicit in CSa (ces, bar 2 of the lament) and structural at 44-45 (C-flat region).
- DIMINISHED SEVENTHS: vii(o)7 of F under CSb's des'' (exposition bars 5-8 and 14-17: e-g-bes-des).
- LAMENT BASS: 14-17 (full chromatic descent bes, -> c,), 43-46, and over the dominant pedal 47-50.
- PEDAL POINTS: dominant pedal 47-50 that IS the subject (answer in augmentation); tonic pedal 59-60
  that is the subject's mirror.
- DECEPTIVE CADENCE: 57 (V -> VI, G-flat), the last flat-side sonority before the major.
- MODAL MIXTURE at the very end: minor iv (ges) in the plagal close, 68.
- THE LAST NOTE: the tune's open ending c'' rises to d'' (67): the one scale degree that the whole
  piece has been withholding (des in minor, d in major).

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
