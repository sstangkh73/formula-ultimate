# Work 138: Geometry-general structural evaluator

Thai companion: `work138-geometry_general_evaluator.th.md`

Status: Planned

Original Work 106 package: none. This is a forward corrective extension authored by Work 137.

Dependencies: Work 062 (campaign evidence), Work 078 and Work 092 (grammars), Work 110 (mesh bridge), Work 111 (solid fields), Work 135 (native geometry). Existing structural seams: `element_verification`, `refined_mesh`, `acceptance`.

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Problem this work corrects

The evaluator used by the bounded campaign does not read geometry. `src/formula_ultimate/experiments/whole_vehicle_search.py` derives `capacity_factor` from `min(core_width_scale, contact_radius_scale**2, source_size_scale**2, propulsor_size_scale**2)` and scales a frozen Work 048 load by `mass_ratio / capacity_factor`. The candidate space in `main_campaign_protocol.py` is therefore five scale variables bounded `0.8`–`1.2`, and `scripts/cad/generate_vehicle_assembly.py` can only emit a box or a cylinder.

Two measured consequences, both from `artifacts/work062/` on 2026-09-20:

1. A shape outside that template cannot be scored at all, so the search cannot leave the template. The free-form grammar exists and works: `artifacts/work092/run_e/` holds ten valid one-solid free-form candidates covering all 18 operators, including `curved_branch` and `organic_load_bridge`. None of them can enter a vehicle candidate today.
2. Of 72 finalists, 21 were cut as `refined_disagreement`. In every one of those 21, all holdout cases recorded `converged: true` and `fine_cross_model_passed: false`, and the CAD stage recorded `not_run`. The solver succeeded; the cheap model and CalculiX disagreed, and the candidate was discarded rather than judged by the better model.

Work 138 makes geometry the input to evaluation. It does not by itself open the design grammar; that is Work 139.

## 2. Outcome and claim boundary

Passing Work 138 means only `passed_geometry_general_structural_evaluation`: an evaluator that accepts any valid solid assembly, derives its own mass properties and load response, and reports a registered status per candidate. It is not a performance result, not promotion, not manufacturability and not physical validation.

## 3. Entry evidence and frozen identity

Pin and record before any admitted run: repository commit and clean-tree state; CadQuery, OCCT, FreeCAD, Gmsh and CalculiX versions with executable SHA-256; the Work 135 declaration and its STEP hashes; the Work 062 protocol, result-ledger and stage-ledger hashes. `gmsh` is not importable as a Python module in the pinned environment, so the mesher is invoked as `gmsh.exe`, following `scripts/structural/run_beam_bending_acceptance.py`.

## 4. Proposed maintained files

- `src/formula_ultimate/structural/geometry_general_evaluator.py`
- `scripts/structural/mesh_step_solid.py` — STEP to Gmsh `msh2`, deterministic options recorded
- `scripts/structural/run_geometry_general_evaluator.py`
- `config/development/geometry_general_evaluator_v1.json`
- `tests/test_geometry_general_evaluator.py`
- `docs/contracts/GEOMETRY_GENERAL_EVALUATOR_V1.md` and its Thai companion

## 5. Evaluation contract

Input is a solid assembly as STEP plus a declared material per solid and a declared load case set. No candidate may declare its own stiffness, strength, mass or margin.

Ordered path:

```text
STEP solid set
  -> validity and single-solid check per part
  -> geometry-derived volume, mass, centre of mass and inertia
  -> Gmsh tetrahedral mesh at three or more resolutions
  -> CalculiX C3D10 solve per registered load case
  -> displacement, von Mises, reaction balance, utilization against declared allowables
  -> registered status and evidence hashes
```

Required outputs per candidate: `mass_kg`, `center_m`, `inertia_kg_m2`, per-case `maximum_displacement_m`, `maximum_von_mises_pa`, `utilization`, `reaction_residual_n`, mesh identity per level, and the solver process record.

## 6. Status vocabulary: the cut must be classified

The evaluator returns exactly one status per candidate. Silent rejection is forbidden.

| Status | Meaning | Effect on search |
|---|---|---|
| `passed` | Solved and within declared allowables | Eligible |
| `failed_physics` | Solved and outside declared allowables | Rejected with cause |
| `unresolved_mesh` | Mesh could not be generated at the coarsest registered level | Retry budget, then recorded unresolved |
| `unresolved_solver` | Solver diverged or did not complete | Retry budget, then recorded unresolved |
| `unresolved_convergence` | Refinement levels did not meet the registered convergence criterion | Recorded unresolved |
| `unsupported_representation` | Input is not a valid single solid per part | Rejected before meshing |

