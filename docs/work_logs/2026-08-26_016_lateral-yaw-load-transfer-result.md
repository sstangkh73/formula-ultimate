# Work 016 Result: Lateral/Yaw Dynamics and Load Transfer

Status: Completed

Thai companion: `2026-08-26_016_lateral-yaw-load-transfer-result.th.md`

## Outcome

Work 016 is complete. `work016-planar-v1` now provides a deterministic Level-0
planar rigid-body step that accepts arbitrary full-rank ground-contact layouts,
projects quasi-static normal loads, resolves every contact through the Work 011
combined tyre-force boundary, advances lateral/yaw state, and preserves all
declared force/moment residuals and invalid conditions.

The preferred hypothesis is supported within this model boundary: steering,
combined-force saturation, and acceleration-dependent load transfer produce
coupled but deterministic force/yaw results. Deliberate singular geometry,
contact lift, and insufficient solver iterations are rejected rather than
silently repaired.

This is internal Level-0 analytical evidence, not physical validation or a
real vehicle-dynamics prediction.

## Files changed

- `src/formula_ultimate/physics/lateral.py`: topology-neutral contact contracts,
  normal-load projection, slip kinematics, combined-force coupling,
  fixed-point solve, planar integration, residuals, and observable invalidity.
- `src/formula_ultimate/physics/__init__.py`: public Work 016 API exports.
- `tests/test_lateral.py`: 11 steady, transient, load-transfer, saturation,
  topology, replay, balance, lift, singularity, convergence, and input tests.
- `scripts/validate_lateral.py`: reference and falsification validator.
- `docs/physics/LATERAL_YAW_LOAD_TRANSFER_MODEL.md` and `.th.md`: model
  equations, contracts, evidence, and limitations.
- `docs/problem_reports/2026-08-26_016_slotted-dataclass-serialization.md` and
  `.th.md`: separate resolved test/validator serialization problem.
- queue and this bilingual Work 016 plan/result pair.

## Decisions and evidence

1. Contact topology is an ordered arbitrary set, not a hard-coded four-wheel or
   two-axle layout. A three-contact delta fixture passes.
2. Baseline loads must equal vehicle weight and have zero pitch/roll moment.
3. Dynamic normal loads use the deterministic minimum-change projection
   `Fz = Fz0 + A^T(AA^T)^-1(b-AFz0)`.
4. Negative projected load is observable contact lift and invalidates the
   solve; no normal-load clipping occurs.
5. Local contact kinematics create a linear `-C_alpha*alpha` lateral request.
   Both requested forces then pass through the existing Work 011 ellipse.
6. Load transfer and tyre capacity close through a fixed-point iteration with
   declared limit, relaxation, absolute/relative tolerance, and iteration count.
7. State integration is explicit Euler using start-state derivatives. Force,
   yaw moment, load, convergence, saturation, and replay evidence remain in the
   result.

## Problem encountered and resolved

The first Work 016 run passed 10 tests but the steady-state evidence test errored
because it attempted `__dict__` serialization on a `slots=True` dataclass. The
validator contained the same assumption. The test now uses
`dataclasses.astuple`; the validator uses `dataclasses.asdict`. No physics value
or solver behavior changed. The separate problem report records the failure,
root cause, fix, and passing rerun.

## Experiment review

- Independent variables: contact topology/position/load, steering, cornering
  stiffness, friction limits, longitudinal request, mass, yaw inertia, CG
  height, state, step, relaxation, iteration limit, and tolerance.
- Dependent variables: projected loads, slip angles, requested/applied forces,
  utilization, saturation, total force/moment, accelerations, end state,
  iterations, status, and residuals.
- Controls: SI/sign convention, Work 011 law, deterministic contact order,
  fixed control values, identical initial state, and zero random draws.
- Metrics: six balance residuals, convergence iterations, load direction,
  saturation count/utilization, response signs, and exact replay equality.
- Supporting evidence: straight equilibrium closes in one iteration with all
  six residuals zero; positive steering produces positive lateral/yaw response;
  analytical longitudinal/lateral load transfer has exact zero load residuals;
  transient replay is exactly equal.
- Falsifying evidence: an over-limit combined request saturates; a high-CG/high
  acceleration case produces raw negative loads and invalid contact lift;
  collinear geometry is rank-deficient; one iteration returns non-convergence.
- Contradicting evidence: the first test harness run errored, but did not
  contradict the physical balances; it remains preserved in the problem report.
- Alternative explanations: response-sign tests alone could pass with wrong
  magnitudes, so separate analytical equilibrium, force/moment residual, tyre
  utilization, and replay checks are required.
- Missing evidence: calibrated nonlinear tyres, roll/pitch/heave dynamics,
  suspension, aero, road geometry coupling, relaxation, temperature, wear, and
  independent/higher-fidelity validation.
- Confidence: high for deterministic software contracts and declared balance
  accounting; low/none for real vehicle response or race performance.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast handling.

```powershell
python -m unittest tests.test_lateral -v
```

Exit status: `0`; `Ran 11 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 121 tests`; `OK`.

```powershell
python scripts/validate_lateral.py
```

Exit status: `0`. Relevant output:

```text
steady: status ok, iterations 1, all six residuals 0
transient a_y: 0.6665333377777185 m/s^2
transient yaw acceleration: 0.6665333377777185 rad/s^2
transient iterations: 33; replay_equal: true
transient pitch residual: -1.8613102170661477e-09 N*m
transient roll residual: 9.311389703725581e-08 N*m
load transfer front/rear: 5486.0 / 6286.0 N
load transfer left/right: 4761.0 / 7011.0 N
load residuals: 0
combined-force saturated contacts: 3
maximum applied utilization: 1.0
one-iteration falsification: invalid, did not converge
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each. Full validation is rerun after this result; staged
scope/check runs before commit.

## Limitations and follow-up

- Load transfer is quasi-static and has no suspension or body roll/pitch state.
- The linear slip request is not a calibrated tyre model.
- Explicit Euler response is time-step dependent.
- No aero, braking/regen, degradation, circuit-line coupling, or race-loop
  integration is included in Work 016.
- Work 017 will own aerodynamic force, balance, and cooling flow; it was not
  started here.
- Commit hash is reported in final handoff; no remote push is performed.
