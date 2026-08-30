# Work 061 Plan: Protocol v3 Admission-Path Remediation and Burn-In

Status: Completed

Thai companion: `2026-08-31_061_v3-admission-path-remediation-burn-in-plan.th.md`

## Objective

Create successor protocol/campaign v3 after Work 060 failed closed before main-ledger initialization. Replace the hard-coded v1 admission hash path with the exact active protocol path, add a regression test that executes successor admission validation, then run and commit a fresh excluded-seed burn-in before any successor main opportunity.

## Frozen remediation scope

- New IDs: `bounded_whole_vehicle_main_campaign_v3` and `FU-BMC-003`.
- Frozen source commit: `3d140bf8ffb2ad7f1476ca81905fb84648741481`.
- Preserve Work 060 failure SHA-256 `8b02e9292e173b797afe12134031547c3060a70a8da1270a1e06fe1b8a17e1e2` and v2 admission fingerprints without reusing observations.
- Change only admission protocol-file identity routing: validation must hash the `--protocol` path actually selected by the command.
- Scientific rules, seeds, budgets, search, physics, partitions, thresholds, outcomes, statistics, and claims remain byte-equivalent after identity/remediation fields are removed.

## Planned files and tests

- Add the full v3 protocol declaration and extend exact successor validation.
- Move admission validation into a testable campaign-physics function accepting the active protocol path.
- Update the generic command to call that function; add Work 061/062 wrappers.
- Test valid v3 admission against the v3 path, rejection against a different path, scientific equivalence across v1/v2/v3, and the previous JSON representation regression.
- Run fresh v3 process-resume and burn-in ledgers under `artifacts/work061/`, document, validate, and commit.

## Success and stop criteria

Success requires focused/full tests, exact v3 protocol validation, process probe `1/1/0`, fresh burn-in `240/240/0`, equal `80/80/80`, unique GRID, terminal downstream evidence, exact replay, accepted decision, commit, and clean-tree replay whose admission validator passes against the exact v3 path without creating a main ledger.

Stop if any code/config change is needed after v3 burn-in, if admission-path regression fails, or if any fairness, identity, partition, solver, CAD, ledger, or replay gate fails. No main seed in Work 061.

## Evidence discipline and non-goals

Report the two prior fail-closed controls rather than hiding them. This remains bounded digital evidence, not physical validation or safety proof. Do not change scientific settings, push, or publish.
