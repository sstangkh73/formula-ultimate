# Work 035 Plan: Beam-Bending Acceptance

Status: Completed

Thai companion: `2026-08-29_035_beam-bending-acceptance-plan.th.md`

## Objective

Implement and execute the next canonical structural specimen: a replayable
cantilever-beam solve that tests whether a finite transverse end load produces
the expected shear transfer, bending moment, displacement, axial bending stress,
reaction force/moment, and external work through a 3D solid.

## Scope

- Add a versioned SI rectangular cantilever configuration using the same
  synthetic linear-elastic material claim boundary as Work 034.
- Generate three predeclared Gmsh C3D4 meshes and distribute a transverse end
  load by boundary-triangle tributary area.
- Extend strict CalculiX parsing to retain complete element stress tensors while
  preserving Work 034 compatibility.
- Evaluate load-weighted tip displacement, support force and moment closure,
  external work, and an interior element-centroid `Sxx` bending-stress field.
- Compare against Euler-Bernoulli references only inside a declared slender,
  small-deflection and Saint-Venant interior gauge domain.
- Gate analytical agreement, force/moment equilibrium, exact volume/element
  coverage, mesh convergence, output freshness, hashes, and failure evidence.
- Add focused tests and bilingual physics/result documentation.

## Planned files

- `config/structural/beam_bending_acceptance_v1.json`
- `src/formula_ultimate/structural/acceptance.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_beam_bending_acceptance.py`
- `scripts/run_work035.ps1`
- `tests/test_beam_bending_acceptance.py`
- `tests/test_structural_acceptance.py`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.md`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.th.md`
- matching Work 035 plan/result records in English and Thai

## Experiment definition

### Preferred hypothesis

Within the declared Euler-Bernoulli domain, three independently meshed C3D4
cantilever solves close the transverse force and root moment, reproduce tip
deflection/external work within tolerance, reproduce the signed interior axial
bending-stress field within its separately declared tolerance, and converge
between the two finest meshes.

### Independent variable

- predeclared Gmsh characteristic mesh size at three levels

### Dependent variables

- mesh identity/count/volume and loaded/fixed surface identity;
- load-weighted transverse tip displacement and external work;
- support force and support moment about the declared origin;
- signed element-centroid `Sxx` versus Euler-Bernoulli stress in the declared
  interior gauge domain;
- analytical residuals, last-two-mesh changes, solver status, wall time,
  artifact/source/config/tool hashes, and typed failure evidence.

### Controls

- geometry, coordinate frame, material law/provenance, resultant force,
  tributary-area load distribution, clamp representation, element family/order,
  gauge exclusions, solver/mesher executables, tolerances, and compute policy.

### Falsification cases

- malformed/non-finite material, geometry, load, mesh, stress, or boundary
  identity is rejected;
- incorrect loaded-face area or unclosed nodal resultant fails;
- missing stress components/elements or duplicate evidence identities fail;
- force or moment closure, analytical response, and convergence each gate
  independently;
- clamp and load-introduction regions are excluded by declared geometry rather
  than silently selected after results are observed;
- no failed solve is replaced with an analytical value.

## Analytical reference

For beam length `L`, section width `b`, bending depth `h`, end force magnitude
`P`, `I = b*h^3/12`, centroid coordinate `z_c = h/2`, and interior element
centroid `(x, z)`:

```text
tip deflection magnitude = P*L^3/(3*E*I)
root moment magnitude    = P*L
Sxx(x,z)                 = P*(L-x)*(z-z_c)/I
external work            = P*tip_deflection/2
```

The stress sign will be checked against the declared negative-`z` load and
coordinate convention. A sign reversal is a failure, not an absolute-value pass.

## Validation

Planned fail-fast commands:

```powershell
py -3.14 -m unittest tests.test_beam_bending_acceptance tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

## Success criteria

- All three real Gmsh/CalculiX runs create fresh admitted evidence.
- Applied nodal forces close to the declared resultant.
- Support force and root moment close within predeclared tolerance.
- Tip displacement, external work, and signed interior `Sxx` field pass their
  predeclared analytical tolerances.
- The two finest meshes pass declared displacement/work/stress convergence.
- Focused/full/static/staged checks pass and the explicit commit succeeds.

## Risks

- First-order tetrahedra may be overly stiff in bending and may require finer
  meshes than tension.
- A fully fixed face creates local end stress effects; the stress gauge must be
  predeclared away from both clamp and load-introduction regions.
- Euler-Bernoulli theory omits shear deformation and local 3D effects. The beam
  must remain slender and the comparison domain explicit.
- Element-centroid stress is piecewise constant for C3D4 and may converge more
  slowly than global displacement.
- Passing this specimen does not validate yield, plastic collapse, buckling,
  fracture, fatigue, joints, contact, or a whole vehicle.

## Explicit non-goals

- No nonlinear material law, yield credit, fracture, fatigue, buckling,
  loaded-interface failure, connection removal, or `DNF` coupling.
- No arbitrary minimum thickness, design optimization, whole-car geometry,
  independent-solver agreement, physical coupon claim, push, or publication.
