# Geometry-General Structural Evaluator v1

Thai companion: `GEOMETRY_GENERAL_EVALUATOR_V1.th.md`

Protocol version: `geometry_general_evaluator_v1`. Implemented by Work 138.

## 1. What this contract covers

Any valid single solid can be scored. The evaluator reads geometry, not design
variables:

```text
STEP solid (or the registered benchmark box)
  -> Gmsh second-order tetrahedral mesh at three or more refinement levels
  -> geometry-derived volume, mass, centre of mass and point-mass inertia
  -> CalculiX C3D10 linear static solve per registered load case
  -> displacement, von Mises, reaction balance, utilization
  -> exactly one registered status, with evidence hashes
```

No candidate may declare its own stiffness, strength or margin. A declared mass
is checked against the mesh, never trusted.

## 2. Status vocabulary

| Status | Meaning |
| --- | --- |
| `passed` | Converged, balanced, and within the declared allowable |
| `failed_physics` | Solved, and outside the declared allowable, or its declared mass is contradicted |
| `unresolved_mesh` | No mesh at the coarsest registered level, or the mesh exceeds the node budget |
| `unresolved_solver` | Solver did not complete, or the reaction does not balance the applied resultant |
| `unresolved_convergence` | Fewer than three solved levels, or the last two exceed the registered change limits |
| `unsupported_representation` | Not one valid tetrahedral solid, or the declared selections are unusable |

`unresolved_*` is a statement about the tooling, never about the design. A run
reports the count and the cause of every unresolved candidate, because that
distribution is the evidence for which capability to add next.

## 3. Numerical registration

Frozen in `config/development/geometry_general_evaluator_v1.json` before any
admitted run: element type `C3D10`; at least three mesh levels, strictly coarse
to fine, expressed as Gmsh `Mesh.MeshSizeFactor`; the convergence limits on
maximum displacement and p90 von Mises between the last two solved levels; the
allowable and the material source per material; load cases with their
selections and resultants; the reaction-balance and declared-mass residuals;
and the node, time and retry budgets.

## 4. Meshing and solver constraints

- **Straight-sided quadratic elements.** `Mesh.SecondOrderLinear = 1`. Curving
  midside nodes onto a curved boundary produced inverted elements that
  CalculiX rejects with a nonpositive jacobian. The cost is a faceted curved
  surface, which is a registered geometric approximation.
- **Field width.** CalculiX reads a free field into a 20-character buffer. A
  21-character scientific value is silently truncated — measured in Work 138:
  `-1.00000000000000e+03` was read as `-1.0` and returned exit code 0 with a
  displacement 1000x too small — and 22 characters or more abort the run. Every
  numeric field is therefore written through `calculix_number`, and the deck is
  re-checked field by field before it is handed to the solver.
- **Consistent surface load.** A resultant is distributed over a TRI6 face with
  the exact consistent weights: corner shape functions integrate to zero and
  each midside integrates to `A/3`. The distributed load must close on the
  declared resultant within `1e-12`.

## 5. Mandatory controls

Every admitted run exercises eight controls and must reject all of them:
`analytical_benchmark`, `under_refined_mesh`, `unsupported_representation`,
`declared_mass_contradiction`, `removed_load_case`,
`post_observation_allowable`, `deterministic_restatement`, and
`work062_refined_disagreement_reevaluated`. A surviving control sets the run
status to `failed_controls`.

## 6. Acceptance and claim boundary

A run is admitted as `passed_geometry_general_structural_evaluation` only when
all eight controls are rejected, every candidate carries exactly one registered
status, and a clean replay reproduces the result SHA-256 exactly.

That status means a structural evaluation of the declared solids under the
declared load cases. It is not promotion, not manufacturability, not race time,
and not physical validation. Materials are synthetic geometry-only values
unless their evidence class says otherwise.

## 7. Comparison rule

Results from this evaluator must never be compared against results from the
scaling-law campaign evaluator in `whole_vehicle_search`. Any comparison
requires every arm, including the fixed-topology baseline, to be re-evaluated
here under the same mesh, solver, retry and budget registration.
