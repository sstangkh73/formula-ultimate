# Work Result 002: Level-0 Longitudinal Reference Kernel

Date: 2026-08-23
Status: Completed

## Summary

Implemented the first deterministic one-dimensional physics reference kernel
for Formula Ultimate. It simulates forward point-mass motion under constant
tractive force, aerodynamic drag, rolling resistance, and constant road grade.
The implementation exposes immutable state, per-step force telemetry, explicit
input failures, partial final timesteps, and the impulse introduced by the
forward-only zero-speed constraint.

The physics plan now also gives future agents explicit authority to generate
actual 3D component geometry, subject to trusted geometry/property/solver gates
before the component can influence 1D or race fitness.

## Changes

### Physics implementation

- Added `src/formula_ultimate/physics/longitudinal.py`.
- Added validated SI-unit parameter records for vehicle, environment, and
  integration configuration.
- Added immutable state, result, and per-step telemetry records.
- Added analytical drag, grade, and rolling-resistance force functions.
- Added fixed-step/partial-step longitudinal integration.
- Added an explicit within-step stop calculation and zero-speed constraint
  impulse rather than allowing reverse motion or silently hiding the boundary.
- Added distinct input and numerical error types.

### Validation

- Added `tests/test_longitudinal.py` with eight physics tests.
- Extended the repository contract so every plan marked `Completed` must have a
  matching result record; in-progress plans remain valid during work.
- Updated GitHub Actions to install the package before running the test suite.

### Research documentation

- Updated `docs/PHYSICS_SYSTEM_PLAN.md` with an agent-designed component
  geometry pipeline and 3D promotion gates.
- Updated `README.md` to distinguish the analytical reference kernel from a
  validated race-car simulator.

## Model Decisions

1. Only forward one-dimensional motion is permitted in this kernel.
2. Tractive force is commanded externally; no drivetrain behavior is implied.
3. Forces are evaluated at the start of each timestep.
4. Velocity uses constant-acceleration integration within the step and position
   uses average velocity.
5. The final timestep is shortened to end at the requested duration exactly.
6. A step that would cross into reverse integrates to its stopping time and
   records the remaining unilateral-constraint impulse.
7. Agent-generated 3D components cannot self-report mass, strength, cooling, or
   efficiency. Trusted extraction and multi-fidelity solvers produce those
   properties from immutable geometry/material artifacts.

## Validation Evidence

### Environment installation

Command:

```powershell
python -m pip install -e .
```

Environment: Windows, Python 3.14.3

Exit code: `0`

Result: editable package `formula-ultimate-0.0.1` built and installed.

### Complete test suite

Command:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

Result:

```text
8 longitudinal physics tests ... ok
5 repository contract tests ... ok

Ran 13 tests
OK
```

The physics cases cover:

- zero-input rest;
- constant-force analytical acceleration;
- drag-only coast-down convergence;
- grade equilibrium;
- rolling-resistance analytical deceleration;
- stop-without-reverse and constraint impulse;
- deterministic replay;
- invalid/non-finite input rejection.

### Analytical reference values

Command: executed the committed public API for a 1,000 kg lossless constant-force
case and a drag-only coast-down case.

Exit code: `0`

Result:

```text
constant_force: t=5.000000000000 s
                x=25.000000000000 m
                v=10.000000000000 m/s

drag_exact:     26.155187445510 m/s
dt=0.50 result: 26.131992459120 m/s  error=0.023194986390 m/s
dt=0.05 result: 26.152886710667 m/s  error=0.002300734843 m/s
fine/coarse error ratio: 0.099191
```

Reducing the timestep by 10 reduced the measured drag-reference speed error to
approximately 9.92% of the coarse error in this case.

### Compilation and pre-commit gates

Commands:

```powershell
python -m compileall -q src tests
git diff --cached --check
```

Expected final exit code for each: `0`.

The commands are rerun after this result record is staged. GitHub Actions then
runs the complete suite independently on Python 3.11 after push.

## Evidence Supporting the Intended Claim

- Constant-force motion matches its closed-form solution to the asserted
  floating-point tolerance.
- Grade equilibrium and constant rolling deceleration match their analytical
  references.
- Drag-only error decreases materially under timestep refinement.
- Identical inputs produce exactly equal immutable result records.
- Invalid parameters fail rather than entering the simulation.

## Evidence Against or Missing

- No energy-conservation audit exists yet.
- Drag integration is still explicit and first-order for changing force.
- Rolling resistance is a declared envelope, not a detailed tyre model.
- No component, powertrain, thermal, topology, lap, or race model exists.
- No Level-1 or empirical cross-validation has occurred.
- No 3D geometry has been generated or evaluated yet.

## Alternative Explanations

- Passing analytical cases demonstrates correctness only inside the narrow
  equations tested; it does not demonstrate race prediction accuracy.
- Deterministic replay can coexist with a consistently biased model.
- Timestep convergence toward one analytical drag case does not prove every
  future force/controller combination converges acceptably.

## Confidence

- High confidence in the tested constant-force, grade, and rolling analytical
  reference behavior.
- Moderate confidence in the bounded drag-only integration behavior pending a
  broader convergence matrix.
- Very low confidence for real-vehicle prediction because the necessary
  component, tyre, thermal, and validation layers do not yet exist.

## Deviations from Plan

- GitHub Actions and the repository-contract test were updated because the new
  importable source package requires installation and completed plans must be
  enforced symmetrically with result records.
- Zero-speed constraint impulse telemetry was added during review to avoid
  concealing the force/velocity effect of the forward-only boundary.

## Recommended Next Work

Work Plan 003 should add an energy/work audit around the reference kernel before
implementing motors or batteries. The audit should compare tractive work,
kinetic-energy change, road-load work, grade potential-energy change, and the
zero-speed constraint contribution under timestep refinement.
