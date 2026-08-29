# Work 036 Plan: Solid-Shaft Torsion Acceptance

Status: Completed

Thai companion: `2026-08-29_036_solid-shaft-torsion-plan.th.md`

## Objective

Implement and execute a replayable solid-circular-shaft specimen that verifies
that a declared pure torque crosses a finite 3D solid and produces the expected
reaction torque, twist, signed shear-stress vector field, and external work in
the declared small-strain linear-elastic domain.

## Claim boundary

Passing Work 036 will verify only Saint-Venant torsion of a homogeneous,
isotropic, prismatic solid shaft through the installed Gmsh/CalculiX route. It
will not validate yielding, plastic redistribution, fracture, fatigue, spline or
gear contact, bearings, joints, rotating inertia, power transmission, or a
vehicle drivetrain.

## Proposed canonical fixture

- shaft axis: positive `x`;
- length `L = 0.1 m`;
- radius `R = 0.01 m`;
- synthetic material: `E = 70 GPa`, `nu = 0.3`, density `2700 kg/m^3`;
- derived shear modulus: `G = E/[2*(1+nu)] = 26.9230769231 GPa`;
- base torque magnitude: `T = 10 N*m` about positive `x`;
- fixed face: `x = 0`;
- loaded face: `x = L`;
- stress gauge: predeclared interior interval, initially
  `0.02 m <= x <= 0.08 m`;
- three decreasing Gmsh characteristic sizes, with the exact accepted sequence
  pinned in the configuration before an accepted run.

The values remain a synthetic analytical fixture, not a material certificate.
If the first-order tetrahedral sequence cannot meet the declared gates, failed
runs will be retained and the mesh/element strategy will change explicitly;
tolerances will not be loosened merely to admit a result.

## Analytical reference

For polar second moment `J = pi*R^4/2`, radial coordinates relative to the
shaft centre `(y_c, z_c)`, and `y_r = y-y_c`, `z_r = z-z_c`:

```text
J                   = pi*R^4/2
tau_xy(x,y,z)       = -T*z_r/J
tau_xz(x,y,z)       =  T*y_r/J
tau(r)              = T*r/J
tau_max             = T*R/J
theta               = T*L/(J*G)
U                   = T*theta/2
```

For the proposed fixture, the reference values are approximately:

```text
J       = 1.57079632679e-8 m^4
tau_max = 6.36619772368e6 Pa
theta   = 2.36493114917e-3 rad
U       = 1.18246557458e-2 J
```

Exact values will be generated from the committed configuration, not copied
from rounded documentation.

## Pure-torque load construction

The loaded circular face will receive a distributed tangential traction, not a
single point force. For a linear boundary triangle with vertices `i,j,k`, area
`A`, and linearly varying tangential traction `t`, consistent nodal force is:

```text
f_i = A/12 * (2*t_i + t_j + t_k)
```

The assembled load must satisfy, about the loaded-face centre:

```text
sum(F_i)             = (0, 0, 0)
sum(r_i cross F_i)   = (T, 0, 0)
```

Any normalization or pure-wrench projection must be deterministic, recorded,
and tested. It may remove only numerical integration residuals; it must not hide
an incorrect surface identity or arbitrary point-load shortcut.

## Measurements

### Loaded-face twist

Twist will be recovered by an area-weighted least-squares rigid rotation of the
loaded face around its centre, rather than from one node:

```text
theta_fit = sum(w_i * (y_r*u_z - z_r*u_y)) / sum(w_i * r_i^2)
```

Radial expansion, axial translation, and rigid transverse translation will be
reported separately so they cannot contaminate the twist result silently.

### Reaction and equilibrium

- total support force vector;
- support moment vector about the fixed-face centre;
- applied-minus-reaction torque residual;
- unintended bending moments about `y` and `z`;
- external work `0.5*sum(F_i dot u_i)`.

### Shear-stress field

Complete element stress tensors will be compared at tetrahedron centroids in
the declared interior gauge. The primary metric is a volume-weighted signed
normalized RMS error for the vector `(Sxy, Sxz)` against the analytical field.
A signed vector correlation gate prevents a swapped axis or reversed torque
from passing through magnitude-only comparison. The neutral-axis region will
not dominate normalization, and end regions will remain excluded as declared.

## Experiment matrix

### Canonical mesh sequence

Run base `+T` on three meshes and gate:

