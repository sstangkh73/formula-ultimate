# Whole-Race Coupled Orchestrator

Status: Work 028 reference implementation

Thai companion: `WHOLE_RACE_COUPLED_ORCHESTRATOR.th.md`

## Purpose

Work 028 supplies the missing loop around the atomic coupled-step transaction. It executes a declared Level-0 vehicle configuration until a terminal race outcome and retains enough identity and numerical evidence to replay or reject the run.

This is an integration and selection gate. It is not a calibrated real-circuit simulator or physical validation.

## Architecture v4

`config/simulation/coupled_level0_architecture_v4.json` declares eight ordered stages:

1. `input_bridge`
2. `aerodynamic_map`
3. `normal_load_solver`
4. `contact_limit_solver`
5. `vehicle_motion_solver`
6. `energy_graph_audit`
7. `health_event_solver`
8. `race_progress_solver`

The v4 change routes `state.current` into the race-progress stage and versions that stage as `work028-race-progress-v1`. Earlier architecture files remain unchanged for replay compatibility.

Adapter registration order does not define execution order. The compiled architecture does.

## Race Loop

For each attempted step, `run_whole_race`:

1. rejects an already terminal initial state;
2. limits requested duration by the remaining race timeout;
3. resolves typed circuit, spatial, weather, traffic, state, and strategy inputs;
4. constructs duration-dependent adapters from the committed state;
5. executes one atomic transaction;
6. records traces, residuals, events, published signals, fingerprints, and start/end state identities;
7. advances only when the transaction commits; and
8. stops on finish, depletion, physical failure, timeout, invalidity, or evaluation-budget exhaustion.

An invalid transaction retains its attempted telemetry but has no end-state fingerprint and cannot partially advance the committed race state.

## Race-Progress Merge

The race-progress adapter reads the current, motion, energy, and health candidates plus upstream residual evidence. It adds finish, timeout, and step-complete candidates, then uses the common deterministic event arbitrator.

The committed candidate is localized to the winning event time. Finish distance is set exactly to the declared target. Terminal status is one of:

- `finished`
- `depleted`
- `failed`
- `timeout`
- `invalid`

Exact-time ties remain visible in the event ledger. The common event priority decides the committed status; a finish/depletion tie therefore keeps both events while committing the declared winner consistently.

## Observable Evidence

Each `CoupledRaceStepTelemetry` record contains:

- step index and requested duration;
- transaction status and failure detail;
- scenario/input fingerprint;
- start and optional end state SHA-256 identities;
- time, distance, and primary-energy boundaries;
- published signal IDs;
- all adapter traces;
- owned residual entries; and
- terminal/event candidates published by the transaction.

`CoupledRaceReplayMetadata` pins the architecture fingerprint, ordered model versions, seed, evaluation budget, timestep, initial/final states, scenario fingerprints, and attempted/committed step counts. `WholeRaceResult` also has a fingerprint over outcome, final state, telemetry, and replay metadata.

Residual identity ownership is exclusive. The energy adapter publishes `energy.*`; the health adapter may retain truncated energy evidence internally but publishes only `health.*`; race progress publishes `race.*`.

## Analytical Reference and Falsification

The controlled reference uses a fixed four-contact vehicle, zero aerodynamic coefficients, a straight analytical corridor, constant `10 m/s` initial motion, no drive/brake request, and a `30 m` target. It finishes in three committed one-second steps with zero finish-distance residual.

The falsification matrix includes:

- low primary energy plus auxiliary draw, localized to depletion at `0.5 s`;
- excessive central heat, localized to failure at `0.2 s`;
- timeout inside a step at `1.5 s`;
- corridor invalidity with no committed next state;
- missing adapter coverage and transaction rollback;
- evaluation-budget exhaustion;
- exact finish/depletion tie; and
- reversed adapter registration and same-seed replay.

## Invariants

- Only `state.next` from a successful complete transaction advances the race.
- A terminal state is never stepped again.
- Scenario race distance must equal the shared start-state race distance within `1e-9 m`.
- Energy depletion at the exact requested step end remains an observable event.
- Residual IDs are unique within one transaction.
- Same inputs, versions, seed, and architecture replay exactly.
- Registration permutation cannot change the compiled execution result.

## Limitations and Claim Boundary

The reference is intentionally analytical. It does not yet execute measured spatial/weather evidence across the ten real circuit profiles, optimize strategy, calibrate tyre/aero/thermal/reliability models, model full 3D contact, prove numerical convergence, or compare topology-search candidates fairly. Those gaps prevent claims of real-race pace, safety, manufacturability, discovered technology, or physical validity.

Work 029 must construct the controlled ten-circuit baseline campaign. Work 030 must attempt integrated falsification, refinement, uncertainty review, and cross-model promotion before autonomous candidates can advance beyond this Level-0 gate.
