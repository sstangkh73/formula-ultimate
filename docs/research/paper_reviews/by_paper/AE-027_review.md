# AE-027: AirfRANS: High Fidelity Computational Fluid Dynamics Dataset for Approximating Reynolds-Averaged Navier-Stokes Solutions

Thai companion: `AE-027_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | F. Bonnet, Jocelyn Ahmed Mazari, P. Cinnella, P. Gallinari |
| Year | 2022 |
| Venue | Neural Information Processing Systems |
| DOI | Not recorded |
| arXiv | 2212.07564 |
| Canonical record | [https://arxiv.org/abs/2212.07564](https://arxiv.org/abs/2212.07564) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-027_Bonnet2022_airfrans-high-fidelity-computational-fluid-dynamic.pdf) |
| Source SHA-256 | `3e995da6a0242420bb8dbb2cde5d998592615a5f9440c4a18b03a15e3371e161` |
| Full-text coverage | 62/62 pages (100.00%); 24,330 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does AirfRANS: High Fidelity Computational Fluid Dynamics Dataset for Approximating Reynolds-Averaged Navier-Stokes Solutions establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were different, surface, coefficient, models, regime, coefficients, airfoil, data. The paper-specific method or result selected for transfer review is: **Airfoil RANS dataset with physics-consistency metrics**.

## Principal findings

- **Paper finding (conservative paraphrase):** Airfoil RANS dataset with physics-consistency metrics
- **Reviewer interpretation:** relevant to wing-element surrogates and evaluation of physical consistency
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to wing-element surrogates and evaluation of physical consistency This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Airfoil RANS dataset with physics-consistency metrics** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Register the dataset or benchmark behind 'Airfoil RANS dataset with physics-consistency metrics' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 62 pages, 136,548 characters, 24,330 words.
- Pages with substantial extractable text: 62/62.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 8, 9, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
