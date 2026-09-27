# AR-021: Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing

Thai companion: `AR-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Giovanni Lambertini, M. Pini, Nicola Musiu, Ayoub Raji, Francesco Iacovacci, Marko Bertogna |
| Year | 2026 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2609.12292 |
| Canonical record | [https://arxiv.org/abs/2609.12292](https://arxiv.org/abs/2609.12292) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-021_Lambertini2026_mission-performance-automatic-and-adaptive-race-pa.pdf) |
| Source SHA-256 | `964d1b3baad2ad83c62fa2a822408f91b18bcd50777928d3081691dc0ba86f64` |
| Full-text coverage | 8/8 pages (100.00%); 6,415 extracted words |

## Research question

How does Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were performance, vehicle, race, tire, parameters, lateral, autonomous, longitudinal. The paper-specific method or result selected for transfer review is: **Adaptive pace progression towards the limit**.

## Principal findings

- **Paper finding (conservative paraphrase):** Adaptive pace progression towards the limit
- **Reviewer interpretation:** relevant to safely finding each candidate's achievable pace
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to safely finding each candidate's achievable pace This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Adaptive pace progression towards the limit** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Adaptive pace progression towards the limit' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 37,864 characters, 6,415 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
