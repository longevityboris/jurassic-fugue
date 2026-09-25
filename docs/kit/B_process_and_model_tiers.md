# B. Process, cost and model-tier audit

Scope: what "The Neighbour" actually cost, per agent role; which assets carry over to a new piece and what is hard-coded; which tier each role needs; the process rules that cut waste; the build estimate for the kit.

## Headline

1. **Measured spend: 1,288M raw tokens, about $728 at Opus 5.5 list prices** (162 transcripts, 147 workflow agents). 95.4% of raw tokens were cache reads, but in dollars the split is roughly a third each: cache writes 32%, cache reads 34%, output 34%. The things that drive cost are turns per agent times context size (two-thirds of spend) and thinking/output volume (one third). The choice of model comes third.
2. **A third of the spend was one-off engine building** (piano, strings, organ, orchestra, mix: builders + QA + fixers = $240, 33%). A new piece reuses the engines, so that third drops to zero. This is the biggest single saving, and it comes from reuse rather than from a cheaper model.
3. **Rework and harness overhead cost about 25% on top.** Designers ran three times (v1, v2, aborted restart: 12 agents, $106, of which one clean run of 4 was $80). The round-2 blueprint critics ran four times ($22 instead of about $6). 63 cache-miss rewrites cost $62 (8.5%), and half of them followed a gap of more than 5 minutes, i.e. an agent waiting on a render or search. Each agent's first turn carries about 42-52K tokens of harness context (system prompt, tools, skills list), which is re-read on every one of the 5,438 turns: about $70 (10%).
4. **Agent length predicts cost.** Agents that ran 60-116 minutes cost $15-23 each. Agents that ran 10-25 minutes cost $2-6. Median 31 turns, p90 107, context per turn 100-370K.
5. **Tiering, honestly quantified:** after reuse and process fixes (to about $280 per piece), tiering saves a further ~22% (to about $218). Most of that comes from **turning reviewing into code** (the counterpoint reviewer duplicates `splice_check.py` + `check.py` + `strict.py`) and from **running Opus at medium effort** on reviewers, fixers and performers. Sonnet/Haiku lanes save under $10 per piece. At these prices **Opus 5.5 cache reads ($0.20/M) cost the same as Sonnet 5's**, so moving a read-heavy lane to Sonnet saves about 30%, not 50%.
6. **Keep Opus high/xhigh** for the designer, synthesizer, blueprint fixer, composer, musical critic, and the panel's Bach, arc and theme lenses. These roles carry the "Bach/Beethoven" intellect, and the known gaps (bar 54 seventh, S2 never exposed) are theirs. The kit should also **add** the skipped review round 2 (+$9).
7. **Jev fits bounded routing, not musical judgement.** Interim results from the Jev lane's probe on this project's own data (`docs/kit/jev_probe_results.jsonl`):
   - Routing findings to a section file: 89% correct (90% at confidence ≥ 0.7), against 81% for the substring match `wf_compose.js` uses today.
   - Routing notes versus performance: 86%.
   - Severity: 67%, which is too weak.
   - Choosing the better of two revisions: 51%, which is chance.
   - Detecting an injected parallel fifth: mean noul 0.55 corrupted vs 0.54 original, so no signal.

   It costs about $0.04 per piece, so the case for it is calibrated branching, not savings.
8. **Per new piece of this scale: about $218 API-equivalent (-70% vs $728; -50% vs a like-for-like $436 with engines reused and no rework), and about 4-6 h wall-clock instead of 21 h.** The kit itself is about 80-120 agent-hours (roughly $450-800 one-off) and pays for itself within 1-2 pieces.

## 1. What the run cost, measured

Method: every `~/.claude/projects/-Users-biobook-Music-llm-music-fugue-jp/**/*.jsonl` was parsed. Usage was deduplicated per message id, each agent's `.meta.json` supplied its label and phase, and tokens were priced at Opus 5.5 list: input $4, cache write $5 (1.25x), cache read $0.20, output $20 per MTok. The script is in the appendix. $728 corresponds to 182M Opus-input-equivalent tokens, against the 205M "cost-weighted" in the brief. The difference is weighting: cache reads priced at 0.1x instead of Opus 5.5's 0.05x would give 244M. Percentages below hold under either weighting. Dollars stand in for plan usage, which was the real constraint: usage limits killed three runs.

