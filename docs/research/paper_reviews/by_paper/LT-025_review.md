# LT-025: Time-optimal Control Strategies for Electric Race Cars with Different Transmission Technologies

Thai companion: `LT-025_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | O. Borsboom, C. A. Fahdzyana, Mauro Salazar, T. Hofman |
| Year | 2020 |
| Venue | Vehicle Power and Propulsion Conference |
| DOI | Not recorded |
| arXiv | 2005.07592 |
| Canonical record | [https://arxiv.org/abs/2005.07592](https://arxiv.org/abs/2005.07592) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-025_Borsboom2020_time-optimal-control-strategies-for-electric-race.pdf) |
| Source SHA-256 | `de23f2383a968bce3e711a8c97e2b81b647856f9513649285ea213b23b947c41` |
| Full-text coverage | 6/6 pages (100.00%); 4,475 extracted words |

## Research question

How does Time-optimal Control Strategies for Electric Race Cars with Different Transmission Technologies formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were control, electric, problem, energy, transmission, battery, vehicle, optimization. The paper-specific method or result selected for transfer review is: **Earlier transmission-technology comparison under time-optimal control**.

## Principal findings

- **Paper finding (conservative paraphrase):** Earlier transmission-technology comparison under time-optimal control
- **Reviewer interpretation:** precedent for architecture comparison at equal control effort
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** precedent for architecture comparison at equal control effort This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Earlier transmission-technology comparison under time-optimal control** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Earlier transmission-technology comparison under time-optimal control' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 6 pages, 25,885 characters, 4,475 words.
- Pages with substantial extractable text: 6/6.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
