# Proposal 2 — "The Neighbour": a Beethoven-arc ricercar a 4 on the Jurassic Park theme

Status: IN PROGRESS. Sections 1 and 2 (materials, exposition, triple counterpoint) are verified.
Sections still marked TODO are not yet proven.

## 0. Core idea

The subject opens with a lower neighbour: B-flat, A, B-flat (1, #7, 1). The piece is built on that one
gesture at every scale:

* in the subject (the neighbour, twice, the second time harmonised differently);
* in countersubject 1, a chromatic lament (D-flat, C, B-flat, A, A-flat ... G-flat, F), homage to the
  chromatic fourth of Bach's Thema Regium;
* in countersubject 2, a motor of eighths whose cells are the neighbour figure (bar 2, rising) and
  its mirror (bar 4, falling);
* in the inversion, where the lower semitone B-flat/A becomes the upper semitone F/G-flat (5, b6, 5);
* in the tonal plan: Part I in B-flat minor, the inversion fugue a semitone lower in A minor (the
  large-scale "A"), and the return to B-flat, in MAJOR, as the large-scale resolution of the neighbour.

Model: Beethoven Op. 110 finale (fugue, collapse into an arioso, inverted fugue "poi a poi di nuovo
vivente" a semitone away, radiant major return), with the gravity of Op. 131 No. 1 and the density of
the Hammerklavier at the climax.

## 1. Materials (B-flat minor, LilyPond \absolute, c' = middle C)

### Subject I (S1) = theme bars 1-5.3 at the theme's own rhythm (19 beats)

    bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' | c''4. a'8 f'4

* No pitch or rhythm of the tune is changed. The only decision is where it stops: it runs on through
  the falling arpeggio C-A-F of theme bar 5 and ends on F (5) over the dominant. It never stops on the
  pickup notes D-flat/B-flat (the old piece's flaw). The last three beats (C-A-F) overlap the next
  entry: the subject cadences while the next voice enters, so entries follow every 4 bars with no
  codetta.
* Real rhythm, not halved: the long notes (dotted halves) are what give the counterpoint room.
* Harmonic skeleton designed into the countersubjects (bass of the three-voice form):
  `V (4-3 on the subject's B-flat/A) | i ... vii°4/2 | i6  V  v  v7 | iv ... N  i6 | V`.
  The repeated B-flat is heard first as a 4-3 suspension over V (bar 1 beat 4), then as a 7-6
  suspension over C (bar 2 beat 4): the same two notes, re-harmonised.

### Answer (ANS): real, at the fifth (F minor)

    f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f'' | g''4. e''8 c''4

Justification: the head is 1-#7-1 and the subject does not touch 5 until its final note, so there is
no 1-5 exchange to mutate. The answer's subdominant region (bars 3-4: B-flat, A-flat) is the home
tonic, so the answer leans back toward B-flat minor by itself.

### Countersubject 1 (CS1), "Lament": starts on the subject's beat 4, 16 beats, B-flat-minor form

    r2. f4 | des'2. c'4 | bes4 a4 aes2 | ges2. f4 | a4. c'8 f4

* A chromatic descent D-flat, C, B-flat, A, A-flat, G-flat, F in half and quarter notes: the
  Thema Regium chromatic fourth. It enters with a rising sixth (a sigh) and ends with a voice
  exchange against the subject's tail (C-A becomes A-C).
* Against the subject: 4-3 (bar 1), 7-6 (bar 2, inverts to 2-3), then 3rds and 6ths, all strong
  beats consonant in both octave placements.

### Countersubject 2 (CS2), "Motor": starts on the subject's bar 2, B-flat-minor form (bass register)

    r1 | bes,8 a,8 bes,8 c8 des8 c8 ees8 ges,8 | des4 c8 f8 ~ f2 | ees8 f8 ees8 des8 ces4 des4 | f,2.

* Eighths exactly where the subject holds (bars 2 and 4) and a held note where the subject moves
  (bar 3): rhythmic complementarity, so the three lines never move in the same rhythm.
* Bar 2 is the neighbour cell (B-flat A B-flat) in diminution, climbing; bar 4 is its mirror
  (E-flat F E-flat) falling through the Phrygian tetrachord F E-flat D-flat C-flat B-flat, which
  puts the Neapolitan (C-flat major, bar 4 beat 3) under the subject's held E-flat.

### Chain

Each voice runs subject/answer (19 beats) -> CS1 (from beat 4 of the next entry) -> CS2 (from bar 2
of the entry after) -> free. The subject's tail, CS1's tail and CS2's tail all fall in the first three
beats of the next entry and are written as one cadence onto the new key.

## 2. Proof table

Checker: `sh lab/chk.sh FILE.ly` (tools/check.py with the task's ranges: S 60-84, A 53-77, T 48-72,
B 36-62). Every file below: errors 0, parallels 0, beat-par 0, unjustified 0.

| lab file | claim | notes |
|---|---|---|
| lab/L02_exposition.ly | 4-voice exposition, bars 1-17: B S1, T ANS + B CS1, A S1 + T CS1 + B CS2, S ANS + A CS1 + T CS2 + B free | one justified P4 (16:4.5 cadential 6/4); one expressive diminished-4th leap in the free bass (15:2.5, A-flat to E, saltus duriusculus) |
| lab/L03_perm_C1-S-C2.ly | triple counterpoint, CS1 above S1 (octave inversion), CS2 bass | clean |
| lab/L03_perm_C2-S-C1.ly | CS2 on top (2 octaves up), S1 middle, CS1 as bass | one D4? in the tail (5:2.5, passing 6/4 while the next entry starts) |
| lab/L03_perm_S-C2-C1.ly | S1 top, CS2 middle, CS1 as bass | one D4? in the tail (same spot) |
| lab/L03_perm_C1-C2-S.ly | S1 as bass, CS1 top, CS2 middle | 3:3 F over C is a 6/4 held from the offbeat; acceptable, or re-touch CS2 bar 3 locally |
| lab/L03_perm_C2-C1-S.ly | S1 as bass, CS2 top, CS1 middle | same 6/4 at 3:3 |
| lab/L01_exposition.ly | superseded first draft (codetta version) | clean, kept for reference |

Entry 3 of L02 is the sixth permutation [S1, CS1, CS2], so all six orderings of S1/CS1/CS2 pass:
triple invertible counterpoint at the octave.

## 3. Architecture (TODO)

## 4. Risks (TODO)
