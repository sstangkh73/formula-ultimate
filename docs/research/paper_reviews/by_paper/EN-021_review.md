# EN-021: Lithium-ion battery degradation: how to model it

Thai companion: `EN-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | S. O’Kane, W. Ai, Ganesh Madabattula, Diego Alonso Alvarez, R. Timms, V. Sulzer, J. Edge, Billy Wu, G. Offer, M. Marinescu |
| Year | 2022 |
| Venue | Physical Chemistry, Chemical Physics - PCCP |
| DOI | Not recorded |
| arXiv | 2112.02037 |
| Canonical record | [https://arxiv.org/abs/2112.02037](https://arxiv.org/abs/2112.02037) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-021_Kane2022_lithium-ion-battery-degradation-how-to-model-it.pdf) |
| Source SHA-256 | `f6eeacc5f62a2070d34c0b86107327f4ed95eea3afee42789d49027b303a5ef7` |
| Full-text coverage | 37/37 pages (100.00%); 14,394 extracted words |

## Research question

How does Lithium-ion battery degradation: how to model it model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, empirical/experimental evidence, simulation/numerical evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were model, degradation, electrode, lithium, discharge, capacity, plating, cracking. The paper-specific method or result selected for transfer review is: **Coupled degradation mechanisms in PyBaMM**.

## Principal findings

- **Paper finding (conservative paraphrase):** Coupled degradation mechanisms in PyBaMM
- **Reviewer interpretation:** relevant if race energy stores degrade over a stint or season
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant if race energy stores degrade over a stint or season This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Coupled degradation mechanisms in PyBaMM** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Coupled degradation mechanisms in PyBaMM' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 37 pages, 83,891 characters, 14,394 words.
- Pages with substantial extractable text: 37/37.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 14, 16, 19. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
