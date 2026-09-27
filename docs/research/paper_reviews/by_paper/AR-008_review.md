# AR-008: RACECAR -- The Dataset for High-Speed Autonomous Racing

Thai companion: `AR-008_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | A. Kulkarni, John Chrosniak, Emory Ducote, Florian Sauerbeck, Andrew Saba, Utkarsh Chirimar, J. Link, Madhur Behl, Marcello Cellina |
| Year | 2023 |
| Venue | IEEE/RJS International Conference on Intelligent RObots and Systems |
| DOI | Not recorded |
| arXiv | 2306.03252 |
| Canonical record | [https://arxiv.org/abs/2306.03252](https://arxiv.org/abs/2306.03252) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-008_Kulkarni2023_racecar-the-dataset-for-high-speed-autonomous-raci.pdf) |
| Source SHA-256 | `e9e349f8ddcde9d37ff5c0fdf57c20ac233b111dc0b7078f58b35dde058efc64` |
| Full-text coverage | 9/9 pages (100.00%); 6,389 extracted words |

## Research question

How does RACECAR -- The Dataset for High-Speed Autonomous Racing combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were data, autonomous, racing, vehicle, racecar, detection, dataset, lidar. The paper-specific method or result selected for transfer review is: **Open multi-sensor data from full-scale autonomous Indy cars up to 273 km/h including banked tracks**.

## Principal findings

- **Paper finding (conservative paraphrase):** Open multi-sensor data from full-scale autonomous Indy cars up to 273 km/h including banked tracks
- **Reviewer interpretation:** real data for vehicle-model validation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** real data for vehicle-model validation This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Open multi-sensor data from full-scale autonomous Indy cars up to 273 km/h including banked tracks** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Register the dataset or benchmark behind 'Open multi-sensor data from full-scale autonomous Indy cars up to 273 km/h including banked tracks' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 38,252 characters, 6,389 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
