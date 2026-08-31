# Functional Powertrain Dynamics v1

Thai companion: `FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.th.md`

## Result and claim boundary

Work 067 implements the first transient component-law specimen behind the Work 066 path `energy_storage -> energy_converter -> power_transmission -> ground_propulsion`. The model produces torque only by removing declared onboard energy. Electrical, conversion, viscous, shaft-damping, connection, and transmission losses become explicit heat. A compliant connection can fail irreversibly, after which transmitted and output drive torque are zero.

The result validates equations, state transitions, accounting, deterministic replay, and deliberate failures for a synthetic reference. It does not identify a preferred motor, engine, energy store, transmission, or vehicle topology, and it is not measured or physically validated hardware.

## Dynamic model

The transmission ratio convention is

```text
n = omega_input / omega_output
```

and shaft twist and torque are

```text
delta = theta_converter - n theta_output
T_shaft = k delta + c (omega_converter - n omega_output).
```

Before failure, the two rotational states obey the implemented forward-only lumped equations

```text
J_converter domega_converter/dt = T_converter - T_shaft - b_converter omega_converter
J_output domega_output/dt = eta_shaft eta_transmission n T_shaft
                                  - T_load - b_output omega_output.
```

`T_converter` is bounded by throttle, an interpolated torque-speed curve, the converter output-power limit, converter input-power limit, connected storage-power limit, conversion efficiency, and remaining stored energy. The external load is unilateral and resistive: it may slow forward rotation but cannot inject undeclared reverse work. Reverse rotation and regeneration are outside v1 and fail validation rather than being inferred.

The energy residual is exposed as

```text
R = E_initial - (E_storage + E_kinetic + E_elastic + E_thermal
                 + W_useful + Q_rejected).
```

No residual is used to correct state. The reference admission ceiling is `|R| / E_scale <= 1e-3`.

## Frozen synthetic reference

The fixed fixture uses storage capacity `50 MJ`, source power `120 kW`, electrical connection efficiency `0.99`, a converter torque envelope of `450 N m` through `200 rad/s` falling to zero at `400 rad/s`, converter inertia `0.2 kg m^2`, shaft stiffness `2000 N m/rad`, damping `35 N m s/rad`, shaft efficiency `0.99`, shaft torque limit `450 N m`, twist limit `0.3 rad`, transmission ratio `3.0`, transmission efficiency `0.95`, output inertia `2.5 kg m^2`, and synthetic lumped thermal parameters.

These numbers align with or are locally more restrictive than the Work 066 architecture fixture. They are not measurements or certified allowables.

## Analytical power partition

At throttle `0.5` and converter speed `200 rad/s`, the independent algebraic check gives:

- converter torque: `225 N m`;
- storage power: `47,846.88995215311 W`;
- converter mechanical power: `45,000 W`;
- output speed: `66.66666666666667 rad/s`;
- output torque: `634.8375 N m`;
- electrical connection heat: `478.4688995215329 W`;
- converter heat: `2,368.42105263158 W`;
- shaft-efficiency heat: `450 W`;
- transmission heat: `2,227.5 W`;
- power residual: `0 W`.

Thus the lower output power is explained by declared losses rather than disappearing energy.

## Transient experiment

The reference command used throttle `0.5`, output-load torque `200 N m`, duration `2 s`, and step `0.0005 s` for `4,000` steps. It completed without a limit failure.

| Metric | Result | Limit/status |
| --- | ---: | --- |
| final converter speed | `322.205241054604 rad/s` | `< 400 rad/s` |
| final output speed | `107.403266469072 rad/s` | `< 150 rad/s` |
| source energy used | `65,729.4197853313 J` | finite/decreasing store |
| useful external work | `30,286.8669266214 J` | positive |
| maximum connection demand | `182.066064231239 N m` | `< 450 N m` |
| maximum shaft twist | `0.0812613938084503 rad` | `< 0.3 rad` |
| maximum output drive torque | `513.699400228442 N m` | `< 1,200 N m` |
| final converter temperature | `300.317298442075 K` | `< 450 K` |
| final transmission temperature | `300.2848072388 K` | `< 450 K` |
| maximum absolute energy residual | `0.500342398881912 J` | observable |
| maximum relative energy residual | `1.00068479776382e-8` | `< 1e-3` |

The reference result SHA-256 is `3248fe721f8fdc39aca182cb81ced64ee7163fdabfa6874778636bd3df2b3543`. An exact rerun reproduced it. Halving the step to `0.00025 s` changed the selected terminal metrics by at most `1.79900311164274e-5`, below the frozen `0.02` ceiling.

## Falsification controls

- Zero-energy control: source energy used and useful work both remained exactly `0 J`; converter and output speeds remained zero.
- Shaft-overload control: reducing the torque limit to `50 N m` produced demand `56.331665505 N m`, terminal `shaft_connection_failure` at `0.002 s`, and transmitted torque `0 N m` after failure.
- Thermal control: deliberately reducing converter heat capacity and maximum temperature produced `converter_overtemperature` at `0.016 s`.
- Invalid declarations: unordered curves, efficiency above one, undeclared power/torque creation, maximum temperature below ambient, excessive numerical tolerance, non-finite runtime state, and incompatible duration/step fail closed.

All eight frozen experiment checks and all eight focused unit tests passed. The full repository regression passed 396 tests.

## Missing evidence and next coupling

The model remains two-inertia, forward-only, lumped, and fixed-step. It omits electrochemistry, combustion, electromagnetic fields, detailed gear/shaft geometry, bearing/contact friction, backlash, lubrication, differential action, regeneration, tyre slip, suspension, and vehicle translation. Its connection torque is not yet derived from shaft stress, yield, fatigue, or fracture geometry. Temperatures are lumped states, not conjugate heat-transfer results.

The next work should connect the two output branches to ground-force/slip and wheel inertia while preserving the same energy ledger. After that, the compliant connection should consume geometry/material evidence from the verified torsion and failure modules so a physically failed shaft causes a whole-vehicle subsystem failure or `DNF`.
