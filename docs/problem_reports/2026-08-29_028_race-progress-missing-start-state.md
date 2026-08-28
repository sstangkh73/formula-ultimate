# Problem Report: Race Progress Stage Missing Start State

Status: Resolved

Thai companion: `2026-08-29_028_race-progress-missing-start-state.th.md`

## Problem

Architecture v3 did not route `state.current` to `race_progress_solver`.

## Impact

The adapter could not calculate finish/timeout crossing fractions or verify that motion, energy, and health candidates descended from the same start state.

## Fix

Preserve v3 and add architecture v4. Version 4 routes `state.current` to race progress and pins `work028-race-progress-v1`.
