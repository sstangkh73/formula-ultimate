# AR-011: Super-Human Performance in Gran Turismo Sport Using Deep Reinforcement Learning

Thai companion: `AR-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Florian Fuchs, Yun-Long Song, Elia Kaufmann, Davide Scaramuzza, P. Dürr |
| Year | 2021 |
| Venue | IEEE Robotics and Automation Letters |
| DOI | Not recorded |
| arXiv | 2008.07971 |
| Canonical record | [https://arxiv.org/abs/2008.07971](https://arxiv.org/abs/2008.07971) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-011_Fuchs2021_super-human-performance-in-gran-turismo-sport-usin.pdf) |
| Source SHA-256 | `74f948d03d56d44e71925ff9f26005953268d455325bfc072f0822f459e035e2` |
| Full-text coverage | 12/12 pages (100.00%); 9,329 extracted words |

## Research question

How does Super-Human Performance in Gran Turismo Sport Using Deep Reinforcement Learning combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were human, approach, learning, setting, agent, time, track, control. The paper-specific method or result selected for transfer review is: **RL driver reaching super-human lap times in time trials**.

## Principal findings

- **Paper finding (conservative paraphrase):** RL driver reaching super-human lap times in time trials
- **Reviewer interpretation:** a learned-driver baseline method
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a learned-driver baseline method This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **RL driver reaching super-human lap times in time trials** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'RL driver reaching super-human lap times in time trials' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 12 pages, 55,637 characters, 9,329 words.
- Pages with substantial extractable text: 12/12.
- High-information cue pages sampled from across the paper: 1, 2, 6, 7, 10, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
