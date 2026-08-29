# Solid-Shaft Torsion Acceptance

Status: Passed for Work 036

Thai companion: `SHAFT_TORSION_ACCEPTANCE.th.md`

## Claim

Work 036 verifies local linear Saint-Venant torsion through `3D cylinder -> Gmsh C3D4 -> CalculiX -> strict evidence gates`. It does not validate yield, fracture, fatigue, joints, gears, bearings, or a drivetrain.

The synthetic fixture uses `L=0.1 m`, `R=0.01 m`, `T=10 N*m`, `E=70 GPa`, and `nu=0.3`. Derived references are `G=26.9230769231 GPa`, `J=1.5707963267949e-8 m^4`, `theta=0.00236458772593673 rad`, and `U=0.0118229386296837 J`.

Tangential traction is consistently integrated on each loaded-face triangle and scaled to a pure wrench: zero resultant force and exact torque. Twist is an area-weighted least-squares face rotation. Interior `(Sxy,Sxz)` is compared as a signed, volume-weighted vector field.

| Mesh | Nodes | C3D4 | Twist error | Shear RMS error | Correlation |
|---|---:|---:|---:|---:|---:|
| 1.9 mm | 4,810 | 22,264 | 4.662% | 11.427% | 0.993825 |
| 1.7 mm | 6,382 | 30,539 | 3.802% | 10.270% | 0.994976 |
| 1.5 mm | 8,967 | 44,200 | 3.023% | 8.932% | 0.996165 |

Fine force and moment closure were `1.52e-13` and `7.02e-9` relative. Last-two twist/work change was `0.810%`; shear-error change was `1.338` percentage points.

Live metamorphic checks passed: `-T` reversed twist/stress with equal positive energy; `2T` doubled twist/stress and quadrupled work; doubled modulus halved twist without changing stress. CalculiX returned exit `0` for the deliberately unrestrained shaft, but displacements exceeded `1e8 m`; the evidence gate rejected it as rigid-body singular behavior.

Early `4 mm`, `2.5 mm`, and `2.0 mm` sequences failed unchanged analytical/stress gates. The accepted sequence was refined rather than loosening tolerances. Replay with `scripts\run_work036.ps1`; inspect `artifacts/work036/fine_1p5mm/shaft.frd` in FreeCAD FEM.

Limitations: faceted circular geometry remains visible in volume error, internal solver strain energy is not independently parsed, and no second solver or physical shaft data exists. The next independent physics milestone is material yield/elastoplastic acceptance or buckling according to the maintained roadmap.
