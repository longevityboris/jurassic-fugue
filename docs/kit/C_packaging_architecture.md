# C. Packaging architecture: how to ship the composition kit

Role: packaging architect. Scope: the form the kit takes (CLI, skills, workflows, MCP), its command surface, layout, versioning, tests and build effort. The musical method and the cost autopsy belong to the sibling reports; they appear here only where they decide a packaging choice.

Working name for the kit: **`kapell`**. Bach's job title was Kapellmeister: he composed the music, rehearsed it and directed the performance, and the kit does the same three jobs (compose, perform, render). No `kapell` binary exists on PATH today.

---

## 1. Verdict

**Build one Python CLI (`kapell`), one installed skill with reference files, and a set of workflow recipes shipped inside the skill. Skip MCP for now; a thin, optional MCP adapter comes later, and only if something other than Claude Code on this Mac needs the kit.**

| Layer | What it holds | Why this layer |
|---|---|---|
| `kapell` CLI (Python, `uv tool install`) | Every deterministic step: materials derivation and search, proofs, check, x-ray, skeleton, splice, assemble, engrave, perform, render, QA, Jev calls, status, setup, doctor | 17,334 lines of working Python already exist (tools, final-lab, four engines), plus 5,141 in the proposal search tools. They run in 0.1 to 17 s and need numpy, scipy, soundfile and mido. They need a stable front door, not a rewrite. |
| `kapell` skill (`~/.claude/skills/kapell/`) | SKILL.md router, 5 reference docs, `workflows/*.js`, `tiers.json` | This is how Claude Code agents on this machine learn a tool. Suno's SKILL.md puts it this way: "All capability detail lives in the binary so it never drifts from this file." |
| Workflow recipes (`workflows/*.js`) | design, compose, review, render and finish pipelines, with a model/effort/Jev tier on every stage | The multi-agent structure that produced the piece, now parameterised by the project (`args`) instead of hardcoding `ROOT`, and with each stage's tier set in the recipe. |
| MCP adapter (deferred) | Generated from `kapell agent-info` if ever needed | No latency case (see §2). It would only matter for Claude Desktop, claude.ai or a remote session, and those can't reach the 15 GB of local samples anyway. |

---

## 2. Evidence behind the choice

| Fact (measured this session) | Packaging consequence |
|---|---|
| The user's tools share one contract. `suno agent-info` returns `{name, version, commands, guides, global_flags, exit_codes, breaking_changes, envelope, config, auto_json_when_piped}`. `akm agent-info` returns `{version, status, data:{commands:{…effect: read/write/execute, examples}}}`. Both offer `agent-info --command X`, `doctor`, and `skill install / skill status`, and suno also has `guide <name>`. | `kapell` adopts the same contract, so agents that already know `suno` and `akm` know `kapell`. |
| Secrets live in akm. `TYPESAFE_API_KEY` is stored, and `akm run --only KEY -- cmd` injects it into a child process. | Jev calls go through `akm run --only TYPESAFE_API_KEY -- kapell jev …`, and the CLI reads the key from the environment. A long-running server holding the key would be a new pattern for this machine. |
| `check.py` takes 0.10 s on the 66-bar score, `suspensions.py` 0.21 s and `harmony.py` about 0.3 s. The organ render takes 17.4 s for 241.7 s of audio, and the piano tests about 25 s. | A resident MCP process would save roughly 0.2 s of Python start-up per call, which is nothing next to agent turns that take minutes. |
| 97% of raw tokens were cache re-reads. `BLUEPRINT.md` is 66 KB (about 17k tokens), `critique_r1.json` 25 KB and `NOTES.md` 13 KB. Composer prompts told every agent to "read the blueprint fully". | The biggest cost lever is context size per agent turn, not the choice of transport. The CLI has to emit **small, sliced artefacts** (section cards, x-ray digests, `status`), and that is a CLI and workflow feature (§4). |
| Workflow `agent()` accepts `{model, effort, schema, agentType, isolation}`. Runs resume from `resumeFromRunId` with a cached prefix. Concurrency is capped at min(16, CPUs−2), which is 14 on this 16-core Mac. Recent Claude Code workflows also pause and resume at usage limits instead of dropping agents. | Tiering can be declared per stage in the recipe. Resume exists in the harness, so the kit only needs idempotent, commit-per-step stages and a `status` that says what is done. |
| This session already lists about 300 deferred MCP tool names and about 60 skills. | Every extra skill description and MCP tool name is carried into every session and subagent. One skill with progressive disclosure beats five separately triggered skills. |
| Argument parsing is inconsistent today. `check.py`, `harmony.py`, `strict.py` and `suspensions.py` parse raw `sys.argv`, while `mix.py` and `orchestrate.py` use argparse. `check.py` opens its input file **at import time** (line 16). `harmony.py --key bes` crashed because the flag wants range syntax (`--key 1-20=bb`). | The wrapper cannot simply shell out to these scripts. Each one needs a thin refactor into an importable function with one normalised flag vocabulary. That is real, estimated work (§11). |
| 14 script files hardcode `/Users/biobook`: 10 point at the repo and 9 at `~/Music/SampleLibraries`. `organ_paths.py` and `setup_organ.sh` pin `LIB`, while the piano README already uses `$PIANO_LIB`. | Path migration to one config key (`KAPELL_LIB`, with the old variables as aliases) is a named task. |
| Sample libraries take 15.3 GB (IowaMIS 5.9, Orchestra 3.9, Organ 1.9, Salamander 1.4, VPO3 1.3, IR 0.75), and renders 3.4 GB under `ricercar/audio/*/out` (gitignored). The tracked repo is 570 files, 9.9 MB. | Libraries stay outside every repo and are verified by `kapell setup` against pinned SHA-256 hashes (the piano setup already does this). Renders move out of the project tree. |

