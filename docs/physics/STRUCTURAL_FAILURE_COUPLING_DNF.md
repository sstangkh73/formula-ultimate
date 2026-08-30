# Structural Failure Coupling and DNF

Thai companion: `STRUCTURAL_FAILURE_COUPLING_DNF.th.md`

## Claim and outcome

Work 046 validates a deterministic structural connection-state and failure-coupling policy inside the narrow numerical domain admitted by Work 051. It supports typed `intact -> degraded -> failed` transitions, localized failure events, zero post-failure wrench, redundant redistribution, failure-energy accounting, critical-path `DNF`, race-event arbitration, and exact replay.

It does not validate real fracture dynamics, crack propagation, fatigue crack growth, contact separation, stress waves, impact, crash energy, occupant safety, or arbitrary joints.

## Admitted evidence identity

Every evaluation must match all of:

- remediation protocol `gate_a_remediation_v1` with decision `narrowly_bounded`;
- element route `C3D10_precritical_v1`;
- support topology SHA-256 `7f4444a78af66157f04441b38e4d4bc3225a892b29f90ebf9840279694fb6258`;
- boundary model `bonded_cylindrical_surface_zero_displacement_v1`;
- yield protocol `yield_plasticity_acceptance_v1`;
- fracture protocol `fracture_initiation_acceptance_v1`;
- fatigue protocol `fatigue_damage_acceptance_v1`.

Any identity mismatch returns `invalid` with no candidate connection state.

## State and load-path policy

The Work 046 bounded fixture has one declared load-path group. Intact and degraded connections carry the applied six-component wrench in proportion to declared positive share weights. Yield evidence changes `intact -> degraded`. Fracture or fatigue evidence changes the connection to `failed` and forces its transmitted wrench to exact zero.

After failure, surviving connections receive a fresh deterministic share. If at least one survivor remains, force and moment closure are audited. If no survivor remains in the required path, the network outcome is `DNF`; applied-load closure is then unavailable rather than silently fabricated.

## Failure-energy policy

For every connection that fails at the localized event:

```text
U_stored = U_dissipated + U_released + residual
U_dissipated = fraction * U_stored
U_released = (1 - fraction) * U_stored
```

The fixture used `12 J` stored energy and a dissipated fraction of `0.7`, producing `8.399999999999999 J` dissipated, `3.6000000000000005 J` released, and an observable floating-point residual of `8.881784197001252e-16 J`. The residual passed the frozen tolerance; it was not overwritten with zero.

This ledger does not model where released energy travels. It prevents energy erasure at the coupling boundary only.

## Experiment and results

The applied wrench was:

```text
force  = (1000, 50, -20) N
moment = (10, 5, -3) N*m
```

`joint_a` yielded at `0.2 s` and fractured at `0.375 s`. Timestep runs at `0.5`, `0.25`, and `0.125 s` all localized the fracture at exactly `0.375 s`; maximum relative event-time change was `0`, below `1e-6`.

In the redundant fixture, `joint_a` transmitted `(0,0,0,0,0,0)` after failure and `joint_b` carried the complete applied wrench. The maximum raw wrench/energy residual magnitude was `8.881784197001252e-16`. The outcome remained `running`.

In the critical fixture, `joint_a` was the only path. Its failure produced exact zero wrench and deterministic `DNF` for every timestep.

Same-input replay was exact. Five negative controls rejected out-of-domain Gate A identity, unknown connection identity, upstream protocol mismatch, an event preceding the current state, and an invalid energy partition.

## Race arbitration

`structural_failure` is a typed central event after `reliability_failure` and before `damage_failure`. Exact-time finish/structural ties retain both candidates and the existing `finished` priority wins. A structural event occurring earlier than finish wins and maps the shared race state to `failed`/structural `DNF` semantics.

This is deterministic Level-0 policy, not a sporting or safety regulation.

## Falsification assessment

Supporting evidence is exact event-time refinement, exact failed-wrench zero, redundant force/moment closure, retained energy residual, critical `DNF`, same-input replay, and fail-closed controls.

Contradicting evidence is that redistribution is instantaneous and the Gate A identity is narrow. A real compliant joint may redistribute through stress waves, slip, contact, plasticity, or progressive fracture. Missing evidence includes physical joint tests, calibrated material records, contact/preload/friction, transient dynamics, post-critical behavior, impact, and crash response.

Confidence is high for the implemented policy mechanics and low for real failure dynamics.

## Reproduction

```powershell
.\scripts\run_work046.ps1
py -3.14 -m unittest tests.test_structural_failure_coupling tests.test_coupling_contracts tests.test_whole_race -q
py -3.14 -m unittest discover -s tests -q
```

Machine-readable evidence is under `artifacts/work046/` and is intentionally ignored by Git. A clean-tree replay is required after commit.
