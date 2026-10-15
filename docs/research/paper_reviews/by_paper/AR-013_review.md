# AR-013: Champion-level drone racing using deep reinforcement learning

Thai companion: `AR-013_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Elia Kaufmann, Leonard Bauersfeld, Antonio Loquercio, Matthias Müller, Vladlen Koltun, Davide Scaramuzza |
| Year | 2023 |
| Venue | Nature |
| DOI | 10.1038/s41586-023-06419-4 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1038/s41586-023-06419-4](https://doi.org/10.1038/s41586-023-06419-4) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-013_Kaufmann2023_champion-level-drone-racing-using-deep-reinforceme.pdf) |
| Source SHA-256 | `c9bcbd98ddbf2b0a18b4cbdbc4e62e429c6a659e1b1054b5d1c2e0219b8da40f` |
| Full-text coverage | 14/14 pages (100.00%); 10,298 extracted words |

## Research question

How does Champion-level drone racing using deep reinforcement learning combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, physical-test evidence, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were discussion, methods, results, and frequent technical terms were swift, human, gate, data, drone, racing, policy, track. The paper-specific method or result selected for transfer review is: **Learned policy beating human champions in the real world with residual models from real data**.

## Principal findings

- **Paper finding (conservative paraphrase):** Learned policy beating human champions in the real world with residual models from real data
- **Reviewer interpretation:** an example of closing the sim-to-real gap
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an example of closing the sim-to-real gap This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Learned policy beating human champions in the real world with residual models from real data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Learned policy beating human champions in the real world with residual models from real data' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 63,175 characters, 10,298 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 5, 7, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: discussion, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
