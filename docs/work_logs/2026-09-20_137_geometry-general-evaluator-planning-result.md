# Work 137 Result: Geometry-General Evaluator Planning

Thai companion: `2026-09-20_137_geometry-general-evaluator-planning-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

Authored the bilingual, execution-ready Work 138 card for a geometry-general structural evaluator, and recorded the numbering mapping in the bilingual detailed-plan index. The card requires a `STEP -> Gmsh -> CalculiX C3D10 -> properties` path that accepts any valid solid, a six-value status vocabulary that separates `failed_physics` from `unresolved_mesh`, `unresolved_solver` and `unresolved_convergence`, eight falsification controls, three or more refinement levels, a compute budget, and exact replay.

This work item changed planning evidence only. It implemented no evaluator, ran no mesher or solver, and made no performance, feasibility or promotion claim.

## Measured entry evidence behind the card

Every number in the card traces to a named path, measured in this session:

- `artifacts/work062/stage_ledger.jsonl`: 72 refinement results — 51 `passed`, 21 `failed` with `refined_disagreement`; 72 CAD witnesses — 51 `passed`, 21 `not_run`. Across all 21 cut candidates, every holdout case has `converged: true` and `fine_cross_model_passed: false`. The cut was cross-model disagreement, not solver failure.
- `artifacts/work062/result_ledger.jsonl`: 2,880 evaluations — 2,107 `feasible`, 773 `structural_failure`, no other failure code.
- `artifacts/work092/run_e/`: 10 free-form solids, each one valid solid, covering all 18 grammar operators.
- Source paths for the template lock: `main_campaign_protocol.py` (five scale variables, `0.8`–`1.2`), `whole_vehicle_search.py` (the `capacity_factor` scaling law), `generate_vehicle_assembly.py` (box or cylinder only), and `config/development/native_detailed_vehicle_v1.json` (48 hand-written part kinds).

Counts found elsewhere in `artifacts/` — for example `unsupported_overhang` 24 and `unsupported_wall` 12 — were **not** used as evidence. `artifacts/work095/run_a/result.json` distributes exactly one of each rejection cause across six families and states `"matched synthetic gate behavior only; no source STEP"`, so it is a designed fixture matrix rather than a measured yield.

## Files changed

- `docs/plans/detailed_part_to_vehicle_v1/work138-geometry_general_evaluator.md` and its Thai companion.
- `docs/plans/detailed_part_to_vehicle_v1/README.md` and its Thai companion.
- This bilingual Work 137 plan and result.

## Decisions

- **Evaluator before grammar.** Opening the free-form grammar first would produce candidates the evaluator cannot score, so they would be cut for lack of an evaluator. The card therefore fixes evaluation first and defers the grammar to Work 139 and the race-time coupling to Work 140.
- **Status vocabulary.** `unresolved_*` is separated from `failed_physics` so that a solver limitation is never recorded as a physical verdict, and so the unresolved cause distribution becomes the evidence for what capability to add next.
- **Control 8.** Re-evaluating the 21 `refined_disagreement` candidates is mandatory, and the card requires reporting a confirmation of the original cut just as plainly as a reversal.
- **Comparison fairness.** The card forbids comparing scaling-law results against evaluator results, and requires re-evaluating baselines with the same registration.
- **Runtime access.** `gmsh` is not importable in the pinned CadQuery environment, so the card specifies calling `gmsh.exe` under `C:/Program Files/FreeCAD 1.1/bin`, as `scripts/structural/run_beam_bending_acceptance.py` already does. `ccx.exe` is present in the same directory.
- **Numbering.** 136 and 137 are consumed. The native-solid physics rerun that Work 135 calls "Work 136" takes the next unused number at execution. The index records this without rewriting Work 135.

## Validation

Environment: Windows 11, Python 3.14.3.

```text
Command: static Work 138 bilingual plan and index contract check (14 required tokens per language, Thai source reference, both index links)
Exit code: 0
Result: work138_plan_contract: PASS

Command: python -m unittest tests.test_repository_contract
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check
Exit code: 0

Command: git diff --cached --check
Exit code: 0
```

## Claims

- Supported: the entry numbers above are reproducible from the named artifact files at this commit.
- Not supported: that a geometry-general evaluator exists, that meshing the Work 135 parts will succeed, or that the 21 cut candidates would pass under it. Those are open questions the card is designed to answer.

## Limitations and follow-up

The Work 138 commands are documented, not executed. No mesh, solve, evaluator module, configuration or test exists from this work item. The next execution item is Work 138; Work 139 and Work 140 still need their own cards.
