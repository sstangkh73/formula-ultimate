# Work 022 Result: Atomic Coupled-Step Transaction

Status: Completed

Thai companion: `2026-08-28_022_atomic-coupled-step-result.th.md`

## Outcome

Work 022 implemented the atomic adapter transaction between the Work 021
architecture and future domain physics. Adapters now execute in compiled order,
receive only copied declared inputs, write exactly their declared outputs, and
publish one complete state only after all eight modules and final-state checks
pass. Every failure rolls back to the exact immutable start state and publishes
zero candidate signals.

This is a generic transaction boundary. The validator executes zero domain
physics adapters and makes no whole-vehicle or physical-validation claim.

## Files changed

- `src/formula_ultimate/simulation/transaction.py`: runtime signal isolation,
  adapter protocol, traces/evidence, preflight, atomic execution, and rollback.
- `src/formula_ultimate/simulation/__init__.py`: public Work 022 exports.
- `tests/test_coupled_transaction.py`: 11 focused success/falsification tests.
- `scripts/validate_coupled_transaction.py`: deterministic reference and fault
  evidence.
- `docs/simulation/ATOMIC_COUPLED_STEP.md` and `.th.md`: model contract.
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` and `.th.md`: Work
  022 completion.
- this bilingual plan/result pair.
- `docs/problem_reports/2026-08-28_022_transaction-evidence-retention.md` and
  `.th.md`: resolved evidence-retention defect.

## Decisions

- Copy runtime payloads on ingress and every declared read.
- Preflight exact signal/adapter coverage and model-version pins before calling
  any adapter.
- Let compiled architecture order override registration order.
- Permit successful adapters to write exactly the complete declared set; permit
  invalid adapters to write nothing and provide a nonblank reason.
- Buffer signals privately through the entire step.
- Retain raw residuals/events separately from state publication, including
  evidence through the stopping module after rollback.
- Require globally unique evidence IDs and a typed, non-regressing `state.next`.

## Problem encountered and resolution

Initial implementation used residual/event evidence for control flow but did
not retain the raw records in the returned step. The separate problem report
records this auditability defect. `CoupledStepResult` now retains raw evidence
on both success and failure, rejects cross-module duplicate IDs, and still
publishes zero signals on invalidity. Regression evidence preserves the failed
`force-x = 2.0 N` entry with `0.1 N` tolerance.

## Validation

Commands ran from `C:\Formula Ultimate` on 2026-08-28 with fail-fast handling.

```powershell
python -m unittest tests.test_coupled_transaction -v
# exit 0; Ran 11 tests in 0.023s; OK

python -m unittest discover -s tests -v
# exit 0; Ran 177 tests in 0.528s; OK

python scripts/validate_coupled_transaction.py
# exit 0
# architecture fingerprint:
# 51ca53e9d4c6058f67f61dc57f3ece7e8c24176d915e74069f27d0aa6999f8a6
# reference status: committed; trace count: 8; published signals: 21
# state: 4.0 -> 4.01 s; 100.0 -> 100.3 m
# reversed registration replay: equal
# injected preflight/adapter/residual/time faults: rollback true, outputs 0
# retained failed residual: force-x = 2.0 N; tolerance = 0.1 N
# domain_physics_adapter_count: 0

python -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Final staged-scope and commit checks occur after staging this result record.

## Experiment review

- Supporting evidence: exact replay under reversed registration; eight traces
  in compiled order; exact 21-output publication only on success; preflight,
  undeclared-read, write-set, exception, invalid-output, residual, and final
  state faults all fail closed.
- Contradicting evidence: none within the generic atomicity hypothesis.
- Alternative explanation: the successful state advance is deliberately
  produced by placeholder adapters, not physical equations.
- Missing evidence: typed circuit/environment inputs and all cross-domain
  physical transfers.
- Confidence: high for the tested transaction contract; unchanged for physical
  vehicle accuracy.

## Limitations and follow-up

This work does not couple any domain solver. Work 023 is next and must provide
typed, deterministic circuit/environment/weather/traffic/strategy inputs for
all ten real-circuit profiles, with missing evidence remaining explicit.

No push or remote publication was performed.
