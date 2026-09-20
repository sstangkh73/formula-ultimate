# Work 139 Result: Free-form Vehicle Candidates

Thai companion: `2026-09-20_139_freeform-vehicle-candidates-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

A vehicle candidate can now hold a free-form solid in a functional slot. Two candidates were declared, built in CadQuery, gated on their built solids and evaluated component by component with the Work 138 evaluator. All eight controls were rejected and a clean replay reproduced the result SHA-256 exactly.

Admitted status is `passed_freeform_vehicle_composition`: the candidates are buildable, packaged and evaluable. The summary carries `discovery_claim`, `promotion_allowed`, `race_time_claim` and `physical_validation` as false, and one control asserts exactly that.

## Measured results

Result SHA-256 `5f4a0e831d91dd7dc27496f6c4e8e0280aaca94a1e5ca6c9ce4c254c2bef2874`; `run_b` matched it exactly.

| Candidate | Packaging | Mass | Components | Statuses |
| --- | --- | ---: | ---: | --- |
| `primitive_baseline_139` | `passed` | 30.6572 kg | 4 | 4 × `passed` |
| `freeform_variant_139` | `passed` | 28.0482 kg | 4 | 3 × `passed`, 1 × `unresolved_convergence` |

The pair differs in one component, `propulsor`:

| | Baseline | Free-form variant |
| --- | --- | --- |
| Geometry | `box` 0.1 × 0.1 × 0.1 m | `curved_branch_001` from the Work 092 corpus |
| Curved faces | 0 | 3 |
| Component mass | 2.7000 kg | 0.0911 kg |
| Component status | `passed` | `unresolved_convergence` |
| Utilization | 0.000868 | 0.304135 |
| Candidate mass | 30.6572 kg | 28.0482 kg (`-2.6089 kg`) |

Both candidates measured zero pairwise intersection and zero keep-out invasion on the built solids. The core, source and contact components are identical across the pair and returned identical numbers, which is the expected behaviour of a matched pair.

**What this establishes, and what it does not.** It establishes that an admitted free-form solid can occupy a functional slot, survive packaging gates measured on the built geometry, and be scored by the same evaluator as a primitive. It does **not** establish that the curved part is better. Its mass advantage comes with a `0.304` utilization against `0.000868`, a factor of 350 more of its allowable consumed, and its convergence is unresolved on the registered ladder. One substitution under one declared load case cannot support a superiority, discovery or promotion claim, and the result file states this in `matched_report.interpretation`.

## Deviations from plan

None. The plan's scope, validation and non-goals were followed as written.

## Files changed

- `src/formula_ultimate/search/freeform_vehicle_candidate.py`
- `scripts/cad/build_freeform_vehicle_candidate.py`
- `scripts/development/run_freeform_vehicle_candidate.py`
- `config/development/freeform_vehicle_candidate_v1.json`
- `tests/test_freeform_vehicle_candidate.py`
- `docs/contracts/FREEFORM_VEHICLE_CANDIDATE_V1.md` and its Thai companion
- `docs/plans/detailed_part_to_vehicle_v1/work139-freeform_vehicle_candidates.md`, its Thai companion, and the bilingual index
- this bilingual plan and result

Generated evidence stays ignored under `artifacts/work139/{pilot,run_a,run_b}`.

## Bug reports

1. **Repository-relative paths broke the builder.** Symptom: the build aborted with `'artifacts\work139\pilot\cad\primitive_baseline_139\core.step' is not in the subpath of 'C:\Formula Ultimate'`. Root cause: the builder called `Path.relative_to(ROOT)` on an output path the runner had passed as a relative path. Fix: `_repository_path` resolves against the working directory first, then takes the repository-relative POSIX form.
2. **The determinism control hashed the wrong records.** Symptom: `AttributeError: 'list' object has no attribute 'get'` while running the controls. Root cause: the control re-applied `strip_process_evidence` to a list of already-stripped component lists. Fix: the control hashes the reported records directly and compares against a JSON round trip of them.
3. **The manifest hash depended on the output directory.** Symptom: `run_b` differed from `run_a` at both `manifest_sha256` values and therefore at the result hash, although every STEP hash matched. Root cause: the hashed manifest body included `step_path` and `assembly_step_path`, which contain the run directory. Fix: the manifest hash now covers geometry identity only — the paths are kept in the manifest for use but excluded from the hash. Regression: `run_a` and `run_b` now produce the same result SHA-256.

## Validation

Environment: Windows 11, Python 3.14.3, CadQuery 2.8.0 in `.tools/cadquery-mcp`, Gmsh 4.15.0 and CalculiX 2.22 from `C:/Program Files/FreeCAD 1.1/bin`.

```text
Command: python -m unittest tests.test_freeform_vehicle_candidate -v
Exit code: 0
Result: Ran 13 tests — OK (the CadQuery builder test ran; it skips where the runtime is absent)

Command: python scripts/development/run_freeform_vehicle_candidate.py --config config/development/freeform_vehicle_candidate_v1.json --output-root artifacts/work139/run_a
Exit code: 0
Result: passed_freeform_vehicle_composition; controls 8/8 rejected; 1 unresolved component;
        result SHA-256 5f4a0e831d91dd7dc27496f6c4e8e0280aaca94a1e5ca6c9ce4c254c2bef2874

Command: python scripts/development/run_freeform_vehicle_candidate.py --config ... --output-root artifacts/work139/run_b --replay-reference artifacts/work139/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1001 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: python -m unittest tests.test_repository_contract
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## Claims

- Supported: an admitted free-form solid composes into a vehicle candidate, passes envelope, intersection, keep-out and function-coverage gates measured on the built solids, and is scored by the Work 138 evaluator; the run replays exactly.
- Not supported: that the free-form variant is better, lighter in any useful sense, or a discovery; that the corpus member is suitable for propulsion beyond occupying the slot geometrically; that any candidate is promotable, manufacturable or physically validated.

## Limitations and follow-up

- Corpus members may be placed but not scaled, so slot fit is a matter of luck rather than design. A parametric free-form family is follow-up work.
- The free-form component remains `unresolved_convergence` on the registered ladder, inherited from the Work 138 limitation; a curvature-aware refinement ladder would resolve it.
- Only one load case per component, and no assembly-level load path: components are evaluated in isolation, not as a connected structure.
- The vehicle-level mass is a sum of component masses; there is no joint, fastener or interface mass.
- Next: Work 140, feeding evaluator output into race time, and then a search over free-form compositions rather than a single declared pair.