### Options compared

Scores run 1 to 5, higher is better. They are judgements, and the reasons are in each cell.

| | One big skill only | Set of 5 skills | **CLI + 1 skill + workflows (recommended)** | MCP server (+ skill) |
|---|---|---|---|---|
| Speed | 2: agents re-derive steps in prose, and scripts get invoked ad hoc with inconsistent flags | 2: same | **5**: deterministic steps in 0.1 to 17 s; agents only reason | 5: same compute, plus about 0.2 s saved on start-up (irrelevant here) |
| Cost (tokens) | 2: the playbook text sits in context whenever the skill fires | 1: five descriptions in every session and subagent, plus trigger mis-picks | **5**: `agent-info --command X` and `guide X` are loaded on demand, and outputs are compact JSON | 3: tool schemas or names are carried per agent, with a ToolSearch round-trip each time |
| Flexibility | 4: anything goes, which is also why every run drifts | 4 | **5**: shell pipes, scripts, workflows, Codex and any agent can call it; new forms plug in as templates | 3: MCP clients only; workflows reach it through ToolSearch |
| Agent ergonomics | 3 | 2: which skill applies? | **5**: matches suno, akm, elevenlabs and agenttalk; one JSON envelope; exit codes drive loops | 4: typed schemas are nice, but it is a new pattern on this machine |
| Maintenance | 2: prose drifts from code | 1: five docs drift | **4**: one surface; skill and guides are generated from the package | 2: two surfaces (CLI and server) plus a daemon lifecycle |

---

## 3. The CLI surface

### Conventions (copied from suno and akm)

* **Envelope.** Success is `{version:"1", status:"success"|"no_results"|"partial_success"|"fail", data}`. Errors are `{version, status:"error", error:{code, message, suggestion}}`. Output is JSON automatically when piped, and `--json` and `--quiet` are global flags.
* **Exit codes.** 0 ok; 1 transient (retry); 2 config or environment (missing engine, library or key: run `kapell doctor`); 3 bad input; 4 rate limited (Jev 429); **5 musical check failed**, with the violations in `data`. Code 5 is a documented extension, so shell loops such as `until kapell check …; do …; done` work.
* **Manifest.** Every command declares `effect: read|write|execute`, `examples`, `runtime_s` and `output_tokens_typ`. The last field tells an agent what a call will cost in context before it runs it. `breaking_changes` is keyed by version.
* **Project discovery.** Commands walk up from the working directory to `kapell.toml`, as git does, so no absolute paths appear in prompts.

### Commands

