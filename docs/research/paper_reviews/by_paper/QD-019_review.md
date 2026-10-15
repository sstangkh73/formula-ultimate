# QD-019: Designing Air Flow with Surrogate-assisted Phenotypic Niching

Thai companion: `QD-019_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Alexander Hagg, Dominik Wilde, Alexander Asteroth, Thomas Bäck |
| Year | 2020 |
| Venue | Lecture Notes in Computer Science |
| DOI | 10.1007/978-3-030-58112-1_10 |
| arXiv | 2105.04256 |
| Canonical record | [https://doi.org/10.1007/978-3-030-58112-1_10](https://doi.org/10.1007/978-3-030-58112-1_10) |
| Library topic | Quality-diversity, novelty, surrogate, and multifidelity search |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/03_search_qd_multifidelity/QD-019_Hagg2020_designing-air-flow-with-surrogate-assisted-phenoty.pdf) |
| Source SHA-256 | `3e661fbc3ae594356ceb5d46575ffbc76bc6f6bbe4adb2441a0eb26b18d57b7d` |
| Full-text coverage | 14/14 pages (100.00%); 6,056 extracted words |

## Research question

How does Designing Air Flow with Surrogate-assisted Phenotypic Niching trade quality, diversity, evaluation cost, and fidelity error in an adaptive search?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, discussion, introduction, results, and frequent technical terms were performance, feature, sphen, sail, features, map-elites, models, shapes. The paper-specific method or result selected for transfer review is: **Surrogate-assisted QD for air-flow design with phenotypic niching**.

## Principal findings

- **Paper finding (conservative paraphrase):** Surrogate-assisted QD for air-flow design with phenotypic niching
- **Reviewer interpretation:** direct method for diverse aero/cooling geometry
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** direct method for diverse aero/cooling geometry This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

QD conclusions depend on descriptor geometry, archive resolution, evaluation budget, and proxy fidelity; archive score alone is not vehicle value. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Surrogate-assisted QD for air-flow design with phenotypic niching** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **QD archive, descriptor schema, resource ledger, and multifidelity promotion policy**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | QD archive, descriptor schema, resource ledger, and multifidelity promotion policy |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Surrogate-assisted QD for air-flow design with phenotypic niching' against the target below. |
| Experiment and control | Compare the paper-derived search rule with objective optimization, random search, and MAP-Elites under matched proposals, seeds, wall/CPU/GPU budgets, and stratified high-fidelity audits. |
| Acceptance and failure evidence | Require improved feasible coverage or held-out quality with confidence intervals and no unacceptable proxy false-negative rate; unknown high-fidelity outcomes remain `not_estimable`. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 36,034 characters, 6,056 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, discussion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
