# SI-001: DiffTaichi: Differentiable Programming for Physical Simulation

Thai companion: `SI-001_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Yuanming Hu, Luke Anderson, Tzu-Mao Li, Qi Sun, N. Carr, Jonathan Ragan-Kelley, F. Durand |
| Year | 2020 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 1910.00935 |
| Canonical record | [https://arxiv.org/abs/1910.00935](https://arxiv.org/abs/1910.00935) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-001_Hu2020_difftaichi-differentiable-programming-for-physical.pdf) |
| Source SHA-256 | `88837aafd34badf97251153106530ce546705e64630fa7f1d94849b391a6e4be` |
| Full-text coverage | 20/20 pages (100.00%); 9,204 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in DiffTaichi: Differentiable Programming for Physical Simulation is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were differentiable, simulation, difftaichi, physical, time, gradient, programming, simulator. The paper-specific method or result selected for transfer review is: **Differentiable simulation language**.

## Principal findings

- **Paper finding (conservative paraphrase):** Differentiable simulation language
- **Reviewer interpretation:** a route to gradient refinement inside an admitted topology, with the caveat that gradients do not prove accuracy
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a route to gradient refinement inside an admitted topology, with the caveat that gradients do not prove accuracy This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Differentiable simulation language** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Differentiable simulation language' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 20 pages, 58,251 characters, 9,204 words.
- Pages with substantial extractable text: 20/20.
- High-information cue pages sampled from across the paper: 1, 2, 6, 8, 13, 16, 20. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
