# Problem Report: Health Stage Could Not Merge Energy and Motion

Status: Resolved

Thai companion: `2026-08-29_027_health-stage-signal-gap.th.md`

## Problem

Architecture v2 did not route `energy.residuals` or `state.motion_candidate` to `health_event_solver`.

## Impact

The health stage could not assign propulsion/recovery losses as heat, inspect depletion evidence, or truncate motion to the same earliest event time.

## Fix

Preserve v2 and add `coupled_level0_architecture_v3.json`. Version 3 routes both signals to health and pins the energy and health adapters to Work 027 model versions.

## Limitation

The versioned dependency fix does not itself prove physical fidelity.
