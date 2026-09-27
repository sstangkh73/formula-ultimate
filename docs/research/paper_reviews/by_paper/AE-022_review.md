# AE-022: Faster by Design: Interactive Aerodynamics via Neural Surrogates Trained on Expert-Validated CFD

Thai companion: `AE-022_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Nicholas Thumiger, Andrea Bartezzaghi, Mattia Rigotti, Cezary Skura, Thomas Frick, Elisa Serioli, Fabrizio Arbucci, A. Malossi |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2604.18491 |
| Canonical record | [https://arxiv.org/abs/2604.18491](https://arxiv.org/abs/2604.18491) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-022_Thumiger2026_faster-by-design-interactive-aerodynamics-via-neur.pdf) |
| Source SHA-256 | `7011edf84b011f6ec7166295a59dc7371dab5e0cd10da00cd502b30e68db4ec8` |
| Full-text coverage | 7/7 pages (100.00%); 4,781 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Faster by Design: Interactive Aerodynamics via Neural Surrogates Trained on Expert-Validated CFD establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, methods, results, and frequent technical terms were gist, aerodynamic, mesh, model, dataset, neural, design, surface. The paper-specific method or result selected for transfer review is: **Neural surrogates trained on expert-validated race-car CFD (including an LMP2 car)**.

## Principal findings

- **Paper finding (conservative paraphrase):** Neural surrogates trained on expert-validated race-car CFD (including an LMP2 car)
- **Reviewer interpretation:** the closest race-car surrogate study
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the closest race-car surrogate study This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Neural surrogates trained on expert-validated race-car CFD (including an LMP2 car)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Neural surrogates trained on expert-validated race-car CFD (including an LMP2 car)' against the target below. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 7 pages, 31,622 characters, 4,781 words.
- Pages with substantial extractable text: 7/7.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
