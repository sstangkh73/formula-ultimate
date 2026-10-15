# OE-016: Scalable Co-Optimization of Morphology and Control in Embodied Machines

Thai companion: `OE-016_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Nick Cheney, J. Bongard, Vytas SunSpiral, Hod Lipson |
| Year | 2018 |
| Venue | Journal of the Royal Society Interface |
| DOI | Not recorded |
| arXiv | 1706.06133 |
| Canonical record | [https://arxiv.org/abs/1706.06133](https://arxiv.org/abs/1706.06133) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-016_Cheney2018_scalable-co-optimization-of-morphology-and-control.pdf) |
| Source SHA-256 | `ec75ed5670641b271a45297862b1ada057c6d96b983ca525809d86e1bee40f98` |
| Full-text coverage | 10/10 pages (100.00%); 8,135 extracted words |

## Research question

Can a co-design search preserve a new morphology long enough for its controller to adapt, instead of discarding it on immediate fitness?

## Method and evidence

The study evolves voxel-based virtual robots and adds morphology age as a second objective, comparing morphological-innovation protection with unprotected and alternative-protection treatments over 5,000 generations (pp. 4-6).

## Principal findings

- **Paper finding (conservative paraphrase):** With morphology protection, mean fitness rose from 18.715 at generation 0 to 22.916 at generation 5,000 (p < 0.001). An alternative protection treatment did not beat no protection (p = 0.240) and was significantly worse than morphology protection (p = 1.211e-4) (p. 4).
- **Reviewer interpretation:** The paper isolates controller-adaptation lag as a selection bias: a structurally promising child can look worse only because it inherits a controller specialized for its parent (p. 5).
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** The paper isolates controller-adaptation lag as a selection bias: a structurally promising child can look worse only because it inherits a controller specialized for its parent (p. 5). This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The evidence is from virtual voxel locomotion, and the authors state that the fitness gain does not conclusively prove their proposed causal explanation (p. 4). It does not establish the same effect in racing vehicles or under equal controller-training cost. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The paper isolates controller-adaptation lag as a selection bias: a structurally promising child can look worse only because it inherits a controller specialized for its parent (p. 5).** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Add morphology age and controller-training spend to each candidate ledger record; run protected versus unprotected co-design at matched total controller steps and require the held-out benefit to survive after every morphology receives equal adaptation opportunity. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 10 pages, 52,154 characters, 8,135 words.
- Pages with substantial extractable text: 10/10.
- High-information cue pages sampled from across the paper: 1, 2, 4, 5, 6, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
