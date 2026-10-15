# EN-009: Maximum-distance Race Strategies for a Fully Electric Endurance Race Car

Thai companion: `EN-009_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jorn van Kampen, T. Herrmann, Mauro Salazar |
| Year | 2022 |
| Venue | European Journal of Control |
| DOI | Not recorded |
| arXiv | 2111.05784 |
| Canonical record | [https://arxiv.org/abs/2111.05784](https://arxiv.org/abs/2111.05784) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-009_Kampen2022_maximum-distance-race-strategies-for-a-fully-elect.pdf) |
| Source SHA-256 | `bee9d5099a17a16ebdea67d9bbd8aad4ab17e0e8fb59a4ffa202ef3da965c2a6` |
| Full-text coverage | 8/8 pages (100.00%); 7,407 extracted words |

## Research question

How does Maximum-distance Race Strategies for a Fully Electric Endurance Race Car model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were stint, time, race, control, optimal, energy, problem, battery. The paper-specific method or result selected for transfer review is: **Endurance strategy under fixed energy with pit decisions**.

## Principal findings

- **Paper finding (conservative paraphrase):** Endurance strategy under fixed energy with pit decisions
- **Reviewer interpretation:** relevant to race-long energy budgeting
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to race-long energy budgeting This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Endurance strategy under fixed energy with pit decisions** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Endurance strategy under fixed energy with pit decisions' against the target below. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 42,466 characters, 7,407 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
