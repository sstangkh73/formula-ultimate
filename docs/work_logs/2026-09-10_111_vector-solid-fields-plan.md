# Work 111 Plan: Vector Solid Fields from Generated Geometry

Thai companion: `2026-09-10_111_vector-solid-fields-plan.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement small-strain isotropic linear-elastic tetrahedral FEM on actual Work 110 meshes, with three displacement DOFs per node, traction/body-force conventions, explicit supports, recovered reactions, vector displacement and tensor stress fields. Use synthetic fixture materials only.

The admitted experiment contains a structured cuboid reference for affine patch and analytic axial-displacement checks, plus the unfamiliar Work 109 geometry routed through Work 110 at `0.02`, `0.01` and `0.008 m`. Sharp-corner point maxima are excluded; the registered stress quantity is element-volume-weighted p90 von Mises stress.

## Variables, controls and files

- IV: geometry, load direction, Young's modulus and resolution.
- DV: vector displacement, compliance, p90 von Mises stress, reactions, strain energy, force/moment/energy residual and diagonal conditioning proxy.
- Controls: same SI material/load/support semantics; analytic cuboid; affine patch; stiffness scaling; rigid-mode, severed-path and corrupt-stiffness failures.
- Success: nonsingular solves, residual gates, analytic/patch gates, bounded last-two changes, deterministic field identities and causal load/material mutations.

Planned files: `src/formula_ultimate/structural/vector_solid_fields.py`, `config/development/vector_solid_fields_v1.json`, `scripts/development/run_vector_solid_fields.py`, `tests/test_vector_solid_fields.py`, bilingual `docs/contracts/VECTOR_SOLID_FIELDS_V1*`, this bilingual plan/result, and ignored `artifacts/work111/run_a|run_b`.

## Validation

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_vector_solid_fields tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_a
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_b --replay-reference artifacts\work111\run_a\result.json
python -m compileall -q src scripts tests
```

Then run affected regressions, `git diff --check`, explicit staging, cached-scope inspection and `git diff --cached --check`; commit immediately if all gates pass.

## Risks and non-goals

Voxel geometry changes with resolution, stress near stepped corners can be singular, and a diagonal proxy is not a spectral condition number. Preserve these limits. Non-goals: nonlinear/contact/plastic/fatigue mechanics, certified material data, stress-convergence proof, vehicle feasibility, physical validation, dependency installation, push or history rewrite.
