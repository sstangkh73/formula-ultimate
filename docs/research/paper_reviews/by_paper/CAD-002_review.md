# CAD-002: Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts

Thai companion: `CAD-002_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Mohammad Sadil Khan, Sankalp Sinha, T. Sheikh, Didier Stricker, S. Ali, M. Z. Afzal |
| Year | 2024 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2409.17106 |
| Canonical record | [https://arxiv.org/abs/2409.17106](https://arxiv.org/abs/2409.17106) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-002_Khan2024_text2cad-generating-sequential-cad-models-from-beg.pdf) |
| Source SHA-256 | `fe5c6bd551f9f3797640593051bbda04c5dbecc7a47d59b4fcf7727bd750f1a4` |
| Full-text coverage | 21/21 pages (100.00%); 12,688 extracted words |

## Research question

Does Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, limitations, results, and frequent technical terms were model, sketch, prompts, models, text, text2cad, design, deepcad. The paper-specific method or result selected for transfer review is: **Text to CAD sequences with graded prompt levels**.

## Principal findings

- **Paper finding (conservative paraphrase):** Text to CAD sequences with graded prompt levels
- **Reviewer interpretation:** a data and evaluation reference for language-to-geometry proposals
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a data and evaluation reference for language-to-geometry proposals This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Text to CAD sequences with graded prompt levels** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Text to CAD sequences with graded prompt levels' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 21 pages, 78,226 characters, 12,688 words.
- Pages with substantial extractable text: 21/21.
- High-information cue pages sampled from across the paper: 1, 2, 5, 7, 8, 9, 15, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, limitations, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