`unresolved_*` is not `failed_physics`. A run must report the count and the cause distribution of unresolved candidates, because that distribution is the evidence for which capability to add next. The registered retry policy must be declared before the run and applied identically to every arm.

## 7. Numerical registration

Freeze before any admitted run: element type and order (`C3D10` unless justified), the three or more mesh resolutions coarse to fine, the convergence criterion on displacement and stress between the last two levels, the allowable set per material with its source, the load cases with their provenance, the reaction-balance tolerance, per-candidate wall-clock and memory budgets, and the retry policy for each `unresolved_*` cause.

Materials come from the declared catalogue with their data source recorded. A geometry-only synthetic density must be labelled as such in the evidence.

## 8. Mandatory falsification controls

Each control must be rejected by the evaluator, and each rejection must be recorded:

1. An analytical benchmark whose closed-form answer is known, solved within the registered tolerance. Reuse the beam benchmark already in `artifacts/work062` as the anchor.
2. A deliberately under-refined mesh, which must produce `unresolved_convergence` rather than a pass.
3. A self-intersecting or multi-solid input, which must produce `unsupported_representation`.
4. A candidate whose declared mass contradicts its geometry-derived mass, which must be rejected.
5. A load case removed from the set, which must change the result and never silently pass.
6. An allowable weakened after the result is seen, which must be rejected as post-observation repair.
7. The same candidate evaluated twice, which must produce identical hashes.
8. One of the 21 Work 062 `refined_disagreement` candidates, evaluated directly. The result must be a registered status from this evaluator, and the record must state plainly whether the earlier cut is confirmed or reversed.

## 9. Acceptance

Accept only when: the analytical benchmark passes; all eight controls behave as registered; convergence is demonstrated on at least three levels for every admitted candidate; mass properties agree between CadQuery and FreeCAD within the registered residuals; every candidate carries one status from section 6; and a clean replay run reproduces the result SHA-256 exactly.

## 10. Comparison fairness

If this evaluator is later used for any comparison, every arm, including the fixed-topology baseline, must be re-evaluated with it under the same mesh, solver, retry and compute registration. Results produced by the scaling-law evaluator must never be compared against results produced by this one.

## 11. Ordered implementation

1. Mesh one Work 135 part from its STEP file and record the Gmsh invocation and mesh identity.
2. Solve that part with CalculiX C3D10 and reproduce the analytical benchmark.
3. Add the three-level refinement and the convergence criterion.
4. Add mass properties from geometry and cross-check them in FreeCAD.
5. Add the status vocabulary, the retry policy and the evidence record.
6. Add the eight controls and their tests.
7. Evaluate the 21 Work 062 `refined_disagreement` candidates and record the outcome.
8. Evaluate a Work 092 free-form solid to demonstrate that a non-template shape is now scorable.

## 12. Proposed validation commands

Replace `python` with the resolved executable that holds each dependency, and record exit codes.

```powershell
python -m unittest tests.test_geometry_general_evaluator -v
python scripts/structural/mesh_step_solid.py --step <part.step> --levels 3 --output artifacts/work138/mesh
python scripts/structural/run_geometry_general_evaluator.py --config config/development/geometry_general_evaluator_v1.json --output-root artifacts/work138/run_a
python scripts/structural/run_geometry_general_evaluator.py --config config/development/geometry_general_evaluator_v1.json --output-root artifacts/work138/run_b --replay-reference artifacts/work138/run_a/result.json
python -m unittest tests.test_repository_contract -v
python -m compileall -q src scripts tests
git diff --check
```

## 13. Risks and handoff

- Cost: a solid solve per candidate is far more expensive than the scaling law. Register the compute budget, keep a cheap pre-filter, and send only survivors to this evaluator. If the budget cannot cover the registered candidate count, reduce the count rather than the refinement.
- Mesh fragility: thin walls, slivers and small fillets in the Work 135 parts may not mesh. That outcome is `unresolved_mesh` evidence and a geometry-quality finding, not permission to simplify the part into a box.
- Scope creep: this work evaluates geometry. It does not change the grammar, the search or the race simulator. Opening the free-form grammar to vehicle candidates is Work 139, and feeding evaluator output into race time is Work 140.
- Honesty: if the 21 re-evaluated candidates turn out to have been correctly cut, record that result. It contradicts the motivating hypothesis and must be reported as found.
