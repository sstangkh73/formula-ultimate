# QD-015: Multi-Objective Quality Diversity Optimization

Thai companion: `QD-015_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Thomas Pierrot, Guillaume Richard, Karim Beguir, Antoine Cully |
| Year | 2022 |
| Venue | Annual Conference on Genetic and Evolutionary Computation |
| DOI | Not recorded |
| arXiv | 2202.03057 |
| Canonical record | [https://arxiv.org/abs/2202.03057](https://arxiv.org/abs/2202.03057) |
| Library topic | Quality-diversity, novelty, surrogate, and multifidelity search |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/03_search_qd_multifidelity/QD-015_Pierrot2022_multi-objective-quality-diversity-optimization.pdf) |
| Source SHA-256 | `fc1384bee75a740c2375abfed5b40eae001160cf8e66437d2c519525c6f46218` |
| Full-text coverage | 9/9 pages (100.00%); 7,387 extracted words |

## Research question

How does Multi-Objective Quality Diversity Optimization trade quality, diversity, evaluation cost, and fidelity error in an adaptive search?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, results, and frequent technical terms were pareto, optimization, solutions, space, front, mome, multi-objective, map-elites. The paper-specific method or result selected for transfer review is: **MOME keeps a Pareto front per cell**.

## Principal findings

- **Paper finding (conservative paraphrase):** MOME keeps a Pareto front per cell
- **Reviewer interpretation:** fits H2's race time/energy/mass/reliability trade-offs inside a diverse archive
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** fits H2's race time/energy/mass/reliability trade-offs inside a diverse archive This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

QD conclusions depend on descriptor geometry, archive resolution, evaluation budget, and proxy fidelity; archive score alone is not vehicle value. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **MOME keeps a Pareto front per cell** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **QD archive, descriptor schema, resource ledger, and multifidelity promotion policy**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | QD archive, descriptor schema, resource ledger, and multifidelity promotion policy |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'MOME keeps a Pareto front per cell' against the target below. |
| Experiment and control | Compare the paper-derived search rule with objective optimization, random search, and MAP-Elites under matched proposals, seeds, wall/CPU/GPU budgets, and stratified high-fidelity audits. |
| Acceptance and failure evidence | Require improved feasible coverage or held-out quality with confidence intervals and no unacceptable proxy false-negative rate; unknown high-fidelity outcomes remain `not_estimable`. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 45,553 characters, 7,387 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