| Command | Effect | Wraps (existing files) | Typical runtime | Notes |
|---|---|---|---|---|
| `new DIR --brief brief.md [--template fugue4\|fugue3\|sonata\|variations\|chorale-prelude]` | write | new `templates/` | <1 s | Writes `kapell.toml`, folders and git init. The template fixes voices, ranges and meter. |
| `status` | read | git log + `runs/` journal + last x-ray | <1 s | Under 2k tokens: phase, done and open sections, last check totals, quotas, next command. It is the resume point after usage-limit kills (three runs died that way). |
| `materials derive --subject S` | write | `proposal-4/tools/mats.py`, `p4.py`, `proposal-1/lab/mats.py` | <1 s | Tonal and real answer, inversion, augmentation, diminution, retrograde, at reference pitch, written to `materials/materials.ly` and `.json` |
| `find cs --against S [--invertible 8,10,12]` | read | `proposal-4/tools/solve.py` (beam search, `invert=`), `gen_cs*.py`, `proposal-1/lab/cssearch.py` | seconds to minutes | Returns the top N checker-clean candidates with cost terms |
| `find stretto --lines S[,I] --intervals … --distances …` | read | `stretto.py`, `stretto_ck.py`, `proposal-1 P09_*` | seconds | |
| `find combo --lines S1,S2,CS1,CS2` | read | `search_combo.py`, `combo_rank.py`, `combo_real.py`, `proposal-1/lab/perm.py`, `matrix.py` | seconds | Includes all 6 vertical permutations (the T1 to T6 labs) |
| `find aug --subject S --against …` | read | `aug_search.py`, `aug_pedal.py`, `proposal-1/lab/augsearch.py`, `apo.py` | seconds | |
| `prove LAB.ly` | write | `check.py` + `strict.py` + `verify.py` | <1 s | Appends a row to `design/proofs.json`; the blueprint cites proof ids, not prose |
| `skeleton build` | write | `final-lab/piece.py`, `build_sk.py`, `sections.py`, `timeline.py`, `plan.json` | <1 s | One source gives the skeleton `.ly`, `plan.json` and **per-section context cards** (§4) |
| `check FILE\|--section N [--bars A-B]` | read | `tools/check.py`, `lyparse.py` | 0.1 s | Normalised flags; errors-only digest by default, `--full` for every line |
| `xray FILE\|--section N` | read | `check` + `harmony.py` + `suspensions.py` + `strict.py` + `grid.py` + `spanmap.py` + **new** role-coverage and quota checks | <1 s | One JSON bundle replaces five scripts with five flag dialects |
| `splice --section N` | read | `splice_check.py` | <1 s | Seams and blueprint "keep" items |
| `assemble` | write | `tools/assemble.py`, `make_global.py` | <1 s | |
| `engrave --layout piano\|quartet\|organ\|orchestra\|ensemble\|all` | write | lilypond + layout templates | seconds | `all` is the default in the finish recipe. Only 2 of 5 layouts were printed for The Neighbour. |
| `perform --version V` | write | `tools/perform.py`, `performance/*/articulate.py`, `presence.py`, `levels.py`, `bowing.py`, `swell.py` | seconds | Lints the plan: every featured role gets a dynamic or articulation cue (§5) |
| `render --version organ\|piano\|quartet\|orchestra\|ensemble [--bars A-B] [--stems]` | execute | `performance/*/render.sh`, `audio/{organ,piano,strings,orchestra}/render_*.py`, `orchestrate.py`, `mix.py` | 17 s (organ) to minutes (orchestra) | `--bars` gives quick previews; writes `renders/<version>.{wav,m4a,render.json}` outside the repo |
| `qa --version V` | read | `qa_orchestra.py`, `strings/qa_render.py`, `organ/analyze_organ.py`, `orchestration/tests/qa_mix.py`, `piano/analyse_dynamics.py` | seconds | Numeric thresholds are enforced **in code**, never by Jev |
| `jev triage\|dedupe\|route\|rank\|calibrate` | execute | new `kapell/jev/` | 70 to 500 ms per call | See §7. Run under `akm run --only TYPESAFE_API_KEY --`. |
| `workflow args RECIPE` | read | new | <1 s | Emits the JSON `args` for a Workflow call: sections, card paths, tiers, project root. Scripts cannot read files, so the CLI computes their inputs. |
| `setup --engine piano\|organ\|strings\|orchestra\|all [--check]` | execute | `audio/*/setup_*.sh` | 6 s when present; downloads otherwise | SHA-256 pins as the piano setup already does |
| `doctor` | read | new | seconds | lilypond, sfizz_render build, libraries, IRs, Jev key present, Python dependencies |
| `guide [name]` | read | new `guides/*.md` | instant | Raw markdown on stdout, a documented envelope exception (as in suno) |
| `skill install\|status` | write | new | instant | Copies SKILL.md, references and workflows from the installed package to `~/.claude/skills/kapell/` |
| `agent-info [--command X]` | read | new | instant | |

