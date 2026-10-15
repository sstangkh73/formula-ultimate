# AE-004: Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design

Thai companion: `AE-004_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Francisco Palacios, Juan Alonso, Karthikeyan Duraisamy, Michael Colonno, Jason Hicken, Aniket Aranake, Alejandro Campos, Sean Copeland, Thomas Economon, Amrita Lonkar, Trent Lukaczyk, Thomas Taylor |
| Year | 2013 |
| Venue | 51st AIAA Aerospace Sciences Meeting including the New Horizons Forum and Aerospace Exposition |
| DOI | 10.2514/6.2013-287 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.2514/6.2013-287](https://doi.org/10.2514/6.2013-287) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-004_Palacios2013_stanford-university-unstructured-su2-an-open-sourc.pdf) |
| Source SHA-256 | `5ec996782943d83bf1ed7172cbf6e84e6553bba76b5ec1dd5e0b1909e593ce52` |
| Full-text coverage | 60/60 pages (100.00%); 29,480 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were design, aiaa, where, mesh, figure, surface, qeronautics, thomas. The paper-specific method or result selected for transfer review is: **Open CFD and adjoint design suite**.

## Principal findings

- **Paper finding (conservative paraphrase):** Open CFD and adjoint design suite
- **Reviewer interpretation:** an independent second solver for aero cross-checks
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an independent second solver for aero cross-checks This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Open CFD and adjoint design suite** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a bounded diagnostic pilot from 'Open CFD and adjoint design suite' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 60 pages, 168,158 characters, 29,480 words.
- Pages with substantial extractable text: 60/60.
- High-information cue pages sampled from across the paper: 19, 54. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
