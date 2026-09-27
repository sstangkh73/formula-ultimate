# AR-018: Game Theory in Formula 1: From Physical to Strategic Interactions

Thai companion: `AR-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Giona Fieni, Marc-Philippe Neumann, F. Furia, Alessandro Caucino, Alberto Cerofolini, V. Ravaglioli, C. Onder |
| Year | 2025 |
| Venue | European Journal of Control |
| DOI | Not recorded |
| arXiv | 2503.05421 |
| Canonical record | [https://arxiv.org/abs/2503.05421](https://arxiv.org/abs/2503.05421) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-018_Fieni2025_game-theory-in-formula-1-from-physical-to-strategi.pdf) |
| Source SHA-256 | `d4cdeca06d9f43729525c96f8ca6d871e446c7b8b6081125169f8391f04ff566` |
| Full-text coverage | 18/18 pages (100.00%); 12,826 extracted words |

## Research question

How does Game Theory in Formula 1: From Physical to Strategic Interactions combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, simulation/numerical evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were game, energy, drag, optimization, stackelberg, problem, nash, solution. The paper-specific method or result selected for transfer review is: **Game-theoretic view of F1 interactions**.

## Principal findings

- **Paper finding (conservative paraphrase):** Game-theoretic view of F1 interactions
- **Reviewer interpretation:** relevant only if multi-car races enter the environment
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant only if multi-car races enter the environment This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Game-theoretic view of F1 interactions** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Game-theoretic view of F1 interactions' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 76,615 characters, 12,826 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
