# Work 116 Plan: Material Provenance and Scoped Failure

Thai companion: `2026-09-12_116_material-failure-scope-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a traceable material/process applicability registry over the exact Work 111 field, Work 114 history and Work 115 temperature evidence. Preserve units, provenance, temperature/rate/history ranges, uncertainty and process dependence before any failure-law evaluation.

Verify bounded first-yield and Euler-column reference laws with safe/failed and imperfection-sensitivity fixtures. Candidate properties remain synthetic, so numerical margins are diagnostic only and cannot become measured survival evidence. Fatigue, fracture and wear remain explicit unresolved extension slots.

## Variables, controls and files

- IV: material/process record, temperature, strain rate, load history and column imperfection.
- DV: eligibility, yield/buckling margin, uncertainty interval, sensitivity and missing-domain coverage.
- Controls: analytic yield/Euler references, known safe and failed cases, zero/increased imperfection; reject out-of-range properties, missing units, unjustified mixtures and synthetic-to-measured relabeling.
- Success: dependency evidence is pinned, law references pass, imperfection reduces buckling capacity, candidate coverage never exceeds provenance, missing domains block dependent claims and replay is exact.

Planned files: `src/formula_ultimate/structural/material_failure_scope.py`, `config/development/material_failure_scope_v1.json`, `scripts/development/run_material_failure_scope.py`, `tests/test_material_failure_scope.py`, bilingual `docs/contracts/MATERIAL_FAILURE_SCOPE_V1*`, this bilingual plan/result and ignored `artifacts/work116/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_material_failure_scope tests.test_repository_contract -v
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_a
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_b --replay-reference artifacts/work116/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected regressions and explicit staged/cached diff checks; commit immediately only after all gates pass.

## Risks and non-goals

Reference-law verification does not calibrate the synthetic candidate material. Non-goals: universal constitutive behavior, fatigue life, fracture, wear, manufacturing qualification, safety certification, complete physical survival, push or history rewrite.