Manifest excerpt (shape only):

```json
{"name":"kapell","version":"0.1.0","envelope":{"version":"1"},
 "exit_codes":{"0":"ok","1":"transient","2":"config/env: run kapell doctor","3":"bad input","4":"rate limited","5":"musical check failed: see data.violations"},
 "commands":{
  "xray":{"effect":"read","runtime_s":0.6,"output_tokens_typ":900,
          "args":[{"name":"target","kind":"positional","description":"score file or --section N"}],
          "options":[{"name":"--bars","type":"string"},{"name":"--full","type":"bool","default":false}],
          "examples":[["xray","--section","7"],["xray","score/music-voices.ly","--bars","49-56"]]},
  "render":{"effect":"execute","runtime_s":"17-240",
          "options":[{"name":"--version","values":["organ","piano","quartet","orchestra","ensemble"],"required":true},
                     {"name":"--bars","type":"string"},{"name":"--stems","type":"bool"}]}}}
```

---

## 4. Context-cost design (the main lever)

With 97% of raw tokens spent on cache re-reads, the cost of a long agent is roughly its **context size × turns**. Every CLI output is designed to shrink context:

1. **Section cards.** `skeleton build` writes `design/cards/secNN.md` (target under 3k tokens): the section's own blueprint paragraph, its roles table, boundary notes and keep items, the materials excerpts it uses at pitch, and the neighbouring sections' first and last chords. Composers read their card, not the 17k-token blueprint. That cuts about 14k tokens per turn per composer. At roughly 30 to 60 turns per composer, it saves 0.4 to 0.8M raw tokens per agent (estimate).
2. **Digests by default.** `check` prints only violations and totals. A clean `check.py` run on the full score still prints every dissonance line; the digest is about 150 tokens. `xray` caps its output and prints `--full` as a hint.
3. **`agent-info --command X` and `guide X`** load on demand. SKILL.md stays under about 120 lines, and the playbook sits in `references/`.
4. **Findings as data, not prose.** Critics return schema'd findings with `where: "secNN bar:beat"`. Code groups them by section, so each fixer sees only its own (as `wf_compose.js` already partly does).
5. **Short-lived agents with typed handoffs.** One agent per section per round, instead of long agents that re-read everything each turn. The recipes enforce `schema` on every `agent()`.
6. **Commit-per-step plus `status`.** After a usage-limit pause or kill, a resumed run replays cached `agent()` results; `status` tells a fresh coordinator what is done in under 2k tokens, instead of re-reading the repository (10M of coordination cost last time).

---

## 5. Turning the final-check gaps into kit features

Each known gap in The Neighbour is a missing **check, quota or lint**. Code can catch all of them, so they go into `xray`, `perform` and the recipes rather than into prose reminders:

| Gap in The Neighbour | Kit feature that catches it | Where |
|---|---|---|
| Bar 54: the seventh (E-flat) of V4/2 never resolves | `xray` rule: chordal sevenths and other tendency tones must resolve by step in the same voice or in a hand-off voice within N beats; report unresolved ones as `DIS7` | `analysis/harmony.py` |
| S2 never gets its own exposition, answer or inversion, so "double fugue" overstated it | Role-coverage check: `kapell.toml` declares the form (`form = "double-fugue"`), and the template requires S2 roles `subject`, `answer`, `inversion` and a combination with S1; `xray` fails the form claim if the roles table lacks them | `piece/model.py` |
| 18 strong-beat suspensions against a target of 20 | Quotas in `kapell.toml` (`[quotas] strong_suspensions = 20`), reported by `xray` and `status` | `analysis/quotas.py` |
| Arioso tenor lament and bass head imitation not brought out in performance plans | `perform` lint: every role tagged `feature` in the piece model needs a dynamic, articulation or registration cue in every version's plan | `perform/lint.py` |
| Review round 2 skipped for time | The review recipe loops until `major == 0` or `rounds == max_rounds`, with a budget guard; skipping a round is logged, never silent | `workflows/review.js` |
| Only piano and quartet scores printed | `engrave --layout all` runs in the finish recipe; `status` lists missing layouts | `workflows/finish.js` |

