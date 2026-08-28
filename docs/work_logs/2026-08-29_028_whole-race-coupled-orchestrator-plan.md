# Work 028 Plan: Whole-Race Coupled Orchestrator

Status: Completed

Thai companion: `2026-08-29_028_whole-race-coupled-orchestrator-plan.th.md`

## Objective

Execute one fixed-topology reference vehicle through every coupled stage in deterministic transactions until finish, depletion, physical failure, timeout, or invalidity, with exact same-seed replay and complete per-step provenance telemetry.

## Scope

- Implement the `race_progress_solver` adapter that merges motion, energy, and health candidates into exactly one `state.next`.
- Version the architecture for the Work 028 race-progress adapter if required.
- Build a fixed-topology reference fixture using the Work 023-027 adapters.
- Run repeated atomic `execute_coupled_step` transactions.
- Rebuild duration-dependent adapters from the committed state each step.
- Stop on finish, depletion, thermal/degradation/damage/reliability/contact failure, timeout, or invalid transaction.
- Record architecture, model versions, seed, scenario/input fingerprints, start/end state, signals, residuals, events, traces, and terminal reason.
- Prove registration-order invariance and same-seed exact replay.
- Add explicit failure fixtures for depletion, failure, timeout, invalid input, and incomplete provenance.
- Record and resolve every discovered defect in a separate bilingual report.

## Planned Files

- `src/formula_ultimate/simulation/whole_race.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_whole_race.py`
- `scripts/validate_whole_race.py`
- `config/simulation/coupled_level0_architecture_v4.json` if required
- `docs/simulation/WHOLE_RACE_COUPLED_ORCHESTRATOR.md`
- `docs/simulation/WHOLE_RACE_COUPLED_ORCHESTRATOR.th.md`
- Work 028 problem reports if required
- implementation queue, this plan, and matching bilingual result records

## Experiment Definition

- Independent variables: fixed vehicle/scenario configuration, strategy command, timestep, energy start, thermal/reliability parameters, timeout, seed, and adapter registration order.
- Dependent variables: outcome, final state/time/distance/energy/health, step count, event winner, telemetry fingerprint, residual ledger, and replay metadata.
- Controls: architecture fingerprint, model versions, component/contact topology, spatial/weather evidence, evaluation budget, and exact initial state.
- Metrics: finish-distance residual, energy residual, failed residual count, transaction rollback correctness, replay equality, provenance completeness, and terminal localization.
- Success criteria: reference reaches an intended terminal outcome; same inputs/seed replay exactly; reversed adapter registration produces identical result; each declared terminal failure is observable; invalidity publishes no state; telemetry contains complete provenance for every committed step.
- Failure criteria: a terminal state advances again; a failed transaction partially commits; telemetry omits a model/input/seed/state identity; same-seed results differ; or finish/depletion/failure/timeout precedence is inconsistent.
- Falsification attempt: low energy, high heat/hazard, zero progress, invalid corridor, exhausted evaluation budget, exact finish tie, and adapter-order permutation.

## Validation

1. Focused Work 028 tests.
2. Entire repository test suite.
3. Standalone Work 028 validator.
4. Python bytecode compilation.
5. `git diff --check` and `git diff --cached --check`.
6. Explicit staged-scope review before commit.

## Success Criteria

- All eight architecture stages execute through the atomic transaction boundary.
- One fixed-topology reference completes a deterministic analytical race fixture.
- Finish, depletion, failure, timeout, and invalid outcomes are tested.
- Same-seed and registration-order replay are exact.
- Complete provenance and residual/event evidence are retained per step.
- English and Thai documentation agree.
- Work 028 is committed as one validated commit.

## Risks

- The current race-progress stage may lack a Work 028 adapter/version contract.
- Full real-circuit spatial/weather evidence is unavailable, so the reference must remain an analytical fixture.
- Aerodynamic map bounds and corridor width can terminate a long run before the intended gate.
- Terminal events inside a prospective step require consistent state merge and finish priority.
- Telemetry can become large; the validation fixture must remain bounded.

## Explicit Non-goals

- No ten-circuit baseline campaign or Work 029 compute fairness result.
- No integration-falsification release gate from Work 030.
- No claim that the analytical fixture predicts a real Formula 1 race.
- No CAD optimization, topology search, CFD, or physical validation.
