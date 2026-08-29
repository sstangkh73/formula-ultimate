# Tension Solver Acceptance

Status: Passed for Work 034

Thai companion: `TENSION_SOLVER_ACCEPTANCE.th.md`

## Claim boundary

Work 034 verifies one local structural-analysis route:

```text
declared 3D prism -> Gmsh C3D4 mesh -> CalculiX linear solve
-> strict result parser -> analytical and mesh-convergence gates
```

It demonstrates that an applied axial load crosses a meshed solid and appears
as displacement, support reaction, axial stress, and external work. It does not
validate a real material, candidate vehicle, nonlinear failure, or the complete
`3D -> STEP -> FreeCAD -> Level 0` candidate route.

## Declared specimen and equations

The synthetic SI fixture is a `0.1 m x 0.01 m x 0.01 m` rectangular prism with
`E = 70 GPa`, `nu = 0.3`, density `2700 kg/m^3`, a fully fixed `x = 0` face,
and a `1000 N` resultant on the `x = 0.1 m` face. The load is distributed to
surface nodes by triangle tributary area rather than divided equally.

The analytical reference is:

```text
A       = 1.0e-4 m^2
sigma   = F/A       = 1.0e7 Pa
epsilon = sigma/E   = 1.4285714285714287e-4
delta   = FL/(AE)   = 1.4285714285714287e-5 m
U       = F*delta/2 = 7.1428571428571435e-3 J
```

The configured material is an analytical fixture, not an aluminium certificate
or measured coupon dataset.

## Results

All three predeclared meshes passed. Stress is the tetrahedron-volume-weighted
mean `Sxx`; displacement is the load-weighted loaded-face displacement. Peak
stress is deliberately excluded because the fully fixed boundary creates a
local end effect.

| Mesh | Size (m) | Nodes | C3D4 | Displacement (m) | Displacement error | Mean Sxx (Pa) | Force residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse | 0.0100 | 86 | 198 | 1.4162150e-5 | 0.86495% | 9,999,999.72 | 2.0e-4 N |
| medium | 0.0075 | 140 | 313 | 1.4182479165e-5 | 0.72265% | 9,999,999.89 | 0 N |
| fine | 0.0050 | 190 | 434 | 1.4198094754e-5 | 0.61334% | 9,999,999.88 | -3.0e-5 N |

Between the two finest meshes, relative changes were `0.11010%` for
displacement/external work and `1.70e-7%` for mean axial stress. The fine-mesh
force-closure residual was `3.0e-8` relative. Every generated tetrahedral
volume closed to the declared `1.0e-5 m^3` within the gate.

Replay evidence is written to ignored `artifacts/work034/`. The accepted summary
records commands, exit codes, wall times, repository identity, source/config/tool
hashes, per-mesh input/output hashes, solver output, metrics, and the structured
falsification review. A failed stage writes `experiment_failure.json` and returns
a nonzero exit code; it is not replaced by an analytical answer.

## Reproduce and inspect

Run the installed Gmsh/CalculiX route:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
```

The numerical record is `artifacts/work034/experiment_summary.json`. Each mesh
directory contains `tension.geo`, `tension.msh`, `tension.inp`, `tension.dat`,
and `tension.frd`. Open the `.frd` result in FreeCAD's FEM workbench to inspect
the solved displacement/stress field, or import `.msh` to inspect the mesh. The
undeformed prism is only `100 mm x 10 mm x 10 mm`; use Fit All if it is not
visible. Field visualization is diagnostic; the JSON gates are the accepted
machine-readable evidence.

## Falsification review and limitations

Supporting evidence is fresh output from three connected meshes, closed loads
and reactions, analytical agreement, and last-two-mesh convergence. The simple
uniform-tension prism is also the strongest alternative explanation for the
close agreement: this fixture is intentionally easy and does not establish
accuracy for arbitrary geometry.

Missing evidence remains decisive: independent-solver agreement, measured
coupon data, bending, torsion, buckling, loaded interfaces, plasticity, yield,
fracture, fatigue, and post-failure connection removal. External work was
checked against `F*delta/2`; solver-reported internal strain energy was not
independently parsed. This result therefore authorizes the next specimen, not a
whole-vehicle safety or physical-validation claim.
