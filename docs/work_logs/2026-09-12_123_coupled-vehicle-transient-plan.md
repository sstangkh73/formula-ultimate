# Work 123 Plan: Coupled Whole-Candidate Transient Harness

Thai companion: `2026-09-12_123_coupled-vehicle-transient-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Integrate exact Work 117–122 identities into one bounded exploratory candidate transient with explicit state ownership and exchange signs. Couple controller demand, ground-force capacity, actuation power/loss, stored energy, drag/cooling and thermal state through a shared time base while retaining structural/material/interaction limitations.

Use conservative step work accounting, event timing, fixed-point power coupling and three time steps. Record histories, interface ledgers, validity excursions and stop/failure states; compare a decoupled control to localize coupling effects. Successful integration must not promote the incomplete candidate.

## Variables, controls and files

- IV: coupling enabled/decoupled, time step, controller demand, event timing, initial energy, frame/sign schema and model validity.
- DV: trajectory, final speed/position/energy/temperature, interface work/heat residual, coupling iterations, events and promotion blockers.
- Controls: same external task/initial state; mismatched sign/frame, double-counted power, delayed command event, depleted energy, out-of-range flow model and decoupled run.
- Success: exact upstream identities, conservative ledgers, stable three-level refinement, causal controls, explicit unresolved blockers and exact replay.

Planned files: `src/formula_ultimate/simulation/coupled_vehicle_transient.py`, `config/development/coupled_vehicle_transient_v1.json`, `scripts/development/run_coupled_vehicle_transient.py`, `tests/test_coupled_vehicle_transient.py`, bilingual `docs/contracts/COUPLED_VEHICLE_TRANSIENT_V1*`, this bilingual plan/result and ignored `artifacts/work123/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_coupled_vehicle_transient tests.test_repository_contract -v
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_a
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_b --replay-reference artifacts/work123/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 117–122 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

This reduced harness is not a complete detailed vehicle. Non-goals: favorable coefficients for unresolved domains, verified failure margins, full controller/ground/aero dynamics, race completion, vehicle readiness, physical validation, push or history rewrite.
