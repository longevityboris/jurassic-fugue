# A. Musical meta-critique of *The Neighbour*, and what a masterwork recipe needs

Scope: the finished 66-bar ricercar (`ricercar/score/music-voices.ly`) set against the works it aims at
(Bach, Mozart, Beethoven, Liszt), then each gap traced to how we worked, then the tools and the recipe
that would raise the ceiling. All numbers below come from the finished score, measured by the
commands in "Evidence base". Bar:beat in 4/4.

## Verdict in one paragraph

*The Neighbour* is a correct, well-planned, conceptually unified piece. Its triple invertible
counterpoint is proven, the German-sixth pivot into A minor is well judged, and the idea of a neighbour
note working at five scales is a good one. It stays below Bach, Mozart and Beethoven for one main
reason: its intellect is mostly in the plan and in paper proofs, not in the unfolding line. The fugue
subject has almost no contrapuntal potential. The second subject is shown, never developed. The keys
are named in a table but never confirmed by cadences, so they are never really arrived at. There is
almost no development, only 2 bars of episode in 66. The stile-antico dissonance that should drive the
piece is missing from 53 of 66 bars, and the form is a chain of seven separately composed tableaux, each
building from soft. Almost all of this comes from our process: skeleton first, sections in parallel,
checkers that measure correctness, no ledger of motivic development, and no revision round by ear. None
of it comes from any lack of reasoning power in the model.

## Evidence base (reproducible)

| measurement | command | result |
|---|---|---|
| harmony x-ray | `python3 ricercar/tools/harmony.py ricercar/score/music-voices.ly --stats` | 360 attacks sampled; seventh-type 10%, dim7 3% |
| prepared suspensions | `python3 ricercar/design/final-lab/suspensions.py ricercar/score/music-voices.ly -v` | 18 strong-beat suspensions (in 13 distinct bars), 13 weak-beat |
| hollow and unison beats | `python3 ricercar/design/final-lab/grid.py ... --attacks` | 7 four-voice beats with at most 2 pitch classes (24:3, 38:1-2, 41:3, 43:4.5, 50:4.75, 66:1); 1 unison (5:3) |
| texture, rhythm, register per bar | ad-hoc script over `tools/lyparse.py` (not committed) | 741 attacks = 11.2 per bar (2.8 per voice); only 12 sixteenths, all in bars 50-53; composite rhythm fills 67% of eighth slots |
| cadences | ad-hoc scan: bass 5-1 with the leading tone sounding beforehand | three in the whole piece: 20:1 (D-flat), 41:4 (A minor, weak beat), 63:1 (B-flat major) |
| role coverage | piano `plan.json` roles over the score | free 34%, countersubjects 17%, S1/answer 19%, tune/cf 9%, rests 15% |

Attacks per bar by section: exposition 6.8, entry 4 and episode 13.6, stretto and Climax I 9.4, **arioso
20.8**, fuga inversa 13.1, **pedal and Climax II 9.9 (bars 46-49: 3, 6, 9, 9)**, apotheosis and coda 11.2.

## 1. The ten main shortfalls, with bar evidence and a better model

Each item gives the finding, the masterwork that solves the same problem better, and the process cause
(explained further in part 2).

### 1. The subject has little contrapuntal potential

**Finding.** S1 is the tune's first 19 beats, verbatim and in real time. It has 16 attacks. The first 8
beats are B-flat A B-flat twice, with the same dotted-half-plus-two-eighths rhythm. That rhythm fills 42
of the 227 voice-bars that have notes, 18.5% of the piece. Almost all of the subject's identity is in its
rhythm, not in its intervals. The consequences are measurable:
- proposal-4's own `stretto_ck.py` found no clean stretto closer than 2 bars. A 1-bar stretto works only
  at the lower 9th or 10th, and only if another voice supplies a bass.
- The inversion of a repeated-note head is still a repeated note. The critic's line "a mirror of a pedal
  is a pedal" holds for 61-62 ("answer against its mirror").
- The augmented inversion at 46-54 is heard as a held F: `f,1 | f,2 f,4 ges,4 | f,1 ...`.
- The Climax I heads at 26:3-28 are single repeated pitches, so the liquidation can only stack
  pitches. It cannot develop anything.

