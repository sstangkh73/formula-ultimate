# Work 022 Plan: Atomic Coupled-Step Transaction

Status: Completed

Thai companion: `2026-08-28_022_atomic-coupled-step-plan.th.md`

## Objective

Implement the adapter execution and transaction boundary required to run one
compiled coupling architecture atomically. Every adapter must receive only its
declared immutable inputs, return exactly its declared outputs, and either
produce one complete committed `state.next` or leave the start state unchanged
with explicit invalidity evidence.

## Scope

- Define immutable runtime signal values and a read view restricted to each
  module's declared `consumes` set.
- Define adapter output, trace, failure, and step-result records.
- Validate exact initial-signal and adapter coverage before execution.
- Execute adapters only in compiled architecture order.
- Reject missing, extra, duplicate, or malformed writes; mismatched adapter
  identity; adapter exceptions; invalid adapter status; and invalid final state.
- Buffer all candidate outputs privately and expose them only after a complete
  successful step.
- Require `state.next` to be a `SharedVehicleState`, with non-regressing time and
  race distance.
- Add focused falsification tests, a deterministic validator, bilingual model
  and result documentation, queue status updates, and one verified commit.

## Planned files

- `src/formula_ultimate/simulation/transaction.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_coupled_transaction.py`
- `scripts/validate_coupled_transaction.py`
- `docs/simulation/ATOMIC_COUPLED_STEP.md` and `.th.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` and `.th.md`
- this bilingual plan/result pair
- separate bilingual problem reports if a material issue is encountered

## Experiment definition

- Preferred hypothesis: an ordered transaction can make every partial or
  undeclared adapter update observable while committing exactly one complete
  next state only after all modules pass.
- Independent variables: adapter ordering, identity, read/write declaration,
  returned outputs/status, exceptions, initial signal coverage, and final state.
- Dependent variables: transaction status, committed state, failure module and
  reason, trace length/order, and published output set.
- Controls: Work 021 compiled architecture, immutable start state, private
  candidate signal buffer, exact declared output equality, and deterministic
  module order.
- Success criteria: a deterministic eight-adapter reference transaction commits
  once; adapters observe only declared inputs; all injected faults roll back
  with the original state and no published candidate outputs.
- Failure criteria: partial output becomes visible, start state mutates, an
  undeclared/missing write passes, execution continues after failure, adapter
  order changes, or an invalid/non-monotonic next state commits.
- Falsification: permute adapter registration, omit/add adapters or initial
  signals, return missing/extra/duplicate outputs, throw an exception, report
  invalidity mid-pipeline, and return a wrong or regressing `state.next`.

## Risks

- Python immutability is a contract boundary, not a hostile-code sandbox;
  adapters remain trusted repository code.
- Generic payloads establish atomicity and provenance but do not yet establish
  physical units or semantics; Work 023–027 own typed domain adapters.
- A successful no-op reference pipeline proves transaction behavior only, not
  vehicle physics.

## Explicit non-goals

- No circuit, aero, contact, motion, energy, thermal, health, or race physics
  coupling; no whole-race loop; no optimizer/CAD/CFD/FEA; no physical-validation
  claim; no README change; and no remote push.

## Validation

```powershell
python -m unittest tests.test_coupled_transaction -v
python -m unittest discover -s tests -v
python scripts/validate_coupled_transaction.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Completion requires all gates to pass, synchronized bilingual documentation,
explicit staged scope, a successful commit, and post-commit clean-state/hash
verification.
