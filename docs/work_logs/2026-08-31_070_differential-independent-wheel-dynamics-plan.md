# Work 070 Plan: Differential and Independent Driven-Wheel Dynamics

Status: Completed

Thai companion: `2026-08-31_070_differential-independent-wheel-dynamics-plan.th.md`

## Objective and scope

Replace the Work 068 common-wheel-speed assumption with an explicit, energy-conserving differential/carrier contract for the two powered contacts of the Work 069 v3 stable-support reference. The model must permit different left/right angular speeds when contact loads differ, retain geometry-derived radius/inertia and static normal loads, respect architecture port/connection limits, expose all loss and residual terms, and propagate a differential/branch failure to `DNF`.

This work changes the dynamic model and experiment declaration only. It reuses the exact Work 069 materialized 3D architecture and STEP/FreeCAD evidence because no exterior solid changes. The differential remains a lumped law inside the existing `torque_transmission` component; resolving gears/bearings as separate solids is explicitly deferred.

## Physical model and no-double-counting rule

For carrier speed `omega_c` and differential-mode speed `delta_omega`:

```text
omega_L = omega_c - delta_omega
omega_R = omega_c + delta_omega
omega_c = (omega_L + omega_R) / 2.
```

Work 067 output inertia `J_output = 2.5 kg m^2` already contains the common-mode contribution of both geometry-derived wheel inertias:

```text
J_output = J_other + J_L + J_R.
```

Therefore the independent-mode energy adds only

```text
E_delta = 0.5 (J_L + J_R) delta_omega^2,
```

and never adds the wheel common-mode inertia again. With reflected branch load torques `q_L`, `q_R`, modal inertia `J_delta = J_L + J_R`, and differential damping `c_delta`:

```text
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega.
```

The implicit-midpoint damping update must close this identity per step:

```text
W_carrier = W_reflected_branches + Delta(E_delta) + Q_differential.
```

Each architecture branch connection has declared efficiency `eta = 0.98`. Wheel torque `tau_i` is reflected upstream as `q_i = tau_i / eta`; the difference `q_i omega_i - tau_i omega_i` is observable connection heat. Wheel input work then partitions into body work plus slip heat. Negative dissipation beyond tolerance is invalid rather than clipped silently.

## Experiment design

- Independent variables: left/right friction coefficient, static normal load derived from v3 geometry, throttle, initial energy, step size, branch connection efficiency, differential damping, and branch speed limit.
- Dependent variables: carrier/left/right speed, differential-mode speed and energy, per-branch drive/load torque, force/slip/utilization, connection heat, differential heat, vehicle speed/distance, interface/global energy residuals, failure state/time, and replay hash.
- Controls: symmetric grip, zero energy, mirrored split grip, deliberately reduced admissible branch-speed limit, half-step refinement, immutable Work 069 geometry, fixed powertrain declaration, and exact deterministic ordering.
- Preferred hypothesis: symmetric grip keeps `delta_omega = 0`; split grip produces finite unequal branch speeds without violating the carrier average or energy identity; mirrored grip exchanges branch states; all admitted runs respect limits and replay exactly.
- Falsification: common speed persists under unequal load, carrier average fails, wheel inertia is counted twice, branch connection loss disappears, hidden energy is created, a branch exceeds port speed/torque without `DNF`, zero energy creates motion, mirrored cases are asymmetric, or half-step/replay gates fail.

## Planned files

- `config/vehicle/functional_differential_drive_v1.json`
- `src/formula_ultimate/simulation/differential_drive_coupling.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_differential_drive.py`
- `tests/test_differential_drive_coupling.py`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.md`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.th.md`
- matching bilingual Work 070 result records
- ignored deterministic evidence under `artifacts/work070/`

## Validation and success criteria

1. The loader materializes and validates the Work 069 v3 architecture, identifies exactly two powered branches, and reconciles component/contact/port/connection identities.
2. Radius and axial inertia match the 3D component geometry within relative tolerance `<= 1e-9`; `J_other + J_L + J_R = 2.5 kg m^2` within that tolerance.
3. Static driven-contact loads match Work 069's equilibrium solution; the passive rear contact is not treated as a propulsion source.
4. At every admitted step, `(omega_L + omega_R)/2 = omega_c`, branch speeds are nonnegative and within architecture limits, and transmitted torque respects port limits.
5. Symmetric grip keeps independent-mode speed/energy zero within numerical tolerance.
6. Unequal grip creates nonzero independent speeds and modal energy while carrier/interface/global energy residuals remain below declared ceilings.
7. Mirrored unequal-grip controls exchange left/right states and retain equal aggregate vehicle metrics within tolerance.
8. Zero onboard energy produces zero drive torque, force, vehicle motion, and differential-mode energy.
9. A deliberate admissible low branch-speed limit produces an observable terminal branch-overspeed `DNF`; execution after terminal failure is rejected.
10. Exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, bilingual evidence, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

The model is an ideal open-differential kinematic/energy specimen with lumped damping. It does not resolve tooth contact, backlash, bearing compliance, housing stress, lubricant flow, torque-vectoring control, limited-slip clutch friction, brake intervention, reverse rotation, wheel hop, transient suspension, tyre thermal/wear state, or measured coefficients. Fixed static normal loads are retained from Work 069; transient load transfer remains outside this longitudinal specimen.

Work 070 does not claim real handling, durability, manufacturing readiness, race completion, or physical validation. It does not change 3D solids. Separate internal differential geometry and structural/thermal verification will be required before a detailed whole-car claim.
