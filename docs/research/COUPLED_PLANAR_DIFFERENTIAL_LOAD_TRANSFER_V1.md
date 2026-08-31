# Coupled Planar Differential and Load Transfer V1

Thai companion: `COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.th.md`

## Claim boundary

Work 071 is a deterministic synthetic Level-0 coupling experiment. It tests whether the Work 069 three-contact geometry and the Work 070 independent-wheel differential can exchange longitudinal force, lateral force, yaw moment, wheel speed, normal load, and energy without violating their declared interfaces. It is not physical validation, a resolved suspension model, or evidence that the candidate is race ready.

## Model and energy initialization

The materialized Work 069 v3 architecture remains unchanged (`cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`). Two front contacts are powered and steered; the rear support is passive. Geometry-derived mass, centre of mass, yaw inertia, contact positions, wheel radii, component limits, and actuator steering limit are reconciled before execution.

For contact `i`, body velocity is transformed into its steered local frame. Longitudinal wheel slip and lateral slip angle request tyre forces, then a friction ellipse projects both together onto the available normal-load-dependent capacity. A fixed-point solve updates quasi-static normal loads from the same step's longitudinal and lateral acceleration:

```text
sum(N_i)       = m g
sum(x_i N_i)   = -m a_x h
sum(y_i N_i)   = -m a_y h
omega_L        = omega_c - delta_omega
omega_R        = omega_c + delta_omega
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega
```

Negative normal load is not clipped: it produces terminal `contact_lift` and `DNF`. The rear contact can transmit lateral force but is forbidden to supply propulsion torque.

The initial vehicle speed is `10 m/s`. Wheel, carrier, and converter speeds are kinematically matched. Body and rotating kinetic energy are deducted from the declared `50,000,000 J` storage budget, so total accounted initial energy is exactly `50,000,000 J`; the remaining initial powertrain-accounted energy is `49,986,155.22844996 J`.

## Experiment design

- Independent variables: steering sign and magnitude, left/right friction, throttle, step size, differential state, and acceleration-dependent load transfer.
- Dependent variables: trajectory, body velocity, yaw, branch speeds, differential mode, three contact loads/forces/utilization, saturation, heat, work, balance residuals, energy residuals, terminal state, and replay identity.
- Controls: zero steer, positive/negative steer mirror, split-grip/spatial mirror, excessive steer, exact replay, and half-step refinement.
- Preferred hypothesis: the admitted command remains coupled and conservative; symmetric and mirror controls preserve the expected invariants; an infeasible command fails observably.
- Falsifiers: hidden load clipping, rear propulsion, wrong yaw sign, non-mirrored controls, carrier-average error, contact utilization above tolerance, missing heat/work, unconverged states, excessive numerical residual, or replay/refinement failure.

The reference uses steering `+0.01 rad`, throttle `0.3`, duration `0.5 s`, and time step `0.001 s`. The deliberate failure control uses steering `+0.04 rad`. Split grip uses left/right longitudinal friction `1.0/1.2`.

## Results

The reference completed 500 steps. It ended at `(x, y) = (5.3705046591, 0.1338516706) m`, heading `0.0977737591 rad`, yaw rate `0.3638034160 rad/s`, and body velocities `(u, v) = (11.4022671884, -0.3456498170) m/s`. Independent branch speeds were `95.1693758072 rad/s` left and `83.5724925848 rad/s` right. Minimum normal load was `282.9427858151 N`; maximum combined utilization was `1.0000000000000002`; 302 steps reported saturation instead of hiding unserved demand.

Zero steer retained exactly zero lateral position, heading, lateral velocity, yaw rate, and differential speed. Opposite steer mirrored every selected signed state with zero recorded absolute mismatch. Split grip produced branch speeds `98.9391511463/82.1868161465 rad/s`; swapping grip and steering sign exchanged the branch speeds and mirrored lateral/yaw states with zero recorded mismatch.

The `+0.04 rad` falsification control did not pass as a feasible manoeuvre. At attempted step 443, the solved minimum normal load became `-0.1415633491 N`. The run terminated at `0.442 s` as `DNF: contact_lift`, preserving the negative value as evidence.

The reference maximum residuals were:

- load balance: `4.547473508864641e-13`
- carrier average: `0 rad/s`
- modal equation: `3.9168668308775523e-13 N m`
- torque: `0 N m`
- contact energy: `4.5313752750075764e-13 J`
- differential interface energy: `4.539453665394766e-13 J`
- body energy: `1.4557244298885053e-11 J`
- global energy: `0.25046080350875854 J`, relative `5.009216070175171e-9`

The largest half-step relative difference was `0.002683761648435663` for differential speed, below the frozen `0.02` gate. Independent executions produced byte-identical evidence files with file SHA-256 `3D9BF89250E57EC818B785797F3854F4A729BDBAEEBEB8313DD31EE5A2726359`. The canonical evidence payload identifies itself as `935eaec117ab5835e7af8b47cf50f63ec79cfa30e0d57cccad79b5ba1629a6ba`.

## Interpretation and limitations

The evidence supports the narrow claim that forces and energy can propagate through the declared geometry, tyres, differential, powertrain, and planar rigid body in one deterministic Level-0 transaction. It contradicts a rigid equal-wheel-speed assumption and demonstrates an explicit physical feasibility boundary through contact lift.

Alternative explanations remain: the favourable residuals can arise from internally consistent equations without representing a real tyre or suspension. Coefficients are synthetic, normal-load transfer is quasi-static, and the tyre has no relaxation, temperature, wear, camber, aligning moment, or measured data. There is no spring/damper travel, roll-centre geometry, unsprung mass, wheel hop, aero map, road roughness, path controller, track boundary, lap timing, or physical correlation. Confidence is high in deterministic software coupling and low in real-world predictive accuracy.

The next claim should require transient wheel/suspension states and then closed-loop path/circuit operation while preserving the same energy, contact, failure, and replay gates.
