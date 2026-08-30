# Bounded Whole-Vehicle Campaign Readiness

Thai companion: `BOUNDED_WHOLE_VEHICLE_CAMPAIGN_READINESS.th.md`

## Decision

Work 054 decision: `ready_for_bounded_whole_vehicle_campaign`.

This means the bounded research process may proceed from pilot to a preregistered whole-vehicle campaign using the Work 047 grammar, Work 048 loads, Work 049 fixed baselines, Work 050 equal-budget search mechanics, and Work 053 refined structural gate. It does not mean a vehicle is physically validated, safe, manufacturable, race-ready, or superior to real designs.

## Evidence chain

```text
Work 047 complete derivable assembly grammar
  -> Work 048 force/moment transfer and overload DNF
  -> Work 049 fixed reference/heavy baseline controls
  -> Work 050 equal 96/96/96 GRID/RANDOM/EVOLUTION pilot
  -> Work 053 independent frame + CalculiX section-force gate
  -> Work 054 deterministic readiness adjudication
```

All Work 050 readiness checks already passed except `independent_refined_evaluation`. Work 053 made that evaluator available and evaluated all nine frozen promotions. Work 054 joined those records without changing objectives, thresholds, candidate identities, treatment budgets, or rejected outcomes.

## Refined-supported set

| Treatment | Original promotions | Supported | Treatment winner | Holdout objective (s) |
|---|---:|---:|---|---:|
| GRID | 3 | 2 | `candidate-12b30a0606bccf88` | `34.1204253544251` |
| RANDOM | 3 | 3 | `candidate-58b6c6238b708e6a` | `35.42349737959053` |
| EVOLUTION | 3 | 2 | `candidate-333486cb11b2f603` | `34.16703235066346` |

Global pilot winner: `candidate-12b30a0606bccf88`. It is refined-supported. The deterministic adjudication SHA-256 is `c8a5e89fba6d96be5a5cfa063a51a1d2b0eb597c25f24784dbe85a4c062da953`.

Two candidates remain rejected and are not eligible for the bounded campaign:

- GRID `candidate-9b03158dc541df18`
- EVOLUTION `candidate-372db49a7cbceba5`

Their contradictory cross-model stress evidence is preserved; no objective or yield-margin argument overrides it.

## What is now allowed

- Preregister and run a larger, equal-compute whole-vehicle campaign inside the exact bounded grammar/evaluator/load domain.
- Apply the Work 053 refined gate to every promoted candidate before comparing treatment outcomes.
- Compare fixed-topology and free-topology treatments only when component library, constraints, seeds, compute accounting, and evidence gates are equal.
- Report failures, numerical invalidity, conservation residuals, and DNF as outcomes rather than silently repairing them.

## What remains prohibited

- Claiming physical validation, real-world safety, race superiority, or engineering discovery from Level 0/beam-network evidence.
- Admitting the two rejected candidates or substituting proxy capacity for refined evaluation.
- Expanding to arbitrary topology or different loads/materials without a new protocol and transfer evidence.
- Treating synthetic material yield margin as a certified allowable.

Before any hardware claim, the project still needs higher-fidelity solid/contact/nonlinear analysis, buckling and fatigue coupling at vehicle interfaces, physical material records, calibration specimens, manufacturing tolerances, and hardware tests.
