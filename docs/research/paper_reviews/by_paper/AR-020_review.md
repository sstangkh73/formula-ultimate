# AR-020: Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies

Thai companion: `AR-020_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Joschua Wüthrich, Romir Damle, Giona Fieni, M. Zeilinger, C. Onder, Andrea Carron |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2604.00826 |
| Canonical record | [https://arxiv.org/abs/2604.00826](https://arxiv.org/abs/2604.00826) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-020_Wuthrich2026_bridging-rl-and-mpc-for-mixed-integer-optimal-cont.pdf) |
| Source SHA-256 | `ae93eb9f850808f67d51a5d1f9ead026ba77b11ccd1543a834d8d039aea53ee8` |
| Full-text coverage | 8/8 pages (100.00%); 7,312 extracted words |

## Research question

How does Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were hybrid, cost, control, discrete, time, continuous, race, action. The paper-specific method or result selected for transfer review is: **Combines RL and MPC for mixed-integer race strategy**.

## Principal findings

- **Paper finding (conservative paraphrase):** Combines RL and MPC for mixed-integer race strategy
- **Reviewer interpretation:** relevant to discrete strategy choices
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to discrete strategy choices This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Combines RL and MPC for mixed-integer race strategy** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Combines RL and MPC for mixed-integer race strategy' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 44,410 characters, 7,312 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 5, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
