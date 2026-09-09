# Work 129: Independent higher-fidelity claim checks

Thai companion: `work129-independent_claim_validation.th.md`

Status: Planned

Original Work 106 package: 128

Dependencies: Work 125, Work 126, Work 127, Work 128

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Challenge the mechanisms and margins that determine the result using independently constructed stronger analyses.

Final geometry, source materials and boundary histories from Works 125–128; do not copy the original solver's conclusions as inputs.

## 2. Proposed files

- `src/formula_ultimate/experiments/independent_claim_validation.py`
- `config/development/independent_claim_validation_v1.json`
- `scripts/development/run_independent_claim_validation.py`
- `tests/test_independent_claim_validation.py`

## 3. Implementation sequence

1. Select critical claims by impact and uncertainty, including negative/near-limit cases.
2. Construct independent mesh/model/boundary interpretation and document shared assumptions explicitly.
3. Use stronger applicable physics and refinement; compare local fields and system-relevant responses.
4. Resolve discrepancies as numerical, modeling or data differences; update claim scope without rewriting original outcomes.

## 4. Experiment

- IV: Independent formulation/backend, fidelity and critical condition.
- DV: Field/response disagreement, ranking stability, margin changes and uncertainty.
- Controls: Same actual candidate and physically equivalent conditions, not necessarily identical mesh.

## 5. Tests and falsification

Shared-function wrappers must not qualify as independent; inject a known modeling omission and test whether the comparison exposes it.

## 6. Registration and acceptance

Freeze claim selection, independence declaration, stronger-model applicability and discrepancy decision criteria.

Selected claims either survive bounded independent checks or are downgraded with reasons. Unexplained ranking/margin discrepancies block promotion.

## 7. Deliverables and handoff

Independent model package, comparison fields, discrepancy register and revised evidence envelope.

Supplies candidate-specific evidence to manufacturing Work 130 and physical-test planning.

## 8. Risks and non-goals

Independent software can share wrong assumptions. Document common-mode uncertainty; this work still cannot replace physical measurements.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_independent_claim_validation tests.test_repository_contract -v
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_a
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_b --replay-reference artifacts/work129/run_a/result.json
```
