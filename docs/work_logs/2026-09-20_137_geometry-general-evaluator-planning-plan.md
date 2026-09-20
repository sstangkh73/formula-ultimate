# Work 137 Plan: Geometry-General Evaluator Planning

Thai companion: `2026-09-20_137_geometry-general-evaluator-planning-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Objective

Author a bilingual, execution-ready plan for Work 138, a geometry-general structural evaluator. Today the campaign evaluator reads five scale variables, not geometry, so an arbitrary shape cannot be scored at all. Work 138 must replace that with a `STEP -> mesh -> solver -> properties` path that accepts any valid solid.

This work item is planning only. It writes no evaluator, runs no solver and makes no performance claim.

## Entry evidence measured on 2026-09-20

- `artifacts/work062/stage_ledger.jsonl`: 72 finalists entered refinement, 51 passed, and 21 were cut with `refined_disagreement`. In all 21, every holdout case recorded `converged: true` with `fine_cross_model_passed: false`, and their CAD stage recorded `not_run`. The cut was model disagreement, not solver failure.
- `artifacts/work062/result_ledger.jsonl`: 2,880 evaluations, 2,107 `feasible`, 773 `structural_failure`, and no other failure code.
- `src/formula_ultimate/experiments/main_campaign_protocol.py`: the candidate space is five scale variables bounded `0.8`–`1.2`.
- `src/formula_ultimate/experiments/whole_vehicle_search.py`: `capacity_factor` is `min(core_width_scale, contact_radius_scale**2, source_size_scale**2, propulsor_size_scale**2)` and utilization is a frozen Work 048 load scaled by `mass_ratio / capacity_factor`. This is a scaling law tied to one template, not a geometry evaluation.
- `scripts/cad/generate_vehicle_assembly.py`: `shape_for()` emits a box or a cylinder, nothing else.
- `artifacts/work092/run_e/`: ten free-form solids, including `curved_branch` and `organic_load_bridge`, built as one valid solid each with all 18 grammar operators exercised. The free-form grammar works but never reaches a vehicle candidate or the race simulator.
- Runtimes present: CadQuery `2.8.0` in `.tools/cadquery-mcp`, and `gmsh.exe` and `ccx.exe` under `C:/Program Files/FreeCAD 1.1/bin`. `gmsh` is not importable as a Python module, so Work 138 must call the executable, as `scripts/structural/run_beam_bending_acceptance.py` already does.
- Existing seams to reuse: `structural/element_verification.py` parses Gmsh `msh2` and builds C3D4/C3D10 CalculiX decks; `structural/refined_mesh.py` and `structural/acceptance.py` hold refinement and acceptance logic. `structural/geometry_mesh_bridge.py` is a labelled-cell bridge, not a STEP reader, so Work 138 needs a new STEP path.

## Planned files

- `docs/plans/detailed_part_to_vehicle_v1/work138-geometry_general_evaluator.md` and its Thai companion.
- `docs/plans/detailed_part_to_vehicle_v1/README.md` and its Thai companion: add the Work 137 and Work 138 rows with the numbering mapping.
- This bilingual Work 137 plan and its matching bilingual result.

## Validation

1. Static contract check that both plan-card languages contain the required tokens and that both index languages link the new card.
2. `python -m unittest tests.test_repository_contract -v`: exit 0.
3. `git diff --check` and `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: the Work 138 card defines inputs, representation, mesh and solver contracts, refinement registration, negative controls, acceptance, artifacts, replay, tests, risks and non-goals, and every entry number above is traceable to a named artifact or source path. Failure: the card claims capability as implemented, quotes a number with no source, or prescribes a conventional vehicle layout.

## Risks and non-goals

- Risk: a geometry-general evaluator is slower than the scaling law, so a campaign could become unaffordable. The card must register a compute budget and a fidelity ladder rather than assume every candidate can be meshed and solved.
- Risk: replacing the evaluator invalidates comparison against earlier runs. The card must require re-evaluating the baselines with the same evaluator before any comparison.
- Non-goals: no implementation, no solver run, no change to Works 062 or 135 records, no push and no history rewrite.
