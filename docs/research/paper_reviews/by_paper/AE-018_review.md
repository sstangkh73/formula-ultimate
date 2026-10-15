# AE-018: Geometry-Informed Neural Operator for Large-Scale 3D PDEs

Thai companion: `AE-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Zong-Yi Li, Nikola B. Kovachki, C. Choy, Boyi Li, Jean Kossaifi, S. Otta, M. A. Nabian, Maximilian Stadler, Christian Hundt, K. Azizzadenesheli, Anima Anandkumar |
| Year | 2023 |
| Venue | Neural Information Processing Systems |
| DOI | Not recorded |
| arXiv | 2309.00583 |
| Canonical record | [https://arxiv.org/abs/2309.00583](https://arxiv.org/abs/2309.00583) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-018_Li2023_geometry-informed-neural-operator-for-large-scale.pdf) |
| Source SHA-256 | `d39234e06de75ca58b2e6f0f7069ae16305193c30173bb1c7a9b6aade5c7262a` |
| Full-text coverage | 22/23 pages (95.65%); 9,743 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Geometry-Informed Neural Operator for Large-Scale 3D PDEs establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were neural, gino, operator, model, arxiv, latent, error, graph. The paper-specific method or result selected for transfer review is: **GINO predicts car surface pressure from geometry**.

## Principal findings

- **Paper finding (conservative paraphrase):** GINO predicts car surface pressure from geometry
- **Reviewer interpretation:** an early neural-operator car-aero result to reproduce
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an early neural-operator car-aero result to reproduce This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **GINO predicts car surface pressure from geometry** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a bounded diagnostic pilot from 'GINO predicts car surface pressure from geometry' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 23 pages, 59,957 characters, 9,743 words.
- Pages with substantial extractable text: 22/23.
- High-information cue pages sampled from across the paper: 1, 2, 3, 8, 9, 10, 12, 18. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
