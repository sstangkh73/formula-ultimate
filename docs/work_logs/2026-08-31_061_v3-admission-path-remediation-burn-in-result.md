# Work 061 Result: Protocol v3 Admission-Path Remediation and Burn-In

Status: Completed

Thai companion: `2026-08-31_061_v3-admission-path-remediation-burn-in-result.th.md`

## Outcome

Created `bounded_whole_vehicle_main_campaign_v3` / `FU-BMC-003`, preserved Work 060 failure provenance, and changed only admission protocol-file routing. Admission validation is now a testable function that hashes the exact active protocol path before any ledger is created and requires matching protocol/campaign, fingerprint, upstream, tools, implementation, committed ancestor, and clean worktree. Fresh v3 process recovery and burn-in passed; decision `burn_in_accepted_for_admitted_main_campaign`.

## Validation

- `py -3.14 -m unittest tests.test_main_campaign_protocol tests.test_campaign_physics tests.test_campaign_runner -q` → exit `0`, `29` tests, `OK`.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work061.ps1` → exit `0`; process probe `1/1/0`; burn-in attempts `240`, promotions/refined/CAD `6/6/6`, supported streams `3`, replay exact.
- `py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind burn-in --protocol config/experiments/bounded_whole_vehicle_main_campaign_v3.json --artifact-root artifacts/work061 --verify-only` → exit `0`, exact.
- `py -3.14 -m unittest discover -s tests -q` → exit `0`, `Ran 372 tests in 26.565s`, `OK`.
- `py -3.14 -m compileall -q src scripts tests` → exit `0`.

## Evidence

- Protocol fingerprint: `9ef748f2719923632a05ef5fcbba95b8f2fa1b4156d2dbbf6cb9b4fbd02d4c36`.
- Training fingerprint: `99c43aa5b8c6dfd64e13b48da47288f2081afe9159a1fc0d76de44f2f2b08eac`.
- Stage fingerprint: `47e6a64109492cb3af077c76c0b602f9ebc4bb99b30266f226d88def96bbed65`.
- Training reservations/results/pending `240/240/0`; stream counts `80/80/80`; GRID unique `80`; feasible/structural failure `189/51`.
- Promotions/shortfall `6/0`; terminal and passed holdout/refinement/CAD evidence complete.

## Review and limitations

Supporting evidence includes exact active-path admission regression, scientific equivalence, cleanly separated identities, process recovery, equal budgets, physical benchmark, downstream completion, and replay. Contradicting evidence is that two earlier versions found missing orchestration tests; those failures remain part of the record. Success on primitive bounded geometry may not transfer to arbitrary vehicles. Main campaign, independent replication, higher-fidelity nonlinear/contact/solid analysis, material calibration, tolerances, and hardware tests remain missing. Confidence is high only for exact v3 admission mechanics and bounded burn-in.

Commit identity and post-commit clean-tree admission replay are reported after this record is committed.
