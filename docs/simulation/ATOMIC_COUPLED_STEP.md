# Atomic Coupled-Step Transaction

Thai companion: `ATOMIC_COUPLED_STEP.th.md`

## Status and claim boundary

Work 022 implements the generic execution boundary between the Work 021
architecture and future domain adapters. It can execute eight registered
adapters in causal order and publish one complete next-state transaction.

The reference validator uses placeholder payloads and reports
`domain_physics_adapter_count: 0`. A committed reference step therefore proves
transaction behavior only. It does not prove that circuit, aerodynamic,
contact, motion, energy, thermal, health, or race physics are coupled correctly.

## Transaction flow

```text
compiled architecture + immutable start state
              + exact initial signals + exact adapter set
                               |
                           preflight
                               |
                    private candidate signal bus
                               |
       adapters execute in compiled stage/module order
                               |
        validate identity, version, reads, writes, evidence
                               |
              validate complete monotonic state.next
                    /                          \
          publish all outputs             publish none
          + committed state               + failure/evidence
```

Registration order is not execution order. Adapter tuples may be permuted; the
compiled architecture always controls execution.

## Runtime signals and read isolation

`RuntimeSignal` stores a deep-copied payload snapshot. Its `value` property and
the adapter `read()` operation return new copies, preventing ordinary adapters
from sharing mutable references with the caller or candidate bus.

`AdapterReadView` contains only the signals listed in the current module's
`consumes` declaration. Reading any other ID raises `CoupledTransactionError`.
The immutable `SharedVehicleState` is also supplied as the common start-state
identity. This is a trusted-code contract, not a hostile Python sandbox.

## Preflight gate

Before the first adapter executes, `execute_coupled_step` requires:

- exact initial-signal coverage, with no missing, extra, or duplicate IDs;
- a `manifest.current_state` payload equal to the explicit `start_state`;
- exact adapter coverage, with no missing, extra, or duplicate module IDs; and
- every adapter `model_version` equal to its compiled module pin.

A preflight failure produces an invalid result with zero traces and zero
published signals. No adapter is called.

## Adapter contract

Each adapter declares `module_id`, `model_version`, and `execute(view)`. A
successful `AdapterOutput` must:

- identify the module being executed;
- use status `ok`;
- write every declared `produces` signal exactly once and no other signal;
- use unique residual and event IDs; and
- contain no failure reason.

An adapter may instead return status `invalid`, a nonblank reason, evidence, and
zero candidate writes. Invalid outputs are terminal for the step. Returning
writes with invalid status is itself a protocol violation.

Exceptions, non-`AdapterOutput` values, wrong module identity, and malformed
write sets become observable `adapter_exception` failures. Execution stops at
the failing module.

## Evidence retention

`CoupledStepResult` retains:

- ordered `AdapterTrace` records;
- raw `ResidualEntry` records including value, unit, scale, and tolerance; and
- raw `EventCandidate` records.

Evidence produced through the stopping module remains available after rollback.
Residual/event IDs must be globally unique across the step. A failed residual
returns `residual_failure` and its exact raw value; it is never corrected.
Evidence retention is separate from state publication, so an invalid result
still has an empty `published_signals` collection.

## Atomic commit and rollback

All successful adapter outputs remain in a private candidate bus until the last
module completes. `state.next` must exist, contain `SharedVehicleState`, and
must not regress `time_s` or `race_distance_m`.

Only then does the result expose:

- status `committed`;
- the one complete `committed_state`;
- all 21 reference produced signals; and
- all traces and evidence.

Every invalid result exposes:

- status `invalid`;
- a structured failure code/reason/module;
- `committed_state = None`;
- `published_signals = ()`; and
- `rolled_back_state` equal to the exact start state.

No state is mutated in place and no earlier candidate signal is published after
a later failure.

## Failure codes

The implemented boundary reports explicit codes including:

- `initial_signal_coverage`
- `current_state_signal_missing`
- `current_state_mismatch`
- `adapter_coverage`
- `adapter_version_mismatch`
- `adapter_exception`
- `adapter_invalid`
- `evidence_identity_duplicate`
- `residual_failure`
- `next_state_missing`
- `next_state_type`
- `time_regression`
- `distance_regression`

## Validation evidence

The deterministic reference executes:

```text
input_bridge -> aerodynamic_map -> normal_load_solver
-> contact_limit_solver -> vehicle_motion_solver
-> energy_graph_audit -> health_event_solver
-> race_progress_solver
```

It advances the placeholder state from `4.0 s` to `4.01 s` and from `100.0 m`
to `100.3 m`, publishes 21 outputs only after all eight traces pass, and replays
exactly when adapter and initial-signal registration are reversed.

Falsification covers preflight failure, undeclared reads, missing/extra writes,
wrong identity/version/return type, invalid adapter output, failed residual,
exception, invalid write on failure, wrong next-state type, time regression,
and distance regression. Every injected invalidity retains the start state and
publishes zero signals.

## Limitations and next boundary

- Payload identities and atomicity are enforced, but domain units and semantics
  are not yet supplied by real adapters.
- Deep-copy isolation may be inappropriate for very large future arrays; any
  zero-copy replacement must preserve the same immutability evidence.
- Monotonic time/distance is necessary but not sufficient for valid motion.
- Work 023 must implement typed deterministic circuit, environment, weather,
  traffic, and strategy inputs for all ten circuit profiles.
- Level-0 transaction success is not physical validation, safety,
  manufacturability, discovery, or race superiority.
