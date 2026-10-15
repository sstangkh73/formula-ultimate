# SI-020: Energy conservation and power bonds in co-simulations: non-iterative adaptive step size control and error estimation

Thai companion: `SI-020_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Severin Sadjina, Lars T. Kyllingstad, Stian Skjong, E. Pedersen |
| Year | 2017 |
| Venue | Engineering computations |
| DOI | Not recorded |
| arXiv | 1602.06434 |
| Canonical record | [https://arxiv.org/abs/1602.06434](https://arxiv.org/abs/1602.06434) |
| Library topic | Simulation infrastructure and differentiable physics |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/06_simulation_infrastructure/SI-020_Sadjina2017_energy-conservation-and-power-bonds-in-co-simulati.pdf) |
| Source SHA-256 | `bb2e17ce18e507768e371000c81175481dacf7398b0edb5d7f455cb24384c7f1` |
| Full-text coverage | 14/14 pages (100.00%); 10,076 extracted words |

## Research question

Can exchanged power residuals provide a non-iterative error estimate and adaptive macro-step controller for co-simulation?

## Method and evidence

ECCO computes residual power/energy from power bonds at subsystem interfaces and adapts the macro step without rollback or subsystem-internal access. It is tested on linear and nonlinear quarter-car co-simulation variants (pp. 1, 5, 8-11).

## Principal findings

- **Paper finding (conservative paraphrase):** In a reported linear benchmark, residual-energy-based adaptation reduces residual energy by about 90%; alternative system partitioning produces larger errors, showing that coupling topology itself matters (pp. 10-11).
- **Reviewer interpretation:** The error signal is independently observable at the interface rather than constructed by negating a prescribed input, matching the project's need for transferred-energy evidence.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** The error signal is independently observable at the interface rather than constructed by negating a prescribed input, matching the project's need for transferred-energy evidence. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The global-error argument assumes coupling without algebraic loops and the evidence is from quarter-car benchmarks; tolerance choice and subsystem partition remain application-specific. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The error signal is independently observable at the interface rather than constructed by negating a prescribed input, matching the project's need for transferred-energy evidence.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **simulation coupling contract, evaluator applicability registry, and solver-failure ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | simulation coupling contract, evaluator applicability registry, and solver-failure ledger |
| Proposed change | Instrument every Work 123 coupling bond with exchanged effort/flow and residual energy, compare constant and ECCO-adaptive macro steps, and fail promotion when residual-energy reduction does not correlate with independent state/output error. |
| Experiment and control | Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost. |
| Acceptance and failure evidence | Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 58,688 characters, 10,076 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 5, 8, 9, 10, 11, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
