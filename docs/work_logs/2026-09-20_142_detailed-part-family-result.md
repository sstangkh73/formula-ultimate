# Work 142 Result: Detailed Part Family and Survey Delta

Thai companion: `2026-09-20_142_detailed-part-family-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

Seven parts were built at part resolution and gated, and the vehicle survey was re-run with nine definitions substituted by those builds. Both pairs of runs rejected all eight controls and replayed exactly.

The geometry moved a long way. The verdicts moved less, because raising part detail raises what the mesh must resolve, and the registered mesh is now the binding constraint.

## Family run

`artifacts/work142/family_a`, result SHA-256 `744463abe5e1daa2d6cc1920d245284d678e8672a6b9b2f2c2c9a8edf46a07eb`, replayed exactly by `family_b`. Registered mesh size factor `0.08`, chosen from the pilot before the admitted run; every other number of the bar is unchanged from Work 140.

| Part | Status | Faces | Curved | Edges | Elements across |
| --- | --- | ---: | ---: | ---: | ---: |
| `reference_m8_bolt` | `passed_resolution` | 28 | 17 | 73 | 2.13 |
| `detailed_nyloc_nut` | `passed_resolution` | 13 | 4 | 28 | 8.07 |
| `detailed_serrated_washer` | `passed_resolution` | 52 | 50 | 125 | 1.88 |
| `detailed_stepped_axle` | `passed_resolution` | 17 | 7 | 42 | 1.03 |
| `detailed_flanged_bushing` | `passed_resolution` | 14 | 9 | 23 | 1.84 |
| `detailed_slotted_rotor` | `passed_resolution` | 53 | 27 | 151 | 1.18 |
| `detailed_beaded_gasket` | `unresolved_measurement` | — | — | — | — |

The gasket carries no measurements because its own build is not byte-reproducible; see the bug reports.

**The threaded joint still fails, as expected.** `reference_threaded_pair` is `unsupported_joint_evidence` with engagement faces `[2, 0]`: the bolt carries thread flanks and the nut does not, because an internal thread remains unbuildable here. The tightened rule introduced in this work is what makes that visible — Work 140 counted engagement faces across the pair, so this joint would have passed on the bolt's thread alone.

## Survey delta

`artifacts/work142/survey_a`, result SHA-256 `8d4e4e5e926c2af5af4b3bfdc9e33c7da57d14af930c768329c81af54c08acdf`, replayed exactly by `survey_b`. The bar is identical to Work 141, including the mesh size factor `0.15`, so the two runs are comparable.

| Status | Work 141 (`ba0616d5`) | Work 142 (`8d4e4e5e`) | Change |
| --- | ---: | ---: | ---: |
| `passed_resolution` | 16 | 18 | **+2** |
| `insufficient_resolution` | 19 | 11 | **−8** |
| `unresolved_measurement` | 9 | 15 | **+6** |
| `unmanufacturable_feature` | 0 | 0 | 0 |

Per substituted definition:

| Definition | Work 141 | Work 142 | Faces |
| --- | --- | --- | --- |
| `washer` | `insufficient_resolution` | `passed_resolution` | 4 → 52 |
| `nut` | `insufficient_resolution` | `passed_resolution` | 9 → 13 |
| `bolt` | `insufficient_resolution` | `unresolved_measurement` | 5 → 33 |
| `motor_rotor` | `insufficient_resolution` | `unresolved_measurement` | 6 → 53 |
| `front_bushing` / `rear_bushing` | `insufficient_resolution` | `unresolved_measurement` | 4 → 14 |
| `rear_axle` | `insufficient_resolution` | `unresolved_measurement` | 8 → 17 |
| `front_axle` | `unresolved_measurement` | `unresolved_measurement` | 12 → 17 |
| `pack_gasket` | `insufficient_resolution` | `unresolved_measurement` | 10 → not reproducible |

No unsubstituted definition changed status, which is the expected behaviour of a controlled substitution.

**How to read this.** Every substituted part now carries the geometry its class requires — that is the geometric result, and it is unambiguous. Seven of the nine nevertheless carry no verdict, because at mesh factor `0.15` the solver cannot resolve their new features: the bolt reaches `0.20` elements across its feature scale, the bushings `0.99`, the axles `0.56`, the rotor `0.64`. The family run shows those same parts resolving at factor `0.08`. Detail is not free: it moves work from the modeller to the mesher.

## Deviations from plan

The plan expected the upgraded parts to land in `passed_resolution` in the survey. Seven landed in `unresolved_measurement` instead, for the mesh reason above. The registered survey bar was deliberately left at Work 141's value rather than loosened or refined, so that the two surveys remain comparable; refining it after seeing the result would have been post-observation repair.

## Files changed

- `scripts/cad/detailed_part_builders.py`: the seven builders, plus the three simple reference shapes moved out of the measurer.
- `scripts/cad/measure_part_resolution.py`: builders imported from the library; per-side engagement faces; STEP session-counter canonicalisation; a second build of every part to detect an irreproducible build.
- `scripts/structural/mesh_step_solid.py`: Gmsh pinned to one thread.
- `src/formula_ultimate/assembly/part_resolution.py`: `threaded` now requires engagement geometry on both parts.
- `scripts/development/build_vehicle_part_resolution_config.py`: the `--upgrade` substitution set.
- `config/development/detailed_part_family_v1.json`, `config/development/vehicle_part_resolution_v2.json`.
- `tests/test_part_resolution.py` was already covering the paths this work touched and needed no change beyond passing unchanged.
- this bilingual plan and result.

Generated evidence stays ignored under `artifacts/work142/`.

## Bug reports

1. **Gmsh returned a different mesh for the same input between runs.** Symptom: `family_b` differed from `family_a` in node count and characteristic length for the gasket, so the replay was not exact. Root cause: Gmsh meshes with several threads by default and the resulting node set is not reproducible. Fix: pin `General.NumThreads` and `Mesh.MaxNumThreads1D/2D/3D` to 1 in both geo writers. Consequence to state plainly: runs recorded before this change — Works 138, 139, 140 and 141 — would produce different hashes if re-run now. Their recorded evidence stands as what those runs produced; it is not re-derivable under the pinned mesher.
2. **OCCT parallel booleans varied a volume in the last unit in the last place.** Symptom: the gasket's measured volume differed between runs at the seventeenth digit. Fix: `BOPAlgo_Options.SetParallelMode_s(False)` in the builder library.
3. **A STEP file carried a per-process export counter.** Symptom: exporting the same solid twice in one process produced two different SHA-256 values; the only difference was `Open CASCADE STEP translator 7.9 1` versus `... 2` in the product name. Fix: canonicalise that counter alongside the timestamp.
4. **An irreproducible build had no status.** Symptom: after fixes 1 to 3 the gasket still produced different bytes between two builds in one run. Fix: the measurer now builds every part twice and, when the two builds differ, records `unresolved_measurement` with the cause and no numbers, so the run stays replayable and the problem is visible rather than silently varying. The gasket is the one part in this family that hits it; its build uses a fillet over a selected edge set after a boolean, which is the likely source.
5. **A threaded joint could pass on one thread.** Symptom: engagement faces were counted across the pair. Fix: per-side counts, with `threaded` requiring at least one on each part. The reference pair now fails honestly.

## Validation

Environment: Windows 11, Python 3.14.3, CadQuery 2.8.0 in `.tools/cadquery-mcp`, Gmsh 4.15.0 pinned to one thread.

```text
Command: python -m unittest tests.test_part_resolution
Exit code: 0
Result: Ran 21 tests — OK

