# Work 087 Result: Load Structure, Packaging, and Thermal Integration

Thai companion: `2026-09-04_087_load-structure-packaging-thermal-integration-result.th.md`

## Status and outcome

Status: Partial

The work produced an inspectable, geometry-causal integration witness with the exact five Work 083 parts, exact seven Work 084 parts, and five newly generated integration solids. The bundle contains seventeen per-part STEP files, a seventeen-solid assembly STEP, and an FCStd document with seventeen named solid objects. No box was substituted for a functional part and no collision was silently repaired.

The candidate is correctly `not_admitted`. Eight forbidden cross-system pairs have positive overlap, one additional forbidden pair has zero clearance, and the largest overlap is `1.677032693654574e-05 m3` between `carrier` and `converter_rotor`. In addition, the Work 083 vertical travel produces `0.007 m` maximum misalignment at a rigid Work 084 coaxial butt interface, against a `1e-6 m` tolerance. The new load frame also lacks meshed convergence evidence and all material/process values remain synthetic.

Algebraic force, moment, and thermal ledgers close and all preregistered controls produce their required consequences. Those passes do not override the geometry, kinematic-interface, structural-evidence, or material-evidence blockers.

## Files changed

- `config/candidates/load_structure_integration_001.json`
- `src/formula_ultimate/subsystems/load_structure_integration.py`
- `scripts/candidates/build_load_structure_integration_001.py`
- `scripts/candidates/inspect_load_structure_integration_freecad.py`
- `tests/test_load_structure_integration_001.py`
- `docs/contracts/LOAD_STRUCTURE_INTEGRATION_001.md` and Thai companion
- this result and its Thai companion
- the Work 087 plan and Thai companion, changed to `Partial`

Generated CAD and replay evidence under `artifacts/work087/` are ignored and were not committed.

## Exact evidence

- Result identity: `faae1e084549e6ce5bbe23e1a635e7bb5e16aa37f9f2e339f11af9df6e4ba6ae`.
- Byte-identical result JSON SHA-256: `38c8327a4f454dd0eb46fae7daa466638f938e3fa38aeeb8c971a7ab8bfe7cc9`.
- Assembly STEP SHA-256: `33c1ade66729602bf9d022c36af017690ce1783364d38fddc71604684e62ee7d`.
- Evaluation SHA-256: `9212dbe1b3e5299fbb11c54e6eacb616e68302e586359ee156c5c576a6131a04`.
- Exact replay: `run_c` reproduced `run_b` byte for byte.
- Geometry: `17` solids; synthetic-density mass `2.7451889573288466 kg`; integration-part ground clearance `0.0697 m`; routing clearance `0.002 m`; service clearance `0.012 m`.
- Positive forbidden overlaps: `8`; largest `1.677032693654574e-05 m3`; minimum forbidden clearance `0 m`.
- Rigid-interface maximum misalignment: `0.007 m`; tolerance `1e-6 m`.
- All six declared load cases have zero recorded force and moment residual at the stored precision; thermal residual is zero at the stored precision.

The eight positive-overlap pairs are `carrier/converter_housing`, `carrier/converter_rotor`, `carrier/input_shaft`, `contact_roller/converter_housing`, `contact_roller/converter_rotor`, `converter_housing/guide_frame`, `converter_rotor/guide_frame`, and `guide_frame/input_shaft`. `contact_roller/input_shaft` is the additional zero-clearance forbidden pair.

## Exact validation commands and results

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\candidates\build_load_structure_integration_001.py `
  --config config\candidates\load_structure_integration_001.json `
  --output-root artifacts\work087\run_b `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"
# exit 0; status=partial; candidate_verdict=not_admitted

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\candidates\build_load_structure_integration_001.py `
  --config config\candidates\load_structure_integration_001.json `
  --output-root artifacts\work087\run_c `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work087\run_b\result.json
# exit 0; exact replay

python -m unittest tests.test_load_structure_integration_001 tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 608 tests in 340.892s; OK (skipped=3)
```

## Evidence review and limitations

Supporting evidence is the exact upstream identities, actual B-rep pair checks, named-object FCStd inspection, geometry-derived mass properties, explicit load/thermal ledgers, causal failure controls, and exact replay. Contradicting evidence is decisive: the current layouts geometrically interfere and their rigid motion interfaces are incompatible. An alternative explanation is not numerical noise because the positive overlaps are many orders above the frozen `1e-12 m3` tolerance and involve multiple distinct part pairs. Missing evidence includes a collision-free repackaging, an articulated or otherwise compatible motion-transfer interface, converged meshes for the new load frame, design-eligible material/process data, nonlinear contact, durability, crashworthiness, and physical tests.

Work 088 may audit whole-candidate readiness from this immutable evidence, but it must fail closed as `not_ready`; it must not simulate or claim a whole mechanically admissible vehicle from this geometry.
