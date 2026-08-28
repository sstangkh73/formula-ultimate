# Digital Race Reliability and Strategy Model

Thai companion: `DIGITAL_RACE_RELIABILITY_STRATEGY_MODEL.th.md`

## Status and claim boundary

Work 019 implements `digital-race-level0-v1`, a deterministic multi-lap,
multi-sector race gate with explicit per-lap pace commands, event-local weather
and traffic, degradation, damage, onboard primary energy, seeded reliability,
and terminal-event localization.

It is a Level-0 strategy and failure-selection model. It is not calibrated
reliability, real lap-time prediction, coupled vehicle physics, safety evidence,
or physical validation. A candidate that passes still requires higher-fidelity
coupling and empirical evidence.

## Topology-neutral contract

The model never prescribes body shape, wheel count, axle layout, engine type,
energy technology, fastener type, or component topology. A scenario supplies an
ordered set of abstract sectors whose `lap_fraction` values must sum to one.
Each sector declares SI base speed, onboard energy per distance, degradation per
distance, and damage per distance.

This abstraction lets a free-topology candidate publish its own reduced-order
sector evidence while comparing it against the same circuit, sector contract,
strategy schedule, environmental schedule, seed, and finish gate.

## Real-circuit distance and event order

For every real `CircuitProfile`, the model traverses:

```text
published race_laps * declared sectors_per_lap
```

Ordinary event distance is:

```text
d_nominal = published lap_length * sector lap_fraction
```

Published lap lengths are rounded and the race start may be offset from the
finish. The existing circuit profile exposes:

```text
d_offset = published race_distance - lap_length * race_laps
```

Rather than silently changing every lap, Work 019 sets the last event distance
to the remaining published race distance. Its
`official_distance_adjustment_m` records the difference from the nominal final
sector. All prior event adjustments remain zero. The final state is the exact
published target, while the adjustment remains auditable.

## Strategy, environment, and degradation equations

For event distance `d`, start degradation `g`, base sector speed `v0`, lap pace
`p`, weather multipliers `w`, traffic multipliers `q`, and speed-loss coefficient
`k_v`:

```text
degradation_speed_factor = 1 - k_v*g
v_travel = v0 * p * w_speed * q_speed * degradation_speed_factor
t_request = d / v_travel + t_traffic

E_drive = d * e0 * p^2 * w_energy * q_energy
E_source = E_drive + P_aux * t_request

delta_g = d * r_g * p^2 * w_degradation * q_degradation
delta_D = d * r_D * p^3 * w_damage * q_damage
```

One command is required for every published lap. A missing or extra command,
duplicate schedule key, out-of-range event, non-positive multiplier, or sector
fraction mismatch fails before execution.

Traffic delay is a declared reduced-order event penalty. For localization,
progress, drive energy, degradation, and damage are distributed uniformly over
the combined travel-plus-delay duration. This is not a microscopic queue or
overtaking model. A weather or traffic event affects exactly its declared
zero-based `(lap_index, sector_index)`; unspecified keys use neutral conditions.

## Seeded reliability uncertainty

The start-of-event hazard rate is:

```text
lambda = lambda0
       * w_reliability
       * q_reliability
       * p^n
       * (1 + k_g*g + k_D*D)
```

Exactly one pseudorandom draw is consumed for every entered event:

```text
u ~ Uniform[0, 1)
t_reliability = -ln(1 - u) / lambda
```

For zero hazard the candidate time is absent, but the draw is still recorded so
event count and random-stream position are deterministic. Replay metadata keeps
model/circuit/layout/scenario/vehicle/strategy identity, all pace values,
weather and traffic keys/identities, seed, entered events, and draw count.

These declared hazards are scenario parameters. Seeded repeatability makes an
uncertain experiment auditable; it does not calibrate or validate real failure
probability.

## Event localization and priority

All rates are constant within one event. Candidate times are solved
analytically for:

- final published-distance completion;
- seeded reliability failure;
- damage limit;
- degradation limit;
- onboard-energy depletion; and
- global timeout.

