# Work 124: Multiscale discovery and fair accounting

Thai companion: `work124-multiscale_discovery_search.th.md`

Status: Planned

Original Work 106 package: 123

Dependencies: Work 109, Work 117, Work 123

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Search geometry, topology, materials, interfaces and controller together with traceable decisions and matched compute opportunity.

Work 109 generator and Work 117 feedback; local mode can start before Work 123 vehicle mode. Audit old intake/accounting assumptions before admission.

## 2. Proposed files

- `src/formula_ultimate/search/multiscale_discovery_search.py`
- `config/development/multiscale_discovery_search_v1.json`
- `scripts/development/run_multiscale_discovery_search.py`
- `tests/test_multiscale_discovery_search.py`

## 3. Implementation sequence

1. Define scoped feasible/near-feasible/unresolved archives and causal shape/function descriptors.
2. Reserve resources before every CAD/mesh/solver/tuning call; charge failures, retries and audits.
3. Verify full source/admission provenance and separate exact decisions from numerical replay.
4. Allocate score-independent representation audits and compute-budgeted refinement/promotion.

## 4. Experiment

- IV: Search/representation policy, fidelity allocation, archive strategy and coupling mode.
- DV: Verified utility/diversity, time-to-evidence, false-negative audits and total resource usage.
- Controls: Matched external task, library opportunity, seed pairing, hardware and complete budget.

## 5. Tests and falsification

Budget exhaustion before execution, failed attempts, cache invalidation, tampered admission summary, inactive appendage and same-topology useful shape.

## 6. Registration and acceptance

Freeze all budget partitions, accounting units, escalation rules, meaningful signed effect and uncertainty comparison method.

Accounting/provenance/replay gates pass; unknown counters are not zero. Beneficial continuous shape changes remain eligible without graph novelty.

## 7. Deliverables and handoff

Search ancestry, registered budget ledger, archives, audit samples and signed benefit/uncertainty reports.

Supplies the admitted experiment engine to Works 125 and 127.

## 8. Risks and non-goals

Do not make one optimizer or representation mandatory. Bound expensive identity/solver calls and report not-evaluated proposals; no novelty claim from diversity alone.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_multiscale_discovery_search tests.test_repository_contract -v
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_a
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_b --replay-reference artifacts/work124/run_a/result.json
```
