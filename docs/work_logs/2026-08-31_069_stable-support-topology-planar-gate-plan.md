# Work 069 Plan: Stable Support Topology and Planar Gate

Status: Completed

Thai companion: `2026-08-31_069_stable-support-topology-planar-gate-plan.th.md`

## Objective and discovered prerequisite

Falsify the Work 066/068 reference ground-support topology before adding independent wheel speeds and steering dynamics. The current two contacts both lie at `x = 0.45 m`, while the geometry-derived centre of mass lies at `x = -0.024952088769517506 m`. Their line segment therefore cannot contain the centre-of-mass projection or balance static pitch moment. Dynamic load transfer on that topology would simulate a vehicle that is already statically unstable.

Work 069 will preserve the frozen v2 fixture as evidence, create a separate technology-neutral v3 reference with one passive rear support contact, regenerate STEP/FreeCAD evidence, and implement a support/load-transfer/planar steering admission gate. A three-contact reference avoids prescribing a conventional four-wheel layout while creating a support polygon that can contain the centre of mass.

Independent left/right wheel-speed and differential dynamics move to Work 070 because Work 067 currently has one common output speed. Splitting it without an explicit differential/carrier energy contract would duplicate inertia or create energy.

## Research question and hypotheses

Question: can a minimally remediated free-topology architecture produce a geometry-derived support polygon that contains the centre of mass, closes vertical/pitch/roll equilibrium under declared acceleration cases, retains all Work 066 functional paths, and generates a bounded nonzero steering/yaw response?

Preferred hypothesis: the v3 three-contact reference passes architecture, overlap, STEP, FreeCAD, support-polygon, static load, bounded longitudinal/lateral transfer, combined-force, steering-sign, exact-replay, and refinement checks. The frozen v2 topology must fail the support-polygon gate.

Falsification includes v2 incorrectly passing, a v3 contact outside its solid or support connection, centre of mass outside/on the support boundary, negative normal load in an admitted case, force/moment residual above tolerance, contact capacity exceeded, wrong steering/yaw sign, mass/inertia mismatch after CAD import, nondeterministic evidence, or a supposedly stable result that relies on silent contact-force clipping.

## Architecture remediation

The v3 fixture will copy v2 and add one passive ground-support component behind the centre of mass. It will have its own geometry, material, structural mount, ground port, bounded normal/longitudinal/lateral limits, and declared contact. The two existing powered/direction-controlled ground units remain unchanged. The new component is a support capability, not an undeclared propulsion source.

The support polygon and all contact lever arms are derived from component/port world positions. Static normal forces must satisfy

```text
sum(N_i) = m g
sum(x_i N_i) = 0
sum(y_i N_i) = 0.
```

For quasi-static planar accelerations at centre-of-mass height `h`, v1 uses

```text
sum(x_i N_i) = -m a_x h
sum(y_i N_i) = -m a_y h.
```

The three unknown normal forces are solved directly; negative force is an observable contact-lift failure, not clipped to zero.

## Experiment design

- Independent variables: support component geometry/pose, contact positions/limits, material density, centre of mass, centre-of-mass height, longitudinal/lateral accelerations, steering command, cornering stiffness, friction coefficients, initial planar speed, and time step.
- Dependent variables: polygon containment/margin, barycentric/static load fractions, per-contact normal loads, vertical/pitch/roll residuals, contact lift, combined tyre utilization, body forces, yaw moment/rate/heading, STEP solid count, mass/centre/inertia residuals, and replay hashes.
- Controls: immutable v2 negative control, SI right-handed frame, unchanged powered paths, exact architecture identities, geometry-derived locations/mass/inertia, no hidden CAD repair, deterministic ordering, and frozen tolerances.
- Metrics: signed support margin, minimum normal load, maximum contact utilization, equilibrium residuals, yaw-response sign/magnitude, CAD residuals, exact replay, and half-step refinement.

Load cases will include static, bounded acceleration, bounded braking, bounded left/right lateral acceleration, and deliberate excessive lateral acceleration causing contact lift. Steering controls will include zero steer and equal-magnitude positive/negative steer.

## Planned files

- `config/vehicle/functional_vehicle_architecture_v3_planar.json`
- `src/formula_ultimate/simulation/planar_support_gate.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/planar_support_gate_v1.json`
- `scripts/experiments/run_planar_support_gate.py`
- `tests/test_planar_support_gate.py`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.md`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.th.md`
- matching bilingual Work 069 plan/result records
- ignored CAD/FreeCAD/experiment evidence under `artifacts/work069/`

Existing generic CAD generation and FreeCAD inspection scripts will be reused rather than copied.

## Validation and success criteria

1. Frozen v2 fails specifically because the centre-of-mass projection is outside its degenerate two-contact support segment.
2. v3 passes the complete functional architecture contract with no overlap or disconnected component.
3. v3 support polygon is nondegenerate and contains the geometry-derived centre-of-mass projection with positive margin.
4. Static loads are positive and close vertical, pitch, and roll equilibrium within relative residual `<= 1e-9`.
5. Frozen bounded acceleration/braking and left/right lateral cases retain positive normal loads and respect contact normal-force limits.
6. Deliberate excessive lateral acceleration reports contact lift and is rejected without clipping.
7. Zero steer has zero symmetric yaw response; positive/negative steering produce opposite bounded yaw signs under the existing combined-force tyre law.
8. STEP generation and independent FreeCAD inspection pass with exact component identity/solid count and mass/centre/inertia relative residuals `<= 1e-6`.
9. Canonical experiment replay and STEP/component hashes reproduce exactly; planar half-step refinement changes selected metrics by `<= 2%`.
10. Focused/full tests, compilation, bilingual evidence, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

The passive support and all material/contact values remain synthetic. A three-point layout is a validation fixture, not a preferred or mandatory discovered topology. Quasi-static load transfer omits suspension transients, heave, pitch/roll inertia, compliance, wheel lift duration, and road roughness. The existing combined-force model remains a Level-0 friction boundary, not a measured tyre.

Work 069 does not implement independent wheel speeds, a differential, torque vectoring, wheel rotational integration, transient suspension, tyre thermal/wear state, full aerodynamic load maps, race trajectory control, lap fitness, physical validation, or safety certification. Work 070 must introduce an explicit differential/carrier energy contract before independent driven-wheel dynamics.
