# ST-008: An efficient 3D topology optimization code written in Matlab

Thai companion: `ST-008_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Kai Liu, Andrés Tovar |
| Year | 2014 |
| Venue | Structural and Multidisciplinary Optimization |
| DOI | 10.1007/s00158-014-1107-x |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1007/s00158-014-1107-x](https://doi.org/10.1007/s00158-014-1107-x) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-008_Liu2014_an-efficient-3d-topology-optimization-code-written.pdf) |
| Source SHA-256 | `6c85761e58c49983a5679c0d5587f7bcf38b40295028000f35a76b489cca30c3` |
| Full-text coverage | 21/22 pages (95.45%); 10,433 extracted words |

## Research question

What structural, meshing, contact, or failure method does An efficient 3D topology optimization code written in Matlab validate, and over which numerical and physical regime?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, and frequent technical terms were optimization, topology, element, design, problem, line, where, method. The paper-specific method or result selected for transfer review is: **Compact 3D topology optimisation reference**.

## Principal findings

- **Paper finding (conservative paraphrase):** Compact 3D topology optimisation reference
- **Reviewer interpretation:** a 3D structural baseline for part-level comparisons
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a 3D structural baseline for part-level comparisons This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Compact 3D topology optimisation reference** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Build a bounded diagnostic pilot from 'Compact 3D topology optimisation reference' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 22 pages, 59,462 characters, 10,433 words.
- Pages with substantial extractable text: 21/22.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
