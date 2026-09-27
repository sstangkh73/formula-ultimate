# LT-002: Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification

Thai companion: `LT-002_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Giacomo Perantoni, David J. N. Limebeer |
| Year | 2015 |
| Venue | Journal of Dynamic Systems, Measurement, and Control |
| DOI | 10.1115/1.4028253 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1115/1.4028253](https://doi.org/10.1115/1.4028253) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-002_Perantoni2015_optimal-control-of-a-formula-one-car-on-a-three-di.pdf) |
| Source SHA-256 | `13a940df8476727bec322b1a16fea8c6e70af1f93078f551264105695bc8012c` |
| Full-text coverage | 22/22 pages (100.00%); 9,868 extracted words |

## Research question

How does Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were road, optimal, track, ribbon, control, boundary, used, curvature. The paper-specific method or result selected for transfer review is: **Builds and identifies a 3D track ribbon (curvature, elevation, banking) from data**.

## Principal findings

- **Paper finding (conservative paraphrase):** Builds and identifies a 3D track ribbon (curvature, elevation, banking) from data
- **Reviewer interpretation:** the guide for replacing our synthetic tracks
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the guide for replacing our synthetic tracks This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Builds and identifies a 3D track ribbon (curvature, elevation, banking) from data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Builds and identifies a 3D track ribbon (curvature, elevation, banking) from data' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 22 pages, 56,635 characters, 9,868 words.
- Pages with substantial extractable text: 22/22.
- High-information cue pages sampled from across the paper: 2, 3, 4, 10, 11, 12, 13, 15. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
