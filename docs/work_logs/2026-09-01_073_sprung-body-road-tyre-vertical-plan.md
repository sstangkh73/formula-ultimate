# Work 073 Plan: Sprung-Body Heave/Pitch/Roll, Road, and Tyre Vertical Coupling

Status: Completed

Thai companion: `2026-09-01_073_sprung-body-road-tyre-vertical-plan.th.md`

## Objective and scope

Replace the unresolved vertical boundary of Work 072 with a coupled linear vertical system containing sprung-body heave, pitch, and roll; one geometry-derived unsprung displacement per contact; suspension springs/dampers; tyre vertical springs/dampers; and deterministic road displacement. Actual tyre normal load must feed the Work 071 combined-force ellipse inside the same acceleration/load fixed point.

This is a synthetic Level-0 whole-vehicle vertical-dynamics gate on the unchanged Work 069 v3 geometry and Work 071 horizontal drivetrain/planar dynamics. It must preserve the Work 072 result when Work 073 is not selected, expose all vertical energy paths, and fail without clipping on contact loss or suspension travel exhaustion.

## Geometry-derived properties and coordinates

Ground-contact component masses remain the Work 072 effective unsprung masses. Sprung mass is the sum of every architecture component not assigned to a ground contact. Sprung roll and pitch inertia are assembled from those components' primitive centroidal inertia and parallel-axis terms about the declared whole-vehicle centre of mass. The loader must reconcile these identities with the materialized architecture.

All vertical displacements are measured from static equilibrium and are positive upward. Generalized coordinates are:

```text
q = [z_s, theta, phi, z_u1, z_u2, z_u3]
```

where `z_s` is sprung heave, `theta` is pitch about body `y`, `phi` is roll about body `x`, and `z_ui` is each unsprung position. At contact `(x_i, y_i)` relative to the declared vehicle centre of mass:

```text
z_body_i = z_s - x_i theta + y_i phi
s_i = z_ui - z_body_i
t_i = z_road_i - z_ui.
```

`s_i` is suspension compression and `t_i` is tyre compression.

## Equations and coupling

Suspension and tyre incremental forces are:

```text
F_s,i = k_s,i s_i + c_s,i s_dot_i
F_t,i = k_t,i t_i + c_t,i t_dot_i
N_actual,i = N_0,i + F_t,i.
```

The assembled linear system is:

```text
M q_ddot + C q_dot + K q = f_inertial(a_x, a_y) + f_road(z_road, z_dot_road).
```

Horizontal acceleration creates explicit pitch/roll generalized forces about centre-of-mass height `h`:

```text
Q_theta = -m a_x h
Q_phi   =  m a_y h.
```

The system is advanced with implicit midpoint. During every Work 071 fixed-point iteration, the quasi-static target load is used only to reconstruct the current `a_x/a_y` inertial forcing; Work 073 solves the vertical state and returns `N_actual` to the tyre model. A singular matrix, non-finite state, or excessive residual is invalid and cannot commit.

## Energy ledger

Vertical stored energy contains sprung/unsprung kinetic energy, suspension spring energy, and tyre spring energy relative to the current road position. Dissipation contains suspension-damper and tyre-damper heat. External work is:

```text
W_inertial = Q_inertial dot (q_body,new - q_body,old)
W_road = sum(F_t,i z_dot_road,i dt)
R_vertical = delta(E_vertical) + Q_suspension_damper + Q_tyre_damper
             - W_inertial - W_road.
```

Initial vertical energy, if any, must be deducted from the fixed `50,000,000 J` storage budget. Road work remains an explicit external input. Horizontal and vertical ledgers remain separate and are combined only through a declared conservation residual.

## Experiment design

- Independent variables: steering sign, time step, geometry-derived mass/inertia, suspension stiffness/damping, tyre vertical stiffness/damping, and per-contact road profile amplitude/start/duration.
- Dependent variables: heave/pitch/roll and rates, unsprung states, suspension/tyre deflection, actual load, all vertical forces, stored energy, damper heats, inertial/road work, force/energy residuals, horizontal trajectory/yaw, terminal state, and replay identity.
- Controls: Work 072 preservation, flat-road reference, zero steer, opposite-steer mirror, single-contact raised-cosine bump and its spatial mirror, zero tyre damping, soft-tyre scale, road-drop contact loss, large-bump travel failure, exact replay, and half-step refinement.
- Preferred hypothesis: flat-road horizontal acceleration excites finite heave/pitch/roll while all contacts remain valid; mirror controls exchange left/right states; bump input produces nonzero road work and local load response; zero tyre damping produces zero tyre heat; soft tyres alter response; extreme road controls fail explicitly.
- Falsification: mass/inertia double counting, wrong pitch/roll signs, tyre target load bypassing vertical dynamics, road motion doing no work, damping creating energy, hidden clipping, missing contact identity, singular solve presented as valid, Work 072 hash drift, or mirror/replay/refinement failure.

## Planned files

- `config/vehicle/sprung_body_road_tyre_vertical_v1.json`
- `src/formula_ultimate/simulation/sprung_body_vertical_coupling.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_sprung_body_vertical_coupling.py`
- `tests/test_sprung_body_vertical_coupling.py`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.md`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.th.md`
- matching bilingual Work 073 result records
- ignored deterministic evidence under `artifacts/work073/`

## Validation and success criteria

1. Loader derives sprung mass and roll/pitch inertia from non-ground architecture components and rejects identity or mass closure mismatch.
2. Work 072 unselected control retains its committed result SHA-256.
3. The implicit-midpoint matrix solve closes all six generalized equations and the vertical energy equation within `1e-9` relative tolerance.
4. Initial total accounted energy remains exactly `50,000,000 J`.
5. Flat-road reference finishes 500 steps with positive actual loads, suspension travel within `0.05 m`, and nonzero finite body-mode response.
6. Actual tyre load is the exact load used by Work 071 contact force capacity.
7. Zero steer is left/right symmetric; opposite steer mirrors roll, left/right unsprung states, loads, and selected planar/yaw states.
8. A raised-cosine bump produces nonzero signed road work and an observable local load response; its spatial mirror exchanges left/right evidence.
9. Zero tyre damping produces exactly zero tyre-damper heat; soft-tyre response differs from reference.
10. Road-drop and large-bump controls terminate as `contact_loss` or `suspension_travel` without clipping.
11. Exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, bilingual repository contract, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

This linear small-angle model omits nonlinear linkage kinematics, motion ratios from CAD joints, bump stops, tyre enveloping/contact-patch pressure, chassis flex, anti-dive/squat geometry, damper hysteresis, wheel gyroscopic coupling, aero downforce, measured road spectra, and sub-step failure localization. Horizontal inertial forcing uses the declared whole-vehicle mass and centre-of-mass height while sprung properties exclude ground components; that convention is explicit but not experimentally calibrated.

Work 073 does not add path control, track boundaries, lap timing, detailed suspension CAD, structural FEA, measured parameter identification, or physical validation. It cannot establish race readiness.
