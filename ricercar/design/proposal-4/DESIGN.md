# Proposal 4: "Ricercar sopra il canto fermo" (melodic-beauty / cantus-firmus design)

Status: design complete; 10 proof labs (P01-P10) all checker-clean. Everything in the proof table
has a lab file in `lab/` that was run through `tools/ck.sh` (= project checker with the four voice
ranges S 60-84, A 53-77, T 48-72, B 36-62). What is NOT proven is listed in section D.

## 0. Concept in one paragraph

The whole piece is built from the tune's two halves and the idea that the tune, sung whole and
unhurried, is the goal. Part I is a grave B-flat-minor fugue on the antecedent (theme bars 1-4 at
their real rhythm) with two countersubjects of fixed register: a chromatic lament below, a sighing
descant above. Part II adds the consequent (bars 5-8) as a second subject, drives it up the sharp
side in stretto, and proves that the two halves of one melody can be sung at the same time. Part III
sets the subject against its own mirror image, then presses it into a stretto chain down the flat
side (e-flat, a-flat, a false glimpse of D-flat major, the Neapolitan C-flat). Part IV is a dominant
pedal that IS the subject: the answer in augmentation in the bass (a held F with its E-natural
neighbour is exactly what the augmented answer sounds like), under the consequent, the lament and
finally the answer at the top of the range; the climax cadences deceptively. Part V is the
apotheosis: the complete tune in B-flat major, at its own tempo, as a cantus firmus in the soprano,
over its own mirror image (bass, first half) and the answer (bass, second half); the tune's open
ending c'' finally rises to d'', the one note that separates minor from major.

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
| P07_chain_flatward_Dflat_major.ly | Part III chain (bars 37-46): S1 e-flat (S), a-flat (A), then the MAJOR form in D-flat (T), each a fifth lower, 2 bars apart | errors 0, parallels 0, beat-par 0, unjustified 0 | leading-tone neighbours and escape tones only |
| P08_mirror_pair_Eflat.ly | S1 (alto, ees') and its diatonic mirror (bass, ees) simultaneously, two voices alone | errors 0, parallels 0, beat-par 0, unjustified 0 | 4:1 aes'/bes, = V7 of e-flat (7th held from 3:4.5, resolves) |
| P09_dominant_pedal_augmentation_climax.ly | answer in 2x augmentation (bass, 8 bars) under S2 (S), the lament (T) and the answer at the top (S, f'' -> bes''); climax It6 - V (4-3) - VI; general pause | errors 0, parallels 0, beat-par 0, unjustified 0 | pedal dissonances (sus4 at 1:1, V7 at 3:1, lament passing tones over f,); 9:1 augmented sixth ges,/e'; 10:1 bes''/f, 4-3 suspension |
| P10_S2_stretto_4th.ly | S2 (alto, g') and S2 at the lower 4th (tenor, d') 2 bars later | errors 0, parallels 0, beat-par 0, unjustified 0 | 3:3 aes'/g 9-8 suspension; 4:1 g'/d' 4th needs the bass below it (form table note) |

Search evidence (not proofs, kept for the composer): `tools/stretto_ck.py s1` lists every S1 stretto
the checker accepts (best: lower 12th/5th at +8 beats, strict 0/1; lower 5th +12; 1-bar stretto only
at the lower 10th/9th with 4ths that need a bass); `tools/stretto_ck.py inv` shows S1 with its mirror
is clean simultaneously at the octave, the lower 6th and the lower 12th; `tools/combo_ck.py minor`
shows S2 over the answer (CB1) and S2 over S1 at the lower 11th +8 beats are clean;
`tools/aug_pedal.py` lists the subject forms that sit cleanly over the augmented answer.

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
| 19-22 | II Il conseguente | S2 (theme bars 5-8) enters, ALTO on g' (f-minor form; continues the C chord of bar 18), free motor bass in eighths (not lab-proven) | f | p, poco piu mosso |
| 21-24 | | = P10: S2 stretto at the lower 4th: TENOR on d' (c-minor form), 2 bars after the alto; the bass must sit below the tenor at 22:1 (e.g. g or bes) because alto g'/tenor d' is a 4th | c | mp |
| 25-28 | | FIRST COMBINATION CB1 = P05: S2 (soprano, c'') over the answer (alto, f'); both halves of the tune at once | b-flat (on V) | mf |
| 29-32 | | episode: CSb head in sequence down by fifths, lament fragments in bass -> e-flat minor | -> e-flat | mf > p |
| 33-36 | III Inversio | = P08: S1 (alto, ees') with its diatonic MIRROR (bass, ees -> bes,) simultaneously, the two voices ALONE (CSb was tested above this pair and does not fit: PAR! + DIS!) | e-flat | p subito, misterioso |
| 37-42 | | STRETTO CHAIN at the lower fifth, 2 bars apart = P07 (P04 in b-flat is the same device): S ees'' (e-flat), A aes' (a-flat), T des' (D-FLAT MAJOR: the tune's first, false, glimpse of major) | e-flat -> a-flat -> D-flat | p < f |
| 43-46 | | episode (not lab-proven): bass lament in half notes on the flat side: G-flat -> C-flat (NEAPOLITAN region) -> German sixth ges-bes-des-e -> V at 47 | G-flat -> C-flat -> (b-flat: Ger6) | f > mp < |
| 47-54 | IV Pedale | = P09: ANSWER IN 2x AUGMENTATION in the bass: F pedal 47-50 (f... f-e ...), rising f-g-bes 51-53, bes-aes-f 54. Above: S2 (soprano, c'') 47-50 with a breath (c''2. r4) before 51; lament CSa over the pedal (tenor 47-50: bes-a-aes-g-ges-f = sus4-3, then chromatic prolongation of V); the ANSWER at the top (soprano f'' 51-54, peak bes'' at 53-54); alto to be composed | b-flat: V | mf < ff |
| 55-57 | | CLIMAX (= P09 bars 9-11): 55 ITALIAN sixth fff (ges, e' bes' bes''); 56 V (f, f' c'' bes''->a'': the subject's head as the 4-3 suspension of the dominant); 57 DECEPTIVE cadence to G-flat (ges, des' bes' bes''). An Italian, not German, sixth here because Ger6 -> V puts parallel fifths between bass and the fifth of the chord | | fff, allargando |
| 58 | | general pause (fermata), then the lament's first two notes alone, pp | | pp |
| 59-68 | V Apoteosi | = P06 (its bars 1-10): the COMPLETE TUNE in B-flat major as cantus firmus at its own tempo (soprano 59-66), over its own mirror (bass 59-62; the mirror's last pickup g,-bes, is replaced by d, to avoid fifths on successive beats) and the answer in F major (bass 63-66); 66 V (ii4/2 - V6/5 - V); 67 the tune's open ending c'' rises to d'' over I; 68 plagal shadow: minor iv6/4 (ges'/ees') -> I | B-flat major | f, largamente, cantabile; 68 mp |
| 69-70 | | final B-flat major chord held, d'' on top | B-flat | p < mf (fermata) |

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
| 33 | A + B | S1 + mirror (simultaneous, octave) | e-flat | ees' + ees |
| 37 | S | S1 (chain 1) | e-flat | ees'' |
| 39 | A | S1 (chain 2, lower 5th) | a-flat | aes' |
| 41 | T | S1 major form (chain 3, lower 5th) | D-flat | des' |
| 47 | B | answer in 2x augmentation (pedal) | b-flat: V | f, |
| 47 | S | S2 over the pedal | b-flat: V | c'' |
| 51 | S | answer over the moving augmentation (peak bes'') | f / b-flat | f'' |
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
- 47-50 (= P09): V pedal: Vsus4 -> V (47) | v6-ish (aes over f) - vii(o)7/V - It6 colour over the pedal (48) | V V(maj7 passing e) (49) | V7 (ees) - V(b9: des) (50)
- 51-54 (= P09): V (f'' over f,) - vi(o)7 (g,) | i (bes,) | i - IV6/4 (g'' over bes,) - i | i - VII (aes,) - V (f,)
- 55-58: It6 | V (4-3 = bes''-a'') | VI (deceptive) | general pause
- 59-68 (= P06, B-flat major): I | I (IV6/4 neighbour) | I V6 V6/5 V7 | V7 I6 | V (C7/E = V6/5 of V) | V | V7 vi | ii4/2 V6/5 V | I | iv6/4 (minor) I

### C6. Special harmonic events (where they sit and why)

- AUGMENTED SIXTHS built into the countersubject: every CSa cell ends with the lament's chromatic
  eighth forming an augmented sixth with the subject's leading-tone neighbour (2:4.5 of every entry
  that has CSa); the German sixth returns structurally at 46 (episode into the pedal) and as an
  ITALIAN sixth at the climax, 55 (P09).
- NEAPOLITAN: implicit in CSa (ces, bar 2 of the lament) and structural at 44-45 (C-flat region).
- DIMINISHED SEVENTHS: vii(o)7 of F under CSb's des'' (exposition bars 5-8 and 14-17: e-g-bes-des).
- LAMENT BASS: 14-17 (full chromatic descent bes, -> c,), 43-46, and over the dominant pedal 47-50.
- PEDAL POINTS: dominant pedal 47-50 that IS the subject (answer in 2x augmentation, P09); tonic pedal
  59-60 that is the subject's mirror (at tempo, P06).
- DECEPTIVE CADENCE: 57 (V -> VI, G-flat), the last flat-side sonority before the major.
- MODAL MIXTURE at the very end: minor iv (ges) in the plagal close, 68.
- THE LAST NOTE: the tune's open ending c'' rises to d'' (67): the one scale degree that the whole
  piece has been withholding (des in minor, d in major).

## D. Risks and what is NOT proven

1. The checker is permissive (any attacked note left by step counts as "APP", any held note that
   later steps down counts as "SUS"). Every strong-beat dissonance in P01-P10 was read and explained
   in the proof table, but a clean summary line is not a guarantee of taste. Pedal passages (P09
   47-50, P06 59-60) rely on the pedal-point licence (upper voices consonant among themselves).
2. Fixed registral roles instead of invertible counterpoint: CSa must stay BELOW the subject and CSb
   ABOVE it (the subject's first two bars are a pedal, so a fifth under it becomes a fourth when
   inverted). Consequences: exposition order S-A-B-T is forced by the elision (the answer must enter
   below the voice ending on c''), and the bass entry at 10 has only CSb (alto) above it. Anyone
   re-ordering entries must re-check.
3. Elision at the start of CSb: the first quarter c'' is the end of the preceding S1. Where the
   soprano is not coming off S1 (bar 14) it must start des'' instead (P03 1:1 shows c''/bes as an
   appoggiatura against the lament).
4. Free voices not lab-proven (to be composed and checked by the composer): the soprano descant
   10-13 and the alto 14-17 in the exposition (the combinations under them are proven pairwise and
   as the triple complex P03, by exact transposition); the codetta bar 9; the motor bass 19-24
   (no motor countersubject survived: the solver's candidates were stepwise but harmonically aimless
   and cross-related with S2's a-natural, and CSb does not fit against S2); the episodes 29-32 and
   43-46; the upper voice(s) over the mirror pair 33-36 (CSb tested there: fails); the alto 47-54 in
   P09 (it must avoid e/f octaves with the augmented bass's e,-f, neighbour notes); the inner voices of
   P06 are free lines (the lament tried as the tenor there gave 2 BEAT against the mirror bass), so
   "other voices weave the subjects" in the apotheosis is true for the bass (mirror, answer) and not
   for the inner voices.
5. Part II states S2 three times in 10 bars (alto 19, tenor 21, soprano 25). Moving S2 below the
   answer in 25-28 is not an option (CB1 is only proven with S2 above). If the third S2 feels
   redundant, cut the episode 29-32 to 2 bars rather than dropping the combination (the budget has
   about 20 s of slack above 210 s).
6. Range and idiom: the bass lament in answer context descends to c, (C2 = cello open C; piano fine);
   the tenor at c (48) is the viola's lowest note; the soprano peak bes'' (53-56) is high for a sung
   line but ordinary for violin I and piano. Left-hand span at 14-17 (tenor f-bes over bass bes,-c,)
   is up to 2 octaves: fine on cello/viola, needs the tenor taken by the right hand on piano.
7. D-flat MAJOR at 41 uses the major form of S1 in the middle of flat-side minor keys; it is meant
   as a false dawn. If it sounds too bright, the tenor can take the minor form (des'-ces'-... with
   fes), at the cost of an ugly spelling.
8. Tempo: 231.6 s assumes quarter = 72 / 80 / 66. The tune's recognisability depends on not taking
   the apotheosis slower than about quarter = 60 (below that the dotted halves lose the tune).

## E. Inherited work from the interrupted session
- `lab/L01_exposition.ly` (4-voice exposition draft): checker 3 BEAT (13:4-14:1 S/T 8ve,
  15:4-16:1 S/T 8ve, 16:4-17:1 T/B 5th) and a CS1 whose last note is an unresolved accented 2nd
  (8:3 c''/bes'). Superseded by the new materials below; kept only as history.
- `lab/t_e2.ly` (answer + old CS1, 2 voices): clean (0/0/0) but uses the superseded CS1.
- `tools/p4.py` (pitch-exact transformations, lab writer, checker runner), `strict2.py` (strict
  two-voice evaluator used for ranking), `search_combo.py`, `combo_real.py`, `combo_rank.py`,
  `stretto.py`: kept and used.
