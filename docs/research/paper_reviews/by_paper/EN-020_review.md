# EN-020: An asymptotic derivation of a single particle model with electrolyte

Thai companion: `EN-020_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | S. Marquis, V. Sulzer, R. Timms, Colin P. Please, S. Chapman |
| Year | 2019 |
| Venue | Journal of the Electrochemical Society |
| DOI | Not recorded |
| arXiv | 1905.12553 |
| Canonical record | [https://arxiv.org/abs/1905.12553](https://arxiv.org/abs/1905.12553) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-020_Marquis2019_an-asymptotic-derivation-of-a-single-particle-mode.pdf) |
| Source SHA-256 | `d84860c8a4f7beeac88c07fe86251ad1a49aefc779ad2aef273a9d88ce9e661b` |
| Full-text coverage | 43/43 pages (100.00%); 14,696 extracted words |

## Research question

How does An asymptotic derivation of a single particle model with electrolyte model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence, mathematical/formal evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, and frequent technical terms were model, electrolyte, voltage, spme, electrode, models, page, concentration. The paper-specific method or result selected for transfer review is: **Derives SPMe as a controlled reduction of the DFN model**.

## Principal findings

- **Paper finding (conservative paraphrase):** Derives SPMe as a controlled reduction of the DFN model
- **Reviewer interpretation:** a principled low-fidelity battery rung
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a principled low-fidelity battery rung This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Derives SPMe as a controlled reduction of the DFN model** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Derives SPMe as a controlled reduction of the DFN model' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 43 pages, 77,647 characters, 14,696 words.
- Pages with substantial extractable text: 43/43.
- High-information cue pages sampled from across the paper: 1, 2, 3, 21, 22, 23, 25, 28. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
