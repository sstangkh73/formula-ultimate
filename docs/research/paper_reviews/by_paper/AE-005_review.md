# AE-005: DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction

Thai companion: `AE-005_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Mohamed Elrefaie, Angela Dai, Faez Ahmed |
| Year | 2024 |
| Venue | Design Automation Conference |
| DOI | Not recorded |
| arXiv | 2403.08055 |
| Canonical record | [https://arxiv.org/abs/2403.08055](https://arxiv.org/abs/2403.08055) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-005_Elrefaie2024_drivaernet-a-parametric-car-dataset-for-data-drive.pdf) |
| Source SHA-256 | `29eacd8ab473b092a9994853527bf01a94c7f4b5ce66ca760250a2b37bc3c9fd` |
| Full-text coverage | 18/18 pages (100.00%); 13,121 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, and frequent technical terms were dataset, model, aerodynamic, design, drivaernet, drag, learning, data. The paper-specific method or result selected for transfer review is: **Thousands of parametric car CFD results**.

## Principal findings

- **Paper finding (conservative paraphrase):** Thousands of parametric car CFD results
- **Reviewer interpretation:** training/validation data for drag surrogates, limited to road-car shapes
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** training/validation data for drag surrogates, limited to road-car shapes This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Thousands of parametric car CFD results** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Register the dataset or benchmark behind 'Thousands of parametric car CFD results' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 85,938 characters, 13,121 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 2, 3, 8, 13, 14, 15. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
