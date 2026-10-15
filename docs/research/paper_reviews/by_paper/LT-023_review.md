# LT-023: Minimum-lap-time Control Strategies for All-wheel Drive Electric Race Cars via Convex Optimization

Thai companion: `LT-023_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Stan Broere, Jorn van Kampen, Mauro Salazar |
| Year | 2022 |
| Venue | European Control Conference |
| DOI | Not recorded |
| arXiv | 2111.04650 |
| Canonical record | [https://arxiv.org/abs/2111.04650](https://arxiv.org/abs/2111.04650) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-023_Broere2022_minimum-lap-time-control-strategies-for-all-wheel.pdf) |
| Source SHA-256 | `f8b2e98f79ad97735392575fd23489bc8e8197ad7856487cbcbcce119d644d46` |
| Full-text coverage | 9/9 pages (100.00%); 7,435 extracted words |

## Research question

How does Minimum-lap-time Control Strategies for All-wheel Drive Electric Race Cars via Convex Optimization formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were control, electric, power, race, battery, convex, energy, vehicle. The paper-specific method or result selected for transfer review is: **Per-tyre grip limits with all-wheel drive in a convex lap formulation**.

## Principal findings

- **Paper finding (conservative paraphrase):** Per-tyre grip limits with all-wheel drive in a convex lap formulation
- **Reviewer interpretation:** relevant to independent-wheel torque allocation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to independent-wheel torque allocation This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Per-tyre grip limits with all-wheel drive in a convex lap formulation** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Per-tyre grip limits with all-wheel drive in a convex lap formulation' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 41,128 characters, 7,435 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
