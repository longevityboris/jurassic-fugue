# Fugue on the Theme from Jurassic Park: analysis

Files: `fugue.ly` (score), `fugue.pdf`, `fugue.midi`, `check.py` (counterpoint checker).
The source targets LilyPond 2.24 syntax (`\version "2.24.0"`). It was compiled with LilyPond 2.26.0, which reported no warnings. It was not run through a 2.24 binary.

## Subject (alto, bars 1–2)
The subject is reference bars 1–4 at half their note values. Bars 1–2 of the reference become subject bar 1: the repeated tonic B♭ with the lower-neighbour A in a dotted-quarter + two-16ths rhythm. Bars 3–4 become subject bar 2: the rising B♭–C–C–E♭ and the fall E♭–D–B♭. No pitch had to change. Harmonically it implies I | I–ii–V4/2 (E♭ as the seventh)–I6/I, so it ends on the tonic with forward motion in the 16ths.

## Answer (soprano, bars 3–4; pedal, bars 8–9)
The answer is real, in F. The subject starts on the tonic and its head is 1–7–1. It never stresses the dominant early, so no tonal mutation is needed.

## Countersubject (first heard in the alto, bars 3–4)
It opens with an eighth rest, then moves in eighths and sixteenths against the held notes of subject bar 1. Against the dotted figures of bar 2 it has quarter notes, then sixteenths against the held E♭. Every strong beat is a 3rd, 6th or octave. Fifths occur only as weak passing notes, so it inverts cleanly at the octave. Below the subject it forms a 7–6 suspension (bar 3, beat 4); above it the same spot becomes a 2–3 bass suspension (bar 6, beat 4).
- Below the subject or answer: bars 3–4, 12–13, 20–21, 31–32.
- Above it: bars 6–7, 8–9, 16–17, 33–34, and the head alone in bar 26.

## Exposition (bars 1–9)
- Bars 1–2: alto, subject (tonic).
- Bars 3–4: soprano, answer (dominant).
- Bar 5: link, built from the theme's bar-7 cell E♭.–D D.–C in diminution; it returns from F to B♭.
- Bars 6–7: tenor, subject.
- Bars 8–9: pedal, answer. The exposition closes in F.

## Middle section (bars 10–25)
- **A, bars 10–11, Episode 1: circle of fifths** Gm–Cm–F7–B♭7–E♭ (bass G–C–F–B♭–E♭). The theme's bar-5 arpeggio cell (C–A–F | D–B♭) passes from soprano to tenor to tenor to alto. Bar 11 in the tenor uses the cell's own pitches. The soprano holds a prepared seventh, E♭ over F, and resolves it to D.
- **B, bars 12–13:** soprano subject in E♭ major, countersubject in the alto.
- **C, bars 14–15, Episode 2: chain of four 7–6 suspensions.** The soprano uses the theme's bar-7 rhythm (dotted quarter, eighth tied over) over the falling pedal F–E♭–D–C. Each suspension is prepared by a tie and resolves down a step. The alto uses the countersubject's sixteenth figure and the subject-head neighbour. The passage ends on D7/C, then G minor.
- **D, bars 16–17:** tenor subject in G minor (with F♯ as the neighbour), countersubject in the soprano.
- **E, bars 18–19, Episode 3: manuals only.** The pedal rests from bar 18 to 21. The soprano plays reference bars 5–8, halved and set in C minor, ending on a half cadence on G. The tenor becomes the bass, and its clef changes to bass clef.
- **F, bars 20–21:** alto subject in C minor on the manuals alone, countersubject in the tenor below.
- **G, bars 22–25, Episode 4: second circle of fifths.** The pedal returns on the full cycle F–B♭–E♭–A–D–G–C–F, one harmony per half bar.
  - Soprano: a model in the subject's bar-2 rhythm, one step lower each bar.
  - Alto: the subject-head neighbour, inverted, falling A–G–F–E♭.
  - Tenor: syncopated fifth-to-root half notes.
  - The passage ends on F7, preparing B♭.

## Stretto (H, bars 26–29)
- Entries: tenor on B♭3 (bar 26), soprano on B♭4 (bar 27), alto on B♭3 (bar 28), each one bar apart.
- **Why the octave:** entries a 4th or 5th apart were tested and rejected. The answer's E♮ collides with the subject's E♭ on the last sixteenth of beat 2, and the subdominant entry sounds the resolution against its own suspension. At the octave, the held tonic of each new entry is a prepared suspension against the previous entry's C (resolving to A), and all other strong-beat intervals are consonant.
- **Fit:** the soprano plays the countersubject head in bar 26 and then enters.

## Ending (bars 30–37)
- **I, bar 30:** the pedal descends B♭2–A–G–F–E♭–D–C, then E♮ as leading tone to F.
- **Bars 31–32:** dominant pedal on F2, subject in the soprano (tonic subject over V, so cadential 6/4 colour; its E♭ becomes the seventh of V7), countersubject in the alto.
- **J, bars 33–34:** final pedal entry on low B♭2, countersubject in the soprano. Its last B♭ is tied into bar 35 as the tonic pedal.
- **Bars 35–36:** tenor subject over the B♭2 pedal, which holds for bar 35 and the first half of bar 36. The cadential tail changes from E♭4.–D16–B♭16 to E♭2 | D1, so the seventh resolves on the last downbeat.
- **Bar 36, beat 3:** the pedal moves to F (V7).
- **Bar 37:** B♭, a perfect authentic cadence. Soprano C→B♭ (2̂→1̂), tenor E♭→D, alto A→F; final chord B♭2–D4–F4–B♭4.

## Checker status (`python3 check.py`)
- 0 parallel or antiparallel fifths/octaves, 0 successive-beat fifths/octaves, no voice out of range, all bar lengths correct.
- 5 remaining flags, all deliberate:
  - 16th-note anticipations at 10:2.75, 10:4.75 and 11:4.75.
  - A 6/4 over the dominant pedal at 32:4.75, resolved when the pedal moves.
  - A pedal-point ii over the tonic pedal at 36:2.
