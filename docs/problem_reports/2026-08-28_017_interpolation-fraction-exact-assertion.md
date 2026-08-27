# Work 017 Problem Report: Exact Assertion on Interpolation Fraction

Status: Resolved

Thai companion: `2026-08-28_017_interpolation-fraction-exact-assertion.th.md`

## Problem

The first Work 017 test run passed 10 tests and failed the interior interpolation
test because it compared a computed binary floating-point fraction to decimal
`0.5` with exact equality:

```text
AssertionError: 0.5 != 0.4999999999999999
Ran 11 tests
FAILED (failures=1)
```

The ride-height interval is `[0.04, 0.08]` and the query is `0.06`; the
mathematical fraction is exactly one half. Decimal inputs are not exactly
representable in binary floating point, so the calculated fraction differs by
approximately `1.11e-16`.

## Impact

The coefficient interpolation assertions passed. This is a test-assertion
defect, not evidence of an incorrect bracket, coefficient, force, moment, or
cooling result.

## Fix

The test now uses `assertAlmostEqual` for all three interpolation fractions while retaining
exact equality checks for exact grid-node identity and deterministic replay.

## Verification

```powershell
python -m unittest tests.test_aerodynamics -v
python scripts/validate_aerodynamics.py
```

Both commands exited with status `0`; `Ran 11 tests`; `OK`; the validator
reported `replay_equal: true`, drag ratio `4.0`, mass-flow ratio `2.0`, and the
raw ride-height fraction `0.4999999999999999`. The issue is resolved.
