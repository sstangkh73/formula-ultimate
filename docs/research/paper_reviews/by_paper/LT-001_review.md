# LT-001: Optimal control for a Formula One car with variable parameters

Thai companion: `LT-001_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Giacomo Perantoni, David J.N. Limebeer |
| Year | 2014 |
| Venue | Vehicle System Dynamics |
| DOI | 10.1080/00423114.2014.889315 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1080/00423114.2014.889315](https://doi.org/10.1080/00423114.2014.889315) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-001_Perantoni2014_optimal-control-for-a-formula-one-car-with-variabl.pdf) |
| Source SHA-256 | `03368de69d623d3b40719bb2ebde917c5561093ae598e76fa7fdab83606c328a` |
| Full-text coverage | 37/37 pages (100.00%); 11,267 extracted words |

## Research question

How does Optimal control for a Formula One car with variable parameters formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were track, control, vehicle, optimal, centre, tyre, time, line. The paper-specific method or result selected for transfer review is: **Minimum-lap-time control with vehicle parameters as optimisation variables**.

## Principal findings

- **Paper finding (conservative paraphrase):** Minimum-lap-time control with vehicle parameters as optimisation variables
- **Reviewer interpretation:** the template for design/driver fairness
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the template for design/driver fairness This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Minimum-lap-time control with vehicle parameters as optimisation variables** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Minimum-lap-time control with vehicle parameters as optimisation variables' against the target below. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 37 pages, 63,175 characters, 11,267 words.
- Pages with substantial extractable text: 37/37.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 8, 11, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
