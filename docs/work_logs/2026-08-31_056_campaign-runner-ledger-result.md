# Work 056 Result: Campaign Runner and Append-Only Ledgers

Status: Completed

Thai companion: `2026-08-31_056_campaign-runner-ledger-result.th.md`

## Outcome

Implemented a deterministic, resume-safe campaign runner with separate hash-chained opportunity-budget and terminal-result ledgers. The Work 056 preparation command returned `runner_prepared_campaign_locked`; it performed zero candidate, burn-in, and main-seed evaluations. Therefore this work is runner-mechanics evidence only, not campaign-outcome or physical-validation evidence.

## Files changed

- `src/formula_ultimate/experiments/campaign_runner.py`: chained JSONL ledger, cross-ledger validation, candidate/evaluation identity verification, deterministic agent reconstruction, interruption resume, explicit execution authorization, and training-only promotion selection.
- `src/formula_ultimate/experiments/__init__.py`: public runner exports.
- `scripts/experiments/prepare_main_campaign_runner.py` and `scripts/run_work056.ps1`: preparation-only state initialization, exact replay, and execution-lock control.
- `tests/test_campaign_runner.py`: ten positive and adversarial runner/ledger tests.
- `docs/research/BOUNDED_MAIN_CAMPAIGN_RUNNER_LEDGER.md` and Thai companion: maintained contract and evidence boundary.
- Work 056 bilingual plan and result records.

Generated ignored evidence: `artifacts/work056/runner_preparation.json` and empty `artifacts/work056/preparation_only/*.jsonl` ledgers.

## Decisions

- Opportunity is consumed by a durable reservation before evaluator invocation. An interruption leaves the latest reservation pending; resume completes that exact candidate without allocating another attempt.
- Candidate ID, RNG checkpoint, ancestry, evaluation SHA-256, sequence, and previous-row hash are checked independently of the row hash.
- Execution requires a non-empty authorization matching campaign ID, evidence class, and seed. Admitted main execution also requires its explicit flag.
- Promotion reads training evidence only, selects at most two feasible candidates per treatment/seed, and records shortfall without borrowing.
- Preparation uses campaign ID `PREP-FU-BMC-001` and evidence class `preparation_only`; its rows cannot be confused with admitted `FU-BMC-001` evidence.

## Validation record

All commands ran from `C:\Formula Ultimate` on Python 3.14.

1. Focused runner tests after identity/authorization hardening:

   ```powershell
   py -3.14 -m unittest tests.test_campaign_runner -q
   ```

   Exit status: `0`. Relevant output: `Ran 10 tests in 0.188s` and `OK`.

2. Preparation-only command:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work056.ps1
   ```

   Exit status: `0`. Relevant output: `status=passed`, `decision=runner_prepared_campaign_locked`, `execution_lock=rejected_as_expected`, `replay=exact`, `reservations=0`, `results=0`, `pending=0`, and `candidate_evaluations=0`.

3. Focused integration and repository-contract tests:

   ```powershell
   py -3.14 -m unittest tests.test_campaign_runner tests.test_main_campaign_protocol tests.test_whole_vehicle_search tests.test_repository_contract -q
   ```

   Exit status: `0`. Relevant output: `Ran 27 tests in 0.868s` and `OK`.

4. Full test suite:

   ```powershell
   py -3.14 -m unittest discover -s tests -q
   ```

   Exit status: `0`. Relevant output: `Ran 360 tests in 28.745s` and `OK`.

5. Python compilation:

   ```powershell
   py -3.14 -m compileall -q src scripts tests
   ```

   Exit status: `0`; no error output.

Staged-scope checks, commit identity, and clean-tree replay are recorded in the final handoff because the commit hash does not exist until after this result file is staged.

## Review discipline

Supporting evidence: exact ledger replay, one-time recovery of a pending reservation, authorization lock before evaluator invocation, rejection of mutated/truncated/rehashed-invalid evidence, monotonic budget enforcement, and training-only per-stream promotion were exercised by tests.

Contradicting evidence: no external solver or real process interruption was exercised. A hash chain is not an external signature, and fixture behavior cannot establish storage durability on every filesystem or hardware failure mode.

Alternative explanation: the unit fixtures may omit timing, process, or adapter failures that occur during a long CalculiX or FreeCAD run.

Missing evidence: CalculiX evaluation adapter, STEP/FreeCAD finalist adapter, real interruption recovery, burn-in seed `55999`, burn-in acceptance, admitted main seeds, statistical analysis, and higher-fidelity physical validation.

Confidence: high that the implemented software contract is deterministic and fail-closed for the tested cases; zero campaign-outcome evidence was produced.

## Follow-up

Work 057 should implement and test the physical adapter boundary, then run only the excluded burn-in seed `55999` under a separate explicit authorization. The admitted paired seeds must remain locked until burn-in acceptance is reviewed and recorded.
