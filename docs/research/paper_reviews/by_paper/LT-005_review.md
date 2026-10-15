# LT-005: Optimizing the aero-suspension interactions in a Formula One car

Thai companion: `LT-005_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Mehdi Imani Masouleh, David J. N. Limebeer |
| Year | 2016 |
| Venue | IEEE Transactions on Control Systems Technology |
| DOI | 10.1109/tcst.2015.2475396 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1109/tcst.2015.2475396](https://doi.org/10.1109/tcst.2015.2475396) |
| Library topic | Minimum-lap-time and vehicle design/control co-optimization |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/07_lap_time_vehicle_dynamics/LT-005_Masouleh2016_optimizing-the-aero-suspension-interactions-in-a-f.pdf) |
| Source SHA-256 | `82b38b530044791aabfb77e4b6c9e7767a37b7843a4fcf3e6c295d4b95bacca7` |
| Full-text coverage | 16/16 pages (100.00%); 13,250 extracted words |

## Research question

How much do suspension kinematics and attitude-sensitive aerodynamics change the optimal lap when modeled together?

## Method and evidence

The paper embeds polynomial surrogates of a physical suspension-kinematics model and attitude-dependent aero into a Formula One optimal-control lap calculation, retaining high kinematic accuracy while reducing solve cost (pp. 4, 6, 11).

## Principal findings

- **Paper finding (conservative paraphrase):** Reported surrogate errors are at most 0.147 mm in front ride height and 0.038 degrees in roll over the tested mesh. Including steer and sideslip aero sensitivities raises the reported lap time to 83.45 s, and lower high-speed ride height gains downforce while roll degrades it (pp. 6, 11).
- **Reviewer interpretation:** Aero and suspension cannot be optimized as independent peak metrics: the controller changes ride and roll along the lap, moving the aero operating point.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** Aero and suspension cannot be optimized as independent peak metrics: the controller changes ride and roll along the lap, moving the aero operating point. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The result is tied to the chosen F1 model, surrogate mesh, aero maps, track, and optimal-control transcription; polynomial fit accuracy does not validate the underlying aero or suspension data. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Aero and suspension cannot be optimized as independent peak metrics: the controller changes ride and roll along the lap, moving the aero operating point.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **integrated transient lap evaluator, optimal-control transcription, and independent forward replay**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | integrated transient lap evaluator, optimal-control transcription, and independent forward replay |
| Proposed change | Add ride height, pitch, roll, steer, and sideslip as shared states between Work 121 aero and Work 123 vehicle dynamics; require independent forward replay and aero-map envelope checks. |
| Experiment and control | Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines. |
| Acceptance and failure evidence | Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 74,154 characters, 13,250 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 4, 6, 10, 11, 12, 13, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
