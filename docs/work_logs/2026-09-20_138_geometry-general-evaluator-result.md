# Work 138 Result: Geometry-General Structural Evaluator

Thai companion: `2026-09-20_138_geometry-general-evaluator-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

The evaluator specified by Work 137 exists and runs. A valid single solid is now scored from its own geometry: `STEP -> Gmsh second-order tetrahedra -> CalculiX C3D10 -> mass properties, displacement, von Mises, reaction balance -> one registered status`. Four candidates were evaluated across three refinement levels each, all eight controls were rejected, and a clean replay reproduced the result SHA-256 exactly.

Admitted status is `passed_geometry_general_structural_evaluation`. That is a structural evaluation of the declared solids under the declared load cases. It is not promotion, manufacturability, race time or physical validation.

## Measured results

Result SHA-256 `50e50ed6fa8aa3dfe93804f3a3e67a1471331b203c0da4c1d1c6001d0054d6ec`; `run_b` matched it exactly.

| Candidate | Status | Finest mesh | Mass from mesh | Peak displacement | Peak von Mises | Utilization |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `cantilever_benchmark` | `passed` | 34,122 nodes | 3.9000 kg | 0.591937 mm | 14.51 MPa | 0.0415 |
| `work135_frame_spine` | `passed` | 8,829 nodes | 153.1728 kg | 32.11 mm | 86.44 MPa | 0.3602 |
| `work092_curved_branch` | `unresolved_convergence` | 1,406 nodes | 0.0831 kg | 0.491 mm | 78.61 MPa | 0.3275 |
| `work062_cut_candidate_core` | `passed` | 6,877 nodes | 17.7555 kg | 0.0314 mm | 2.50 MPa | 0.0104 |

- **The analytical benchmark passes.** The finest cantilever level gives `0.5919367 mm` against the Euler-Bernoulli `0.5952381 mm`, a relative error of `0.55%` inside the registered `10%`. The whole chain — mesh, deck, solve, parse — is anchored to a closed form.
- **Mass is derived, not declared.** For `frame_spine` the mesh gives `153.1728 kg` against the Work 135 CadQuery mass `153.1054 kg`, a residual of `0.00044`, well inside the registered `0.05`. The evaluator independently reproduces a CAD mass property from tetrahedra.
- **The heaviest Work 135 part now has load evidence.** Under a declared `10 kN` vertical resultant on its rear face, the spine frame deflects `32 mm` and peaks at `86.4 MPa`, a utilization of `0.36` against the declared `240 MPa` allowable. This is the first time any Work 135 part has been evaluated by physics rather than by a declared thickness.
- **A shape the campaign evaluator cannot score was scored.** `curved_branch_001` from the Work 092 free-form corpus meshed and solved, which the five-variable scaling-law evaluator cannot do at all. Its registered outcome is `unresolved_convergence`: the last two levels changed by `15.7%` in displacement and `42.7%` in p90 stress, against limits of `5%` and `20%`. The registered ladder is not fine enough for this geometry, and the medium level even produced fewer nodes (804) than the coarse level (844), so `Mesh.MeshSizeFactor` is not monotone for it. That is recorded as tooling evidence, not as a verdict on the part, and it was not tuned away after the fact.
- **A Work 062 cut candidate was re-evaluated.** `candidate-000847d87c0270ab` was one of the 21 finalists cut as `refined_disagreement`, and its CAD stage never ran. Its assembly was rebuilt from the sealed variables in `artifacts/work062/result_ledger.jsonl` through `mutate_candidate_assembly`, its core component was exported to STEP with CadQuery, and this evaluator returned `passed` with a utilization of `0.0104`.

**This does not reverse the Work 062 cut, and the card's wording is corrected here.** The Work 062 gate compared a project beam model against CalculiX B31 section forces over the Work 048 load cases; this run applies a different, declared solid load case to one component. The two are not comparable. What is established is narrower and still useful: the geometry of a candidate that the campaign discarded is evaluable, and the discard was a cross-model disagreement rather than a solver failure. A comparable re-evaluation needs the Work 048 load cases applied to the full assembly, which is follow-up work.

## Deviations from plan

The plan listed `carrier_plate` as a candidate alongside `spine_frame`. It was replaced by `work062_cut_candidate_core`, because control 8 needs a Work 062 cut candidate with real geometry and the candidate budget was kept at four. `carrier_plate` remains available and unevaluated.

## Files changed

- `src/formula_ultimate/structural/geometry_general_evaluator.py`
- `scripts/structural/mesh_step_solid.py`
- `scripts/structural/run_geometry_general_evaluator.py`
- `config/development/geometry_general_evaluator_v1.json`
- `tests/test_geometry_general_evaluator.py`
- `docs/contracts/GEOMETRY_GENERAL_EVALUATOR_V1.md` and its Thai companion
- this bilingual plan and result

Generated evidence stays ignored under `artifacts/work138/{inputs,pilot,run_a,run_b}`.

## Bug reports

1. **CalculiX silently truncates a long numeric field.** Symptom: a deck written with `:.17g` node coordinates was rejected with exit 201 and `node 12 is not defined`. Root cause, found by a controlled probe rather than by guessing: CalculiX reads a free field into a 20-character buffer. At 21 characters `-1.00000000000000e+03` was read as `-1.0`, returning **exit code 0** with a displacement `1000x` too small; at 22 characters the run aborts. Work 085 met the abort mode and fixed it inside its own runner; the silent mode is recorded here for the first time. Fix: every numeric field is written by `calculix_number`, which reduces precision until the field fits, and `build_deck` re-checks each numeric field before handing the deck to the solver. Regression: `CalculiXFieldTests` asserts the limit, round-trip accuracy, and refusal of non-finite values.
2. **Curved second-order elements invert.** Symptom: `frame_spine` failed at all three levels with `*ERROR in e_c3d: nonpositive jacobian determinant`, 85 elements at the coarsest level. `Mesh.HighOrderOptimize = 2` reduced it to 5 and `= 4` left 83, so optimization alone does not close it. Root cause: midside nodes curved onto the part's curved boundary produce inverted C3D10 elements. Fix: `Mesh.SecondOrderLinear = 1`, straight-sided quadratic tetrahedra; zero jacobian errors afterwards. The cost, a faceted curved surface, is registered in the contract.
3. **Relative paths broke the mesher.** Symptom: every candidate returned `unresolved_mesh` with `Unable to open file ... part.geo`. Root cause: Gmsh ran with `cwd` set to the work directory while receiving paths relative to the repository root. Fix: resolve both paths before the call.
4. **The field-width guard rejected the heading.** Symptom: every candidate returned `unsupported_representation` with "deck contains a field CalculiX would truncate". Root cause: the guard measured the free-text `*HEADING` continuation line. Fix: the guard skips the heading line and only measures fields that parse as numbers.
5. **The determinism control was itself nondeterministic.** Symptom: `run_b` differed from `run_a` at exactly one value, the `deterministic_restatement` detail hash. Root cause: that control hashed the candidate records including process evidence, which carries wall-clock times. Fix: both the control and the published result hash the same evidence-stripped records. Regression: `run_a` and `run_b` now agree exactly.

## Validation

Environment: Windows 11, Python 3.14.3, Gmsh 4.15.0 and CalculiX 2.22 from `C:/Program Files/FreeCAD 1.1/bin`, CadQuery 2.8.0 in `.tools/cadquery-mcp`.

```text
Command: python -m unittest tests.test_geometry_general_evaluator -v
Exit code: 0
Result: Ran 24 tests — OK (the Gmsh/CalculiX kernel test ran; it skips where the runtimes are absent)

