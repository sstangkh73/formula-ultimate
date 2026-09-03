# Work 086 Result: Refined Housing Mesh Convergence

Thai companion: `2026-09-04_086_refined-housing-mesh-convergence-result.th.md`

## Status and outcome

Status: Completed

The new frozen mesh experiment resolved Work 085's single convergence failure without relaxing the `12%` gate. The runner verified the exact failed-evidence file, reproduced its `13.187908211258156%` housing displacement change, derived a config that changed only `cases[2].mesh_levels_m`, and reran all nine Gmsh/CalculiX cases.

With housing meshes `4.5/3.5/2.75 mm`, last-two changes are displacement `6.528877212806262%`, compliance `5.626733597565592%`, and p90 stress `0.5739008104203665%`. Every metric is below `12%`. All three cases are elastic relative to the synthetic `250 MPa` yield value, and all equilibrium/energy gates pass. Two clean roots reproduced the complete result exactly.

This closes the meshed torsion/bearing/housing software blocker recorded by Work 084/085. It does not change their historical statuses, does not close the design-evidence blocker, and does not produce physical validation.

## Files changed

- `config/structural/refined_housing_mesh_convergence_v1.json`
- `src/formula_ultimate/structural/refined_mesh.py`
- `scripts/structural/run_refined_housing_mesh.py`
- `tests/test_refined_housing_mesh.py`
- this result and its Thai companion
- the Work 086 plan and Thai companion, changed to `Completed`

Generated derived configs and solver/replay evidence under `artifacts/work086/` are ignored and were not committed.

## Exact evidence

- Prior failed evidence file SHA-256: `71244cf626bc593f953dc5c37329541eb55462340a6c28885601b4d733f2c247`.
- Derived generalized solver config identity: `0d3d6b707b2d738d70d05d85a14628737f0d546097a4cb0776ebb1cb054866de`.
- Refinement result identity: `ec818c21ea45f4a129f762bac3130e06628c7b560bb1d74dff8a8c9555cdf827`.
- Byte-identical result JSON SHA-256: `0c4930b49e6d77189f24e6a752ae8b14664c1bc9c6c054349d01a74be1636e64`.
- Replay identity: `b00c72af7f899918641a27ade27ac23780b1f630fc0851c2c596343a72558fdf`, `exact=true`.
- Fine housing mesh: `11789` nodes, `49282` tetrahedra, displacement `8.697399879757787e-7 m`, compliance `8.061086986709912e-9 m/N`, p90 stress `313161.0272046963 Pa`.
- Fine shaft mesh: p90 stress `144476407.7862506 Pa`, below synthetic yield but not a design claim.
- Maximum recorded force/moment/energy residuals remain below `1e-5/1e-5/1e-4`.

## Exact validation commands and results

```powershell
python scripts\structural\run_refined_housing_mesh.py `
  --config config\structural\refined_housing_mesh_convergence_v1.json `
  --output-root artifacts\work086\run_a `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
# exit 0; result_sha256=ec818c21ea45f4a129f762bac3130e06628c7b560bb1d74dff8a8c9555cdf827

python scripts\structural\run_refined_housing_mesh.py `
  --config config\structural\refined_housing_mesh_convergence_v1.json `
  --output-root artifacts\work086\run_b `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe" `
  --replay-reference artifacts\work086\run_a\result.json
# exit 0; replay_exact=true

python -m unittest tests.test_refined_housing_mesh tests.test_generalized_structural_coupling tests.test_repository_contract -v
# exit 0; Ran 27 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 598 tests in 343.349s; OK (skipped=3)
```

## Evidence review and limitations

Supporting evidence: exact failed-input identity, an unchanged gate, a one-path config transformation, nine converged solves, three passing last-two metrics per case, and exact replay. Contradicting evidence: the fine shaft p90 stress is about `57.8%` of the synthetic yield value and deserves higher-order/contact/fatigue study; it is not a comfortable physical margin. Alternative explanation: apparent convergence may remain element-family dependent because every solve uses first-order C3D4 tetrahedra. Missing evidence remains design-eligible material/process data, independent solver/element comparison, nonlinear contact, fatigue/fracture, fasteners, bearing life, manufacturing tolerance, and physical tests.

The next work may integrate Works 083/084 only as identity-locked synthetic fixtures. Its verdict must remain non-admitted until the separate material/process evidence blocker is resolved.
