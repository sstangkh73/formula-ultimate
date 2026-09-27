# AR-017: Towards Learning-Based Formula 1 Race Strategies

Thai companion: `AR-017_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Giona Fieni, Joschua Wüthrich, Marc-Philippe Neumann, Mohammad M. Moradi, C. Onder |
| Year | 2025 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2512.21570 |
| Canonical record | [https://arxiv.org/abs/2512.21570](https://arxiv.org/abs/2512.21570) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-017_Fieni2025_towards-learning-based-formula-1-race-strategies.pdf) |
| Source SHA-256 | `fc609aa9dcff9179d5e6cba8ce96eb7785f8db45daeef2fc6c4aad32ad133270` |
| Full-text coverage | 13/13 pages (100.00%); 9,889 extracted words |

## Research question

How does Towards Learning-Based Formula 1 Race Strategies combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were race, tire, time, energy, wear, agent, battery, strategy. The paper-specific method or result selected for transfer review is: **Learning-based F1 strategy**.

## Principal findings

- **Paper finding (conservative paraphrase):** Learning-based F1 strategy
- **Reviewer interpretation:** recent context for race-level decision making
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** recent context for race-level decision making This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Learning-based F1 strategy** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Learning-based F1 strategy' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 13 pages, 56,349 characters, 9,889 words.
- Pages with substantial extractable text: 13/13.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 6, 10, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
