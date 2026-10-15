# AG-020: CAD-Recode: Reverse Engineering CAD Code from Point Clouds

Thai companion: `AG-020_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | D. Rukhovich, Elona Dupont, Dimitrios Mallis, K. Cherenkova, Anis Kacem, Djamila Aouada |
| Year | 2024 |
| Venue | IEEE International Conference on Computer Vision |
| DOI | Not recorded |
| arXiv | 2412.14042 |
| Canonical record | [https://arxiv.org/abs/2412.14042](https://arxiv.org/abs/2412.14042) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-020_Rukhovich2024_cad-recode-reverse-engineering-cad-code-from-point.pdf) |
| Source SHA-256 | `979e38357c87401dcd71a3b4bca5e57d0ae14eeb9404a93234527d09bcfc0727` |
| Full-text coverage | 22/22 pages (100.00%); 14,547 extracted words |

## Research question

Can the agent or generative method in CAD-Recode: Reverse Engineering CAD Code from Point Clouds produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were segment, code, point, model, cad-recode, dataset, cloud, cadquery. The paper-specific method or result selected for transfer review is: **Recovers CadQuery programs from point clouds with a large synthetic CadQuery corpus**.

## Principal findings

- **Paper finding (conservative paraphrase):** Recovers CadQuery programs from point clouds with a large synthetic CadQuery corpus
- **Reviewer interpretation:** useful data and a geometry-to-code check
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** useful data and a geometry-to-code check This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Recovers CadQuery programs from point clouds with a large synthetic CadQuery corpus** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Recovers CadQuery programs from point clouds with a large synthetic CadQuery corpus' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 22 pages, 89,150 characters, 14,547 words.
- Pages with substantial extractable text: 22/22.
- High-information cue pages sampled from across the paper: 2, 3, 4, 6, 7, 10, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
