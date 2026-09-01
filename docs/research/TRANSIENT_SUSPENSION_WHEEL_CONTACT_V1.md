# Transient Suspension and Wheel-Contact Coupling V1

Thai companion: `TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.th.md`

## Claim boundary

Work 072 adds a deterministic transient vertical state to every Work 071 contact and feeds the resulting actual normal load back into the tyre-force calculation. It tests a narrow software-level claim: geometry-identified wheel/support masses, declared springs and dampers, tyre capacity, planar motion, yaw, differential motion, and energy ledgers can participate in one converged Level-0 transaction.

It is not physical validation, a complete suspension, or race-readiness evidence. Spring and damper values are synthetic experiment inputs. The materialized architecture remains unchanged with SHA-256 `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`.

## Model

Each contact uses its geometry-derived component mass as effective unsprung mass: `13.30024665823775 kg` for each powered front unit and `4.342937684322531 kg` for the passive rear support. Powered contacts use `k = 35,000 N/m` and damping ratio `0.35`; the passive contact uses `k = 50,000 N/m` and damping ratio `0.4`. All contacts declare `0.05 m` compression and rebound travel.

Displacement `z` is measured from the static preload equilibrium and is positive in compression. The Work 071 quasi-static load becomes `N_target`, while the spring-damper oscillator determines tyre load:

```text
delta_N = N_target - N_0
m z_ddot = delta_N - k z - c z_dot
N_actual = N_0 + k z_mid + c z_dot_mid.
```

Implicit-midpoint integration is used. `N_actual`, not `N_target`, is passed into the Work 071 combined tyre-force ellipse inside the same acceleration/load fixed point. Actual load `<= 0 N` produces `contact_loss`. Travel outside the declared envelope produces `suspension_travel`. Neither value is clipped.

Vertical energy is audited separately:

```text
E = 0.5 m z_dot^2 + 0.5 k z^2
W_boundary = delta_N (z_new - z_old)
Q_damper = c z_dot_mid^2 dt
R = delta(E) - W_boundary + Q_damper.
```

`W_boundary` explicitly represents exchange with the omitted sprung-body vertical modes. Initial perturbation energy is deducted from the common `50,000,000 J` storage budget.

## Experiment design

- Independent variables: steering sign, time step, stiffness, damping, and controlled initial travel/velocity.
- Dependent variables: target/actual normal load, travel, velocity, acceleration, spring/damper force, energy/work/heat, tyre force/utilization, trajectory, yaw, differential state, terminal state, and identity hash.
- Controls: rigid Work 071, zero steer, opposite steer, zero damping, half stiffness, contact-loss perturbation, travel-exhaustion perturbation, exact replay, and half-step refinement.
- Preferred hypothesis: actual load differs from target and changes horizontal response; symmetric/mirror invariants hold; damping only dissipates; deliberately infeasible states fail visibly.
- Falsifiers: tyre uses target instead of actual load, hidden load/travel clipping, incorrect geometry identity, nonzero undamped heat, unexplained energy, mirror/replay/refinement failure, or post-failure force transmission.

## Results

The reference completed 500 steps with steering `+0.01 rad`, throttle `0.3`, duration `0.5 s`, and `dt = 0.001 s`. Final planar position was `(5.369677667803904, 0.13391224133502547) m`; final yaw rate was `0.3637589747733689 rad/s`.

The reference actual normal-load range was `282.92044294869817` to `1597.6137536723597 N`. Maximum target-to-actual difference was `96.89914047704144 N`, demonstrating a non-rigid transient response. Maximum travel was `0.011753827694854656 m`; maximum vertical speed was `0.19365997408307992 m/s`. Final contact states were:

- left: `z = -0.011753827694854656 m`, `z_dot = -0.016030373931809734 m/s`
- rear: `z = 0.0026632563500025683 m`, `z_dot = -0.010840790285720183 m/s`
- right: `z = 0.007851425941973965 m`, `z_dot = 0.031545417354367576 m/s`

Accumulated explicit vertical boundary work was `4.606168739325264 J`; damper heat was `0.9238099457339569 J`. Maximum force residual was `3.979039320256561e-13 N`, maximum suspension-energy residual was `8.296586074402201e-16 J`, and maximum total global relative residual was `5.010984838008881e-9`.

Zero steer retained exact left/right suspension symmetry and zero lateral/yaw state. Opposite steering exchanged the left/right travel and velocity and mirrored planar/yaw states with zero recorded mismatch. The undamped control produced exactly `0 J` damper heat. Halving stiffness increased maximum travel from `0.011753827694854656 m` to `0.02332339540361481 m`, contradicting an explanation in which the vertical states were disconnected telemetry.

The contact-loss control started the left contact at `-0.03 m`. Its first attempted transaction preserved an actual load of `-329.1330469175954 N`, did not commit the failed step, and returned `DNF: contact_loss`. The travel control started the right contact at `0.049 m` and `1.0 m/s`; it committed two deterministic steps, retained the over-travel value `0.05068991458357319 m`, and returned `DNF: suspension_travel`. Their initial suspension energies, `15.75 J` and `48.66762332911888 J`, were deducted from storage, preserving total initial energy at exactly `50,000,000 J`.

The maximum half-step relative difference was `0.008650825751444935` for accumulated damper heat, below the frozen `0.02` gate. Primary and replay evidence files were byte-identical with file SHA-256 `E48CA5034D8361C5E45AAF2D88BA5FC1349015AAD4144345CB5CBFD2AE66B719`. The canonical evidence payload identifies itself as `25b269082eb921efc54c334c6dc3d9623bcb7d6fa91beb9d2ea9b4083270b97b`.

The untransformed Work 071 control retained result SHA-256 `f8f3d888b23a9e21b7bb9ad8b7153ecd5bd4752c7937ebf8cc42a952b64c9cdd`, showing that the extension hook did not alter the prior model.

## Interpretation, contradicting evidence, and limitations

The evidence supports the software claim that transient suspension states causally alter tyre normal load and therefore horizontal force and motion. It also supports the force and energy implementation of the declared oscillator and falsifies the notion that failed travel/contact is silently repaired.

It does not show that the coefficients or motion predict a real vehicle. The favourable residuals may only demonstrate internal equation consistency. Effective mass is the complete geometry-derived ground-component mass, not a measured unsprung modal mass. Boundary work comes from omitted heave/pitch/roll modes rather than a resolved sprung body. There is no tyre vertical stiffness, road displacement, linkage motion ratio, roll centre, anti-dive/squat, bump stop, hysteresis, aero load, measured data, or sub-step event localization. Confidence is high in deterministic coupling and low in real-world predictive accuracy.

Before a strong whole-vehicle dynamics claim, the next fidelity layer should close sprung-body heave/pitch/roll and road/tyre vertical compliance, then connect the resulting vehicle to a closed-loop path and circuit gate.
