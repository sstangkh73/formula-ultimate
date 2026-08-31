# Work 064 Result: Work 062 Finalist Nonlinear Execution

Status: Stopped

Thai companion: `2026-08-31_064_work062-finalist-nonlinear-execution-result.th.md`

## Outcome

The committed execution at `5739f5864eb47ca6bf3fa7440adc44a065a51afd` produced 102 terminal case records for 51 candidates. The first-pass summary reported 102 case passes and 51 candidate passes, with displacement amplification `1.0000041846576189` to `1.0000299794481688`, stress amplification `1.0000069976482437` to `1.0000338606574917`, and yield margin `358.6735825412834` to `1068.5258384564943`.

The mandatory immediate verify-only command failed with `VehicleFrameError: Work 064 deterministic summary replay mismatch`. Therefore none of those apparent passes is admitted as a completed research result.

## Root cause and preserved evidence

Candidate aggregate evidence used tuples in memory for `failure_codes` and `case_result_sha256`. Strict JSON serialization stored those values as lists. Verify-only reconstructed tuples and compared the in-memory mapping directly with the loaded JSON mapping, so structurally equivalent scientific values compared unequal. The append-only ledger remains under `artifacts/work064/` with 102 unique terminal records and is preserved as stopped evidence; it will not be edited or relabeled.

## Commands and exit status

- `py -3.14 scripts/structural/run_whole_vehicle_nonlinear_gate.py --artifact-root artifacts/work064` → exit `0`; provisional `51/51` candidate passes, 102 cases.
- `py -3.14 scripts/structural/run_whole_vehicle_nonlinear_gate.py --artifact-root artifacts/work064 --verify-only` → exit `1`; exact error `Work 064 deterministic summary replay mismatch`.
- Pre-execution validation: `py -3.14 -m unittest discover -s tests -q` → exit `0`; `Ran 379 tests in 28.216s`, `OK`.
- Pre-execution compilation: `py -3.14 -m compileall -q src scripts tests` → exit `0`.

## Decision, limitations, and follow-up

This is an orchestration/replay representation defect, not evidence that the nonlinear physics cases failed. However, exact replay is a required evidence gate, so Work 064 stops. A successor must use a new protocol/campaign identity, canonicalize the complete summary through strict JSON before both storage and comparison, add a regression test that crosses the actual write/read boundary, commit the remediation, and rerun fresh candidate processes without reusing Work 064 observations.
