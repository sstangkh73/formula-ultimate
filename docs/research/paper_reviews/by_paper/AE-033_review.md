# AE-033: Fourier Neural Operator for Parametric Partial Differential Equations

Thai companion: `AE-033_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Zong-Yi Li, Nikola B. Kovachki, K. Azizzadenesheli, Burigede Liu, K. Bhattacharya, Andrew M. Stuart, Anima Anandkumar |
| Year | 2021 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2010.08895 |
| Canonical record | [https://arxiv.org/abs/2010.08895](https://arxiv.org/abs/2010.08895) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-033_Li2021_fourier-neural-operator-for-parametric-partial-dif.pdf) |
| Source SHA-256 | `6cd2645d4a50d1a61a261529b33747c674d78851bdbe6993b0961f81a17dc6f2` |
| Full-text coverage | 16/16 pages (100.00%); 8,316 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Fourier Neural Operator for Parametric Partial Differential Equations establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were neural, fourier, operator, equation, networks, learning, resolution, operators. The paper-specific method or result selected for transfer review is: **Neural operator learning solution maps of PDEs**.

## Principal findings

- **Paper finding (conservative paraphrase):** Neural operator learning solution maps of PDEs
- **Reviewer interpretation:** the base architecture of many flow surrogates
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the base architecture of many flow surrogates This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Neural operator learning solution maps of PDEs** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a bounded diagnostic pilot from 'Neural operator learning solution maps of PDEs' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 48,917 characters, 8,316 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
