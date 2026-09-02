# Work 076 Plan: Integrated Level-0 Closed-Loop Lap Gate

Status: Completed

Thai companion: `2026-09-02_076_integrated-level0-lap-gate-plan.th.md`

## Objective and scope

Combine the Work 074 controller, Work 075 linkage transform, Work 073 vertical tyre/road dynamics, and the existing drivetrain/planar plant into one deterministic synthetic-lap experiment. The gate must require centreline progress, corridor containment, positive contact, bounded suspension travel, energy closure, and an exact finish event.

This is a one-lap synthetic Level-0 integration gate. It is not a real-circuit lap, lap-time optimization, safety validation, or proof of a complete physical car.

## Experiment design

- Independent variables: controller gains, linkage geometry selection, corridor curvature/direction/width, time step, energy/throttle, and injected steering/contact faults.
- Dependent variables: finish time/progress, maximum/final tracking error, steering saturation, tyre loads, travel/body modes, energy/residual maxima, terminal reason, and deterministic hashes.
- Controls: exact replay, opposite-direction mirror lap, open-loop departure, narrow-corridor departure, contact-loss road input, linkage-degeneracy rejection, energy depletion/timeout boundary where reachable, and half-step refinement on a shortened matched segment.
- Preferred hypothesis: the selected candidate completes exactly one analytical closed loop while staying inside the declared corridor and physical gates; controls fail for their declared causal reason.
- Falsification: progress credited without spatial motion, closure by distance alone, off-corridor finish, contact/travel clipping, hidden controller saturation, energy creation, identity drift, wrong first failure, or replay mismatch.

## Planned files

- `config/vehicle/integrated_level0_lap_gate_v1.json`
- `src/formula_ultimate/simulation/integrated_lap_gate.py`
- simulation exports, runner, tests, bilingual research/result records
- ignored evidence under `artifacts/work076/`

## Validation and success criteria

The reference must reach one corridor length with an exact localized finish distance, remain within width after vehicle-envelope allowance, retain positive normal loads and travel below limits, and pass all equation/energy tolerances. Mirror and replay identities, causal DNF controls, Work 074/075 upstream hashes, focused/full tests, compilation, bilingual contract, one scoped commit, and post-commit replay must pass. Any numerical or physical failure blocks a finish claim.

## Risks and explicit non-goals

The analytical circle and synthetic road are not real track data. The model omits braking zones, variable speed, aerodynamic load, thermal limits over race duration, detailed tyre relaxation/contact, driver/traffic, barriers, weather, structural load coupling, and real linkage CAD. A passed gate authorizes only the next fidelity step.
