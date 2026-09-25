# D. Jev calibration probe: which kit decisions can a System One model own?

The probe tested TypeSafe's Jev (`jev-1.13.0`, pinned) on 672 labelled decisions drawn from The Neighbour's own history: git revisions, deliberately corrupted passages, 100 reviewer findings, and the four design proposals. It cost **$0.021** in total: 472 requests, 490,555 input tokens, median latency 0.63 s, p95 1.88 s, and 79 s of wall time at 8 parallel requests, including the local check.py and grid.py runs.

**Verdict in one line:** Jev is a good dispatcher and a poor musician. It can route and triage review findings. It cannot tell better counterpoint from worse, whether from LilyPond or from a named-pitch grid. On music it mostly says so itself, with low confidence.

Script: `docs/kit/jev_probe.py`. Run it with `akm run --only TYPESAFE_API_KEY -- python3 docs/kit/jev_probe.py`; the key never appears in any file. Raw answers are in `jev_probe_results.jsonl`, the summary in `jev_probe_summary.json`, and item provenance (commit SHAs, corruption sites, check.py counts) in `jev_probe_items.json`.

## Test set

| Task | Items | Label source | Decisions |
|---|---|---|---|
| T1 before/after revisions | 17 section revisions whose notes changed (git history of `ricercar/score/sections/*.ly`, `%` headers stripped so the rationale can't leak) | the reviewers accepted the later version | 17 × 2 orders × 2 representations = 68 |
| T2 corruptions | 28: 10 parallel fifths against the bass, 10 strong-beat semitone clashes, 8 wrong notes in a subject entry (4 entries × 2) | built in code; every parallel or clash is confirmed by check.py (parallels or unjustified count rises, spelling matched to the section) | 112 pairwise + 80 single-passage |
| T3 finding triage | 100 of the 119 major/minor findings in the workflow journals (all 30 render-listen findings, plus 50 counterpoint/music review and 20 panel findings sampled at random) | reviewer severity; source workflow (route); section from `where` | 100 × (severity, route, section) full text + 100 × severity on a redacted first sentence = 400 |
| T4 proposals | 4 DESIGN.md files (first 6,000 characters), all 6 pairs in both orders | judges' totals #2 23, #1 22.5, #3 21.5, #4 18 | 12 |

The two representations were `lily`, the raw LilyPond voices (`bes'2. bes'8 a'8 |`), and `grid`, the project's own grid.py output: one row per eighth, S A T B pitch names, and a music21 chord name. Pairwise questions were asked in both orders to measure position bias.

## Results

| Task | n | Accuracy (95% CI) | Baseline | Position bias (picks slot 1) | Both orders right |
|---|---|---|---|---|---|
| T1 revisions, lily | 34 | **0.47** (0.32-0.63) | 0.50 chance | 0.62 | 5/17 |
| T1 revisions, grid | 34 | **0.56** (0.40-0.71) | 0.50 | 0.71 | 6/17 |
| T2 pairwise, lily (all kinds) | 56 | 0.59 (0.46-0.71) | 0.50 | **0.84** (0.95 on parallels and clashes) | 6/28 |
| T2 pairwise, grid (all kinds) | 56 | **0.70** (0.57-0.80) | 0.50 | 0.55 | 16/28 |
| - parallel fifths, grid | 20 | 0.70 | check.py: 1.00 | 0.50 | 6/10 |
| - strong-beat clash, grid | 20 | 0.75 | check.py: 1.00 | 0.55 | 7/10 |
| - wrong subject note, grid / lily | 16 / 16 | 0.63 / 0.69 | a pitch diff against the subject: 1.00 | 0.63 / 0.56 | 3/8 / 4/8 |
| T2 single passage "contains an error?" (Noul) | 40 + 40 | AUC **0.54** (lily 0.545, grid 0.54) | 0.50 | - | mean p(error) 0.54 corrupted vs 0.53 original |
| T3 severity, full text | 100 | 0.67 (0.57-0.75) | **0.68** (always "minor") | picks major 63% vs 32% true | - |
| T3 severity, redacted first sentence | 100 | 0.61 (0.51-0.70) | 0.68 | picks major 49% | - |
| T3 route (fix the notes vs fix the performance) | 100 | **0.86** (0.78-0.92) | 0.70 | - | - |
| T3 section (7-way, bar table in the question) | 98 | **0.89** (0.81-0.94) | regex on the first bar number: 0.89 on 91/98 | - | - |
| T4 proposals, pairwise | 12 | 0.75 (0.47-0.91) | 0.50 | 0.42 | - |

Reading the table:

- **T1 (the decision that matters most for composing) is at chance** in both representations, and Jev picked the same pair differently in the two orders 6-7 times out of 17. Judging whether a reviewer's revision improved the counterpoint is beyond it.
- **Representation matters.** With raw LilyPond, Jev fell back on "version 1" (95% on parallels and clashes). The named-pitch grid removed that bias and raised T2 from 0.59 to 0.70. Any music question sent to Jev should use the grid, never LilyPond.
- **It detects errors only when it has a reference.** Pairwise on the grid reaches 0.70. Asked whether one passage contains an error, it is at chance (AUC 0.54). A kit has no reference copy when checking new music, so this rules out Jev as a checker. check.py already catches 100% of these corruptions, by construction and for free.
- **Severity:** Jev over-calls "major" and loses to the always-minor baseline (0.67 vs 0.68). But the errors all go one way. It called 31 of the 32 real majors major (recall 0.97). Of the 37 findings it called minor, 36 were minor (0.97 negative predictive value). So it works as a recall-first screen, not as a classifier. Redacting the rhetoric (first sentence only, words like major/must/rule/weakest masked) cost 6 points and halved the over-calling: part of the signal is the reviewer's tone, not the music.
- **Route:** all 30 render-listen findings went to "performance". 14 review/panel findings also went to "performance". In the ones I read, the finding is really about performance: piano hand spans at 13:4, the missing damper pedal in plan.json, perform.py playing F5 legato through a written lift. So 0.86 is a floor, limited by label noise.
- **Section lookup:** Jev ties the regex (0.89 each). Regex first with Jev as the fallback also scores 87/98. The misses are label noise (a finding filed under sec06 that talks about bar 55). Code owns this.
- **T4:** Jev's soft ranking was #1 > #3 > #2 > #4 against the judges' #2 > #1 > #3 > #4 (Spearman 0.4, n = 4). It placed the clear loser (#4, 18) last. The top three are within 1.5 judge points, which is inside anyone's noise. It is judging design prose, not notes.

## Calibration

Reliability by Jev's own `confidence` (Choice answers):

| Confidence | Notation tasks (T1+T2 pairwise), n | acc | Text triage (T3 severity/route/section), n | acc |
|---|---|---|---|---|
| 0.00-0.25 | 79 | 0.58 | 21 | 0.52 |
| 0.25-0.50 | 61 | 0.56 | 16 | 0.62 |
| 0.50-0.75 | 33 | 0.64 | 30 | 0.60 |
| 0.75-0.90 | 7 | 0.86 | 38 | 0.66 |
| 0.90-1.00 | 0 | - | 193 | **0.91** |

Pooled expected calibration error (on the top probability) is 0.10.

- **On music, Jev knows it does not know.** 78% of notation answers had confidence below 0.5, and none reached 0.9. The 7 answers at 0.75 or above were 86% right, and the 6 grid-pairwise answers at 0.5 or above were all right. No confident wrong answers on notes, so a gate can't be fooled, but coverage is tiny: 4% of notation decisions clear 0.75.
- **On text triage, confidence is usable but not linear.** Everything below 0.9 is 52-66% accurate. At 0.9 or above it is 91% accurate and covers 84% of route and section decisions. The gates below are set from this table, not from the docs' default of 0.5.

Accuracy and coverage at each gate threshold:

| Decision | conf ≥ 0 | ≥ 0.5 | ≥ 0.75 | ≥ 0.9 |
|---|---|---|---|---|
| Route | 0.86 @ 100% | 0.87 @ 95% | 0.89 @ 93% | **0.90 @ 84%** |
| Section | 0.89 @ 100% | 0.90 @ 98% | 0.91 @ 91% | **0.96 @ 84%** |
| Severity (full text) | 0.67 @ 100% | 0.71 @ 70% | 0.76 @ 49% | 0.78 @ 27% |
| Pairwise notes, grid | 0.70 @ 100% | 1.00 @ 11% | - | - |

## Verdict for the kit

**Jev can own these (cheap, fast, good enough; code acts on the answer):**

1. **Route each review or listen finding to its fixing lane:** composer (notes), performance (plan.json, perform.py), or render/mix. Act automatically at confidence ≥ 0.9 (0.90 on 84% of findings, with the misses mostly mislabelled). Below that, send to the orchestrator. This replaces an LLM turn that reads every finding. At about 1k tokens a finding, a 120-finding review round costs about $0.005 and takes under a second when parallelised.
2. **Park minor findings.** When Jev says "minor" on the full text, the kit can defer the finding to a batch or backlog pass. That held for 36 of 37 (NPV 0.97, 37% of findings). Everything Jev calls major goes to a real reviewer, because its "major" is only 49% precise.
3. **Glue decisions of the same shape:** dedupe "is finding A the same issue as B?", "does this agent report claim PASS?", "is this commit message about notes or the header only?", and choosing which skill or lane runs next. These are closed-set judgments over prose, the task class where it scored 0.86-0.96 at high confidence. (Inferred from T3; not measured one by one.)

**Gate these (threshold, then escalate):**

4. **Severity ranking** when a round has too many findings to fix: use P(major) only to order the queue, with the probe's rule (confidence ≥ 0.9 → 0.78; otherwise escalate). Never let it drop a finding it calls major.
5. **Design-stage pruning:** pairwise over proposal prose, both orders, soft wins summed. Use it only to drop a clear loser before the expensive judge panel (it found #4). Never use it to pick the winner.
6. **Section/bar lookup,** only as a fallback when the regex finds no bar number, and only at confidence ≥ 0.9 (0.96).

**Jev should not touch:**

7. **Whether a revision is musically better** (T1: 0.47-0.56, flips with order). This is the core of the composing loop. Keep Opus reviewers here, possibly with a Sonnet pre-pass, but not Jev.
8. **Error detection in new music** (single-passage AUC 0.54). Parallels, dissonance treatment, suspensions and subject integrity belong to check.py, strict.py, suspensions.py and a pitch diff against the subject: deterministic, exact and free. If Jev ever sees notes, use the grid representation, both orders, and treat confidence < 0.5 as "no answer".
9. **Anything numeric or positional:** bar arithmetic, counting suspensions, timing, loudness (Jev's documented weak points, and the kit already has tools for them).
10. **Generation of any kind** (notes, fixes, headers). Jev returns only choices, scores and probabilities.

## What this means for cost

The 205M cost-weighted tokens of The Neighbour went into composing, joining, reviewing and render engines. Jev cannot take any of those. What it can take is the orchestration glue: routing, triage, parking, dedupe, pass/fail reading. Those are the steps that made long agents re-read big contexts (97% of raw tokens were cache re-reads). Moving them to Jev (about $0.00004 a decision) and the musical checks to the deterministic tools shrinks what each Opus agent has to read. It does not replace the Opus judgment the music needs. Smaller LLMs (Sonnet/Haiku) for the middle tier were not tested here; they are the next probe.

## Caveats

- Labels are one reviewer's call. Some T1 revisions are sideways moves (header or balance), so a perfect judge would not reach 1.0.
- T2 corruptions are check.py-detectable by construction, which is the point: code already owns them.
- The route labels come from the source workflow and are noisy (see above).
- Sample sizes are small: T1 n = 17 pairs; T4 n = 4 proposals and 12 comparisons. The CIs in the results table are Wilson 95%.
- One model version (`jev-1.13.0`). Re-run the probe before trusting a new alias; `--summarize` recomputes from the JSONL without API calls.
