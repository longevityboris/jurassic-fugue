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
(pending: being rebuilt; see lab/ as proofs land)

## B. Proof table
(pending)

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
