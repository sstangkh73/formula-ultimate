# Problem Report: Hidden Vertical Projection During Motion Step

Status: Resolved

Thai companion: `2026-08-28_026_motion-vertical-projection.th.md`

## Context

The first Work 026 implementation draft calculated the candidate `z` coordinate by assigning the advanced centreline `z` coordinate.

## Impact

If the start state had a non-zero vertical offset from the local corridor reference, one motion step would erase that offset without a declared vertical force, constraint impulse, or residual. This would be a hidden state correction.

## Root Cause

Centreline advancement and vehicle-state advancement shared the same vertical value even though Work 026 is a planar longitudinal/lateral/yaw model and does not solve vertical dynamics.

## Fix

Preserve the start vehicle's vertical offset and retain constant-velocity vertical kinematics because Work 026 does not solve vertical force. Candidate `z` is now:

`z_candidate = z_start + v_z_start * duration`

`v_z` remains unchanged and a `motion.kinematic-z` residual checks the position update. The centreline reference is still advanced independently for corridor evidence; Work 026 does not project the vehicle onto it.

## Regression Gate

A unit test starts above the reference centreline with declared vertical velocity and verifies the exact constant-velocity `z` update.

## Limitation

Grade-constrained vertical motion, suspension heave, road contact impulses, jumps, and full 3D rigid-body dynamics remain outside Work 026. Grade evidence is retained but is not silently imposed on the candidate state.
