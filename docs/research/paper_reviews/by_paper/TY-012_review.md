# TY-012: A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing

Thai companion: `TY-012_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Cole Cappello, A. Hoegh |
| Year | 2025 |
| Venue | Journal of Sports Analytics |
| DOI | Not recorded |
| arXiv | 2512.00640 |
| Canonical record | [https://arxiv.org/abs/2512.00640](https://arxiv.org/abs/2512.00640) |
| Library topic | Tyres, friction, and road contact |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/09_tyres_friction/TY-012_Cappello2025_a-state-space-approach-to-modeling-tire-degradatio.pdf) |
| Source SHA-256 | `ecacae600f48f42f4b9c51586b5e4784901f05def46737fb96e1188187ed7c7e` |
| Full-text coverage | 18/18 pages (100.00%); 6,059 extracted words |

## Research question

Which tyre/contact states and operating conditions does A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing identify, and can they support transient racing predictions?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, physical-test evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were degradation, model, tire, tires, time, race, models, times. The paper-specific method or result selected for transfer review is: **Bayesian state-space tyre degradation estimated from real 2025 F1 lap times**.

## Principal findings

- **Paper finding (conservative paraphrase):** Bayesian state-space tyre degradation estimated from real 2025 F1 lap times
- **Reviewer interpretation:** data-driven degradation rates for race-length simulation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** data-driven degradation rates for race-length simulation This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Tyre parameters and conclusions are condition-, construction-, and dataset-specific; a fitted curve outside its load/temperature/wear envelope is not validated. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Bayesian state-space tyre degradation estimated from real 2025 F1 lap times** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation |
| Proposed change | Register the dataset or benchmark behind 'Bayesian state-space tyre degradation estimated from real 2025 F1 lap times' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Fit and validate against separate manoeuvres across combined slip, load, camber, pressure, temperature, wear, speed, and road state; compare with the present low-fidelity model. |
| Acceptance and failure evidence | Require bounded force/moment and temperature/wear errors on held-out manoeuvres and improved lap replay without hiding extrapolation outside the tyre envelope. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 35,225 characters, 6,059 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 6, 7, 14, 17. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
