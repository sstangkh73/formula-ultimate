# Work 139: Free-form vehicle candidates

Thai companion: `work139-freeform_vehicle_candidates.th.md`

Status: Planned

Original Work 106 package: none. Forward corrective extension, authored with Work 139 itself.

Dependencies: Work 047 (vehicle assembly primitives), Work 091/092 (free-form wire and solid grammars), Work 138 (geometry-general evaluator).

Mandatory common requirements: [index and execution rules](README.md).

## 1. Outcome and boundary

A vehicle candidate may declare a component as an admitted free-form solid instead of a box or a cylinder, and every component is evaluated by the Work 138 evaluator. Passing means only `passed_freeform_vehicle_composition`: the candidate is buildable, packaged and evaluable. It is not a discovery, not promotion, not race time and not physical validation.

Novel appearance is not evidence. A free-form component earns nothing by being curved; it is evaluated under the same loads, the same evaluator and the same registration as the primitive baseline.

## 2. Why this is needed

`scripts/cad/generate_vehicle_assembly.py` emits a box or a cylinder and nothing else, and the campaign evaluator scores five scale variables rather than geometry. Work 138 removed the evaluation limit. This work removes the composition limit, so a shape from the Work 092 corpus can occupy a functional slot in a vehicle.

## 3. Representation

A component declares either:

- `primitive`: `box` or `cylinder_z`, as today; or
- `freeform_reference`: the Work 092 corpus path, its declaration SHA-256, and an admitted `candidate_id`, with a placement (`translation_m`, `rotation_deg_xyz`).

Only admitted corpus members are allowed in v1. A new free-form declaration must first pass the Work 092 corpus gate. Scaling a corpus member is not permitted, because that would change geometry outside the admitted declaration.

## 4. Packaging gates, measured on the built solids

1. every component is one valid solid;
2. every component lies inside the declared envelope;
3. no pairwise Boolean intersection above the declared tolerance;
4. every declared keep-out stays clear;
5. every required function tag is covered by at least one component;
6. mass properties come from the geometry, never from a declaration.

## 5. Evaluation

Each component is handed to the Work 138 evaluator as a `step_file` candidate with the declared material and load case, and carries back exactly one registered status. A candidate is `evaluable` only when no component is `unsupported_representation`; `unresolved_*` components are reported with their causes, never dropped.

## 6. Matched comparison rule

The admitted run evaluates a primitive baseline and a free-form variant that differ in one component only. Both use the same evaluator, mesh ladder, materials, loads and budgets. The run reports mass and utilization side by side and states plainly that this is a matched evaluation, not a discovery claim: a single pair under one load case cannot establish superiority.

## 7. Mandatory controls

1. a component outside the envelope is rejected;
2. overlapping components are rejected;
3. a missing required function tag is rejected;
4. a corpus hash that does not match the declaration is rejected;
5. a `candidate_id` absent from the admitted corpus is rejected;
6. a declared mass that contradicts the built geometry is rejected;
7. the result carries no discovery, promotion or race-time claim;
8. a clean replay reproduces the result SHA-256 exactly.

## 8. Proposed files

- `src/formula_ultimate/search/freeform_vehicle_candidate.py`
- `scripts/cad/build_freeform_vehicle_candidate.py` (pinned CadQuery runtime)
- `scripts/development/run_freeform_vehicle_candidate.py`
- `config/development/freeform_vehicle_candidate_v1.json`
- `tests/test_freeform_vehicle_candidate.py`
- `docs/contracts/FREEFORM_VEHICLE_CANDIDATE_V1.md` and its Thai companion

## 9. Acceptance

All eight controls rejected, every component carrying one registered status, packaging gates measured on the built solids, and an exact replay.

## 10. Risks and handoff

- A corpus member may not fit any functional slot. Then the candidate stops as `incomplete_composition` rather than being replaced by a box.
- Free-form parts may mesh poorly; that is `unresolved_*` evidence from Work 138, not a verdict on the shape.
- Feeding evaluator output into race time remains Work 140, and searching over free-form compositions remains later work.
