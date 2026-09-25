# Plan: a composition kit for masterwork-level music at a fraction of the cost

Sources: four research reports in this folder, written 2026-09-25 from the finished *Neighbour* and its run logs.
[A](A_musical_metacritique.md) is the musical meta-critique, [B](B_process_and_model_tiers.md) the process, cost and model-tier audit, [C](C_packaging_architecture.md) the packaging design, [D](D_jev_probe.md) a live Jev test on 672 labelled decisions from this project.

## 1. What we learned

**The limit was the process, not the model's musicianship.** The ideas were real but lived in the plan and the proofs more than in the sound (A):

| Shortfall in *The Neighbour* | Process cause |
|---|---|
| The subject is the tune verbatim; its head is a repeated note, so strettos closer than 2 bars fail and inversion/augmentation turn into pedals | Subject inherited, never searched for contrapuntal potential |
| S2 heard 3 times at one pitch, never answered, inverted or put in stretto: "double fugue" was a label | No ledger of how each theme is treated |
| Keys named but rarely confirmed: 3 root-position authentic cadences in 66 bars, none in B-flat minor for 54 bars; A minor only plagal | Checkers measure correctness, not cadence strength or key |
| Bar 54, the pivot into the apotheosis, is the weakest cadence (V4/2 seventh never resolves) | Parallel section composers; nobody owned the long line |
| 2 bars of episode in 66; 53 of 66 bars without a strong suspension; one metre, few sixteenths | Skeleton-first with locked spans squeezed the free material |
| Two climaxes use the same gesture; the arioso is denser than the climax approach | No tension or density profile against the intended arc |
| Some proven devices cannot be heard; performance plans ignore parts of the analysis | Devices chosen because provable; plans written by hand |

**Cost was driven by long agents re-reading big contexts, not by which model ran** (B, C). Ricercar total: about 205M cost-weighted tokens, roughly $730 at list price, 21 hours. About a third was building sound engines that now exist. Agents running 60-116 minutes cost $15-23 each; 10-25 minute agents cost $2-6. Moving roles from Opus to Sonnet or Haiku saves under $10 a piece; giving each agent a short brief instead of the whole blueprint saves far more.

**Jev is a cheap dispatcher, not a musician** (D, measured: $0.02 for 672 decisions, 0.6 s median):
- judging which of two passages is better: 0.47-0.56 (chance); spotting injected errors: AUC 0.54 (check.py already catches 100%);
- routing a review finding to notes vs performance: 0.86, and 0.90 when confident; its "minor" calls are right 36 of 37 times;
- ranking whole designs: only good enough to drop a clear loser.

## 2. The kit

**Package:** one Python CLI (working name `kapell`) with an `agent-info` manifest like `suno` and `akm`, plus one installed skill (the method, five reference files) and five workflow recipes with a `tiers.json`. No MCP server now; checkers run in 0.1-0.3 s and the samples are local. An MCP adapter can be generated from the manifest later if Claude Desktop or a remote session needs it (C).

**Commands** (C §3): `new` (project from a brief) · `find` (subjects, countersubjects, invertibility, stretto, combinations) · `prove` · `check` / `xray` (all checkers + quality metrics in one short JSON) · `splice` / `assemble` · `engrave --layout all` · `perform` · `render --version organ|piano|quartet|orchestra|ensemble` · `qa` · `jev route|park` · `status` (resume point after a usage-limit kill, under 2k tokens).

**New musical tools** (A §3), in order of value:

| Tool | Raises the ceiling by | Cognition |
|---|---|---|
| T1 subject-lab: generate hundreds of subject variants from a source tune and score their contrapuntal potential (stretto table, invertibility at 8ve/10th/12th, inversion, combinability, recognisability) | a subject designed like Bach's, not inherited | code search; Opus picks |
| T2 theme ledger: every occurrence of each theme and cell, by form, key and voice | no theme left undeveloped | code |
| T3 cadence and key profiler, with tendency-tone checks at hinges | keys confirmed, bar-54 errors caught | code |
| T4 tension and density profiler against the intended arc | real dramaturgy, no repeated climax gesture | code |
| T5 long-line and seam analyser (Schenker-lite) | one coherent line across sections | code + Opus reads |
| T6 audibility check (rhythmic contrast, register, stem levels per entry) | devices you can hear | code |
| T7 listening loop: auto-render each revision, compare measured loudness and density with T4 | revision by "ear" | code; Opus on flagged bars |
| T8 quality metrics beside correctness in the checker | critics start from numbers | code |
| T9 performance plans derived from the analysis | every entry and role brought out | code; Opus edits |
| T10 mixed metres and tempo maps | freedom of rhythm and metre | code |
| T11 N-voice combination finder, S2 stretto and inversion | Jupiter-style combination | code |
| T12 suspension and dissonance planner | stile-antico richness | code proposes; model fills |

