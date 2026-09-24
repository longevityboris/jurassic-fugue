# Proposal 2 — "The Neighbour": a Beethoven-arc ricercar a 4 on the Jurassic Park theme

Status: SKELETON (work in progress; sections marked TODO are not yet verified).

## 0. Core idea

The subject opens with a lower neighbour: B-flat, A, B-flat (1, #7, 1). The whole piece is built
on that one gesture at every scale:

* in the subject itself (the neighbour, twice);
* in countersubject 1, a chromatic lament that descends from B-flat through A, A-flat, G, G-flat to F
  (homage to the chromatic fourth of Bach's Thema Regium);
* in the inversion, where the lower semitone B-flat/A becomes the upper semitone F/G-flat (5, b6, 5),
  the Phrygian sigh;
* in the tonal plan: Part I in B-flat minor, the inversion fugue in A minor (a semitone below: the
  large-scale "A"), then the return to B-flat, in MAJOR, as the large-scale resolution of the neighbour.

Model: Beethoven Op. 110 finale (fugue, collapse into an arioso, inverted fugue "poi a poi di nuovo
vivente" a semitone away, radiant major return), with the Op. 131 No. 1 gravity and Hammerklavier
density at the climax.

## 1. Materials (TODO: final versions)

Current verified draft (lab/L01_exposition.ly):

* S1 = theme bars 1-5 beat 3 at the theme's own rhythm, B-flat minor, 19 beats, ends on F (5) with the
  falling arpeggio C-A-F (a half cadence, so every entry ends on a strong degree):
  `bes'2. bes'8 a' | bes'2. bes'8 a' | bes'4. c''8 c''4. ees''8 | ees''2. des''8 bes' | c''4. a'8 f'4`
* Answer: real, at the fifth (F minor):
  `f''2. f''8 e'' | f''2. f''8 e'' | f''4. g''8 g''4. bes''8 | bes''2. aes''8 f'' | g''4. e''8 c''4`
  Justification: the head is 1-#7-1 and the subject does not touch 5 until its last note, so no
  tonal mutation is needed.

## 2. Proof table

| lab file | claim | checker summary |
|---|---|---|
| lab/L01_exposition.ly | 4-voice exposition draft, bars 1-18 (B, T, A, S) | errors 0, parallels 0, beat-par 0, unjustified 0 |
| lab/t_duo.ly | S1 + CS1 above... (draft) | errors 0, parallels 0, beat-par 0, unjustified 0 |
| lab/t_trio.ly | S1 + CS1 + lament bass (draft) | errors 0, parallels 0, beat-par 0, unjustified 0 |

Checker: `sh lab/chk.sh FILE.ly` (tools/check.py with the task's ranges: S 60-84, A 53-77,
T 48-72, B 36-62).

## 3. Architecture (TODO)

## 4. Risks (TODO)
