# Work 021 Result: Coupling Contract and Architecture Compiler

Status: Completed

Thai companion: `2026-08-28_021_coupling-contract-architecture-result.th.md`

## Outcome

Work 021 established the first executable central boundary for future coupled
vehicle simulation. It provides a deterministic architecture compiler, pinned
experiment manifest, topology-neutral shared runtime state, observable residual
ledger, and deterministic event arbitration. It also records the ordered Work
021–030 implementation queue.

This is a contract and architecture result. It executes zero vehicle-physics
modules and is not evidence of a coupled vehicle or physical validation.

## Files changed

- `config/simulation/coupled_level0_architecture_v1.json`: versioned eight-stage
  reference architecture.
- `src/formula_ultimate/simulation/coupling.py`: contracts, compiler, manifest,
  shared state, residual ledger, and event arbitration.
- `src/formula_ultimate/simulation/__init__.py`: public coupling exports.
- `tests/test_coupling_contracts.py`: 12 focused contract and falsification
  tests.
- `scripts/validate_coupling_contracts.py`: deterministic evidence generator.
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` and `.th.md`:
  ordered Work 021–030 queue.
- `docs/simulation/COUPLING_CONTRACT_AND_ARCHITECTURE.md` and `.th.md`:
  architecture and claim-boundary documentation.
- this bilingual plan/result pair.
- `docs/problem_reports/2026-08-28_021_json-loader-type-coercion.md` and
  `.th.md`: resolved loader problem and evidence.

## Decisions

- Use eight causal stages: `inputs`, `aerodynamics`, `load_balance`,
  `contact_limits`, `motion`, `energy_audit`, `health`, and `race_progress`.
- Require every consumed signal to be an initial signal or have exactly one
  producer in a strictly earlier stage.
- Canonicalize declarations before SHA-256 hashing so module input order cannot
  alter architecture or experiment identity.
- Keep contacts and component-health records as arbitrary uniquely identified
  collections; do not encode a four-wheel, axle, body, or powertrain layout.
- Preserve residual values exactly and expose invalidity instead of correcting
  conservation errors silently.
- Resolve simultaneous events by declared priority after earliest-time
  localization within a fixed tolerance.
- Treat all JSON schema/type errors as invalid declarations, not values to
  coerce.

## Problem encountered and resolution

The first passing implementation coerced several JSON values with `str(...)`.
Review showed that a numeric `architecture_id` could therefore be accepted as a
string. The separate problem report records the defect. Strict JSON string and
string-array readers replaced coercion, and a numeric-ID regression test now
requires `CouplingContractError`. All gates passed after the correction.

## Evidence and validation

Commands were run from `C:\Formula Ultimate` on 2026-08-28 with fail-fast exit
handling.

```powershell
python -m unittest tests.test_coupling_contracts -v
# exit 0; Ran 12 tests in 0.030s; OK

python -m unittest discover -s tests -v
# exit 0; Ran 166 tests in 0.445s; OK

python scripts/validate_coupling_contracts.py
# exit 0
# architecture fingerprint:
# 51ca53e9d4c6058f67f61dc57f3ece7e8c24176d915e74069f27d0aa6999f8a6
# manifest fingerprint:
# 7f40394bf539ef230870a758cfba81c093268d38f52c7efac359fdd9ec5fb416
# input_permutation_equal: true
# contact_count: 3
# residual status: invalid; raw_energy_residual_j: -2.0
# exact event tie winner: finished
# physics_execution_count: 0

python -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

The final staged-scope check and commit verification are performed after this
result record is staged, as required by the repository protocol.

## Experiment review

- Supporting evidence: architecture and manifest fingerprints are invariant to
  declaration ordering; the reference covers all eight stages; arbitrary
  three-contact state is accepted; invalid dependency, hash, contact, residual,
  event, and JSON-type cases remain explicit.
- Contradicting evidence: none within the declared contract-only hypothesis.
- Alternative explanation: deterministic results come from schema
  canonicalization and do not demonstrate correct physical equations.
- Missing evidence: adapters, atomic state transition, cross-domain force and
  energy exchange, numerical convergence, ten-circuit integrated races, and
  higher-fidelity validation.
- Confidence: high that the central contract behaves as tested; no confidence
  increase is claimed for whole-vehicle physical accuracy.

## Limitations and follow-up

Signal names do not yet carry executable unit/semantic adapters. Work 022 is
therefore next: implement an atomic coupled-step transaction so modules read one
immutable start state and either commit one complete next state or return an
observable invalid result without partial mutation.

No push or remote publication was performed.
