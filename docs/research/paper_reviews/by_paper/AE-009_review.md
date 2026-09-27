# AE-009: AhmedML: High-Fidelity Computational Fluid Dynamics Dataset for Incompressible, Low-Speed Bluff Body Aerodynamics

Thai companion: `AE-009_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Neil Ashton, Danielle C. Maddix, Samuel Gundry, Parisa M. Shabestari |
| Year | 2024 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2407.20801 |
| Canonical record | [https://arxiv.org/abs/2407.20801](https://arxiv.org/abs/2407.20801) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-009_Ashton2024_ahmedml-high-fidelity-computational-fluid-dynamics.pdf) |
| Source SHA-256 | `28586b44def69eee8d82f8fab95c74905616c2f59326cc7dec68c751657cf70f` |
| Full-text coverage | 36/38 pages (94.74%); 13,818 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does AhmedML: High-Fidelity Computational Fluid Dynamics Dataset for Incompressible, Low-Speed Bluff Body Aerodynamics establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, results, and frequent technical terms were dataset, flow, body, data, ahmed, geometry, used, page. The paper-specific method or result selected for transfer review is: **500 Ahmed-body variants with hybrid RANS-LES**.

## Principal findings

- **Paper finding (conservative paraphrase):** 500 Ahmed-body variants with hybrid RANS-LES
- **Reviewer interpretation:** a simpler bluff-body benchmark for testing aero pipelines
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a simpler bluff-body benchmark for testing aero pipelines This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **500 Ahmed-body variants with hybrid RANS-LES** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Register the dataset or benchmark behind '500 Ahmed-body variants with hybrid RANS-LES' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 38 pages, 85,485 characters, 13,818 words.
- Pages with substantial extractable text: 36/38.
- High-information cue pages sampled from across the paper: 1, 2, 4, 5, 8, 9, 17, 23. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
