# AE-024: Adapting Automotive Aerodynamics Surrogates to New Vehicle Families via Transfer Learning

Thai companion: `AE-024_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | SeungHwan Keum, A. Warey |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2605.27968 |
| Canonical record | [https://arxiv.org/abs/2605.27968](https://arxiv.org/abs/2605.27968) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-024_Keum2026_adapting-automotive-aerodynamics-surrogates-to-new.pdf) |
| Source SHA-256 | `22ac267982a1bc22f654a5408cb83c9074da36ea2b7fe4f260e55df5d1de3f8e` |
| Full-text coverage | 23/23 pages (100.00%); 13,518 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does Adapting Automotive Aerodynamics Surrogates to New Vehicle Families via Transfer Learning establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, discussion, introduction, methods, results, and frequent technical terms were learning, geometry, transfer, lora, model, surface, vehicle, fine-tuning. The paper-specific method or result selected for transfer review is: **Measures surrogate failure and adaptation on new vehicle families**.

## Principal findings

- **Paper finding (conservative paraphrase):** Measures surrogate failure and adaptation on new vehicle families
- **Reviewer interpretation:** directly relevant because novel architectures are out of distribution
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** directly relevant because novel architectures are out of distribution This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Measures surrogate failure and adaptation on new vehicle families** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Measures surrogate failure and adaptation on new vehicle families' against the target below. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 23 pages, 88,096 characters, 13,518 words.
- Pages with substantial extractable text: 23/23.
- High-information cue pages sampled from across the paper: 2, 3, 4, 5, 6, 8, 9, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, discussion, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
