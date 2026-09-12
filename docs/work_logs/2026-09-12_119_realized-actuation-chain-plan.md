# Work 119 Plan: Realized Transmission and Actuation Chain

Thai companion: `2026-09-12_119_realized-actuation-chain-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement one disclosed, bounded coaxial rotary reference route that converts an input torque/speed port into an output torque/speed port through realized transfer members, supports and containment. Pin Work 114 load/motion, Work 115 thermal burden and Work 116 material-applicability evidence while keeping alternative conversion routes open through explicit extension slots.

Derive member mass, torsional stiffness/stress, speed/load saturation, efficiency loss, heat and support reactions from registered geometry and synthetic properties. Preserve the material-survival claim as blocked and reject ideal conversion without complete hardware coverage.

## Variables, controls and files

- IV: transfer-member geometry, reduction ratio, input torque/speed, temperature, direction, output lock and path/support connectivity.
- DV: output torque/speed/work, loss/heat, stiffness/twist, stress, capacity, complete hardware mass and support reactions.
- Controls: same ports/materials/energy opportunity; disconnected path, locked output, reverse operation, saturated torque and removed supports.
- Success: geometry supports every admitted action; input power equals output plus modeled loss; envelope/temperature limits fail closed; controls are causal; exact replay passes.

Planned files: `src/formula_ultimate/subsystems/realized_actuation_chain.py`, `config/development/realized_actuation_chain_v1.json`, `scripts/development/run_realized_actuation_chain.py`, `tests/test_realized_actuation_chain.py`, bilingual `docs/contracts/REALIZED_ACTUATION_CHAIN_V1*`, this bilingual plan/result and ignored `artifacts/work119/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_realized_actuation_chain tests.test_repository_contract -v
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_a
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_b --replay-reference artifacts/work119/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 114/115/116 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

The selected route is a synthetic Level-0 reference, not a permanent technology whitelist or build authorization. Non-goals: requiring gears/shafts/motors for every proposal, validated efficiency/material strength, fatigue/wear, detailed bearings/fasteners, controller hardware, physical validation, push or history rewrite.
