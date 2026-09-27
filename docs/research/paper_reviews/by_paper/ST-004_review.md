# ST-004: Giga-voxel computational morphogenesis for structural design

Thai companion: `ST-004_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Niels Aage, Erik Andreassen, Boyan S. Lazarov, Ole Sigmund |
| Year | 2017 |
| Venue | Nature |
| DOI | 10.1038/nature23911 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1038/nature23911](https://doi.org/10.1038/nature23911) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-004_Aage2017_giga-voxel-computational-morphogenesis-for-structu.pdf) |
| Source SHA-256 | `9cb39abb372166ce8b8ed7cd70becfba1086b4d86184fc56a9c3e13eac2d48e0` |
| Full-text coverage | 19/19 pages (100.00%); 6,630 extracted words |

## Research question

What structural, meshing, contact, or failure method does Giga-voxel computational morphogenesis for structural design validate, and over which numerical and physical regime?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence, mathematical/formal evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were methods, and frequent technical terms were design, wing, optimization, page, topology, data, stiffness, extended. The paper-specific method or result selected for transfer review is: **Topology optimisation of a full aircraft wing at billion-voxel resolution discovered non-conventional internal structure**.

## Principal findings

- **Paper finding (conservative paraphrase):** Topology optimisation of a full aircraft wing at billion-voxel resolution discovered non-conventional internal structure
- **Reviewer interpretation:** closest structural analogue to whole-part discovery
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** closest structural analogue to whole-part discovery This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Topology optimisation of a full aircraft wing at billion-voxel resolution discovered non-conventional internal structure** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Topology optimisation of a full aircraft wing at billion-voxel resolution discovered non-conventional internal structure' against the target below. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 19 pages, 42,065 characters, 6,630 words.
- Pages with substantial extractable text: 19/19.
- High-information cue pages sampled from across the paper: 2, 3, 4, 6, 7, 9, 11, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
