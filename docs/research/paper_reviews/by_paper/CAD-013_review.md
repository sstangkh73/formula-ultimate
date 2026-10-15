# CAD-013: JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints

Thai companion: `CAD-013_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Karl D. D. Willis, P. Jayaraman, Hang Chu, Yunsheng Tian, Yifei Li, Daniele Grandi, Aditya Sanghi, Linh-Tam Tran, J. Lambourne, Armando Solar-Lezama, W. Matusik |
| Year | 2022 |
| Venue | Computer Vision and Pattern Recognition |
| DOI | Not recorded |
| arXiv | 2111.12772 |
| Canonical record | [https://arxiv.org/abs/2111.12772](https://arxiv.org/abs/2111.12772) |
| Library topic | CAD, B-rep, assemblies, and geometry generation |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/04_cad_brep_assembly/CAD-013_Willis2022_joinable-learning-bottom-up-assembly-of-parametric.pdf) |
| Source SHA-256 | `1a4f6b4944b07a43ef4489363cf619437a54c9ec6f5362e2a997a62210381485` |
| Full-text coverage | 30/31 pages (96.77%); 18,587 extracted words |

## Research question

Can B-rep graph learning recover joint axes and poses from weak supervision in ordinary parametric CAD assemblies?

## Method and evidence

JoinABLe encodes B-rep faces and edges as graphs, predicts joint-axis entity pairs, and searches joint pose. It uses weak labels from the Fusion 360 Gallery assembly dataset and compares multiple geometric baselines (pp. 1, 22-28).

## Principal findings

- **Paper finding (conservative paraphrase):** The reported joint-axis accuracy is 79.53%, close to the 80% human result and above the tested baselines (p. 1). Performance is higher for hole-based joints; edge length and entity type are important features, while face area can hurt (results appendix, pp. 22-25).
- **Reviewer interpretation:** Equivalent labels materially raise measured accuracy (p. 22), showing that assembly evaluation must distinguish genuine geometric equivalence from forgiving an incorrect mate.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** Equivalent labels materially raise measured accuracy (p. 22), showing that assembly evaluation must distinguish genuine geometric equivalence from forgiving an incorrect mate. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The method predicts joints from dataset regularities and is easier on hole-like interfaces; it does not prove load transfer, tolerance, collision-free motion, fastening detail, or manufacturing feasibility. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Equivalent labels materially raise measured accuracy (p. 22), showing that assembly evaluation must distinguish genuine geometric equivalence from forgiving an incorrect mate.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks |
| Proposed change | Use JoinABLe as a proposal baseline in Work 140, but require exact face/edge grounding, declared DOF, motion probe, interference, and load-path checks before accepting a joint. |
| Experiment and control | Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks. |
| Acceptance and failure evidence | Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 31 pages, 111,462 characters, 18,587 words.
- Pages with substantial extractable text: 30/31.
- High-information cue pages sampled from across the paper: 1, 2, 6, 7, 8, 13, 22, 24. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