**Better models.**
- The Art of Fugue subject has 12 notes and outlines the triad, the leading tone and the scale. It
  supports stretto, inversion and mirror writing, and augmentation and diminution together (Contrapuncti
  5-7 and 12-13).
- The subject of the Op. 110 fugue is a chain of rising fourths, so stretto and inversion follow from it
  almost automatically.
- The pathotype subjects (the Thema Regium, K. 426) carry a diminished-seventh leap, which gives them
  harmonic tension of their own.
- Most relevant to us: Bach's chorale fugues (the Clavierübung III fughettas and the pre-imitation
  chorale preludes) compress and ornament the chorale line to make a fugue subject, then keep the
  untouched tune for a cantus firmus in long notes. We did the second half of that (the cantus at 55)
  but not the first.
- Liszt's thematic transformation in the B minor Sonata shows that a tune can be re-rhythmed and
  re-characterised and stay recognisable.

**Process cause.** The subject was fixed ("the tune untouched") before any search. Our search tools
(`proposal-4/tools/solve.py`, `search_combo.py`, `stretto.py`, `proposal-1/lab/search.py`) searched for
countersubjects and combinations to go with a given subject. Nothing searched for the subject itself or
scored candidate subjects on contrapuntal potential.

### 2. S2 is shown, never developed: "double fugue" is a label

**Finding.**
- S2 is stated three times: 30:1 (soprano), 48:1 (alto) and 59:1 (soprano, inside the tune). **All three
  start on the same c''.** S2 is never transposed, answered, inverted, put in stretto or used as a bass.
- Its combination with S1 (48-51) lasts 16 beats, over a pedal, with S1 in the tenor. That pair is never
  heard the other way up.
- The triple counterpoint has six proven orders, but only three are heard (9, 13, 55).
- Proposal-4 had worked out an S2 stretto at the lower fourth (`P10_S2_stretto_4th.ly`, clean). The
  synthesis dropped it.

**Better models.**
- Art of Fugue Contrapunctus 9: the new subject gets a full exposition before the main subject joins it
  in augmentation.
- WTC I C-sharp minor: each of three subjects enters and establishes itself before they are combined.
- St Anne (BWV 552/2): each section introduces a subject, then combines it with the first.
- Hammerklavier fugue: the late D-major cantabile subject gets its own entries before the combination.
- Jupiter finale: each of the five motifs is exposed and put through fugato or stretto on its own, and
  the coda rotates all five through the voices. Every voice carries every motif, so the combination is
  both heard and earned.

**Process cause.** The design stage was judged by a checklist of devices, which rewards having a
device, not a balanced treatment of each theme. Nothing tracked what each theme has done, as theme × form
× key × voice × device, so the gap never showed.

### 3. Keys are named, not confirmed by cadences

**Finding.** Only three bass motions in the whole piece go from the dominant root to the tonic root with
the leading tone sounding: 20:1 (into D-flat), 41:4 (A minor, weak beat) and 63:1 (B-flat major, at 92% of
the piece).
- **The home key, B-flat minor, gets no root-position authentic cadence in 54 bars.** It is asserted
  only by subject entries.
- A minor, the "large-scale lower neighbour" that carries the concept, is confirmed by inverted and
  plagal cadences only. The blueprint's own chain is "V6-vii dim-i at 44" and "iv-i at 45:3".
- The 45:3 "full cadence" in NOTES.md is plagal.
- The listener therefore does not hear B-flat, A, B-flat as three keys. Part of the concept exists only
  on paper.

**Better models.**
- Bach's fugues move their middle entries into new keys through episodes that end on the new tonic,
  as when WTC I C minor reaches the relative major and the minor dominant. Each key is confirmed
  before the next entry, so the listener hears the tonal plan instead of reading about it.
- Beethoven's Op. 131 makes a semitone neighbour key (D against C-sharp minor) audible across a whole
  work. The fugue subject's sforzando on A plants it, and the D-major second movement confirms it.
  That is the model for "the neighbour writ large".

**Process cause.**
- The tonal plan lived as a table of labels. `harmony.py` names chords, and nothing asked whether a key
  had been confirmed.
- The skeleton locked the entries, and cadences were left to the section composers inside FREE windows
  of a beat or two.
- The critique's "A minor is never established" was answered by adding cadence labels, not by
  measuring cadence strength.

### 4. The pivotal arrival (bars 54-55) is the weakest cadence in the piece

