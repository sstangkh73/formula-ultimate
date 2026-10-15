# LT-015: GripMap: An Efficient, Spatially Resolved Constraint Framework for Offline and Online Trajectory Planning in Autonomous Racing

Thai companion: `LT-015_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Frederik Werner, Ann-Kathrin Schwehn, M. Lienkamp, Johannes Betz |
| Year | 2025 |
| Venue | 2025 IEEE Intelligent Vehicles Symposium (IV) |
| DOI | Not recorded |
| arXiv | 2504.12115 |
| Canonical record | [https://arxiv.org/abs/2504.12115](https://arxiv.org/abs/2504.12115) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-015_Werner2025_gripmap-an-efficient-spatially-resolved-constraint.pdf) |
| Source SHA-256 | `e2fa016e661797d87b4ac194823ae3d51afb23bd53ed4613803f8cfba85e138c` |
| Full-text coverage | 9/9 pages (100.00%); 6,963 extracted words |

## Research question

How does GripMap: An Efficient, Spatially Resolved Constraint Framework for Offline and Online Trajectory Planning in Autonomous Racing formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were gripmap, vehicle, grip, racing, constraints, autonomous, trajectory, planning. The paper-specific method or result selected for transfer review is: **Spatially resolved grip constraints for planning**.

## Principal findings

- **Paper finding (conservative paraphrase):** Spatially resolved grip constraints for planning
- **Reviewer interpretation:** a data structure for track-position-dependent grip
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a data structure for track-position-dependent grip This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Spatially resolved grip constraints for planning** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a bounded diagnostic pilot from 'Spatially resolved grip constraints for planning' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 44,717 characters, 6,963 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 2, 3, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
