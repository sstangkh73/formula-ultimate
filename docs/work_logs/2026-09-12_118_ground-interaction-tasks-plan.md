# Work 118 Plan: Ground Interaction, Stopping and Direction Control

Thai companion: `2026-09-12_118_ground-interaction-tasks-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement architecture-neutral ground-contact ports and a bounded rigid-route friction reference pinned to Work 114 motion/contact evidence and Work 116 material-applicability evidence. Evaluate propulsion reaction, stopping and yaw-direction response without assuming wheels, steering linkages or a contact-count rule.

Use explicit SI sign conventions, a registered synthetic rigid/dry surface record, Coulomb force-circle saturation, lift-off/disconnection rules, stopping energy accounting and time-step refinement. Return maximum contact loads and moments to local part-model evidence while preserving unsupported tire, soft-soil and non-tire domains as unresolved.

## Variables, controls and files

- IV: contact placement, normal load, friction coefficient, commanded longitudinal/lateral force, initial velocity, yaw command and time step.
- DV: admitted contact force, yaw moment/response, stopping time/distance, dissipated energy, energy residual, saturation state and returned local loads.
- Controls: same external route/surface/initial energy; zero friction, lift-off, reverse motion, saturation, disconnected actuation and no physical interaction.
- Success: reference forces obey the force circle and signs; analytic stopping and energy references converge; placement changes yaw moment; forbidden interactions generate no ground force; exact replay passes.

Planned files: `src/formula_ultimate/simulation/ground_interaction_tasks.py`, `config/development/ground_interaction_tasks_v1.json`, `scripts/development/run_ground_interaction_tasks.py`, `tests/test_ground_interaction_tasks.py`, bilingual `docs/contracts/GROUND_INTERACTION_TASKS_V1*`, this bilingual plan/result and ignored `artifacts/work118/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_ground_interaction_tasks tests.test_repository_contract -v
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_a
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_b --replay-reference artifacts/work118/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 114/116 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

The dry rigid Coulomb law is a bounded causal reference, not a tire, compliant-terrain or arbitrary-locomotion model. Non-goals: prescribing contact type/count, validated traction, soft soil, hydroplaning, wear/thermal evolution, complete vehicle control, physical validation, push or history rewrite.
