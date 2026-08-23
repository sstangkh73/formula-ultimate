# Work Plan 002: Level-0 Longitudinal Reference Kernel

Date: 2026-08-23
Status: Completed

## Objective

Implement and test the first deterministic one-dimensional physics kernel for
Formula Ultimate while preserving an explicit future path for agents to design
the geometry of physical components in 3D.

## Scope

- Implement a bounded forward-motion longitudinal point-mass model.
- Model constant commanded traction, aerodynamic drag, rolling resistance, and
  road grade using SI units.
- Produce immutable state and per-step telemetry suitable for replay.
- Reject invalid or non-finite physics inputs explicitly.
- Validate the kernel against analytical reference cases and deterministic
  replay.
- Document how future agent-generated 3D components will be promoted into the
  1D system through independently measured physical properties.

## Non-Goals

- Powertrain component graphs or topology evolution.
- Gearbox, motor, battery, ICE, or thermal component implementation.
- Tyre slip curves or lateral vehicle dynamics.
- 3D geometry generation, meshing, CFD, or FEA implementation.
- Claiming that the Level-0 kernel predicts a real race car.

## Planned Deliverables

- `src/formula_ultimate/physics/longitudinal.py`
- `tests/test_longitudinal.py`
- Updates to `docs/PHYSICS_SYSTEM_PLAN.md` describing the 1D-to-3D contract.
- Updates to `README.md` reflecting the implemented reference kernel.
- `docs/work_logs/2026-08-23_002_level0-reference-kernel-result.md`

## Model Boundary

- Vehicle motion is non-negative and one-dimensional.
- Vehicle mass and road-load parameters are fixed during a run.
- Tractive force is an external command; drivetrain physics is deferred.
- Force is evaluated at the beginning of each fixed/partial timestep.
- Velocity is integrated from acceleration; position uses average velocity over
  the step, with an explicit within-step stop calculation when needed.
- Grade is constant within the reference scenario.

## Validation Plan

1. Zero-input vehicle at rest remains at rest.
2. Constant-force acceleration without losses matches the analytical solution.
3. Drag-only coast-down approaches the analytical solution as timestep shrinks.
4. Grade-equilibrium traction maintains constant speed without other losses.
5. An underpowered vehicle cannot integrate into negative speed or distance.
6. Invalid mass, timestep, duration, coefficients, and non-finite inputs fail.
7. Identical inputs produce identical state and telemetry sequences.
8. Run the complete repository test suite, Python compilation, and Git diff
   whitespace gate.

## Success Criteria

- All planned analytical/invariant tests pass on Windows and GitHub Actions.
- The implementation uses explicit SI-unit names and no hidden global state.
- Final time is exact even when duration is not divisible by the base timestep.
- The result record preserves the exact commands and concise outputs.
- Documentation distinguishes agent-designed 3D geometry from catalog-only
  parameter selection and defines promotion evidence.

## Failure Criteria

- The kernel cannot reproduce constant-force analytical motion within floating
  point tolerance.
- Smaller timesteps do not reduce error in the chosen drag-only reference case.
- Invalid states are silently clipped other than the explicitly declared
  zero-speed boundary.
- A 3D component can self-report unverified mass/performance into the 1D model.

## Risks and Controls

- Numerical results may look plausible while being wrong: use closed-form
  analytical references and convergence tests.
- Static friction is outside the first model: clearly define rolling-resistance
  activation and avoid claiming tyre fidelity.
- A fixed Level-0 component catalog could suppress future invention: define a
  promotion interface for generated geometry and solver-derived properties.
- 3D agents may exploit mesh/solver defects: require geometry validity,
  independent property extraction, multi-fidelity analysis, and replayable
  artifacts before a generated component affects research fitness.
