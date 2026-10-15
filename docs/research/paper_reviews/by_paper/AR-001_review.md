# AR-001: Outracing champion Gran Turismo drivers with deep reinforcement learning

Thai companion: `AR-001_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Peter R. Wurman, Samuel Barrett, Kenta Kawamoto, James MacGlashan, Kaushik Subramanian, Thomas J. Walsh, Roberto Capobianco, Alisa Devlic, Franziska Eckert, Florian Fuchs, Leilani Gilpin, Piyush Khandelwal, Varun Kompella, HaoChih Lin, Patrick MacAlpine, Declan Oller, Takuma Seno, Craig Sherstan, Michael D. Thomure, Houmehr Aghabozorgi, Leon Barrett, Rory Douglas, Dion Whitehead, Peter Dürr, Peter Stone, Michael Spranger, Hiroaki Kitano |
| Year | 2022 |
| Venue | Nature |
| DOI | 10.1038/s41586-021-04357-7 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1038/s41586-021-04357-7](https://doi.org/10.1038/s41586-021-04357-7) |
| Library topic | Autonomous racing control, data, and strategy |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/14_autonomous_racing_strategy/AR-001_Wurman2022_outracing-champion-gran-turismo-drivers-with-deep.pdf) |
| Source SHA-256 | `057fb4d120cb041524655ebae79980c1f1997090ac09c122e7f5a493a42febfb` |
| Full-text coverage | 11/11 pages (100.00%); 6,960 extracted words |

## Research question

How does Outracing champion Gran Turismo drivers with deep reinforcement learning combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were task, tensor, policy, table, reward, return, p_obs, page. The paper-specific method or result selected for transfer review is: **Learned driver beating top humans in a high-fidelity game**.

## Principal findings

- **Paper finding (conservative paraphrase):** Learned driver beating top humans in a high-fidelity game
- **Reviewer interpretation:** a method for strong per-design drivers, not physical validation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a method for strong per-design drivers, not physical validation This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Learned driver beating top humans in a high-fidelity game** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol |
| Proposed change | Build a bounded diagnostic pilot from 'Learned driver beating top humans in a high-fidelity game' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints. |
| Acceptance and failure evidence | Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 11 pages, 23,134 characters, 6,960 words.
- Pages with substantial extractable text: 11/11.
- High-information cue pages sampled from across the paper: 4. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