The earliest candidate truncates time, distance, energy, degradation, and
damage together. Within the declared `event_time_tolerance_s`, a final finish
wins a tie, then reliability, damage, degradation, depletion, and timeout. At a
non-final sector boundary, any terminal candidate at or before the boundary
wins; otherwise the event completes and the next sector begins.

Terminal outcomes are:

- `finished`, `failure_mode=none`;
- `failed`, `failure_mode=reliability|damage|degradation`;
- `depleted`, `failure_mode=energy`;
- `timeout`, `failure_mode=timeout`; or
- `invalid`, `failure_mode=numerical`.

Hard-limit events retain the analytically localized boundary. Runtime overflow,
non-finite rates, non-positive effective speed, event ordering that overspends
energy beyond tolerance, and residual failure become observable `invalid`
results rather than silent correction.

## Energy and residual evidence

The model has no refuelling or external primary-energy input. Executed source
energy is:

```text
E_used = E_drive_requested * executed_fraction + P_aux * t_executed
E_remaining_next = E_remaining_start - E_used
```

Every event records:

```text
distance residual = d_end - d_start - d_executed
energy residual   = E_start - E_used - E_end
```

Energy is monotonic non-increasing. A sub-tolerance negative boundary caused by
floating-point event localization may be set to zero only while its raw value
remains in `energy_boundary_residual_j`. Larger overspend invalidates the race.
The result also retains a direct terminal reconciliation residual instead of
rounding it away.

## Reference evidence

`scripts/validate_digital_race.py` demonstrates:

- all ten real circuit profiles finish at zero distance residual with their
  exact lap/event counts and observable final distance adjustment;
- repeated runs with the same seed are exactly equal;
- onboard energy never increases and no replenishment event exists;
- pace `1.2` finishes the Monaco reference in `2410.1454516951667 s`, faster
  than pace `0.8` at `3615.1432624331906 s`, but consumes more energy and
  accumulates more degradation and damage;
- a declared `7.5 s` traffic penalty increases total time by approximately
  `7.5 s`;
- one wet event increases time by `3.178249263393809 s` and energy by
  `133480 J` relative to neutral conditions;
- reliability seed `23`, draw `0.9248652516259452`, and hazard `1 /s` produce
  the analytical and simulated failure time `2.5884721324944864 s`; and
- depletion, degradation, damage, timeout, and numerical invalidity each return
  their distinct expected outcome/failure mode.

Unit tests additionally cover exact seeded replay, two-seed uncertainty,
official-distance residual placement, final finish/depletion tie priority,
scale-aware energy closure, invalid contracts, and localized hard limits.

## Falsification and interpretation

The preferred hypothesis is only conditionally supported: an aggressive pace
is faster in the reference but measurably costs energy, degradation, damage,
and hazard. The test suite actively forces each non-finish outcome, so a fast
partial run cannot be ranked as a successful race.

Alternative explanations remain. The outcome could change under sector rates
derived from higher-fidelity aerodynamics, tyre, thermal, suspension, braking,
energy-graph, and traffic models. Therefore the Work 019 result ranks only
candidates that finish this declared Level-0 experiment; it does not establish
that the preferred strategy or design is superior in reality.

## Current integration boundary and limitations

- Work 019 consumes abstract sector coefficients; it does not yet time-step the
  Work 011–018 tyre, energy, thermal, lateral, aerodynamic, or suspension models
  together.
- Degradation and damage are scalar linear states rather than component-level
  failure mechanisms, wear maps, fatigue, corrosion, or collision physics.
- Reliability hazard is constant within each event and uncalibrated.
- Weather has no spatial field, rainfall evolution, surface water, wind vector,
  temperature coupling, or forecast uncertainty.
- Traffic is an event multiplier/delay, not multiple interacting vehicles,
  overtaking, flags, safety car, pit lane, or race control.
- Strategy controls pace only. There is no refuelling, pit repair, energy
  replenishment, tyre change, or tactical opponent AI.
- The official-distance adjustment is bookkeeping evidence, not surveyed
  start/finish-line geometry.
- Passing this model is never by itself physical validation, safety evidence,
  manufacturability evidence, or proof of real-world race superiority.
