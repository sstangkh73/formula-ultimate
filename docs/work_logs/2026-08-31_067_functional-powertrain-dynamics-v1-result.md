# Work 067 Result: Functional Powertrain Dynamics v1

Thai companion: `2026-08-31_067_functional-powertrain-dynamics-v1-result.th.md`

Status: Completed

## Outcome

Implemented and exercised a deterministic transient model for the Work 066 energy-storage, converter, compliant connection, transmission, and output-load path. The positive reference conserved energy within the frozen threshold, all declared local limits remained respected, every modeled loss appeared in the heat ledger, and refined integration agreed with the reference step. Zero-energy, shaft-overload, thermal-failure, invalid-input, and replay controls passed.

## Files changed

- `src/formula_ultimate/simulation/powertrain_dynamics.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_powertrain_dynamics_v1.json`
- `scripts/experiments/run_functional_powertrain_dynamics.py`
- `tests/test_functional_powertrain_dynamics.py`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.md`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.th.md`
- this bilingual Work 067 plan/result set

Ignored experiment evidence is `artifacts/work067/powertrain_dynamics_evidence.json`.

## Decisions

- The converter remains technology-neutral and is defined by its energy interface, torque-speed map, efficiency map, inertia, thermal state, and limits.
- A two-inertia compliant shaft exposes twist, torque, damping heat, and irreversible failure rather than treating the drivetrain as a force label.
- The transmission ratio is `omega_input / omega_output`; torque multiplication includes declared shaft and transmission efficiencies.
- The forward-only output load cannot inject reverse energy. Reverse operation and regeneration remain explicit non-goals.
- Numerical energy residuals are recorded and gated but never used to repair state.

## Exact validation commands and outputs

```powershell
py -3.14 -m unittest tests.test_functional_powertrain_dynamics -v
```

Exit status `0`; `Ran 8 tests ... OK`.

```powershell
py -3.14 scripts/experiments/run_functional_powertrain_dynamics.py --config config/vehicle/functional_powertrain_dynamics_v1.json --output artifacts/work067/powertrain_dynamics_evidence.json
```

Exit status `0`; status `passed`; evidence SHA-256 `9b99b5afb6a0368b450d54d6bab983c4e0444be188baf783ed1f54c0e3a8713c`; reference result SHA-256 `3248fe721f8fdc39aca182cb81ced64ee7163fdabfa6874778636bd3df2b3543`; maximum relative energy residual `1.0006847977638245e-08`; maximum refinement difference `1.79900311164274e-05`; overload terminal `shaft_connection_failure`; thermal terminal `converter_overtemperature`.

Reference evidence: `4,000` steps; final converter/output speeds `322.205241054604/107.403266469072 rad/s`; source energy used `65,729.4197853313 J`; useful work `30,286.8669266214 J`; maximum connection demand `182.066064231239 N m`; maximum twist `0.0812613938084503 rad`; maximum output drive torque `513.699400228442 N m`; final temperatures `300.317298442075/300.2848072388 K`.

```powershell
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit statuses `0`; full regression output `Ran 396 tests ... OK`; compilation and diff checks emitted no errors.

## Falsification and limitations

The zero-energy control produced exactly zero source use and useful work. The overload control exceeded a deliberately reduced `50 N m` shaft limit with demand `56.331665505 N m`, failed at `0.002 s`, and then transmitted zero torque. The thermal control terminated as `converter_overtemperature` at `0.016 s`. Invalid maps, efficiencies, conservation declarations, temperatures, tolerances, time grids, and non-finite states were rejected.

No contradiction was observed inside the declared model. This does not validate a physical engine, motor, battery, gearbox, shaft, or complete vehicle. All reference maps and thermal/failure values are synthetic. The fixed-step, two-inertia model omits detailed fields, contact, geometry-derived stress/fatigue, tyre slip, translation, regeneration, and measured calibration. It must not be used for a race-performance or safety claim.

## Follow-up

Work 068 should couple the two powertrain outputs to wheel inertia and a bounded ground-force/slip law, verify torque-to-force and wheel/vehicle energy transfer analytically, and propagate a failed drive connection into subsystem failure and `DNF`. A later work item should replace the synthetic shaft limit with geometry/material evidence from the torsion, yield, fracture, and fatigue chain.
