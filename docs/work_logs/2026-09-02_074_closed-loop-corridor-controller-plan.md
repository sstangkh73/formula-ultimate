# Work 074 Plan: Closed-Loop Corridor Controller

Status: Completed

Thai companion: `2026-09-02_074_closed-loop-corridor-controller-plan.th.md`

## Objective and scope

Add a deterministic feedback controller that converts the current Work 073 planar state and a declared `CircuitCorridor` centreline into a bounded steering command. Run the controller step-by-step through the unchanged Work 073 vertical/tyre/drivetrain plant so that tracking error affects tyre forces, body modes, energy, and terminal state rather than merely drawing a path.

Work 074 is a short-horizon synthetic Level-0 control specimen. It does not claim autonomous racing, optimal control, or real-circuit admission.

## Experiment design

- Independent variables: corridor curvature sign, controller feed-forward/heading/cross-track gains, steering limit, station spacing, and initial lateral/heading disturbance.
- Dependent variables: commanded steer, feed-forward and feedback terms, signed cross-track/heading error, progress, actual normal loads, body modes, energy residual, saturation count, and terminal outcome.
- Controls: exact replay, straight corridor, left/right mirror, zero-feedback control, wrong-sign gain, steering saturation, corridor departure, and half-step refinement.
- Preferred hypothesis: correct-sign feedback reduces disturbed cross-track error relative to feed-forward-only control, mirrors under curvature/disturbance sign reversal, and remains coupled to Work 073 without changing its fixed-steer hash.
- Falsification: wrong correction sign, noncausal look-ahead, silent steering clipping, centreline identity mismatch, target-load bypass, unexplained energy, mirror/replay failure, or a disturbed controller no better than its zero-feedback control.

## Planned files

- `config/vehicle/closed_loop_corridor_controller_v1.json`
- `src/formula_ultimate/simulation/closed_loop_corridor_controller.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_closed_loop_corridor_controller.py`
- `tests/test_closed_loop_corridor_controller.py`
- bilingual research and Work 074 result records
- trilogy plans for Work 075 and Work 076, requested together with Work 074
- ignored evidence under `artifacts/work074/`

## Validation and success criteria

The loader must reject invalid gains, limits, spacing, non-closed/identity-mismatched fixtures where prohibited, and non-finite states. Reference execution must preserve positive tyre loads and bounded travel; every command must remain within the explicit steering limit. Correct feedback must reduce final absolute cross-track error versus the preregistered zero-feedback control. Straight and mirror controls, exact replay, fixed-steer Work 073 hash preservation, equation/energy residuals, half-step refinement `<= 2%`, focused/full tests, bilingual contract, scoped commit, and post-commit replay must pass.

## Risks and explicit non-goals

Nearest-centreline projection on a deterministic sampled polyline is an approximation whose spacing error remains observable. The controller has no speed optimization, braking, obstacle avoidance, traffic response, state estimator, actuator latency, noise, or learning. Synthetic corridor evidence cannot admit a real circuit.
