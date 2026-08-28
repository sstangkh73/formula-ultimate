# Work 018 Problem Report: Tyre-Limit Fixture Triggered Suspension Failure

Status: Resolved

Thai companion: `2026-08-28_018_tyre-limit-fixture-suspension-failure.th.md`

## Problem

The first Work 018 run passed 12 tests and failed the tyre-limit test because the
result was `failed`, not the expected `ok`:

```text
Ran 13 tests
FAILED (failures=1)
AssertionError: 'ok' != 'failed'
```

The test lowered normal load from `1000 N` to `100 N` to create a
`mu*Fz*R = 30 N*m` tyre torque ceiling, but retained a `1000 N` suspension
preload. The model therefore calculated a large rebound acceleration and
correctly localized a suspension-travel failure inside the one-second interval.

## Root cause

The fixture changed two coupled physical conditions unintentionally: tyre load
and suspension force imbalance. The test intended to isolate tyre saturation,
but its suspension was no longer at equilibrium.

## Fix

The test and validator now use a dedicated tyre-limit fixture with `100 N`
preload and `100 N` normal load.
The suspension then remains in equilibrium while the declared tyre torque limit
remains `30 N*m`. Apply the same correction to the validator.

The production solver must not be changed to suppress the observed suspension
failure.

## Verification

```powershell
python -m unittest tests.test_suspension_braking -v
python scripts/validate_suspension_braking.py
```

Both commands exited with status `0`; `Ran 13 tests`; `OK`. The validator
reported tyre limit `30 N*m`, tyre scale `0.2`, applied torque `30 N*m`, and
unserved torque `120 N*m` without a suspension event. The issue is resolved.
