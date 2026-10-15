# LT-010: A Curvilinear Abscissa Approach for the Lap Time Optimization of Racing Vehicles

Thai companion: `LT-010_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | R. Lot, F. Biral |
| Year | 2014 |
| Venue | IFAC Proceedings Volumes |
| DOI | 10.3182/20140824-6-za-1003.00868 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.3182/20140824-6-za-1003.00868](https://doi.org/10.3182/20140824-6-za-1003.00868) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-010_Lot2014_a-curvilinear-abscissa-approach-for-the-lap-time-o.pdf) |
| Source SHA-256 | `93ca3344cac924334fc4970bf416489466862bdbe7bbe162d2a83a8078575aaa` |
| Full-text coverage | 7/7 pages (100.00%); 5,918 extracted words |

## Research question

How does A Curvilinear Abscissa Approach for the Lap Time Optimization of Racing Vehicles formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were vehicle, equations, time, road, problem, control, model, minimum. The paper-specific method or result selected for transfer review is: **Curvilinear-coordinate formulation used by most modern lap-time solvers**.

## Principal findings

- **Paper finding (conservative paraphrase):** Curvilinear-coordinate formulation used by most modern lap-time solvers
- **Reviewer interpretation:** needed to pose our track-relative dynamics
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** needed to pose our track-relative dynamics This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Curvilinear-coordinate formulation used by most modern lap-time solvers** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a bounded diagnostic pilot from 'Curvilinear-coordinate formulation used by most modern lap-time solvers' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 7 pages, 33,563 characters, 5,918 words.
- Pages with substantial extractable text: 7/7.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
