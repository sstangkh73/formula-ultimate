# Problem Report: Baseline Contact State Used the Wrong Positional Field

Status: Resolved

Thai companion: `2026-08-29_029_contact-runtime-positional-order.th.md`

## Problem

The first Work 029 campaign constructed `ContactRuntimeState` positionally and placed the intended `300 K` brake temperature into `suspension_travel_m`. The resulting initial travel was `300 m`.

## Impact

Every circuit/seed run failed closed in `contact_limit_solver` before the first commit with `suspension_travel_m is outside declared travel limits`.

## Fix

Construct the baseline contact state with explicit keyword arguments for travel, angular speed, suspension velocity, and brake temperature. No tolerance or travel limit was relaxed.
