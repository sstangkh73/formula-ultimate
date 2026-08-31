# Work 071 Plan: Coupled Planar Differential and Per-Step Load Transfer

Status: Completed

Thai companion: `2026-08-31_071_coupled-planar-differential-load-transfer-plan.th.md`

## Objective and scope

Couple the Work 070 independent driven-wheel/differential state to the Work 069 three-contact planar steering and geometry-derived load-transfer model. Each time step must solve contact normal loads, longitudinal wheel slip, lateral slip angle, combined-force capacity, powertrain load, differential modal motion, vehicle translation, and yaw as one deterministic fixed-point transaction.

This is a per-step acceleration-dependent quasi-static load redistribution, not a resolved suspension transient. It is a Level-0 coupled admission gate on the unchanged Work 069 geometry. The work must preserve all Work 070 energy and branch-limit contracts while adding body lateral/yaw energy and lateral-slip dissipation.

## Physical coupling

At each contact with body-frame position `(x_i, y_i)`, steer angle `delta_i`, body velocities `(u, v)`, and yaw rate `r`:

```text
v_x_body_i = u - r y_i
v_y_body_i = v + r x_i
v_x_local_i = cos(delta_i) v_x_body_i + sin(delta_i) v_y_body_i
v_y_local_i = -sin(delta_i) v_x_body_i + cos(delta_i) v_y_body_i
alpha_i = atan2(v_y_local_i, max(abs(v_x_local_i), v_regularization)).
```

Driven longitudinal request comes from each Work 070 wheel speed and normal-load-dependent slip capacity. Lateral request is `-C_alpha alpha_i`. Both are projected together onto the declared friction ellipse; saturation remains observable.

Per-step normal loads satisfy:

```text
sum(N_i) = m g
sum(x_i N_i) = -m a_x h
sum(y_i N_i) = -m a_y h.
```

The fixed-point loop must include aerodynamic drag, rolling resistance, powertrain load availability, combined-force projection, and load transfer. Negative normal load is terminal contact lift and is never clipped.

The differential still uses:

```text
omega_L = omega_c - delta_omega
omega_R = omega_c + delta_omega
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega.
```

Energy accounting adds planar body kinetic energy `0.5 m(u^2+v^2)`, yaw energy `0.5 I_z r^2`, lateral-slip heat `-F_y v_y dt`, longitudinal slip heat, branch-connection heat, differential heat, aerodynamic work, and rolling work. Body integration error and global conservation residual remain explicit outputs.

## Experiment design

- Independent variables: steer sign/magnitude, throttle, initial speed, step size, left/right friction, cornering stiffness, differential damping, geometry-derived centre of mass/inertia/contact locations, and force limits.
- Dependent variables: trajectory, heading, body velocities, yaw rate, carrier/branch speeds, differential modal energy, per-contact normal load/slip/forces/utilization, saturation, body work, all heat terms, equilibrium/interface/body/global residuals, contact lift, subsystem state, and replay hash.
- Controls: zero steer, equal positive/negative steer, split-grip and mirrored split-grip, excessive steer/contact-lift attempt, exact replay, and half-step refinement.
- Preferred hypothesis: zero steer remains symmetric with zero yaw/modal motion; opposite steer produces mirror trajectory/yaw; admitted steering retains all contacts and closes energy/balance gates; independent branch speeds remain kinematically tied to carrier average; deliberate excessive demand is rejected as contact lift or another explicit physical limit.
- Falsification: force from an unpowered rear support, hidden normal-load clipping, incorrect steer/yaw sign, mirror mismatch, differential average violation, missing lateral heat, contact/port limit violation, non-convergent fixed point presented as valid, or energy/refinement/replay failure.

## Planned files

- `config/vehicle/coupled_planar_differential_v1.json`
- `src/formula_ultimate/simulation/coupled_planar_differential.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_coupled_planar_differential.py`
- `tests/test_coupled_planar_differential.py`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.md`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.th.md`
- matching bilingual Work 071 result records
- ignored deterministic evidence under `artifacts/work071/`

## Validation and success criteria

1. Loader reconciles the Work 069 v3 architecture, Work 070 differential declaration, Work 067 powertrain, contact identities, geometry-derived mass/COM/yaw inertia, branch radius/inertia, actuator steer limit, and force/speed/torque limits.
2. Initial wheel/carrier/converter speeds are kinematically matched to the declared nonzero vehicle speed without hidden initial energy; total initial energy includes every rotating and body kinetic term.
3. The coupled fixed-point loop converges or returns an explicit invalid/DNF result; it never publishes an unconverged state.
4. Every admitted step closes vertical/pitch/roll, longitudinal/lateral/yaw, carrier-average, modal, torque, differential-interface, body-work, and global energy residual gates.
5. Zero steer retains zero lateral position, heading, lateral velocity, yaw rate, and differential-mode speed under symmetric grip within frozen tolerance.
6. Positive/negative admitted steer commands produce opposite finite yaw/trajectory signs and mirror selected states within tolerance.
7. Normal loads vary per step with acceleration, remain positive in admitted cases, and respect architecture limits; the passive rear contact transmits no propulsion torque.
8. Combined contact utilization stays `<= 1` within numerical tolerance, with saturation and unserved force observable.
9. A deliberate excessive steer or acceleration control reaches an explicit contact-lift/limit `DNF` without clipping.
10. Exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, bilingual evidence, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

The fixed-point coupling can become stiff near saturation or contact lift. The model uses rigid quasi-static normal-load redistribution and explicit body integration; it lacks spring/damper travel, roll centres, unsprung mass, wheel hop, tyre relaxation, camber, aligning moment, aero maps, road roughness, and measured coefficients. Numerical residual is evidence, not physical loss.

Work 071 does not add internal gear geometry, suspension solids, driver/path controller, track boundaries, lap timing, tyre temperature/wear, real-circuit admission, or physical validation. It does not establish race readiness.
