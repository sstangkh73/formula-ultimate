# Problem Report: Hidden Thermal Ambient Default

Status: Resolved

Thai companion: `2026-08-29_027_hidden-ambient-default.th.md`

## Problem

The first central-health draft passed a hard-coded `300 K` ambient temperature into every thermal component because the health-stage architecture does not consume environment inputs.

## Impact

Thermal results could appear evidence-backed while depending on an undeclared neutral condition.

## Fix

Make `ambient_temperature_k` a required positive finite field of `CentralHealthConfiguration` and record it in validation fixtures. No neutral thermal ambient is inserted by the solver.

## Limitation

Work 028 must explicitly construct this configuration from the declared step environment; real weather calibration remains absent.
