# TY-013: Extended Pacejka Tire Model for Enhanced Vehicle

Thai companion: `TY-013_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Kanwar Bharat Singh, S. Sivaramakrishnan |
| Year | 2023 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2305.18422 |
| Canonical record | [https://arxiv.org/abs/2305.18422](https://arxiv.org/abs/2305.18422) |
| Library topic | Tyres, friction, and road contact |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/09_tyres_friction/TY-013_Singh2023_extended-pacejka-tire-model-for-enhanced-vehicle.pdf) |
| Source SHA-256 | `9a5127b3a5cf37cefdece054a5c23c9fbcc62835bc531ab45dba20d2d5c9ef0a` |
| Full-text coverage | 36/36 pages (100.00%); 10,814 extracted words |

## Research question

Which tyre/contact states and operating conditions does Extended Pacejka Tire Model for Enhanced Vehicle identify, and can they support transient racing predictions?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were tire, model, temperature, vehicle, figure, stiffness, load, cornering. The paper-specific method or result selected for transfer review is: **Extends the Pacejka model with additional effects for vehicle simulation**.

## Principal findings

- **Paper finding (conservative paraphrase):** Extends the Pacejka model with additional effects for vehicle simulation
- **Reviewer interpretation:** a comparator for tyre-model extensions
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a comparator for tyre-model extensions This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Tyre parameters and conclusions are condition-, construction-, and dataset-specific; a fitted curve outside its load/temperature/wear envelope is not validated. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Extends the Pacejka model with additional effects for vehicle simulation** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation |
| Proposed change | Build a bounded diagnostic pilot from 'Extends the Pacejka model with additional effects for vehicle simulation' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Fit and validate against separate manoeuvres across combined slip, load, camber, pressure, temperature, wear, speed, and road state; compare with the present low-fidelity model. |
| Acceptance and failure evidence | Require bounded force/moment and temperature/wear errors on held-out manoeuvres and improved lap replay without hiding extrapolation outside the tyre envelope. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 36 pages, 66,631 characters, 10,814 words.
- Pages with substantial extractable text: 36/36.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 10, 13, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
