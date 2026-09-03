# Work 088 Plan: Whole Mechanical Vehicle Candidate 001 Admission Audit

Thai companion: `2026-09-04_088_whole-mechanical-vehicle-candidate-001-plan.th.md`

## Status

Status: Completed

## Objective

Execute the scope originally numbered Work 086 after the two inserted structural-remediation works. Assemble an immutable, deterministic whole-candidate evidence index from the exact Work 083, 084, 086, and 087 results; verify all required CAD and report artifacts; evaluate every preregistered whole-vehicle admission case; and either admit the candidate to Level 0 or stop before simulation with a machine-readable `not_ready` verdict.

The expected verdict is `not_ready` because Work 087 recorded forbidden geometry interference, a motion-interface mismatch, missing meshed convergence for the new load frame, and synthetic material/process evidence. Producing the correct fail-closed verdict is the success criterion for this audit; it is not permission to relabel the candidate as a complete vehicle.

## Scope and planned files

- Add `config/candidates/whole_mechanical_vehicle_candidate_001.json` with frozen source identities, seed, required artifact classes, admission cases, and evidence policy.
- Add `src/formula_ultimate/experiments/whole_mechanical_vehicle_candidate.py` for schema, identity, artifact, case, blocker, and replay checks.
- Add `scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py` to create an immutable evidence bundle without mutating upstream geometry.
- Add `tests/test_whole_mechanical_vehicle_candidate_001.py` with positive audit, source-tamper, missing-artifact, blocker-suppression, premature-simulation, synthetic-evidence, case-omission, and replay tests.
- Add `docs/contracts/WHOLE_MECHANICAL_VEHICLE_CANDIDATE_001.md` and its Thai companion.
- Add this plan/result and their Thai companions.
- Generate ignored evidence under `artifacts/work088/`.

## Independent/dependent variables, controls, and metrics

- Independent variables are limited to the frozen evidence bundle and injected falsification controls; no geometry parameter may change in this work.
- Dependent outputs are source/artifact identity status, per-case readiness, blocker set, Level-0 execution status, candidate verdict, bundle identity, and replay equality.
- Controls: one changed source identity, one missing artifact, one suppressed blocker, one forced simulation request, one relabelled evidence class, one omitted admission case, and one replay.
- Metrics: exact SHA-256 identity equality, required-artifact coverage, required-case coverage, blocker preservation, `level0_simulation.status`, deterministic result equality, and test exit status.

## Validation and success criteria

- Verify the seventeen individual STEP files, complete assembly STEP, FCStd, assembly tree, joint/DOF manifest, material manifest, mass/COM/inertia report, interference report, structural report, energy ledger, failure report, replay manifest, and Level-0 decision record.
- Evaluate static support, acceleration, braking, steady cornering, combined braking/cornering, bump/vertical event, torque reaction, thermal-duration, single-connection failure, refinement/replay, and mirrored/control cases.
- Preserve every upstream blocker and prove that blocked admission prevents Level-0 execution.
- Produce two byte-identical result files from the same config and source evidence.
- Pass focused tests, repository-contract tests, compilation, and full regression.

## Risks, non-goals, and stop conditions

Risks include treating an indexed report as new physical evidence, confusing a correct audit with vehicle admission, accepting stale ignored artifacts, and letting a later passing check mask a blocker. The runner must fail closed on identity or schema corruption and return a valid `not_ready` decision when intact evidence contains blockers.

This work does not repair geometry, create missing structural evidence, run an inadmissible Level-0 simulation, validate materials, establish crashworthiness or safety, claim race completion, optimize topology, or claim physical validation. If source identities or required artifacts cannot be verified, stop the audit as invalid rather than infer missing evidence.
