# CAD-009: SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks

Thai companion: `CAD-009_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Xiang Xu, Karl D. D. Willis, J. Lambourne, Chin-Yi Cheng, P. Jayaraman, Yasutaka Furukawa |
| Year | 2022 |
| Venue | International Conference on Machine Learning |
| DOI | Not recorded |
| arXiv | 2207.04632 |
| Canonical record | [https://arxiv.org/abs/2207.04632](https://arxiv.org/abs/2207.04632) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-009_Xu2022_skexgen-autoregressive-generation-of-cad-construct.pdf) |
| Source SHA-256 | `e7531936b3b73095f979299d386fda8ecce3a712a9d3c194a4d5fddf832eabfa` |
| Full-text coverage | 23/23 pages (100.00%); 7,590 extracted words |

## Research question

Does SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were skexgen, generation, sketch, sequence, geometry, construction, codebooks, topology. The paper-specific method or result selected for transfer review is: **Disentangles topology and geometry codes in CAD sequences**.

## Principal findings

- **Paper finding (conservative paraphrase):** Disentangles topology and geometry codes in CAD sequences
- **Reviewer interpretation:** relevant to separating structural choices from dimensions in the genome
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to separating structural choices from dimensions in the genome This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Disentangles topology and geometry codes in CAD sequences** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Disentangles topology and geometry codes in CAD sequences' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 23 pages, 47,545 characters, 7,590 words.
- Pages with substantial extractable text: 23/23.
- High-information cue pages sampled from across the paper: 1, 2, 4, 5, 6, 7, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
