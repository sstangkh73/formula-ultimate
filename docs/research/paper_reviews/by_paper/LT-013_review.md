# LT-013: Online Time-Optimal Trajectory Planning on Three-Dimensional Race Tracks

Thai companion: `LT-013_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Matthias Rowold, Levent Ögretmen, Ulf Kasolowsky, B. Lohmann |
| Year | 2023 |
| Venue | 2023 IEEE Intelligent Vehicles Symposium (IV) |
| DOI | Not recorded |
| arXiv | 2304.10954 |
| Canonical record | [https://arxiv.org/abs/2304.10954](https://arxiv.org/abs/2304.10954) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-013_Rowold2023_online-time-optimal-trajectory-planning-on-three-d.pdf) |
| Source SHA-256 | `8a9979bec19bedd2d4ac5ffa005147f4b04943bb551341f9cf15c7380c7af380` |
| Full-text coverage | 9/9 pages (100.00%); 6,938 extracted words |

## Research question

How does Online Time-Optimal Trajectory Planning on Three-Dimensional Race Tracks formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were racing, line, planning, velocity, global, local, track, speed. The paper-specific method or result selected for transfer review is: **Point-mass time-optimal planning on 3D tracks with open code**.

## Principal findings

- **Paper finding (conservative paraphrase):** Point-mass time-optimal planning on 3D tracks with open code
- **Reviewer interpretation:** a cheap lower-fidelity rung of the ladder
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a cheap lower-fidelity rung of the ladder This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Point-mass time-optimal planning on 3D tracks with open code** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a bounded diagnostic pilot from 'Point-mass time-optimal planning on 3D tracks with open code' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 39,820 characters, 6,938 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 2, 5, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