---

## 6. Skill set and workflow recipes

### One installed skill, five reference files

```
~/.claude/skills/kapell/            (installed by `kapell skill install`, generated from the package)
  SKILL.md                          router: when to use, the 10 commands that matter, the recipe table, pointers
  references/method.md              composing playbook: brief -> materials -> proofs -> blueprint -> skeleton -> sections -> seams -> review -> perform
  references/counterpoint.md        what check/xray enforce and what they don't (judgement areas), with Bach, Mozart and Beethoven exemplars by device
  references/orchestration.md       ensemble idioms, ranges, doubling rules, the 5 render versions and their contracts
  references/performance.md         plan schema, articulation, registration, bowing, tempo maps, the feature-role lint
  references/recipes.md             the workflows, their args, and the tier table (below)
  workflows/{design,compose,review,render,finish}.js
  workflows/tiers.json              one file sets model/effort/Jev per stage
```

This follows the layout of `~/.claude/skills/litscreen/`, which is already a skill plus a dynamic workflow on this machine (`SKILL.md`, `scripts/`, `workflows/`, `tests/`). Recommended over five separate skills because:

* trigger descriptions for about 60 skills already ride in every session and subagent, and five overlapping music skills would compete for the same prompts;
* the reference files load only when read (progressive disclosure);
* `kapell guide <name>` prints the same files from the package, so there is one source and no drift.

### Recipes and their tiers

Recipes take the project root and card paths from `kapell workflow args RECIPE`, which removes the hardcoded `ROOT` in `wf_*.js`. Every `agent()` has a schema, an exclusive file set (one section file per composer, as now) and a tier drawn from `tiers.json`.

| Stage | Tier (default) | Reason |
|---|---|---|
| Materials search, proofs, check, x-ray, splice, assemble, engrave, render, QA thresholds | **Code** (no LLM) | Already deterministic; last time agents drove these by hand inside long contexts |
| Design proposals (N independent), judges, blueprint synthesis | **Opus, high to xhigh** | This is where the Bach, Beethoven or Liszt level of thinking is decided |
| Section composers | **Opus, high** | Musical invention under constraints |
| Seam joiner, fixers per finding | **Opus, medium** | Local and well specified by the finding plus the card |
| Critics (rigour, arc, beauty, idiom) | **Opus, high** | Judgement on musical substance |
| Finding dedupe, severity triage, route-to-section, "needs a second reviewer?" | **Jev** (Score, Noul, Choice) + code | Semantic, narrow, calibrated, $0.04/M tokens (§7) |
| Performance plan authors (per version) | **Opus, medium** (or Sonnet if the rule below is relaxed) | Schema'd JSON with musical intent; linted by `perform` |
| Listening QA read-out, NOTES.md, README, commit messages | **Opus, low** (or Sonnet or Haiku if relaxed) | Mechanical prose from measured data |
| Completeness critic at the end | **Opus, high** | Cheap insurance, one agent |

**A conflict to resolve before build.** `~/.claude/CLAUDE.md` says: "Workers inherit the session model; never downgrade a lane." The user's current request asks where lower reasoning and faster models fit. The recipes do not override the standing rule silently. Instead:

* **Default (compatible with the rule as written):** every LLM lane inherits the session model. Savings come from code replacing LLM steps, Jev (not an LLM lane), smaller contexts, and `effort: low|medium` on mechanical stages. Whether lower *effort* counts as a "downgrade" is for the user to decide.
* **Opt-in:** `tiers.json` has a `"relaxed": false` switch. Setting it to `true` lets the lanes marked "(or Sonnet…)" above run on a cheaper model, and no composing, critic or design lane ever does. Flipping the switch is the user's decision; the kit records which tier ran in every run journal.

---

## 7. Where Jev fits, and the calibration gate

Jev facts from docs.typesafe.ai, read this session:

* **Model and price:** `jev-1.13.0` costs $0.042 per million input tokens; output is free.
* **Limits:** 64k tokens per request; state plus the longest question must fit in 32k; 1,200 requests per minute. Input is text only.
* **Known weaknesses:** it reads literally, and it is weak at math and counting, at indirection, and at large irrelevant states. It does not generate text.
* **Pin the version:** the docs say tuned thresholds should pin the versioned id rather than `jev-latest`, so the kit pins `jev-1.13.0` in `kapell.toml`.

