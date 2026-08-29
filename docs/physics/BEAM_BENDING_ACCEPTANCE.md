# Beam-Bending Acceptance

Status: Passed for Work 035

Thai companion: `BEAM_BENDING_ACCEPTANCE.th.md`

## Claim boundary

Work 035 verifies one local linear-elastic cantilever route:

```text
declared 3D beam -> Gmsh C3D4 mesh -> CalculiX static solve
-> full stress/reaction parsing -> analytical/equilibrium/convergence gates
```

It demonstrates transverse load transfer through a 3D solid into deflection,
axial bending stress, support force, and support moment. It does not validate
yield, plastic reserve, buckling, fracture, fatigue, a joint, or a vehicle.

## Fixture and analytical domain

The synthetic fixture is `L = 0.12 m`, `b = 0.012 m`, `h = 0.012 m`, with
`E = 70 GPa`, `nu = 0.3`, density `2700 kg/m^3`, and a `5 N` end resultant in
negative `z`. The `x = 0` face is fixed and the load is distributed over the
finite `x = L` face by triangle tributary area. The slenderness is `L/h = 10`,
the minimum admitted by this fixture contract.

For `I = b*h^3/12`, the references are:

```text
I                  = 1.728e-9 m^4
tip displacement   = P*L^3/(3*E*I) = 2.38095238095238e-5 m
root moment        = P*L             = 0.6 N*m
root outer stress  = P*L*(h/2)/I     = 2.08333333333333e6 Pa
external work      = P*delta/2       = 5.95238095238095e-5 J
Sxx(x,z)           = P*(L-x)*(z-h/2)/I
```

The stress comparison uses tetrahedron-centroid `Sxx` between
`x = 0.024 m` and `x = 0.096 m`. Clamp and load-introduction regions are
excluded before evaluation. Error is a volume-weighted signed normalized RMS;
signed correlation prevents an absolute-value result from hiding reversed
bending physics.

## Accepted results

| Mesh | Size (m) | Nodes | C3D4 | Tip (m) | Tip error | Stress RMS error | Signed correlation |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse | 0.0014 | 6,944 | 31,022 | 2.2812166e-5 | 4.1889% | 14.2772% | 0.989799 |
| medium | 0.0012 | 10,343 | 48,003 | 2.3062422e-5 | 3.1378% | 12.1645% | 0.992602 |
| fine | 0.0010 | 16,767 | 81,764 | 2.3281446e-5 | 2.2179% | 10.1221% | 0.994880 |

Fine-mesh force closure was `4.59e-12` relative and moment closure was
`2.46e-8` relative. Between the two finest meshes, displacement/external-work
change was `0.9497%`; stress-error change was `2.0425` percentage points. All
were below the predeclared gates.

## Failed attempts retained as evidence

The first run failed before solving because CalculiX permits at most 16 node-set
entries per line while the fixed face had 18. The adapter now wraps node sets
deterministically and a regression test enforces the limit for both tension and
bending decks.

The original `6 mm`-deep beam with a `3 mm` coarse mesh failed displacement and
stress gates because first-order tetrahedra were too stiff in bending. A second
`12 mm`-deep fixture with `2 mm` mesh passed global deflection but failed the
declared stress RMS gate at `19.77%`. A `1.5 mm` mesh reached `15.14%`, still
above the unchanged `15%` gate. The accepted sequence starts at `1.4 mm`; the
tolerance was not loosened to admit the failed meshes.

## Reproduce and inspect

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
```

Machine-readable evidence is in `artifacts/work035/experiment_summary.json`.
Each mesh directory contains `beam.geo`, `beam.msh`, `beam.inp`, `beam.dat`, and
`beam.frd`. Open the fine `.frd` file in FreeCAD's FEM workbench and use Fit All
to inspect displacement and stress fields. Visualization is diagnostic; the
JSON gates and hashed artifacts are the admitted evidence.

## Limitations and next gate

The Euler-Bernoulli comparison is intentionally limited to a regular slender
beam and excludes end regions. C3D4 centroid stress converges slower than global
displacement. External work is checked, but solver-reported internal energy is
not independently parsed. No physical material or second-solver data exists.

This result authorizes a separately planned torsion specimen. It does not
authorize structural fitness for arbitrary vehicle geometry or any nonlinear
failure claim.
