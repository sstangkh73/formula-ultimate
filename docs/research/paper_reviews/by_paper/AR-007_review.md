# AR-007: TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge

Thai companion: `AR-007_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Johannes Betz, Tobias Betz, F. Fent, Maximilian Geisslinger, Alexander Heilmeier, Leonhard Hermansdorfer, T. Herrmann, Sebastian Huch, Phillip Karle, M. Lienkamp, B. Lohmann, Felix Nobis, Levent Ogretmen, Matthias Rowold, Florian Sauerbeck, Tim Stahl, Rainer Trauth, Frederik Werner, Alexander Wischnewski |
| Year | 2023 |
| Venue | J. Field Robotics |
| DOI | Not recorded |
| arXiv | 2205.15979 |
| Canonical record | [https://arxiv.org/abs/2205.15979](https://arxiv.org/abs/2205.15979) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-007_Betz2023_tum-autonomous-motorsport-an-autonomous-racing-sof.pdf) |
| Source SHA-256 | `92c1b50e8cf6f71dde574a9b08dd30ac6fd3f27e3d0039bf92e1432c867d6f92` |
| Full-text coverage | 27/27 pages (100.00%); 23,556 extracted words |

## Research question

How does TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were vehicle, autonomous, software, wiley, race, object, racing, based. The paper-specific method or result selected for transfer review is: **Complete open autonomous racing stack with planning and control**.

## Principal findings

- **Paper finding (conservative paraphrase):** Complete open autonomous racing stack with planning and control
- **Reviewer interpretation:** reusable components for a driver baseline
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** reusable components for a driver baseline This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Complete open autonomous racing stack with planning and control** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Complete open autonomous racing stack with planning and control' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 27 pages, 146,876 characters, 23,556 words.
- Pages with substantial extractable text: 27/27.
- High-information cue pages sampled from across the paper: 2, 7, 8, 10, 14, 18, 19, 20. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