**Use Jev for** narrow semantic decisions over small text states, where calibrated probability and confidence let code decide:

| `kapell jev …` | Question type | State | Typical cost |
|---|---|---|---|
| `triage` | Score (major, minor, nit) + Noul ("does it cite a bar and a concrete fix?") | one critic finding + the x-ray excerpt for its bars (~2k tokens) | 40 findings ≈ 80k tokens ≈ **$0.003** |
| `dedupe` | Noul ("same underlying issue?") on candidate pairs that code has already pre-filtered by section and bar overlap | two findings | pennies |
| `route` | Choice (composer, seam joiner, performance, orchestration, blueprint) | one finding | pennies |
| `rank` | Score on descriptive levels | a **code-computed text profile** of each candidate (contour words, leap list, peak placement, cadence type, dissonance summary), never raw `.ly`; ~1.5k tokens each | 200 candidates ≈ 300k tokens ≈ **$0.013** |
| `gate` | Noul with confidence, e.g. "is this section ready for Opus review?", over an x-ray digest; low confidence goes to Opus | x-ray digest | pennies |

**Do not use Jev for:** composing anything, counting suspensions or parallels (`suspensions.py` does it in 0.2 s), numeric QA thresholds such as loudness, balance or tuning (code), or anything that needs the whole blueprint in its state.

**The gate before Jev enters any loop: calibration.** Jev's musical judgement is unvalidated. `kapell jev calibrate` scores data already on disk and compares the results with the Opus verdicts:

* the 40 findings in `critique_r1.json` (2 critics, 11 major and 29 minor), scored with `triage` against their recorded severities;
* a sample of the 140 lab `.ly` files across `proposal-1..4/lab` and `final-lab`, scored with `rank` against the proofs tables and the judges' choices (whatever the workflow journals still hold);
* **acceptance:** agreement (weighted kappa or AUC) above a threshold the user sets, with abstention when confidence is low.

This takes about one day of work and under $0.10 of Jev input. It decides whether Jev is a triage tool here or stays optional. The calibration runs again as a test whenever the pinned model id changes.

**Preliminary evidence** from a sibling's probe (`docs/kit/jev_probe_summary.json`, uncommitted and still in progress when this was written; the figures may change):

| Probe | Result | What it means |
|---|---|---|
| Musical quality from raw `.ly`, single items | AUC 0.545 (n=40) | Chance level. |
| Musical quality from raw `.ly`, pairwise | accuracy 0.47 to 0.59; picked the first slot 62 to 95% of the time | Chance level with strong position bias. |
| Same pairwise probe on a code-rendered beat grid | accuracy 0.70 (n=56, 95% CI 0.57 to 0.80) | Text representation matters. |
| Routing findings to a fixer role | 0.86 (n=100) | Strong enough to use. |
| Mapping findings to a section | 0.89 (n=98) | Code does this exactly from `bar:beat`. |
| Finding severity | 0.67 with context, 0.61 redacted | Marginal. |

That fits the plan above and sharpens it:

* **ship `route`**;
* **use `triage` only as a prior**, with low-confidence cases sent to Opus;
* **keep `rank` experimental**, fed with grid or profile text, never `.ly`, and always asked in both orders to cancel the slot bias;
* **do section mapping in code.**

The calibration gate stays mandatory.

---

## 8. Repository and template layout

**Separate kit repo** (`kapell`), pushed to whichever GitHub org the user chooses. The current remote, `longevityboris/jurassic-fugue`, is the piece. `fugue-jp` becomes the **first project instance and the regression fixture**. Its files stay where they are, and the kit vendors copies of the tools on day one (no edits to this repo).

