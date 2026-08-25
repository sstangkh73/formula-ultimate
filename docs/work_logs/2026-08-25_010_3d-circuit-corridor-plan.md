# Work 010 Plan: Versioned 3D Circuit Corridor and Swept Envelope

Status: Completed

Thai companion: `2026-08-25_010_3d-circuit-corridor-plan.th.md`

## Objective

Create the durable bilingual queue for Work 010–019 and implement the first
item: a versioned circuit-corridor physics boundary that can represent
centerline curvature, grade, banking, left/right clearance, evidence quality,
and the kinematic swept envelope of a whole vehicle before race simulation.

## Scope

- Create a bilingual ten-item physics implementation queue covering Work
  010–019 and its completion order.
- Define strict SI-unit corridor segment, vehicle envelope, source evidence,
  integrated 3D station, and assessment contracts.
- Integrate piecewise-constant curvature, grade, and banking into deterministic
  3D reference stations.
- Screen static width, steering curvature, and inside/outside swept radial
  envelope for straight and constant-radius segments.
- Distinguish `admitted`, `rejected`, `indeterminate`, and synthetic
  verification outcomes. Non-surveyed geometry must not authorize a real race.
- Connect the corridor layer to the ten real-circuit catalogue without
  fabricating missing surveyed geometry.
- When the public real-circuit geometry evidence gap is confirmed, create a
  separate bilingual problem report and resolve it through an evidence-class
  gate, an import contract, and analytical fixtures rather than guessed data.
- Add unit, analytical-reference, invalid-input, evidence-gate, and
  deterministic-replay tests.
- Produce full bilingual result evidence, validate, and commit Work 010 before
  starting Work 011.

## Planned files

- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.th.md`
- `src/formula_ultimate/physics/corridor.py`
- `src/formula_ultimate/physics/__init__.py`
- `config/circuits/corridor_schema_v1.json`
- `scripts/validate_corridor.py`
- `tests/test_corridor.py`
- `docs/physics/CIRCUIT_CORRIDOR_MODEL.md`
- `docs/physics/CIRCUIT_CORRIDOR_MODEL.th.md`
- a separate bilingual problem report if the geometry-evidence problem occurs
- this Work 010 plan/result pair in English and Thai

The exact schema fixture path may change if a smaller deterministic interface
is sufficient; any deviation will be recorded.

## Model boundary

The Level-0/early-Level-1 corridor is a piecewise analytical representation.
It can reject a vehicle for insufficient static clearance, steering authority,
or constant-radius swept clearance. It cannot replace a laser scan, detailed
wall/kerb mesh, transient suspension pose, tyre slip, or collision engine.

Only geometry marked with an admission-capable evidence class may return
`admitted`. Approximate, digitized, or synthetic inputs remain visibly
non-authoritative even when their mathematical screen passes.

## Experiment definition

### Preferred hypothesis

A vehicle that passes static width can still be rejected by steering or swept
overhang on a curved corridor, so adding curvature and complete longitudinal
envelope materially constrains agent design before dynamics optimization.

### Independent variables

- corridor curvature and left/right widths;
- vehicle width, wheelbase, front/rear overhang, and maximum steering angle;
- geometry evidence class.

### Dependent variables

- required steering angle;
- inner and outer swept radii/margins;
- first failing segment and reason;
- admission status;
- deterministic 3D station coordinates and closure residual.

### Controls

- SI units and sign convention;
- fixed integration station spacing;
- vehicle reference point at rear-axle center;
- piecewise-constant segment assumption;
- identical evidence gate and tolerances across candidates.

### Falsification and failure criteria

- Construct a vehicle that passes static width but whose overhang violates the
  outer curved boundary and require rejection.
- Construct a vehicle whose required steer exceeds its declared limit and
  require rejection.
- Ensure a mathematically passing synthetic corridor cannot be called admitted.
- Reject non-finite, negative, impossible, discontinuous, or unsupported data.
- Report public real-circuit geometry that lacks survey-grade evidence as
  indeterminate, not zero curvature or guessed width.

## Validation

```powershell
python -m unittest discover -s tests -v
python scripts/validate_corridor.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate will run separately or with explicit fail-fast control flow.

## Success criteria

- The bilingual Work 010–019 queue exists and preserves sequential order.
- Corridor and vehicle contracts are strict, deterministic, and SI-based.
- Straight, left-turn, and right-turn analytical cases pass reference tests.
- Static-fit-but-swept-fail and steering-fail candidates are rejected.
- Unsupported real geometry remains indeterminate.
- A separate problem report records and resolves any evidence gap encountered.
- Full tests, compilation, bilingual Markdown contract, working/staged
  whitespace checks, commit, and post-commit verification pass.

## Risks

- Public official sources may provide diagrams but not surveyed 3D coordinates
  or explicit uncertainty.
- A constant-curvature rigid-body envelope omits tyre slip, roll, pitch,
  suspension travel, and wall deformation.
- Piecewise integration can accumulate closure error; it must remain observable.
- Treating approximate geometry as authoritative would create false physical
  confidence and unsafe agent incentives.

## Explicit non-goals

- No claim that all ten real circuits now have surveyed 3D geometry.
- No extraction of dimensions from unscaled marketing maps.
- No full collision mesh, tyre model, racing-line optimizer, or lap-time model.
- No Work 011 tyre implementation before Work 010 is validated and committed.
- No push to a remote repository.
