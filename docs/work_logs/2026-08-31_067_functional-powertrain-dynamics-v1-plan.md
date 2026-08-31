# Work 067 Plan: Functional Powertrain Dynamics v1

Status: Completed

Thai companion: `2026-08-31_067_functional-powertrain-dynamics-v1-plan.th.md`

## Objective

Implement the first transient physical model for the Work 066 path `energy_storage -> energy_converter -> power_transmission -> ground_propulsion`. Requested torque must be bounded by stored energy, declared power, a torque-speed envelope, efficiencies, shaft dynamics, transmission ratio, thermal state, and failure limits. Every joule removed from storage must become mechanical energy, useful external work, stored heat, rejected heat, or an observable numerical conservation residual.

This work converts the reference architecture from a connected static contract into a falsifiable component-dynamics specimen. It does not yet claim a complete engine, gearbox, tyre, or whole-car simulation.

## Research question and hypotheses

Question: can the functional architecture transmit bounded torque through a transient compliant drivetrain while conserving energy and failing closed when energy, torque, speed, or temperature limits are violated?

Preferred hypothesis: the reference path accelerates a declared load, follows its torque-speed and efficiency maps, converts all modeled losses to heat, conserves energy within the frozen numerical tolerance, and produces zero downstream drive after a terminal connection failure.

Falsification includes acceleration with zero stored energy, output torque beyond the local path limit, output power greater than conserved input, missing loss heat, non-finite state, unreported energy residual, increasing stored energy without a declared recovery path, a failed shaft continuing to transmit torque, materially different results on deterministic replay, or time-step refinement disagreement beyond the declared bound.

## Scope and state model

The technology-neutral reference model will contain:

1. a finite onboard energy state in joules and maximum source power;
2. an interpolated converter torque-speed envelope and load-dependent efficiency map;
3. converter rotational inertia and viscous loss;
4. a torsionally compliant connection with stiffness, damping, torque limit, twist limit, and irreversible failure state;
5. a transmission ratio, mechanical efficiency, reflected downstream inertia, and output torque/speed limits;
6. an external output-load torque and useful-work accumulator;
7. converter and transmission lumped thermal states, heat capacities, ambient rejection coefficients, and maximum temperatures;
8. explicit energy storage, kinetic, elastic, thermal, useful-work, rejected-heat, and residual terms;
9. deterministic terminal state and event/failure codes.

The ratio convention is `ratio = omega_input / omega_output`; ideal output torque is input torque multiplied by `ratio`, then reduced by transmission efficiency. SI units and a right-handed frame remain mandatory.

## Experiment design

- Independent variables: throttle schedule, output load torque, initial stored energy, converter speed, shaft stiffness/damping/limits, inertia, ratio, torque-speed curve, efficiency curve, cooling coefficients, failure thresholds, duration, and time step.
- Dependent variables: storage energy, shaft speeds and twist, transmitted/output torque, useful work, component temperatures, generated/rejected heat, limit flags, failure code/time, energy residual, and replay hash.
- Controls: frozen Work 066 component limits, piecewise-linear maps, deterministic fixed-step integration, no regeneration, no silent clipping of invalid state, explicit SI units, and canonical JSON identity.
- Metrics: relative energy-conservation residual, maximum local-limit utilization, terminal speed/energy/temperature, useful-work fraction, failure response, exact replay, and coarse-versus-refined time-step difference.

The positive reference case will use a bounded throttle/load schedule. Negative controls will include zero stored energy, deliberate shaft overload, deliberate thermal limit violation, invalid configuration, and tampered/non-finite inputs. An analytical locked-speed conversion case will verify power and heat partition independently of the transient integrator.

## Planned files

- `src/formula_ultimate/simulation/powertrain_dynamics.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_powertrain_dynamics_v1.json`
- `scripts/experiments/run_functional_powertrain_dynamics.py`
- `tests/test_functional_powertrain_dynamics.py`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.md`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.th.md`
- matching bilingual Work 067 plan/result records
- ignored deterministic evidence under `artifacts/work067/`

## Validation and success criteria

1. Configuration values and maps are finite, ordered, dimensionally explicit, and fail closed when invalid.
2. Zero energy yields zero converter torque, zero output work, and no force-from-nowhere.
3. The analytical conversion check closes storage, connection, converter, and transmission power/loss terms to floating-point tolerance.
4. The transient reference run respects every declared energy, torque, speed, twist, and temperature limit or reports the exact terminal failure.
5. Converter, cable, shaft damping, transmission, and viscous losses appear as heat; ambient cooling appears as rejected heat.
6. Total energy accounting includes storage, mechanical, elastic, thermal, useful work, rejected heat, and a signed observable residual with relative magnitude `<= 1e-3` for the reference run.
7. Deliberate shaft overload breaks the connection irreversibly and all subsequent transmitted/output drive torque is zero.
8. Deliberate overtemperature terminates with the correct component failure code.
9. Repeated runs are byte-identical after canonical serialization; a half-step refinement changes selected terminal metrics by `<= 2%`.
10. Focused/full tests, compilation, bilingual evidence, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

Fixed-step lumped dynamics can hide stiff-shaft integration error; conservation residual and step refinement are therefore admission evidence, not silent corrections. Synthetic torque-speed, efficiency, thermal, stiffness, and failure data are test fixtures, not measured component maps or certified limits. A reference drivetrain may bias future discovery and must not become a mandatory topology.

Work 067 does not model electrochemistry, combustion, electromagnetic fields, gear teeth, bearings, backlash/contact, lubrication, detailed shaft stress, fatigue/fracture growth, differential action, regenerative braking, tyre slip, suspension, vehicle translation, steering, aerodynamics, race strategy, manufacturing, physical validation, or safety certification. These require later work items and higher-fidelity evidence.
