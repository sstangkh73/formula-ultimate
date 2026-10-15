# SI-018: On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming

Thai companion: `SI-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Andreas Wächter, Lorenz T. Biegler |
| Year | 2006 |
| Venue | Mathematical Programming |
| DOI | 10.1007/s10107-004-0559-y |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1007/s10107-004-0559-y](https://doi.org/10.1007/s10107-004-0559-y) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-018_Wachter2006_on-the-implementation-of-an-interior-point-filter.pdf) |
| Source SHA-256 | `75e2147b1e520bd534de21f41218f8ae12e89859befae999aa8e00346b3bdc3b` |
| Full-text coverage | 28/28 pages (100.00%); 14,872 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were step, algorithm, iteration, method, restoration, phase, problem, lter. The paper-specific method or result selected for transfer review is: **IPOPT, the NLP solver used by most published minimum-lap-time work**.

## Principal findings

- **Paper finding (conservative paraphrase):** IPOPT, the NLP solver used by most published minimum-lap-time work
- **Reviewer interpretation:** know its convergence behaviour before trusting a lap
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** know its convergence behaviour before trusting a lap This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **IPOPT, the NLP solver used by most published minimum-lap-time work** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'IPOPT, the NLP solver used by most published minimum-lap-time work' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 28 pages, 83,169 characters, 14,872 words.
- Pages with substantial extractable text: 28/28.
- High-information cue pages sampled from across the paper: 1, 2, 3, 9, 11, 12, 13, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
