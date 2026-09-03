# Work 088 Result: Whole Mechanical Vehicle Candidate 001 Admission Audit

Thai companion: `2026-09-04_088_whole-mechanical-vehicle-candidate-001-result.th.md`

## Status and outcome

Status: Completed

The admission audit completed successfully and returned `candidate_verdict=not_ready`. This means the audit mechanism is complete; it does **not** mean the mechanical vehicle candidate is complete or ready for whole-vehicle research.

The audit identity-verified the exact Work 083, 084, 086, and 087 results; all seventeen individual STEP files; the seventeen-solid assembly STEP; and the FCStd file. It produced coverage records for all thirteen required artifact classes and evaluated all eleven preregistered whole-candidate cases. Every case is visibly blocked by at least one preserved upstream blocker. The Level-0 decision is `not_run_pre_admission_blocked`, with `attempted=false`.

## Decisive blockers

1. `forbidden_work083_work084_geometry_interference`: eight cross-system pairs have positive overlap and one additional forbidden pair has zero clearance.
2. `work083_vertical_motion_breaks_rigid_work084_coaxial_butt_interface`: maximum misalignment is `0.007 m` against a `1e-6 m` tolerance.
3. `new_load_frame_has_no_meshed_convergence_evidence`.
4. `synthetic_material_process_evidence`.

No threshold, geometry, source identity, or blocker was changed after observing the result.

## Files changed

- `config/candidates/whole_mechanical_vehicle_candidate_001.json`
- `src/formula_ultimate/experiments/whole_mechanical_vehicle_candidate.py`
- `scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py`
- `tests/test_whole_mechanical_vehicle_candidate_001.py`
- `docs/contracts/WHOLE_MECHANICAL_VEHICLE_CANDIDATE_001.md` and Thai companion
- this result and its Thai companion
- the Work 088 plan and Thai companion, changed to `Completed`

Generated audit/replay evidence under `artifacts/work088/` is ignored and was not committed. It identity-references the exact CAD under `artifacts/work087/run_b/` rather than duplicating or mutating it.

## Exact evidence

- Config identity: `72bc6714765f24dbf09c09e9de5cd684ee507b54d30d54c6afddaf51743c0843`.
- Result identity: `fea24fccd400d98b8b951f9bf1336310fc43689935c4c9b75dcb4173e84d9a24`.
- Byte-identical result JSON SHA-256: `17e5efe1c1ad84465a1f9f4ebcef80b8c86ae8c68fa76fe93a6037ba8f33ebc0`.
- Admission report identity: `0f8271d156f49cd90b1184d773f630c58fa0fe7bb8cb91a084abe313e1eb9ebc`; file SHA-256 `e29d9aa3e97dcdd09228bd9918300d7c47d762380616fdc05ed4840e233c056a`.
- Artifact manifest identity: `9cfbcf225a507895f18f019c32a255b066986b08a782effddaca771ce63ad14f`; file SHA-256 `0bf43b3f0d49373f8c1726a5594480198e21856df49826d37d0adb05103ae611`.
- Geometry identity: `17` individual STEP files, assembly STEP `33c1ade66729602bf9d022c36af017690ce1783364d38fddc71604684e62ee7d`, FCStd `4c792bbe1cb2a7bf796087b316b5e2369357d093eb051c0591f642b3238a578d`.
- Coverage: `13/13` required artifact classes; `11/11` admission cases evaluated; `0/11` ready.
- Replay: `run_b/result.json` is byte-identical to `run_a/result.json`.

## Exact validation commands and results

```powershell
python -m unittest tests.test_whole_mechanical_vehicle_candidate_001 tests.test_repository_contract -v
# exit 0; Ran 18 tests; OK

python -m compileall -q src scripts tests
# exit 0

python scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py `
  --config config/candidates/whole_mechanical_vehicle_candidate_001.json `
  --output-root artifacts/work088/run_a
# exit 0; audit_status=passed; candidate_verdict=not_ready

python scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py `
  --config config/candidates/whole_mechanical_vehicle_candidate_001.json `
  --output-root artifacts/work088/run_b `
  --replay-reference artifacts/work088/run_a/result.json
# exit 0; byte-identical replay

python -m unittest discover -s tests -q
# exit 0; Ran 620 tests in 342.715s; OK (skipped=3)
```

## Evidence review and limitations

Supporting evidence for the audit is exact source/file hashing, actual presence and identity of every CAD file, full required-class coverage, full case coverage, causal negative controls, and exact replay. Contradicting evidence against candidate admission is the direct B-rep interference, incompatible rigid/moving interface, missing integrated-frame mesh evidence, and synthetic-only material/process evidence. An alternative explanation based on numerical tolerance is implausible for the largest overlap because it is more than seven orders of magnitude above the `1e-12 m3` gate; nevertheless, future repackaging must be evaluated from new geometry rather than by reclassifying current contacts.

The evidence still does not establish a collision-free complete vehicle, integrated structural survival, fatigue/fracture/buckling coverage, design-eligible materials, crashworthiness, safety, race completion, higher-fidelity validity, or physical validation. The next work must remediate geometry and interface architecture before repeating the integrated mesh and admission sequence.
