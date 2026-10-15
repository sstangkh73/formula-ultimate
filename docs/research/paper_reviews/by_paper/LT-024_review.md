# LT-024: Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions

Thai companion: `LT-024_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Camiel Cartignij, Mauro Salazar |
| Year | 2023 |
| Venue | Vehicle Power and Propulsion Conference |
| DOI | Not recorded |
| arXiv | 2311.03545 |
| Canonical record | [https://arxiv.org/abs/2311.03545](https://arxiv.org/abs/2311.03545) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-024_Cartignij2023_time-optimal-design-and-control-of-electric-race-c.pdf) |
| Source SHA-256 | `840b73c28b9d0902631db5366a01969d9131fc6effec5ba06cf9be0bc29ea5e3` |
| Full-text coverage | 4/4 pages (100.00%); 3,588 extracted words |

## Research question

How does Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were control, problem, optimization, design, electric, race, algorithm, time. The paper-specific method or result selected for transfer review is: **Compares fixed, CVT and multi-speed transmissions with jointly optimised control**.

## Principal findings

- **Paper finding (conservative paraphrase):** Compares fixed, CVT and multi-speed transmissions with jointly optimised control
- **Reviewer interpretation:** an architecture choice evaluated fairly
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an architecture choice evaluated fairly This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Compares fixed, CVT and multi-speed transmissions with jointly optimised control** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Compares fixed, CVT and multi-speed transmissions with jointly optimised control' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 4 pages, 21,350 characters, 3,588 words.
- Pages with substantial extractable text: 4/4.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
