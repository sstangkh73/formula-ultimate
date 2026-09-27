# AR-022: Learning-Based On-Track System Identification for Scaled Autonomous Racing in Under a Minute

Thai companion: `AR-022_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Onur Dikici, Edoardo Ghignone, Cheng Hu, N. Baumann, Lei Xie, Andrea Carron, Michele Magno, M. Corno |
| Year | 2024 |
| Venue | IEEE Robotics and Automation Letters |
| DOI | Not recorded |
| arXiv | 2411.17508 |
| Canonical record | [https://arxiv.org/abs/2411.17508](https://arxiv.org/abs/2411.17508) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-022_Dikici2024_learning-based-on-track-system-identification-for.pdf) |
| Source SHA-256 | `30fd62a1a76b61b47498c183c2d83e38e6c7e93f041ba28e1d78125ea0c1e6f6` |
| Full-text coverage | 8/8 pages (100.00%); 6,653 extracted words |

## Research question

How does Learning-Based On-Track System Identification for Scaled Autonomous Racing in Under a Minute combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were model, vehicle, data, identification, tire, racing, method, system. The paper-specific method or result selected for transfer review is: **Identifies tyre/vehicle models from about 30 s of driving data**.

## Principal findings

- **Paper finding (conservative paraphrase):** Identifies tyre/vehicle models from about 30 s of driving data
- **Reviewer interpretation:** a fast calibration route for physical correlation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a fast calibration route for physical correlation This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Identifies tyre/vehicle models from about 30 s of driving data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Identifies tyre/vehicle models from about 30 s of driving data' against the target below. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 41,687 characters, 6,653 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
