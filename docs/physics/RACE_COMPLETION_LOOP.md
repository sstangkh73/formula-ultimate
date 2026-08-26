# Deterministic Full-Race Completion Loop

Status: Implemented for Work 015

Thai companion: `RACE_COMPLETION_LOOP.th.md`

## Purpose and evidence boundary

Work 015 answers a necessary question: does a candidate finish the published
race distance before onboard energy, thermal failure, timeout, or numerical
invalidity terminates it? It does not calculate a credible lap time. Each real
circuit is reduced to total race distance and reference air density; geometry,
cornering, braking, traffic, weather, and strategy are absent.

The ten-circuit finish fixture deliberately uses a sufficient, simplified
vehicle budget to verify loop behavior. Its roughly `228–248 s` results are
analytical software fixtures, not predictions or performance claims.

## State and onboard-energy contract

State contains elapsed time (`s`), distance (`m`), speed (`m/s`), remaining
onboard energy (`J`), and Work 014 thermal state. No API adds energy during the
race. Start-of-step temperature sets the derating factor and applied force:

```text
F_applied = F_commanded * thermal_derating_factor
E_wheel = F_applied * delta_x
E_source = E_wheel + P_waste_heat*delta_t + P_auxiliary*delta_t
E_remaining_next = E_remaining - E_source
```

Waste heat is charged to the source and supplied to Work 014. Auxiliary power
is charged but not thermally resolved. Per-step source terms and accounting
residual remain visible.

## Terminal outcomes

| Outcome | Meaning |
|---|---|
| `finished` | Published `race_distance_m` crossed |
| `depleted` | Onboard energy prevents completion of the next interval |
| `timeout` | Declared time limit reached before finish |
| `failed` | Thermal failure occurs or is already latched |
| `invalid` | Runtime numerical physics cannot produce a finite valid state |

Finish/depletion events use fixed-iteration bisection over the same motion
solver. Thermal failure uses Work 014's analytical event time. The earliest
event wins; exact-time priority is `finished`, `failed`, `depleted`, `timeout`.

## Numerical event-boundary evidence

Work 015 found and resolved a real numerical problem documented in
`docs/problem_reports/2026-08-26_015_event-tie-energy-overspend.md`. An exact
finish/depletion/timeout tie produced an upper-bound energy deficit of
`-0.000244140625 J` on a `1354976035920.0 J` scale.

Race controls now declare absolute/relative energy-event tolerances (`1e-6 J`
and `1e-12` defaults), preserved in replay metadata. If a higher-priority finish
or failure has a negative raw boundary residual within scaled tolerance,
remaining usable energy becomes zero while the signed residual remains visible
in step and terminal output. Beyond tolerance the run is `invalid`. This is not
energy replenishment.

## Deterministic replay

Replay metadata records schema/model versions, circuit/layout, vehicle ID,
fixed time step, timeout, seed, bisection iterations, and energy tolerances. The
current loop makes zero stochastic draws. Repeating all ten profiles produces
exact dataclass equality.

Run:

```powershell
python scripts/validate_race.py
python -m unittest tests.test_race -v
```

## Limitations and follow-up

- Total-distance point mass omits the circuit corridor, sectors, curvature,
  braking, grade distribution, tyre capacity, and driver/controller decisions.
- Force and heat are constant within a step.
- Waste/auxiliary powers are declared inputs, not calibrated efficiency maps.
- No recovery, refueling, pit operation, reliability stochasticity, or strategy.
- `finished` means only this Level-0 gate passed; it is not physical validation.
- Work 016 must add lateral/yaw/load-transfer constraints without reinterpreting
  these fixture times as real performance.
