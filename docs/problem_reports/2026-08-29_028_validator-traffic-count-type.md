# Problem Report: Validator Used a Floating-Point Traffic Count

Status: Resolved

Thai companion: `2026-08-29_028_validator-traffic-count-type.th.md`

## Problem

The standalone Work 028 validator constructed isolated-traffic evidence with `nearby_vehicle_count = 0.0`, while the typed input contract requires a non-negative integer.

## Impact

The validator stopped before executing the coupled race, so it could not produce independent evidence even though the focused tests passed.

## Fix

Changed the validator fixture to use integer `0`. The production type contract remains strict and no implicit coercion was added.
