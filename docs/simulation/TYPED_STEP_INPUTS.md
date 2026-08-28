# Typed Circuit and Environment Step Inputs

Thai companion: `TYPED_STEP_INPUTS.th.md`

## Status and claim boundary

Work 023 defines the typed evidence entering the first `inputs` stage of the
coupled architecture. It resolves all ten real-circuit catalog profiles
deterministically and connects complete scenarios to the Work 022 atomic
adapter protocol.

The catalog does not contain surveyed local corridor geometry, event-time
weather, or a traffic scenario. All ten catalog-only resolutions are therefore
`incomplete`; the validator reports `real_physics_ready_profile_count: 0`.
This is deliberate evidence, not a failed attempt to invent neutral conditions.

## Typed records

`SpatialStepEvidence` declares circuit and segment identity, source, curvature
in `1/m`, grade/bank in radians, left/right width in metres, and horizontal
uncertainty in metres. Status is either `available` with every SI field present,
or `missing` with a reason and no numeric values.

`WeatherStepEvidence` declares source, air and track temperature in kelvin,
pressure in pascals, relative humidity in `[0,1]`, 3D wind velocity in `m/s`,
and precipitation mass flux in `kg/(m^2*s)`. Status is `observed` with every
field present or `missing` with no numeric defaults.

`TrafficStepEvidence` distinguishes:

- `isolated_control`: an explicit zero-nearby-vehicle experiment;
- `observed`: a sourced non-negative nearby-vehicle count; and
- `missing`: unknown traffic, never interpreted as zero.

`StrategyStepCommand` carries throttle, brake, and recovery fractions in
`[0,1]` plus normalized steering request in `[-1,1]`.

## Scenario resolution and identity

`CircuitInputScenario` binds one immutable `CircuitProfile`, race distance, and
matching spatial/weather/traffic evidence. Cross-circuit evidence and distance
outside `[0, race_distance_m]` are rejected.

`resolve_step_inputs` returns `ready` only when spatial and weather evidence are
present and traffic is explicitly observed or isolated. Otherwise it returns
`incomplete` with an ordered `missing_evidence` tuple.

The SHA-256 fingerprint includes the complete circuit profile, nested source
evidence and access dates, race distance, all three evidence records, and the
strategy command. Reordering the ten profiles does not change per-circuit
fingerprints. Changing profile content under the same ID does change the hash.

## Input adapter

`CircuitEnvironmentInputAdapter` implements the compiled `input_bridge`
identity and reads:

```text
manifest.circuit_profile   -> CircuitInputScenario
manifest.current_state     -> SharedVehicleState
manifest.strategy_command  -> StrategyStepCommand
```

A ready scenario emits exactly:

```text
circuit.segment_inputs     -> SpatialStepEvidence
control.step_command       -> StrategyStepCommand
environment.step_inputs    -> EnvironmentStepInputs(weather, traffic)
state.current              -> SharedVehicleState
```

An incomplete or wrong-typed scenario returns `AdapterOutput(status="invalid")`
with a reason and zero writes. Work 022 then rolls back the whole step.

## Ten-circuit evidence result

The versioned catalog contains Monaco, Monza, Spa, Singapore, Suzuka,
Silverstone, Hungaroring, Mexico City, Bahrain, and Sao Paulo. Each resolves
deterministically, but each currently reports exactly:

```text
missing_evidence = ("spatial", "weather", "traffic")
status = "incomplete"
```

Circuit-level lap length, race distance, turns, width evidence, altitude, and
design pressure are not substitutes for a local segment corridor or event-time
conditions.

## Analytical fixture

One complete analytical fixture supplies explicit geometry, observed weather,
and `isolated_control` traffic. It resolves `ready` and emits all four typed
signals. It validates the contract only; its geometry/weather are not assigned
to a real race claim.

## Falsification and limitations

Tests reject cross-circuit evidence, non-finite/out-of-range values, missing
records carrying neutral zeros, unknown traffic interpreted as isolated,
out-of-race distance, and wrong adapter payload types. They also prove replay,
profile-content fingerprint sensitivity, and zero writes on incomplete input.

Work 024 may consume only ready typed inputs to couple aerodynamic force and
cooling evidence into chassis force/moment and normal loads. Work 023 does not
execute aero or vehicle physics and is not physical validation, safety,
manufacturability, discovery, or race-performance evidence.