**Finding.** The nine-bar dominant (46-54) is the longest tension in the piece, and it resolves as
follows:
- 54:1 is V4/2 with the seventh, E-flat, in the bass. The E-flat moves up to G-flat instead of down to
  D.
- At 54:4 there is an A diminished seventh over G-flat.
- The bass then leaps G-flat to B-flat, so the flat sixth never falls to F.
- The E-flat reappears in the tenor and rises to F.
- The tune enters at p (piano plan level 3.2), in the middle register.

Neither tendency tone in the bass resolves at the one moment the whole plan points to. The real V7-I comes
eight bars later (63:1). The apotheosis is also registrally smaller than what came before. Its top note is
F5 (the tune's f'' at 60:4). Climax II reaches C6 (52:3) and the false dawn C-flat 6 (24-25). The
"transfiguration" sits a fifth below the climax that precedes it.

**Better models.**
- Op. 110: after the fugue inverted and the "poi a poi" revival, the return to A-flat is a
  long-prepared structural dominant. The end climbs to the widest register of the movement.
- Weinen, Klagen: the chorale arrives in plain diatonic major only after the lament ground is
  exhausted. It sounds as a structural downbeat.

**Process cause.** Section 6 and section 7 had different composers, and the hinge was one bar at the
boundary between them. The final check flagged "54 V4/2 seventh never resolves", but review round 2
was skipped. The register choice followed "tune at its own pitch" without a check on the whole-piece
register arc.

### 5. There is almost no development: 2 bars of episode in 66

**Finding.** The only episode is 18-19. The only other motivic working-out is the liquidation (26:3-28).
Everywhere else one entry follows another, so there is no fragmentation, sequence or recombination of
the cells.
- The neighbour cell is applied at five scales, but it is never developed: stated, fragmented,
  sequenced and recombined into something new.
- Free counterpoint is 34% of all voice-time. That is enough room for development, but it is spent on
  descants and fillers inside FREE windows.

**Better models.**
- WTC I C minor gives about a third of its 31 bars to episodes. Each is built from the subject head or
  the countersubjects, often in invertible counterpoint, and each carries the modulation.
- The Grosse Fuge and the Hammerklavier fugue build whole sections out of fragments: the trill, the
  leaping countersubject, the syncopations.

**Process cause.** Skeleton-first design turned the piece into a map of LOCKED thematic spans with
narrow FREE windows. The composers were told to "honour the blueprint exactly" (`wf_compose.js`), so no
one could open four bars for an episode. Proofs of combinations were the design currency. Developmental
trajectory had no currency at all.

### 6. The stile-antico dissonance is missing

**Finding.** There are 18 prepared strong-beat suspensions, but they fall in only 13 bars. There are
none in:
- bars 1-16 (the whole exposition and entry 4);
- bars 27-31 (Climax I and the start of the arioso);
- bars 33-42 (the pivot and most of the fuga inversa);
- bars 45-57 (Climax II, the hinge and the arrival of the tune).

53 of 66 bars have no strong-beat suspension. The harmony x-ray gives seventh-type sonorities 10% and
diminished sevenths 3%. The local harmonic events (Neapolitan, dim7 slide, German sixth) are good but
few, and the critic noted that the Neapolitan at 12:3 comes back at the same point of CS2 because the
counterpoint is built that way.

**Better models.**
- The Ricercar a 6 and WTC I C-sharp minor keep a chain of prepared dissonance going in nearly every
  bar, which is the expressive engine of stile antico.
- K. 426/546 gets its severity from dissonance within the subject and from chromatic stretto.

**Process cause.** `check.py` rewards consonance: "0 unjustified dissonances" is the gate, and it passes
any stepwise dissonance, so the safe move is to avoid dissonance. Nothing rewards dissonance density. The
suspension count was added late as a target (20) and missed (18). Free voices were written to pass the
checker, not to create tension.

### 7. Rhythm and metre stay fixed

**Finding.**
- The piece is in 4/4 throughout.
- Eighths make up 345 of 741 notes and quarters 138. There are only 12 sixteenths, all in 50-53.
- The two signature rhythms (dotted half + 8 + 8, and dotted quarter + eighth in pairs) dominate.
- The surface rhythm runs against the form. The inward arioso is the densest section (20.8 attacks per
  bar, repeated chords). The approach to Climax II (bars 46-49: 3, 6, 9, 9 attacks, 6.75 on average) is
  sparser than any other four-bar stretch after bar 8 except the Climax I fermata bars (26-29, 6.25).
- The composite rhythm leaves a third of the eighth slots empty.

**Better models.**
- St Anne recasts its first subject in a new metre in each section (4/2, 6/4, 12/8), which raises the
  tempo and changes the character with the same pitches.
- The Grosse Fuge previews its subject in several rhythmic guises in the Overtura and changes metre
  and tempo between its large sections.
- Art of Fugue Contrapuncti 2-7 change the subject's rhythmic profile (dotted, French overture,
  diminution in stretto).
