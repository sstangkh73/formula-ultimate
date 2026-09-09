# Work 119: Realized transmission and actuation chain

Thai companion: `work119-realized_actuation_chain.th.md`

Status: Planned

Original Work 106 package: 118

Dependencies: Work 114, Work 115, Work 116

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Turn commanded power/motion into a detailed supported hardware path with real reactions and losses.

Interface, moving contact, thermal and material models; choose a disclosed tractable reference route, not a permanent technology whitelist.

## 2. Proposed files

- `src/formula_ultimate/subsystems/realized_actuation_chain.py`
- `config/development/realized_actuation_chain_v1.json`
- `scripts/development/run_realized_actuation_chain.py`
- `tests/test_realized_actuation_chain.py`

## 3. Implementation sequence

1. Freeze input/output ports and rate/load envelope; select only supported conversion laws.
2. Generate internal transfer members, interfaces, supports and needed containment geometry.
3. Derive stiffness, losses, reaction loads and thermal burden from the realized route.
4. Validate a bounded response map and expose extension interfaces for alternative routes.

## 4. Experiment

- IV: Transfer geometry, interface arrangement, speed/load and temperature.
- DV: Output work/torque/force, loss, capacity, mass and support reactions.
- Controls: Same port task, allowed materials and energy input; optimized reference arrangement.

## 5. Tests and falsification

Disconnect power path, lock output, reverse operation, saturate demand and remove supports; check energy destination in each case.

## 6. Registration and acceptance

Freeze conversion assumptions, load/speed/temperature envelope, loss/error tolerances and hardware coverage.

Every claimed action has geometry/material support and verified accounting; ideal torque with unexplained hardware cannot pass.

## 7. Deliverables and handoff

Internal CAD, physical path graph, response/loss maps, support/thermal loads and validation report.

Feeds energy Work 120, controller hardware Work 122 and transient integration Work 123.

## 8. Risks and non-goals

New conversion physics may exceed one package. Split its law verification before admission; do not assume gears, shafts or a specific motor are mandatory.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_realized_actuation_chain tests.test_repository_contract -v
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_a
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_b --replay-reference artifacts/work119/run_a/result.json
```
