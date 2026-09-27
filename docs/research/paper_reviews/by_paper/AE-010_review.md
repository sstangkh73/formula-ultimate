# AE-010: WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics

Thai companion: `AE-010_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Neil Ashton, Jordan B. Angel, A. Ghate, G. Kenway, M. Wong, C. Kiris, Astrid Walle, Danielle C. Maddix, G. Page |
| Year | 2024 |
| Venue | Neural Information Processing Systems |
| DOI | Not recorded |
| arXiv | 2407.19320 |
| Canonical record | [https://arxiv.org/abs/2407.19320](https://arxiv.org/abs/2407.19320) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-010_Ashton2024_windsorml-high-fidelity-computational-fluid-dynami.pdf) |
| Source SHA-256 | `6c2c5b3118718f1f129b78cad2a4f351e66bdfab39004fc15cd322c897dbac64` |
| Full-text coverage | 35/39 pages (89.74%); 11,517 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were dataset, data, coefficient, geometry, body, windsor, velocity, drag. The paper-specific method or result selected for transfer review is: **Wall-modelled LES of Windsor-body variants (CC-BY-SA)**.

## Principal findings

- **Paper finding (conservative paraphrase):** Wall-modelled LES of Windsor-body variants (CC-BY-SA)
- **Reviewer interpretation:** open high-fidelity data including ground proximity
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** open high-fidelity data including ground proximity This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Wall-modelled LES of Windsor-body variants (CC-BY-SA)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Register the dataset or benchmark behind 'Wall-modelled LES of Windsor-body variants (CC-BY-SA)' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 39 pages, 70,759 characters, 11,517 words.
- Pages with substantial extractable text: 35/39.
- High-information cue pages sampled from across the paper: 2, 3, 4, 7, 9, 16, 17, 21. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
