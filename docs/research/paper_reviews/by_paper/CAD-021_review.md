# CAD-021: CADENA: Stepwise CAD Reverse Engineering

Thai companion: `CAD-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | S. Kabisov, G. Savrasov, Maksim Elistratov, Antonio Rodriguez, Daniil Ignatiev, N. Gavrilov, Rustam Uzdenov, A. I. Boyko, I. Pasechnik, Anton Konushin, Andrey Kuznetsov, Dmitrii Zhemchuzhnikov |
| Year | 2026 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2608.00799 |
| Canonical record | [https://arxiv.org/abs/2608.00799](https://arxiv.org/abs/2608.00799) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-021_Kabisov2026_cadena-stepwise-cad-reverse-engineering.pdf) |
| Source SHA-256 | `46aeb8dd8bde57c8ecc0c9bb8e83a0c5b587b42ce9c3391955e12731c4a43fec` |
| Full-text coverage | 24/24 pages (100.00%); 16,481 extracted words |

## Research question

Does CADENA: Stepwise CAD Reverse Engineering represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, limitations, methods, results, and frequent technical terms were parts, geometry, operation, model, cadena, rather, table, program. The paper-specific method or result selected for transfer review is: **Stepwise recovery of editable CAD from geometry**.

## Principal findings

- **Paper finding (conservative paraphrase):** Stepwise recovery of editable CAD from geometry
- **Reviewer interpretation:** useful for turning evolved meshes or fields back into editable parts
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** useful for turning evolved meshes or fields back into editable parts This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Stepwise recovery of editable CAD from geometry** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Stepwise recovery of editable CAD from geometry' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 24 pages, 97,414 characters, 16,481 words.
- Pages with substantial extractable text: 24/24.
- High-information cue pages sampled from across the paper: 1, 3, 7, 10, 11, 12, 13, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, limitations, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
