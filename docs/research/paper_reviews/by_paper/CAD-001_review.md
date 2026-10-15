# CAD-001: DeepCAD: A Deep Generative Network for Computer-Aided Design Models

Thai companion: `CAD-001_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Rundi Wu, Chang Xiao, Changxi Zheng |
| Year | 2021 |
| Venue | IEEE International Conference on Computer Vision |
| DOI | Not recorded |
| arXiv | 2105.09492 |
| Canonical record | [https://arxiv.org/abs/2105.09492](https://arxiv.org/abs/2105.09492) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-001_Wu2021_deepcad-a-deep-generative-network-for-computer-aid.pdf) |
| Source SHA-256 | `9d715b7ca3202a7bc098a37a66ec0f71194113051e2c03623aa2184eac967569` |
| Full-text coverage | 15/15 pages (100.00%); 10,542 extracted words |

## Research question

Does DeepCAD: A Deep Generative Network for Computer-Aided Design Models represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were command, model, shape, models, parameters, sequence, generative, dataset. The paper-specific method or result selected for transfer review is: **Generates sketch-and-extrude construction sequences**.

## Principal findings

- **Paper finding (conservative paraphrase):** Generates sketch-and-extrude construction sequences
- **Reviewer interpretation:** a proposal representation whose outputs still need our load-path and process gates
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a proposal representation whose outputs still need our load-path and process gates This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Generates sketch-and-extrude construction sequences** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Generates sketch-and-extrude construction sequences' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 15 pages, 63,207 characters, 10,542 words.
- Pages with substantial extractable text: 15/15.
- High-information cue pages sampled from across the paper: 1, 2, 5, 6, 7, 12, 14, 15. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
