# AE-011: Ground Effect Aerodynamics of Race Cars

Thai companion: `AE-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Xin Zhang, Willem Toet, Jonathan Zerihan |
| Year | 2006 |
| Venue | Applied Mechanics Reviews |
| DOI | 10.1115/1.2110263 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1115/1.2110263](https://doi.org/10.1115/1.2110263) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-011_Zhang2006_ground-effect-aerodynamics-of-race-cars.pdf) |
| Source SHA-256 | `8e255e21118832919cf59c0f9611e7ef4d5170cec3a50058bd418f3c38a54ae2` |
| Full-text coverage | 17/17 pages (100.00%); 17,466 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Ground Effect Aerodynamics of Race Cars establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were introduction, and frequent technical terms were ground, effect, downforce, h20852, wing, wheel, aerodynamics, force. The paper-specific method or result selected for transfer review is: **Review of wings, diffusers and wheels in ground effect with experimental data**.

## Principal findings

- **Paper finding (conservative paraphrase):** Review of wings, diffusers and wheels in ground effect with experimental data
- **Reviewer interpretation:** the physics of ride-height-dependent downforce
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the physics of ride-height-dependent downforce This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Review of wings, diffusers and wheels in ground effect with experimental data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Review of wings, diffusers and wheels in ground effect with experimental data' against the target below. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 17 pages, 107,446 characters, 17,466 words.
- Pages with substantial extractable text: 17/17.
- High-information cue pages sampled from across the paper: 2, 4, 5, 6, 7, 8, 9, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
