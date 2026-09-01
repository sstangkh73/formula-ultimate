# Work 072 Plan: Transient Suspension, Wheel Load, and Contact Coupling

Status: Completed

Thai companion: `2026-09-01_072_transient-suspension-wheel-contact-plan.th.md`

## Objective and scope

Extend the committed Work 071 planar/differential/load-transfer transaction with one transient vertical suspension state per geometry-derived ground contact. Quasi-static load-transfer output becomes a target load, while effective unsprung mass, spring stiffness, damping, travel, and velocity determine the normal load actually available to the tyre during the step.

This is a synthetic Level-0 transient load-path gate on the unchanged Work 069 v3 geometry and Work 071 horizontal dynamics. It must expose delayed load response, suspension energy, damping loss, travel exhaustion, contact loss, and numerical error. It must not present a clipped load, failed contact, or unconverged coupled step as valid.

## Physical model

For each contact `i`, displacement `z_i` is measured from its declared static preload equilibrium and positive displacement means compression. Geometry-derived ground-component mass is used as the effective unsprung mass `m_i`. The Work 071 quasi-static solution supplies target load `N_target,i`; static preload is `N_0,i`:

```text
delta_N_i = N_target,i - N_0,i
m_i z_ddot_i = delta_N_i - k_i z_i - c_i z_dot_i
N_actual,i = N_0,i + k_i z_mid,i + c_i z_dot_mid,i.
```

The oscillator is advanced with an implicit-midpoint step. `N_actual,i`, not `N_target,i`, sets the combined tyre-force ellipse in the Work 071 transaction. The callback is evaluated inside the same acceleration/load-transfer fixed point, so target load, suspension response, tyre force, body acceleration, wheel speed, and differential state must converge together.

The per-contact vertical energy ledger is:

```text
E_i = 0.5 m_i z_dot_i^2 + 0.5 k_i z_i^2
W_boundary,i = delta_N_i (z_new,i - z_old,i)
Q_damper,i = c_i z_dot_mid,i^2 dt
R_energy,i = delta(E_i) - W_boundary,i + Q_damper,i.
```

Boundary work is explicit energy exchanged with omitted sprung-body heave/pitch/roll modes; it is not silently sourced from the horizontal drivetrain. Initial suspension perturbation energy must be deducted from the fixed `50,000,000 J` storage budget so controls cannot create hidden energy.

Actual normal load `<= 0 N` is terminal `contact_loss`. Compression or rebound beyond declared travel is terminal `suspension_travel`. Values are preserved without clipping. V1 detects these events at the deterministic transaction boundary; exact sub-step event localization is a non-goal and limitation.

## Experiment design

- Independent variables: steering sign, time step, per-contact geometry-derived effective mass, spring stiffness, damping ratio, compression/rebound travel, and controlled initial travel/velocity perturbations.
- Dependent variables: target and actual normal load, travel, vertical velocity/acceleration, suspension energy, boundary work, damper heat, dynamic force/energy residuals, planar trajectory/yaw, wheel/differential speed, tyre utilization, terminal reason/time, and replay hash.
- Controls: rigid Work 071 reference, transient reference, zero steer, opposite-steer mirror, zero damping, stiffness change, immediate contact-loss perturbation, travel-exhaustion perturbation, exact replay, and half-step refinement.
- Preferred hypothesis: the transient reference finishes with positive loads and bounded travel; actual load differs observably from quasi-static target; mirror steering exchanges left/right vertical states; zero damping produces zero damper heat; softer stiffness changes response; deliberately infeasible perturbations fail as contact loss or travel exhaustion.
- Falsification: actual load is ignored by tyre capacity, preload or component identity is mismatched, hidden clipping occurs, damping creates energy, vertical force/energy residual exceeds tolerance, initial perturbation energy is added outside the energy budget, mirror/replay/refinement fails, or a failed suspension continues transmitting valid force.

## Planned files

- `config/vehicle/transient_suspension_coupling_v1.json`
- extension hook in `src/formula_ultimate/simulation/coupled_planar_differential.py`
- `src/formula_ultimate/simulation/transient_suspension_coupling.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_transient_suspension_coupling.py`
- `tests/test_transient_suspension_coupling.py`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.md`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.th.md`
- matching bilingual Work 072 result records
- ignored deterministic evidence under `artifacts/work072/`

## Validation and success criteria

1. Loader reconciles the exact Work 071 declaration, materialized architecture, contact/component identities, static preloads, geometry-derived component masses, contact limits, and SI numerical domain.
2. Work 071 without a transform retains byte-identical reference evidence and its existing tests.
3. Every transient contact satisfies the midpoint force equation and vertical energy equation within declared `1e-9` relative tolerance.
4. Initial total accounted energy remains exactly `50,000,000 J`, including any initial suspension kinetic/spring energy.
5. The reference finishes all 500 steps; every actual load is positive, every travel stays inside its envelope, and actual load affects tyre utilization/force.
6. Zero steer preserves left/right symmetry. Opposite steer mirrors left/right suspension travel, velocity, load, and selected planar/yaw states within tolerance.
7. Zero damping produces exactly zero damper heat; a stiffness control changes at least one frozen response metric.
8. Contact-loss and travel-exhaustion controls terminate as explicit `DNF` without clipping or post-failure force transmission.
9. Work 071 horizontal energy gates and the new suspension/global-with-boundary energy gates both pass.
10. Exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, bilingual repository contract, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

The synthetic single-degree oscillator does not resolve tyre vertical stiffness, sprung-body heave/pitch/roll inertia, suspension linkage kinematics, motion ratio, roll centres, anti-dive/squat, bump stops, wheel geometry deformation, road displacement, tyre relaxation, or measured damping hysteresis. The geometry supplies component identity and effective mass, but spring/damper coefficients are declared experiment inputs rather than CAD-derived or measured values.

Work 072 does not add brake actuation, aero-map coupling, path control, track boundaries, lap timing, structural FEA of suspension members, detailed joints/fasteners, CAD solids, or physical validation. It cannot establish race readiness.
