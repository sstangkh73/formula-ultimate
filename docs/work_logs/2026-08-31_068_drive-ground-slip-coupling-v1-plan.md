# Work 068 Plan: Drive-to-Ground Slip Coupling v1

Status: Completed

Thai companion: `2026-08-31_068_drive-ground-slip-coupling-v1-plan.th.md`

## Objective

Couple the Work 067 transient powertrain output to the two Work 066 ground-propulsion components through geometry-derived effective radius and rotational inertia, a bounded longitudinal slip law, normal-load/friction limits, and forward vehicle translation. Torque must become contact force, vehicle kinetic energy, resistance work, or slip heat. A terminal drive-path failure must propagate to subsystem failure and race outcome `DNF`.

This is the first causal `stored energy -> shaft torque -> ground force -> vehicle acceleration` experiment. It remains a straight-line synthetic specimen rather than a complete tyre, suspension, differential, or race simulation.

## Research question and hypotheses

Question: can the independently validated powertrain deliver torque through declared ground interfaces without exceeding contact capacity or creating energy, while a broken drive path deterministically prevents race continuation?

Preferred hypothesis: the reference run produces finite positive acceleration, all contact forces remain within the Work 066 limits and the slip-law friction bound, the powertrain useful-work sink partitions into body work plus non-negative slip heat, global energy residual remains below the frozen threshold, exact replay and time-step refinement pass, and deliberate shaft failure yields `DNF` with zero subsequent drive torque.

Falsification includes motion with zero energy/throttle, ground force without torque, force beyond either `mu Fz` or the declared port/contact limit, a torque-to-force residual, negative unreported slip dissipation, vehicle energy exceeding powertrain output, incompatible geometry/inertia identity, failed drive connection transmitting torque, missing `DNF`, non-finite state, nondeterministic replay, or refinement disagreement beyond the declared bound.

## Model and equations

Each declared ground unit uses its Work 066 component/contact identity, effective radius `r`, geometry-derived axial inertia, normal load, friction coefficient, slip stiffness, and maximum longitudinal force. The sum of geometry-derived ground-unit inertia plus explicitly declared other downstream inertia must equal the Work 067 output inertia; no inertia may be silently duplicated.

For the forward-only v1 boundary:

```text
v_slip = r omega - v_vehicle
kappa = v_slip / max(v_vehicle, v_regularization)
F_capacity = min(mu Fz, F_declared)
F_requested = F_capacity tanh(C_kappa kappa / F_capacity), for kappa > 0
T_load = sum(F_applied r)
m dv/dt = sum(F_applied) - F_drag - F_rolling
```

Negative slip does not imply regeneration in v1; it requests zero drive force and remains observable in telemetry. The per-step interface partition is

```text
T_load omega = sum(F_applied v_vehicle)
               + sum(F_applied (r omega - v_vehicle)).
```

The second term is slip heat. The global ledger replaces the Work 067 useful-work sink with vehicle kinetic energy, aerodynamic/rolling work, and slip heat. Residuals are reported, never corrected.

## Experiment design

- Independent variables: throttle, duration, time step, mass, effective radii, geometry-derived inertia, other reflected inertia, normal loads, friction coefficient, longitudinal slip stiffness, contact limits, drag area, rolling resistance, and drive-failure limit.
- Dependent variables: ground-unit slip velocity/ratio, requested/applied force, contact utilization, axle load torque, vehicle acceleration/speed/distance, body work, slip heat, drag/rolling work, global energy residual, subsystem state, `DNF` reason/time, and deterministic hash.
- Controls: Work 066 architecture identity and geometry, Work 067 committed configuration, SI units, static normal-load closure, no regeneration, no reverse motion, deterministic fixed steps, canonical JSON, and no hidden repair.
- Metrics: maximum force/utilization/slip, torque-to-force and power-partition residuals, final speed/distance, energy residual, exact replay, and coarse/fine terminal differences.

Controls will include zero throttle, zero stored energy, friction saturation, geometry/inertia mismatch, invalid/non-finite declarations, deliberate shaft overload, exact replay, and half-step refinement. A separate analytical constant-state partition will verify `T omega = F v + Qdot_slip` independently of integration.

## Planned files

- `src/formula_ultimate/simulation/drive_ground_coupling.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_drive_ground_coupling_v1.json`
- `scripts/experiments/run_drive_ground_coupling.py`
- `tests/test_drive_ground_coupling.py`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.md`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.th.md`
- matching bilingual Work 068 plan/result records
- ignored deterministic evidence under `artifacts/work068/`

## Validation and success criteria

1. Ground component/contact IDs, radii, mass, contact limits, and axial inertias reconcile with Work 066 geometry within declared tolerance.
2. Ground-unit plus other reflected inertia reconciles exactly with the Work 067 output inertia.
3. The analytical torque/power partition closes to floating-point tolerance.
4. Zero throttle or zero stored energy produces zero ground force, speed, distance, and useful vehicle work.
5. Reference forces never exceed `min(mu Fz, declared maximum)` and axle load torque equals `sum(F r)`.
6. Slip heat is finite and non-negative; vehicle kinetic, drag, rolling, and slip terms replace powertrain useful work without hidden energy.
7. Reference global relative energy residual is `<= 1e-3` and every per-step torque/power residual is within the same relative ceiling.
8. Deliberate drive-path failure produces subsystem state `failed`, outcome `DNF`, exact reason/time, and zero transmitted/output drive torque afterward.
9. Canonical replay is exact; half-step refinement changes selected terminal metrics by `<= 2%`.
10. Focused/full tests, compilation, bilingual evidence, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

The regularized `tanh` slip law is synthetic and can only falsify plumbing and conservation errors; it is not a measured tyre curve. Static normal loads omit load transfer. A common output speed omits differential action and independent left/right wheel-speed states. Fixed-step explicit coupling can introduce phase error, which is exposed through global residual and refinement.

Work 068 does not implement combined lateral slip, steering, suspension motion, dynamic normal loads, road roughness, tyre temperature/wear, aquaplaning, wheel lift, differential/contact mechanics, regenerative braking, reverse motion, aerodynamic maps, race strategy, detailed shaft stress, measured calibration, physical validation, or safety certification. The reference topology remains a falsification fixture, not a required vehicle layout.
