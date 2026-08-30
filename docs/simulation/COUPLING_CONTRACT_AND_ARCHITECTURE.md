# Coupling Contract and Architecture

Thai companion: `COUPLING_CONTRACT_AND_ARCHITECTURE.th.md`

## Status and claim boundary

Work 021 implements the first executable central contract for the coupled-
vehicle program. It provides:

- an eight-stage deterministic coupling architecture compiler;
- explicit signal producer/consumer provenance;
- a versioned, fingerprinted experiment manifest;
- a topology-neutral shared vehicle state;
- a unit-aware residual ledger; and
- deterministic terminal-event arbitration.

The reference architecture declares how the existing Level-0 capability groups
must eventually exchange evidence. It does **not** call Work 011–019 physics
solvers, advance a coupled vehicle, produce a race time, or establish physical
validation. The Work 021 validator reports `physics_execution_count: 0`.

## Why this contract exists

Independent physics modules can each pass tests while still being coupled
incorrectly. Typical integration failures include using an aerodynamic result
from the wrong timestep, applying normal load after tyre force has already been
resolved, counting regenerative energy twice, allowing a module to overwrite
another module's signal, or updating only part of the shared state before a
failure.

Work 021 moves these errors into a fail-closed architecture boundary before the
actual adapter execution is implemented. Work 022 owns atomic execution and
state commit/rollback semantics.

## Canonical causal stages

The fixed stage order is:

| Index | Stage | Intended responsibility |
|---:|---|---|
| 0 | `inputs` | Pin current state, circuit/environment evidence, and strategy/control command. |
| 1 | `aerodynamics` | Produce aerodynamic force/moment and cooling evidence. |
| 2 | `load_balance` | Resolve chassis balance and contact normal loads. |
| 3 | `contact_limits` | Resolve tyre, suspension, braking, and recovery limits per contact. |
| 4 | `motion` | Produce one candidate longitudinal/lateral/yaw motion state. |
| 5 | `energy_audit` | Produce candidate energy state and conservation evidence. |
| 6 | `health` | Produce thermal/degradation/damage states and failure candidates. |
| 7 | `race_progress` | Reconcile candidates/residuals and produce the next shared state/race events. |

A module may consume only an initial signal or a signal produced by a strictly
earlier stage. Same-stage and later-stage dependencies are rejected. Multiple
modules may occupy a stage in future versions, but a signal still has exactly
one producer.

## Module and signal contract

Each `CoupledModuleSpec` declares:

```text
module_id
stage
model_version
consumes[]
produces[]
```

The compiler rejects:

- blank or duplicate module IDs;
- unknown or missing required stages;
- blank or duplicate signals inside one declaration;
- a module consuming and producing the same signal;
- an initial signal or produced signal with multiple producers;
- a consumed signal with no producer; and
- a dependency from the same or a later stage.

Input module order is not execution order. The compiler sorts by canonical
stage and module ID, sorts non-semantic signal sets for hashing, and generates a
SHA-256 architecture fingerprint. Reversing all module declarations and initial
signals produces an exactly equal compiled architecture.

## Reference architecture

`config/simulation/coupled_level0_architecture_v1.json` declares:

```text
input_bridge
  -> aerodynamic_map
  -> normal_load_solver
  -> contact_limit_solver
  -> vehicle_motion_solver
  -> energy_graph_audit
  -> health_event_solver
  -> race_progress_solver
```

It contains all eight required stages and 24 initial/produced signal identities.
Its compiled fingerprint is:

```text
51ca53e9d4c6058f67f61dc57f3ece7e8c24176d915e74069f27d0aa6999f8a6
```

The JSON loader requires an exact root/module key set and actual JSON string or
string-array types. It never converts numbers, booleans, or objects into signal
or module names. Unknown fields, missing fields, malformed JSON, and wrong types
fail with `CouplingContractError`.

The names map current capability boundaries; they are not executable adapters
yet. A `model_version` pin identifies intended source evidence but does not prove
that two modules already share a compatible payload.

## Experiment manifest

`ExperimentManifest` pins all identity required before a coupled evaluation:

- `experiment_id` and `candidate_id`;
- design-language version;
- one or more geometry artifact IDs and lowercase SHA-256 hashes;
- component-catalog version;
- circuit-profile ID;
- regulatory, energy, and solver profile versions;
- model-version pins;
- compiled architecture fingerprint;
- source commit;
- random seed;
- evaluation budget; and
- timestep in seconds.