- The fugue of Op. 110 moves into continuous sixteenth motion and speeds up "poi a poi".

**Process cause.**
- The rule "the subject's rhythm is untouched".
- A duration window of 210-240 s fixed the tempi.
- All tools assume one metre: `lyparse` takes a single `measure`, and `check.py`, `grid.py` and
  `perform.py` work on a fixed 4/4 grid.
- Neither a rhythmic-density curve nor a tension curve was ever computed against the intended arc.

### 8. The form is a chain of tableaux, and the climax gesture repeats

**Finding.**
- The piano plan drops to soft six times after a build: at 18, 24:3, 30 (pp after a general pause),
  35 (pp), 46 (level 2.3) and 55.
- The texture collapses at the seams: 26 to 27 goes from 10 attacks to 2, 34 to 35 from 19 to 4, and
  45 to 46 from 15 to 3.
- Both climaxes use the same gesture: a crescendo to a fermata on a dim7 or V, then silence or a
  breath, then subito soft.
- The seven sections are seven waves. By the second one the listener can predict the third.

**Better models.**
- In Op. 110 the collapse happens once, as a dramatic event (the return of the arioso, "ermattet,
  klagend"). The ten repeated G-major chords are the hinge, and the rest is one unbroken ascent.
- Bach's fugues accumulate: density and dissonance grow across the piece. They do not reset.

**Process cause.**
- Seven composers worked in parallel, one per section, each with boundary conditions at both seams.
- Every composer naturally shaped their own section as an arc. No one owned the long line.
- The join step fixed voice leading at the seams, not the drama across them.
- Review round 2, the only whole-piece pass, was skipped for time.

### 9. Devices were chosen because they could be proved, and some cannot be heard

**Finding.**
- "Answer against its mirror" (61-62) and "tune over its mirror" are true in the proofs but
  inaudible, because the heads are repeated notes.
- The "three speeds" at Climax II (50-53) are heard as a pedal (the augmentation), the tenor's S1, and
  4-note rhythmic tags in the soprano (`f''4. f''16 ees''16`).
- The augmentation is complete only on paper. NOTES.md presents all of these as devices "to listen
  for".

**Better models.**
- In the Jupiter coda each combined motif has its own rhythm (whole notes, dotted figure, scale in
  eighths, trill motif), so the ear can separate five lines.
- In the Art of Fugue the augmentation and diminution in Contrapunctus 7 are audible because the
  subject has intervallic profile at every speed.

**Process cause.**
- The design currency was provable devices: judges counted them, and `proofs.txt` listed them.
- No step asked whether a device is audible in the render, and no tool measured separability (rhythmic
  contrast, register gap, how much the entering line stands out).
- This problem comes from the same root as shortfall 1.

### 10. The performance plans do not use the analysis

**Finding.** The piano plan's roles cut entries short:
- the tenor's stretto leader is boosted 20:1-22:1, not to 24:4;
- the bass INV is boosted 35:1-37:1, although it runs to 39:3;
- the arioso's bass imitation (30:2) and the tenor's lament role are not marked, so they are not
  brought out.

Printed scores exist only for piano and quartet. The symphonic version cites Webern but changes colour
"at phrase joins".

**Better model.** Webern's orchestration of the Ricercar a 6 splits the Thema Regium across instruments
along its motivic segments. The colour is derived from an analysis of the subject.

**Process cause.** Roles in `plan.json` were written by hand from the skeleton's plan, then partly
edited by the performance agents. No analyser produced a voice × time role map and motif segmentation
for the renderers to consume.

**Also noted, lower priority:**
- 7 hollow four-voice beats remain.
- The coda holds d'' for 8 beats over a tonic pedal (63-64).
- `check.py` measures intervals in semitones, so spelled dissonances such as the augmented fifth D over
  G-flat can pass.

## 2. Process causes, consolidated

| process cause | shortfalls | how it did the damage |
|---|---|---|
| **Subject fixed before any search** ("tune untouched") | 1, 7, 9 | Every later device inherited a subject whose head is a repeated note. |
| **Skeleton-first, spans LOCKED, composers told "honour exactly"** | 3, 5, 6 | Development, cadences and dissonance live in the free material, and the free material was squeezed into beat-sized windows. |
| **Parallel composition by section** (7 composers) | 4, 8 | Seams were fixed for voice leading; long-range drama and the pivotal cadence had no owner. |
| **Checkers measure correctness, not quality** (0 PAR, 0 DIS, 0 clash) | 3, 6, 9 | They reward consonance and caution; no metric for cadence strength, dissonance density, development or audibility. |
| **No ledger of theme treatment or motivic development** | 2, 5 | S2 at one pitch three times went unnoticed through two critique rounds. |
| **Design judged by counting devices and proofs** | 2, 9 | Proofs are necessary but not sufficient. Six proven orders, three heard. |
| **One metre, one grid built into the tools** | 7 | Changing metre or rhythmic character would break every tool. |
| **No listening or revision loop; round 2 skipped** | 4, 8, 10 | Known defects (bar 54, suspensions 18/20, the performance role gaps) shipped. |
| **Performance plans written by hand** | 10 | Roles drift from the score. |
| **Budget spent on re-reading context** (97% of tokens were cache re-reads) | all | There was money for 155 agents but not for one more revision round. |

## 3. Process changes and new tools

Cognition tags:
- **DEEP**: creative or structural reasoning, frontier model, high effort.
- **GEN**: routine generation under tight constraints, a mid-tier or small model.
- **JUDGE**: bounded judgment, typed Choice/Score over a feature table, a Jev candidate, gated by
  confidence and escalated to DEEP when uncertain.
- **CODE**: deterministic.

The Jev assignments are hypotheses. The sibling probe `docs/kit/jev_probe.py` tests pairwise quality
choices, corruption detection and finding triage on this piece's own history. Its results should decide
which JUDGE rows go to Jev.

### 3.1 Tools

| # | tool | what it does | fixes | cognition | build (dev-days) |
|---|---|---|---|---|---|
| T1 | **subject-lab** | Generates candidate subjects from a source tune by diminution, ornamentation, choice of pitch skeleton, re-rhythming and head compression. Scores each for contrapuntal potential: clean strettos by interval × distance under the strict evaluator, invertibility at the 8ve, 10th and 12th, answer type, inversion quality, combinability with S2, harmonic implication, and recognisability of the tune (pitch-contour correlation). Reuses `stretto.py`, `solve.py` and `strict2.py`. | 1, 7, 9 | CODE for search and scoring; GEN for variants; JUDGE to rank the top 50 for character; DEEP to pick 1-3 | 3-4 |
| T2 | **theme ledger and motif tracker** | Finds every occurrence of each theme and cell (under transposition, inversion, augmentation and diminution, rhythmic variant, fragment) and prints a theme × form × key × voice × bar matrix and a motif-density curve. Flags themes stated at one pitch only, forms never used, and inverse pairs never heard. | 2, 5, 9, 10 | CODE | 3 |
| T3 | **cadence and key profiler** | Key-by-bar estimate (windowed key profiles plus a cadence detector: PAC, IAC, HC, plagal, deceptive, evaded), with a strength score for each cadence and a list of "key claimed but never confirmed". Also checks tendency tones at structural points (sevenths, leading tones, flat sixths at cadences and hinges). | 3, 4 | CODE | 2 |
| T4 | **tension and density profiler** | Per-beat curves: attack density, composite-rhythm fill, dissonance density (prepared and unprepared, by metric weight), harmonic rhythm, register span and top note, tonal distance from the tonic, and a composite tension index. Overlays them on the intended form curve from the design and reports inversions (for example "arioso denser than the climax approach") and repeated gestures. | 6, 7, 8 | CODE | 2 |
| T5 | **long-line and seam analyser** | Schenker-lite: extracts structural top voice and bass at cadences, section boundaries and metric peaks. Checks that the top voice descends or ascends coherently, that each voice's line runs across seams (no register jumps or dropped threads), and that texture changes at seams are intended, not accidental. | 4, 8 | CODE for extraction; DEEP to interpret | 3 |
| T6 | **audibility and separability check** | For each thematic entry and claimed device: rhythmic contrast against the other voices, register gap, onset alignment, and the level of the entering voice relative to the rest in the rendered stems. Produces a device list marked audible or paper-only. | 9, 10 | CODE; JUDGE for borderline cases | 2 |
| T7 | **listening loop** | Renders every revision to piano automatically, measures loudness (LUFS per bar), onset density and spectral centroid from the audio, and compares them with T4's intended curve. A human or audio-capable model checks only the moments T4 and T6 flag. | 4, 8, 10 | CODE; JUDGE; DEEP only on flagged bars | 2 |
| T8 | **quality metrics alongside correctness in the checker** | Keeps `check.py` and `strict.py` as gates, adds scored metrics (from T3, T4, T6) with target bands per section from the design, fixes the spelled-interval blind spot, and reports unisons (the critic asked for this). | 3, 6 | CODE | 1.5 |
| T9 | **analysis-driven performance plan** | Generates `plan.json` roles, boosts and motif segments (for Webern-style colour) from T2, and dynamics shapes from T4. Agents edit a derived plan instead of writing one. | 10 | CODE; GEN for the interpretation text | 2 |
| T10 | **metre and tempo-map support** | Mixed metres and tempo maps in `lyparse`, `check.py`, `grid.py`, `perform.py` and the renderers. | 7 | CODE | 2 |
| T11 | **combination finder, generalised** | Extends `solve.py` and `search_combo.py` to N-voice invertible combinations with rhythmic-contrast constraints (Jupiter style: every voice takes every motif) and to S2 stretto and inversion. | 2, 9 | CODE; JUDGE to rank | 2 |
| T12 | **suspension and dissonance planner** | Given a two-voice frame, proposes prepared-dissonance chains (7-6, 4-3, 9-8, 2-3) for free voices that hit per-section dissonance targets, and checks them with `suspensions.py`. | 6 | CODE for candidates; GEN to fill; JUDGE to rank | 1.5 |

Tool build total: about 25 dev-days of agent-assisted engineering. T1-T4 (about 10 days) raise the ceiling
the most.

### 3.2 Process changes

1. **Design the subject; do not inherit it.** The tune becomes the cantus firmus and the source of
   materials. The fugue subject is the best T1 candidate that still sounds like the tune. The untouched
   tune keeps its place at the apotheosis. That was the one part of our plan that worked like Bach.
2. **Design the drama and the lines before the proofs.** The design document starts with a tension
   curve (T4 format), a cadence plan with strengths (T3 format), a theme-treatment plan (T2 format: every
   theme gets exposition, transposition, inversion or stretto, and combination in at least two orders),
   and a structural two-voice line. Only then comes the search for proofs.
3. **Compose the frame first, not the sections.** One DEEP composer writes the outer-voice frame
   (soprano and bass, figured) for the whole piece in one pass, so the long line, the cadences and the
   pivotal hinge have one owner. Inner voices are then filled in parallel by section. That is the
   routine part, and it is where parallelism belongs.
4. **Unlock the free material.** Entries stay locked. Everything between entries is FREE with targets
   (development density, dissonance band, cadence required), and each section composer must plan at
   least one real episode where the design calls for one.
5. **Critics read the metrics first.** Every critic receives T2-T6 output before reading notes, so the
   deep critique is spent on judgment, not on counting.
6. **Two revision rounds are mandatory and budgeted.** The saving from shorter contexts (next point) pays
   for them.
7. **Keep contexts small.** Each agent gets the design summary plus its own section and the relevant
   metric tables. Nobody receives the full 778-line blueprint. With 97% of tokens spent on cache
   re-reads, this is the biggest cost lever.

## 4. A recipe for a masterwork-level piece, stage by stage

Cost ranges are rough estimates, in the same cost-weighted units as the run's own cost breakdown, for
a piece of this scale (about 4 minutes, 4 voices). They assume the tools in part 3 exist. The last run
cost 205M.

| stage | what happens | output | cognition | est. cost |
|---|---|---|---|---|
| 0. Brief | Source material, constraints, the work's model (Op. 110 arc, Jupiter combination, St Anne metres), duration, forces. | 1-page brief | DEEP (human + 1 agent) | 1M |
| 1. Material lab | T1 generates 200-2,000 candidate subjects and countersubjects and scores them. JUDGE ranks by character. DEEP picks S1, S2 and CS with reasons and proves the key combinations (T11: invertible orders, strettos, inversions, metre transformations). | `materials.ly` + potential report | CODE, GEN, JUDGE, DEEP | 8-12M |
| 2. Dramaturgy | Tension curve, cadence plan, theme-treatment plan, register arc, metre and tempo plan, climax strategy (one climax, or two contrasting in kind), audibility target for each device. Two competing designs, one judge. | design (about 200 lines, not 778) + target curves | DEEP | 10-15M |
| 3. Frame | One composer writes the outer-voice frame of the whole piece with figured harmony. Checked by T3 (cadences), T5 (long line) and T4 (curve fit). One revision. | `frame.ly` | DEEP + CODE | 8-12M |
| 4. Fill | Section agents write the inner voices and episodes against the frame, locked entries and free targets, using T12 for dissonance chains. `check.py`/`strict.py` gates plus T8 metrics per section. | sections | GEN for routine filling, DEEP for episodes and pivotal bars | 12-18M |
| 5. Whole-piece review x2 | Metrics first (T2-T6), then three critics (counterpoint, drama, audibility), then fixers, then re-measure. Round 2 is not optional. JUDGE triages findings by severity and routes them. | revised score | DEEP critics; JUDGE triage; GEN fixers for local fixes | 15-20M |
| 6. Listen | T7 renders piano, measures and flags; DEEP listens only at flagged bars; a final small round of fixes. | QA report | CODE, JUDGE, DEEP | 3-5M |
| 7. Perform and render | T9 derives plans from the analysis; version agents edit the derived plans; renderers; audio QA. | 5 versions | GEN, CODE, JUDGE for mix checks | 10-15M |
| 8. Documentation | Listener's guide generated from the ledger and the metrics, then edited. | NOTES.md | GEN + DEEP edit | 2M |
| **total** | | | | **about 70-100M**, versus 205M, with two review rounds this run skipped |

Where the savings come from:
- **Design stage:** 68M falls to about 20-27M, because deterministic search and scoring replace four
  full design proposals, each written and judged by agents.
- **Composing and review:** 38M falls to about 30M, even with the extra round, because contexts are
  smaller and critics start from metrics.
- **Rendering engines:** already built, so the kit reuses them (the 31M + 14M engine build is not
  repeated).
- **Coordination:** a scripted pipeline with checkpoints avoids the three usage-limit crashes.

Where not to economise: stages 1-3 and the critics in stage 5 need the frontier model at high effort.
That is where Bach-level quality is decided. Cheaper models and Jev belong only in the rows tagged GEN
and JUDGE.

## 5. Priorities if we revise *The Neighbour* itself (smaller scope than the kit)

1. Bar 54: resolve the hinge through a root-position V7-I, or make it a bVI-V-I, and put the tune's
   entry on the structural downbeat. About 1 bar of work, DEEP.
2. Give S2 one transposed and inverted statement (the S2 stretto at the lower fourth from proposal-4,
   clean), for example in the fuga inversa or in the pedal section. About 4-6 bars, DEEP.
3. Add a root-position authentic cadence in B-flat minor at 17-18 or 29, and a strong-beat perfect
   authentic cadence in A minor at 45. About 2 bars each.
4. Add prepared suspensions in the exposition's free voices (9-16) and in 46-49. Target at least 26.
   GEN with T12, checked.
5. Regenerate the performance roles from the score (T9).

---

Files referenced: `ricercar/score/music-voices.ly`, `ricercar/score/sections/*.ly`,
`ricercar/design/BLUEPRINT.md`, `ricercar/design/critique_r1.json`,
`ricercar/design/final-lab/{suspensions,grid,strict,splice_check}.py`,
`ricercar/design/proposal-4/{DESIGN.md,tools/stretto.py}`, `ricercar/tools/{check,harmony,lyparse}.py`,
`ricercar/tools/wf_compose.js`, `ricercar/performance/beethoven_piano/plan.json`.
