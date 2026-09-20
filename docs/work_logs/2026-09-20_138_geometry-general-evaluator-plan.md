# Work 138 Plan: Geometry-General Structural Evaluator

Thai companion: `2026-09-20_138_geometry-general-evaluator-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

Execution plan card: `docs/plans/detailed_part_to_vehicle_v1/work138-geometry_general_evaluator.md`

## Objective

Implement the evaluator specified in the Work 138 card: a `STEP -> Gmsh -> CalculiX C3D10 -> properties` path that accepts any valid single solid, derives its own mass properties and load response, returns one registered status per candidate, and replays exactly.

## Capability probe on 2026-09-20 (before implementation)

- `gmsh.exe` meshed `artifacts/work135/run_a/cad/parts/carrier_plate.step` at second order in `1.3 s`: 13,334 nodes, 7,586 C3D10 tetrahedra.
- `ccx.exe` (CalculiX 2.22) solved a C3D10 deck built from that mesh in about `1 s`.
- A deck written with `:.17g` node coordinates was rejected. Controlled probe: CalculiX truncates a free-field numeric at 20 characters. A 21-character scientific value `-1.00000000000000e+03` was read as `-1.0` and produced a displacement `1000x` too small **with exit code 0**; 22 characters and longer abort with exit 201. Work 085 already hit the rejection mode and fixed it inside its own runner. This evaluator must therefore format every numeric field defensively.

## Scope

- `src/formula_ultimate/structural/geometry_general_evaluator.py`: protocol validation, CalculiX-safe number formatting, boundary selection, TRI6-consistent surface loads, C3D10 deck construction, `.dat` parsing with all integration points, mesh mass properties, convergence, and the status vocabulary.
- `scripts/structural/mesh_step_solid.py`: STEP to Gmsh `msh2` at a declared characteristic length, with process and hash evidence.
- `scripts/structural/run_geometry_general_evaluator.py`: the admitted runner, including the analytical benchmark, the eight controls, `result.json` with a canonical SHA-256, and `--replay-reference`.
- `config/development/geometry_general_evaluator_v1.json`.
- `tests/test_geometry_general_evaluator.py`: logic tests that always run, and kernel tests that skip when `gmsh.exe` or `ccx.exe` are absent.
- `docs/contracts/GEOMETRY_GENERAL_EVALUATOR_V1.md` and its Thai companion.
- This bilingual plan and its matching bilingual result.

## Candidates for the admitted run

1. `cantilever_benchmark`: a box beam meshed directly, compared against the Euler-Bernoulli tip deflection. This is control 1.
2. `spine_frame` and `carrier_plate` from Work 135: the heaviest structural part and a carrier, both from their exact occurrence STEP files.
3. `curved_branch_001` from `artifacts/work092/run_e`: a free-form solid that the current campaign evaluator cannot score at all.

## Validation

1. `python -m unittest tests.test_geometry_general_evaluator -v`: exit 0.
2. `python scripts/structural/run_geometry_general_evaluator.py --config ... --output-root artifacts/work138/run_a`: exit 0, every candidate carries one registered status, and the benchmark passes.
3. The same runner into `run_b` with `--replay-reference artifacts/work138/run_a/result.json`: exit 0 and identical result SHA-256.
4. `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: the benchmark meets its registered tolerance, all eight controls behave as registered, every candidate reports a registered status, mesh-derived mass agrees with the Work 135 CadQuery mass within the registered residual, and the replay is exact.

Failure: any candidate silently disappears, a solver failure is recorded as a physical verdict, the benchmark misses its tolerance, or the replay differs.

## Risks and non-goals

- A part may not mesh or converge. That is recorded as `unresolved_*` evidence, not as a failure of the work and not a reason to simplify the part.
- The result is a structural evaluation only. It is not promotion, not manufacturability, not race time and not physical validation.
- Non-goals: no change to the grammar, the search, the race simulator, or the Works 062, 092 and 135 records; no push; no history rewrite.
