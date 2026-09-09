# Work 111: Vector solid fields from generated geometry

Thai companion: `work111-vector_solid_fields.th.md`

Status: Planned

Original Work 106 package: 110

Dependencies: Work 110

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Replace scalar-member evidence with an explicitly scoped vector solid mechanics capability on real candidate meshes.

Input: Work 110 meshes and semantic supports; declared elastic fixture materials, not certified production data.

## 2. Proposed files

- `src/formula_ultimate/structural/vector_solid_fields.py`
- `config/development/vector_solid_fields_v1.json`
- `scripts/development/run_vector_solid_fields.py`
- `tests/test_vector_solid_fields.py`

## 3. Implementation sequence

1. Define displacement, traction, body-force and support conventions in SI frames.
2. Implement/adapt a linear elastic vector solve and recover reactions from the assembled system.
3. Compute declared quantities of interest, strain energy, force/moment balance and conditioning.
4. Run reference and unfamiliar-shape cases across refinement levels; compare independent formulations.

## 4. Experiment

- IV: Boundary geometry, loading direction, material stiffness and refinement.
- DV: Displacement, compliance, stress quantities, reaction residuals and discretization error.
- Controls: Same physical load/support definitions and geometry across compared solvers.

## 5. Tests and falsification

Rigid translation/rotation, patch test, off-axis loading, unsupported rigid modes, severed load path and corrupted stiffness. Verify reactions are not assigned equal to the input.

## 6. Registration and acceptance

Freeze material assumptions, 3-level schedule, residual/error tolerances and nonsingular stress quantities.

Reference and convergence gates pass; geometry mutations cause reproducible vector-field changes. Non-converged or singular cases cannot become survivors.

## 7. Deliverables and handoff

Displacement/stress fields, recovered reactions, energy tables, convergence and independent-reference comparisons.

Enables detailed connections Work 113, thermal coupling Work 115 and failure scope Work 116.

## 8. Risks and non-goals

Sharp-corner point stress may not converge. Define a justified geometry/quantity treatment visibly. No nonlinear contact, fatigue or physical-validation claim.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_repository_contract -v
python scripts/development/run_vector_solid_fields.py --config config/development/vector_solid_fields_v1.json --output-root artifacts/work111/run_a
python scripts/development/run_vector_solid_fields.py --config config/development/vector_solid_fields_v1.json --output-root artifacts/work111/run_b --replay-reference artifacts/work111/run_a/result.json
```
