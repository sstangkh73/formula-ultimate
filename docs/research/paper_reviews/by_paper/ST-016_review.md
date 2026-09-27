# ST-016: High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes

Thai companion: `ST-016_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Z. Ferguson, Pranav Jain, D. Zorin, T. Schneider, Daniele Panozzo |
| Year | 2023 |
| Venue | International Conference on Computer Graphics and Interactive Techniques |
| DOI | Not recorded |
| arXiv | 2205.13727 |
| Canonical record | [https://arxiv.org/abs/2205.13727](https://arxiv.org/abs/2205.13727) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-016_Ferguson2023_high-order-incremental-potential-contact-for-elast.pdf) |
| Source SHA-256 | `74901a12ee4f11b6fcf19efdea5ef6b75a55426f5a0ea6fe7051e5fd142e5a1b` |
| Full-text coverage | 11/11 pages (100.00%); 10,418 extracted words |

## Research question

What structural, meshing, contact, or failure method does High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes validate, and over which numerical and physical regime?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, methods, results, and frequent technical terms were mesh, linear, contact, bases, method, high-order, figure, simulation. The paper-specific method or result selected for transfer review is: **Extends IPC to curved high-order meshes**.

## Principal findings

- **Paper finding (conservative paraphrase):** Extends IPC to curved high-order meshes
- **Reviewer interpretation:** relevant once CAD-conforming meshes are used
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant once CAD-conforming meshes are used This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Extends IPC to curved high-order meshes** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Build a bounded diagnostic pilot from 'Extends IPC to curved high-order meshes' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 11 pages, 62,765 characters, 10,418 words.
- Pages with substantial extractable text: 11/11.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 8, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
