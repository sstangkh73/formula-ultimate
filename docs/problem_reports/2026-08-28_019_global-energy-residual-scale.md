# Work 019 Problem Report: Global Energy Residual Scale

Status: Resolved

Thai companion: `2026-08-28_019_global-energy-residual-scale.th.md`

## Problem

The first Work 019 test run passed every behavioral case but failed nine of ten
real-circuit subtests because the test treated a terminal subtraction involving
approximately `1e10 J` as zero to seven decimal places. Observed residuals were
between `1.9073486328125e-06 J` and `1.1444091796875e-05 J` in magnitude:

```text
Ran 9 tests
FAILED (failures=9)
```

The races finished at the exact published distance and their per-event energy
balances remained within `1e-8 J`. The terminal values are ordinary binary
floating-point accumulation/cancellation at roughly `1e-15` relative scale,
not evidence of energy creation or destruction.

## Impact

The exact-zero-style assertion was stricter than the numerical representation
and obscured the useful non-zero residual. The model deliberately retains that
terminal residual as observable evidence.

## Fix

Keep the raw terminal residual unchanged. Test each per-event residual against
the declared `1e-8 J` absolute bound and test the terminal reconciliation at a
scale-aware relative bound of `2e-15` against initial onboard energy.

## Verification

```powershell
python -m unittest tests.test_digital_race -v
python -m unittest discover -s tests -v
python scripts/validate_digital_race.py
```

All commands exited with status `0`. The focused suite reported `Ran 9 tests`;
the repository suite reported `Ran 154 tests`; both reported `OK`. The validator
retained raw terminal residuals up to `1.1444091796875e-05 J`, reported all ten
finishes at zero distance residual, and confirmed monotonic onboard energy. The
issue is resolved without altering or hiding production residuals.
