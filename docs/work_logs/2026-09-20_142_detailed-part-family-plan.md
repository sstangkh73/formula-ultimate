# Work 142 Plan: Detailed Part Family and Survey Delta

Thai companion: `2026-09-20_142_detailed-part-family-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Objective

Raise the part families that failed the Work 141 survey — fasteners, seals and rotating or bearing parts — to the registered bar, then re-run the survey with those parts substituted and report the movement as a measured before-and-after.

## Entry evidence

- Work 141 admitted result `ba0616d501b75966db183b6b643fa651ada1617025f6045cf7d42e6a2c9c40b6`: of 44 material definitions, 16 pass, 19 are `insufficient_resolution` and 9 are `unresolved_measurement`. All 4 fasteners and seals fail; 10 of 11 rotating or bearing parts fail.
- Work 140 built one part at the bar already, `reference_m8_bolt`: 34 faces, 17 curved, 85 edges.
- Capability probe on 2026-09-20 built and measured six more candidates under the pinned CadQuery runtime:
  - `nyloc_nut`: 13 faces, 4 curved, 28 edges, 3 scales;
  - `serrated_washer`: 52 faces, 50 curved, 125 edges, 3 scales;
  - `beaded_gasket`: 50 faces, 40 curved, 112 edges, 3 scales;
  - `stepped_axle`: 26 faces, 16 curved, 65 edges, 3 scales;
  - `flanged_bushing`: 14 faces, 9 curved, 23 edges, 3 scales;
  - `slotted_rotor`: 53 faces, 27 curved, 151 edges, 2 scales.
  Each is one valid solid and each clears its class requirement. Three earlier attempts failed and were repaired: a chamfer over every circular edge of the nut, a swept bead on the gasket, and a revolve axis on the bushing.

## Gate tightening in this work

Work 140 counts `engagement_faces` across the pair, so a threaded joint could pass on one threaded part and one plain one. That is too weak: a thread bears on a thread. This work measures engagement faces per side and requires at least one on each part for the `threaded` technology.

The expected consequence is that the reference bolt paired with the nyloc nut still fails, because an internal thread remains unbuildable in this toolchain. Reporting that failure is preferable to passing a joint that only has half a thread.

## Scope

- `scripts/cad/detailed_part_builders.py`: the six new builders, registered so `measure_part_resolution.py` can build them by name.
- `src/formula_ultimate/assembly/part_resolution.py`: per-side engagement-face evidence for threaded joints.
- `scripts/cad/measure_part_resolution.py`: report engagement faces per side.
- `config/development/detailed_part_family_v1.json`: gate the seven upgraded parts and the reference threaded pair.
- `config/development/vehicle_part_resolution_v2.json`: the Work 141 survey with nine definitions substituted by upgraded builds — `bolt`, `nut`, `washer`, `pack_gasket`, `front_axle`, `rear_axle`, `front_bushing`, `rear_bushing` and `motor_rotor`.
- `tests/test_part_resolution.py`: extend for the per-side rule.
- This bilingual plan and its matching bilingual result.

## Validation

1. `python -m unittest tests.test_part_resolution -v`: exit 0.
2. Gate the family: `run_part_resolution_gate.py --config config/development/detailed_part_family_v1.json --output-root artifacts/work142/family_a`, and a replay into `family_b`: exit 0 both times, identical result SHA-256.
3. Re-run the survey: `--config config/development/vehicle_part_resolution_v2.json --output-root artifacts/work142/survey_a`, and a replay into `survey_b`: exit 0 both times, identical result SHA-256.
4. `python -m unittest discover -s tests`, `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: every upgraded part carries `passed_resolution` under the unchanged bar, the survey delta is reported against Work 141 with both runs replaying exactly, and the threaded joint verdict is reported honestly whichever way it lands.

Failure: a requirement is relaxed, a part is declared upgraded without being measured, the substitution is presented as a change to the Work 135 vehicle rather than a proposed upgrade set, or the delta is quoted without both result hashes.

## Risks and non-goals

- Risk: an upgraded part is detailed but functionally wrong — more faces is not better engineering. The result must say that passing means resolution only.
- Risk: the upgraded parts are not dimensionally matched to their vehicle neighbours; they are not installed into the vehicle and no packaging gate is claimed.
- Non-goals: no change to the Work 135 declaration, no contact solve, no race-time coupling, no push beyond what the user has already requested, no history rewrite.
