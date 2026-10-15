# EN-010: Optimal Endurance Race Strategies for a Fully Electric Race Car under Thermal Constraints

Thai companion: `EN-010_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jorn van Kampen, T. Herrmann, T. Hofman, Mauro Salazar |
| Year | 2023 |
| Venue | IEEE Transactions on Control Systems Technology |
| DOI | Not recorded |
| arXiv | 2301.08060 |
| Canonical record | [https://arxiv.org/abs/2301.08060](https://arxiv.org/abs/2301.08060) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-010_Kampen2023_optimal-endurance-race-strategies-for-a-fully-elec.pdf) |
| Source SHA-256 | `09aae4eb3913e5caa27cd89e3138edfdf7c6f400cee26e9e5e92f0814baa9f32` |
| Full-text coverage | 16/16 pages (100.00%); 13,996 extracted words |

## Research question

How does Optimal Endurance Race Strategies for a Fully Electric Race Car under Thermal Constraints model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **technical/methodological study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were stint, battery, time, temperature, race, optimal, charge, energy. The paper-specific method or result selected for transfer review is: **Adds battery and motor thermal limits to endurance strategy**.

## Principal findings

- **Paper finding (conservative paraphrase):** Adds battery and motor thermal limits to endurance strategy
- **Reviewer interpretation:** a direct coupling of our thermal and energy gates
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a direct coupling of our thermal and energy gates This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Adds battery and motor thermal limits to endurance strategy** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Adds battery and motor thermal limits to endurance strategy' against the target below. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 82,128 characters, 13,996 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 6, 11, 13, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
