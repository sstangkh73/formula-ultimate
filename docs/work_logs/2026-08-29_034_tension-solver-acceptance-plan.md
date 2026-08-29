# Work 034 Plan: Tension Solver Acceptance Harness

Status: Completed

Thai companion: `2026-08-29_034_tension-solver-acceptance-plan.th.md`

## Objective

Implement and execute the first accepted structural solve for Formula Ultimate:
a fail-closed, replayable axial-tension specimen that proves the local
`3D geometry -> Gmsh mesh -> CalculiX solve -> parsed evidence -> analytical
and mesh-convergence gates` route.

## Scope

- Define a versioned SI-unit tension experiment with a rectangular prismatic
  solid, isotropic linear-elastic material, distributed end traction, and a
  fixed support face.
- Generate Gmsh geometry and first-order tetrahedral meshes at three predeclared
  characteristic sizes.
- Convert the exact Gmsh mesh into a CalculiX input deck with surface-area-
  weighted nodal loads over the finite loaded face.
- Execute CalculiX in isolated artifact directories and require fresh expected
  output plus parsed completion evidence.
- Parse displacements, reactions, non-singular axial stress evidence, and
  external-work/strain-energy consistency where the accepted solver output
  supports it.
- Compare against `sigma = F/A`, `epsilon = sigma/E`,
  `delta = FL/(AE)`, and `U = F*delta/2`.
- Gate force closure, analytical agreement, finiteness, topology/mesh identity,
  and last-two-mesh convergence without imposing a physical minimum thickness.
- Preserve source/config/tool/input/output hashes, commands, exit behavior,
  wall time, mesh counts/quality evidence, repository identity, failures, and a
  structured falsification review under ignored `artifacts/work034/`.
- Add unit and integration tests that do not require external solver processes,
  plus one live acceptance launcher for this installed toolchain.
- Maintain all Markdown in English/Thai pairs.

## Planned Files

- `config/structural/tension_solver_acceptance_v1.json`
- `src/formula_ultimate/structural/__init__.py`
- `src/formula_ultimate/structural/acceptance.py`
- `scripts/structural/run_tension_acceptance.py`
- `scripts/run_work034.ps1`
- `tests/test_structural_acceptance.py`
- `docs/physics/TENSION_SOLVER_ACCEPTANCE.md`
- `docs/physics/TENSION_SOLVER_ACCEPTANCE.th.md`
- matching Work 034 plan/result records in English and Thai

The exact adapter/parser split may change after observing real Gmsh/CalculiX
artifacts. Any deviation will be recorded.

## Experiment Definition

### Preferred hypothesis

Within the declared small-strain linear-elastic range, all three solver meshes
produce a valid connected solid, close the applied axial force through support
reactions, reproduce analytical end displacement and axial stress within
predeclared tolerances, and show converged global response between the two
finest meshes.

This is solver-route verification, not general structural or physical
validation.

### Independent variables

- predeclared Gmsh characteristic mesh size (three levels)

### Dependent variables

- node/tetrahedron/boundary-face counts and mesh identity;
- loaded-end axial displacement;
- support reaction and force residual;
- named non-singular axial stress evidence;
- external work and admitted internal energy evidence;
- analytical residuals, mesh-to-mesh changes, solver status, exit behavior,
  artifacts, hashes, and wall time.

### Controls

- bar length/cross-section and coordinate frame;
- material `E`, `nu`, and density assumptions;
- applied resultant force and surface-load distribution algorithm;
- Gmsh/CalculiX executables, element family/order, solver step, parsing rules,
  tolerances, resource policy, and repository/source/config identity.

### Falsification and failure cases

- Unit tests reject malformed/non-finite config, zero/negative geometry,
  incomplete/disconnected mesh evidence, wrong boundary identity, stale/missing
  solver output, unclosed nodal load, malformed/non-finite results, and
  excessive analytical or convergence residuals.
- The live route fails if Gmsh or CalculiX returns unacceptable process/artifact
  evidence, regardless of later files.
- No failed mesh/solve is retried silently or replaced with an analytical value.
- Singular peak stress is not used as the stress metric.

## Validation

Planned fail-fast commands:

```powershell
py -3.14 -m unittest tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exact commands, exit codes, relevant outputs, solver/parser behavior, artifacts,
hashes, limitations, and the final commit will be recorded in the result.

## Success Criteria

- Three declared meshes are generated and solved through the real installed
  Gmsh and CalculiX executables.
- Each mesh contains one admitted 3D load path and finite support/load faces.
- Distributed nodal loads sum to the exact declared resultant within tolerance.
- Fresh solver evidence proves completion; stale/missing output fails closed.
- Force equilibrium closes and analytical displacement/stress/energy evidence
  passes declared tolerances.
- The two finest meshes satisfy the declared global-response convergence gate.
- Replay metadata and source/artifact hashes are sufficient to reproduce the
  semantic run.
- Focused/full/static/repository/staged checks pass and the explicit work-item
  commit succeeds.

## Risks

- CalculiX and Gmsh CLI exit behavior on this bundled Windows installation may
  differ between version probes and actual runs.
- Gmsh physical-surface export and tetrahedral face identity may require an
  explicit project-owned mesh conversion step.
- Equal nodal loads do not represent uniform traction; the adapter must weight
  end-face nodes by surface triangle tributary area.
- Fully fixed end nodes can create local Poisson/end effects; displacement and
  stress gauges must remain away from that boundary.
- Linear tetrahedra may be stiff or converge slowly; failure to meet declared
  tolerances must remain evidence and may require a separately planned element-
  order change.
- Solver output formats may be version-specific; parser tests must use minimal
  committed fixtures or generated strings and fail on unknown structure.
- Linear elasticity cannot establish yield redistribution, fracture, fatigue,
  buckling, or arbitrary candidate safety.

## Explicit Non-Goals

- No bending, torsion, buckling, loaded-interface, plasticity, fracture,
  fatigue, post-failure, or vehicle `DNF` implementation in this work item.
- No arbitrary minimum thickness, manufacturability constraint, component
  optimization, design-agent search, or whole-vehicle geometry.
- No claim of physical validation, independent solver agreement, safety,
  certification, or real-world material accuracy.
- No cloud execution, external upload, push, publication, or history rewrite.
