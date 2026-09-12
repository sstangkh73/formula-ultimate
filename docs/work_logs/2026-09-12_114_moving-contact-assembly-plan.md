# Work 114 Plan: Moving Contact Assembly

Thai companion: `2026-09-12_114_moving-contact-assembly-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a bounded two-coordinate moving/compliant assembly using the exact Work 113 joint stiffness/contact applicability. Track an axially compliant moving member under imposed base reversal plus a tangential stick/slip history, unilateral opening/closing, recovered contact reactions, swept clearance and an energy/work ledger.

Compare three explicit time steps and a reduced in-range response against the detailed event law. Retain the Work 088 rigid/moving incompatibility as a fail-closed regression rather than silently imposing rigidity.

## Variables, controls and files

- IV: joint strategy, placement clearance, compliance, preload, motion amplitude/history and time step.
- DV: displacement/phase, constraint drift, contact force, opening/closing/slip events, minimum swept clearance, transmitted impulse and energy residual.
- Controls: identical initial/boundary histories; free rigid motion, incompatible constraints, severed coupling, reversal/contact impact, collision and reduced-model range violation.
- Success: deterministic histories, contact events and reactions are computed rather than assigned, registered time-step quantities meet last-two gates, energy/constraint/clearance gates pass, invalid assemblies are blocked locally, and replay is exact.

Planned files: `src/formula_ultimate/assembly/moving_contact_assembly.py`, `config/development/moving_contact_assembly_v1.json`, `scripts/development/run_moving_contact_assembly.py`, `tests/test_moving_contact_assembly.py`, bilingual `docs/contracts/MOVING_CONTACT_ASSEMBLY_V1*`, this bilingual plan/result and ignored `artifacts/work114/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_moving_contact_assembly tests.test_repository_contract -v
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_a
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_b --replay-reference artifacts/work114/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected regressions, explicit staged-scope inspection and cached diff checks; commit only after all declared gates pass.

## Risks and non-goals

Penalty-contact stiffness creates a small stable time scale; expose time-step dependence. Tangential motion is a registered prescribed-history contact probe, not full planar rigid-body dynamics. Non-goals: complete suspension, crash, vehicle readiness, nonlinear flexible-body FEA, physical validation, push or history rewrite.
