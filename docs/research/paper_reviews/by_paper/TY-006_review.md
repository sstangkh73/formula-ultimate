# TY-006: The Formula SAE Tire Test Consortium-Tire Testing and Data Handling

Thai companion: `TY-006_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Edward M. Kasprzak, David Gentz |
| Year | 2006 |
| Venue | SAE Technical Paper Series |
| DOI | 10.4271/2006-01-3606 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.4271/2006-01-3606](https://doi.org/10.4271/2006-01-3606) |
| Library topic | Tyres, friction, and road contact |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/09_tyres_friction/TY-006_Kasprzak2006_the-formula-sae-tire-test-consortium-tire-testing.pdf) |
| Source SHA-256 | `5e1f8f64a5d742170595e5714b15cf60185d789672ba31a230d23cc42bc3dc26` |
| Full-text coverage | 12/12 pages (100.00%); 7,879 extracted words |

## Research question

Which tyre/contact states and operating conditions does The Formula SAE Tire Test Consortium-Tire Testing and Data Handling identify, and can they support transient racing predictions?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, physical-test evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, and frequent technical terms were tire, test, fsae, testing, data, slip, calspan, angle. The paper-specific method or result selected for transfer review is: **How the FSAE TTC measured and distributes tyre data**.

## Principal findings

- **Paper finding (conservative paraphrase):** How the FSAE TTC measured and distributes tyre data
- **Reviewer interpretation:** the most accessible real racing-tyre data source to request
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the most accessible real racing-tyre data source to request This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Tyre parameters and conclusions are condition-, construction-, and dataset-specific; a fitted curve outside its load/temperature/wear envelope is not validated. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **How the FSAE TTC measured and distributes tyre data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation |
| Proposed change | Register the dataset or benchmark behind 'How the FSAE TTC measured and distributes tyre data' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Fit and validate against separate manoeuvres across combined slip, load, camber, pressure, temperature, wear, speed, and road state; compare with the present low-fidelity model. |
| Acceptance and failure evidence | Require bounded force/moment and temperature/wear errors on held-out manoeuvres and improved lap replay without hiding extrapolation outside the tyre envelope. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 12 pages, 46,779 characters, 7,879 words.
- Pages with substantial extractable text: 12/12.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
