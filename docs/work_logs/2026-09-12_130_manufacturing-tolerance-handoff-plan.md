# Work 130 Plan: Manufacturing Tolerance Handoff

Thai companion: `2026-09-12_130_manufacturing-tolerance-handoff-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Map every Work 126 component region to an explicit candidate process route, stock/source assumption, assembly step and inspection access; propagate registered tolerances into clearance and preload; and carry Work 129's downgraded evidence envelope into a manufacturing handoff decision.

Readiness is permitted only for routes with applicable process-capability evidence, accessible assembly/inspection, feasible ordering and worst-case tolerance margins. Unsupported routes remain `unknown`, not impossible. No purchasing, fabrication or safety certification is authorized.

## Variables, controls and files

- IV: process route, evidence class, tolerance allocation, assembly order and access state.
- DV: route status, access, worst-case clearance/preload, assembly feasibility and unresolved blockers.
- Controls: inaccessible fastener, trapped core, cyclic/impossible assembly, nominal-only clearance and insufficient preload must fail closed.
- Success: all regions mapped, exact source identity, worst-case tolerance propagation, inspection/assembly dossier, explicit redesign list and exact replay.

Planned files: `src/formula_ultimate/assembly/manufacturing_tolerance_handoff.py`, `config/development/manufacturing_tolerance_handoff_v1.json`, `scripts/development/run_manufacturing_tolerance_handoff.py`, `tests/test_manufacturing_tolerance_handoff.py`, bilingual `docs/contracts/MANUFACTURING_TOLERANCE_HANDOFF_V1*`, this bilingual plan/result, and ignored `artifacts/work130/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_manufacturing_tolerance_handoff tests.test_repository_contract -v
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_a
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_b --replay-reference artifacts/work130/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 126/129 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

The input is a G3 box registry, not native manufacturing CAD. Minimum-feature heuristics do not establish process capability. Non-goals: purchasing, fabrication, supplier qualification, safety certification, global impossibility claims, push or history rewrite.