Artifacts and model pins have unique IDs. Commit/hash syntax, positive budget,
integer seed, and finite positive timestep are enforced. The canonical manifest
fingerprint sorts artifact and model-pin identities, so declaration permutation
does not change experiment identity. Changing a meaningful field such as the
seed does change it.

The Work 021 reference manifest uses seed `17`, budget `1000`, timestep
`0.01 s`, and fingerprint:

```text
7f40394bf539ef230870a758cfba81c093268d38f52c7efac359fdd9ec5fb416
```

The manifest is an identity contract, not permission to self-report physical
properties. Geometry hashes must later point to independently evaluated
artifacts.

## Topology-neutral shared state

`SharedVehicleState` contains a minimal common runtime boundary:

- time and race distance;
- 3D position and velocity;
- yaw and yaw rate;
- remaining primary and recovered energy;
- completed laps;
- an arbitrary non-empty tuple of unique contact states;
- an arbitrary tuple of unique component-health states; and
- explicit running/terminal status.

Each contact has its own ID, normal load, longitudinal/lateral force, suspension
travel, and angular speed. Each component-health state has an ID, temperature,
degradation, damage, and failure latch. Inputs are finite and constrained where
physically required.

The contract accepts the validator's three-contact arrangement
`front/left/right`. It does not require four wheels, left/right pairs, axles,
symmetry, a conventional body, or a powertrain technology. These fields are a
shared evidence boundary; Work 022 must ensure adapters write only declared
candidate outputs and commit atomically.

## Residual ledger

`ResidualEntry` supports declared quantities and exact units:

| Quantity | Unit |
|---|---|
| `force` | `N` |
| `moment` | `N*m` |
| `energy` | `J` |
| `distance` | `m` |
| `time` | `s` |
| `state` | `1` |

The acceptance boundary is:

```text
tolerance = absolute_tolerance + relative_tolerance * scale
passed = abs(raw_residual) <= tolerance
```

The raw value is retained. `ResidualLedger.status` is `invalid` when any unique
entry fails and lists the exact failed residual IDs. The reference validator
retains `-2.0 J` and reports failed ID `energy`; it does not correct the value to
zero.

## Event arbitration

Each `EventCandidate` declares unique ID, type, non-negative candidate time, and
source module. The central tie priority is:

```text
finished
thermal_failure
reliability_failure
structural_failure
damage_failure
degradation_failure
energy_depletion
timeout
step_complete
```

The earliest time is found first. Candidates within declared
`time_tolerance_s` are a tie and use the priority above, followed by event ID as
a deterministic final key. The decision retains the true earliest time, all
tied candidate IDs, the winner, and the tolerance.

In the reference exact tie at `10.0 s`, `finished` wins over
`thermal_failure`. When thermal failure occurs at `9.9 s`, it wins because it is
not a tie. This is declared event semantics for the Level-0 integration program,
not a real sporting/safety regulation.

## Falsification evidence

The tests and validator demonstrate:

- exact replay of the loaded reference architecture;
- complete eight-stage coverage;
- architecture and manifest permutation invariance;
- deterministic SHA-256 identities;
- rejection of missing producer, duplicate producer/ID, missing stage, and
  same/later-stage dependency;
- rejection of extra/missing JSON keys, malformed JSON, wrong JSON types,
  invalid hashes/commits/budgets/timesteps, and duplicate version/artifact IDs;
- acceptance and exact replay of an arbitrary three-contact shared state;
- rejection of empty/duplicate contacts and invalid numeric/status values;
- observable passing/failing residuals and strict units; and
- deterministic event localization, tie priority, and duplicate-ID rejection.

## Limitations and next boundary

- No physics solver executes through this architecture yet.
- Signals currently carry identity/provenance names, not typed runtime payloads.
- No atomic start-state/output/next-state transaction exists yet.
- No adapter confirms that Work 011–019 units and timing semantics match this
  contract.
- No coupled force, moment, energy, thermal, or race residual has been measured.
- The reference topology is an integration control, not a mandatory design.
- Work 022 must implement adapter protocol, declared read/write sets, atomic
  step transaction, rollback on invalidity, and partial-write rejection.
- Level-0 contract success is not physical validation, safety,
  manufacturability, technology discovery, or real-race evidence.
