# Work 049 Plan: Fixed-Topology End-to-End Whole-Vehicle Baseline

Status: Completed

Thai companion: `2026-08-30_049_fixed-topology-end-to-end-baseline-plan.th.md`

## Objective

Run one immutable reviewed Work 047 vehicle through the complete currently admitted evidence chain before any search: deterministic CAD, STEP, independent FreeCAD properties, frozen Work 048 training/holdout loads, bounded structural/failure outcomes, and a coupled Level 0 race decision. Falsify the chain with weak, disconnected, heavy-feasible, timestep, and structural-resolution controls.

## Scope and planned files

- Add a fixed-baseline manifest under `config/vehicle/` that pins all upstream identities, Level 0 energy/time inputs, structural capacity scales, timestep levels, and refinement levels.
- Add an end-to-end baseline evaluator under `src/formula_ultimate/experiments/` and a runner under `scripts/experiments/`.
- Add `scripts/run_work049.ps1`, focused tests, a bilingual baseline report, and matching bilingual result records.
- Write ignored evidence under `artifacts/work049/`.

## Experiment definition

- Independent variables: immutable baseline variant, training/holdout partition, capacity scale, declared mass scale, structural resolution label, Level 0 timestep, and frozen energy/race inputs.
- Dependent variables: CAD/STEP/FreeCAD identities, load-case result hashes, maximum structural utilization, failure event/outcome, Level 0 energy/time state, finish or `DNF`, convergence metrics, and compute/process evidence.
- Controls: no geometry mutation for the reference baseline, fixed adapter/settings/seeds/component library, exact Work 048 partition hashes, one evaluator API, SI units, and explicit unsupported-evidence states.
- Falsification controls: deliberately weak capacity, disconnected load path, heavy but feasible mass, missing evidence, repeated same-input run, and paired timestep/structural-resolution levels.

## Validation

1. Unit-test identity pinning, reference finish, weak/disconnected `DNF`, heavy-feasible finish, and exact replay.
2. Invoke Work 048 as the CAD/FreeCAD/load/failure upstream stage and require its clean result identities.
3. Require complete results for every frozen training and holdout case.
4. Require timestep and bounded structural-resolution changes to satisfy preregistered relative gates.
5. Count deliberate failures as results; never repair or discard them.
6. Run repository-contract, full unit, compile, staged-diff, and clean-tree replay gates.

## Success criteria

- The reference fixed topology finishes the declared bounded Level 0 fixture and is structurally feasible for all training cases.
- Weak and disconnected controls produce explicit `DNF`; the heavy control remains feasible but is slower and consumes more energy.
- Repeated evaluation preserves exact hashes and all outputs identify their upstream commit/config/STEP/partition evidence.
- Unsupported evidence returns an invalid result with no candidate fitness.

## Risks

The race state is a bounded deterministic Level 0 fixture, not a real circuit. Structural resolution is an analytical capacity perturbation audit, not mesh-converged whole-vehicle FEA. A successful baseline can validate orchestration while still leaving the scientific apparatus not ready for a main campaign.

## Explicit non-goals

No autonomous mutation, optimization, novelty claim, physical vehicle validation, real-circuit admission, safety certification, CFD, whole-vehicle stress FEA, manufacturing proof, push, or publication is included.
