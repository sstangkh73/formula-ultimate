# AG-009: Physics-in-the-Loop: A Hybrid Agentic Architecture for Validated CAD Engineering Design

Thai companion: `AG-009_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Elias Berger, Muhammad Usama, J. Mehlstäubl, Bernhard Saske, Kristin Paetzold-Byhain |
| Year | 2026 |
| Venue | Proceedings of the Thirty-Fifth International Joint Conference on Artificial Intelligence |
| DOI | Not recorded |
| arXiv | 2605.19717 |
| Canonical record | [https://arxiv.org/abs/2605.19717](https://arxiv.org/abs/2605.19717) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-009_Berger2026_physics-in-the-loop-a-hybrid-agentic-architecture.pdf) |
| Source SHA-256 | `f3193bb4315aeca93ddfa7fe5c45dd5a6b1f235177a9ba0afcfc204c97ac074b` |
| Full-text coverage | 9/9 pages (100.00%); 5,931 extracted words |

## Research question

Can the agent or generative method in Physics-in-the-Loop: A Hybrid Agentic Architecture for Validated CAD Engineering Design produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, physical-test evidence, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, discussion, introduction, results, and frequent technical terms were design, engineering, load, models, feedback, claude, gemini, arxiv. The paper-specific method or result selected for transfer review is: **Generate-simulate-refine CAD agent with a validated physics tool in the loop rather than visual feedback**.

## Principal findings

- **Paper finding (conservative paraphrase):** Generate-simulate-refine CAD agent with a validated physics tool in the loop rather than visual feedback
- **Reviewer interpretation:** the same pattern as our CadQuery-to-evaluator loop
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the same pattern as our CadQuery-to-evaluator loop This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Generate-simulate-refine CAD agent with a validated physics tool in the loop rather than visual feedback** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Generate-simulate-refine CAD agent with a validated physics tool in the loop rather than visual feedback' against the target below. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 9 pages, 38,496 characters, 5,931 words.
- Pages with substantial extractable text: 9/9.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, discussion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
