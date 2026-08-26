# Work 016 Problem Report: Slotted Dataclass Serialization

Status: Resolved

Thai companion: `2026-08-26_016_slotted-dataclass-serialization.th.md`

## Problem

The first Work 016 test run produced 10 passes and one error. The steady-state
test attempted to enumerate `PlanarBalanceResiduals.__dict__`, but every Work
016 evidence dataclass uses `slots=True` and therefore has no `__dict__`.

```text
AttributeError: 'PlanarBalanceResiduals' object has no attribute '__dict__'
Ran 11 tests
FAILED (errors=1)
```

The validator contained the same unsupported serialization assumption. This
was a test/evidence formatting defect; the physics calculations in the other
ten tests passed.

## Root cause

The test and validator treated a slotted dataclass like a normal object with an
instance dictionary. `slots=True` intentionally removes that dictionary.

## Fix

- The test now uses `dataclasses.astuple` to enumerate residual values.
- The JSON validator now uses `dataclasses.asdict` for named residual fields.
- No physics equation, tolerance, solver branch, or output value was changed.

## Verification

```powershell
python -m unittest tests.test_lateral -v
python scripts/validate_lateral.py
```

Result:

```text
Ran 11 tests
OK
validator exit status: 0
```

The subsequent full repository run also passed 121 tests. The issue is resolved
and no unsupported `__dict__` access remains in the Work 016 test or validator.
