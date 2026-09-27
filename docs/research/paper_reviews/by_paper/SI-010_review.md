# SI-010: Dojo: A Differentiable Physics Engine for Robotics

Thai companion: `SI-010_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Taylor A. Howell, Simon Le Cleac'h, Jan Brudigam, Qianzhong Chen, Jian-Kai Sun, J. Kolter, Mac Schwager, Zachary Manchester |
| Year | 2022 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2203.00806 |
| Canonical record | [https://arxiv.org/abs/2203.00806](https://arxiv.org/abs/2203.00806) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-010_Howell2022_dojo-a-differentiable-physics-engine-for-robotics.pdf) |
| Source SHA-256 | `729928039c101eba82d02ddfe215d7d19e592414bff32f690014be9f3e071bf7` |
| Full-text coverage | 18/18 pages (100.00%); 13,906 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in Dojo: A Differentiable Physics Engine for Robotics is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were dojo, contact, simulation, gradients, optimization, dynamics, robotics, solver. The paper-specific method or result selected for transfer review is: **Differentiable contact via interior-point complementarity**.

## Principal findings

- **Paper finding (conservative paraphrase):** Differentiable contact via interior-point complementarity
- **Reviewer interpretation:** a gradient-through-contact option for ground interaction
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a gradient-through-contact option for ground interaction This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Differentiable contact via interior-point complementarity** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Differentiable contact via interior-point complementarity' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 86,101 characters, 13,906 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
