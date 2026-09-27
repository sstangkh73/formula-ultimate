# EN-022: A continuum of physics-based lithium-ion battery models reviewed

Thai companion: `EN-022_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ferran Brosa Planella, W. Ai, Adam M. Boyce, Abir Ghosh, I. Korotkin, Smita Sahu, V. Sulzer, R. Timms, T. Tranter, M. Zyskin, S. Cooper, J. Edge, J. Foster, M. Marinescu, Billy Wu, G. Richardson |
| Year | 2022 |
| Venue | Progress in Energy |
| DOI | Not recorded |
| arXiv | 2203.16091 |
| Canonical record | [https://arxiv.org/abs/2203.16091](https://arxiv.org/abs/2203.16091) |
| Library topic | Energy storage, powertrain, and race energy management |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/08_energy_powertrain/EN-022_Planella2022_a-continuum-of-physics-based-lithium-ion-battery-m.pdf) |
| Source SHA-256 | `f27ddf8166e5b2f22c055d340bc35df7d7f3122878e5f970a4ff3a4b8f373022` |
| Full-text coverage | 50/50 pages (100.00%); 28,303 extracted words |

## Research question

How does A continuum of physics-based lithium-ion battery models reviewed model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, empirical/experimental evidence, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were model, models, electrode, electrolyte, battery, lithium, particle, current. The paper-specific method or result selected for transfer review is: **Reviews the hierarchy of physics-based cell models**.

## Principal findings

- **Paper finding (conservative paraphrase):** Reviews the hierarchy of physics-based cell models
- **Reviewer interpretation:** a map for choosing battery fidelity per gate
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a map for choosing battery fidelity per gate This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Reviews the hierarchy of physics-based cell models** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Reviews the hierarchy of physics-based cell models' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation. |
| Acceptance and failure evidence | Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 50 pages, 173,212 characters, 28,303 words.
- Pages with substantial extractable text: 50/50.
- High-information cue pages sampled from across the paper: 2, 11, 12, 21, 22, 27, 28, 29. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
