# AR-025: Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling

Thai companion: `AR-025_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Thomas Herrmann, Alexander Wischnewski, Leonhard Hermansdorfer, Johannes Betz, Markus Lienkamp |
| Year | 2021 |
| Venue | IEEE Transactions on Intelligent Vehicles |
| DOI | 10.1109/tiv.2020.3047858 |
| arXiv | 2012.13586 |
| Canonical record | [https://doi.org/10.1109/tiv.2020.3047858](https://doi.org/10.1109/tiv.2020.3047858) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-025_Herrmann2021_real-time-adaptive-velocity-optimization-for-auton.pdf) |
| Source SHA-256 | `1a41bb54b79ca4e09aa1f8a5327bdbf50acbccdac3c9604f2f22f38f7b501ead` |
| Full-text coverage | 13/13 pages (100.00%); 11,640 extracted words |

## Research question

How does Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were optimization, velocity, sglo, acceleration, race, vehicle, path, limits. The paper-specific method or result selected for transfer review is: **Real-time velocity planning with energy and friction limits on an electric racecar**.

## Principal findings

- **Paper finding (conservative paraphrase):** Real-time velocity planning with energy and friction limits on an electric racecar
- **Reviewer interpretation:** a driver component for energy-limited races
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a driver component for energy-limited races This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Real-time velocity planning with energy and friction limits on an electric racecar** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Real-time velocity planning with energy and friction limits on an electric racecar' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 13 pages, 69,706 characters, 11,640 words.
- Pages with substantial extractable text: 13/13.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
