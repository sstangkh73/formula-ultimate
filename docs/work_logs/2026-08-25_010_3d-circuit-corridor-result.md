# Work 010 Result: Versioned 3D Circuit Corridor and Swept Envelope

Status: Completed

Completed on: 2026-08-26 (Asia/Bangkok)

Thai companion: `2026-08-25_010_3d-circuit-corridor-result.th.md`

## Outcome

Work 010 is complete. The repository now has a durable sequential Work 010–019
physics queue and a deterministic SI-based corridor gate that integrates
piecewise-constant curvature, grade, and bank into 3D stations. It screens a
whole rigid vehicle for static width, bicycle-model steering authority, and
inside/outside constant-radius swept clearance.

The preferred hypothesis was supported by the falsifying fixture: a 2.0 m-wide
vehicle fits a 3.0 m total static corridor, yet is rejected on a 5.0 m-radius
curve because its front outside corner produces a negative swept margin.

No Level-0 physical-validation claim is made. The ten real circuit profiles
remain `indeterminate` because no admission-capable surveyed 3D corridor is
present in the reviewed evidence.

## Files changed

- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` and `.th.md`: sequential Work
  010–019 queue, completion gates, and shared definition of done.
- `src/formula_ultimate/physics/corridor.py`: strict evidence, segment,
  corridor, vehicle, station, closure, swept-envelope, assessment, parsing, and
  loading contracts.
- `src/formula_ultimate/physics/__init__.py`: public corridor API exports.
- `config/circuits/corridor_schema_v1.json`: three analytical fixtures under
  schema `1.0`; explicitly not real-circuit geometry.
- `scripts/validate_corridor.py`: deterministic fixture and ten-circuit
  evidence-coverage validator.
- `tests/test_corridor.py`: 15 analytical, negative-input, evidence-gate,
  closure, symmetry, and replay tests.
- `docs/physics/CIRCUIT_CORRIDOR_MODEL.md` and `.th.md`: equations, coordinate
  convention, evidence states, model boundary, and limitations.
- `docs/problem_reports/2026-08-25_010_survey-geometry-evidence-gap.md` and
  `.th.md`: separate problem investigation and bounded resolution.
- this Work 010 plan/result pair in English and Thai.

## Implemented contracts and decisions

1. All geometry uses metres, `1/m`, and radians. Segment length is horizontal
   plan distance; positive curvature turns left and positive grade raises `z`.
2. The vehicle rear-axle center follows the corridor centerline. Width,
   wheelbase, front/rear overhang, and steering limit define the rigid envelope.
3. Constant-curvature integration uses the exact analytical arc update, while
   station spacing affects output sampling only.
4. Horizontal source uncertainty is subtracted from both corridor sides before
   clearance assessment. Invalid/non-finite values fail rather than being
   corrected.
5. Any geometry or steering failure returns `rejected`. A passing synthetic
   fixture returns `verification_passed`; approximate data remains
   `indeterminate`; only `surveyed` or `operator_engineering` evidence can
   return `admitted`.
6. Closure position, height, and wrapped heading residuals are observable and
   are never silently closed.

## Problem encountered and resolution

The Work 008 catalogue does not contain survey-grade centerlines, boundaries,
wall/kerb geometry, coordinate reference systems, timestamps, and quantified
uncertainty for all ten layouts. The problem was documented separately rather
than hidden inside this result.

The software/research boundary is resolved by a versioned import contract,
evidence-class gate, transparent analytical fixtures, explicit residuals, and
`indeterminate` outcomes for unsupported real tracks. This does not manufacture
the missing data. Licensed survey or circuit-operator engineering data remains
required for real-circuit admission.

## Experiment review

- Independent variables: segment curvature and widths; vehicle width,
  wheelbase, overhangs, steering limit; evidence class and uncertainty.
- Dependent variables: 3D stations, steering demand, inside/outside margin,
  first failure, closure residual, and admission status.
- Controls: SI/sign convention, rear-axle reference, constant segment
  properties, deterministic spacing, identical evidence gate.
- Supporting evidence: the full-circle analytical closure residual is
  `4.898587196589412e-15 m` horizontal, `0.0 m` vertical, and
  `2.4492935982947064e-16 rad` heading; left/right quarter-circle endpoints
  match their analytical mirrors.
- Contradicting/falsifying evidence: the static-fit fixture fails the outside
  sweep; the high-curvature fixture fails steering; synthetic success cannot
  produce `admitted`.
- Alternative explanation excluded: a failure is not inferred merely from
  total width; steering and swept geometry are individually observable.
- Missing evidence: real survey-grade corridor data and higher-order vehicle
  dynamics.
- Confidence: high for the implemented equations and software behavior against
  the declared analytical boundary; low/none for real-circuit admission until
  authoritative geometry is supplied.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast exit handling.

### Work-specific unit tests

```powershell
python -m unittest tests.test_corridor -v
```

Exit status: `0`. Relevant output: `Ran 15 tests`; `OK`.

### Full repository tests

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`. Relevant output: `Ran 57 tests`; `OK`.

### Deterministic validator

```powershell
python scripts/validate_corridor.py
```

Exit status: `0`. Relevant output:

```text
synthetic_full_circle_pass: verification_passed
synthetic_overhang_reject: rejected
synthetic_steering_reject: rejected
real circuit total: 10
real circuit admitted: 0
real circuit indeterminate: 10
```

### Compilation and whitespace

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each command. `git diff --cached --check` is rerun after
explicit staging and before the commit.

## Limitations

- The planar rigid-body envelope omits tyre force, slip, compliance, roll,
  pitch, suspension, walls, kerbs, collision, and transient yaw.
- Grade and bank are represented but do not change force capacity or swept
  clearance in Work 010.
- Analytical fixtures verify equations; they are not physical or real-circuit
  validation.
- Real admission requires separately licensed/audited geometry ingestion.

## Follow-up

Proceed to Work 011 only after the Work 010 commit and post-commit state are
verified. Work 011 will implement tyre-road longitudinal/lateral force and an
observable saturation boundary without changing Work 010 evidence semantics.
