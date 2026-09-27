# QD-003: Data-Efficient Design Exploration through Surrogate-Assisted Illumination

Thai companion: `QD-003_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Adam Gaier, A. Asteroth, Jean-Baptiste Mouret |
| Year | 2018 |
| Venue | Evolutionary Computation |
| DOI | Not recorded |
| arXiv | 1806.05865 |
| Canonical record | [https://arxiv.org/abs/1806.05865](https://arxiv.org/abs/1806.05865) |
| Library topic | Quality-diversity, novelty, surrogate, and multifidelity search |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/03_search_qd_multifidelity/QD-003_Gaier2018_data-efficient-design-exploration-through-surrogat.pdf) |
| Source SHA-256 | `85ecbc13345539cd4b1ef7322499b70108b8f38b603a532509b08b37ea589d19` |
| Full-text coverage | 30/30 pages (100.00%); 14,513 extracted words |

## Research question

Can surrogate-assisted illumination map many high-performing design niches using far fewer expensive evaluations than MAP-Elites or single-optimum search?

## Method and evidence

SAIL combines a Gaussian-process surrogate, an upper-confidence-bound acquisition map, and MAP-Elites. It is tested first on 2-D airfoils and then on realistic 3-D aerodynamic design with expensive flow simulation (pp. 1-2, 8, 13).

## Principal findings

- **Paper finding (conservative paraphrase):** The paper reports hundreds of diverse high-performing designs with orders-of-magnitude fewer evaluations than MAP-Elites or CMA-ES in the 2-D task, and demonstrates high-performing illumination maps in the 3-D task (p. 1). UCB sampling improves accuracy around high-fitness regions relative to uniform or variance-only sampling (p. 13).
- **Reviewer interpretation:** Besides saving evaluations, SAIL exposes encoding bias: its maps show which regions an encoding can express and where the surrogate is easy or hard to learn (discussion, pp. 25-26).
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** Besides saving evaluations, SAIL exposes encoding bias: its maps show which regions an encoding can express and where the surrogate is easy or hard to learn (discussion, pp. 25-26). This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The gain depends on chosen behavioral features, Gaussian-process adequacy, acquisition policy, and expensive-truth sampling. The 3-D study was costly enough that detailed learning curves available for the airfoil case were not reproduced (p. 19). An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Besides saving evaluations, SAIL exposes encoding bias: its maps show which regions an encoding can express and where the surrogate is easy or hard to learn (discussion, pp. 25-26).** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **QD archive, descriptor schema, resource ledger, and multifidelity promotion policy**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | QD archive, descriptor schema, resource ledger, and multifidelity promotion policy |
| Proposed change | Add a SAIL arm to the search benchmark with the same high-fidelity call budget as MAP-Elites; audit surrogate error by archive cell and require gains in held-out feasible coverage, not predicted QD score alone. |
| Experiment and control | Compare the paper-derived search rule with objective optimization, random search, and MAP-Elites under matched proposals, seeds, wall/CPU/GPU budgets, and stratified high-fidelity audits. |
| Acceptance and failure evidence | Require improved feasible coverage or held-out quality with confidence intervals and no unacceptable proxy false-negative rate; unknown high-fidelity outcomes remain `not_estimable`. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 30 pages, 91,245 characters, 14,513 words.
- Pages with substantial extractable text: 30/30.
- High-information cue pages sampled from across the paper: 1, 2, 6, 8, 13, 19, 21, 24. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, discussion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
