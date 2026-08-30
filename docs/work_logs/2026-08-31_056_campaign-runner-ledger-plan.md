# Work 056 Plan: Campaign Runner and Append-Only Ledgers

Status: Completed

Thai companion: `2026-08-31_056_campaign-runner-ledger-plan.th.md`

## Objective

Implement the deterministic, resume-safe orchestration core required by the frozen Work 055 campaign without running burn-in or any admitted main seed. The runner must consume opportunity before evaluation, preserve candidate/RNG/ancestry identity, append tamper-evident budget and result records, reconstruct state exactly after interruption, select up to two training promotions per treatment/seed, and refuse main execution until a later work item supplies and validates the physical adapters and burn-in authorization.

## Scope and planned files

- Add campaign-runner state, chained JSONL ledger, resume/replay, promotion, and stage-transition contracts under `src/formula_ultimate/experiments/`.
- Add a Work 056 preparation/verification command and `scripts/run_work056.ps1`. It may initialize and verify an empty ignored workspace under `artifacts/work056/`; it must report `candidate_evaluations=0`.
- Add focused tests using synthetic callback results and temporary ledgers. Fixture opportunities are software tests, not Work 055 campaign observations and cannot enter campaign evidence.
- Add bilingual runner/ledger documentation and matching bilingual result records.

## Runner contract

- `budget_ledger.jsonl` reserves and consumes an attempt before evaluation and stores the full candidate declaration needed for deterministic recovery.
- `result_ledger.jsonl` stores exactly one terminal training result per reserved attempt. A crash after reservation leaves an explicit pending attempt; resume must reconstruct the same candidate and may complete that exact reservation only.
- Every row carries protocol/campaign identity, monotonic sequence, previous-row SHA-256, payload, and record SHA-256. Truncation, mutation, duplicate result, skipped attempt, treatment/seed drift, or cross-ledger mismatch fails closed.
- The runner rebuilds each agent by replaying proposal and observation order, compares candidate identity and RNG checkpoint, and resumes from the first incomplete reservation.
- Promotion selection uses only terminal training-feasible records, sorts by training objective then candidate ID, caps at two per treatment/seed, and records an explicit shortfall without borrowing.
- Main seeds and burn-in seed are execution-locked in Work 056. Only `prepare`/`verify` commands are allowed outside tests.

## Validation

1. Prove exact chained-ledger replay, append, restart, and fingerprint behavior.
2. Simulate interruption after reservation and verify the exact candidate completes once without extra budget.
3. Reject altered/truncated rows, wrong previous hash, duplicate result, unreserved result, skipped attempt, changed RNG/candidate, seed/treatment drift, and cross-seed promotion borrowing.
4. Verify equal planned budget and non-repeating GRID mapping from the Work 055 protocol while performing zero campaign evaluations.
5. Run focused/full tests, compilation, repository contract, fail-fast staged checks, explicit scoped commit, and clean-tree Work 056 replay.

## Success criteria

- Runner mechanics and append-only ledgers are deterministic and fail closed under all declared negative fixtures.
- Work 056 command returns `runner_prepared_campaign_locked`, exact replay, and `candidate_evaluations=0`.
- No artifact from unit fixtures can be confused with `FU-BMC-001` campaign evidence.
- No admitted or burn-in seed is evaluated.

## Failure criteria

Stop if an interrupted attempt can disappear or consume twice, if altered ledger content is accepted, if resume creates a different candidate, if promotion reads holdout/refined data, or if any Work 056 command can execute main/burn-in seeds.

## Risks and explicit non-goals

Filesystem append plus `flush/fsync` reduces but cannot eliminate storage/hardware failure; hash chains detect corruption but are not an external signature. Work 056 does not implement CalculiX/STEP/FreeCAD campaign adapters, run burn-in, run the main campaign, perform statistical analysis, change Work 055 rules, push, or publish.
