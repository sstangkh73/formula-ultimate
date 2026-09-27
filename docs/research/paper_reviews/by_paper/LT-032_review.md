# LT-032: A Sequential Convex Programming Approach to Free-trajectory Minimum-lap-time Optimization of Racing Cars

Thai companion: `LT-032_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Erik van den Eshof, Wytze de Vries, Jorn van Kampen, Mauro Salazar |
| Year | 2025 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2511.13522 |
| Canonical record | [https://arxiv.org/abs/2511.13522](https://arxiv.org/abs/2511.13522) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-032_Eshof2025_a-sequential-convex-programming-approach-to-free-t.pdf) |
| Source SHA-256 | `25636c7321c8ac0d4742ace538a316c70d0e82abaad8ca3d3479bec7216c7f1a` |
| Full-text coverage | 8/8 pages (100.00%); 5,958 extracted words |

## Research question

How does A Sequential Convex Programming Approach to Free-trajectory Minimum-lap-time Optimization of Racing Cars formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were sref, trajectory, racing, model, optimization, vehicle, control, problem. The paper-specific method or result selected for transfer review is: **Recent efficient free-trajectory lap-time optimisation**.

## Principal findings

- **Paper finding (conservative paraphrase):** Recent efficient free-trajectory lap-time optimisation
- **Reviewer interpretation:** relevant to the cost of giving every candidate an optimised driver
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to the cost of giving every candidate an optimised driver This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Recent efficient free-trajectory lap-time optimisation** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Recent efficient free-trajectory lap-time optimisation' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 35,846 characters, 5,958 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
