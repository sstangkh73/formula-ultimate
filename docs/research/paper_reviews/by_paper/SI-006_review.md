# SI-006: preCICE v2: A sustainable and user-friendly coupling library

Thai companion: `SI-006_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | G. Chourdakis, Kyle Davis, Benjamin Rodenberg, Miriam Schulte, Frédéric Simonis, B. Uekermann, G. Abrams, H. Bungartz, Lucia Cheung Yau, I. Desai, K. Eder, Richard Hertrich, Florian Lindner, A. Rusch, D. Sashko, David Schneider, A. Totounferoush, Dominik Volland, Peter Vollmer, Oguz Ziya Koseomur |
| Year | 2022 |
| Venue | Open Research Europe |
| DOI | Not recorded |
| arXiv | 2109.14470 |
| Canonical record | [https://arxiv.org/abs/2109.14470](https://arxiv.org/abs/2109.14470) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-006_Chourdakis2022_precice-v2-a-sustainable-and-user-friendly-couplin.pdf) |
| Source SHA-256 | `9a72ccfb27a218ddd6bb030924d86482c2cc4756927e423202a3bf85efeacc8a` |
| Full-text coverage | 47/47 pages (100.00%); 29,074 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in preCICE v2: A sustainable and user-friendly coupling library is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, simulation/numerical evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, and frequent technical terms were precice, coupling, mapping, adapter, data, solver, library, openfoam. The paper-specific method or result selected for transfer review is: **Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration**.

## Principal findings

- **Paper finding (conservative paraphrase):** Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration
- **Reviewer interpretation:** relevant to coupled thermal-solid work (Work 115)
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to coupled thermal-solid work (Work 115) This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 47 pages, 181,190 characters, 29,074 words.
- Pages with substantial extractable text: 47/47.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 9, 11, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