**New recipe** (A §4): brief → material lab (T1, T11) → dramaturgy first (tension curve, cadence plan, theme-treatment plan, register arc; two designs, one judge) → **one composer writes the outer-voice frame of the whole piece** → parallel agents fill inner voices and episodes against free-material targets → two mandatory review rounds, critics reading T2-T6 metrics first → listening loop → derived performance plans and renders → listener's guide from the ledger.

**Process rules** (B): agent tasks capped at about 20 minutes, 40 turns and 150K context; each agent gets a generated section card (under 3k tokens) instead of the 17k-token blueprint; renders and searches run outside agents; stages commit as they go and restart from `status`; one heavy run per usage window.

## 3. Model tiers per stage

| Tier | Stages |
|---|---|
| **Opus, high effort** | brief shaping, picking materials, dramaturgy and design, the outer-voice frame, episodes and pivotal bars, the Bach / arc / theme critics, coordination |
| **Opus, medium effort** (approved) | routine inner-voice filling against a frame, local fixes from findings, integrator, editing derived performance plans, listener's guide and README, engine and tool maintenance, reading audio-QA reports, idiom review |
| **Sonnet / Haiku** | not used (decided 2026-09-25: stay within Opus; mechanical jobs go to code) |
| **Jev** | route each finding to notes or performance; park findings it calls minor; tie a finding to a section when the bar-number regex fails (confidence ≥ 0.9); drop a clear loser before the design judges |
| **Code** | every correctness and quality check (check, strict, splice, suspensions, T2-T8), the counterpoint-reviewer role (B: replaces a whole agent), searches, renders, audio measurement, plan derivation, status and resume |

Decided: every agent runs Opus 5.5. Effort is the only dial: high for the creative and critical stages, medium for routine ones. Replacing the counterpoint-reviewer agents with code (D2) stands.

## 4. Build phases and estimates

Units: cost-weighted tokens as in the run report (about $3.5 per million at list price, measured on this run). Wall-clock assumes at most 6 parallel lanes and one heavy run per usage window.

| Phase | Work | Agent runs | Tokens | Wall-clock |
|---|---|---|---|---|
| 1. Foundation | kit repo; vendor current tools; golden tests on *The Neighbour* first; CLI core, `status`, `doctor`; analysis package with one flag vocabulary; three new checks (unresolved seventh, device coverage, role-to-plan coverage); perform/render/engrave wrappers; path migration | 10 | 12-15M | 3-4 h |
| 2. Piece model and search | `piece.toml` schema, cards, splice and assemble for any voice count and metre (T10); merge the four proposals' search code into `find` (T11); T1 subject-lab | 8-10 | 12-16M | 3-4 h |
| 3. Quality tools | T2, T3, T4, T8 first (the biggest gain), then T5, T6, T12 | 8-10 | 10-14M | 3 h |
| 4. Recipes and glue | skill + 5 references, 5 workflow recipes, `tiers.json`, Jev routing and parking module, T9 derived plans, T7 listening loop, dry-run tests | 6-8 | 8-11M | 2-3 h |
| 5. Review and pilot | adversarial review of the kit, fixes; pilot = *The Neighbour* 1.1 (fix bar 54, give S2 a transposed and inverted statement, add real cadences in B-flat minor and A minor, raise strong suspensions to at least 26, regenerate performance roles), which tests the kit on known flaws | 6-8 | 12-18M | 3-4 h |
| **Total** | | **about 40-45** | **about 55-75M** (about $200-270; B's wider estimate is $450-800) | **about 14-18 h of runs, 3-4 usage windows, 2 days** |

**Per new piece afterwards** (estimate; the pilot measures it): about **40-90M** cost-weighted tokens (about $140-320) and **5-8 hours**. The low end is a lean piece with one review round (C). The high end is the full masterwork recipe with two rounds (A). This run cost 205M ($730) and 21 hours.

## 5. Decisions for you

1. ~~Model tiers~~ decided: Opus only, high or medium effort.
2. The kit's name (`kapell`) and home (a new repo under `longevityboris`, public or private).
3. Pilot choice: revise *The Neighbour* first (recommended: it tests every new check on known flaws), or go straight to a new piece.
4. MCP: not now, unless you want the kit from Claude Desktop or a remote session.
