# Geometry-to-Structural Physics Coupling V1

Thai companion: `GEOMETRY_STRUCTURAL_COUPLING_V1.th.md`

## Scope and evidence boundary

Work 082 binds the exact `bracket_001.step` identity and Work 081 cylindrical-interface signature into Gmsh tetrahedral meshes, CalculiX decks, parsed structural fields, residual gates, refinement evidence, and connection-state propagation. The reference uses the Work 079 synthetic aluminium-like record and therefore remains `synthetic_verification` with `design_use_allowed=false`.

Passing V1 proves only that the bounded geometry-to-solver software path is deterministic and causal under the declared fixture. It is not real-part capacity, physical validation, fracture/fatigue life, crashworthiness, safety, or production approval.

## Frozen reference

- STEP SHA-256: `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89`
- Work 081 FreeCAD report: `34ad809df13ba746352107e952e67a6d187795c96e1cb1096a6efc9a7ba28132`
- loaded surface signature: `04e1d97edb2595c219cc0132fdfb43b74132d3ca9b7cf3656d445706550e332f`
- material record: `72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097` (`synthetic`)
- load: consistent `500 N` tangential load over the measured through-hole surface;
- support: measured `x=0.06 m` end plane;
- meshes: `6 mm`, `4 mm`, and `3 mm` first-order tetrahedra.

The Gmsh route imports the exact STEP rather than reconstructing typed dimensions. Boundary triangles are selected geometrically. The CalculiX deck distributes the declared resultant by triangle area and records displacement, reactions, stress/strain, internal energy, and field output.

## Admitted numerical evidence

| Mesh | Nodes | Tetrahedra | Max displacement (m) | Compliance (m/N) | p90 von Mises (Pa) |
|---|---:|---:|---:|---:|---:|
| coarse 6 mm | 930 | 2,924 | `1.526042230277076e-5` | `2.831564572874119e-8` | `3.708533574964357e6` |
| medium 4 mm | 2,297 | 8,542 | `1.57548489513747e-5` | `2.8876628978500013e-8` | `3.8627178311174945e6` |
| fine 3 mm | 4,382 | 17,463 | `1.5955631992710995e-5` | `2.919834633813767e-8` | `3.926391799777586e6` |

Medium-to-fine changes are about `1.27%` displacement, `1.11%` compliance, and `1.65%` p90 stress, all below the frozen `5%` gate. Fine force, moment, and energy relative residuals are `4.4238208804794904e-8`, `2.249840148494702e-8`, and `3.1124177238745204e-8`, respectively. The p90 metric avoids treating idealized-constraint point singularities as an admitted capacity metric.

## Failure propagation and replay

The reference remains in the synthetic elastic domain. A severed or ultimate-domain-exceeded critical connection changes `bracket_structural_mount` to `failed`, writes zero transmitted force, and sets subsystem state to `dnf`. Yield-domain exceedance is observable as degraded; unsupported fracture/fatigue evidence never receives a neutral capacity.

CalculiX FRD files contain a runtime clock field. V1 retains raw files but canonicalizes only the single `1UTIME` value before hashing; missing or multiple time fields fail. Mesh, deck, DAT, parsed metrics, adjudication, connection result, and canonical FRD hashes replay exactly.

## Run command

```powershell
python scripts\structural\run_geometry_structural_coupling.py `
  --config config\structural\geometry_structural_coupling_v1.json `
  --geometry-root artifacts\work081 `
  --output-root artifacts\work082\run_a `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
python -m unittest tests.test_geometry_structural_coupling -v
```

## Limitations

The support and distributed cylindrical load are idealized bonded boundaries. The model is linear elastic C3D4 and does not represent contact, preload, friction, large deformation, plastic redistribution, crack growth, fatigue, local bearing damage, or manufacturing residual stress. Work 083 may consume this only as software-coupling evidence; a real ground-interaction design claim remains blocked by sourced material/process and higher-fidelity evidence.
