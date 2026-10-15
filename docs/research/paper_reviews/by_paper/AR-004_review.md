# AR-004: Autonomous Racing using Learning Model Predictive Control

Thai companion: `AR-004_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ugo Rosolia, Ashwin Carvalho, F. Borrelli |
| Year | 2016 |
| Venue | American Control Conference |
| DOI | Not recorded |
| arXiv | 1610.06534 |
| Canonical record | [https://arxiv.org/abs/1610.06534](https://arxiv.org/abs/1610.06534) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-004_Rosolia2016_autonomous-racing-using-learning-model-predictive.pdf) |
| Source SHA-256 | `ed4c3e160f7f6570c1706f7112a4fb9911277df324c0a3d68a8afc2b0f274860` |
| Full-text coverage | 8/8 pages (100.00%); 5,469 extracted words |

## Research question

How does Autonomous Racing using Learning Model Predictive Control combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, simulation/numerical evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were time, iteration, control, vehicle, model, problem, controller, system. The paper-specific method or result selected for transfer review is: **Iterative learning MPC improves lap time from previous laps**.

## Principal findings

- **Paper finding (conservative paraphrase):** Iterative learning MPC improves lap time from previous laps
- **Reviewer interpretation:** a controller that approaches each vehicle's limit
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a controller that approaches each vehicle's limit This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Iterative learning MPC improves lap time from previous laps** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Iterative learning MPC improves lap time from previous laps' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 29,026 characters, 5,469 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 5, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
