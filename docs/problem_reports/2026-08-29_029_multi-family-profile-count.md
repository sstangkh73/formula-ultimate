# Problem Report: Completed Profile Count Was Actually a Family-Profile Count

Status: Resolved

Thai companion: `2026-08-29_029_multi-family-profile-count.th.md`

## Problem

The first campaign aggregate counted completed `(family_id, circuit_id)` pairs but exposed the value as `completed_profile_count`. This happened to equal ten for the single Work 029 family but would over-count if another reference family were added.

## Impact

A future multi-family campaign could claim more completed profiles than exist in the catalog.

## Fix

Count a circuit profile as completed only when every declared family/seed run for that circuit finished, and set `total_profile_count` to the catalog profile count. Per-family run evidence remains unchanged.
