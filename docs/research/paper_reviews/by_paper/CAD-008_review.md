# CAD-008: SolidGen: An Autoregressive Model for Direct B-rep Synthesis

Thai companion: `CAD-008_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | P. Jayaraman, J. Lambourne, Nishkrit Desai, Karl D. D. Willis, Aditya Sanghi, Nigel J. W. Morris |
| Year | 2023 |
| Venue | Trans. Mach. Learn. Res. |
| DOI | Not recorded |
| arXiv | 2203.13944 |
| Canonical record | [https://arxiv.org/abs/2203.13944](https://arxiv.org/abs/2203.13944) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-008_Jayaraman2023_solidgen-an-autoregressive-model-for-direct-b-rep.pdf) |
| Source SHA-256 | `97e584ecac93939bee5f0ac5d7aa3784648099f1cea03c971454e37e6c128f24` |
| Full-text coverage | 26/26 pages (100.00%); 12,786 extracted words |

## Research question

Does SolidGen: An Autoregressive Model for Direct B-rep Synthesis represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were uni00000013, model, solidgen, uni00000048, b-rep, models, learning, face. The paper-specific method or result selected for transfer review is: **Direct B-rep synthesis with indexed boundary representation**.

## Principal findings

- **Paper finding (conservative paraphrase):** Direct B-rep synthesis with indexed boundary representation
- **Reviewer interpretation:** shows how to generate valid topology without a construction history
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** shows how to generate valid topology without a construction history This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Direct B-rep synthesis with indexed boundary representation** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Direct B-rep synthesis with indexed boundary representation' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 26 pages, 82,615 characters, 12,786 words.
- Pages with substantial extractable text: 26/26.
- High-information cue pages sampled from across the paper: 1, 2, 8, 9, 10, 11, 13, 21. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
