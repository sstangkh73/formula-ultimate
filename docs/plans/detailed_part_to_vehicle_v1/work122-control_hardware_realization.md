# Work 122: Controller, sensor and support hardware

Thai companion: `work122-control_hardware_realization.th.md`

Status: Planned

Original Work 106 package: 121

Dependencies: Work 119, Work 120

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Ensure sensing and actuation are backed by physical hardware, mounting, signal paths, finite authority and energy.

Work 119 actuator envelope, Work 120 supply and Work 112 interfaces; declare what is measured versus estimated.

## 2. Proposed files

- `src/formula_ultimate/subsystems/control_hardware_realization.py`
- `config/development/control_hardware_realization_v1.json`
- `scripts/development/run_control_hardware_realization.py`
- `tests/test_control_hardware_realization.py`

## 3. Implementation sequence

1. Define required observable states and realizable sensor/signal pathways.
2. Represent sensor/controller/actuator support geometry, connectors, mounting and supply loads.
3. Implement latency, noise, saturation and fault behavior tied to registered assumptions.
4. Evaluate common-controller and matched-budget adaptation modes; charge tuning cost.

## 4. Experiment

- IV: Hardware placement/specification, controller parameters, noise, delay and failure states.
- DV: Tracking/stability metrics, sensing error, energy, mass and adaptation cost.
- Controls: Same task, actuator limits and total tuning opportunity.

## 5. Tests and falsification

Sensor dropout, disconnected signals, exhausted supply, saturated actuator and increased delay; a noncausal controller parameter must not count as useful mutation.

## 6. Registration and acceptance

Freeze sensor/actuator applicability, sample interval, noise/delay models, tuning budget and error criteria.

Every claimed sensing/actuation path has hardware/accounting evidence; controller comparisons include finite limits and matched adaptation cost.

## 7. Deliverables and handoff

Hardware CAD/manifest, signal graph, closed-loop traces, fault report and tuning ledger.

Feeds Work 123 closed-loop simulation and Work 127 fair controller comparisons.

## 8. Risks and non-goals

Ideal full-state observation can hide required hardware. Keep exploratory idealization labeled; no arbitrary advanced electronics or safety-critical controller certification.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_control_hardware_realization tests.test_repository_contract -v
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_a
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_b --replay-reference artifacts/work122/run_a/result.json
```
