# ST-015: Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics

Thai companion: `ST-015_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Minchen Li, Zachary Ferguson, Teseo Schneider, Timothy Langlois, Denis Zorin, Daniele Panozzo, Chenfanfu Jiang, Danny M. Kaufman |
| Year | 2020 |
| Venue | ACM Transactions on Graphics |
| DOI | 10.1145/3386569.3392425 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1145/3386569.3392425](https://doi.org/10.1145/3386569.3392425) |
| Library topic | Structures, meshing, contact, and topology optimization |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/05_structures_meshing_contact/ST-015_Li2020_incremental-potential-contact-intersection-and-inv.pdf) |
| Source SHA-256 | `f0bd0b51ae00f022bd69fc54592d323a8a688cbbe9cc38c5939b8c18a31df0b5` |
| Full-text coverage | 20/20 pages (100.00%); 19,060 extracted words |

## Research question

Can contact dynamics remain intersection- and element-inversion-free under large deformation while exposing separate physical and geometric accuracy tolerances?

## Method and evidence

IPC formulates contact as barrier potentials inside implicit nonlinear elastodynamics, uses continuous collision detection and a custom Newton-type solver, and benchmarks deformable/self-contact cases with declared material, time-step, and geometric tolerances (pp. 1, 7, 10, 16).

## Principal findings

- **Paper finding (conservative paraphrase):** The method produces intersection- and inversion-free trajectories across the reported examples and permits independent dynamics and surface-conformation tolerances (p. 1). Resolution raises contact count, iteration count, memory roughly linearly, and timing slightly superlinearly in the mat study (p. 16).
- **Reviewer interpretation:** The paper treats missed collision and infeasible linearized constraints as numerical failures rather than hiding them with non-physical fail-safes (pp. 5, 7).
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** The paper treats missed collision and infeasible linearized constraints as numerical failures rather than hiding them with non-physical fail-safes (pp. 5, 7). This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Cost rises with contact complexity and mesh resolution, and the authors give no general convergence guarantee for their lagged friction variables, except stiction (conclusion, p. 20). Geometric non-penetration is not constitutive validation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The paper treats missed collision and infeasible linearized constraints as numerical failures rather than hiding them with non-physical fail-safes (pp. 5, 7).** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **structural/contact evaluator, mesh-refinement evidence, and material-failure gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | structural/contact evaluator, mesh-refinement evidence, and material-failure gate |
| Proposed change | Add IPC as an independent contact candidate for Work 114/123, with CCD failure, barrier tolerance, friction convergence, energy residual, reaction recovery, and mesh refinement all retained in the ledger. |
| Experiment and control | Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads. |
| Acceptance and failure evidence | Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 20 pages, 120,111 characters, 19,060 words.
- Pages with substantial extractable text: 20/20.
- High-information cue pages sampled from across the paper: 1, 2, 5, 6, 7, 8, 10, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
