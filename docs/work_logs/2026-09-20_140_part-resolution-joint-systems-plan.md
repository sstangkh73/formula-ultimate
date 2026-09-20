# Work 140 Plan: Part Resolution and Joint Systems

Thai companion: `2026-09-20_140_part-resolution-joint-systems-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

Execution plan card: `docs/plans/detailed_part_to_vehicle_v1/work140-part_resolution_joint_systems.md`

## Objective

Give the project a measurable definition of "detailed enough" and a technology-neutral definition of "a real joint", then apply both to the existing vehicle and report the verdict honestly.

## Entry evidence measured on 2026-09-20

- All 48 Work 135 definitions declare exactly three features; the smallest declared dimension in the vehicle is `1.5 mm` (washer thickness) and the median smallest feature per part is `6.0 mm`.
- The Work 135 fastener is `{"kind": "bolt_z", "shaft_radius_m": 0.004, "shaft_length_m": 0.28, "head_radius_m": 0.008, "head_height_m": 0.006}`: two cylinders, no thread, no chamfer, no bearing face.
- `config/cad/freeform_brep_solid_grammar_v2.json` already allows `minimum_feature_m = 1e-05` and 32 features per candidate, so the kernel is not the limit.
- Capability probe: a swept M8 thread fuses into a valid single solid in `0.4 s` (21 faces, 17 curved). A full reference bolt with hex head, hex socket and chamfer builds in `0.5 s` as one valid solid with 34 faces, 17 curved, 85 edges, smallest face area `0.1544 mm^2` and smallest edge `0.0843 mm`. An under-head fillet raised `StdFail_NotDone` and was left out.
- Capability probe: cutting an internal thread from a hex nut removed no measurable material — the boolean silently returned an unthreaded bore. This is recorded as a kernel limitation and will be reported as `unresolved_measurement`, not worked around by declaring the nut threaded.

## Scope

- `src/formula_ultimate/assembly/part_resolution.py`: declaration schema, the joint-technology registry and its required evidence, the resolution gates, the status vocabulary and the run summary.
- `scripts/cad/measure_part_resolution.py`: under the pinned CadQuery runtime, build the reference parts, import declared STEP parts, and measure faces, edges, curved faces, surface types, smallest face area, smallest edge, volume, bounding box; per joint, measure minimum distance, interference volume and mating-face pairs.
- `scripts/development/run_part_resolution_gate.py`: run the measurement, apply the gates, check mesh resolution with the Work 138 mesher, run eight controls, write `result.json` with a canonical SHA-256 and support `--replay-reference`.
- `config/development/part_resolution_gate_v1.json`, `tests/test_part_resolution.py`, the bilingual contract, the bilingual plan card, the index rows, and this bilingual plan and result.

## Validation

1. `python -m unittest tests.test_part_resolution -v`: exit 0.
2. `python scripts/development/run_part_resolution_gate.py --config ... --output-root artifacts/work140/run_a`: exit 0, eight controls rejected, one registered status per subject.
3. The same runner into `run_b` with `--replay-reference`: exit 0 and an identical result SHA-256.
4. `python -m unittest discover -s tests`, `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: every gate number is measured on built geometry, every subject carries one registered status, all controls are rejected, and the replay is exact.

Failure: a gate is relaxed after seeing a result, a kernel refusal is hidden behind a simplified part, a subject disappears from the accounting, or the run claims more than a geometry verdict.

## Risks and non-goals

- The Work 135 fastener is expected to fail. Reporting that is the point of the work.
- Non-goals: no contact or tied-surface solve across joints, no redesign of the Work 135 vehicle, no race-time coupling, no push, no history rewrite.
