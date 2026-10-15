# SI-011: A pressure field model for fast, robust approximation of net contact force and moment between nominally rigid objects

Thai companion: `SI-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ryan Elandt, Evan Drumwright, Michael Sherman, A. Ruina |
| Year | 2019 |
| Venue | IEEE/RJS International Conference on Intelligent RObots and Systems |
| DOI | Not recorded |
| arXiv | 1904.11433 |
| Canonical record | [https://arxiv.org/abs/1904.11433](https://arxiv.org/abs/1904.11433) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-011_Elandt2019_a-pressure-field-model-for-fast-robust-approximati.pdf) |
| Source SHA-256 | `b6287d5912239ac53343d6441cfab246df2f5e316c89d3f137bbb75727887c18` |
| Full-text coverage | 8/8 pages (100.00%); 6,568 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in A pressure field model for fast, robust approximation of net contact force and moment between nominally rigid objects is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were contact, pressure, surface, objects, model, rigid, forces, object. The paper-specific method or result selected for transfer review is: **Hydroelastic contact giving distributed pressure rather than point forces**.

## Principal findings

- **Paper finding (conservative paraphrase):** Hydroelastic contact giving distributed pressure rather than point forces
- **Reviewer interpretation:** relevant to contact patches of arbitrary ground-contact endpoints
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to contact patches of arbitrary ground-contact endpoints This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Hydroelastic contact giving distributed pressure rather than point forces** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Hydroelastic contact giving distributed pressure rather than point forces' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 40,478 characters, 6,568 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
