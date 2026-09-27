# ST-018: Affine Body Dynamics: Fast, Stable & Intersection-free Simulation of Stiff Materials

Thai companion: `ST-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | L. Lan, D. Kaufman, Min-Chen Li, Chenfanfu Jiang, Yin Yang |
| Year | 2022 |
| Venue | ACM Transactions on Graphics |
| DOI | Not recorded |
| arXiv | 2201.10022 |
| Canonical record | [https://arxiv.org/abs/2201.10022](https://arxiv.org/abs/2201.10022) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-018_Lan2022_affine-body-dynamics-fast-stable-intersection-free.pdf) |
| Source SHA-256 | `c1a1de3aca16e5b1538187eb0d88c404cceb7241fd58d28eec1e923dc30e89e2` |
| Full-text coverage | 14/14 pages (100.00%); 13,230 extracted words |

## Research question

What structural, meshing, contact, or failure method does Affine Body Dynamics: Fast, Stable & Intersection-free Simulation of Stiff Materials validate, and over which numerical and physical regime?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, results, and frequent technical terms were body, rigid, simulation, contact, time, rigid-ipc, bodies, collision. The paper-specific method or result selected for transfer review is: **Stiff bodies as affine deformations with IPC contact**.

## Principal findings

- **Paper finding (conservative paraphrase):** Stiff bodies as affine deformations with IPC contact
- **Reviewer interpretation:** a fast option for many-part assemblies
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a fast option for many-part assemblies This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Stiff bodies as affine deformations with IPC contact** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Build a bounded diagnostic pilot from 'Stiff bodies as affine deformations with IPC contact' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 80,408 characters, 13,230 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7, 8, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