- finite connected volume and circular-boundary identity;
- applied zero resultant force and exact torque;
- force and moment closure;
- analytical twist and external-work agreement;
- signed shear-vector RMS/correlation;
- last-two-mesh convergence for twist, energy, and shear error;
- fresh `.msh`, `.inp`, `.dat`, and `.frd` evidence plus hashes.

### Live metamorphic cases

Use one declared mesh and the same geometry/material/load adapter:

1. `-T`: twist and both shear components reverse sign; energy remains positive
   and equal within tolerance.
2. `2T`: twist and shear double within the linear range; external work becomes
   four times the base value.
3. `2G` fixture: twist halves while torque/shear remain unchanged within the
   declared comparison tolerance.
4. Missing rotational restraint: solver/evidence must fail rather than return
   an admitted torsion result.

Radius `R^4` sensitivity will be covered first by unit/reference tests. A second
live-radius solve will be added only if it fits the common declared compute
budget without weakening the canonical mesh sequence.

## Variables and controls

### Independent variables

- characteristic mesh size for the canonical sequence;
- signed torque and torque scale for metamorphic cases;
- declared shear modulus for the stiffness metamorphic case.

### Dependent variables

- twist and contaminating rigid/radial motion;
- support force/moment and all residual components;
- interior signed `(Sxy, Sxz)` field metrics;
- external work and analytical residual;
- mesh counts/quality/volume, solver status/iterations, wall time, hashes, and
  typed failure status.

### Controls

- geometry and coordinate frame;
- material-law ID/provenance and SI units;
- boundary/load-face identity and pure-wrench construction;
- clamp, gauge exclusions, element family/order, mesher/solver/adapter versions;
- tolerances, resource budget, source/config identity, and repository revision.

## Proposed gates

Initial gates will be declared in the versioned configuration before the first
accepted run. Target bounds are:

- load resultant relative to `T/R`: `<= 1e-8`;
- applied torque construction relative residual: `<= 1e-10`;
- support torque closure: `<= 1e-5` relative;
- unintended support moment components: `<= 1e-5` relative;
- twist analytical error: `<= 5%`;
- external-work analytical error: `<= 5%`;
- signed shear-vector normalized RMS error: `<= 15%`;
- signed shear-vector correlation: `>= 0.98`;
- last-two twist/work change: `<= 3%`;
- last-two shear-error absolute change: `<= 5` percentage points.

These are solver-acceptance gates, not safety factors or material allowables.

## Planned files

- `config/structural/shaft_torsion_acceptance_v1.json`
- `src/formula_ultimate/structural/acceptance.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_shaft_torsion_acceptance.py`
- `scripts/run_work036.ps1`
- `tests/test_shaft_torsion_acceptance.py`
- regression updates to existing structural tests where shared code changes
- `docs/physics/SHAFT_TORSION_ACCEPTANCE.md`
- `docs/physics/SHAFT_TORSION_ACCEPTANCE.th.md`
- matching Work 036 result records in English and Thai

## Validation

Planned fail-fast commands:

```powershell
py -3.14 -m unittest tests.test_shaft_torsion_acceptance tests.test_beam_bending_acceptance tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work036.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

## Success criteria

- Three canonical real solver meshes and all mandatory metamorphic cases pass.
- The applied load is demonstrably a pure torque, not a hidden force couple with
  an undeclared resultant.
- Twist, torque reaction, shear-vector field, energy, and mesh convergence pass
  independent declared gates.
- Reversed/doubled torque and doubled shear modulus produce the required signed
  scaling; missing restraint fails closed.
- Work 034/035 regressions, focused/full/static/staged checks, bilingual records,
  explicit commit, and clean committed-tree replay all pass.

## Risks

- A faceted tetrahedral approximation changes circular area, volume, and `J`;
  geometry error must be reported and converge, not mixed silently with solver
  error.
- First-order tetrahedra may be too stiff or noisy in shear.
- Tangential load integration can introduce unintended force/bending if surface
  coordinates or centre identity are wrong.
- Full-face clamping creates an end effect; the interior gauge must stay fixed.
- CalculiX text precision may be insufficient for tiny residuals; explicit total
  rows or higher-precision evidence must be used rather than loosening physics
  gates without justification.

## Explicit non-goals

- No yield/plasticity, fracture, fatigue, buckling, contact, spline/gear/bearing
  model, rotating inertia, drivetrain efficiency, failure coupling, or `DNF`.
- No arbitrary minimum radius/thickness, whole-vehicle optimization, physical
  validation claim, external upload, push, publication, or history rewrite.
