# AE-023: Multi-Granularity Conformal Prediction for Reliable Neural-Operator Automotive Aerodynamic Surrogates

Thai companion: `AE-023_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Chundong Jia, Chao Xia, A. Vdovin, Qing Jia, Simone Sebben, Zhi-Gang Yang |
| Year | 2026 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2607.17297 |
| Canonical record | [https://arxiv.org/abs/2607.17297](https://arxiv.org/abs/2607.17297) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-023_Jia2026_multi-granularity-conformal-prediction-for-reliabl.pdf) |
| Source SHA-256 | `d44406000d263b957c262a017b9bb1a14d376e0a63e885853a0c21734b047cd4` |
| Full-text coverage | 44/44 pages (100.00%); 12,061 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Multi-Granularity Conformal Prediction for Reliable Neural-Operator Automotive Aerodynamic Surrogates establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, methods, and frequent technical terms were prediction, calibration, normalized, conformal, coverage, interval, pressure, surface. The paper-specific method or result selected for transfer review is: **Conformal uncertainty bounds for aero surrogates**.

## Principal findings

- **Paper finding (conservative paraphrase):** Conformal uncertainty bounds for aero surrogates
- **Reviewer interpretation:** a way to attach calibrated error bars to surrogate-based promotion
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a way to attach calibrated error bars to surrogate-based promotion This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Conformal uncertainty bounds for aero surrogates** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Conformal uncertainty bounds for aero surrogates' against the target below. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 44 pages, 78,297 characters, 12,061 words.
- Pages with substantial extractable text: 44/44.
- High-information cue pages sampled from across the paper: 3, 4, 6, 7, 17, 20, 23, 25. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
