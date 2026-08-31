# Drive-to-Ground Slip Coupling v1

Thai companion: `DRIVE_GROUND_SLIP_COUPLING_V1.th.md`

## Result and boundary

Work 068 closes the first deterministic causal chain from Work 067 stored energy and shaft torque to Work 066 ground contact, longitudinal force, and vehicle acceleration. Each admitted ground unit is reconciled against its architecture component, contact, radius, geometry-derived axial inertia, port limits, and static normal load. A broken drive connection propagates to drive-subsystem state `failed` and race outcome `DNF`.

The result is a straight-line synthetic slip experiment. It validates coupling identities, limits, energy partition, failure propagation, deterministic replay, and numerical refinement. It is not a measured tyre model or whole-vehicle physical validation.

## Geometry and inertia closure

The reference consumes vehicle mass `272.55249331647553 kg` from the Work 066 geometry. Both ground units use radius `0.14 m` and geometry-derived axial inertia `0.13034241725073026 kg m^2`. Their combined inertia is `0.2606848345014605 kg m^2`; the remaining explicitly declared downstream inertia is `2.2393151654985397 kg m^2`. The sum is exactly the Work 067 output inertia `2.5 kg m^2`, preventing wheel inertia from being counted twice.

Each static normal load is `1336.4134542910074 N`, and the pair closes `m g = 2672.8269085820148 N`. Each reference contact declares maximum longitudinal force `4000 N`, while its synthetic friction capacity is lower: `mu Fz = 1.2 * 1336.4134542910074 = 1603.6961451492088 N`.

## Slip and force law

For common output speed `omega`, vehicle speed `v`, effective radius `r`, regularization speed `v0`, stiffness `C`, and forward drive slip:

```text
v_slip = r omega - v
kappa = v_slip / max(v, v0)
F_capacity = min(mu Fz, F_declared)
F = F_capacity tanh(C kappa / F_capacity), when kappa > 0
F = 0, when kappa <= 0
T_load = sum(F r).
```

The zero-force negative-slip branch prevents undeclared regenerative energy in v1. The request, capacity, applied force, utilization, and unserved torque remain explicit.

At a constant analytical state with `omega = 100 rad/s`, `v = 12 m/s`, two forces of `1000 N`, and both radii `0.14 m`:

```text
T_load = 280 N m
T_load omega = 28,000 W
sum(F v) = 24,000 W
slip heat = 4,000.0000000000036 W
power residual = -3.637978807091713e-12 W.
```

Thus the difference between axle power and body power is observable slip dissipation rather than missing energy.

## Transient reference result

The reference used throttle `0.5`, duration `2 s`, step `0.0005 s`, and `4000` steps.

| Metric | Result | Gate |
| --- | ---: | --- |
| final vehicle speed | `14.3996903855916 m/s` | positive/finite |
| final distance | `16.4550513109228 m` | positive/finite |
| source energy used | `65239.388932965 J` | decreasing onboard store |
| vehicle kinetic energy | `28257.0273591386 J` | derived from mass/speed |
| slip heat | `1791.64460139612 J` | non-negative |
| aerodynamic work | `984.746997658385 J` | non-negative |
| rolling work | `659.722558888986 J` | non-negative |
| maximum total ground force | `2832.59764718983 N` | below combined capacity |
| maximum contact utilization | `0.883146615946464` | `<= 1` |
| maximum slip ratio | `0.111448036394737` | observable |
| maximum torque residual | `0 N m` | passed |
| maximum interface residual | `1.81721304670646e-12 J` | passed |
| maximum global residual | `0.510794088244438 J` | observable |
| maximum global relative residual | `1.02158817648888e-8` | `< 1e-3` |

The result SHA-256 is `b7311a924e74bc412c611f261e11928745dec381f093c13085814b05624a3070`. Exact replay reproduced it. Halving the time step changed selected terminal values by at most `4.969084181339372e-5`, below the frozen `0.02` ceiling.

## Falsification controls

- Zero throttle: force, speed, distance, and contact body work remained zero.
- Zero stored energy with full throttle: the same quantities remained zero; no force from nowhere appeared.
- Friction saturation: arbitrarily high positive slip approached but did not exceed `min(mu Fz, F_declared)`.
- Negative slip: requested drive force was zero; no undeclared regeneration was inferred.
- Drive failure: a deliberately reduced shaft limit caused `shaft_connection_failure` at `0.002 s`, drive subsystem `failed`, outcome `DNF`, and final transmitted output drive torque `0 N m`.
- Invalid controls: changed radius, axial inertia, contact force/normal-load limit, inertia closure, numerical tolerance, and non-finite friction were rejected.

All ten frozen experiment checks, eight focused tests, and the full 404-test repository regression passed.

## Missing evidence and next work

The v1 coupling uses static normal loads, common output speed, a forward-only regularized `tanh` force curve, and fixed-step explicit coupling. It has no differential action, independent wheel speeds, load transfer, suspension motion, lateral slip, steering, tyre thermal/wear state, road surface variation, regeneration, or reverse motion. The force curve and friction coefficient are synthetic, not fitted measurements.

The next work should introduce dynamic normal-load transfer and independent left/right wheel states, then combine longitudinal and lateral slip with steering. That will allow a straight-line powertrain specimen to become a planar vehicle-dynamics experiment without weakening the energy and DNF contracts.
