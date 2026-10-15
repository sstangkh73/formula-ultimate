# CAD-006: ABC: A Big CAD Model Dataset For Geometric Deep Learning

Thai companion: `CAD-006_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Sebastian Koch, A. Matveev, Zhong-Shi Jiang, Francis Williams, Alexey Artemov, Evgeny Burnaev, M. Alexa, D. Zorin, Daniele Panozzo |
| Year | 2019 |
| Venue | Computer Vision and Pattern Recognition |
| DOI | Not recorded |
| arXiv | 1812.06216 |
| Canonical record | [https://arxiv.org/abs/1812.06216](https://arxiv.org/abs/1812.06216) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-006_Koch2019_abc-a-big-cad-model-dataset-for-geometric-deep-lea.pdf) |
| Source SHA-256 | `535f9252d9dcd6fcf99b41db4e3c015c1b8be1dd741d7fec569074a449f0cda5` |
| Full-text coverage | 15/15 pages (100.00%); 10,370 extracted words |

## Research question

Does ABC: A Big CAD Model Dataset For Geometric Deep Learning represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were models, point, methods, learning, axis, dataset, surface, patches. The paper-specific method or result selected for transfer review is: **One million B-rep models with parametric curves and surfaces**.

## Principal findings

- **Paper finding (conservative paraphrase):** One million B-rep models with parametric curves and surfaces
- **Reviewer interpretation:** a benchmark source for geometry-kernel robustness tests
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a benchmark source for geometry-kernel robustness tests This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **One million B-rep models with parametric curves and surfaces** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Register the dataset or benchmark behind 'One million B-rep models with parametric curves and surfaces' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 15 pages, 60,487 characters, 10,370 words.
- Pages with substantial extractable text: 15/15.
- High-information cue pages sampled from across the paper: 1, 2, 5, 6, 7, 15. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
