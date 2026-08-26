# Lumped Thermal, Cooling, Derating, and Failure Model

Status: Implemented for Work 014

Thai companion: `THERMAL_MODEL.th.md`

## Purpose and claim boundary

Work 014 adds one deterministic thermal node per modeled component. It converts
declared heat and ambient conductance into temperature, a power-availability
factor, and a latched over-temperature event. It is a Level-0 analytical model,
not evidence of real hardware temperature, safety, cooling performance, or
physical validation.

## SI contract and exact step

Temperature uses kelvin (`K`), heat capacity `J/K`, conductance `W/K`, power
`W`, time `s`, and energy `J`. For constant inputs over one step:

```text
G = G_passive + cooling_command * G_active
C dT/dt = P_heat - G (T - T_ambient)
```

For `G > 0`:

```text
T_eq = T_ambient + P_heat / G
T(t) = T_eq + (T0 - T_eq) exp(-G t / C)
```

For `G = 0`, `T(t) = T0 + P_heat*t/C`. The integrated total heat rejected is
derived independently from storage:

```text
E_rejected = P_heat*t - C*(T1 - T0)
residual = E_generated - E_passive - E_active - delta_E_stored
```

Passive and active rejected energy are divided by their conductance fractions.
They are signed: a negative value means warmer ambient supplies heat to a colder
component. The residual remains an output and is never corrected.

## Derating and failure

```text
factor = 1                                      if T <= T_derate
factor = (T_fail - T) / (T_fail - T_derate)    if T_derate < T < T_fail
factor = 0                                      if T >= T_fail
```

If a requested step crosses `T_fail`, the first crossing time is solved from the
same analytical trajectory. Only time through that event is executed. The end
temperature is the event temperature, the remaining requested duration is
reported as unexecuted, and failure latches. A later step returns
`already_failed` without advancing. A state already above the threshold keeps
its actual temperature and returns `failed_at_start`; it is not clipped back.

## Observable statuses

| Status | Meaning |
|---|---|
| `normal` | Step completed without entering derating |
| `derated` | Start or end of completed step lies in derating range |
| `failed` | First threshold crossing localized inside the requested step |
| `failed_at_start` | Unlatched input state is already at/above threshold |
| `already_failed` | Latched state refuses further execution |

## Analytical evidence

- `C=1000 J/K`, `100 W`, `10 s`, no cooling: `300 -> 301 K`.
- `C=1000 J/K`, `G=100 W/K`, `390 K`, ambient `300 K`, `10 s`:
  `333.1091497054298 K`, matching the exponential closed form.
- `C=1000 J/K`, `1000 W`, `350 K`, no cooling, `T_fail=400 K`: failure at
  `50 s`; a requested `100 s` step leaves `50 s` unexecuted.

Run:

```powershell
python scripts/validate_thermal.py
python -m unittest tests.test_thermal -v
```

## Limitations and follow-up

- One uniform node omits geometry-driven gradients and hotspots.
- Conductances, heat capacity, and thresholds are declared inputs without CFD,
  material, or test calibration in Work 014.
- Inputs are constant within a step; controllers must choose their own step.
- Convection is linear; radiation, coolant flow/inventory, phase change,
  contact resistance, fan/pump energy, aging, and fire are omitted.
- Work 015 must treat `unexecuted_duration_s` and latched failure as a failed
  race outcome, never a successful shortened step.
