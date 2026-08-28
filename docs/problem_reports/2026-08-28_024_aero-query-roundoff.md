# Work 024 Problem Report: Aerodynamic Query Roundoff at Exact Node

Status: Resolved

Thai companion: `2026-08-28_024_aero-query-roundoff.th.md`

## Problem

The ENU-to-body regression at vehicle yaw `pi/2` should produce exactly zero
aerodynamic yaw, but floating-point rotation produced approximately `1e-16 rad`.
A one-node yaw map containing `0.0 rad` correctly rejected that raw value as
outside its declared envelope.

## Impact

The map did not clamp incorrectly; the coupling layer failed to distinguish
coordinate-transform roundoff from a meaningful out-of-envelope query. Exact
physical node cases could therefore fail depending on trigonometric roundoff.

## Fix

Snap a derived query to a declared map node only within relative/absolute
`1e-12` numerical tolerance. Retain raw and queried airspeed/yaw plus the exact
snapped axis names in `AerodynamicQueryEvidence`. Values outside that tolerance
remain invalid and are never clamped.

## Verification

The regression retains nonzero raw yaw, records `yaw_angle` in the snapped-axis
tuple, queries exactly `0.0 rad`, and succeeds. A `40 m/s` query outside the
`30 m/s` node tolerance remains invalid with zero writes. Focused 10/10 and all
196 repository tests pass.
