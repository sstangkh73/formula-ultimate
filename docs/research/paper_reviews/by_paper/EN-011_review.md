# EN-011: Human-in-the-loop Energy and Thermal Management for Electric Racing Cars through Optimization-based Control

Thai companion: `EN-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Erik van den Eshof, Jorn van Kampen, Mauro Salazar |
| Year | 2024 |
| Venue | European Journal of Control |
| DOI | Not recorded |
| arXiv | 2412.15379 |
| Canonical record | [https://arxiv.org/abs/2412.15379](https://arxiv.org/abs/2412.15379) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-011_Eshof2024_human-in-the-loop-energy-and-thermal-management-fo.pdf) |
| Source SHA-256 | `be1a9d8f70b9c5ceb6fc60624ad539401898467880746761c7a3974d424635f1` |
| Full-text coverage | 7/7 pages (100.00%); 6,136 extracted words |

## Research question

How does Human-in-the-loop Energy and Thermal Management for Electric Racing Cars through Optimization-based Control model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were energy, problem, stint, time, electric, control, kinetic, racing. The paper-specific method or result selected for transfer review is: **Optimisation-based energy and thermal guidance delivered to a human driver**.

## Principal findings

- **Paper finding (conservative paraphrase):** Optimisation-based energy and thermal guidance delivered to a human driver
- **Reviewer interpretation:** relevant to realistic driver execution of optimal strategies
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to realistic driver execution of optimal strategies This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Optimisation-based energy and thermal guidance delivered to a human driver** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Optimisation-based energy and thermal guidance delivered to a human driver' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 7 pages, 37,419 characters, 6,136 words.
- Pages with substantial extractable text: 7/7.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
