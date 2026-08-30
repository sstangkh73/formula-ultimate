# Work 057 Plan: Campaign Physical Adapter and Burn-In

Status: Stopped — burn-in exposed a downstream serialization replay mismatch after all 240 training opportunities; protocol v1 prohibits repair and continuation after burn-in observation.

Thai companion: `2026-08-31_057_campaign-physical-adapter-burn-in-plan.th.md`

## Objective

Connect the committed Work 056 deterministic runner to the frozen Work 047–053 whole-vehicle evaluation chain, prove recovery across a separate process boundary, and execute only excluded burn-in seed `55999`. The work must produce an immutable go/stop adjudication before any admitted seed is touched.

## Scope and planned files

- Add reusable campaign evaluation, holdout, Work 053 refinement, STEP/FreeCAD witness, adjudication, and analysis code under `src/formula_ultimate/experiments/`.
- Add one generic campaign command under `scripts/experiments/` and a fail-fast `scripts/run_work057.ps1` wrapper.
- Add focused tests for physical-adapter identity, solver failure accounting, partition isolation, process-boundary resume, promotion/refinement/witness eligibility, and burn-in stop/go logic.
- Produce ignored Work 057 ledgers and evidence under `artifacts/work057/`.
- Add bilingual research and result records, validate, and commit Work 057 before starting Work 058.

## Frozen burn-in design

- Independent variable: proposal treatment (`GRID`, `RANDOM`, `EVOLUTION`).
- Burn-in seed: `55999`, excluded from pilot and main inference.
- Opportunities: `80` per treatment, `240` total. Every reserved attempt consumes one opportunity, including invalid, failed, or interrupted evaluation.
- Candidate variables, ranges, GRID mapping, RANDOM distribution, EVOLUTION initialization/mutation/parent rule, training partition, holdout partition, material, loads, thresholds, and promotion cap remain exactly those in `bounded_whole_vehicle_main_campaign_v1` and its pinned upstream identities.
- Dependent outputs: terminal training status/failure code, mass, energy, Level-0 objective, holdout status, Work 053 stress/deformation/convergence/cross-model result, STEP/FreeCAD validity and hash identity, supported-finisher presence, elapsed cost, and all conservation/numerical failures.
- Controls: equal treatment opportunity, exact replay, unique GRID proposals, no holdout access during proposal/training, analytical cantilever benchmark, project-vs-CalculiX cross-model comparison, invalid/mutated evidence rejection, and a process-boundary pending-reservation resume probe isolated from campaign evidence.

## Pipeline and evidence boundary

```text
reserve opportunity
  -> training grammar/geometry/Level 0
  -> training-only promotion (max 2 per treatment/seed)
  -> frozen holdout Level 0
  -> Work 053 project frame + CalculiX B31 refinement
  -> candidate-specific 3D -> STEP -> FreeCAD witness
  -> eligibility and burn-in infrastructure adjudication
```

Level 0 remains a selection gate. Work 053 remains bounded linear-elastic beam-network evidence. A STEP/FreeCAD witness proves exact candidate geometry transfer only. None is a physical-safety or manufacturability validation.

## Burn-in success criteria

Return `burn_in_accepted_for_admitted_main_campaign` only if all of the following are true:

1. frozen protocol and all upstream/tool SHA-256 identities match;
2. exactly `240` opportunities and terminal training results exist, split `80/80/80`, with no duplicates, skips, retries, or GRID repeats;
3. ledger replay and a separate-process pending-reservation recovery are exact;
4. training selection never reads holdout/refined data and promotion shortfalls are explicit without borrowing;
5. every promoted candidate receives a terminal holdout, refinement, and (when refinement passes) STEP/FreeCAD witness result; candidate identity is preserved throughout;
6. solver/process failures are terminal counted outcomes, not silent repair or neutral substitution;
7. no protocol code/config/threshold change is required after observing burn-in.

The burn-in need not favor the preferred hypothesis or produce a supported finisher. It tests infrastructure and protocol execution, not treatment efficacy.

## Failure and falsification criteria

Stop before Work 058 on any protocol/upstream/tool mismatch, ledger/replay disagreement, budget inequality, repeated GRID opportunity, partition leakage, missing terminal result, changed candidate, unavailable refined evaluator, hidden CAD repair, or required implementation/config change after burn-in. Record whether the failure contradicts runner reliability, adapter coherence, or only candidate feasibility.

## Validation

Run focused tests, full tests, compilation, preparation replay, the isolated process-resume probe, and burn-in. Re-run burn-in in verify-only mode, inspect exact counts and hashes, write bilingual result records, stage only Work 057 files, run `git diff --cached --check`, commit, and replay verification from the clean commit.

## Risks and non-goals

CalculiX subprocess count and STEP/FreeCAD generation may be slow. Hash chains are tamper-evident but not externally signed. Work 057 does not use main seeds, estimate treatment effects, change the frozen protocol, claim physical validation, push, or publish.