```
kapell/                                  (kit repo, uv tool)
  pyproject.toml                         numpy, scipy, soundfile, mido; entry point kapell
  src/kapell/cli.py envelope.py manifest.py config.py project.py status.py
  src/kapell/analysis/  lyparse check harmony suspensions strict grid spanmap quotas roles xray
  src/kapell/materials/ derive solve stretto combo augment matrix profile     (profile = text features for Jev rank)
  src/kapell/piece/     model skeleton cards splice assemble engrave
  src/kapell/perform/   perform articulate presence levels bowing swell lint
  src/kapell/engines/   piano/ organ/ strings/ orchestra/   (each: render, setup, CONTRACT.md, qa)
  src/kapell/mix/       orchestrate mix
  src/kapell/jev/       client questions calibrate
  guides/               method counterpoint orchestration performance recipes  (also the skill references)
  skill/SKILL.md  workflows/*.js  workflows/tiers.json
  templates/piece-<form>/                 kapell.toml, brief.md, folders
  tests/unit tests/golden tests/engines tests/jev

<piece>/                                  (one git repo per piece, created by `kapell new`)
  kapell.toml          form, key plan, meter, voices+ranges, quotas, versions to render, kit version pin, jev model pin
  brief.md
  materials/           materials.ly, materials.json
  design/              blueprint.md (prose), piece.toml (single source: sections, roles, keep, tempo), proofs.json, cards/
  score/               sections/secNN_*.ly, music-voices.ly, out/*.pdf
  performance/<version>/plan.json (+ spec.json for orchestral versions)
  reviews/round-N/*.json
  runs/                journal of workflow run ids, tiers used, and token totals per stage

~/Music/SampleLibraries/                  (unchanged, 15.3 GB; KAPELL_LIB, with PIANO_LIB kept as an alias)
~/Music/kapell-renders/<piece>/<version>/ wav, m4a, stems, render.json (outside git)
```

* `piece.py` is Python-as-data today (a `SECTIONS` list of dicts). The kit turns it into a declarative `piece.toml` validated against a schema, so agents edit data rather than code and `xray` can read roles and quotas.
* The four engines keep their contracts. `audio/organ/CONTRACT.md` already says "This contract is fixed; additions are backward compatible", and the kit extends that rule to piano, strings and orchestra.

---

## 9. Versioning

* **Kit:** semver, plus `breaking_changes` in `agent-info` (as suno does). `kapell.toml` pins `kit = "0.3"`, and `status` warns when the installed kit differs.
* **Engines:** each engine records the SHA-256 of the script that built its derived assets, as the piano setup already does ("render_piano.py refuses" a stale SFZ). `render.json` records the kit version, engine hash and sample-library manifest hash, so a render can be reproduced.
* **Jev:** the model id is pinned per project; recalibration runs on change.
* **Workflows:** recipe files carry `meta.name` with a version suffix; `runs/` records which recipe version and tiers produced each artefact.
* **Skill:** `kapell skill status` compares the installed skill with the package's copy (as `suno skill status` does).

---

## 10. Tests

| Tier | What | Runtime | Source |
|---|---|---|---|
| Unit | `lyparse`, check rules on tiny fixtures (a parallel fifth, an unprepared fourth, an unresolved seventh, a crossing), materials derivation, quota and role checks, envelope and exit codes, agent-info schema | <10 s | new |
| **Golden (The Neighbour)** | `kapell check` on `music-voices.ly` gives **0 errors, 0 parallels, 0 beat-parallels, 0 unjustified** (reproduced this session); suspensions **18 strong / 13 weak**; `xray` reports the bar-54 unresolved seventh and the S2 coverage failure (the new checks must find the known gaps); `skeleton build` reproduces `SK_final.ly` and `plan.json` byte for byte; `engrave` reproduces the committed PDFs (already re-tested byte-identical) | <30 s | fugue-jp as fixture |
| Engines (`--engines`, opt-in) | piano `run_tests.sh` (~25 s), `organ/tests/contract_tests.py`, `orchestration/tests/test_orchestrate.py`, 8-bar render smoke per version with QA thresholds | 2 to 5 min | existing |
| Workflow dry-run | each recipe run with `args.dry = true`: agents replaced by fixture returns, which checks control flow, schemas and tier wiring | <1 min | new |
| Jev calibration | §7, fixed model id, skipped without a key (exit 2) | ~1 min, <$0.10 | new |

`kapell selftest` runs unit and golden tests; the extra tiers run behind flags.

---

## 11. Effort estimate

