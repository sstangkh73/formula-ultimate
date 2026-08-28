# Problem Report: Contact Subsystem State Was Not Persistent

Status: Resolved

Thai companion: `2026-08-29_027_contact-state-persistence.th.md`

## Problem

`ContactRuntimeState` omitted suspension velocity, brake temperature, recovered contact-store energy, and latched suspension/brake failures. The Work 025 adapter accepted external subsystem snapshots, so a multi-step orchestrator could accidentally reuse stale state.

## Impact

Thermal accumulation, regeneration capacity, suspension dynamics, and failures could reset between coupled steps while replay metadata still looked valid.

## Fix

Extend `ContactRuntimeState` with backward-compatible fields for the full Work 018 persistent state. Work 025 now verifies external snapshots against shared state and can derive snapshots from shared state. Work 027 merges contact end state back into the next shared candidate.

## Limitation

The fields remain reduced-order Level-0 state, not measured hardware state.
