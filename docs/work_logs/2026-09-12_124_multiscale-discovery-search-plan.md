# Work 124 Plan: Multiscale Discovery and Fair Accounting

Thai companion: `2026-09-12_124_multiscale-discovery-search-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a deterministic multiscale search/accounting reference pinned to Work 109 freeform representation, Work 117 task feedback and Work 123 exploratory vehicle harness. Maintain scoped feasible, near-feasible and unresolved archives without treating diversity as novelty or promoting incomplete vehicle evidence.

Reserve partitioned CAD/mesh/solver/tuning/audit resources before execution; charge failures, retries and audits; expose not-evaluated proposals after exhaustion. Verify full ancestry/admission hashes, invalidate stale cache, and separate exact decision replay from upstream numerical replay.

## Variables, controls and files

- IV: search/representation policy, fidelity allocation, archive rule, coupling mode, topology/continuous shape and seed.
- DV: scoped utility/diversity, signed effects, uncertainty, archive membership, time-to-evidence, unknown/not-evaluated counters and resource usage.
- Controls: matched task/library/seeds/hardware/budget; pre-execution exhaustion, charged failure, stale cache, tampered summary, inactive appendage and useful same-topology shape.
- Success: provenance/accounting/replay pass; unknown counters remain nonzero; representation audits are score-independent; continuous beneficial shape remains eligible.

Planned files: `src/formula_ultimate/search/multiscale_discovery_search.py`, `config/development/multiscale_discovery_search_v1.json`, `scripts/development/run_multiscale_discovery_search.py`, `tests/test_multiscale_discovery_search.py`, bilingual `docs/contracts/MULTISCALE_DISCOVERY_SEARCH_V1*`, this bilingual plan/result and ignored `artifacts/work124/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_multiscale_discovery_search tests.test_repository_contract -v
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_a
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_b --replay-reference artifacts/work124/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 109/117/123 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

This is a bounded accounting/search reference, not a mandated optimizer or proof of discovery. Non-goals: novelty from diversity alone, evaluating every proposal, vehicle promotion, validated performance, physical validation, push or history rewrite.
