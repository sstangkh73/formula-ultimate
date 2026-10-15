# AE-007: CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics

Thai companion: `AE-007_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | M. Elrefaie, Du-Le Shu, Matt Klenk, Faez Ahmed |
| Year | 2025 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2512.07847 |
| Canonical record | [https://arxiv.org/abs/2512.07847](https://arxiv.org/abs/2512.07847) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-007_Elrefaie2025_carbench-a-comprehensive-benchmark-for-neural-surr.pdf) |
| Source SHA-256 | `653bf51e34585036ffee19733c52ec4b5f5e356af5f0698ed1fef2fb46b1cad5` |
| Full-text coverage | 39/39 pages (100.00%); 24,347 extracted words |

## Research question

What aerodynamic mechanism, dataset, solver, or surrogate does CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics establish, and over what geometry and flow domain?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, discussion, introduction, methods, results, and frequent technical terms were models, training, model, error, pressure, surface, learning, test. The paper-specific method or result selected for transfer review is: **Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories**.

## Principal findings

- **Paper finding (conservative paraphrase):** Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories
- **Reviewer interpretation:** the evaluation protocol for any aero surrogate we use
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the evaluation protocol for any aero surrogate we use This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories' against the target below. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 39 pages, 160,322 characters, 24,347 words.
- Pages with substantial extractable text: 39/39.
- High-information cue pages sampled from across the paper: 2, 3, 4, 9, 10, 12, 13, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, discussion, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
