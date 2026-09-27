# AR-002: Optimization-Based Autonomous Racing of 1:43 Scale RC Cars

Thai companion: `AR-002_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Alexander Liniger, A. Domahidi, M. Morari |
| Year | 2015 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 1711.07300 |
| Canonical record | [https://arxiv.org/abs/1711.07300](https://arxiv.org/abs/1711.07300) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-002_Liniger2015_optimization-based-autonomous-racing-of-1-43-scale.pdf) |
| Source SHA-256 | `bb5d2330f57ab2b703429d12471854e14136787bfb232b7577e1310791c6103c` |
| Full-text coverage | 20/20 pages (100.00%); 11,975 extracted words |

## Research question

How does Optimization-Based Autonomous Racing of 1:43 Scale RC Cars combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, mathematical/formal evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were control, path, model, time, controller, problem, horizon, trajectory. The paper-specific method or result selected for transfer review is: **Model predictive contouring control for racing**.

## Principal findings

- **Paper finding (conservative paraphrase):** Model predictive contouring control for racing
- **Reviewer interpretation:** an implementable controller baseline with explicit horizon and actuator limits
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an implementable controller baseline with explicit horizon and actuator limits This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Model predictive contouring control for racing** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Model predictive contouring control for racing' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 20 pages, 68,772 characters, 11,975 words.
- Pages with substantial extractable text: 20/20.
- High-information cue pages sampled from across the paper: 2, 3, 10, 11, 15, 16, 18. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
