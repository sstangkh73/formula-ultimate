# CAD-033: KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity

Thai companion: `CAD-033_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Zi-Qi Gao, Zhijie Yang, Qiang Zou |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2606.01702 |
| Canonical record | [https://arxiv.org/abs/2606.01702](https://arxiv.org/abs/2606.01702) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-033_Gao2026_kdh-cad-knowledge-data-hybrid-cad-learning-under-d.pdf) |
| Source SHA-256 | `341e6905aeb9509b6f27e8bc7df22361a14a2f25e5e7f2f54dc331699310c6c8` |
| Full-text coverage | 18/18 pages (100.00%); 12,585 extracted words |

## Research question

Does KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were knowledge, data, models, kdh-cad, part, learning, model, category. The paper-specific method or result selected for transfer review is: **Combines engineering knowledge with scarce CAD data**.

## Principal findings

- **Paper finding (conservative paraphrase):** Combines engineering knowledge with scarce CAD data
- **Reviewer interpretation:** relevant because vehicle-part data is small and proprietary
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant because vehicle-part data is small and proprietary This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Combines engineering knowledge with scarce CAD data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Combines engineering knowledge with scarce CAD data' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 79,774 characters, 12,585 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 5, 7, 8, 10, 11, 12, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
