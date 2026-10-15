# EN-017: Python Battery Mathematical Modelling (PyBaMM)

Thai companion: `EN-017_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Valentin Sulzer, Scott G. Marquis, Robert Timms, Martin Robinson, S. Jon Chapman |
| Year | 2021 |
| Venue | Journal of Open Research Software |
| DOI | 10.5334/jors.309 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.5334/jors.309](https://doi.org/10.5334/jors.309) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-017_Sulzer2021_python-battery-mathematical-modelling-pybamm.pdf) |
| Source SHA-256 | `9b8917cc70b00d64a89bb040b0a041f37141084d203c47b37763ea66b1817b08` |
| Full-text coverage | 8/8 pages (100.00%); 4,348 extracted words |

## Research question

How does Python Battery Mathematical Modelling (PyBaMM) model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, mathematical/formal evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, and frequent technical terms were pybamm, model, models, battery, https, software, modelling, journal. The paper-specific method or result selected for transfer review is: **The battery modelling package already mirrored in private/materials/sources**.

## Principal findings

- **Paper finding (conservative paraphrase):** The battery modelling package already mirrored in private/materials/sources
- **Reviewer interpretation:** the citation for its models and parameter sets
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the citation for its models and parameter sets This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The battery modelling package already mirrored in private/materials/sources** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Register the dataset or benchmark behind 'The battery modelling package already mirrored in private/materials/sources' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 27,862 characters, 4,348 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 2, 4, 5. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
