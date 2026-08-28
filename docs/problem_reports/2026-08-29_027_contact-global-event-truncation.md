# Problem Report: Contact Events Did Not Truncate Peer Contacts

Status: Resolved

Thai companion: `2026-08-29_027_contact-global-event-truncation.th.md`

## Problem

Work 025 evaluated each contact independently for the requested duration. If one suspension or brake failed early, other contacts could still accumulate force, heat, and recovered energy to the original step end.

## Impact

One aggregate contact signal could contain quantities integrated over different physical durations.

## Fix

Evaluate once to locate the earliest positive contact failure, then deterministically rerun every contact with that common shortened duration. `ContactEnergyTransfers` exposes requested and executed duration. A regression fixture verifies all contact end times and energy use the same event time.

## Limitation

Events at the exact start remain observable as pre-existing invalid/failed state and are not advanced.
