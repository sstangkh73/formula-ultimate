# Problem Report: Input Scenario Distance Could Differ from Shared State

Status: Resolved

Thai companion: `2026-08-29_028_input-state-distance-mismatch.th.md`

## Problem

The Work 023 input adapter validated a scenario's race distance against the circuit but did not require it to equal `state.current.race_distance_m`.

## Impact

A whole-race step could select spatial/weather evidence for one station while integrating a vehicle at another station.

## Fix

The input bridge now requires equality within `1e-9 m` and returns invalid with zero writes on mismatch. Existing analytical fixtures were corrected to declare the state distance they actually use.
