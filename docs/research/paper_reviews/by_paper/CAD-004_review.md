# CAD-004: Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences

Thai companion: `CAD-004_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Karl D. D. Willis, Yewen Pu, Jieliang Luo, Hang Chu, Tao Du, J. Lambourne, Armando Solar-Lezama, W. Matusik |
| Year | 2021 |
| Venue | ACM Transactions on Graphics |
| DOI | Not recorded |
| arXiv | 2010.02392 |
| Canonical record | [https://arxiv.org/abs/2010.02392](https://arxiv.org/abs/2010.02392) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-004_Willis2021_fusion-360-gallery-a-dataset-and-environment-for-p.pdf) |
| Source SHA-256 | `a962861a275a5daa0c7de98d7a50fe249e7df72e7caaf862d366974b4675686e` |
| Full-text coverage | 24/24 pages (100.00%); 16,116 extracted words |

## Research question

Does Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were discussion, introduction, limitations, results, and frequent technical terms were sketch, design, reconstruction, extrude, geometry, data, face, dataset. The paper-specific method or result selected for transfer review is: **Human CAD construction sequences plus a reconstruction environment**.

## Principal findings

- **Paper finding (conservative paraphrase):** Human CAD construction sequences plus a reconstruction environment
- **Reviewer interpretation:** data for learning realistic part-construction priors
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** data for learning realistic part-construction priors This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Human CAD construction sequences plus a reconstruction environment** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Register the dataset or benchmark behind 'Human CAD construction sequences plus a reconstruction environment' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 24 pages, 99,885 characters, 16,116 words.
- Pages with substantial extractable text: 24/24.
- High-information cue pages sampled from across the paper: 2, 3, 4, 7, 9, 10, 11, 13. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: discussion, introduction, limitations, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
