# SI-021: Co-simulation: State of the art

Thai companion: `SI-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | C. Gomes, Casper Thule, David Broman, P. Larsen, H. Vangheluwe |
| Year | 2018 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 1702.00686 |
| Canonical record | [https://arxiv.org/abs/1702.00686](https://arxiv.org/abs/1702.00686) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-021_Gomes2018_co-simulation-state-of-the-art.pdf) |
| Source SHA-256 | `5ce85c761a65389ca10448f701514e0a5f8596e0c14815972d4ad7b0316be438` |
| Full-text coverage | 157/157 pages (100.00%); 47,789 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in Co-simulation: State of the art is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, discussion, introduction, methods, results, and frequent technical terms were co-simulation, simulation, time, model, unit, step, system, systems. The paper-specific method or result selected for transfer review is: **Survey of co-simulation orchestration, stability and accuracy**.

## Principal findings

- **Paper finding (conservative paraphrase):** Survey of co-simulation orchestration, stability and accuracy
- **Reviewer interpretation:** background for coupling many subsystem models
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** background for coupling many subsystem models This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Survey of co-simulation orchestration, stability and accuracy** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Survey of co-simulation orchestration, stability and accuracy' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 157 pages, 303,080 characters, 47,789 words.
- Pages with substantial extractable text: 157/157.
- High-information cue pages sampled from across the paper: 28, 30, 33, 34, 36, 45, 55, 84. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, discussion, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
