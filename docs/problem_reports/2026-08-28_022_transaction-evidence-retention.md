# Work 022 Problem Report: Transaction Evidence Retention

Status: Resolved

Thai companion: `2026-08-28_022_transaction-evidence-retention.th.md`

## Problem

Review after the first passing Work 022 validator found that adapter residuals
and event candidates affected control flow and appeared by ID in traces, but the
raw `ResidualEntry` and `EventCandidate` records were not retained in
`CoupledStepResult`. A failed residual therefore prevented commit correctly but
its exact value, unit, tolerance, and event evidence were unavailable to the
caller after rollback.

## Impact

Signal atomicity was intact, but scientific auditability was incomplete. This
would violate the project rule that conservation residuals and invalid states
remain observable rather than being reduced to a generic failure.

## Planned fix

- Add immutable transaction-level residual and event collections.
- Retain all evidence produced through the stopping module on invalidity.
- Keep `published_signals` empty for every invalid transaction; evidence is not
  a partial state commit.
- Reject duplicate residual/event IDs across modules to keep provenance
  unambiguous.
- Add regression tests and validator evidence for raw failed residual retention.

## Verification

The corrected result retains the injected `force-x` residual with raw value
`2.0 N` and tolerance `0.1 N`, while `published_signal_count` remains `0` and
rollback returns the exact start state.

```powershell
python -m unittest tests.test_coupled_transaction -v
# Ran 11 tests ... OK (exit 0)

python -m unittest discover -s tests -v
# Ran 177 tests ... OK (exit 0)

python scripts/validate_coupled_transaction.py
# residual retained; rollback true; published signals 0; exit 0

python -m compileall -q src scripts tests
# exit 0
```
