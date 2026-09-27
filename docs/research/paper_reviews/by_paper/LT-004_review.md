# LT-004: Minimum time optimal control simulation of a GP2 race car

Thai companion: `LT-004_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Nicola Dal Bianco, Roberto Lot, Marco Gadola |
| Year | 2018 |
| Venue | Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering |
| DOI | 10.1177/0954407017728158 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1177/0954407017728158](https://doi.org/10.1177/0954407017728158) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-004_Bianco2018_minimum-time-optimal-control-simulation-of-a-gp2-r.pdf) |
| Source SHA-256 | `768e8d5d13f396e5eaa5f80dea2fb69cf3ce246a92014cc915c4b33602843d32` |
| Full-text coverage | 27/27 pages (100.00%); 10,936 extracted words |

## Research question

How does Minimum time optimal control simulation of a GP2 race car formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, mathematical/formal evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were tyre, wheel, front, rear, suspension, model, control, optimal. The paper-specific method or result selected for transfer review is: **14-DOF car, nonlinear tyres, ride-height aero and telemetry comparison**.

## Principal findings

- **Paper finding (conservative paraphrase):** 14-DOF car, nonlinear tyres, ride-height aero and telemetry comparison
- **Reviewer interpretation:** the nearest public coupled-model target
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the nearest public coupled-model target This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **14-DOF car, nonlinear tyres, ride-height aero and telemetry comparison** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in '14-DOF car, nonlinear tyres, ride-height aero and telemetry comparison' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 27 pages, 62,571 characters, 10,936 words.
- Pages with substantial extractable text: 27/27.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 13, 17. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
