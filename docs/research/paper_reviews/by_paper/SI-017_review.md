# SI-017: CasADi: a software framework for nonlinear optimization and optimal control

Thai companion: `SI-017_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Joel A. E. Andersson, Joris Gillis, Greg Horn, James B. Rawlings, Moritz Diehl |
| Year | 2019 |
| Venue | Mathematical Programming Computation |
| DOI | 10.1007/s12532-018-0139-4 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1007/s12532-018-0139-4](https://doi.org/10.1007/s12532-018-0139-4) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-017_Andersson2019_casadi-a-software-framework-for-nonlinear-optimiza.pdf) |
| Source SHA-256 | `55106413bd7b129b173b32fac5007de604031a3296df731cd9a37bfc4c214239` |
| Full-text coverage | 33/33 pages (100.00%); 16,702 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in CasADi: a software framework for nonlinear optimization and optimal control is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were introduction, and frequent technical terms were control, casadi, optimization, function, nonlinear, optimal, problems, page. The paper-specific method or result selected for transfer review is: **The standard open tool for direct-collocation minimum-lap-time problems**.

## Principal findings

- **Paper finding (conservative paraphrase):** The standard open tool for direct-collocation minimum-lap-time problems
- **Reviewer interpretation:** needed for optimised driver baselines
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** needed for optimised driver baselines This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The standard open tool for direct-collocation minimum-lap-time problems** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'The standard open tool for direct-collocation minimum-lap-time problems' against the target below. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 33 pages, 94,129 characters, 16,702 words.
- Pages with substantial extractable text: 33/33.
- High-information cue pages sampled from across the paper: 2, 3, 10, 13, 16, 18, 20, 22. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
