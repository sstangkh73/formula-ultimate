# AG-026: CADEngBench: It Looks Like CAD, but Does It Work? Evaluating Parametric Design, Assembly Reasoning, and Physics Simulation

Thai companion: `AG-026_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Harmanjot Singh, Abhra Dubey, Jorge Alejandro Amador Herrera |
| Year | 2026 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2608.09296 |
| Canonical record | [https://arxiv.org/abs/2608.09296](https://arxiv.org/abs/2608.09296) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-026_Singh2026_cadengbench-it-looks-like-cad-but-does-it-work-eva.pdf) |
| Source SHA-256 | `8856c68ecf3f1cbc1aae0ac4e7b3ba9fc453925e959e009a89a65128ddcff30f` |
| Full-text coverage | 27/27 pages (100.00%); 13,971 extracted words |

## Research question

Do text/code-capable models produce CAD that remains valid under parameter edits, engineering checks, matched FEA, and assembly-joint execution?

## Method and evidence

CADEngBench-P uses 300 parametric parts for 600 zero-to-CAD and functional-edit tasks, while CADEngBench-A uses 150 body pairs for joint retrieval, exact entity grounding, frame prediction, and kinematic verification; eight multimodal code-capable models are compared (p. 1).

## Principal findings

- **Paper finding (conservative paraphrase):** Editing supplied CAD is substantially easier than generating it; complex edits and matched linear-static FEA remain difficult. Assembly models often find the right region but not the recorded joint or mating entities, and no model leads every evaluation stage (pp. 1, 5, 22-23).
- **Reviewer interpretation:** A generated program can execute and match one nominal shape while encoding the wrong parameter dependency, causing its structural-response family to diverge (p. 5).
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** A generated program can execute and match one nominal shape while encoding the wrong parameter dependency, causing its structural-response family to diverge (p. 5). This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The benchmark uses declared DFM rules, CalculiX linear-static FEA, and recorded assembly relations; it does not cover nonlinear material/contact, fatigue, tolerance stacks, or complete vehicle function. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **A generated program can execute and match one nominal shape while encoding the wrong parameter dependency, causing its structural-response family to diverge (p. 5).** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Adopt hidden parametric-family, matched-FEA, exact-mate, and motion-probe tests in the agent verifier; score end-to-end failure when any earlier geometry or joint-grounding stage fails. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 27 pages, 97,218 characters, 13,971 words.
- Pages with substantial extractable text: 27/27.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 7, 12, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
