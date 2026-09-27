# CAD-022: HoLa: B-Rep Generation using a Holistic Latent Representation

Thai companion: `CAD-022_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Yilin Liu, Duoteng Xu, Xingyao Yu, Xiang Xu, Daniel Cohen-Or, Hao Zhang, Hui Huang |
| Year | 2025 |
| Venue | ACM Transactions on Graphics |
| DOI | 10.1145/3730842 |
| arXiv | 2504.14257 |
| Canonical record | [https://doi.org/10.1145/3730842](https://doi.org/10.1145/3730842) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-022_Liu2025_hola-b-rep-generation-using-a-holistic-latent-repr.pdf) |
| Source SHA-256 | `57c15e096b5ee0c48a50fa6716acf733ccddac0c9ea8859b12d2a4da5012a3f0` |
| Full-text coverage | 25/25 pages (100.00%); 14,542 extracted words |

## Research question

Does HoLa: B-Rep Generation using a Holistic Latent Representation represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, limitations, methods, and frequent technical terms were b-rep, latent, generation, surface, models, model, primitives, input. The paper-specific method or result selected for transfer review is: **Single latent space for B-rep geometry and topology**.

## Principal findings

- **Paper finding (conservative paraphrase):** Single latent space for B-rep geometry and topology
- **Reviewer interpretation:** a follow-up to BrepGen for freeform solid proposals
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a follow-up to BrepGen for freeform solid proposals This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Single latent space for B-rep geometry and topology** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Single latent space for B-rep geometry and topology' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 25 pages, 89,518 characters, 14,542 words.
- Pages with substantial extractable text: 25/25.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 7, 12, 13, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, limitations, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
