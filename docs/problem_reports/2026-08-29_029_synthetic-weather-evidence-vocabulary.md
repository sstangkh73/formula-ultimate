# Problem Report: Weather Contract Could Not Represent Synthetic Controls

Status: Resolved

Thai companion: `2026-08-29_029_synthetic-weather-evidence-vocabulary.th.md`

## Problem

`WeatherStepEvidence.status` accepted only `observed` or `missing`. A controlled analytical baseline therefore had to either mislabel synthetic weather as observed or fail before simulation.

## Impact

Mislabeling would make the Work 029 proxy campaign appear to contain measured local weather evidence and could incorrectly support real-circuit admission.

## Fix

Added the explicit `synthetic_control` status and allowed the aerodynamic adapter to consume it. It requires the same complete, finite SI fields as an observed record but retains a distinct identity and fingerprint. Documentation and tests prohibit interpreting it as observation or real-circuit evidence.
