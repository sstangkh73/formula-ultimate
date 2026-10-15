# CAD-019: TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation

Thai companion: `CAD-019_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ming-Ze Sun, Haiyong Jiang, Bingchen Yang, Haoxuan Song, Yidi Li, Jun Xiao, Peter Wonka |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2607.21928 |
| Canonical record | [https://arxiv.org/abs/2607.21928](https://arxiv.org/abs/2607.21928) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-019_Sun2026_tg-diff-coupling-discrete-topology-diffusion-and-t.pdf) |
| Source SHA-256 | `65e4810017865136db25147cc1d13babaaa9bc816eeba5b3d99b2467e1f51651` |
| Full-text coverage | 15/15 pages (100.00%); 11,523 extracted words |

## Research question

Does TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, limitations, methods, results, and frequent technical terms were generation, surface, topology, b-rep, diffusion, surfaces, geometry, generated. The paper-specific method or result selected for transfer review is: **Generates B-rep topology first then geometry**.

## Principal findings

- **Paper finding (conservative paraphrase):** Generates B-rep topology first then geometry
- **Reviewer interpretation:** mirrors the topology-then-dimensions split in our genome
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** mirrors the topology-then-dimensions split in our genome This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Generates B-rep topology first then geometry** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Generates B-rep topology first then geometry' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 15 pages, 73,918 characters, 11,523 words.
- Pages with substantial extractable text: 15/15.
- High-information cue pages sampled from across the paper: 1, 2, 5, 7, 8, 10, 11, 13. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, limitations, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
