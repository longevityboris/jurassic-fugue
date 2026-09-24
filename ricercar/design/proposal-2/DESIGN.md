# Proposal 2: "The Neighbour", a ricercar a 4 with a Beethoven arc on the Jurassic Park theme

B-flat minor to B-flat major, 4/4, 62 bars, about 230 s (measured with `tools/perform.py`).
Voices S A T B. All material, every combination and the whole 62-bar skeleton check clean
(0 PAR!, 0 BEAT, 0 DIS!) under `tools/check.py` with the instrument ranges enforced.

The skeleton `lab/L11_full_skeleton.ly` is a proof: every bar exists and has been checked. It is not the
final score. The composer should keep the architecture, the thematic lines and the harmony, and is free
to enrich free voices, change articulation and adjust voicing.

---------------------------------------------------------------------------------------------------

## 0. The idea

The subject opens with a lower neighbour: B-flat, A, B-flat (1, #7, 1). The whole piece is built from that
one gesture, at five scales:

1. **Motive.** The subject states the neighbour twice. The first B-flat is harmonised as a 4-3 over V, the
   second as a 7-6 over C, so the same two notes get two different meanings.
2. **Countersubjects.** CS1 is a chromatic lament: neighbour steps chained downward, D-flat C B-flat A
   A-flat G-flat F. It is the chromatic fourth of Bach's Thema Regium. CS2 is a motor built from the
   neighbour cell in diminution: rising in its bar 2, mirrored and falling in its bar 4.
3. **Inversion.** The tonal mirror turns the lower semitone B-flat/A into the upper semitone F/G-flat
   (5, b6, 5, the Phrygian sigh). The subject moves i to V (a question); its inversion moves V to i
   (the answer).
4. **Harmony.** At the Part I climax the neighbour is applied to a whole chord. Four entries of the
   subject's head sit on the four notes of E-G-B-flat-D-flat, and each slides down a semitone, so the
   diminished seventh on E melts into the diminished seventh on A.
5. **Tonal plan.** Part I is in B-flat minor. The inverted fugue is a semitone lower, in A minor (the
   large-scale "A"). The piece then returns through F (the subject's own final note) to B-flat, in
   MAJOR. The whole plan is B-flat, A, (F), B-flat: the subject's first bar, at the scale of the piece.

**Model.** The frame is Beethoven's Op. 110 finale: fugue, collapse, arioso dolente, inverted fugue
"poi a poi di nuovo vivente" a semitone away, then a radiant major close. The climax has the density of
the Hammerklavier fugue: the subject, the second subject and the inversion in augmentation sound at
once. The exposition has the gravity of Op. 131 No. 1: a single low voice, long values, no
accompaniment.

---------------------------------------------------------------------------------------------------

## 1. Materials (LilyPond `\absolute`, c' = middle C; B-flat minor unless stated)

### S1, Subject I = theme bars 1 to 5 beat 3, at the theme's own rhythm (19 beats)

    bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' | c''4. a'8 f'4

* No pitch or rhythm of the tune is changed. The only decision is where it ends. It runs on through the
  falling arpeggio C-A-F of theme bar 5 and closes on F (5) over the dominant, so it ends on a strong
  degree and never stops on the pickup notes D-flat/B-flat, which was the old piece's flaw.
* The last three beats (C-A-F) overlap the next entry. The subject cadences while the next voice
  enters. Entries therefore come every 4 bars with no codetta, and each entry's tail is written together
  with the others as one cadence.
* It keeps the real rhythm, not halved. The dotted halves give the other voices room to move.
* Harmonic skeleton, as supplied by the countersubjects:
  `V(4-3) | i ... vii°4/2 | i6  V  v  v7 | iv ... N(C-flat)  i6 | V`.

### ANS, the answer: real, at the fifth (F minor)

    f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f'' | g''4. e''8 c''4

The answer is real rather than tonal. The head is 1-#7-1 and the subject does not touch 5 until its last
note, so there is no 1-5 exchange to mutate. The answer's bars 3-4 (B-flat, A-flat) sit on the home
tonic, so it leans back toward B-flat minor by itself. The third entry (subject after answer) begins over
the answer's C-major tail: its B-flat is heard first as the 7th of C7, then as a 4-3 over F, and only
becomes the tonic at its second bar (bar 10).

### CS1, "Lament": enters on the subject's beat 4, 16 beats (tenor-register form against S1 on bes')

    r2. f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4 | a4. c'8 f4

* It opens with a rising sixth (a sigh), then descends chromatically: D-flat, C, B-flat, A, A-flat,
  G-flat, F.
* Against the subject it forms a 4-3 (bar 1) and a 7-6 (bar 2, which inverts to a 2-3), and elsewhere
  3rds and 6ths. It is consonant on every strong beat in both octave placements.
* Its tail swaps voices with the subject's tail: the subject has C-A, the lament A-C.
* Stretto form: in stretto the tail takes the minor dominant, `aes4. c'8 f4`.

### CS2, "Motor": enters on the subject's bar 2 (bass-register form)

    r1 | bes,8 a,8 bes,8 c8 des8 c8 ees8 ges,8 | des4 c8 f8 ~ f2 | ees8 f8 ees8 des8 ces4 des4 | f,2.

* Its rhythm complements the subject's. It moves in eighths where the subject holds (bars 2 and 4) and
  holds where the subject moves (bar 3), so the three lines never share a rhythm.
* Bar 2 is the neighbour cell in diminution, climbing. Bar 4 is its mirror, falling through the Phrygian
  tetrachord F E-flat D-flat C-flat B-flat. That puts a **Neapolitan (C-flat major)** under the
  subject's held E-flat (bar 12 beat 3).

S1, CS1 and CS2 are **triple invertible counterpoint at the octave**: all six vertical orderings pass the
checker (section 2).

### S2, Subject II = theme bars 5 to 8 (16 beats)

    c''4. a'8 f'4 des''8 bes' | c''2. f''8 bes' | ees''4. des''8 des''4. c''8 | c''1

S2 begins with S1's tail (C-A-F) and ends open on C, the 5th of V. That ending is the theme's own half
cadence, and it is used as such: S2 is the arioso melody (bars 30-33), a combining voice over the
dominant pedal (bars 42-45), and the second half of the theme in the apotheosis.

### INV, the inversion: tonal mirror (B-flat and F swap, C and E-flat, A and G-flat, A-flat and G; D-flat stays)

    f''2. f''8 ges''8 | f''2. f''8 ges''8 | f''4. ees''8 ees''4. c''8 | c''2. des''8 f''8 | ees''4. ges''8 bes''4

It starts on 5 and ends on 1, rising through iv to i: the subject's i-V question becomes V-i.
In A minor (Part III), transposed down a semitone: `e e f e | e e f e | e d d b | b c e | d f a`.

### INV-AUG, the inversion in augmentation, in the bass from F2 (38 beats, bars 42-51)

    f,1 | f,2 f,4 ges,4 | f,1 | f,2 f,4 ges,4 | f,2. ees,4 | ees,2. c,4 | c,1 | c,2 des,4 f,4 | ees,2. ges,4 | bes,2

In augmentation the inversion becomes the piece's dominant pedal. It gives four bars of F with G-flat
neighbours, then V4/2 (E-flat), then the lowest note of the piece (C2, the cello's open C) under the
climax, then D-flat and F, then iv-iv6 (E-flat, G-flat), and finally lands on B-flat exactly at the first
note of the apotheosis. The one line prepares the climax and cadences plagally into the major.

### The head, H (for the liquidation), and the other derived forms

* `x2. x8 (x-1)8` on E, G, B-flat and D-flat (bars 26-29).
* CS1 inverted, the lament rising (A minor, alto, bar 35): `r2. a'4 | c'2. d'4 | e'4 f'4 fis'2 | gis'2. a'4 | f'4. d'8 a'2`
* CS2 inverted (A minor, soprano, bar 36): `e''8 f''8 e''8 d''8 c''8 d''8 b'8 g''8 | c''4 d''8 a'8 ~ a'4 b'4 | b'8 a'8 b'8 c''8 d''4 c''4`

### Major forms (apotheosis)

* The whole theme, soprano, bars 51-58:
  `bes'2. bes'8 a'8 | bes'2. bes'8 a'8 | bes'4. c''8 c''4. ees''8 | ees''2. d''8 bes'8 | c''4. a'8 f'4 d''8 bes'8 | c''2. f''8 bes'8 | ees''4. d''8 d''4. c''8 | bes'1`
* The mirror under it, tenor, bars 51-55 (it keeps G-flat, the minor b6):
  `f2. f8 ges8 | f2. f8 ges8 | f4. ees8 ees4. c8 | c2. d8 f8 | ees4. ges8 bes4`
* The coda inversion, alto, bars 58-62 (major body, G-flat neighbours, G natural at the end):
  `f'2. f'8 ges'8 | f'2. f'8 ges'8 | f'4. ees'8 ees'4. c'8 | c'2. d'8 f'8 | ees'4. g'8 bes'4`
* The coda soprano, which follows the subject's contour in augmentation and ends on the major third:
  `bes'1 | bes'2. a'4 | bes'2 c''2 | c''2. bes'4 | c''2 d''2`

### Tune tweaks, all small, each justified

| where | change | why |
|---|---|---|
| everywhere | D-flat for D (minor mode) | decided in advance (THEME.md) |
| S1 boundary | the subject runs to theme bar 5 beat 3 | it ends on 5 over V with no pickup ending, and allows elided 4-bar entries |
| stretto, bars 24 and 26 | subject tails take the minor dominant (C-A-flat-F, F-D-flat-B-flat) | the next key is already sounding; as the music sinks, the dominants lose their leading tones |
| bar 48 (climax) | the tenor's subject tail C-A-F becomes C-A-B-flat | the subject breaks off into C7 (V7/V) at the climax |
| bar 58 | the theme's open ending (C, tied) closes on B-flat | the theme cadences on the tonic only once, at the arrival of the apotheosis |
| bars 51-55, 58-62 | the mirror keeps G-flat (minor b6) inside B-flat major | the minor is remembered inside the major, not erased |
| bar 34 | the arioso's final C is held over E (b6-5) | the Phrygian sigh that turns B-flat into A minor |

---------------------------------------------------------------------------------------------------

## 2. Proof table (every file: `sh lab/chk.sh FILE.ly` = tools/check.py with S 60-84, A 53-77, T 48-72, B 36-62)

Every row: **errors 0, parallels 0, beat-par 0, unjustified 0.** The last column explains each remaining
flag (D4?, DIR or MEL).

| lab file | claim proved | flags explained by ear |
|---|---|---|
| L02_exposition.ly | 4-voice exposition, bars 1-17: B S1; T ANS + B CS1; A S1 (over C7) + T CS1 + B CS2; S ANS + A CS1 + T CS2 + B free (tonic pedal, N6, cadential 6/4) | MEL 15:2.5 bass A-flat to E, a diminished 4th (saltus duriusculus, deliberate) |
| L03_perm_C1-S-C2.ly | CS1 above S1 (octave inversion), CS2 bass | none |
| L03_perm_C2-S-C1.ly | CS2 on top, S1 middle, CS1 as bass | D4? 5:2.5 in the tail: a passing 6/4 while the next entry starts |
| L03_perm_S-C2-C1.ly | S1 top, CS2 middle, CS1 bass | same tail 6/4 |
| L03_perm_C1-C2-S.ly | S1 as bass, CS1 top, CS2 middle | none (3:3 F over C is justified as a suspension) |
| L03_perm_C2-C1-S.ly | S1 as bass, CS2 top, CS1 middle | none |
| (L02 bars 9-13) | [S1, CS1, CS2], the sixth ordering | none, so **all 6 orderings pass: triple counterpoint** |
| L07_partI_episode_stretto_climax.ly | bars 17-29: episode; **stretto** bass S1 (b-flat) + soprano S1 (e-flat, 4th + 2 octaves above, 2 bars later) with CS1/CS2; **liquidation stretto** of the head at half-bar distances on a diminished 7th; climax | none |
| L08_partI_complete.ly | Part I joined, bars 1-29 (seam at 17) | the bar-15 diminished 4th only |
| L10_arioso.ly | bars 29-35: A°7 fermata; S2 arioso; **German-sixth pivot** B-flat to A minor | MEL 32:1 bass D to G-flat, a diminished 4th (lament figure) |
| L09_partIII_inversa.ly | bars 34-42: INV alone in the bass; **mirror trio** (INV + CS1 inverted + CS2 inverted = exposition entry 3 upside down); **INV stretto at the 5th above**, 2 bars; B7-C deceptive; seam into bar 42 | DIR 37:2.5, a hidden 5th inside the motor figure (weak 8th, soprano leap within the running line); D4? 42:4.5 = the alto's B-flat over the F pedal (sus4) |
| L04_partIV_pedal.ly | bars 42-51: **INV in augmentation** as the dominant pedal; S2 over it; **S1 + S2 combined** (bars 44-45: S2's sigh E-flat, D-flat, C over S1's B-flat, A in parallel 3rds, with the augmented inversion below: three thematic forms at once); soprano wedge to the V fermata | D4? 47:1 = A over E-flat inside V4/2 (a chord tritone) |
| L05_apotheosis.ly | bars 50-62: IV-iv6-I entry; **the whole theme in major over its own mirror** (S1-major + INV with the minor b6, starting together); final PAC; coda: INV over a tonic pedal, soprano on the major third | D4? 53:3 = E-flat over A inside V6/5 |
| L06_seam_IV_V.ly | Parts IV-V joined, bars 42-62 | the two chord tritones above |
| **L11_full_skeleton.ly** | **the whole piece, bars 1-62**, assembled from L08 + L10 + L09 + L06; also compiles in LilyPond 2.26 without warnings | 2 D4? (chord tritones), 1 DIR, 2 deliberate diminished-4th bass leaps; nothing else |
| L01_exposition.ly, t_*.ly | superseded drafts from the interrupted session (L01: codetta version, fixed and clean) | kept for reference |

Search aids, not proofs: `scan.py` (every interval and distance for two forms, run through the real
checker plus a cross-relation and quality score), `view.py`, `combo4.py` (thematic forms over a fixed
bass), `cs_search.py` (abandoned: the beam search produced trills), `mk.py` (lab writer),
`p2.py` (transforms: real transposition, tonal mirror, augmentation, LilyPond emitter).

Harmony x-ray of L11 (`tools/harmony.py`): 294 attacks, 51% chromatic to the local key, 138 distinct
harmony labels. For comparison, the old piece was mostly diatonic major triads.

---------------------------------------------------------------------------------------------------

## 3. Architecture

### Meter, tempo, duration

4/4 throughout. Measured duration: `tools/perform.py` with `perform/plan.json` on L11 gives **230.3 s**
(piano and strings targets alike). The window is 210-240.

| part | bars | tempo (quarter) | seconds (measured) |
|---|---|---|---|
| I Fuga (B-flat minor) | 1-29 | 74, slowing to 66 in bar 28, fermata 29 | about 99 |
| II Arioso dolente | 30-34 | 52 (1.4 s breath before) | 23.4 |
| III Fuga inversa (A minor to F) | 35-41 | 60 accelerating to 76 ("poi a poi di nuovo vivente") | 24.8 |
| IV Pedal, combination, climax | 42-50 | 76, slowing in 49; fermata 49:4; 0.7 s breath | 32 |
| V Apotheosis and coda (B-flat major) | 51-62 | 63, slowing to 54 from bar 60; final fermata | 51 |
| **total** | **62** | | **230.3** |

### Form table

| bars | section | content | key |
|---|---|---|---|
| 1-4 | Exposition, entry 1 | S1 alone in the bass (cello / piano LH), p sotto voce | b-flat |
| 5-8 | entry 2 | tenor ANS at f'; bass: S1 tail, then CS1 (lament bass) | f |
| 9-12 | entry 3 | alto S1 (head over C7 from the answer's tail); tenor CS1; bass CS2 (walking motor); N at 12:3 | b-flat |
| 13-17:3 | entry 4 | soprano ANS; alto CS1; tenor CS2; free bass: tonic pedal F, vii°6/5 (E°7 over G), N6 (16:3), cadential 6/4, V | f |
| 17:4-19 | Episode 1 | cell b (C-D-flat-D-flat-F) answered by its mirror (G-flat-F-F-E-flat, the inversion's bar 3, foreshadowed); bass fifths F-B-flat-E-flat-F | f to b-flat |
| 20-26:3 | **Stretto** | bass S1 (b-flat) 20; soprano S1 (e-flat), 2 bars later, a 4th + 2 octaves above, entering exactly where the bass subject's harmony reaches iv; alto CS1, tenor CS2; minor-dominant tails; 25:4 ii°7 to 26:1 i6/4 | b-flat to e-flat to b-flat |
| 26:3-28 | **Liquidation** | head H on E (bass 26:3), G (tenor 27:1), B-flat (alto 27:3), D-flat (soprano 28:1); each slides down a semitone: E°7 becomes A°7 (via E-flat major at 27:3, a glimpse of light, then E-flat minor) | b-flat |
| 29 | **Climax I** | A°7 over E-flat, ff, fermata, then general pause | b-flat |
| 30-33 | **Arioso dolente** | soprano S2 over pulsing eighths: V, i6/4, ii-half-dim 6/5, V6/iv (the one ray of D natural), iv6, V7 with b6-5, V7 | b-flat |
| 34 | Pivot | V7 of B-flat = German 6th of A minor; the soprano's C held over E (b6-5); E major | to a |
| 35-36 | **Fuga inversa** | INV alone in the bass from E (the Phrygian F-E sigh), pp; alto CS1 inverted (the lament rising C-D-E-F-F#-G#-A); soprano CS2 inverted | a |
| 37-39 | INV stretto | tenor INV in E minor a 5th above the bass, 2 bars later (the mirror of the subject's 4th-above stretto) | a to e |
| 40-41 | Transition | B7 (V7 of e), then deceptively C (VI of e, = V of F); crescendo, accelerando | e to F |
| 42-45 | **Pedal: S2** | INV-AUG enters on F2 (dominant pedal with G-flat neighbours = vii°4/2); alto S2, p misterioso | b-flat (V) |
| 44-48 | **S1 + S2 combined** | tenor S1 enters under S2 (44-45: three thematic forms at once) and continues over V4/2 (46:4) and C (47:4) | b-flat |
| 46-49 | **Climax II (main)** | soprano wedge F-G-flat-G-B-flat-A against the falling bass F-E-flat-C; 47:4 ii°7 (C2, the lowest note of the piece); 48:2.5 A°7/C; 48:3 **C7 (V7/V): E-flat becomes E, G-flat becomes G, "the light"**; 49:3 E°7 over D-flat; **49:4 V, fff, fermata**, soprano on a'' (leading tone) | b-flat |
| 50 | Subito pp | **IV (E-flat major, the first G natural of the ending), then iv6 (G-flat bass)**; tenor line G, G-flat, F (the lament's last three notes) | b-flat to B-flat |
| 51-58 | **Apotheosis** | soprano: the whole theme in B-flat major; tenor: its mirror (51-55) with G-flat, so each neighbour is V7b9 or vii°7 over the major tonic; bass: I-V, vi7, I6-V6/5, V7-I, V7-I6, ii6/5-V4/2 of IV, IV6-I6/4-V7, I | B-flat |
| 58-62 | Coda | tonic pedal; alto INV (major, G-flat neighbours, then G); soprano B-flat A B-flat C, C B-flat, C D; final IV(add6)/I6-4 to I, pp; last soprano note D, the major 3rd that replaced D-flat | B-flat |

### Tonal plan and its logic

`b-flat - f - b-flat - f | b-flat - e-flat - b-flat (dim7 slide) | b-flat (arioso) | = Ger6 -> a - e - (C) | F pedal = V of b-flat | B-flat major`

* **b-flat and f** (subject and answer) alternate at the fifth, as in any fugue.
* **e-flat** is the stretto follower's key and also the subject's own bar-4 harmony (iv). The stretto
  interval was chosen because the leader's harmony arrives at the follower's tonic just as it enters.
* **The dim7 slide** (26-29) moves the subject's neighbour motion into harmony. It ends on vii°7 of
  B-flat, which leads to the arioso's V.
* **A minor** is the large-scale lower neighbour. It is reached by the most classical enharmonic pivot
  there is: the V7 of B-flat (F A C E-flat) is the German sixth of A minor (F A C D#).
* **e and C** follow the inversion's natural stretto (a fifth up, mirroring the subject's fifth-down
  stretto). The deceptive B7-C turns E minor's VI into the dominant of F.
* **F** is the subject's own last note, the dominant of B-flat. The augmented inversion holds it as a
  pedal for nine bars.
* **B-flat major** comes in by a plagal step (IV-iv6-I) out of the V fermata. The leading tone A held at
  the top of the fermata resolves to B-flat after the silence. The piece's global motion B-flat, A,
  B-flat is its first three notes.

### Entry table

| bar:beat | voice | form | key | first note |
|---|---|---|---|---|
| 1:1 | B | S1 | b-flat | B-flat2 |
| 5:1 | T | ANS | f | F4 |
| 9:1 | A | S1 | b-flat | B-flat4 |
| 13:1 | S | ANS | f | F5 |
| 20:1 | B | S1 (stretto leader) | b-flat | B-flat2 |
| 22:1 | S | S1 (stretto, 4th + 2 octaves above, +2 bars) | e-flat | E-flat5 |
| 26:3 / 27:1 / 27:3 / 28:1 | B / T / A / S | head H (liquidation) | dim7 E-G-B-flat-D-flat to A-C-E-flat-G-flat | E2 / G3 / B-flat4 / D-flat5 |
| 30:1 | S | S2 (arioso) | b-flat | C5 |
| 35:1 | B | INV | a | E3 |
| 37:1 | T | INV (stretto, 5th above, +2 bars) | e | B3 |
| 42:1 | B | INV in augmentation (9.5 bars) | b-flat, dominant pedal | F2 |
| 42:1 | A | S2 | b-flat over V | C5 |
| 44:1 | T | S1 (combined with S2) | b-flat over V | B-flat3 |
| 51:1 | S | whole theme (S1 + S2) in major | B-flat | B-flat4 |
| 51:1 | T | INV (mirror, with G-flat) | B-flat | F3 |
| 58:1 | A | INV (coda, over the tonic pedal) | B-flat | F4 |

Countersubject placements: CS1 at 5:4 (B), 9:4 (T), 13:4 (A), 20:4 (A); CS2 at 10:1 (B), 14:1 (T), 21:1 (T).
Inverted CS1 at 35:4 (A); inverted CS2 at 36:1 (S).

### Harmonic outline (per half bar at entries, cadences and climaxes)

* 1-4: solo line, implying i | i (V at beat 4) | i-ii°-iv | iv-i6 | V.
* 5-8 (two voices, in f): V(4-3) | i6 ... 7-6 | i v6 v | iv6 ... i6/4 | V.
* 9-13: V7/V (the head B-flat as the 7th of C7) V | i (motor) vii°4/2 | i6 V v v7 | iv, N (12:3), i6 | V.
* 13-17: V | i over the tonic pedal, vii°6/5 | i6 V6 v v7 | iv6 N6 (16:3) cad 6/4 | V (C major).
* 18-19: i of f (= v of b-flat) | i | iv | V7 | 20: i.
* 20-26: the entry-3 plan over the bass S1; 23 iv = soprano entry; 24: VII6 v v7; 25: III (D-flat), VI6/4, ii°7 (25:4); 26:1 i6/4; 26:3 E°7.
* 26:3-29: E°7, E-flat 7, E-flat, E-flat minor, E-flat minor 7, A°7/E-flat (complete 28:4.5), fermata 29.
* 30-34: V i6/4 | ii-half-dim 6/5 V6/iv | iv6 V7(b6-5) | V7 | Ger+6 = V7, then E+ (C suspended), then E.
* 35-41 (a): V pedal E with the F neighbour | i6/4 ... | ii°6 V7 | V (B pedal from the tenor) ... | ii°6 i | B7 | C (VI of e) = V of F.
* 42-50: V pedal with vii°4/2 neighbours (43:4, 45:4) | 44 V7sus4, i6/4, V (the S1 + S2 bars) | 46 i6/4, V, V4/2 | 47 V4/2, ii°7(b9) | 48 ii°7, A°7/C, C7 | 49 C7, E°7/D-flat, **V (fermata)** | 50 IV, iv6.
* 51-58: I V7b9 | vi7 vii°7/E-flat | I6 V6/5 | V7 I | V7 V7b9 I6 | ii6/5 V4/2/IV | IV6 I6/4 V7 | **I** (PAC).
* 58-62 over the tonic pedal: I, V/I and vii°7/I neighbours, IV6/4, V7/I, ii7/I, I, IV(add6), I.

### Dynamics arc (encoded in `perform/plan.json`)

p (solo bass) to mp (bar 13) to mf (17) | mp (episode) to f (26) to **ff (29, fermata, general pause)** |
**subito pp** arioso (30), swelling to p in 31 and back | pp (35) to mf over Part III with the
accelerando | **subito p misterioso (42, the pedal enters)** to mp (44) to f (46) to **fff (49:4, V
fermata: the main climax)** | **subito pp (50, IV-iv6)** | p dolce (51) to mf (55) to **ff (57: the
theme's own climax, E-flat D D C)** | f (58, arrival) to pp (62, final fermata).

Three subito-piano moments (30, 42, 50) cut the three rising spans. The main climax (49) is in the last
third of the piece, and the release, the apotheosis, is earned by it.

### Special harmonic events and where they matter

* **Neapolitan**: C-flat major at 12:3 (under the subject's held E-flat), and N6 (G-flat/B-flat) at
  16:3 in f. It marks the subject's darkest bar each time it appears.
* **Diminished sevenths**: vii°4/2 at 10:4.5 and 14:4.5; the E°7 to A°7 slide at 26-29 (the Part I
  climax); A°7/C at 48:2.5 (the Part IV climax recalls the Part I chord); vii°4/2 neighbours at 43:4 and
  45:4; dim7 neighbours over the tonic in the apotheosis (52:4.5) and in the coda.
* **Augmented sixth**: the German sixth at 33-34 (enharmonic V7 of B-flat), the pivot of the whole plan.
* **Secondary dominants**: V7/V (C7) at 9:1-3 and at 48:3 (the moment of light); V6/iv (D natural) at
  31:4; V4/2 of IV at 56:4.
* **Deceptive and interrupted cadences**: 40-41 (B7 to C); 49:4-50 (V fermata to IV, subito pp).
* **Pedal points**: tonic pedal 14 (bass); dominant pedal 42-46 (INV-AUG); tonic pedal 58-62 (coda).
* **Lament bass figures**: CS1 as a bass (5-9); diminished-4th bass leaps (15:2.5, 32:1).
* **Plagal entries into the major**: IV-iv6-I (50-51) and IV(add6)-I (62).

---------------------------------------------------------------------------------------------------

## 4. How the old piece's five flaws are fixed

1. **Rushed subject that stopped mid-phrase.** The subject is at real rhythm (4.75 bars), ends on 5 over
   V and elides into the next entry. The first bar is not one static chord: it is a solo line, and every
   later statement of that bar is harmonised twice (4-3 over V, then 7-6 over C, or C7 then V).
2. **Filler countersubject, padding free voices.** CS1 is a chromatic lament with suspensions. CS2 is a
   rhythmic motor built from the head cell, complementary in rhythm. The free voices carry real lines: a
   lament bass, pedal lines, the wedge, the mirror.
3. **Diatonic harmony.** 51% of attacks are chromatic to the key (L11), with the Neapolitan, dim7 chains,
   the German sixth, V7b9, secondary dominants, deceptive cadences and pedal points.
4. **No devices beyond an octave stretto.** The piece has: triple invertible counterpoint (6 orderings);
   a stretto at the 4th/11th, 2 bars apart; an inversion stretto at the 5th; a head-motive stretto at
   half-bar distances on a dim7; a mirror of a whole 3-voice texture (rectus to inversus); the inversion
   in augmentation as a cantus firmus pedal; S1 + S2 + INV-AUG at once; the subject over its own mirror
   in the apotheosis; and the inversion over a tonic pedal in the coda.
5. **Block form, flat dynamics.** Five parts, two climaxes (29, 49), three subito-piano cuts, a tonal
   neighbour plan (B-flat, A, B-flat), and a major close reached only through the minor iv.

---------------------------------------------------------------------------------------------------

## 5. Idiom notes (piano and string quartet)

* All lines lie inside S 60-84, A 53-77, T 48-72, B 36-62 (the checker enforces this). The lowest note
  is C2 at 47:4-49:2 (cello open C, "sul C"). The highest is B-flat5 at 49 and 50 (vn I).
* Arioso (30-34): repeated eighths in A and T. Strings: pulsing, non tremolo, each eighth lightly
  separated. Piano: una corda, pedal each harmony (plan.json).
* Part IV: the augmented inversion is a sustained bass. Cello: long bows with no accent on the G-flat
  neighbours. Piano: the pedal re-caught on each bass note.
* Apotheosis: the melody is in the soprano at the theme's own register (B-flat4-F5). Voice the tenor's
  mirror audibly (a "cs" role in plan.json).
* **Keyboard spans.** The lower staff (T+B) is wider than a 9th in many bars: the tenor in the answer register
  over a low bass, and the tenor subject over the augmented bass in Part IV. In a printed piano score the
  tenor is taken by the right hand where the alto allows. MIDI sample rendering does not care. Upper-staff
  spans wider than a 9th occur in bars 13, 15-17, 24-25, 36, 39, 50 and 53-56.

---------------------------------------------------------------------------------------------------

## 6. Risks and open points

* **The exposition is long.** It is 17 bars, about 55 s, and it begins with 4.75 bars of a single bass
  line. This is intentional (Op. 131 No. 1) but depends on the performance: plan.json starts at quarter
  74, p sotto voce.
* **Pedal-point dissonance in thin textures.** At 43:4 the augmented bass steps to G-flat under the
  alto's F: a major seventh, one eighth long, in two voices plus pedal. The checker justifies it as a
  bass neighbour. It is audible, and meant to be.
* **G-flat inside the apotheosis.** The mirror voice keeps the minor b6 (bars 51-55, 58-60) on purpose.
  If it sounds like a wrong note in the render, use G natural in those neighbours. The major mirror then
  makes A against G (a major ninth) at the neighbour moments and must be re-proved; that version is not
  proved.
* **Part III is short** (7 bars). The A-minor "neighbour key" is a passage, not a pillar. Its weight comes
  from the German-sixth pivot and the silence before it, not from its length.
* **The liquidation passes through an E-flat major sonority at 27:3**, a by-product of the staggered
  slides. It is heard as a glimpse of light but could sound accidental. The composer can shade it with
  dynamics (it falls inside the crescendo).
* **Checker leniency.** The checker justifies many weak-eighth dissonances as passing, neighbour or
  anticipation notes. The scanner found at least one class it misses: cross relations such as E natural
  against E-flat in a subject/answer stretto. Every lab here was also read by grid for such clashes. The
  stretto intervals were chosen to avoid them, which is why the stretto is at the 4th/11th and not at the
  5th above.
* **Tails in stretto are modified** (minor-dominant tails; the C-A-B-flat break-off at 48). This is
  standard stretto practice, and each change is listed in the tweak table.
* **Two expressive diminished-4th bass leaps** (15:2.5 and 32:1) are flagged MEL by the checker and kept
  on purpose as lament figures.

## 7. Files

* `lab/L11_full_skeleton.ly`: the whole piece, 62 bars, 4 voices (the reference realisation).
* `lab/L02, L03_*, L04, L05, L06, L07, L08, L09, L10`: the individual proofs (table above).
* `perform/plan.json`: tempo map, fermatas, breaths, dynamics arc, voice roles and pedal for
  `tools/perform.py` (measured 230.3 s).
* `lab/p2.py, mk.py, scan.py, view.py, combo4.py`: tools (see section 2).
