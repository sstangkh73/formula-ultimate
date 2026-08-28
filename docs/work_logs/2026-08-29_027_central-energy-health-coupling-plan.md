# Work 027 Plan: Central Energy and Health Coupling

Status: Completed

Thai companion: `2026-08-29_027_central-energy-health-coupling-plan.th.md`

## Objective

Couple Work 025 contact energy transfers and health inputs with Work 024 aerodynamic cooling into one deterministic central energy, thermal, degradation, damage, and seeded-reliability state update. The earliest physical event must truncate every affected quantity to the same executed duration.

## Scope

- Define typed central-energy and component-health configuration and evidence.
- Audit primary use, recovered energy, conversion loss, mechanical heat, thermal storage, and heat rejection without hidden correction.
- Advance `SharedVehicleState.primary_energy_j`, `recovered_energy_j`, and component health.
- Apply thermal derating, degradation, damage, and seeded reliability hazards with explicit event candidates.
- Select the earliest energy, thermal, degradation, damage, suspension, or reliability event with deterministic tie handling.
- Truncate transfers and all state increments to the same event time.
- Add adapter contracts for `energy_graph_audit` and `health_event_solver` plus a final merged health candidate.
- Version the coupling architecture if the existing declared signal dependencies cannot support the required state merge.
- Record every discovered defect in a separate bilingual problem report and resolve it before completion.

## Planned Files

- `src/formula_ultimate/simulation/energy_health_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_energy_health_coupling.py`
- `scripts/validate_energy_health_coupling.py`
- `docs/simulation/CENTRAL_ENERGY_HEALTH_COUPLING.md`
- `docs/simulation/CENTRAL_ENERGY_HEALTH_COUPLING.th.md`
- versioned coupling architecture if required
- Work 027 problem reports if required
- implementation queue, this plan, and matching bilingual result records

## Experiment Definition

- Independent variables: primary draw, regenerative return, brake heat, aerodynamic cooling, component heat generation, degradation/damage rates, reliability hazard, seed, and duration.
- Dependent variables: executed duration, energy stores, component temperatures, degradation, damage, failure flags, derating, residuals, and event candidates.
- Controls: start state, component IDs, thermal parameters, hazard law, random seed, draw index, event priority, and tolerances.
- Metrics: central energy residual, thermal residuals, event-time consistency, state-increment scaling, replay equality, and invalid-output count.
- Success criteria: typed transfers close; same-seed replay is exact; recovery never exceeds declared recovery; cooling is not double counted; earliest events truncate every candidate consistently; invalid audits write zero candidate signals.
- Failure criteria: energy appears or disappears without evidence; a later failure overrides an earlier one; thermal/degradation/damage advances beyond an event; stochastic draws depend on registration order; or failed evidence is silently corrected.
- Falsification attempt: inject hidden energy, excessive recovery, cooling over-credit, mismatched component IDs/times, exact event ties, different seeds, and a failure before the requested step end.

## Validation

1. Focused Work 027 tests.
2. Entire repository test suite.
3. Standalone Work 027 validator.
4. Python bytecode compilation.
5. `git diff --check` and `git diff --cached --check`.
6. Explicit staged-scope review before commit.

## Success Criteria

- Central energy and every configured component advance from declared typed evidence only.
- Conservation residuals pass and remain observable.
- Recovery, heat, cooling, derating, degradation, damage, and seeded reliability are represented.
- Earliest-event truncation is common to all affected state changes.
- English and Thai records agree on equations, units, commands, evidence, and limitations.
- Work 027 is committed as one validated commit before Work 028 starts.

## Risks

- Existing architecture separates energy and health candidates and may omit signals required for a consistent merge.
- Contact brake thermal state and central component thermal state can double count the same heat if ownership is unclear.
- Seeded reliability draws can become order-dependent without per-component deterministic streams.
- Thermal cooling evidence is a capacity and must not be treated as guaranteed rejected heat beyond the thermal law.

## Explicit Non-goals

- No whole-race loop or Work 028 telemetry orchestration.
- No calibrated reliability, material-fatigue, CFD cooling, battery chemistry, or physical-validation claim.
- No silent energy clipping, temperature clipping, failure clearing, or event-time correction.
- No vehicle optimization or ten-circuit campaign.
