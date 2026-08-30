# Work 046 Plan: Structural Failure Coupling and DNF

Status: Completed

Thai companion: `2026-08-30_046_structural-failure-coupling-plan.th.md`

## Objective

Couple admitted yield, fracture-initiation, fatigue, and exact-interface evidence into a deterministic typed connection state so a localized failure removes its wrench path, redistributes through declared redundancy when possible, or emits structural `DNF` when no required path remains.

## Scope and claim boundary

This is a bounded coupling-policy experiment under Work 051's narrow Gate A contract. It validates state transitions, event localization, wrench closure, failure-energy accounting, topology logic, race-event typing, replay, and fail-closed behavior. It does not simulate crack propagation, contact separation dynamics, impact, crash absorption, occupant safety, or real joint strength.

## Experimental design

- Independent variables: failure mechanism (`yield`, `fracture`, `fatigue`), absolute crossing time, critical versus redundant connection topology, timestep, energy partition, and arbitration ties.
- Dependent variables: `intact -> degraded -> failed` state, connection wrench, redistribution, force/moment residual, stored/released/dissipated energy, event time, subsystem outcome, race event, and replay fingerprint.
- Controls: identical pre-failure state, exact Work 051 element/boundary identity, connection definitions, applied wrench, candidate evidence hashes, event priority, and energy policy.
- Preferred hypothesis: a failed connection transmits exactly zero wrench after the localized event; a redundant survivor closes force/moment residuals within `1e-5`; released plus dissipated energy closes within `1e-4`; localized event time changes by at most relative `1e-6` across frozen timestep refinements; a required path with no survivor produces deterministic `DNF`; identical inputs replay exactly.
- Falsification: retain ties and residuals, reject unknown/duplicate connections, reject out-of-domain Gate A evidence, reject event times outside the step, reject invalid energy partitions, and return no candidate state on invalid evidence.

## Planned files

- `config/simulation/structural_failure_coupling_v1.json`
- `src/formula_ultimate/simulation/structural_failure_coupling.py`
- coupling/race integration exports and event typing
- `scripts/simulation/run_structural_failure_coupling.py`
- `scripts/run_work046.ps1`
- `tests/test_structural_failure_coupling.py`
- `docs/physics/STRUCTURAL_FAILURE_COUPLING_DNF.md` and `.th.md`
- matching Work 046 bilingual result records
- ignored evidence under `artifacts/work046/`

## Validation

Run focused tests, deterministic Work 046 experiment, coupling/whole-race regressions, full repository tests, Python compilation, repository-contract checks, staged-diff checks, an explicit scoped commit, and clean-tree replay.

## Success criteria

- Failed connections have a bitwise-zero six-component post-event wrench.
- Redundant redistribution meets `1e-5` force/moment residual limits or fails observably.
- Failure energy meets `1e-4` residual limit without deletion or hidden correction.
- Event-time refinement meets relative `1e-6`.
- Critical topology yields a deterministic structural `DNF`; redundant topology remains running only when it re-equilibrates.
- Invalid evidence produces no committed connection state and same inputs replay exactly.

## Risks

The policy uses typed upstream crossing events rather than a transient fracture solver. Instantaneous redistribution omits stress waves and may create loads outside the upstream evidence domain. The exact Work 051 identity restriction is intentionally narrow.

## Explicit non-goals

No whole-vehicle geometry, arbitrary joint transfer, post-critical structural response, fracture propagation, fatigue crack growth, crashworthiness, design search, push, or publication is included.
