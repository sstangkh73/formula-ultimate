# Work 051 Plan: Gate A Element and Boundary Remediation

Status: Completed

Thai companion: `2026-08-30_051_gate-a-remediation-plan.th.md`

## Objective

Resolve or explicitly bound the two retained Gate A blockers before Work 046: the Work 041 near-critical C3D4/C3D10 disagreement and the Work 045 support-boundary transferability rejection.

## Scope and claim boundary

This work will run two solver-backed remediation studies on the existing synthetic fixtures. It may admit a narrower verified evaluation domain when evidence supports it; it will not rewrite the rejected Work 041 or Work 045 outcomes. It does not validate post-buckling response, real joints, contact, material allowables, a complete vehicle, or physical hardware.

## Experimental design

### Element-family remediation

- Independent variables: C3D10 characteristic mesh size and absolute precritical load.
- Dependent variables: eigenvalue load, nonlinear amplification, last-two refinement change, analytical secant error, reactions, solver status, mesh size, and evidence hashes.
- Controls: Work 041 geometry, material, imperfection field, load schedule, end-face loading, solver, and parser.
- Preferred hypothesis: a preregistered C3D10 refinement series converges within `5%` at every admitted load and remains within `5%` of the analytical precritical secant reference.
- Failure criterion: any missing/non-finite solve, mode-family change, last-two change above `5%`, or secant error above `5%` rejects the C3D10 route.
- Bounding rule: C3D4 remains inadmissible for near-critical promotion where the retained Work 041 cross-family difference exceeds `5%`; no averaging or silent correction is allowed.

### Boundary-domain remediation

- Independent variables: support topology identity and support representation identity.
- Dependent variables: topology signature, admitted-comparison status, compliance change, force/moment/energy residuals, and load shares.
- Controls: Work 045 STEP geometry, material, load interface, load, fine mesh, solver, and result parser.
- Preferred hypothesis: equivalent encodings of the same two-support topology replay identically within numerical tolerance, while deletion of a support is classified as a topology mutation and cannot be used as evidence of representation transferability.
- Failure criterion: a representation-only mutation changes the topology signature or response beyond tolerance, or a changed support set is silently admitted as the same topology.
- Bounding rule: the Work 045 one-support result remains contradictory evidence for transfer to other support topologies; any admitted structural-fitness use is restricted to an exact declared support topology and boundary-model identity.

## Planned files

- `config/structural/gate_a_remediation_v1.json`
- `src/formula_ultimate/structural/gate_a_remediation.py` and package exports
- `scripts/structural/run_gate_a_remediation.py`
- `scripts/run_work051.ps1`
- `tests/test_gate_a_remediation.py`
- `docs/physics/GATE_A_ELEMENT_BOUNDARY_REMEDIATION.md` and `.th.md`
- matching Work 051 bilingual result records
- ignored evidence under `artifacts/work051/`

## Validation

Run focused unit tests, the deterministic Work 051 experiment, Work 041 and Work 045 regressions, the full repository suite, Python compilation, repository-contract checks, staged-diff checks, an explicit scoped commit, and a clean-tree replay.

## Success criteria

- Every experiment and negative control fails closed on invalid identity or evidence.
- The element study either supports C3D10 convergence or retains Gate A as blocked with exact evidence.
- The boundary study distinguishes representation changes from topology changes and reports both without erasing Work 045's rejection.
- A machine-readable decision states whether Gate A is closed, narrowly bounded, or still blocked and whether Work 046 may start.

## Risks

Refined quadratic meshes may exceed the practical compute budget. An exact support-topology identity contract can bound evidence but cannot establish contact, preload, friction, or arbitrary-joint transfer. Analytical secant agreement is not independent physical validation.

## Explicit non-goals

No Work 046 failure coupling, whole-vehicle CAD, whole-vehicle load cases, design search, post-buckling capacity, real-material certification, push, or publication is included.
