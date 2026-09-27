# EN-016: Joint Design and Control of Electric Vehicle Propulsion Systems

Thai companion: `EN-016_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Frans Verbruggen, Mauro Salazar, Marco Pavone, Theo Hofman |
| Year | 2020 |
| Venue | 2020 European Control Conference (ECC) |
| DOI | 10.23919/ecc51009.2020.9143869 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.23919/ecc51009.2020.9143869](https://doi.org/10.23919/ecc51009.2020.9143869) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-016_Verbruggen2020_joint-design-and-control-of-electric-vehicle-propu.pdf) |
| Source SHA-256 | `77a95fd01749dded8c179045656865efc1396ff0178770c3f4f06467c34d37c0` |
| Full-text coverage | 8/8 pages (100.00%); 6,917 extracted words |

## Research question

How does Joint Design and Control of Electric Vehicle Propulsion Systems model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were electric, motor, battery, power, transmission, model, cycle, vehicle. The paper-specific method or result selected for transfer review is: **Co-design of electric propulsion components and control**.

## Principal findings

- **Paper finding (conservative paraphrase):** Co-design of electric propulsion components and control
- **Reviewer interpretation:** method for sizing components within a chosen topology
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** method for sizing components within a chosen topology This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Co-design of electric propulsion components and control** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Co-design of electric propulsion components and control' against the target below. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 38,543 characters, 6,917 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 2, 3, 4, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
