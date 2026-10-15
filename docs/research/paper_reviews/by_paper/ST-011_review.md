# ST-011: Gmsh: A 3-D finite element mesh generator with built-in pre- and post-processing facilities

Thai companion: `ST-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Christophe Geuzaine, Jean‐François Remacle |
| Year | 2009 |
| Venue | International Journal for Numerical Methods in Engineering |
| DOI | 10.1002/nme.2579 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1002/nme.2579](https://doi.org/10.1002/nme.2579) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-011_Geuzaine2009_gmsh-a-3-d-finite-element-mesh-generator-with-buil.pdf) |
| Source SHA-256 | `b9d41566a8df629143e2e608a5815e46853c6b978415cf76e745471b44410e4c` |
| Full-text coverage | 24/24 pages (100.00%); 10,361 extracted words |

## Research question

What structural, meshing, contact, or failure method does Gmsh: A 3-D finite element mesh generator with built-in pre- and post-processing facilities validate, and over which numerical and physical regime?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were mesh, gmsh, model, generation, surface, size, meshes, figure. The paper-specific method or result selected for transfer review is: **The mesher of the geometry-mesh bridge (Work 110)**.

## Principal findings

- **Paper finding (conservative paraphrase):** The mesher of the geometry-mesh bridge (Work 110)
- **Reviewer interpretation:** read with its documentation before trusting mesh quality settings
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** read with its documentation before trusting mesh quality settings This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The mesher of the geometry-mesh bridge (Work 110)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'The mesher of the geometry-mesh bridge (Work 110)' against the target below. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 24 pages, 60,462 characters, 10,361 words.
- Pages with substantial extractable text: 24/24.
- High-information cue pages sampled from across the paper: 1, 3, 4, 5, 12, 14, 15, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
