# Work 080 Plan: Mechanical Assembly and Joint Kernel

Status: In progress

Thai companion: `2026-09-02_080_mechanical-assembly-joint-kernel-plan.th.md`

## Objective and scope

Begin the next three-work batch by preregistering the detailed Work 080-086 execution program, then implement the first geometry-causal mechanical assembly kernel. Work 080 must assemble Work 077/078 physical-part declarations through datum-, axis-, and surface-based constraints; calculate realized degrees of freedom; enforce joint limits and clearance; detect alignment, interference, looseness, and overconstraint; and preserve deterministic replay identities.

This plan does not mark Work 080 implemented. The immediate documentation change creates `docs/plans/WORKS_080_086_DETAILED_EXECUTION_PLAN.md` and its Thai companion. Work 080 remains `In progress` until its declared code, experiments, negative controls, full validation, bilingual result, and separate implementation commit succeed.

## Experiment design

- Independent variables: part topology, datum/interface transforms, mate type, declared joint axes/limits, bearing spacing/alignment, clearance/tolerance, preload declaration, connection compliance, and motion sample.
- Dependent variables: constraint rank, realized translational/rotational DOFs, mate residuals, alignment error, axial/radial clearance, interference depth, minimum gap, motion-envelope collisions, and deterministic assembly identity.
- Controls: admitted reference mechanism, mirrored/permuted declaration replay, misaligned shaft, redundant two-bearing lock, excessive clearance, too-tight interference, collision across joint travel, incorrect intended DOF, duplicate/missing interface, and non-finite transform.
- Preferred hypothesis: the admitted reference assembly realizes exactly its declared motion while every malformed, overconstrained, underconstrained, misaligned, colliding, or identity-drifting control fails closed before downstream physics.
- Falsification: silently dropping a constraint, auto-aligning geometry, clipping joint motion, accepting residual penetration, reporting declared rather than calculated DOF, or changing the assembly result when only mapping-key order changes.

## Planned files

- `docs/plans/WORKS_080_086_DETAILED_EXECUTION_PLAN.md` and Thai companion
- Work 080 schema/config under `config/assembly/`
- assembly/joint implementation under `src/formula_ultimate/assembly/` or the reviewed package boundary
- deterministic runner under `scripts/assembly/`
- focused unit/acceptance/negative-control tests
- bilingual Work 080 contract/research record and matching result record
- ignored solver/geometry evidence under `artifacts/work080/`

Exact implementation filenames remain proposals until repository-boundary review at the start of code work; the program plan lists the intended artifacts and interfaces for all seven remaining works.

## Validation and success criteria

The detailed EN/TH program plan must cover Works 080-086, their dependencies, independent/dependent variables, controls, metrics, artifacts, proposed commands, success/failure gates, claim boundaries, and stop/go rules. For eventual Work 080 completion, focused tests, deterministic replay, full regression, compilation, bilingual contract, explicit staged scope, `git diff --cached --check`, one implementation commit, and post-commit replay must pass. Geometry/config must be frozen before the first admitted Work 080 run.

## Risks and explicit non-goals

Constraint-rank calculations can be numerically sensitive near singular configurations. Collision-free sampled motion does not prove continuous clearance unless the declared continuous/swept-volume check passes. Work 080 does not validate bearing life, contact friction, fastener/weld strength, wear, full multibody dynamics, or physical safety. Later Work plans do not authorize starting their implementations before dependencies pass.
