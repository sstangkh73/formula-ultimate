# Integrated Level-0 Closed-Loop Lap Gate V1

Thai companion: `INTEGRATED_LEVEL0_LAP_GATE_V1.th.md`

## Claim boundary

Work 076 combines the Work 074 controller, Work 075 geometry-derived linkage transform, Work 073 vertical road/tyre/body dynamics, and the existing drivetrain/planar plant. It demonstrates one deterministic lap of an analytical `50 m`-radius circle under synthetic Level-0 assumptions. It is not a real-circuit lap, optimized lap time, physical validation, safety evidence, or proof of a complete vehicle.

## Admission logic

A lap is never awarded from scalar distance alone. Each step projects the physical `(x,y)` state to the declared corridor, unwraps centreline progress across the closed-loop seam, and verifies:

```text
progress_delta <= planar_spatial_distance + 0.02 m
abs(cross_track) <= applicable_half_width - 0.65 m
N_actual,i > 0
suspension travel within transformed linkage limits
combined energy residual <= 0.001.
```

Finish is localized between the two physical states that bracket exactly one corridor length. The interpolated finish pose must return within `0.15 m` of the initial vehicle position and within `0.02 rad` of its initial orientation. This comparison uses the initial vehicle pose, not necessarily the centreline tangent, because steady cornering can require a nonzero body slip/heading offset.

## Reference result

The selected linkage ratios are `0.8 / 1.0 / 0.8`. The controller begins with a `0.06 rad` heading offset, uses `K_heading = 0.6`, `K_cross = 0.15 rad/m`, maximum steer `0.03 rad`, throttle `0.3`, and `dt = 0.005 s`.

- exact credited progress: `314.1592653589793 m`;
- localized lap time: `22.14108931044568 s` after `4429` executed steps;
- finish position residual: `0.047685317265362355 m`;
- finish heading residual: `3.56130463712072e-05 rad`;
- maximum absolute cross-track error: `0.0714069338543296 m`;
- steering saturation count: `0`;
- minimum actual normal load: `156.44738786029893 N`;
- maximum suspension travel: `0.024331844801589377 m`;
- maximum combined relative energy residual: `7.449174538254737e-08`;
- maximum progress-versus-spatial residual: `0.0007138905266217827 m`;
- opposite-direction mirror residual: `5.230538224765269e-14`;
- short-segment half-step difference: `8.335276595736185e-05`.

Exact replay passed. Work 074 result SHA-256 remained `a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374`; Work 075 application SHA-256 remained `51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487`.

Open-loop steering left the corridor after `346` steps. The narrow-corridor control departed after `23` steps. A road-drop input produced `contact_loss` after `5` attempted steps, before lap completion. The timeout control stopped after `20` steps. These outcomes are retained as causal DNF evidence rather than converted to numerical failure or clipped into a finish.

Reference result SHA-256 is `719b39293ecb818560acbd88cf1262da8b3407ffb3e5f150a0130860cf9e0dc3`; canonical evidence SHA-256 is `bdbdf31f63dc4da79c12e159d05e1a0e3c870a7994c846b53e73aba9ac2a9df2`; byte-identical primary/replay file SHA-256 is `F6E8C83A72510837C32B07F925132BAA594C531D1D9B4DBC4C5087C4AD6F80CB`.

## Interpretation and next falsification

The result supports software-level causal integration: steering changes physical contact forces; linkage geometry changes vertical stiffness/travel; actual loads constrain tyre force; spatial motion determines progress; and declared failures prevent a finish. Mirror, replay, failure injection, and refinement controls reduce common sign/state-accounting explanations.

It does not establish predictive accuracy. The course is an analytical circle, road is synthetic, geometry points are not extracted from CAD joints, and the model omits speed/brake control, aerodynamics, tyre relaxation/nonlinear contact, thermal race-duration validation, chassis flex, structural load/failure coupling, barriers, weather, traffic, and measured parameters. The next fidelity gate should use CAD-derived linkage topology and a sourced 3D corridor before any real-lap claim.
