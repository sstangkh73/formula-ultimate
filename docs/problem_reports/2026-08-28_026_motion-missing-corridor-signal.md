# Problem Report: Motion Module Missing Corridor Signal

Status: Resolved

Thai companion: `2026-08-28_026_motion-missing-corridor-signal.th.md`

## Context

Work 026 requires race-distance integration along the circuit tangent and an observable corridor-departure gate.

## Reproduction

Inspect `config/simulation/coupled_level0_architecture_v1.json`. The `input_bridge` produces `circuit.segment_inputs`, but `vehicle_motion_solver` consumes only:

- `aero.force_moment`
- `contact.force_moment`
- `state.current`

The signal reaches `race_progress_solver` later, after the motion candidate has already been calculated.

## Impact

The motion module cannot derive corridor-tangent progress or reject an off-corridor candidate from its declared reads. Any implementation that did so would either perform an undeclared read or use hidden adapter configuration without the step's typed spatial evidence.

## Root Cause

The Work 021 architecture reserved motion outputs before the Work 026 corridor-dependent integration contract was implemented. The dependency list omitted the spatial input needed by that later contract.

## Fix

- Preserve `coupled_level0_architecture_v1.json` as historical evidence.
- Add `coupled_level0_architecture_v2.json`.
- Route `circuit.segment_inputs` to `vehicle_motion_solver` in v2.
- Pin the motion module to `work026-coupled-motion-v1` in v2.
- Add tests that compile v2 deterministically and assert the exact motion input contract.

## Regression Gate

The Work 026 test suite must fail if `circuit.segment_inputs` is removed from the v2 motion module. The motion adapter must reject missing/unsupported spatial evidence with zero output signals.

## Limitation

This fixes signal routing only. Local analytical corridor samples remain Level-0 evidence and do not replace a surveyed three-dimensional circuit corridor.
