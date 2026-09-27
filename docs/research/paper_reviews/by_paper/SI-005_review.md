# SI-005: OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization

Thai companion: `SI-005_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Justin S. Gray, John T. Hwang, Joaquim R. R. A. Martins, Kenneth T. Moore, Bret A. Naylor |
| Year | 2019 |
| Venue | Structural and Multidisciplinary Optimization |
| DOI | 10.1007/s00158-019-02211-z |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1007/s00158-019-02211-z](https://doi.org/10.1007/s00158-019-02211-z) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-005_Gray2019_openmdao-an-open-source-framework-for-multidiscipl.pdf) |
| Source SHA-256 | `2968ee16a5ed3fe48d20e12029f3d93579ce9962eb728a58469ee96825f75b44` |
| Full-text coverage | 30/30 pages (100.00%); 21,243 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, simulation/numerical evidence, mathematical/formal evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, methods, and frequent technical terms were model, openmdao, derivatives, optimization, linear, design, analysis, https. The paper-specific method or result selected for transfer review is: **Coupled-analysis orchestration with derivatives**.

## Principal findings

- **Paper finding (conservative paraphrase):** Coupled-analysis orchestration with derivatives
- **Reviewer interpretation:** a pattern for design/control/energy/structure coupling
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a pattern for design/control/energy/structure coupling This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Coupled-analysis orchestration with derivatives** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Coupled-analysis orchestration with derivatives' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 30 pages, 134,300 characters, 21,243 words.
- Pages with substantial extractable text: 30/30.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7, 14, 24. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
