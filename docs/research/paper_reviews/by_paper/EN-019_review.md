# EN-019: Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models

Thai companion: `EN-019_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Chang-Hui Chen, Ferran Brosa Planella, Kieran O’Regan, Dominika Gastol, W. Dhammika Widanage, Emma Kendrick |
| Year | 2020 |
| Venue | Journal of The Electrochemical Society |
| DOI | 10.1149/1945-7111/ab9050 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1149/1945-7111/ab9050](https://doi.org/10.1149/1945-7111/ab9050) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-019_Chen2020_development-of-experimental-techniques-for-paramet.pdf) |
| Source SHA-256 | `342301e6b2b9f9ea0153b0aa2005f99a67220939863a248d1ae7bf8721af780d` |
| Full-text coverage | 23/23 pages (100.00%); 18,464 extracted words |

## Research question

How does Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, and frequent technical terms were electrode, cell, positive, negative, diffusion, coef, voltage, current. The paper-specific method or result selected for transfer review is: **Measured parameter set for an LG M50 cell (PyBaMM Chen2020)**.

## Principal findings

- **Paper finding (conservative paraphrase):** Measured parameter set for an LG M50 cell (PyBaMM Chen2020)
- **Reviewer interpretation:** real cell data usable for an onboard battery model
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** real cell data usable for an onboard battery model This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Measured parameter set for an LG M50 cell (PyBaMM Chen2020)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Register the dataset or benchmark behind 'Measured parameter set for an LG M50 cell (PyBaMM Chen2020)' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 23 pages, 108,572 characters, 18,464 words.
- Pages with substantial extractable text: 23/23.
- High-information cue pages sampled from across the paper: 2, 3, 5, 7, 11, 13, 16, 18. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
