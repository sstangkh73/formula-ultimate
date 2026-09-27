# ST-012: Fast Tetrahedral Meshing in the Wild

Thai companion: `ST-012_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Yi-Xin Hu, T. Schneider, Bo-Lun Wang, D. Zorin, Daniele Panozzo |
| Year | 2020 |
| Venue | ACM Transactions on Graphics |
| DOI | Not recorded |
| arXiv | 1908.03581 |
| Canonical record | [https://arxiv.org/abs/1908.03581](https://arxiv.org/abs/1908.03581) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-012_Hu2020_fast-tetrahedral-meshing-in-the-wild.pdf) |
| Source SHA-256 | `94711fa5d370d382fe1997d8c8650b6d50406ce85477be5ca0c15d94904d2ded` |
| Full-text coverage | 17/17 pages (100.00%); 15,186 extracted words |

## Research question

What structural, meshing, contact, or failure method does Fast Tetrahedral Meshing in the Wild validate, and over which numerical and physical regime?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, physical-test evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, limitations, methods, results, and frequent technical terms were mesh, input, algorithm, tetrahedral, tetwild, triangle, https, energy. The paper-specific method or result selected for transfer review is: **fTetWild meshes arbitrary, imperfect triangle soups robustly**.

## Principal findings

- **Paper finding (conservative paraphrase):** fTetWild meshes arbitrary, imperfect triangle soups robustly
- **Reviewer interpretation:** a fallback when generated CAD is not clean enough for CAD-based meshing
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a fallback when generated CAD is not clean enough for CAD-based meshing This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **fTetWild meshes arbitrary, imperfect triangle soups robustly** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'fTetWild meshes arbitrary, imperfect triangle soups robustly' against the target below. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 17 pages, 91,640 characters, 15,186 words.
- Pages with substantial extractable text: 17/17.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 8, 9, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, limitations, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
