# Work 028 Result: Whole-Race Coupled Orchestrator

Status: Completed

Thai companion: `2026-08-29_028_whole-race-coupled-orchestrator-result.th.md`

## Outcome

Implemented a deterministic whole-race Level-0 orchestrator that executes the complete eight-stage coupled architecture through atomic transactions until finish, energy depletion, physical failure, timeout, invalidity, or evaluation-budget exhaustion. Each attempted step retains replay identity, numerical evidence, transaction traces, and terminal provenance.

## Files Changed

- Added `config/simulation/coupled_level0_architecture_v4.json`.
- Added `src/formula_ultimate/simulation/whole_race.py` and exported its public contracts from `src/formula_ultimate/simulation/__init__.py`.
- Added `tests/test_whole_race.py` and `scripts/validate_whole_race.py`.
- Strengthened `src/formula_ultimate/simulation/step_inputs.py`, its tests, and validator with the state/scenario distance invariant.
- Corrected exact-end depletion and residual publication ownership in `src/formula_ultimate/simulation/energy_health_coupling.py`.
- Added the bilingual whole-race model record, this plan/result pair, five bilingual problem reports, and updated the coupled implementation queue.

## Resolved Problems

1. Scenario distance could disagree with the shared start state.
2. The race-progress stage lacked `state.current` in the compiled signal graph.
3. Energy depletion exactly at the requested step end did not produce a depletion event.
4. The health adapter re-emitted energy residual IDs already owned by the energy adapter.
5. The standalone validator used floating-point `0.0` for an integer traffic count.

Every problem has a separate English and Thai report in `docs/problem_reports`.

## Decisions

- Preserve architecture v1-v3 and add v4 with `work028-race-progress-v1`.
- Keep adapter registration independent from compiled execution order.
- Rebuild duration-dependent adapters from the last committed state every step.
- Merge motion, energy, health, finish, timeout, and step-complete candidates through the common deterministic event arbitrator.
- Keep exact-time ties observable while committing one deterministic status.
- Publish residual IDs only from their owning adapter.
- Treat evaluation-budget exhaustion as a timeout outcome with the explicit reason `evaluation budget exhausted`.
- Retain invalid attempted-step telemetry without an end-state identity or partial state advance.

## Experiment and Falsification Result

- Independent variables exercised: initial energy, auxiliary draw, central heat, timeout, evaluation budget, corridor width, seed, and adapter registration order.
- Dependent evidence: outcome, terminal time/state, committed step count, residuals, event ledger, state/input fingerprints, traces, and replay fingerprint.
- Controls: architecture fingerprint, eight model versions, fixed four-contact topology, zero-aero analytical map, straight corridor, `1 s` timestep, `10 m/s` start speed, and fixed seed.
- Preferred-hypothesis falsification: depletion, thermal failure, timeout, invalid corridor, missing adapter, budget exhaustion, exact finish/depletion tie, and reversed registration all produced the declared observable result.
- Contradicting evidence: none within the analytical fixtures.
- Alternative explanation: exact replay demonstrates deterministic implementation, not real-world accuracy.
- Missing evidence: measured ten-circuit local geometry/weather, calibrated models, numerical refinement, uncertainty, and higher-fidelity validation.
- Confidence: high for the declared deterministic software contracts; low for real-race prediction because that claim is outside Work 028 evidence.

## Validation Commands and Evidence

All commands returned exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_step_inputs tests.test_energy_health_coupling tests.test_whole_race -v
python -m unittest discover -s tests
python scripts/validate_step_inputs.py
python scripts/validate_energy_health_coupling.py
python scripts/validate_whole_race.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

- focused Work 023/027/028 regression: 29 passed in `0.291 s`;
- full repository suite: 240 passed in `0.742 s`;
- architecture v4 fingerprint: `abf3148cfba2063f8fdba23951239b2b0a4a899c391503d3e46db69fd203618d`;
- reference outcome: `finished`, three committed steps, `3.0 s`, `30.0 m`, finish residual `0.0 m`;
- whole-race replay fingerprint: `419b25773df7982aebb606d5a834b84f95a6c6a0fdc32735c063cb8e10793163`;
- same-seed replay and reversed registration: exact equality;
- depletion: `0.5 s`, primary energy `0.0 J`;
- thermal failure: `0.2 s`;
- timeout: `1.5 s`;
- invalid corridor: no committed state identity;
- all reference residuals passed and all eight adapter traces were recorded per committed step.

## Limitations

Level 0 only. The successful run is a controlled analytical integration fixture, not real-circuit prediction or physical validation. It lacks measured per-segment evidence, strategy optimization, calibrated tyre/aero/thermal/reliability models, full 3D contact, uncertainty quantification, and cross-model validation.

## Follow-up

Work 029 may now build a fair fixed-topology campaign across the ten declared circuit profiles. Work 030 must still close numerical refinement, deliberate integration-defect falsification, and the promotion/release gate before autonomous candidates can be treated as discoveries.
