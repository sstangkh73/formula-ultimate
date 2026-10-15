# EN-030: Competitors-Aware Stochastic Lap Strategy Optimisation for Race Hybrid Vehicles

Thai companion: `EN-030_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | L. Paparusso, M. Riani, F. Ruggeri, F. Braghin |
| Year | 2022 |
| Venue | IEEE Transactions on Vehicular Technology |
| DOI | Not recorded |
| arXiv | 2203.00084 |
| Canonical record | [https://arxiv.org/abs/2203.00084](https://arxiv.org/abs/2203.00084) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-030_Paparusso2022_competitors-aware-stochastic-lap-strategy-optimisa.pdf) |
| Source SHA-256 | `8e4cee7bfb2d4af13983e6f7fe8fdc4ea238a11833b7659ad7efeaa907349e7f` |
| Full-text coverage | 15/15 pages (100.00%); 10,887 extracted words |

## Research question

How does Competitors-Aware Stochastic Lap Strategy Optimisation for Race Hybrid Vehicles model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were time, strategy, competitors, energy, optimal, optimisation, sector, speed. The paper-specific method or result selected for transfer review is: **Stochastic hybrid energy strategy accounting for competitors**.

## Principal findings

- **Paper finding (conservative paraphrase):** Stochastic hybrid energy strategy accounting for competitors
- **Reviewer interpretation:** relevant if race time depends on interaction, not only on the lone vehicle
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant if race time depends on interaction, not only on the lone vehicle This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Stochastic hybrid energy strategy accounting for competitors** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Stochastic hybrid energy strategy accounting for competitors' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 15 pages, 63,477 characters, 10,887 words.
- Pages with substantial extractable text: 15/15.
- High-information cue pages sampled from across the paper: 1, 2, 7, 8, 9, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
