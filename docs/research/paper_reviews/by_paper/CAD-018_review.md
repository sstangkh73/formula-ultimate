# CAD-018: Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations

Thai companion: `CAD-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Heinrich Jiang, Hager Yasser Mohamed, Alexander Hitt, V. Lomakina, He-Nan Jiang, J. Jang |
| Year | 2026 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2609.11573 |
| Canonical record | [https://arxiv.org/abs/2609.11573](https://arxiv.org/abs/2609.11573) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-018_Jiang2026_learn-the-solid-not-the-file-canonical-inputs-for.pdf) |
| Source SHA-256 | `933d6b844ee8fa5fef9cf36c697b9042f92c4be752a2905cf67b0f10980f2fff` |
| Full-text coverage | 18/18 pages (100.00%); 11,062 extracted words |

## Research question

Does Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were b-rep, solid, same, surface, face, features, frame, faces. The paper-specific method or result selected for transfer review is: **Argues learned models must see a canonical solid, not file-order artefacts**.

## Principal findings

- **Paper finding (conservative paraphrase):** Argues learned models must see a canonical solid, not file-order artefacts
- **Reviewer interpretation:** the same concern as our deterministic geometry identity and hashing
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the same concern as our deterministic geometry identity and hashing This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Argues learned models must see a canonical solid, not file-order artefacts** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Argues learned models must see a canonical solid, not file-order artefacts' against the target below. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 67,095 characters, 11,062 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
