# AR-027: Unifying F1TENTH Autonomous Racing: Survey, Methods and Benchmarks

Thai companion: `AR-027_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | B. D. Evans, Raphael Trumpp, Marco Caccamo, H. W. Jordaan, H. Engelbrecht |
| Year | 2024 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2402.18558 |
| Canonical record | [https://arxiv.org/abs/2402.18558](https://arxiv.org/abs/2402.18558) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-027_Evans2024_unifying-f1tenth-autonomous-racing-survey-methods.pdf) |
| Source SHA-256 | `040b8fae665613c2efdae1992e0df38b95f3fee6ceca7ac0b481897da0ab269d` |
| Full-text coverage | 12/12 pages (100.00%); 10,198 extracted words |

## Research question

How does Unifying F1TENTH Autonomous Racing: Survey, Methods and Benchmarks combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were learning, control, racing, autonomous, vehicle, f1tenth, planning, speed. The paper-specific method or result selected for transfer review is: **Benchmarks of racing planners and controllers on a common platform**.

## Principal findings

- **Paper finding (conservative paraphrase):** Benchmarks of racing planners and controllers on a common platform
- **Reviewer interpretation:** a reference for fair controller comparisons
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a reference for fair controller comparisons This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Benchmarks of racing planners and controllers on a common platform** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Benchmarks of racing planners and controllers on a common platform' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 12 pages, 63,563 characters, 10,198 words.
- Pages with substantial extractable text: 12/12.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
