# Work 140 Result: Part Resolution and Joint Systems

Thai companion: `2026-09-20_140_part-resolution-joint-systems-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

"Detailed enough" and "a real joint" are now measured gates rather than opinions. Seven parts and three joints were built, measured, meshed and judged; all eight controls were rejected and a clean replay reproduced the result SHA-256 exactly.

The verdict on the existing vehicle is the finding of this work: **the Work 135 fastener and nut fail the resolution bar**, and **the Work 135 fastener joint has no measurable thread interface**.

## Measured results

Result SHA-256 `b61dbe3c0f63240d174df24cf1e800eb68fc0b92c086e30fea4c93a4ce0883a5`; `run_b` matched it exactly. Registered bar: manufacturing floor `5e-05 m`, at least one element across the modelled feature scale, mesh size factor `0.15`, and for the `fastener` class at least 12 faces, 4 curved faces, 20 edges and 3 decade-separated feature scales.

| Part | Status | Faces | Curved | Edges | Scales | Shortest edge | Feature scale | Elements across |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `work135_bolt` | `insufficient_resolution` | 5 | 2 | 6 | 3 | 6.00 mm | 6.00 mm | 1.37 |
| `work135_nut` | `insufficient_resolution` | 9 | 1 | 21 | 2 | 6.00 mm | 6.00 mm | 15.99 |
| `reference_m8_bolt` | `passed_resolution` | 34 | 17 | 85 | 5 | 0.0843 mm | 0.764 mm | 1.14 |
| `bond_plate_lower` / `bond_plate_upper` | `passed_resolution` | 6 | 0 | 12 | 2 | 5.00 mm | 5.00 mm | 4.63 |
| `press_bushing` | `passed_resolution` | 4 | 2 | 6 | 1 | 10.0 mm | 10.0 mm | 20.95 |
| `press_shaft` | `passed_resolution` | 3 | 1 | 3 | 1 | 12.0 mm | 12.0 mm | 33.39 |

| Joint | Technology | Status | Clearance | Mating pairs | Engagement faces |
| --- | --- | --- | ---: | ---: | ---: |
| `work135_pack_threaded` | `threaded` | `unsupported_joint_evidence` | 0.000 mm | 3 | **0** |
| `reference_bonded_lap` | `bonded` | `passed_joint_evidence` | 0.150 mm | 21 | 0 |
| `reference_interference_fit` | `interference` | `passed_joint_evidence` | −0.0200 mm | 3 | 0 |

- **The vehicle fastener is two cylinders.** Measured: 5 faces, 6 edges, and no non-planar, non-cylindrical face anywhere. The reference fastener, built by this work at part resolution with a swept ISO thread, hex head, hex socket and head chamfer, measures 34 faces, 17 curved faces, 85 edges and five decade-separated feature scales, with a shortest edge of `0.0843 mm` — 71 times finer than anything in the vehicle fastener.
- **The vehicle's fastener joint has no thread.** The gate found a mating face pair and a zero clearance, so the two parts do touch, but zero engagement faces: there is no geometry for a thread to bear on. The declared `threaded` technology is therefore unsupported by the geometry.
- **Two technologies passed on measurement alone.** The bonded lap joint measured a `0.150 mm` bond line against a declared `0.100–0.200 mm` range with `5.60e-03 m^2` of overlap, and the interference fit measured `−0.0200 mm` of penetration against a declared `−0.030 to −0.010 mm` range, recovered from the intersection solid as `2V/A`. Both were declared before the run and neither was adjusted afterwards.
- **The bar is technology-neutral.** Nothing in the registry requires a fastener. A weld, a bond, an interference fit or a single continuous solid each satisfy the gate through their own measurable evidence.

## Deviations from plan

The plan named a reference nut with an internal thread. The capability probe had already shown the boolean silently returning an unthreaded bore, so the threaded technology is represented in the admitted run by the Work 135 pack, which fails, and the passing technologies are bonded and interference. The kernel limitation is recorded below rather than papered over with a nut declared to be threaded.

The pilot informed two registered numbers before the admitted run: the mesh size factor moved from `1.0` to `0.15` after the pilot showed `0.24` and then `0.77` elements across the reference fastener's feature scale, and the part-class requirements were set from the pilot's measurements. Nothing was changed after the admitted run.

## Files changed

- `src/formula_ultimate/assembly/part_resolution.py`
- `scripts/cad/measure_part_resolution.py`
- `scripts/development/run_part_resolution_gate.py`
- `config/development/part_resolution_gate_v1.json`
- `tests/test_part_resolution.py`
- `docs/contracts/PART_RESOLUTION_GATE_V1.md` and its Thai companion
- `docs/plans/detailed_part_to_vehicle_v1/work140-part_resolution_joint_systems.md`, its Thai companion, and the bilingual index
- this bilingual plan and result

Generated evidence stays ignored under `artifacts/work140/{pilot,run_a,run_b}`.

## Bug reports

1. **An internal thread cut removes no material.** Symptom: cutting a swept helix from a hex nut left the bore unthreaded — 23 faces, none of them free-form, and a volume equal to the plain bore. The same sweep fuses correctly as an external thread. Root cause: not established; OCCT appears to return the original shape when the boolean fails on the self-intersecting swept tool. Handling: no nut is declared threaded. The finding is recorded and an internal-thread route is left to follow-up work.
2. **Under-head fillet refused.** Symptom: `StdFail_NotDone` when filleting the edge under the reference fastener's head. Handling: the fillet was left out, and the reference part still clears the bar without it.
3. **The measurer assumed its output lived inside the checkout.** Symptom: `ValueError: ... is not in the subpath of 'C:\Formula Ultimate'` when the test wrote into a temporary directory. Fix: `_repository_path` returns a repository-relative path when possible and an absolute one otherwise.
4. **A geometry shortfall masked the mesh verdict.** Symptom: the `mesh_too_coarse_for_feature` control was not rejected, because its subject was the first measured part and that part failed the resolution requirement first. Fix: geometry gates are evaluated before mesh gates, and the control now selects a subject that already clears the geometry gates. A mesh failure is still recorded in `mesh_failure`.

## Validation

Environment: Windows 11, Python 3.14.3, CadQuery 2.8.0 in `.tools/cadquery-mcp`, Gmsh 4.15.0 from `C:/Program Files/FreeCAD 1.1/bin`.

```text
Command: python -m unittest tests.test_part_resolution
Exit code: 0
Result: Ran 21 tests — OK (the CadQuery measurement test ran; it skips where the runtime is absent)

