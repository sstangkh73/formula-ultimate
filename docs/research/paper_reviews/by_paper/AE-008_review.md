# AE-008: DrivAerML: High-Fidelity Computational Fluid Dynamics Dataset for Road-Car External Aerodynamics

Thai companion: `AE-008_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Neil Ashton, C. Mockett, M. Fuchs, Louis Fliessbach, Hendrik Hetmann, Thilo Knacke, Norbert Schonwald, Vangelis Skaperdas, Grigoris Fotiadis, Astrid Walle, Burkhard Hupertz, Danielle C. Maddix |
| Year | 2024 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2408.11969 |
| Canonical record | [https://arxiv.org/abs/2408.11969](https://arxiv.org/abs/2408.11969) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-008_Ashton2024_drivaerml-high-fidelity-computational-fluid-dynami.pdf) |
| Source SHA-256 | `86b8b7803a3d9975acfe0261eaa93fc14c83e2648c6f9f9a32f8ec2972148fe9` |
| Full-text coverage | 52/56 pages (92.86%); 21,243 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does DrivAerML: High-Fidelity Computational Fluid Dynamics Dataset for Road-Car External Aerodynamics establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, physical-test evidence, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, limitations, and frequent technical terms were dataset, flow, data, pressure, page, geometry, coefficient, model. The paper-specific method or result selected for transfer review is: **500 DrivAer variants with hybrid RANS-LES at 160M cells, open licence**.

## Principal findings

- **Paper finding (conservative paraphrase):** 500 DrivAer variants with hybrid RANS-LES at 160M cells, open licence
- **Reviewer interpretation:** high-fidelity reference data for surrogate validation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** high-fidelity reference data for surrogate validation This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **500 DrivAer variants with hybrid RANS-LES at 160M cells, open licence** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Register the dataset or benchmark behind '500 DrivAer variants with hybrid RANS-LES at 160M cells, open licence' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 56 pages, 129,941 characters, 21,243 words.
- Pages with substantial extractable text: 52/56.
- High-information cue pages sampled from across the paper: 4, 5, 7, 8, 16, 21, 22, 30. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, limitations.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
