# Problem Report: Missing Drive-Energy Transfer

Status: Resolved

Thai companion: `2026-08-29_027_missing-drive-energy-transfer.th.md`

## Problem

Work 025 emitted braking and recovery energy but no mechanical wheel energy for positive drive force. Work 027 therefore could not derive propulsion source demand without inventing energy from force alone.

## Impact

A driven vehicle could accelerate while central onboard energy remained unchanged.

## Fix

Add per-contact `drive_wheel_energy_j` and its aggregate to `ContactEnergyTransfers`. It is calculated from applied positive local longitudinal force, effective radius, wheel angular speed, and the contact's executed duration. Tests cover zero-drive, positive-drive, saturation, and replay.

## Limitation

This is a no-slip wheel-work estimate. Powertrain efficiency and auxiliary demand belong to Work 027 configuration.
