# CAD-015: Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly

Thai companion: `CAD-015_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Yunsheng Tian, Jie Xu, Yichen Li, Jieliang Luo, Shinjiro Sueda, Hui Li, Karl D. D. Willis, Wojciech Matusik |
| Year | 2022 |
| Venue | ACM Transactions on Graphics |
| DOI | 10.1145/3550454.3555525 |
| arXiv | 2211.03977 |
| Canonical record | [https://doi.org/10.1145/3550454.3555525](https://doi.org/10.1145/3550454.3555525) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-015_Tian2022_assemble-them-all-physics-based-planning-for-gener.pdf) |
| Source SHA-256 | `c50242c262ee42e158b7e051157e14323b907d27e0c069f4a107d5b305cdb7c6` |
| Full-text coverage | 15/15 pages (100.00%); 11,928 extracted words |

## Research question

Does Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were introduction, limitations, results, and frequent technical terms were assembly, planning, disassembly, parts, path, state, assemblies, physics-based. The paper-specific method or result selected for transfer review is: **Physics-based disassembly planning proves an assembly can be put together**.

## Principal findings

- **Paper finding (conservative paraphrase):** Physics-based disassembly planning proves an assembly can be put together
- **Reviewer interpretation:** a buildability gate for generated multi-part vehicles
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a buildability gate for generated multi-part vehicles This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Physics-based disassembly planning proves an assembly can be put together** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Physics-based disassembly planning proves an assembly can be put together' against the target below. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 15 pages, 74,639 characters, 11,928 words.
- Pages with substantial extractable text: 15/15.
- High-information cue pages sampled from across the paper: 1, 2, 6, 7, 8, 9, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: introduction, limitations, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
