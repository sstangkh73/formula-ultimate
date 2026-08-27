# Work 017 Result: Aerodynamic Force, Balance, and Cooling Flow

Status: Completed

Thai companion: `2026-08-28_017_aerodynamic-force-balance-cooling-result.th.md`

## Outcome

Work 017 is complete. `work017-aerodynamic-map-v1` now evaluates a provenance-
bearing coefficient grid across declared airspeed, ride height, yaw, and
discrete active-state envelopes. It returns interpolated drag, side force,
downforce, pitch/yaw moments, signed longitudinal centre of pressure, ram-air
mass flow, cooling conductance, signed heat flow, interpolation evidence, and
eight algebraic residuals.

The preferred hypothesis is supported inside the declared software boundary:
the synthetic reference exposes deterministic speed, ride-height, yaw, and
active-state trade-offs while every unsupported envelope query remains
`invalid`. Synthetic evidence remains explicitly distinguishable from
geometry-derived evidence.

This is Level-0 software and analytical evidence, not CFD, measurement, or
physical validation.

## Files changed

- `src/formula_ultimate/physics/aerodynamics.py`: evidence contracts, complete
  coefficient grids, tensor interpolation, force/moment/cooling equations,
  residuals, and observable invalidity.
- `src/formula_ultimate/physics/__init__.py`: public Work 017 API exports.
- `tests/test_aerodynamics.py`: 11 analytical, envelope, provenance, replay,
  cooling, malformed-grid, and numerical-failure tests.
- `scripts/validate_aerodynamics.py`: synthetic two-state reference validator.
- `docs/physics/AERODYNAMIC_FORCE_BALANCE_COOLING_MODEL.md` and `.th.md`: model,
  sign/evidence contracts, equations, integration boundary, and limitations.
- `docs/problem_reports/2026-08-28_017_aerodynamic-speed-scaling-wording.md` and
  `.th.md`: corrected `inverse-square` wording to `speed-squared` before code.
- `docs/problem_reports/2026-08-28_017_interpolation-fraction-exact-assertion.md`
  and `.th.md`: floating-point assertion failure, fix, and passing rerun.
- queue and this bilingual Work 017 plan/result pair.

## Decisions and evidence

1. The map is topology-neutral and does not prescribe wings, body shape, wheel
   count, or conventional vehicle architecture.
2. Provenance bases are `synthetic_reference`, `geometry_derived`, `cfd`, and
   `measured`. Geometry-derived maps require a lowercase SHA-256 geometry digest.
3. Axes are strictly increasing and every active state must contain the complete
   speed-major, height, yaw grid. Active states are discrete.
4. Tensor-linear interpolation exposes every bracket and fraction. Exact nodes
   remain exact; outside points and unknown states are never clamped.
5. Dynamic pressure produces drag, side/down force, and pitch/yaw moment. Centre
   of pressure is derived only for non-zero signed downforce.
6. Ram-air flow produces mass flow, air heat-capacity rate, effective cooling
   conductance, and signed heat rejection. Active-device energy is not hidden
   inside the airflow model.
7. Eight residuals independently close force, moment, mass-flow, conductance,
   and heat-flow equations; runtime non-finite output returns `invalid`.

## Problems encountered and resolved

1. The initial plan incorrectly said `inverse-square force scaling` although its
   equation correctly used `V^2`. Both plans were corrected to `speed-squared`
   before implementation, and a separate bilingual report preserves the issue.
2. The first test run passed 10 tests and failed one exact equality assertion:
   binary floating point represented the ride-height midpoint fraction as
   `0.4999999999999999`, not decimal `0.5`. Fraction checks now use
   `assertAlmostEqual`; exact-node identity and full replay remain exact. The
   rerun passed all 11 tests and the raw fraction remains observable.
3. One documentation patch command was rejected before writing because a code
   block lacked patch line prefixes. The files were then added separately; no
   partial file or repository state was created.

## Experiment review

- Independent variables: map/provenance, continuous axes, active state,
  airspeed/density, ride height, yaw, reference area/length, inlet area, air
  heat capacity, effectiveness, and air/component temperature.
- Dependent variables: coefficients, interpolation brackets/fractions, dynamic
  pressure, five force/moment outputs, centre of pressure, three cooling-path
  outputs, heat flow, eight residuals, status, and reason.
- Controls: SI/sign contracts, fixed grid order, tensor-linear interpolation,
  no extrapolation, discrete active states, identical inputs, zero random draws.
- Metrics: exact-node/interior error, all residuals, `V^2` force ratio, `V`
  mass-flow ratio, yaw symmetry/antisymmetry, active-state drag/cooling delta,
  exact replay, and invalid-case coverage.
- Supporting evidence: all eight residuals are zero at the validator point;
  `40/20 m/s` drag ratio is `4.0`; mass-flow ratio is `2.0`; cooling-open state
  increases both drag and flow; replay is exact.
- Falsifying evidence: each continuous axis outside its bounds, unknown active
  state, incomplete/duplicate grids, invalid coefficients/provenance, and
  non-finite runtime output are rejected. `41 m/s` against a `0–40 m/s` map
  returns `invalid` rather than clamping.
- Contradicting evidence: the initial exact fraction assertion failed and is
  preserved in its report; it contradicted the assertion method, not the
  coefficient outputs.
- Alternative explanations: speed ratios alone could pass with a constant but
  incorrectly indexed map, so exact-node, interior interpolation, yaw symmetry,
  active state, provenance, and bracket evidence are tested separately.
- Missing evidence: geometry-linked CFD/measurement, uncertainty, mesh and
  convergence studies, pressure-drop/UA/fan work, transient flow, and coupling
  into Work 014–016 dynamics.
- Confidence: high for deterministic map/interpolation/algebra contracts; low or
  none for real candidate aerodynamics because the reference is synthetic.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast handling.

```powershell
python -m unittest tests.test_aerodynamics -v
```

Exit status: `0`; `Ran 11 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 132 tests`; `OK`.

```powershell
python scripts/validate_aerodynamics.py
```

Exit status: `0`. Relevant output:

```text
evidence basis: synthetic_reference; geometry_sha256: null
dynamic pressure: 240.0 Pa
coefficients: Cd 0.63, Cy 0.035, Cdown 1.22, Cm 0.05, Cn 0.01, Cflow 0.389
drag/downforce/pitch: 226.8 N / 439.2 N / 54.0 N*m
centre of pressure x: 0.12295081967213115 m
mass flow: 0.74688 kg/s
cooling conductance: 525.43008 W/K
heat rejection: 31525.804799999998 W
all eight residuals: 0
drag 40/20 ratio: 4.0
mass-flow 40/20 ratio: 2.0
cooling-open drag: 270.0 N; flow: 1.51488 kg/s
replay_equal: true
41 m/s query: invalid, outside declared airspeed envelope
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each. Full validation is rerun after this result; staged
scope/check runs before commit.

## Limitations and follow-up

- Linear quasi-steady coefficient interpolation is sparse-map dependent and
  omits separation hysteresis, gusts, transient devices, compressibility, and
  fluid-structure interaction.
- Cooling omits duct pressure loss, heat-exchanger UA, fan/pump curves and
  energy, recirculation, and thermal mass.
- Outputs are not yet coupled into Work 015 race motion, Work 016 load transfer,
  or Work 014 thermal state.
- Work 018 will own suspension, mechanical braking, and regenerative braking;
  it was not started here.
- Commit hash is reported in final handoff; no remote push is performed.