Command: python scripts/development/run_part_resolution_gate.py --config config/development/part_resolution_gate_v1.json --output-root artifacts/work140/run_a
Exit code: 0
Result: passed_part_resolution_gate; parts 5 passed / 2 insufficient; joints 2 passed / 1 unsupported;
        controls 8/8 rejected; result SHA-256 b61dbe3c0f63240d174df24cf1e800eb68fc0b92c086e30fea4c93a4ce0883a5

Command: python scripts/development/run_part_resolution_gate.py --config ... --output-root artifacts/work140/run_b --replay-reference artifacts/work140/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: python -m unittest tests.test_repository_contract
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## Claims

- Supported: the project now has a measured definition of part resolution and a technology-neutral definition of joint evidence; the Work 135 fastener and nut fall below that bar; the Work 135 fastener joint has no thread geometry; a fastener at the required resolution can be built and meshed in this toolchain.
- Not supported: that the rest of the Work 135 vehicle meets or misses the bar, since only its fastener and nut were measured; that any joint carries load, because no force was solved across an interface; anything about manufacturability, race time or physical validation.

## Limitations and follow-up

- Seven parts out of 48 definitions were measured. Running the gate across the whole vehicle is the obvious next step and is cheap: the admitted run took about 45 seconds.
- No contact or tied-surface solve. Interface evidence is geometric only.
- The resolution requirement is a counting rule. It resists the crudest gaming, but a part could in principle add features that carry no function; a functional check belongs with the evaluator, not here.
- An internal thread remains unbuildable in this toolchain, so a fully threaded pair cannot yet pass the `threaded` technology.
- Next: apply the gate to all 48 Work 135 definitions and report the distribution, then raise the parts that fail and re-measure.
