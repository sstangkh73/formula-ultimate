# CAD-010: Hierarchical Neural Coding for Controllable CAD Model Generation

Thai companion: `CAD-010_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Xiang Xu, P. Jayaraman, J. Lambourne, Karl D. D. Willis, Yasutaka Furukawa |
| Year | 2023 |
| Venue | International Conference on Machine Learning |
| DOI | Not recorded |
| arXiv | 2307.00149 |
| Canonical record | [https://arxiv.org/abs/2307.00149](https://arxiv.org/abs/2307.00149) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-010_Xu2023_hierarchical-neural-coding-for-controllable-cad-mo.pdf) |
| Source SHA-256 | `91308decaa58dce8a5d8e8217418eb8ddd481784f971012fa254c09d57dee1e6` |
| Full-text coverage | 20/20 pages (100.00%); 8,622 extracted words |

## Research question

Does Hierarchical Neural Coding for Controllable CAD Model Generation represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were model, generation, models, design, code, neural, figure, hierarchical. The paper-specific method or result selected for transfer review is: **Hierarchical codes for loops, profiles and solids**.

## Principal findings

- **Paper finding (conservative paraphrase):** Hierarchical codes for loops, profiles and solids
- **Reviewer interpretation:** enables controlled partial edits, analogous to local mutation of a part
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** enables controlled partial edits, analogous to local mutation of a part This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Hierarchical codes for loops, profiles and solids** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Hierarchical codes for loops, profiles and solids' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 20 pages, 52,692 characters, 8,622 words.
- Pages with substantial extractable text: 20/20.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
