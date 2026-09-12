# Work 122 Plan: Controller, Sensor and Support Hardware

Thai companion: `2026-09-12_122_control-hardware-realization-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Realize one bounded sensor-controller-actuator signal path with explicit sensor, controller, harness, connector, mount and actuator-interface hardware. Pin Work 119 actuator authority and Work 120 supply evidence; distinguish synthetic/estimated signals from measured evidence.

Implement a deterministic sampled closed-loop reference with registered noise, latency, saturation, dropout, signal disconnection and supply exhaustion. Compare common-controller and adapted-controller parameter sets with the same four-evaluation tuning budget and reject noncausal parameter mutations.

## Variables, controls and files

- IV: hardware placement/specification, proportional gain, sample delay, deterministic noise, dropout, signal connectivity, supply and actuator limit.
- DV: tracking RMSE/final error, saturation/dropout counts, energy, hardware mass and tuning cost.
- Controls: same task/authority/budget; dropout, disconnected signal, exhausted supply, saturation, increased delay and noncausal mutation.
- Success: every path has counted hardware, finite limits are active, matched tuning charges failures/evaluations, controls are causal and exact replay passes.

Planned files: `src/formula_ultimate/subsystems/control_hardware_realization.py`, `config/development/control_hardware_realization_v1.json`, `scripts/development/run_control_hardware_realization.py`, `tests/test_control_hardware_realization.py`, bilingual `docs/contracts/CONTROL_HARDWARE_REALIZATION_V1*`, this bilingual plan/result and ignored `artifacts/work122/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_control_hardware_realization tests.test_repository_contract -v
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_a
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_b --replay-reference artifacts/work122/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 119/120 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

The reference plant, noise, latency and hardware data are synthetic. Non-goals: ideal full-state observation, arbitrary electronics, safety-critical certification, real controller stability, physical validation, push or history rewrite.
