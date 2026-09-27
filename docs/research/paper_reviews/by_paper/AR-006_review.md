# AR-006: Indy Autonomous Challenge - Autonomous Race Cars at the Handling Limits

Thai companion: `AR-006_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Alexander Wischnewski, Maximilian Geisslinger, Johannes Betz, Tobias Betz, F. Fent, Alexander Heilmeier, Leonhard Hermansdorfer, T. Herrmann, Sebastian Huch, Phillip Karle, Felix Nobis, Levent Ogretmen, Matthias Rowold, Florian Sauerbeck, Tim Stahl, Rainer Trauth, M. Lienkamp, B. Lohmann |
| Year | 2022 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2202.03807 |
| Canonical record | [https://arxiv.org/abs/2202.03807](https://arxiv.org/abs/2202.03807) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-006_Wischnewski2022_indy-autonomous-challenge-autonomous-race-cars-at.pdf) |
| Source SHA-256 | `4303396f6524bf83ec396ee057c8ca19190f3a029e2cac90769eee92e9fe119b` |
| Full-text coverage | 16/16 pages (100.00%); 6,696 extracted words |

## Research question

How does Indy Autonomous Challenge - Autonomous Race Cars at the Handling Limits combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were introduction, and frequent technical terms were autonomous, vehicle, control, racing, vehicles, software, ieee, scenarios. The paper-specific method or result selected for transfer review is: **Full-scale autonomous racing at the handling limit with real vehicle behaviour**.

## Principal findings

- **Paper finding (conservative paraphrase):** Full-scale autonomous racing at the handling limit with real vehicle behaviour
- **Reviewer interpretation:** a reference for model-reality gaps at speed
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a reference for model-reality gaps at speed This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Full-scale autonomous racing at the handling limit with real vehicle behaviour** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Register the dataset or benchmark behind 'Full-scale autonomous racing at the handling limit with real vehicle behaviour' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 43,239 characters, 6,696 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
