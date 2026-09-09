# Work 108 Result: Spatial Material and Void Source of Truth

Thai companion: `2026-09-10_108_spatial-material-result.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Outcome

Work 108 implemented the first package in `docs/plans/detailed_part_to_vehicle_v1`. Three admitted Work 092 cases now bind exact source B-reps to explicit material ownership, subtractive void evidence and rigid placement. CadQuery and FreeCAD independently measured the exact placed STEP regions; their volume, mass, centre-of-mass and inertia results passed registered limits. A second clean run replayed exactly.

This is bounded spatial/CAD verification. It is not a structural, thermal, flow, manufacturing, whole-vehicle, scientific-benefit or physical-validation claim.

## Files changed

- `src/formula_ultimate/components/spatial_material.py`
- `config/development/spatial_material_v1.json`
- `scripts/development/run_spatial_material.py`
- `scripts/cad/inspect_spatial_material_freecad.py`
- `tests/test_spatial_material.py`
- `docs/contracts/SPATIAL_MATERIAL_VOID_V1.md` and Thai companion
- `docs/work_logs/2026-09-10_108_spatial-material-plan.md` and Thai companion
- this result and Thai companion
- ignored retained evidence under `artifacts/work108/run_a` and `artifacts/work108/run_b`

No existing source API or historical evidence file was modified.

## Decisions and implementation

- Exact-schema validation requires finite SI values, positive density, a unit rotation axis, complete single ownership of every occupied body, unique region identities and immutable upstream declaration/STEP hashes.
- The source corpus is regenerated in original Work 092 order before any placed-region export. This preserves canonical upstream STEP identities rather than accepting a new exporter counter.
- Curved, subtractive hollow and four-body cases are admitted. The multi-body case assigns one exact solid to each material region after deterministic centre/volume ordering.
- Pairwise occupied-body intersection above `1e-12 m3` fails closed; measured maximum was `0 m3`.
- Cavity evidence must match the actual `outer`, `inner`, `duct` `boolean_subtract` ancestry. Its closure residual was `0`.
- CAD `mm3`, `mm` and `mm5` values are converted to `m3`, `m` and `m5`. Density weighting and the parallel-axis theorem produce system mass properties.
- Work 108 materials are explicitly synthetic constant-density fixtures. Their names do not claim measured strength, thermal or manufacturing properties.
- Material and placement mutations changed dependent evidence identities. Filling the actual hollow geometry changed STEP SHA-256 and mass from `0.115652168747105 kg` to `0.224098880843536 kg`.

## Falsification and development corrections

Three fail-fast development runs exposed and corrected assumptions:

1. The first runner import used the wrong existing API name, `validate_wire_grammar`; the actual Work 091 validator is `validate_grammar`.
2. Interleaving placed-region exports changed an OCCT STEP `PRODUCT` counter and therefore the hollow source SHA-256 despite identical geometry. The runner now regenerates and exports the complete Work 092 source corpus in its original order before downstream exports; it did not lower the identity gate.
3. `Part.read` returned a compound wrapper without `MatrixOfInertia`. The FreeCAD inspector now requires exactly one solid per region and measures that solid directly.

Duplicate ownership, incomplete ownership, unknown material, non-finite placement, unsupported void semantics and stale source identity are rejected. The preferred hypothesis survived the admitted controls: actual geometry, material and placement changes invalidate dependent evidence as intended.

## Numerical evidence

Canonical evidence: `artifacts/work108/run_a`. Replay: `artifacts/work108/run_b/replay.json` with `exact: true`.

| Evidence | Result |
|---|---:|
| Cases / occupied material regions | `3 / 6` |
| CadQuery / FreeCAD | `2.8.0 / 1.1.3` |
| Maximum undeclared overlap | `0 m3` |
| Hollow cavity closure residual | `0` |
| Maximum system volume relative error | `4.01876492153646e-10` |
| Maximum system mass relative error | `1.79738452857777e-9` |
| Maximum system centre absolute error | `1.42850696549512e-11 m` |
| Maximum system inertia relative error | `4.85111865432947e-9` |
| Artifact manifest SHA-256 | `e29833cd993df2e2ffbebca2f60c1c9009cf5ac2f44d7aebc4a487be587276d8` |
| FreeCAD report SHA-256 | `edd1d7abdaef5f8927cad8f7674fea89944ada7faf03fdb1a4b1a2002aec17cb` |
| Result SHA-256 | `662f33cf876f6b6a444b46c346adcd7434e7baf60a95fb3366df3beffaf8470a` |

Case system values:

| Case | Volume (`m3`) | Mass (`kg`) | Centre of mass (`m`) |
|---|---:|---:|---|
| `curved_branch_placed` | `3.37238125113722e-5` | `0.091054293780705` | `[0.11889545450136, -0.0406540121332367, 0.129199002436967]` |
| `tapered_hollow_placed` | `9.63768072892543e-5` | `0.115652168747105` | `[-0.0733739692121858, 0.0776078853869922, 0.0605122443349965]` |
| `multi_body_mixed_material_placed` | `2.93976512599125e-6` | `0.0143313549898507` | `[0.023682615749267, 0.00821489285403821, -0.0125828706419786]` |

## Exact validation commands and exits

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_spatial_material tests.test_repository_contract -v
# exit 0; 13 tests passed

python -m compileall -q src scripts tests
# exit 0

& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_spatial_material tests.test_repository_contract -v
# exit 0; 13 tests passed

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_a --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'
# exit 0; status passed; result_sha256 662f33cf876f6b6a444b46c346adcd7434e7baf60a95fb3366df3beffaf8470a

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_b --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work108\run_a\result.json
# exit 0; status passed; exact replay; same result_sha256

& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_freeform_solid_grammar tests.test_spatial_material tests.test_repository_contract -v
# exit 0; 20 affected tests passed

git diff --check
# exit 0
```

Before commit, explicit staging, staged-name inspection and `git diff --cached --check` are also required. The verified short commit hash is reported in the final handoff because a commit cannot truthfully contain its own identity.

## Limitations, alternatives and follow-up

CadQuery and FreeCAD share OCCT-family geometry technology. Their agreement validates exact artifact transfer and independent application measurements, not independent physics. Constant synthetic density does not model anisotropy, gradients, porosity, temperature dependence, failure or manufacturing variation. Work 108 admits one material per connected source solid; spatially varying material inside one connected body remains missing. The selected Work 092 cases do not establish arbitrary B-rep robustness.

Work 109 may now generate new free-form material/void candidates against this immutable spatial contract. Work 110 may mesh only geometries whose ownership and source identity pass this gate. No vehicle or part should be promoted from these mass-property checks alone.
