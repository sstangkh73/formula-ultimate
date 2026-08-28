# Work 023 Problem Report: Circuit Profile Fingerprint Under-Pinning

Status: Resolved

Thai companion: `2026-08-28_023_profile-fingerprint-underpinning.th.md`

## Problem

Review of the first passing Work 023 focused suite found that the step-input
fingerprint included only `profile.circuit_id`, not the complete circuit profile.
Changing lap facts, evidence, or design-pressure data while retaining the same
ID would therefore leave the fingerprint unchanged.

## Impact

Typed inputs and missing-evidence behavior were correct, but replay identity was
under-pinned and could not prove which catalog contents were evaluated.

## Fix

Canonicalize the complete immutable `CircuitProfile`, including nested source
evidence and ISO-formatted dates, into the step-input fingerprint. Add a
regression test proving that changing profile content under the same ID changes
the fingerprint.

## Verification

The regression changes a profile name under the same circuit ID and now obtains
a different SHA-256 fingerprint. Catalog permutation still replays exactly.

```powershell
python -m unittest tests.test_step_inputs -v
# Ran 9 tests ... OK (exit 0)
python -m unittest discover -s tests -v
# Ran 186 tests ... OK (exit 0)
python scripts/validate_step_inputs.py
# catalog_permutation_replay_equal: true; exit 0
```
