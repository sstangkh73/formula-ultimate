# AR-009: AMZ Driverless: The Full Autonomous Racing System

Thai companion: `AR-009_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Juraj Kabzan, M. I. Valls, Victor Reijgwart, Hubertus Franciscus Cornelis Hendrikx, Claas Ehmke, Manish Prajapat, Andreas Bühler, N. Gosala, Mehak Gupta, R. Sivanesan, Ankit Dhall, Eugenio Chisari, Napat Karnchanachari, Sonja Brits, Manuel Dangel, Inkyu Sa, Renaud Dubé, A. Gawel, Mark Pfeiffer, Alexander Liniger, J. Lygeros, R. Siegwart |
| Year | 2020 |
| Venue | J. Field Robotics |
| DOI | Not recorded |
| arXiv | 1905.05150 |
| Canonical record | [https://arxiv.org/abs/1905.05150](https://arxiv.org/abs/1905.05150) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-009_Kabzan2020_amz-driverless-the-full-autonomous-racing-system.pdf) |
| Source SHA-256 | `9827d916c735ff865147218933e7f153c94933031e66a1393de25f9f50f5a6ca` |
| Full-text coverage | 40/40 pages (100.00%); 19,235 extracted words |

## Research question

How does AMZ Driverless: The Full Autonomous Racing System combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were cones, cone, figure, model, track, system, used, estimation. The paper-specific method or result selected for transfer review is: **Complete Formula Student driverless system with vehicle models and MPC**.

## Principal findings

- **Paper finding (conservative paraphrase):** Complete Formula Student driverless system with vehicle models and MPC
- **Reviewer interpretation:** a well-documented reference implementation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a well-documented reference implementation This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Complete Formula Student driverless system with vehicle models and MPC** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Complete Formula Student driverless system with vehicle models and MPC' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 40 pages, 114,436 characters, 19,235 words.
- Pages with substantial extractable text: 40/40.
- High-information cue pages sampled from across the paper: 2, 4, 8, 11, 13, 16, 18, 19. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
