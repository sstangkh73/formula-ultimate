# Eigenvalue Buckling Acceptance

Status: Passed for Work 037

Thai companion: `EIGENVALUE_BUCKLING_ACCEPTANCE.th.md`

Work 037 verifies ideal linear eigenvalue buckling of a solid rectangular cantilever column (`L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `K=2`) under a distributed `100 N` compression reference. Euler gives `Pcr=3598.2932712304946 N`.

| Mesh | Nodes | C3D4 | Pcr (N) | Error | Pair split | Transverse/axial |
|---|---:|---:|---:|---:|---:|---:|
| 1.5 mm | 7,052 | 29,098 | 3852.795 | 7.073% | 0.380% | 24.64 |
| 1.25 mm | 11,702 | 51,221 | 3776.375 | 4.949% | 0.0458% | 24.95 |
| 1.0 mm | 20,514 | 95,711 | 3715.160 | 3.248% | 0.0128% | 25.66 |

Last-two critical-load change was `1.6477%`; static reaction closure was exact at printed precision. Four eigenfactors and FRD displacement modes were parsed. The near-degenerate first pair and transverse-dominant displacement identify the expected two bending directions. Euclidean tip-vector orthogonality is reported but not gated because a nearly degenerate eigenspace may be returned in an arbitrary mixed basis; a mass/stiffness-weighted MAC is future evidence.

Early 3 mm and 2 mm meshes failed the unchanged 10% analytical gate. Tension loading produced only negative factors and was rejected. An unclamped model misleadingly returned factors near one with exit `0`, but the admission layer rejected it because its required support contract was absent.

Run `scripts\run_work037.ps1`; inspect `artifacts/work037/fine_1mm/column.frd`. This result is an ideal elastic instability estimate only. It is not physical capacity: geometric imperfection, nonlinear geometry/material response, limit point and post-buckling remain mandatory before use in fitness.
