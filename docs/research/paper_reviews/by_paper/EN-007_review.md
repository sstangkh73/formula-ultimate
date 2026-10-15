# EN-007: Low-level Online Control of the Formula 1 Power Unit with Feedforward Cylinder Deactivation

Thai companion: `EN-007_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Marc-Philippe Neumann, Giona Fieni, Camillo Balerna, Pol Duhr, Alberto Cerofolini, C. Onder |
| Year | 2023 |
| Venue | IEEE Transactions on Vehicular Technology |
| DOI | Not recorded |
| arXiv | 2303.00372 |
| Canonical record | [https://arxiv.org/abs/2303.00372](https://arxiv.org/abs/2303.00372) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-007_Neumann2023_low-level-online-control-of-the-formula-1-power-un.pdf) |
| Source SHA-256 | `b99fa3e927275e54f58df0623a98d53b78aa8fdba9b04a777b8a0bfff7f6dcbf` |
| Full-text coverage | 16/16 pages (100.00%); 14,479 extracted words |

## Research question

How does Low-level Online Control of the Formula 1 Power Unit with Feedforward Cylinder Deactivation model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were control, power, energy, online, controller, driver, engine, velocity. The paper-specific method or result selected for transfer review is: **Online F1 power-unit control**.

## Principal findings

- **Paper finding (conservative paraphrase):** Online F1 power-unit control
- **Reviewer interpretation:** shows real-time constraints on energy strategies
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** shows real-time constraints on energy strategies This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Online F1 power-unit control** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Online F1 power-unit control' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 85,658 characters, 14,479 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 2, 3, 8, 11, 12, 13, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
