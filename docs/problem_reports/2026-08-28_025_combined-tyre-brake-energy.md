# Work 025 Problem Report: Combined-Tyre Brake Energy Overcount

Status: Resolved

Thai companion: `2026-08-28_025_combined-tyre-brake-energy.th.md`

## Problem

The first passing Work 025 implementation evaluated brake/regen energy before
the combined tyre ellipse. When simultaneous lateral demand reduced longitudinal
brake force, recovered energy and mechanical heat still reflected the larger
pre-ellipse torque.

## Impact

Force saturation was observable, but wheel energy removal, storage recovery,
loss, heat, and brake temperature could exceed the torque actually transmitted
to the road.

## Fix

Use a deterministic two-pass brake evaluation: first determine subsystem torque
capacity, project that force with lateral demand through the tyre ellipse, then
rerun suspension/brake/regen and thermal integration using the projected brake
torque. Retain original requested torque minus final applied torque as unserved;
do not redistribute it. Add an energy/force consistency regression.

## Verification

The combined braking/steering regression now proves for every contact that
`wheel_energy_removed = abs(applied_Fx) * effective_radius * omega * duration`.
Original brake demand not transmitted by the tyre remains in unserved torque.
Focused 11/11, repository 207/207, and validator checks pass.
