# Work 024 Problem Report: Missing Wind Coordinate Frame

Status: Resolved

Thai companion: `2026-08-28_024_wind-coordinate-frame.th.md`

## Problem

Work 024 integration review found that `WeatherStepEvidence.wind_velocity_mps`
did not declare a coordinate frame. The same tuple could be interpreted as
local ENU velocity or vehicle-body velocity, changing relative airspeed and yaw.

## Impact

Work 023 typing and missing-evidence gates remained valid, but observed wind was
semantically ambiguous and unsafe to consume in aerodynamic physics.

## Fix

Add `wind_coordinate_frame`; require `local_enu` for observed evidence and
require it to be absent when weather is missing. Work 024 then rotates relative
ENU air velocity into body axes using the shared-state yaw. Add rejection and
rotation regression tests and update bilingual Work 023 model documentation.

## Verification

Observed wind without `local_enu` is rejected. The `pi/2` yaw regression rotates
global `(0,30,0) m/s` velocity to body-forward `30 m/s` and evaluates the exact
map node. Work 023 and 024 focused tests and all 196 repository tests pass.
