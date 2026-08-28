# Problem Report: Exact-End Energy Depletion Was Not an Event

Status: Resolved

Thai companion: `2026-08-29_028_exact-end-depletion-event.th.md`

## Problem

Work 027 emitted depletion only when the analytical crossing was strictly before the contact interval end. Exact exhaustion at the end produced zero energy but no event candidate.

## Impact

Work 028 could not retain an exact finish/depletion tie or apply the declared event priority.

## Fix

Treat a depletion crossing at or within `1e-15 s` of the executed interval end as an `energy_depletion` candidate. The race-progress regression proves `finished` wins the exact tie while the tied IDs remain observable.
