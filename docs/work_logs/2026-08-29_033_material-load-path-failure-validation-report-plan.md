# Work 033 Plan: Material Load-Path and Failure Validation Report

Status: Completed

Thai companion: `2026-08-29_033_material-load-path-failure-validation-report-plan.th.md`

## Objective

Produce an implementation-ready experiment plan that verifies force and torque
transmission through actual geometry and material models before Formula
Ultimate uses structural fitness or begins whole-vehicle geometry search.

## Scope

- Define a material-law and solver evidence boundary without imposing arbitrary
  human-preferred thickness or shape limits.
- Plan analytical and finite-element validation for tension, beam bending,
  shaft torsion, buckling, loaded-interface load transfer, and vehicle failure
  coupling.
- Specify geometry, boundary conditions, independent/dependent variables,
  controls, mesh studies, analytical references, success/failure criteria, and
  falsification cases for every specimen.
- Separate physical failure, numerical invalidity/non-convergence, and optional
  manufacturing constraints.
- Define how yield, deformation, buckling, fracture, and fatigue evidence will
  remove or degrade a physical connection and propagate to subsystem failure
  or `DNF`.
- Record the verified local solver inventory and risks relevant to future
  implementation.
- Maintain separate English and Thai report versions.

## Planned Files

- `docs/reports/MATERIAL_LOAD_PATH_FAILURE_VALIDATION_PLAN.md`
- `docs/reports/MATERIAL_LOAD_PATH_FAILURE_VALIDATION_PLAN.th.md`
- matching Work 033 plan/result records in English and Thai

This is a documentation-only work item. It will not implement material laws,
generate meshes, run FEA specimens, mutate candidate geometry, or change the
vehicle simulator.

## Current Tool Evidence to Preserve

- FreeCAD `1.1.3` bundled Python imports `FreeCAD`, `Part`, and `Fem`.
- `C:\Program Files\FreeCAD 1.1\bin\ccx.exe` identifies itself as CalculiX
  `2.22` but returns exit code `201` for `-v`.
- `C:\Program Files\FreeCAD 1.1\bin\gmsh.exe` reports `4.15.0` in the version
  probe but also returns exit code `201` in the observed invocation.
- Future launchers must require expected solver artifacts and parsed evidence;
  neither a process exit code nor console text alone is sufficient.

## Experiment Questions

1. Do displacement, strain, stress, reaction, and strain-energy results match
   analytical references in the linear regime?
2. Does torque produce the correct shear-stress distribution and twist angle?
3. Does the solver detect elastic instability and preserve buckling-mode and
   eigenvalue evidence?
4. Do loads applied at declared interfaces cross the candidate geometry and
   close force/moment equilibrium?
5. Are mesh sensitivity, boundary-condition sensitivity, singularities, and
   non-convergence observable rather than silently accepted?
6. Can structural failure deterministically break/degrade a connection and
   change the coupled vehicle outcome or produce `DNF`?

## Validation

Planned commands:

```powershell
py -3.14 -m unittest tests.test_repository_contract -v
py -3.14 -m unittest discover -s tests -q
git diff --check
git diff --cached --check
```

The result record will capture exact exit codes and concise output.

## Success Criteria

- All six experiment families include hypotheses, variables, controls,
  equations/reference solutions, pass/fail rules, and falsification attempts.
- Thin geometry is not rejected by arbitrary engineering preference; it fails
  only through declared task boundaries, physical material/instability/fatigue
  laws, or observable numerical-resolution limits.
- Physical failure is distinguished from solver invalidity and unsupported
  physics.
- The plan defines reaction-force/moment closure, energy consistency, mesh
  convergence, and boundary-condition audits.
- Failure coupling preserves event time, broken connection identity, released
  or dissipated energy policy, downstream state changes, and replay metadata.
- The report does not call analytical agreement or one FEA run physical
  validation.
- Bilingual, repository, whitespace, and staged-scope checks pass and the work
  is committed.

## Risks

- A fixed minimum thickness would encode a human design preference rather than
  test physics.
- A mesh that cannot resolve thin geometry can be confused with physical
  failure.
- Linear elasticity cannot predict plastic collapse, fracture, or fatigue.
- Idealized clamps and point loads can create artificial stiffness or stress
  singularities.
- Eigenvalue buckling alone does not establish post-buckling capacity.
- CalculiX/FreeCAD/Gmsh process and artifact behavior must be acceptance-tested
  on the installed versions before campaign use.
- A structural failure event can violate force/energy conservation if a
  connection is removed without an explicit release/dissipation model.

## Explicit Non-Goals

- No completed FEA, structural implementation, material calibration, physical
  test, safety certification, or autonomous design search.
- No arbitrary conventional layout, thickness, web, or feature-size rule as a
  substitute for physics.
- No claim that one isotropic material law covers composites, anisotropy,
  joints, adhesives, welds, temperature dependence, or rate effects.
- No full crash, fracture-mechanics, composite-failure, or manufacturing model
  in the first implementation phase.
- No push, publication, external upload, or history rewrite.