| Token class | Raw tokens | Share of raw | $ at Opus 5.5 | Share of $ |
|---|---|---|---|---|
| Cache read | 1,228M | 95.4% | 246 | 34% |
| Cache write | 46.9M | 3.6% | 234 | 32% |
| Output (incl. thinking) | 12.5M | 1.0% | 250 | 34% |
| Uncached input | 0.2M | 0.0% | 1 | 0% |

Per role (the audit's own 4 agents excluded):

| Role | Agents | $ | % | Turns | $/agent | Note |
|---|---|---|---|---|---|---|
| Designer | 12 | 106.2 | 14.6 | 584 | 8.9 | v1 4×$6, v2 4×$17-23 (78-116 min each), aborted restart 4×$0.4 |
| Engine builder | 13 | 103.2 | 14.2 | 1052 | 7.9 | piano, strings, organ, orchestra, mix + finish passes |
| Engine QA | 11 | 68.8 | 9.5 | 741 | 6.3 | adversarial audio QA |
| Engine fixer | 6 | 68.5 | 9.4 | 636 | 11.4 | strings fix r1 alone $21.8 |
| Section reviewer | 14 | 57.3 | 7.9 | 280 | 4.1 | half is the "counterpoint" lens |
| Composer | 7 | 44.3 | 6.1 | 205 | 6.3 | sec02 $11.7 (60 min) |
| Performer/orchestrator | 5 | 32.9 | 4.5 | 336 | 6.6 | 37-50 min each, mostly running renders |
| Blueprint critic | 10 | 32.5 | 4.5 | 177 | 3.3 | r2 ran 4 times across killed runs |
| Blueprint fixer | 2 | 28.1 | 3.9 | 130 | 14.0 | r1: 95 min, 395K output, $20.4 |
| Coordination (main) | 1 | 25.1 | 3.4 | 240 | 25.1 | 1,404 min session, 289K average context |
| Section fixer | 7 | 23.9 | 3.3 | 208 | 3.4 | |
| Section reviser | 7 | 23.3 | 3.2 | 175 | 3.3 | |
| Render reviser | 4 | 23.0 | 3.2 | 276 | 5.8 | |
| Listening QA | 5 | 20.9 | 2.9 | 240 | 4.2 | "cannot hear", runs measurement scripts |
| Whole-piece panelist | 8 | 20.7 | 2.8 | 127 | 2.6 | round 2 killed after 3 turns each |
| Original 37-bar fugue | 1 | 19.5 | 2.7 | 79 | 19.5 | prior work |
| Judge | 3 | 10.7 | 1.5 | 91 | 3.6 | |
| Synthesizer | 1 | 10.7 | 1.5 | 64 | 10.7 | |
| Integrator | 2 | 4.4 | 0.6 | 67 | 2.2 | |
| Finisher | 1 | 3.6 | 0.5 | 47 | 3.6 | |
| **Total** | 147 | **728** | | 5,438 | | |

Waste, measured:

| Item | $ | Evidence |
|---|---|---|
| Duplicate design runs (v1 superseded, restart aborted) | 26 | wf_5ef22788 designers 4×$6; wf_390ce798 designer restarts 4×$0.4 |
| Round-2 critics re-run after kills | ~16 | 8 critic-r2 agents in wf_998ea8cc + wf_a480356e ($22) for one round's work (~$6) |
| Cache-miss rewrites | 62 | 63 turns wrote >50% of context anew; 32 of them came after a >5 min gap (a blocking render/search let the 5-min TTL expire), 31 within 5 min (fat-context workers running in parallel) |
| Harness baseline context | ~70 | first turn about 31K written + 11K read per agent; about 45K re-read on each of 5,438 turns |
| Killed agents' partial work | not separable | three kills; the `skip` list in `wf_continue.js` was set by hand |

## 2. Reusable assets and what is hard-coded

Already general: `check.py` and `harmony.py` take `--voices`, `--measure`, `--range`, `--key`. `perform.py` reads voices and measure from the plan. The engines read library roots from `SAMPLE_LIBRARIES`/`PIANO_LIB`. `splice_check.py` already verifies boundaries, locked subject/answer/cf/cs spans, keep items and unisons, then runs `check.py` + `strict.py` on the joins.

| Asset | Lines | Hard-coded / missing | Generalisation work | Agent-h |
|---|---|---|---|---|
| `tools/lyparse.py` | 82 | `\absolute` only: no tuplets, chords `<>`, grace notes, `\relative`, meter changes, pickups | Add these (needed for Mozart/Beethoven/Liszt figuration and piano chords); golden tests | 6-8 |
| `tools/check.py` | 325 | One strict-fugal rule set; beat grid assumes 4/4-2/2 strong beats; every line counts as a real voice | Style profiles (strict / classical / romantic), doublings vs real voices, beat hierarchy for 3/4, 6/8, 3/2 | 8-12 |
| `tools/harmony.py` | 100 | Fine | Cadence detection, harmonic-rhythm stats | 2-3 |
| **New** resolution checker | - | Absent: bar 54's E-flat seventh went unresolved and nothing flagged it | Track chordal sevenths, leading notes and 4/2 basses to resolution | 4-6 |
| **New** coverage audits | - | Absent: S2 never got an exposition; the lament and head-imitation roles never reached the performance plans | Declared devices vs roles present; every declared role has a performance-plan entry | 3-4 |
| `tools/assemble.py` | 47 | `VOICES = ['soprano','alto','tenor','bass']`; glob `score/sections/sec[0-9]*.ly` | Read voices and paths from the piece spec | 1 |
| `final-lab/strict.py`, `suspensions.py`, `splice_check.py`, `spanmap.py`, `grid.py`, `verify.py` | 128-162 each | SATB literal in each; `suspensions.py` assumes strong beats 1 and 3; `grid.py` has fixed S A T B columns | Voices and meter from the spec | 4-6 |
| `final-lab/timeline.py` | 70 | `LANDMARKS` list of this piece's bars | Landmarks from the spec; emit the NOTES form table | 1-2 |
| `final-lab/piece.py` + `build_sk.py` | 202 + 74 | `piece.py` is the piece: 4 voice strings per section, fugue roles, B-flat | Turn it into a piece-spec schema (sections, voices + ranges, key map, meter map, roles incl. generic melody/accompaniment/bass, keep, tempo, dynamics, landmarks, declared devices) | 8-16 |
| Search tools, 4 copies: `proposal-4/tools/solve.py` (beam search, 494), `stretto.py`, `search_combo.py`, `strict2.py`; `proposal-1/lab/search.py`, `augsearch.py`, `stretto_grid.py`; `proposal-2/lab/cs_search.py`, `combo4.py`; `proposal-3/lab/cs1search.py`, `stretto4.py`, `lab_perm.py` | ~2,500 | Each designer wrote its own; `solve.py` imports the piece-specific `p4.py`/`mats.py` | One contrapuntal search library: free-voice beam search, stretto finder (interval × distance), invertibility at 8ve/10th/12th, subject combination, augmentation/inversion fitters, triple-counterpoint permutations; tests against known Bach cases | 12-20 |
| `tools/perform.py` | 308 | Roles are fugal (subject/answer/cf/cs/free) | Generic roles; meter-aware beats | 3-4 |
| `tools/orchestrate.py` + `ORCHESTRATION.md` | 1,049 | Four renderer groups; voice-to-instrument maps assume 4 voices | Any voice count and instrument set | 3-4 |
| `tools/mix.py` | 1,161 | Detmold hall through `audio/strings/hall.py`; `CAL_DIR` under `ricercar/` | Hall/IR and calibration as parameters (Detmold stays the default) | 3-4 |
| Engines (`audio/piano`, `strings`, `organ`, `orchestra`) | ~11,400 | `organ_paths.py` hard-codes `/Users/biobook/Music/SampleLibraries` and `/opt/homebrew/bin/wvunpack`; `piano_paths.py` Detmold IR; strings = quartet only (vn1, vn2, va, vc) | Config file for paths; one `setup` command; string orchestra with double bass and divisi | 8-12 |
| Engine QA (`audio/piano/qa/qa_*.py`, `organ/tests`, `strings/verify_*.py`, `orchestra/qa_orchestra.py`) | ~3,000 | Run by LLM agents | One deterministic `kit qa VERSION` → JSON (loudness vs plan arc, stem balance, clipping, clicks, stuck notes, tuning, duration) with thresholds | 4-6 |
| `tools/wf_*.js` (6 scripts) | 1,039 | `ROOT`, `LIB` paths; Jurassic Park context prose; SATB MIDI ranges; the version list; 210-250 s target; skip list set by hand | One parametrised workflow: piece spec + style + versions in, per-role model/effort, stage manifests for automatic restarts, Jev hooks | 6-10 |
| Packaging | - | - | CLI (`kit new / verify / search / compose / render / qa / cost`), skill docs, optional MCP wrapper over verify/search/render | 6-10 |
| Regression suite | - | - | "The Neighbour" as a golden piece: `verify` reproduces 0 errors / 0 parallels / 18 strong suspensions; renders byte-identical | 4-6 |
| **Total** | | | | **~80-120** |

At the measured rate (Opus xhigh engine agents: about $8 per agent-hour; Sonnet implementation about half), the kit costs roughly $450-800 one-off. The two tasks that need Opus-high design are the piece-spec schema and the search library. The rest is Sonnet-grade implementation against tests.

## 3. Role → tier map

Tiers: (a) Opus 5.5 high/xhigh, (b) Opus 5.5 low/medium, (c) Sonnet 5, (d) Haiku 4.5, (e) Jev, (f) plain code. Prices per MTok: Opus 5.5 $4 in / $5 write / $0.20 read / $20 out; Sonnet 5 $2 / $2.50 / $0.20 / $10; Haiku 4.5 $1 / $1.25 / $0.10 / $5; Jev $0.04 in, output free.

"Now" is the measured cost. "Clean" removes duplicates and adds the skipped panel round 2. "Kit" applies process fixes and the tier. The factors are estimates, to be measured with the A/B in section 6.

| Role | Tier | Why | Now $ | Clean $ | Kit $ | Main lever |
|---|---|---|---|---|---|---|
| Designer (×4) | a | Invents the subjects, device plan and form: the intellectual core. The search library replaces ad-hoc solver writing (13-22 scripts per proposal) | 106.2 | 80.4 | 48 | reuse the search library, cap context |
| Judge (×3) | b + f | Code tabulates verified devices/proofs per proposal; Opus-medium weighs them. Jev ranking of whole designs is not assumed (the probe's t4 task tests it) | 10.7 | 10.7 | 6 | effort, code metrics |
| Synthesizer | a | Merges designs; structural reasoning | 10.7 | 10.7 | 10 | none |
| Blueprint critic, counterpoint lens | f + b | `verify.py`, `strict.py`, `suspensions.py` and the coverage audit do the checking; Opus-medium interprets | 32.5 (both lenses) | 16 | 11 | code gates, no repeats |
| Blueprint critic, musical lens | a | Judges beauty, arc, idiom | (above) | | | |
| Blueprint fixer | a | Rewrites the plan and materials | 28.1 | 28.1 | 20 | split into ≤20 min tasks |
| Composer (per section) | a | Note-level choices decide quality; the known gaps are compositional | 44.3 | 44.3 | 33 | focused brief, solver in the loop |
| Section reviewer, counterpoint | f + e | `splice_check.py` already checks entry pitches, locks, boundaries, unisons, parallels and clashes; add the resolution checker. Jev routes findings | ~27 | ~27 | 1 | delete the lane |
| Section reviewer, music | b | Singing lines, padding, idiom | ~30 | ~30 | 20 | effort |
| Section reviser / section fixer | b | Applies located findings | 47.2 | 47.2 | 30 | effort, focused input |
| Integrator | c + f | `assemble.py` and the checks are code; seam edits are small | 4.4 | 4.4 | 2 | Sonnet |
| Panel: Bach, arc, theme | a | Whole-piece judgement; round 2 must run | 20.7 (4 lenses) | 31 | 24 | add round 2; code device audit feeds the Bach lens |
| Panel: idiom | c + f | Hand spans, ranges and string crossings can be checked in code | (above) | | | |
| Performer/orchestrator | b + f | Code derives a default plan from the spec's roles (entries, lament, head imitation); Opus-medium adds interpretation; renders run outside the agent | 32.9 | 32.9 | 12 | background renders, generated plan |
| Listening QA | f + c | `kit qa` measures; Sonnet reads the JSON against the plan | 20.9 | 20.9 | 4 | code |
| Render reviser | b | Spec edits | 23.0 | 23.0 | 8 | background renders |
| Finisher / NOTES | c + f | `timeline.py` computes timings; prose is routine | 3.6 | 3.6 | 1.5 | Sonnet |
| Coordination | a (session) | Decisions stay with the user's session | 25.1 | 25.1 | 13 | CLI, automatic restarts |
| Engine builder / QA / fixer | c (if ever) | Reuse. Maintenance and generalisation are DSP code; Sonnet 5 is sufficient against the existing QA suites | 240.5 | 0 | 0 | reuse |
| Mechanical edits, summaries, commit text | d or f | Prefer code: transposition, JSON conversion and file moves are deterministic | ~0 | | | |
| Finding triage (route, dedupe, round gate) | e | See section 4 | 0 | | 0.05 | new |
| Original 37-bar fugue | - | Prior work, not per piece | 19.5 | 0 | 0 | |
| **Total** | | | **728** | **436** | **~242 → ~218** | the last step is the harness diet (−10%) |

Savings by layer: reuse and no rework, $728 → $436 (−40%). Process (focused briefs, ≤20 min agents, background renders, code gates, harness diet), $436 → about $280 (−36%). Tiering (effort, code, Sonnet, Jev), about $280 → $218 (−22%).

### Downgrades that conflict with the user's rule

The user's global rule says: "Workers inherit the session model; never downgrade a lane." These are the recommended exceptions. The user decides each one.

| # | Recommendation | Saving per piece | Risk | Recommendation strength |
|---|---|---|---|---|
| D1 | Opus 5.5 at **medium** effort (same model) for judges, critics' counterpoint lens, section reviewers (music), revisers, fixers, performers, render revisers | ~$35 | Shallower reviews. Mitigated by code gates plus Opus-high panels at the end | Strong. Arguably not a lane downgrade: Opus 5.5's own API default is medium, and Claude Code runs higher. The transcripts do not record effort; median output per agent was 87K tokens (111 agents with >5 turns), which suggests high/xhigh |
| D2 | Remove the counterpoint-reviewer LLM lane (code + Jev) | ~$26 | A code gate misses what a rule doesn't encode. Mitigated by the new resolution and coverage checkers | Strong |
| D3 | Sonnet 5 for integrator, idiom lens, listening-QA reading, NOTES/docs, and engine maintenance/generalisation code | ~$8 per piece; ~$150-250 on the one-off kit build | Sonnet needs more turns on DSP subtleties; cache reads cost the same, so only about 30% is saved | Moderate: worth it for the kit build, marginal per piece |
| D4 | Haiku 4.5 for summaries and format conversion | <$2 | none | Weak: do it in code instead |

Never downgrade: designer, synthesizer, blueprint fixer, composer, musical critic, panel Bach/arc/theme lenses, coordination.

## 4. Jev: where it fits

Jev's own jaggedness notes list what it handles badly: literal reading, numbers and counting, indirection, large irrelevant state, generation. LilyPond or a sonority grid is numeric, multi-hop state, and the interim probe on this project confirms it: 51% on "which revision is better" and no separation between corrupted and original passages. Every use below is a closed question over text:

| Hook | Primitive | Replaces | Evidence / gate |
|---|---|---|---|
| Route a review finding to its section file | Choice over section ids (state: finding + section one-liners) | `x.where.includes(file)` in `wf_compose.js`, which leaves "unplaced" issues | Probe: 89% vs 81% substring; act at confidence ≥ 0.7 (90%), otherwise send to the integrator |
| Route to a lane: notes / performance / engraving / engine / docs | Choice | Integrator guessing | Probe: 86% notes vs performance |
| Dedupe panelist findings | Noul per pair, after code pre-filters by overlapping bars | Fixers getting the same issue four times | Untested; gate at 0.8 |
| Should review round 2 run? | Noul "names a problem a listener would hear" per finding, then OR in code, low confidence → run it | Round 2 skipped for time | Cheap enough to always ask; defaults to running |
| Did the reviser address finding X or defer it? | Noul over the reviser's notes; then code re-runs the checker | Silent non-fixes | Untested |
| Which blueprint paragraphs a given agent needs | Score per paragraph (relevance to section X), keyed by section id, not bar number | "Read the blueprint fully" (66 KB) in every prompt | Cuts context re-reads |
| Severity major/minor | Not recommended | - | Probe: 67% (61% on the first sentence only) |

Volume: about 200 calls × 5K tokens per piece = 1M input tokens ≈ $0.04, at 70-500 ms each. The TypeSafe Python SDK runs inside the workflow's code steps, with the key coming from Keychain via `akm`.

## 5. Process rules

1. **Short agents.** ≤20 min, ≤40 turns, context ≤150K per task. Split larger work into sequenced tasks with file hand-offs. Evidence: the 60-116 min agents cost $15-23, the 10-25 min agents $2-6, and the 95-min blueprint fixer alone emitted 395K output tokens.
2. **Focused briefs instead of "read everything".** Code generates each agent's brief (≤15K tokens): the section's spec from the piece spec, the locked spans from `spanmap.py`, the materials it uses, its neighbours' boundary notes. Tools run in `--quiet`/summary mode, because every tool result is re-read on each later turn. Composer and reviewer turns ran at 110-210K context; the target is under 80K.
3. **Harness diet.** Run kit agents with a minimal agent definition: only Read/Edit/Write/Bash, no MCP servers, no skills listing. Each agent currently starts at about 42-52K tokens before reading any task file. Saving: about $50-70 per run.
4. **Never block a turn on a long command.** Renders, beam searches and LilyPond batches run in the background with polling, or better, outside the agent as a deterministic stage. 32 cache rewrites followed a >5 min wait.
5. **Cap fat-context parallelism.** At most 3-4 concurrent agents with >100K context, within the user's 6-worker cap. 31 rewrites happened within 5 minutes, consistent with eviction under load.
6. **One run per usage window, with automatic restart.** Each stage writes a manifest (input hashes → outputs, verdict). A restart skips completed stages by hash, not by a hand-edited `skip` list. Evidence: designers ran 3 times and critics r2 four times across kills.
7. **Deterministic render pipeline.** `kit render VERSION` = perform → orchestrate → render → mix → encode → `kit qa` JSON, with no agent unless QA fails a threshold. Render agents spent 37-50 min each mostly running scripts.
8. **Code gates before LLM review.** `splice_check`, `verify`, a suspension target, the new resolution checker (it would have caught bar 54), the device-coverage audit (it would have caught S2 never being exposed), the performance-role coverage check (it would have caught the tenor lament and bass head imitation), and engraving every version (only piano and quartet scores were printed). LLM reviewers only see pieces that pass.
9. **Measure every run.** `kit cost` = the appendix script, run after each workflow: per-role $, turns, context, cache-miss count. Use it to settle D1-D3 empirically (section 6).
10. **Opus effort per role, set explicitly** in the workflow (`agent(..., {model, effort})` or the agent definition), never inherited by accident.

## 6. Plan and estimate

| Step | Content | Agent-h | Tier |
|---|---|---|---|
| 1 | Piece-spec schema + `build_sk` generalisation; migrate "The Neighbour" as the golden piece | 10-18 | a (schema) + c |
| 2 | Parser extensions, voice/meter generalisation of all checkers, `assemble.py` | 11-15 | c |
| 3 | Contrapuntal search library (merge the 4 proposal toolsets, with tests) | 12-20 | a + c |
| 4 | New checkers: resolution, device coverage, performance-role coverage, style profiles for `check.py` | 15-22 | b + c |
| 5 | `perform`/`orchestrate`/`mix`/engine config, `kit render`, `kit qa` | 18-26 | c |
| 6 | Parametrised workflow with stage manifests, per-role tier/effort, Jev hooks, `kit cost` | 8-12 | b + c |
| 7 | CLI, skill docs, optional MCP wrapper, regression suite | 8-12 | c |
| **Total** | | **~80-120** | ≈ $450-800 one-off |

A/B test before fixing D1-D3: run the section-reviewer (music) and reviser lanes for two sections at Opus xhigh vs Opus medium (and Sonnet), with the same briefs, and compare findings against the round-1 panel's list and the checker deltas. Cost is about $25. Keep a downgrade only where it recovers at least 90% of the major findings.

Per new piece of this scale afterwards: about $218 API-equivalent (under a third of one usage-limit-killing run) and about 4-6 h on the critical path. Rough breakdown: design 40 min → judge/synthesise 30 → critique/fix 40 → compose 45 → review, fix, panel r1+r2 90 → render + QA 40 → notes 10.

## Appendix: `kit cost` (the measurement used here)

```python
import json, glob, os, collections
base = os.path.expanduser('~/.claude/projects/<project-slug>/')
P = dict(input_tokens=4.0, cache_creation_input_tokens=5.0, cache_read_input_tokens=0.20, output_tokens=20.0)  # Opus 5.5 $/MTok
by_role = collections.Counter()
for f in glob.glob(base + '**/agent-*.jsonl', recursive=True):
    meta = f.replace('.jsonl', '.meta.json')
    label = json.load(open(meta)).get('description', '?') if os.path.exists(meta) else '?'
    seen = {}
    for line in open(f):
        d = json.loads(line)
        m = d.get('message', {}) if d.get('type') == 'assistant' else {}
        if m.get('usage') and m.get('id'):
            seen[m['id']] = m['usage']          # one usage record per API message
    by_role[label] += sum((u.get(k) or 0) * p / 1e6 for u in seen.values() for k, p in P.items())
for label, usd in by_role.most_common():
    print(f'{usd:8.2f}  {label}')
```
