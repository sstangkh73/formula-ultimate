# Work 019 Problem Report: Lookup Command Path Assumptions

Status: Resolved

Thai companion: `2026-08-28_019-lookup-command-path-assumptions.th.md`

## Problem

An initial read-only repository probe assumed the Work 015 files were named
`tests/test_race_loop.py` and `scripts/validate_race_loop.py`, and used a
PowerShell wildcard directly as an `rg` path. The command exited non-zero with
three path errors.

## Impact

No file was changed and no validation result was masked. The failure affected
only discovery of reference implementation and queue text.

## Fix

Repository search identified the actual paths as `tests/test_race.py` and
`scripts/validate_race.py`. The queue lookup now passes both bilingual filenames
explicitly. Subsequent read commands exited with status `0`.

## Verification

The corrected probe displayed the Work 015 test, validator, race model, and
both Work 019 queue rows. The issue is resolved without product-code changes.
