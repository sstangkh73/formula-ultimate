# EN-012: Battery model impact on time-optimal co-design for electric racing cars: review and application

Thai companion: `EN-012_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | G. Riva, Stefano Radrizzani, Giulio Panzani |
| Year | 2023 |
| Venue | IEEE Transactions on Transportation Electrification |
| DOI | Not recorded |
| arXiv | 2312.17003 |
| Canonical record | [https://arxiv.org/abs/2312.17003](https://arxiv.org/abs/2312.17003) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-012_Riva2023_battery-model-impact-on-time-optimal-co-design-for.pdf) |
| Source SHA-256 | `cf3c7217b631b41703a5a946fa9487ccf0f88b8334c2cd438803a0544fa9d4a6` |
| Full-text coverage | 12/12 pages (100.00%); 10,936 extracted words |

## Research question

Which battery-model details are necessary for race-car sizing, and which are necessary for physically informative optimal control?

## Method and evidence

The paper places battery models of increasing detail inside a time-optimal electric-race-car co-design problem, comparing a simple datasheet model with models that include state-of-charge-dependent open-circuit voltage and more realistic electrical behavior; both convex and nonlinear formulations use 15 m spatial steps (pp. 5-9).

## Principal findings

- **Paper finding (conservative paraphrase):** The simple model gives consistent battery-sizing results, while detailed models are needed to study credible control-variable evolution. For the detailed models, race-time difference between 24 and 25 parallel cells is negligible; convex relaxation can also yield non-physical energy-variable profiles (pp. 1-2, 9, 11).
- **Reviewer interpretation:** The paper does not show a generic architecture-ranking reversal; it shows a narrower fidelity split: simple models may suffice for sizing, but not for interpreting optimal energy-control trajectories.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** The paper does not show a generic architecture-ranking reversal; it shows a narrower fidelity split: simple models may suffice for sizing, but not for interpreting optimal energy-control trajectories. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The result is specific to the studied electric race-car problem, battery parameterization, 15 m discretization, and convex/non-convex formulations. It does not include every storage chemistry, degradation pathway, containment, or full thermal architecture. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The paper does not show a generic architecture-ranking reversal; it shows a narrower fidelity split: simple models may suffice for sizing, but not for interpreting optimal energy-control trajectories.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Use the simple model only for a sizing pre-screen; require the state-dependent model for control interpretation and compare both by forward replay, energy/heat closure, and ranking stability before Work 120 promotion. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 12 pages, 64,333 characters, 10,936 words.
- Pages with substantial extractable text: 12/12.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
