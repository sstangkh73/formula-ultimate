# CAD-016: ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility

Thai companion: `CAD-016_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Yun-Sheng Tian, Karl D. D. Willis, Bassel Al Omari, Jieliang Luo, Pingchuan Ma, Yichen Li, Farhad Javid, Edward Gu, Joshua Jacob, S. Sueda, Hui Li, Sachin Chitta, Wojciech Matusik |
| Year | 2024 |
| Venue | IEEE International Conference on Robotics and Automation |
| DOI | Not recorded |
| arXiv | 2309.16909 |
| Canonical record | [https://arxiv.org/abs/2309.16909](https://arxiv.org/abs/2309.16909) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-016_Tian2024_asap-automated-sequence-planning-for-complex-robot.pdf) |
| Source SHA-256 | `3cad226956e6dd20cbe8a836cea6d35d8071631386a60c6284b7ee536387bb46` |
| Full-text coverage | 7/7 pages (100.00%); 6,362 extracted words |

## Research question

Does ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were assembly, parts, sequence, part, planning, assemblies, sequences, algorithm. The paper-specific method or result selected for transfer review is: **Assembly-sequence planning with gravity and stability checks**.

## Principal findings

- **Paper finding (conservative paraphrase):** Assembly-sequence planning with gravity and stability checks
- **Reviewer interpretation:** relevant to manufacturing handoff (Work 130)
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to manufacturing handoff (Work 130) This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Assembly-sequence planning with gravity and stability checks** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Build a bounded diagnostic pilot from 'Assembly-sequence planning with gravity and stability checks' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 7 pages, 39,754 characters, 6,362 words.
- Pages with substantial extractable text: 7/7.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
