# Sprung-Body, Road, and Tyre Vertical Coupling V1

Thai companion: `SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.th.md`

## Claim boundary

Work 073 is deterministic synthetic Level-0 evidence that the current Work 069 v3 architecture can transmit vertical force through a declared sprung body, suspension elements, unsprung masses, compliant tyres, and a moving road boundary while remaining coupled to Work 071 horizontal tyre forces. It is not parameter-identified, physically validated, or evidence that the vehicle is ready to race.

## Physical model

The materialized architecture supplies component mass and centroidal inertia. Ground-contact components retain their Work 072 effective unsprung masses. Every other component contributes to sprung mass and to roll/pitch inertia through its primitive centroidal inertia and the parallel-axis theorem. The derived values are:

- sprung mass: `245.95200000000003 kg`;
- sprung roll inertia: `4.218672483307425 kg m2`;
- sprung pitch inertia: `46.253188363933454 kg m2`.

Displacements are measured from static equilibrium and positive upward. For contact `i` at `(x_i, y_i)`:

```text
q = [z_s, theta, phi, z_u1, z_u2, z_u3]
z_body_i = z_s - x_i theta + y_i phi
s_i = z_ui - z_body_i
t_i = z_road_i - z_ui
F_s,i = k_s,i s_i + c_s,i s_dot_i
F_t,i = k_t,i t_i + c_t,i t_dot_i
N_actual,i = N_static,i + F_t,i
M q_ddot + C q_dot + K q = f_inertial + f_road.
```

The six-degree-of-freedom linear system is advanced by implicit midpoint. Work 071 reconstructs longitudinal/lateral inertial moments from its current acceleration/load iteration; Work 073 then returns `N_actual` inside that same fixed point. Consequently, the combined-force ellipse uses the solved tyre load, not the quasi-static target.

Powered contacts use `k_t = 180,000 N/m`; the passive contact uses `120,000 N/m`. All tyre vertical damping ratios are `0.15`. These are declared synthetic parameters, not measurements.

## Conservation and failure rules

Vertical energy includes sprung/unsprung kinetic energy and suspension/tyre spring energy. Suspension and tyre damper heat, inertial work, and signed road work remain distinct:

```text
R_vertical = delta(E_vertical) + Q_suspension + Q_tyre
             - W_inertial - W_road.
```

Any initial vertical energy is deducted from the fixed `50,000,000 J` storage budget. A non-positive actual normal load produces an uncommitted `DNF: contact_loss`; suspension travel beyond `0.05 m` produces `DNF: suspension_travel` at the committed boundary step. Neither load nor travel is clipped. Singular, non-finite, non-convergent, or excessive-residual states are invalid.

## Preregistered experiment

- Independent variables: steering sign, road contact/amplitude/timing/shape, tyre stiffness/damping, time step, and initial vertical state.
- Dependent variables: heave/pitch/roll, unsprung motion, suspension/tyre deflection and force, actual normal loads, planar/yaw state, heat/work/energy ledgers, equation residuals, terminal reason, and hashes.
- Controls: unchanged Work 072, exact replay, zero steer, opposite steer, left/right bump mirror, zero tyre damping, half tyre stiffness, road drop, large road ramp, initial-state travel excursion, and half time step.
- Failure criteria: upstream hash drift, target load bypass, contact identity mismatch, unexplained energy, mirror error above `1e-9`, refinement above `2%`, hidden clipping, wrong terminal reason, or any failed test.

The preferred hypothesis was deliberately vulnerable to these controls: normal running should excite finite body modes without losing contact, while each changed physical parameter should cause the expected observable response.

## Results

The `+0.01 rad` steering, `0.3` throttle, flat-road reference completed `500` steps at `dt = 0.001 s`:

- actual normal-load range: `298.98159710209535` to `1763.2457662772727 N`;
- maximum heave: `0.0033467120741574362 m`;
- maximum pitch: `0.019441673288686227 rad`;
- maximum roll: `0.03707142724764741 rad`;
- maximum suspension travel: `0.01138991675295634 m`;
- suspension/tyre damper heat: `1.23258623590469 J` / `0.0770877072013249 J`;
- inertial work: `5.93404634108439 J`;
- maximum generalized-equation residual: `5.115907697472721e-12`;
- maximum vertical-energy residual: `1.9463597400459776e-15 J`;
- maximum combined relative energy residual: `5.043254643678665e-9`.

The `0.003 m` left bump completed and supplied `0.7534111876506473 J` of signed road work. Its right-side/opposite-steer mirror differed by at most `1.33226762955019e-15`. The steering mirror residual was at most `1.11022302462516e-16`. Zero tyre damping produced exactly `0 J` tyre heat; half tyre stiffness changed maximum heave to `0.00510845998305605 m`. Maximum half-step relative difference was `0.0037196002671815395`, below `0.02`.

The road-drop control exposed `-334.965753656288 N` and stopped uncommitted at attempted step `23`. The large ramp first exposed contact loss at step `192` with `-2.73545081705686 N`; it did not reach travel first, contradicting the narrower expectation that a large upward ramp would necessarily exhaust suspension travel. The independent initial-state control did expose `0.0506249708792031 m` travel and stopped at step `2`. This distinction is retained rather than relabelled.

Work 072 retained result SHA-256 `2e70e32766915af2237b92cee20aa9ee415f65bfc5ab14e56fd02d1bf41628ad`. Work 073 reference result SHA-256 is `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973`. The primary/replay evidence files are byte-identical with file SHA-256 `EF22581D6DE1172BFA7181A31E5EFD77B9FFF0FB4959C5521527D1C73CF5BA07`; canonical evidence SHA-256 is `84c0911f35ef12036fd5dde2dc05183bf727a1bf3f25927c6a2febafd15ea2e3`.

## Interpretation and missing evidence

Supporting evidence shows a deterministic causal path from road displacement and horizontal acceleration through vertical geometry/mass/spring/damper states to actual tyre load and horizontal force capacity. The large-ramp result contradicts any assumption that travel must be the first limit. Alternative explanations for numerical agreement include the model's linearity and shared implementation between dynamics and ledger checks; the analytical/mirror/refinement controls reduce but do not eliminate that risk.

Missing evidence includes CAD-derived linkage geometry and motion ratios, bump stops, nonlinear tyre contact, measured road spectra, parameter identification, chassis flexibility, anti-dive/squat, aerodynamic load, sub-step event localization, hardware tests, and external solver correlation. Confidence is high that the implemented equations satisfy their declared software contract, and low that the current parameter values predict a real vehicle.
