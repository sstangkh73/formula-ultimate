# Work 125 Plan: Registered Detailed-Part Discovery Comparison

Thai companion: `2026-09-12_125_detailed-part-comparison-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Run a bounded preregistered paired comparison of optimized fixed-family, existing-grammar, open-material and random-control detailed-part arms. Pin Work 113–116 connection/motion/thermal/material evidence and Work 124 accounting; keep pilot/training conditions disjoint from untouched holdout conditions.

Charge equal optimization and holdout budgets, evaluate signed utility differences and uncertainty at stronger fidelity, audit rejected/unresolved geometry independent of proxy score, and ablate claimed active geometry. Completion may yield a negative result; a discovery-benefit claim additionally requires constraints, meaningful signed effect and uncertainty gates.

## Variables, controls and files

- IV: representation arm, tuned parameter, active/ablated coupling, coarse/fine fidelity and held-out condition.
- DV: verified utility, paired effect/interval, mass/energy burden, constraint state, ranking reversal and total charged cost.
- Controls: identical task, material/process boundary, paired seeds and budget; optimized arms, inactive appendage, same-topology response, omitted hardware, fine-fidelity reversal and holdout leak.
- Success: fair accounting/provenance, disjoint holdout, causal ablation, fidelity evidence and exact replay. Positive discovery is not required.

Planned files: `src/formula_ultimate/experiments/detailed_part_comparison.py`, `config/development/detailed_part_comparison_v1.json`, `scripts/development/run_detailed_part_comparison.py`, `tests/test_detailed_part_comparison.py`, bilingual `docs/contracts/DETAILED_PART_COMPARISON_V1*`, this bilingual plan/result and ignored `artifacts/work125/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_detailed_part_comparison tests.test_repository_contract -v
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_a
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_b --replay-reference artifacts/work125/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 113–116/124 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

The registered response fixtures are synthetic and cannot establish external novelty or whole-vehicle benefit. Non-goals: threshold tuning after results, visible-strangeness requirements, physical validation, push or history rewrite.
