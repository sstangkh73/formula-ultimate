# EN-023: Parameterization of a Physico-Chemical Model of a Lithium-Ion Battery: I. Determination of Parameters

Thai companion: `EN-023_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Madeleine Ecker, Thi Kim Dung Tran, Philipp Dechent, Stefan Käbitz, Alexander Warnecke, Dirk Uwe Sauer |
| Year | 2015 |
| Venue | Journal of The Electrochemical Society |
| DOI | 10.1149/2.0551509jes |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1149/2.0551509jes](https://doi.org/10.1149/2.0551509jes) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-023_Ecker2015_parameterization-of-a-physico-chemical-model-of-a.pdf) |
| Source SHA-256 | `57e7c40a758d8da43362c34b2ea1f8671101075f362c8259d7ebf9d562dea1fd` |
| Full-text coverage | 14/14 pages (100.00%); 12,341 extracted words |

## Research question

How does Parameterization of a Physico-Chemical Model of a Lithium-Ion Battery: I. Determination of Parameters model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **technical/methodological study**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, and frequent technical terms were material, diffusion, cell, graphite, charge, current, used, electrode. The paper-specific method or result selected for transfer review is: **Measured Kokam cell parameters (PyBaMM Ecker2015)**.

## Principal findings

- **Paper finding (conservative paraphrase):** Measured Kokam cell parameters (PyBaMM Ecker2015)
- **Reviewer interpretation:** a second measured data set for cross-checking battery models
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a second measured data set for cross-checking battery models This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Measured Kokam cell parameters (PyBaMM Ecker2015)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Register the dataset or benchmark behind 'Measured Kokam cell parameters (PyBaMM Ecker2015)' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 71,229 characters, 12,341 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
