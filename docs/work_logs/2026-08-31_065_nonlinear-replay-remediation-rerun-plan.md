# Work 065 Plan: Nonlinear Replay Remediation and Fresh Rerun

Status: Completed

Thai companion: `2026-08-31_065_nonlinear-replay-remediation-rerun-plan.th.md`

## Objective

Remediate the Work 064 strict-JSON representation defect under new execution protocol `work062_finalist_nonlinear_execution_v2` and campaign `FU-NLG-002`, then rerun all 102 candidate/holdout cases from a clean committed tree. Work 064 observations are not reused.

## Controlled change

The only behavioral remediation is canonical strict-JSON round-trip normalization before summary storage and comparison. Add a regression test that writes and reloads tuple-bearing aggregate evidence across the actual JSON boundary. The Work 063 gate configuration, source inclusion, candidate geometries, loads, mesh, material, thresholds, solver, failure policy, and analysis remain scientifically unchanged.

## Scope and planned files

- Add `config/experiments/work062_finalist_nonlinear_execution_v2.json` with supersession and unchanged-science declarations.
- Update `scripts/structural/run_whole_vehicle_nonlinear_gate.py` for separate execution-protocol identity and strict-JSON summary normalization.
- Update focused runner tests with a disk round-trip replay regression and v2 identity checks.
- Generate fresh ignored evidence under `artifacts/work065/`.
- Add bilingual research/result records and update this plan after terminal replay.

## Validation and success criteria

Before execution, demonstrate v1/v2 scientific-rule equivalence, focused regression tests, full tests, and compilation; then commit plan/code/config/tests. Execute exactly 51 candidates and 102 cases under `FU-NLG-002`. Success requires terminal ledgers, explicit distributions/ranges, exact immediate verify-only replay, bilingual evidence, a second result commit, and exact post-commit clean-tree replay. A zero-pass physical outcome remains valid.

## Commit structure, risks, and non-goals

Two commits are required: the first freezes remediation before fresh execution; the second records results. Any post-start code/config change stops `FU-NLG-002`. Risks remain solver/parser failure and beam-model insensitivity. No physical validation, buckling certification, material nonlinearity, contact, fracture, fatigue, safety, manufacturability, algorithm superiority, or independent search replication is claimed.
