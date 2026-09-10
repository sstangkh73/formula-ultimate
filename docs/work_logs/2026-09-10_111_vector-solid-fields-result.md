# Work 111 Result: Vector Solid Fields from Generated Geometry

Thai companion: `2026-09-10_111_vector-solid-fields-result.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Outcome and files

Work 111 assembled and solved three-displacement-DOF, small-strain isotropic linear-elastic tetrahedral systems on a structured reference and the actual Work 109 field routed through Work 110. It records vector displacement, tensor stress, p90 von Mises stress, recovered reactions, energy, balance residuals, conditioning proxy and deterministic field identities. The material is explicitly synthetic and the claim remains Level-0 numerical evidence.

Changed: `src/formula_ultimate/structural/vector_solid_fields.py`, `config/development/vector_solid_fields_v1.json`, `scripts/development/run_vector_solid_fields.py`, `tests/test_vector_solid_fields.py`, bilingual `docs/contracts/VECTOR_SOLID_FIELDS_V1*`, and this bilingual plan/result. Generated `artifacts/work111/run_a|run_b` remain ignored evidence.

## Decisions and falsification

- Constant-strain TET4 uses `Ke = V B^T D B`; triangle traction is area-weighted and body force is distributed consistently by element volume.
- Support nodes fix all three translations. Reactions come from assembled residual `K u - f`; a separately hashed uniform assigned-reaction control differs from the recovered field.
- The admitted stress quantity is volume-weighted p90 von Mises, not a sharp-corner maximum.
- Controls passed affine patch, rigid translation/rotation, exact inverse stiffness scaling and causal geometry/load mutations. Unsupported rigid modes, severed load path and zero stiffness were rejected.
- The unfamiliar geometry's quantities vary with resolution. Passing the registered last-two gate does not demonstrate asymptotic or physical convergence.

## Numerical evidence

Result SHA-256: `8f057c39a1f79fa45113f86fa48d6cb199562c8ba40ad041bccb9e9c6e8a4c85`. `run_b/replay.json` reports `exact: true`.

| Case / resolution (`m`) | Nodes | Tets | Main quantity | Force residual | Moment residual |
|---|---:|---:|---:|---:|---:|
| reference / `0.04` | `16` | `18` | analytic displacement error `0.04087756582701689` | `6.284990487158661e-16` | `4.105232943528381e-16` |
| reference / `0.02` | `63` | `144` | analytic displacement error `0.024271592769903552` | `2.3581991752920518e-15` | `4.3732590578852406e-16` |
| reference / `0.01` | `325` | `1152` | analytic displacement error `0.016137273749221095` | `1.006596157171345e-14` | `7.469678635014262e-15` |
| unfamiliar / `0.02` | `289` | `984` | max displacement `2.722901067165298e-8 m`; p90 `12696.135980341078 Pa` | `1.354820533070906e-15` | `3.8996688400222213e-16` |
| unfamiliar / `0.01` | `1865` | `8100` | max displacement `1.4485540999002353e-8 m`; p90 `8219.449957122448 Pa` | `1.0627066868689837e-14` | `1.7278112555075858e-15` |
| unfamiliar / `0.008` | `3220` | `14880` | max displacement `1.5494724816709918e-8 m`; p90 `8631.834378747026 Pa` | `4.4855856174795724e-15` | `1.1572425024098133e-15` |

Last-two relative changes were `0.06513079965248782` for maximum displacement, `0.09063743251857388` for compliance and `0.04777483018440845` for p90 stress. Patch, translation and rotation errors were `5.1457251545698746e-20`, `1.4210854715202004e-14` and `6.776263578034403e-20`, respectively. Energy residuals were at most `4.319781655832243e-15`; the minimum diagonal proxy was at least `0.09848484848484801`.

## Validation

```powershell
python -m unittest tests.test_vector_solid_fields -v
# exit 0; 5 tests passed
python -m py_compile scripts/development/run_vector_solid_fields.py src/formula_ultimate/structural/vector_solid_fields.py
# exit 0
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_a
# exit 0; result SHA-256 8f057c39a1f79fa45113f86fa48d6cb199562c8ba40ad041bccb9e9c6e8a4c85
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_b --replay-reference artifacts\work111\run_a\result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_spatial_material tests.test_freeform_material_generator tests.test_geometry_mesh_bridge tests.test_vector_solid_fields tests.test_repository_contract -v
# exit 0; 28 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 111 files
git diff --cached --check
# exit 0
```

The first sandboxed staging attempt could not create `.git/index.lock` (`Permission denied`). Its combined shell sequence also returned the later command's `0`, so it was not accepted as evidence. `git add` was rerun with the required permission and every inspection/check was then executed separately with exit `0`. The verified commit hash is reported in the final handoff.

## Limitations and follow-up

The unfamiliar boundary is voxel-stepped and the six-tetra cells are regular by construction. The diagonal ratio is not a full condition number, stress convergence is not proven, and no independent production solver or experiment cross-check exists. Nonlinear/contact/plastic/fatigue response, certified material data, real load cases, manufacturing and physical validation remain outside scope. Work 113 and Work 115 may consume the fields only under this contract and its limitations.
