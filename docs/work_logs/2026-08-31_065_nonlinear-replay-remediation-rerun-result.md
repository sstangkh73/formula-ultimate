# Work 065 Result: Nonlinear Replay Remediation and Fresh Rerun

Status: Completed

Thai companion: `2026-08-31_065_nonlinear-replay-remediation-rerun-result.th.md`

## Outcome

Remediated the Work 064 tuple/list replay defect by normalizing the complete summary through strict JSON before both storage and comparison. Froze the change in commit `729edcbfa7574a5bfa2d3aa972fb15acec7e4295`, created fresh campaign `FU-NLG-002`, reran all 102 cases without using Work 064 observations, and obtained exact immediate replay. All 51 candidates and 102 cases passed the Work 063 geometric-nonlinearity sensitivity thresholds.

## Files changed

- `config/experiments/work062_finalist_nonlinear_execution_v2.json`
- `scripts/structural/run_whole_vehicle_nonlinear_gate.py`
- `tests/test_work062_nonlinear_execution.py`
- English/Thai Work 065 plan, result, and research result documents.
- Fresh ignored evidence under `artifacts/work065/`.

## Exact validation commands

- `py -3.14 -m unittest tests.test_work062_nonlinear_execution tests.test_vehicle_nonlinear_gate -q` → exit `0`; `Ran 9 tests`, `OK`.
- `py -3.14 -m unittest discover -s tests -q` before execution → exit `0`; `Ran 381 tests in 28.728s`, `OK`.
- `py -3.14 -m compileall -q src scripts tests` before execution → exit `0`.
- `py -3.14 scripts/structural/run_whole_vehicle_nonlinear_gate.py --artifact-root artifacts/work065` → exit `0`; 51 candidates, 102 cases, 51 candidate passes.
- `py -3.14 scripts/structural/run_whole_vehicle_nonlinear_gate.py --artifact-root artifacts/work065 --verify-only` → exit `0`; replay `exact`.
- `py -3.14 -m unittest discover -s tests -q` after execution → exit `0`; `Ran 381 tests in 28.740s`, `OK`.
- `py -3.14 -m compileall -q src scripts tests` after execution → exit `0`.

## Evidence and review

Ledger fingerprint is `ffbc7eef129b5c51cb114bfa6ec849fae15617f32bbc0c022aa05e1f50825e27`; summary identity is `4d28434bd2a050045fdd8579bd4ce5e75ab11c827af3e0744da2d321dfd6227f`. There were 306 solver processes, zero nonzero exits, zero missing confirmations, and no failure codes. Maximum displacement/stress amplification was `1.0000299794481688` / `1.0000338606574917`; minimum yield margin was `358.6735825412834`.

The evidence supports negligible geometric-nonlinearity sensitivity only within the frozen beam/load/synthetic-material domain. It contradicts no gate threshold, but its very large margins may indicate under-severe loads or abstraction limits. No buckling, physical-validation, safety, fracture, fatigue, contact, material-nonlinear, or algorithm-superiority claim is made. The result commit and post-commit clean-tree replay are reported in the final handoff.
