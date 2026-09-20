# Work 141 Result: Vehicle Part-Resolution Survey

Thai companion: `2026-09-20_141_vehicle-part-resolution-survey-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

All 44 material definitions of the Work 135 vehicle were measured against the Work 140 bar. Eight controls were rejected and a clean replay reproduced the result SHA-256 exactly. The size of the resolution gap is now a number.

**16 of 44 definitions clear the bar. 19 fall below it. 9 cannot be judged because the registered mesh could not resolve them.** Every fastener and every rotating or bearing part is below the bar.

## Measured distribution

Result SHA-256 `ba0616d501b75966db183b6b643fa651ada1617025f6045cf7d42e6a2c9c40b6`; `run_b` matched it exactly. Four declared voids were excluded and are listed in the declaration.

| Part class | Parts | `passed_resolution` | `insufficient_resolution` | `unresolved_measurement` |
| --- | ---: | ---: | ---: | ---: |
| `structure_or_housing` | 19 | 13 | 2 | 4 |
| `rotating_or_bearing` | 11 | **0** | 10 | 1 |
| `fluid_or_conductor_route` | 6 | 1 | 1 | 4 |
| `fastener_or_seal` | 4 | **0** | 4 | 0 |
| `electronics_module` | 4 | 2 | 2 | 0 |
| **Total** | **44** | **16** | **19** | **9** |

No part was `unmanufacturable_feature`: nothing in the vehicle is a sliver. The problem is the opposite — the parts are too plain.

The parts that clear the bar are `active_stack`, `busbar`, `carrier_plate`, `cold_plate`, `connector`, `contactor`, `energy_lid`, `front_crosshead`, `front_fork_rail`, `front_hub`, `nose_intake_frame`, `radiator`, `rear_beam`, `rear_hub`, `retention_bar` and `support_bracket` — almost all of them boxes or plates with bores, which is exactly the shape the structural minimum was set to accept.

The most common shortfall is curved faces, missing on 11 parts, followed by edge count on 7 and distinct feature scales on 5. Five parts have only 4 faces and three have 5.

Every rotating or bearing part fails. An axle is a plain cylinder, a bushing is a plain annulus, a rotor has no slots, keyways, steps or fillets — none of the geometry that makes a rotating part a rotating part.

`work135_pack_threaded` remains `unsupported_joint_evidence`, unchanged from Work 140: the vehicle's only declared joint technology has no thread geometry behind it.

## Mesh findings

Three parts failed to mesh at the registered factor `0.15`: `spine_frame`, `coolant_supply_tube` and `power_harness`. `spine_frame` meshes at `0.5` and `1.0`, so this is a mesher behaviour at fine sizes on that geometry, not a property of the part. Six more parts meshed but placed fewer than one element across their feature scale. All nine are `unresolved_measurement`: they carry no resolution verdict and no strength claim may rest on them.

Because geometry gates are decided before mesh gates, the 19 `insufficient_resolution` verdicts are unaffected by any mesh behaviour.

## Deviations from plan

The generator script, the generated declaration and a pilot survey were produced before this work's plan record existed, which is the wrong order under the work protocol. The plan was written before the admitted `run_a`, and the pilot's numbers are not cited as evidence. Recording the deviation rather than backdating the plan.

## Files changed

- `scripts/development/build_vehicle_part_resolution_config.py`
- `config/development/vehicle_part_resolution_v1.json`
- `scripts/development/run_part_resolution_gate.py` — the mesh control now lifts a measurement above the requirement when no subject clears the geometry gates, so the control stays testable on a vehicle where most parts fail
- this bilingual plan and result

Generated evidence stays ignored under `artifacts/work141/{pilot,run_a,run_b}`.

## Bug reports

1. **A control became untestable on a failing population.** Symptom: on the vehicle survey the `mesh_too_coarse_for_feature` control would have had no subject that clears the geometry gates, and the run would have failed on a control defect rather than on a finding. Fix: when no subject passes, the control lifts the measured counts to the class requirement before testing the mesh rule. Regression: `tests.test_part_resolution` passes and the survey run rejects 8/8 controls.

## Validation

Environment: Windows 11, Python 3.14.3, CadQuery 2.8.0 in `.tools/cadquery-mcp`, Gmsh 4.15.0 from `C:/Program Files/FreeCAD 1.1/bin`.

```text
Command: python scripts/development/build_vehicle_part_resolution_config.py
Exit code: 0
Result: 44 parts; 4 void definitions excluded; classes structure 19, rotating 11, route 6, fastener 4, electronics 4

Command: python scripts/development/run_part_resolution_gate.py --config config/development/vehicle_part_resolution_v1.json --output-root artifacts/work141/run_a
Exit code: 0
Result: passed_part_resolution_gate; 16 passed / 19 insufficient / 9 unresolved; controls 8/8 rejected;
        result SHA-256 ba0616d501b75966db183b6b643fa651ada1617025f6045cf7d42e6a2c9c40b6

Command: python scripts/development/run_part_resolution_gate.py --config ... --output-root artifacts/work141/run_b --replay-reference artifacts/work141/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: python -m unittest tests.test_part_resolution
Exit code: 0
Result: Ran 21 tests — OK

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## Claims

- Supported: the distribution above, measured on the exact Work 135 STEP parts with a class mapping fixed before the run; no fastener, seal or rotating part in the vehicle reaches the bar; nothing in the vehicle is a sliver.
- Not supported: that the 16 passing parts are good designs — passing means only that they carry more geometry than a plain primitive; that any part is strong, manufacturable or promotable; that the 9 unresolved parts are either adequate or inadequate.

## Limitations and follow-up

- The requirement is still a counting rule. A part could add featureless geometry to pass; a functional check belongs with the evaluator.
- The class mapping uses the vehicle's own occurrence classes. A mislabelled occurrence class would place a part in the wrong class, and the mapping inherits that error.
- Nine parts have no verdict until the mesh route is fixed for them.
- Next: raise the fastener and rotating-part families to the bar, starting from the Work 140 reference fastener, and re-run this survey to measure the movement. After that, the interface work: force crossing a joint.
