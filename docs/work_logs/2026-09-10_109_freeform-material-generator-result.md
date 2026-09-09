# Work 109 Result: Open Free-Form Material Generator

Thai companion: `2026-09-10_109_freeform-material-generator-result.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Outcome and changed files

Work 109 implemented a bounded implicit Cartesian material/void field, all six planned edit families, deterministic OBJ boundary extraction, topology/feature controls, three representation levels, resource caps and exact replay. It proves execution and geometry coverage within the registered grid, not functional or physical superiority.

Changed files:

- `src/formula_ultimate/search/freeform_material_generator.py`
- `config/development/freeform_material_generator_v1.json`
- `scripts/development/run_freeform_material_generator.py`
- `tests/test_freeform_material_generator.py`
- `docs/contracts/FREEFORM_MATERIAL_GENERATOR_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored evidence under `artifacts/work109/run_a` and `run_b`

## Decisions and falsification

- One scalar label owns each occupied cell. Missing cells are void; mixed labels are unsupported and rejected.
- Geometry identity includes sorted occupancy and labels but excludes case names, so renaming-only pseudo-novelty retains the same identity and is rejected.
- Seven fixed slots exercise six operators; `boundary_displacement` appears once for boundary growth and once to refill the actual through-hole.
- Surface triangles are emitted only when every edge has exactly two incident faces. No healing is allowed.
- The through-hole changed genus `0 -> 1` and its fill returned `1 -> 0`. Split/merge changed occupied components `1 -> 2 -> 1`. The asymmetric thin feature retained fraction was `1.0`.
- The first proposed coarse level, `0.012 m`, exposed an edge-only contact and non-manifold OBJ boundary. That run failed. The registered coarse level became `0.02 m`, while the unsupported `0.012 m` outcome remains disclosed here; no mesh was repaired or silently accepted.
- Refinement volumes differed (`0.001312`, `0.0013500000000000003`, `0.00126976 m3`), contradicting any claim of resolution independence. This is recorded as grid bias rather than a physical constraint.

## Numerical evidence

Canonical `run_a` and replay `run_b` share result SHA-256 `0866184b76def5f40cbde496f067f16db31ddf7bb4bbda41d8054467856a6a67`; replay reports `exact: true`. Artifact manifest SHA-256 is `1874ed3c88aa32d69a338d9bc3c8717dbaf38ad3cc0346ea6e59fb1374d034a2`.

| Stage | Cells | Components | Genus | Triangles | Volume error |
|---|---:|---:|---:|---:|---:|
| source | `1350` | `1` | `0` | `1868` | `9.637352644315593e-16` |
| cavity route | `1194` | `1` | `1` | `2164` | `1.4347063924012536e-14` |
| cavity fill | `1442` | `1` | `0` | `2116` | `8.571362528664874e-15` |
| split | `1118` | `2` | `0` | `2464` | `1.881352606996313e-14` |
| merge | `1126` | `1` | `0` | `2480` | `1.6946676941158857e-14` |
| final redistribution | `1126` | `1` | `0` | `2480` | `1.6946676941158857e-14` |

All errors are below the registered `1e-10` surface-volume limit. Refinement grid visits were `1728`, `13824` and `27000`; no timing estimate substitutes for these deterministic cost counts.

## Exact validation commands and exits

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_freeform_material_generator tests.test_repository_contract -v
# exit 0; 12 tests passed

python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_a
# exit 0; 7 operator slots; status passed

python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_b --replay-reference artifacts/work109/run_a/result.json
# exit 0; exact replay; same result_sha256

python -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

The earlier `0.012 m` runner attempt exited `1` with `surface is not closed two-manifold`. Final affected regression, explicit staged-scope checks and `git diff --cached --check` are required before commit. The verified commit hash is reported in the final handoff.

## Limitations and handoff

This is a voxel boundary, not a smooth B-rep or solver-ready volume mesh. Cartesian resolution and orientation bias reachability, topology and feature survival. The material labels carry no mixed-cell, constitutive or manufacturing meaning. Work 110 must implement the actual geometry-to-mesh bridge, retain field/material identity, quantify approximation and expose unsupported conversions. No scientific benefit or vehicle claim follows from Work 109.
