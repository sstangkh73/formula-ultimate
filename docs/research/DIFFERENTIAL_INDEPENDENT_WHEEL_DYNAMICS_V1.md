# Differential and Independent Driven-Wheel Dynamics v1

Thai companion: `DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.th.md`

## Result and boundary

Work 070 replaces the Work 068 common-wheel-speed approximation with a deterministic ideal open-differential specimen. The two powered contacts of the Work 069 stable v3 architecture now have independent angular speeds while retaining the same geometry, materials, support loads, powertrain, contact limits, and energy source.

This is a Level-0 lumped dynamics contract inside the existing `torque_transmission` component. It validates kinematics, inertia accounting, energy transfer, loss, limits, failure propagation, and replay. It does not represent resolved gear geometry, measured differential hardware, transient suspension, or whole-vehicle physical validation.

## Coordinates and inertia accounting

For carrier speed `omega_c` and differential-mode speed `delta_omega`:

```text
omega_L = omega_c - delta_omega
omega_R = omega_c + delta_omega
omega_c = (omega_L + omega_R) / 2.
```

Each driven solid has geometry-derived axial inertia `0.13034241725073026 kg m^2`. The frozen Work 067 output inertia closes as:

```text
J_other + J_L + J_R
= 2.2393151654985397 + 0.13034241725073026 + 0.13034241725073026
= 2.5 kg m^2.
```

The common wheel inertia is therefore already in `J_output`. Only the independent-mode energy is added downstream:

```text
J_delta = J_L + J_R = 0.2606848345014605 kg m^2
E_delta = 0.5 J_delta delta_omega^2.
```

This prevents wheel inertia from being counted twice.

## Torque, efficiency, and modal energy

Each powered branch uses the architecture connection efficiency `eta_i = 0.98`. A wheel load torque `tau_i = F_i r_i` is reflected to the carrier as:

```text
q_i = tau_i / eta_i.
```

For modal damping `c_delta = 0.02 N m s/rad`, the independent mode obeys:

```text
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega.
```

An implicit-midpoint damping update makes the per-step partition explicit:

```text
W_carrier
= W_reflected_left + W_reflected_right
  + Delta(E_delta) + Q_differential.
```

Each reflected branch work is then divided into wheel input work and connection heat; wheel input work is divided into body work and longitudinal slip heat. Negative loss beyond tolerance is rejected.

## Reference and split-grip results

All admitted runs use throttle `0.5`, duration `2 s`, step `0.0005 s`, and `4000` steps.

| Metric | Symmetric `mu=(1.2,1.2)` | Split `mu=(1.0,1.2)` | Mirrored `mu=(1.2,1.0)` |
| --- | ---: | ---: | ---: |
| final vehicle speed | `11.68448249437216 m/s` | `9.96057727044386 m/s` | `9.96057727044386 m/s` |
| final distance | `11.742989097609598 m` | `10.255133327646465 m` | `10.255133327646465 m` |
| carrier speed | `103.15502526901471 rad/s` | `107.65471518711871 rad/s` | `107.65471518711871 rad/s` |
| left speed | `103.15502526901471 rad/s` | `141.05601957062677 rad/s` | `74.25341080361065 rad/s` |
| right speed | `103.15502526901471 rad/s` | `74.25341080361065 rad/s` | `141.05601957062677 rad/s` |
| final `delta_omega` | `0 rad/s` | `-33.401304383508055 rad/s` | `33.401304383508055 rad/s` |
| maximum modal energy | `0 J` | `324.1158550756573 J` | `324.1158550756573 J` |
| slip heat | `13922.812590781254 J` | `14984.833885342356 J` | `14984.833885342356 J` |
| branch-connection heat | `687.7218665085455 J` | `599.8816054535888 J` | `599.8816054535888 J` |
| differential heat | `0 J` | `60.115830964968396 J` | `60.115830964968396 J` |

Symmetric grip retained exactly equal wheel speeds and zero modal energy. Under split grip, the lower-grip left branch spun faster while the higher-load right branch slowed. Mirroring friction exchanged the two branch states exactly and left aggregate speed, distance, energy, and loss unchanged.

## Residuals, controls, and replay

For the split-grip run:

- maximum carrier-average residual: `1.4210854715202004e-14 rad/s`;
- maximum modal-equation residual: `5.9534599472499394e-12 N m`;
- maximum torque residual: `0 N m`;
- maximum interface energy residual: `1.9071116214020023e-12 J`;
- maximum global energy residual: `0.5030174478888512 J`;
- maximum global relative residual: `1.0060348957777023e-8`;
- maximum contact utilization: `1.0`.

The global residual is observable and well below the frozen `1e-3` ceiling. Halving the time step changed selected terminal metrics by at most `0.00023334677638767642`, below the `0.02` refinement limit.

Zero onboard energy produced zero torque, force, speed, distance, slip heat, connection heat, and modal energy. A deliberate operational branch-speed limit of `25 rad/s` produced `differential_branch_overspeed` at step `532`, vehicle distance `0.2040023153031444 m`, and outcome `DNF`; a terminal state cannot execute another step.

The reference result SHA-256 is `c23eea2641b6863da2d63eb8a2ca3b7ae5ad94a53822c70bffd8fa1bffb1b92a`. The split result SHA-256 is `eee844e411d194c5d2205e5467ce42d3877867b013863fd4cd0772bda2be4879`. Exact replay reproduced both and the canonical experiment evidence SHA-256 `bc23719a3fbd0d343898488f263bf805d8aae8152acc6de4ef23ff2d410cd79a`.

## Geometry evidence and confidence

The materialized architecture SHA-256 remains `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`. Its JSON bytes are identical to the post-commit Work 069 geometry, so the previously verified `11`-solid STEP/FreeCAD evidence remains applicable; Work 070 introduced no hidden geometry change.

Nine focused tests and all `421` repository tests passed. Confidence is high for the declared lumped equations, deterministic branch symmetry, identity/limit reconciliation, energy bookkeeping, failure state, and numerical replay. Confidence remains low for real differential durability or traction prediction because coefficients and internal mechanisms are synthetic.

## Missing evidence and next work

The specimen has an ideal `50:50` open torque split, lumped reflected branch inertia, fixed static normal loads, and no reverse rotation. It omits differential gear tooth contact, shaft torsion per branch, bearing friction maps, backlash, housing deformation, lubricant thermal state, limited-slip or torque-vectoring logic, wheel hop, tyre relaxation, and measured friction/slip curves.

The next work should couple these independent wheel states to Work 069 planar yaw/contact dynamics with transient geometry-derived normal-load transfer. After that, internal transmission geometry and structural/thermal verification must be introduced before the candidate can be called a detailed whole vehicle.