Command: python scripts/structural/run_geometry_general_evaluator.py --config config/development/geometry_general_evaluator_v1.json --output-root artifacts/work138/run_a
Exit code: 0
Result: passed_geometry_general_structural_evaluation; 3 passed, 1 unresolved_convergence; controls 8/8 rejected;
        result SHA-256 50e50ed6fa8aa3dfe93804f3a3e67a1471331b203c0da4c1d1c6001d0054d6ec

Command: python scripts/structural/run_geometry_general_evaluator.py --config ... --output-root artifacts/work138/run_b --replay-reference artifacts/work138/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: .tools/cadquery-mcp/Scripts/python.exe scripts/cad/generate_vehicle_assembly.py --config artifacts/work138/inputs/work062_cut_candidate.json --output-root artifacts/work138/inputs/work062_step --manifest artifacts/work138/inputs/work062_manifest.json
Exit code: 0
Result: 4 valid solids; assembly SHA-256 8ccc596889bd599f0a5cfbbdada58513bd5de2d6b049b9dd87c7615e3c970253

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 988 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## Claims

- Supported: any valid single solid, including a free-form one, can now be meshed, solved and classified; the chain matches a closed form to `0.55%`; mesh-derived mass reproduces the Work 135 CadQuery mass to `0.04%`; the run replays exactly.
- Not supported: that the Work 062 cut was wrong; that the Work 135 spine frame is adequate or optimal, since only one declared load case was applied; that any candidate is manufacturable, promotable or physically validated. Materials are synthetic geometry-only values.

## Limitations and follow-up

- One load case per candidate is evaluated. Multiple cases per candidate are declared in the schema but not yet swept.
- Straight-sided elements approximate curved boundaries; a curvature-aware ladder is needed for parts like `curved_branch_001`, whose refinement ladder is not monotone.
- `artifacts/` is ignored, so the Work 062 candidate's STEP input must be regenerated from the commands above before that candidate can be re-run in a clean checkout.
- `acceptance.py` and `element_verification.py` still write `:.17g` load fields. Plain decimals truncate harmlessly, but a small scientific value would hit bug 1. A separate work item should route those writers through `calculix_number`.
- Next: apply the Work 048 load cases to a full rebuilt Work 062 assembly for a comparable re-evaluation; then Work 139, opening the free-form grammar to vehicle candidates, and Work 140, feeding evaluator output into race time.
