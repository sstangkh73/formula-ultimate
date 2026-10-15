# TH-001: A General Energy Balance for Battery Systems

Thai companion: `TH-001_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | D. Bernardi, E. Pawlikowski, J. Newman |
| Year | 1985 |
| Venue | Journal of The Electrochemical Society |
| DOI | 10.1149/1.2113792 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1149/1.2113792](https://doi.org/10.1149/1.2113792) |
| Library topic | Thermal systems and cooling |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/11_thermal_cooling/TH-001_Bernardi1985_a-general-energy-balance-for-battery-systems.pdf) |
| Source SHA-256 | `f9cff425e1a1c3a08674c296dcb83693d9fbb69f2f4e145ba8262f38a1f16acd` |
| Full-text coverage | 9/9 pages (100.00%); 8,149 extracted words |

## Research question

What terms are required for a thermodynamically complete battery energy balance when multiple reactions, mixing, and phase change occur?

## Method and evidence

The paper derives a general cell energy balance including electrochemical reactions, composition-dependent open-circuit potentials, mixing, phase change, and Joule heating, then applies it to two Li-Al/FeS reaction mechanisms (pp. 1-8).

## Principal findings

- **Paper finding (conservative paraphrase):** The two mechanisms can reach the same final adiabatic-reversible temperature yet follow different heat-generation histories and slope changes. The common single-reaction balance is justified only when phase-change, mixing, and simultaneous-reaction effects are negligible (results/conclusion, pp. 7-9).
- **Reviewer interpretation:** Equal terminal temperature does not imply equal internal thermal mechanism, so a final-temperature check can hide incorrect heat-source provenance.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** Equal terminal temperature does not imply equal internal thermal mechanism, so a final-temperature check can hide incorrect heat-source provenance. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The rigorous balance needs instantaneous composition profiles and reaction-current fractions, which are hard to obtain without a detailed electrochemical model (p. 2); the example chemistry is not a modern racing cell. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Equal terminal temperature does not imply equal internal thermal mechanism, so a final-temperature check can hide incorrect heat-source provenance.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Works 115/121 coupled thermal-solid/flow model and full-stint thermal finish gate**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Works 115/121 coupled thermal-solid/flow model and full-stint thermal finish gate |
| Proposed change | Extend Work 120/115 heat accounting with named irreversible, reversible, mixing, phase, and side-reaction terms; test when the lumped single-reaction model stays within a registered error envelope. |
| Experiment and control | Compare reduced and spatial models over repeated laps, hot ambient, flow blockage, and cooling-actuator failures while closing heat and auxiliary-power balances. |
| Acceptance and failure evidence | Require bounded temperature and heat-flow discrepancy, correct derating/failure timing, full-stint completion, and escalation outside the reduced-model envelope. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 48,316 characters, 8,149 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 2, 4, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
