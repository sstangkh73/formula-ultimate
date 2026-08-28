# Work 026 Plan: Coupled Motion Integration

Status: Completed

Thai companion: `2026-08-28_026_coupled-motion-integration-plan.th.md`

## Objective

Implement one deterministic Level-0 motion step that advances longitudinal and lateral velocity, yaw rate, yaw, planar position, time, and race distance from the summed aerodynamic and contact force/moment signals. Corridor and numerical failures must remain observable.

## Scope

- Define typed motion configuration, candidate state, integration evidence, and corridor evidence.
- Sum the Work 024 aerodynamic wrench and Work 025 contact wrench without hidden force or moment corrections.
- Integrate planar rigid-body motion in SI units using a documented deterministic scheme.
- Advance race distance from corridor-tangent progress, not total speed magnitude.
- Reject missing or unsupported spatial evidence and expose corridor departure, reverse progress, non-finite state, and failed residuals.
- Add analytical-reference, timestep-refinement, deterministic-replay, adapter-contract, and failure tests.
- Add a standalone validator and bilingual model/result documentation.
- If the current coupling architecture cannot provide the required corridor signal, record a separate bilingual problem report and fix it with a new versioned architecture rather than silently changing historical evidence.

## Planned Files

- `src/formula_ultimate/simulation/motion_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_motion_coupling.py`
- `scripts/validate_motion_coupling.py`
- `docs/simulation/COUPLED_MOTION_INTEGRATION.md`
- `docs/simulation/COUPLED_MOTION_INTEGRATION.th.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.th.md`
- this plan and Thai companion
- matching result records
- versioned architecture/test/problem-report files only if the signal-contract audit proves they are required

## Experiment Definition

- Independent variables: force and yaw-moment inputs, timestep, initial body velocity/yaw rate, segment curvature/grade/bank/width, and vehicle corridor margin.
- Dependent variables: next velocity, yaw rate, yaw, position, race-distance increment, integration residuals, and corridor status.
- Controls: mass, yaw inertia, initial state, integration method, input provenance, and deterministic ordering.
- Metrics: analytical state error, coarse-versus-refined timestep error, force/moment residuals, corridor clearance, replay equality, and invalid-output count.
- Success criteria: analytical fixtures match declared tolerances; refinement reduces error on a curved-motion fixture; all declared residuals pass; deterministic replay is exact; corridor departure and missing evidence invalidate the adapter with zero output signals.
- Failure criteria: non-finite or dimensionally invalid input is accepted; race distance advances from lateral/reverse motion; a failed corridor check is hidden; result changes with input ordering; or a failing residual is committed.
- Falsification attempt: include lateral-only, reverse-motion, off-corridor, insufficient-width, missing-spatial-evidence, and deliberately inconsistent wrench fixtures.

## Validation

1. Focused Work 026 unit tests.
2. Entire repository test suite.
3. Standalone Work 026 validator with analytical and refinement evidence.
4. Python bytecode compilation.
5. `git diff --check` and `git diff --cached --check`.
6. Explicit staged-scope inspection before commit.

## Success Criteria

- One candidate motion state is produced from the exact summed wrenches.
- Longitudinal, lateral, yaw, position, time, and corridor-tangent race progress are coupled and replayable.
- Analytical, refinement, residual, and corridor gates pass.
- All failure paths are observable and emit no candidate state.
- English and Thai records agree on equations, units, commands, evidence, limitations, and status.
- The completed work is committed as its own validated commit.

## Risks

- The Work 021 architecture may not route `circuit.segment_inputs` into the motion module.
- A local spatial sample may be insufficient to reconstruct a full surveyed centerline.
- First-order integration can conserve the declared force balance while accumulating trajectory error.
- Treating race distance as speed magnitude would falsely reward lateral or reverse motion.

## Explicit Non-goals

- No claim of calibrated, surveyed-circuit, CFD, tyre-rig, or physical validation.
- No full-race orchestrator, energy/thermal state commit, lap event arbitration, or Work 027-030 implementation.
- No silent projection back onto the corridor and no hidden force redistribution.
- No optimization of a vehicle design.
