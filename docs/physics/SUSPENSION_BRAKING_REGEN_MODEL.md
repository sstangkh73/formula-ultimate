# Suspension, Mechanical Braking, and Regeneration Model

Thai companion: `SUSPENSION_BRAKING_REGEN_MODEL.th.md`

## Status and claim boundary

Work 018 implements `work018-suspension-braking-v1`, a deterministic Level-0
interval evaluator for one independently declared ground-contact suspension and
brake module. It couples normal load, reduced-order suspension travel,
tyre-limited regen/mechanical brake torque, recovered-energy storage, brake
heat, Work 014 thermal derating/failure, and event truncation.

It is not a detailed linkage, tyre, hydraulic, inverter, battery, ABS, whole-
vehicle stopping-distance, safety, or physical-validation model.

## Topology and upstream-load boundary

The API evaluates one identified module and does not prescribe wheel count,
paired axles, left/right symmetry, or a conventional vehicle layout. A candidate
may instantiate any number and arrangement of modules.

`normal_load_n` is an explicit interval input. It may come from Work 016 plus a
future Work 017 aerodynamic-load coupling, but Work 018 does not invent,
redistribute, or silently correct that load. The current tyre ceiling is purely
longitudinal `mu*Fz`; lateral force consumption is not yet coupled.

## Suspension state and force

Suspension travel `x` is positive in compression and negative in rebound. The
valid envelope is:

```text
-maximum_rebound <= x <= maximum_compression
```

At the interval start:

```text
F_suspension = preload + k*x0 + c*v0
a_travel     = (F_normal - F_suspension) / m_effective
x(t)         = x0 + v0*t + 0.5*a_travel*t^2
v(t)         = v0 + a_travel*t
```

Force and acceleration remain constant during one interval. The result exposes
the force residual:

```text
m_effective*a_travel - (F_normal - F_suspension)
```

The evaluator solves linear/quadratic roots for both travel boundaries and
accepts only an outward crossing. The earliest valid crossing terminates the
interval at the analytical time, latches suspension failure, retains the
boundary travel, and leaves the remaining requested time unexecuted. Travel is
never silently clipped back inside the envelope.

## Brake torque allocation

All requested torque values are non-negative braking magnitudes. The contact
ceiling is:

```text
T_tyre_limit = mu * F_normal * effective_radius
```

At wheel speed `omega` above the declared minimum, regen capacity is the
minimum of:

```text
T_regen_component = maximum_regen_torque
T_regen_generator = maximum_generator_input_power / omega
T_regen_charge    = maximum_storage_charge_power /
                    (conversion_efficiency * omega)
T_regen_storage   = remaining_storage_energy /
                    (conversion_efficiency * omega * requested_duration)
```

At zero or below-minimum speed, regen capacity is zero. The declared control
policy allocates regen first and mechanical braking second. Mechanical capacity
is `maximum_mechanical_torque * Work014_start_derating`.

The tyre ceiling applies one common scale to both allocated paths. This
preserves the requested blend rather than silently replacing a saturated path
with another. Requested torque that cannot be applied remains explicit as
`unserved_brake_torque_n_m`. A separate torque residual checks:

```text
T_requested - T_applied_total - T_unserved = 0
```

## Energy and storage accounting

Allocated torques are fixed at the interval start. If an event truncates the
interval, energy is integrated only through executed duration `dt_exec`:

```text
E_regen_wheel = T_regen_applied * omega * dt_exec
E_stored      = efficiency * E_regen_wheel
E_regen_loss  = E_regen_wheel - E_stored
E_mech_heat   = T_mechanical_applied * omega * dt_exec
E_removed     = (T_regen_applied + T_mechanical_applied) * omega * dt_exec
```

The independently observable energy residual is:

```text
E_removed - E_stored - E_regen_loss - E_mech_heat
```

Recovered energy increases only `stored_recovered_energy_j`, never above its
declared capacity. It is conserved vehicle wheel work with explicit loss, not
free energy and not replenishment of undeclared primary propulsion energy.

The storage-capacity torque limit is calculated over the requested interval.
When a failure truncates the interval, the model does not re-optimize torque to
fill the newly unused storage capacity; the start-of-step command stays fixed.

## Brake heat and failure

Mechanical braking power is:

```text
P_mechanical_heat = T_mechanical_applied * omega
```

This power enters the Work 014 lumped thermal model with declared ambient and
active-cooling command. Work 014 supplies temperature integration, derating,
energy residual, exact overtemperature crossing, and latched failure.

The evaluator first obtains candidate suspension and brake-temperature event
times over the requested interval. The earliest event sets `dt_exec`. An exact
tie returns `simultaneous`. Final suspension, brake temperature, storage, and
all energy terms are evaluated only through `dt_exec`. A previously latched
suspension or brake failure returns `already_failed` with zero execution.

## Result states

- `status=ok`, `failure_mode=none`: the requested interval completes.
- `status=failed`, `failure_mode=suspension_travel`: travel limit crosses first.
- `status=failed`, `failure_mode=brake_overtemperature`: thermal limit crosses
  first.
- `status=failed`, `failure_mode=simultaneous`: exact candidate-time tie.
- `status=failed`, `failure_mode=already_failed`: failure was latched at entry.
- `status=invalid`: cross-contract, non-finite runtime, capacity, or energy-
  residual failure; state is unchanged.

## Reference evidence

`scripts/validate_suspension_braking.py` checks:

- `150 N*m` request allocates `100 N*m` regen and `50 N*m` mechanical;
- at `10 rad/s` for `1 s`, `1500 J` wheel energy becomes `800 J` stored,
  `200 J` conversion loss, and `500 J` brake heat with zero residual;
- suspension reaches `0.1 m` at exactly `5 s` and leaves `5 s` unexecuted;
- adiabatic brake heating reaches `400 K` at exactly `50 s`, producing
  `50000 J` mechanical heat and leaving `50 s` unexecuted;
- `mu=1`, `Fz=100 N`, `R=0.3 m` caps torque at `30 N*m`, preserves scale `0.2`,
  and exposes `120 N*m` unserved; and
- identical inputs replay exactly.

The unit suite additionally checks constant-acceleration suspension motion,
every regen torque/power/charge/storage limit, zero-speed regen, thermal
derating, simultaneous travel/thermal failure, already-failed state, invalid
contracts, and runtime non-finite output.

## Current integration boundary

Work 018 exposes typed per-contact load, torque, energy, thermal, and failure
evidence. It is not yet integrated into Work 015 race state or a multi-contact
vehicle controller. Shared central storage allocation, combined lateral tyre
capacity, wheel-speed dynamics, and stopping distance require an explicitly
planned later coupling experiment.

## Limitations and follow-up

- Suspension is one constant-acceleration contact coordinate, not coupled
  heave/pitch/roll, linkage kinematics, anti-geometry, compliance, or road input.
- Wheel speed is constant inside an interval; brake torque does not yet update
  vehicle or wheel angular speed.
- Regen-first is a declared policy, not an optimized race strategy.
- Thermal behavior is lumped and uncalibrated; brake temperature passing is not
  braking-safety evidence.
- Work 019 owns reliability, traffic, weather, degradation, and race strategy.