Command: run_part_resolution_gate.py --config config/development/detailed_part_family_v1.json --output-root artifacts/work142/family_a
Exit code: 0
Result: passed_part_resolution_gate; 6 passed / 1 unresolved; controls 8/8; SHA-256 744463abe5e1daa2...

Command: the same into family_b with --replay-reference
Exit code: 0
Result: replay exact: true

Command: run_part_resolution_gate.py --config config/development/vehicle_part_resolution_v2.json --output-root artifacts/work142/survey_a
Exit code: 0
Result: passed_part_resolution_gate; 18 passed / 11 insufficient / 15 unresolved; controls 8/8; SHA-256 8d4e4e5e926c2af5...

Command: the same into survey_b with --replay-reference
Exit code: 0
Result: replay exact: true

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests ; git diff --check ; git diff --cached --check
Exit code: 0
```

## Claims

- Supported: seven parts were built at the declared resolution and six of them clear the bar under a mesh fine enough to resolve them; substituting nine of them into the survey removes eight `insufficient_resolution` verdicts; both run pairs replay exactly under the pinned toolchain.
- Not supported: that any upgraded part is correct for the vehicle — none is dimensionally matched to its neighbours, none was installed, and no packaging gate was run on them; that a threaded joint anywhere in this project yet has thread evidence on both sides; that more faces means better engineering.

## Limitations and follow-up

- Seven of nine substituted parts have no verdict in the survey until either the registered mesh is refined for the whole survey — which would break comparability with Work 141 unless Work 141 is also re-run — or a per-class mesh registration is introduced.
- The gasket build must be made reproducible before it can carry any measurement.
- An internal thread is still unbuildable, so `threaded` cannot yet pass anywhere.
- Earlier recorded hashes are not re-derivable under the pinned mesher; a future work should re-run Works 138 to 141 and record the new identities if they are to be replayed.
