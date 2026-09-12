# Work 126 Plan: Detailed Vehicle Closure

Thai companion: `2026-09-12_126_detailed-vehicle-closure-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Create one deterministic, inspectable G3 geometry registry for the exploratory detailed candidate and trace every registered external function through material regions, installed hardware and interfaces. Pin Works 118–125, close mass/center/inertia/occupied-volume, energy, signal, heat and load-path ledgers, and audit assembly plus sampled swept motion.

G3 means explicit per-component solid bounds, placement, ownership and interface records in this bounded registry. It is not native CAD, manufacturing release or physical validation. Essential physics gaps remain explicit and must keep the candidate `detailed_exploratory`, never promotion-ready.

## Variables, controls and files

- IV: component placement, hardware-role inclusion, connection path, tolerance state and motion sample.
- DV: function/hardware coverage, unique region ownership, mass/center/inertia/volume residuals, energy/signal/heat/load continuity, overlap/clearance and envelope freshness.
- Controls: remove required fastener/support/seal/signal paths; introduce hidden void, duplicate mass ownership, interference and stale subsystem envelope.
- Success: deterministic replay, all registered geometry/hardware paths closed, zero declared ledger residuals within tolerance, collision-free assembly/motion, and an explicit unresolved-evidence list that blocks promotion.

Planned files: `src/formula_ultimate/assembly/detailed_vehicle_closure.py`, `config/development/detailed_vehicle_closure_v1.json`, `scripts/development/run_detailed_vehicle_closure.py`, `tests/test_detailed_vehicle_closure.py`, bilingual `docs/contracts/DETAILED_VEHICLE_CLOSURE_V1*`, this bilingual plan/result, and ignored `artifacts/work126/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_detailed_vehicle_closure tests.test_repository_contract -v
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_a
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_b --replay-reference artifacts/work126/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 118–125 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

Axis-aligned registered solids can prove bookkeeping and bounded non-overlap only, not detailed surface manufacturability or real collision behavior. Purchased hardware is attributed, not claimed as generated discovery. Non-goals: reusing Work 088 blocked geometry, native CAD certification, material/process qualification, physical survival, promotion, push or history rewrite.
