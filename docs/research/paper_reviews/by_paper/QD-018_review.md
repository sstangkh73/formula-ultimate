# QD-018: BOP-Elites, a Bayesian Optimisation algorithm for Quality-Diversity search

Thai companion: `QD-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Paul Kent, J. Branke |
| Year | 2020 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2005.04320 |
| Canonical record | [https://arxiv.org/abs/2005.04320](https://arxiv.org/abs/2005.04320) |
| Library topic | Quality-diversity, novelty, surrogate, and multifidelity search |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/03_search_qd_multifidelity/QD-018_Kent2020_bop-elites-a-bayesian-optimisation-algorithm-for-q.pdf) |
| Source SHA-256 | `fd45d6b4fef012fc8b45db3945cab823662a052e3cd6fea0349439cc6d6c3e70` |
| Full-text coverage | 12/12 pages (100.00%); 4,573 extracted words |

## Research question

How does BOP-Elites, a Bayesian Optimisation algorithm for Quality-Diversity search trade quality, diversity, evaluation cost, and fidelity error in an adaptive search?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, and frequent technical terms were algorithm, function, optimisation, niche, feature, solution, search, objective. The paper-specific method or result selected for transfer review is: **Bayesian optimisation for QD with very few evaluations**.

## Principal findings

- **Paper finding (conservative paraphrase):** Bayesian optimisation for QD with very few evaluations
- **Reviewer interpretation:** relevant when each evaluation is a CFD or FE run
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant when each evaluation is a CFD or FE run This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

QD conclusions depend on descriptor geometry, archive resolution, evaluation budget, and proxy fidelity; archive score alone is not vehicle value. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Bayesian optimisation for QD with very few evaluations** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **QD archive, descriptor schema, resource ledger, and multifidelity promotion policy**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | QD archive, descriptor schema, resource ledger, and multifidelity promotion policy |
| Proposed change | Build a bounded diagnostic pilot from 'Bayesian optimisation for QD with very few evaluations' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare the paper-derived search rule with objective optimization, random search, and MAP-Elites under matched proposals, seeds, wall/CPU/GPU budgets, and stratified high-fidelity audits. |
| Acceptance and failure evidence | Require improved feasible coverage or held-out quality with confidence intervals and no unacceptable proxy false-negative rate; unknown high-fidelity outcomes remain `not_estimable`. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 12 pages, 27,335 characters, 4,573 words.
- Pages with substantial extractable text: 12/12.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
