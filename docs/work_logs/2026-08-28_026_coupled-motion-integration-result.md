# Work 026 Result: Coupled Motion Integration

Status: Completed

Thai companion: `2026-08-28_026_coupled-motion-integration-result.th.md`

## Outcome

Implemented a deterministic Level-0 planar motion adapter that sums aerodynamic/contact wrenches, advances horizontal velocity, yaw, position, time, and corridor-tangent race distance, and fails closed on residual or corridor errors.

## Files Changed

- Added versioned architecture v2 with the corridor-to-motion dependency.
- Added `motion_coupling.py`, public exports, 12 unit tests, and a standalone validator.
- Added bilingual model documentation, two bilingual problem reports, plan/result records, and queue status updates.

## Decisions

- Preserve architecture v1 and add v2 instead of rewriting historical evidence.
- Use midpoint force orientation, trapezoidal position, and exact constant yaw-acceleration integration.
- Credit only positive corridor-tangent displacement as race distance; retain reverse displacement as uncredited evidence.
- Reject corridor departure rather than projecting the vehicle back inside.
- Keep vertical motion constant-velocity and observable; do not silently impose grade constraints without a vertical force/constraint model.

## Problems Resolved

1. `2026-08-28_026_motion-missing-corridor-signal.md`: architecture v1 could not route typed corridor evidence to motion; resolved in v2.
2. `2026-08-28_026_motion-vertical-projection.md`: the first draft could erase vertical offset and later exposed inconsistent `z`/`v_z`; resolved with constant-velocity vertical kinematics and a `motion.kinematic-z` residual.

## Validation Commands and Evidence

All commands below returned exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_motion_coupling
python -m unittest discover -s tests
python scripts/validate_motion_coupling.py
python -m compileall -q src scripts tests
git diff --check
```

Evidence:

- focused tests: 12 passed in `0.005 s`;
- full suite: 219 passed in final rerun `0.373 s`;
- validator: exit `0`;
- bytecode compilation: exit `0`;
- unstaged diff check: exit `0`;
- architecture fingerprint: `a989fa92bc9eb1bcf83127b572cb2c33b99a802458211dbe4442fa9046c0f5fe`;
- straight fixture: `(12, 0, 0) m/s`, `(11, 0, 0) m`, `11 m` race distance, nine residuals passed;
- refinement: error `0.08383245221108916 m` at `dt = 1.0 s`, `0.00019773501705859235 m` at `dt = 0.05 s`, reduction ratio `423.96361280940005`;
- lateral-only credited progress `0 m`; reverse raw/credited/uncredited `-2/0/2 m`;
- corridor departure and missing spatial evidence: `invalid`, zero outputs;
- deterministic replay: `true`.

## Limitations

- Level-0 analytical verification only; no calibrated or physical validation.
- Local body-width corridor gate does not sweep yawed vehicle corners, length, overhang, barriers, or kerbs.
- No real ten-circuit profile has surveyed local 3D corridor evidence available for admission.
- Grade and bank do not yet generate constraint forces; vertical dynamics remain outside Work 026.
- Energy, thermal, damage, degradation, reliability, and final state arbitration remain for Work 027 onward.

## Follow-up

Work 027 should merge contact energy transfers, aerodynamic cooling, component thermal/degradation/damage state, and deterministic reliability/event evidence before the transaction publishes a final next state.
