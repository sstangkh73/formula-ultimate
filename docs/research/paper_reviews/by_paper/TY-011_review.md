# TY-011: Bayesian Optimization-based Tire Parameter and Uncertainty Estimation for Real-World Data

Thai companion: `TY-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Sven Goblirsch, Benedikt Ruhland, Johannes Betz, Markus Lienkamp |
| Year | 2025 |
| Venue | 2025 IEEE Intelligent Vehicles Symposium (IV) |
| DOI | Not recorded |
| arXiv | 2504.20863 |
| Canonical record | [https://arxiv.org/abs/2504.20863](https://arxiv.org/abs/2504.20863) |
| Library topic | Tyres, friction, and road contact |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/09_tyres_friction/TY-011_Goblirsch2025_bayesian-optimization-based-tire-parameter-and-unc.pdf) |
| Source SHA-256 | `3fb9b0adadf1d34a0c9ec92e3923ef10cddfeb9d94d4519fd4f4d13e86345d8a` |
| Full-text coverage | 8/8 pages (100.00%); 5,640 extracted words |

## Research question

Can tyre parameters and their uncertainty be identified from real driving data, and how does manoeuvre excitation affect identifiability?

## Method and evidence

The study uses stochastic variational inference within a Bayesian-optimization workflow, evaluates excitation effects, and compares with a Nelder-Mead baseline on theoretical and real-world identification cases (pp. 2-3).

## Principal findings

- **Paper finding (conservative paraphrase):** The method estimates parameter distributions rather than one best fit and shows that excitation affects parameter accuracy. The paper also reports that tire-only parameter identification can perform worse than identifying the fuller model, warning against treating other vehicle parameters as known (pp. 2-3).
- **Reviewer interpretation:** The experiment links manoeuvre design to uncertainty: ordinary accessible driving may not excite the parameters that a racing controller needs.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** The experiment links manoeuvre design to uncertainty: ordinary accessible driving may not excite the parameters that a racing controller needs. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The result depends on the tyre/vehicle model, excitation range, sensors, and real-data quality; posterior uncertainty does not correct model-form error or extrapolation outside measured conditions. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The experiment links manoeuvre design to uncertainty: ordinary accessible driving may not excite the parameters that a racing controller needs.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation |
| Proposed change | Design a D-optimal-style tyre identification manoeuvre set, fit joint tyre/vehicle uncertainty, and propagate posterior samples through held-out lap replay before tightening the ground-contact envelope. |
| Experiment and control | Fit and validate against separate manoeuvres across combined slip, load, camber, pressure, temperature, wear, speed, and road state; compare with the present low-fidelity model. |
| Acceptance and failure evidence | Require bounded force/moment and temperature/wear errors on held-out manoeuvres and improved lap replay without hiding extrapolation outside the tyre envelope. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 34,495 characters, 5,640 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 2, 3, 4. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
