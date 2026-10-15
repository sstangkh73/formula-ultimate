# AE-021: Surrogate Modeling of Car Drag Coefficient with Depth and Normal Renderings

Thai companion: `AE-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | B. Song, Chenyang Yuan, F. Permenter, Nikos Aréchiga, Faez Ahmed |
| Year | 2023 |
| Venue | Design Automation Conference |
| DOI | Not recorded |
| arXiv | 2306.06110 |
| Canonical record | [https://arxiv.org/abs/2306.06110](https://arxiv.org/abs/2306.06110) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-021_Song2023_surrogate-modeling-of-car-drag-coefficient-with-de.pdf) |
| Source SHA-256 | `f4efe0d668417e049bc2d5e9202fd23f25f8fb18af03f16279f68a3c765bc22c` |
| Full-text coverage | 17/17 pages (100.00%); 10,172 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Surrogate Modeling of Car Drag Coefficient with Depth and Normal Renderings establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were drag, surrogate, model, models, coefficient, representation, arxiv, renderings. The paper-specific method or result selected for transfer review is: **Image-based drag surrogate with a large car CFD dataset**.

## Principal findings

- **Paper finding (conservative paraphrase):** Image-based drag surrogate with a large car CFD dataset
- **Reviewer interpretation:** a cheap screening surrogate to compare against field surrogates
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a cheap screening surrogate to compare against field surrogates This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Image-based drag surrogate with a large car CFD dataset** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a bounded diagnostic pilot from 'Image-based drag surrogate with a large car CFD dataset' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 17 pages, 64,716 characters, 10,172 words.
- Pages with substantial extractable text: 17/17.
- High-information cue pages sampled from across the paper: 1, 4, 5, 8, 9, 10, 11, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
