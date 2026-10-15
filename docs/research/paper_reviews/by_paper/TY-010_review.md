# TY-010: Tire Modeling and Friction Estimation

Thai companion: `TY-010_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Not recorded in the curated source |
| Year | 2007 |
| Venue | Not recorded |
| DOI | Not recorded |
| arXiv | Not recorded |
| Canonical record | [https://lucris.lub.lu.se/ws/files/4401399/27004.pdf](https://lucris.lub.lu.se/ws/files/4401399/27004.pdf) |
| Library topic | Tyres, friction, and road contact |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/09_tyres_friction/TY-010_Anon2007_tire-modeling-and-friction-estimation.pdf) |
| Source SHA-256 | `4de55ab2dea8ddc65214b72823d9cc615f5a4b0841749c904ec1cde474c0d7a1` |
| Full-text coverage | 98/99 pages (98.99%); 65,895 extracted words |

## Research question

Which tyre/contact states and operating conditions does Tire Modeling and Friction Estimation identify, and can they support transient racing predictions?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were tire, slip, model, force, friction, wheel, figure, data. The paper-specific method or result selected for transfer review is: **Thesis on brush-type tyre models and friction estimation**.

## Principal findings

- **Paper finding (conservative paraphrase):** Thesis on brush-type tyre models and friction estimation
- **Reviewer interpretation:** a physical basis for combined-slip behaviour
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a physical basis for combined-slip behaviour This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Tyre parameters and conclusions are condition-, construction-, and dataset-specific; a fitted curve outside its load/temperature/wear envelope is not validated. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Thesis on brush-type tyre models and friction estimation** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation |
| Proposed change | Build a bounded diagnostic pilot from 'Thesis on brush-type tyre models and friction estimation' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Fit and validate against separate manoeuvres across combined slip, load, camber, pressure, temperature, wear, speed, and road state; compare with the present low-fidelity model. |
| Acceptance and failure evidence | Require bounded force/moment and temperature/wear errors on held-out manoeuvres and improved lap replay without hiding extrapolation outside the tyre envelope. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 99 pages, 352,359 characters, 65,895 words.
- Pages with substantial extractable text: 98/99.
- High-information cue pages sampled from across the paper: 4, 8, 11, 23, 51, 55, 56, 57. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
