# SI-012: Discrete mechanics and variational integrators

Thai companion: `SI-012_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | J. E. Marsden, M. West |
| Year | 2001 |
| Venue | Acta Numerica |
| DOI | 10.1017/s096249290100006x |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1017/s096249290100006x](https://doi.org/10.1017/s096249290100006x) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-012_Marsden2001_discrete-mechanics-and-variational-integrators.pdf) |
| Source SHA-256 | `f9e26f64d6350e7b868334c84c3da15084835a92e6978b98dca61a2f414c0543` |
| Full-text coverage | 158/158 pages (100.00%); 62,091 extracted words |

## Research question

Which simulation, coupling, differentiation, or optimal-control capability in Discrete mechanics and variational integrators is accurate and stable enough for a Formula Ultimate evaluator?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were discrete, lagrangian, hamiltonian, extended, equations, will, variational, symplectic. The paper-specific method or result selected for transfer review is: **Structure-preserving integrators with bounded energy error**.

## Principal findings

- **Paper finding (conservative paraphrase):** Structure-preserving integrators with bounded energy error
- **Reviewer interpretation:** the theory behind treating energy residuals as observable outputs
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the theory behind treating energy residuals as observable outputs This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Structure-preserving integrators with bounded energy error** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Structure-preserving integrators with bounded energy error' against the target below. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 158 pages, 325,611 characters, 62,091 words.
- Pages with substantial extractable text: 158/158.
- High-information cue pages sampled from across the paper: 3, 4, 42, 43, 46, 82, 83, 88. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
