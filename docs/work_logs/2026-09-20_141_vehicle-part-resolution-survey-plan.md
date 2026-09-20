# Work 141 Plan: Vehicle Part-Resolution Survey

Thai companion: `2026-09-20_141_vehicle-part-resolution-survey-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Objective

Apply the Work 140 gate to every material definition in the Work 135 vehicle and report the distribution of verdicts, so the size of the resolution gap is a number rather than an impression.

## Entry evidence

- Work 140 established the gate and measured seven subjects. Its admitted result is `b61dbe3c0f63240d174df24cf1e800eb68fc0b92c086e30fea4c93a4ce0883a5`.
- The Work 135 vehicle declares 48 definitions, of which 4 are declared voids with zero structural density.
- Mesh cost probe at the registered factor `0.15`: seven of the largest parts meshed in `7.7 s` in total, so surveying the whole vehicle is cheap. `spine_frame` failed to mesh at `0.15` while meshing at `0.5` and `1.0`; that is expected to surface as `unresolved_measurement`, and the geometry verdict is decided before the mesh verdict in any case.
- A pilot survey of all 44 material definitions ran before this record was written, to size the work and to confirm the class mapping produced sensible groups. Its numbers are not the admitted evidence; `run_a` below is.

## Scope

- `scripts/development/build_vehicle_part_resolution_config.py`: derive the survey declaration from the Work 135 vehicle, assigning each definition a part class by a rule over the occurrence classes the vehicle itself declares. Void definitions are excluded and listed.
- `config/development/vehicle_part_resolution_v1.json`: the generated declaration, committed so the run is reproducible.
- The Work 140 runner, unchanged apart from one repair: when no subject clears the geometry gates, the mesh control lifts a measurement above the requirement so that the control remains testable.
- This bilingual plan and its matching bilingual result.

## Registered bar

Unchanged from Work 140: manufacturing floor `5e-05 m`, at least one element across the modelled feature scale, mesh size factor `0.15`. Part-class requirements are engineering minimums set above a plain primitive — a box has 6 faces and 12 edges, and the structural minimum is 8 faces and 14 edges.

## Validation

1. `python scripts/development/build_vehicle_part_resolution_config.py`: exit 0, 44 parts, 4 voids excluded.
2. `python scripts/development/run_part_resolution_gate.py --config config/development/vehicle_part_resolution_v1.json --output-root artifacts/work141/run_a`: exit 0, eight controls rejected, one registered status per definition.
3. The same runner into `run_b` with `--replay-reference`: exit 0 and an identical result SHA-256.
4. `python -m unittest tests.test_part_resolution -v`, `python -m unittest discover -s tests`, `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: every material definition carries exactly one registered status, the class mapping is rule-based and auditable, all controls are rejected, and the replay is exact.

Failure: a definition is dropped from the survey, a requirement is relaxed after seeing the distribution, or the result is presented as a verdict on the vehicle's performance rather than on its geometry.

## Risks and non-goals

- Risk: a large share of the vehicle fails. That is the measurement, and it is reported as found.
- Risk: the class mapping flatters the vehicle. Mitigation: the rules are fixed before the run, derived only from occurrence classes, and printed with the generated declaration.
- Non-goals: no redesign of any part, no contact solve, no race-time coupling, no push, no history rewrite.