Estimates, anchored to the measured average of this project: **205M cost-weighted tokens ÷ 155 agents ≈ 1.3M per agent run**. Wall-clock assumes at most 6 parallel lanes with exclusive files (the user's rule).

| # | Component | Main work | Agents | Est. tokens (M) | Risk |
|---|---|---|---|---|---|
| 1 | CLI core | envelope, manifest, config, project discovery, `status`, `doctor`, `skill install`, `guide`, exit codes | 2 | 2.5 | low |
| 2 | Analysis package | make check, harmony, suspensions, strict, grid and spanmap importable (`check.py` reads its file at import); one flag vocabulary; `xray` bundle; **new** unresolved-seventh, role-coverage and quota checks | 3 | 4 | medium: the new checks need musical care |
| 3 | Piece model | `piece.py` to `piece.toml` schema; skeleton, cards, splice, assemble; generalise beyond one piece (forms, voice counts, meters) | 4 | 6 | **high**: the core abstraction |
| 4 | Materials and search | unify 5,141 lines across four proposals (each has its own `mats.py`/`p4.py`) into one materials format and the `find` family; candidate text profiles | 4 | 6 | **high**: four dialects |
| 5 | Perform, render, engines | move perform.py, the performance helpers, 4 engines, orchestrate and mix; path migration (14 files); `setup` wrappers; `render --version` recipes; `engrave --layout all` | 3 | 4 | medium: paths and setup, since the engines already work |
| 6 | Jev module + calibration | client via `akm run`, 5 question sets, calibration harness on the 40 findings and 140 labs | 2 | 2 (+ <$1 Jev) | medium: the result is unknown |
| 7 | Skill + guides | SKILL.md, 5 references distilled from BLUEPRINT, NOTES, sections headers and critique | 2 | 2.5 | low |
| 8 | Workflow recipes | design, compose, review, render and finish, rewritten from `wf_*.js` with `args`, cards, schemas, `tiers.json`, loop guards, dry-run mode | 2 | 3 | medium |
| 9 | Tests | unit, golden, engine flags, dry-run | 2 | 2.5 | low |
| 10 | Review and fix pass | adversarial review of the kit, then fixes | 3 | 4 | low |
| 11 | MCP adapter (deferred, optional) | generated from agent-info | 1 | 1 | low |
| | **Total (without 11)** | | **~27** | **~37M** | |

**Wall-clock:** about 6 to 9 hours in two waves. Wave A runs 1, 2, 5 and 7 in parallel; wave B runs 3, 4, 6 and 8 once the core and analysis APIs exist; then 9 and 10.

**What the next piece should cost** (estimate, and reasoning per line). Of the 205M, most engine-building is one-time: the piano and quartet engines inside the 68M line, the organ, orchestra and mix engines inside the 31M line, and the 14M of finishing work. That is about 60 to 80M that will not recur. The recurring lines (design and judging, composing 38M, recordings 24M, coordination 10M, critics 5M, a wasted first attempt 8M) come to about 125 to 145M. With the kit:

* **Composing and review:** section cards and digests cut context per turn to roughly a third, and code runs the check loops. 38M becomes about **12 to 18M**.
* **Design:** deterministic `find` and `prove` replace agent-driven lab exploration, though the design lanes stay at full Opus. Their share of the 68M becomes about **10 to 15M**.
* **Recordings:** plan authors plus `render` and `qa` in code, in place of agents driving engines. 24M becomes about **3 to 5M**.
* **Coordination and restarts:** `status` plus resume, in place of re-reading the repository. 10 + 8M becomes about **2 to 3M**.
* **Target for piece #2: about 30 to 45M cost-weighted tokens and 5 to 8 hours**, against 205M and about 21 hours. The first new piece is the real measurement; `runs/` records tokens per stage so the estimate can be checked.

---

## 12. Build order and open decisions

1. Create the kit repo; vendor tools as-is; CLI core; golden tests pass on fugue-jp **before** any refactor (a safety net).
2. Analysis package and `xray` with the three new checks; confirm they flag bar 54 and S2 on the fixture.
3. Piece model and cards; materials and `find`; perform and render wrappers; path migration.
4. Jev module and calibration. **Decision point:** keep Jev in the review loop only if it passes.
5. Skill, recipes and tiers; workflow dry-run tests; review pass.
6. Pilot a short new piece (a 3-voice fugue or chorale prelude of about 1 minute) end to end and measure tokens per stage.

**Decisions that belong to the user:**

* whether to relax "never downgrade a lane" for the marked mechanical lanes (§6);
* the Jev acceptance threshold (§7);
* the GitHub org for the kit repo;
* whether any non-Claude-Code client (Desktop, claude.ai, a remote session) needs the kit. That alone would justify the MCP adapter.
