# Bounded Whole-Vehicle Search Pilot and Readiness Review

Thai companion: `BOUNDED_WHOLE_VEHICLE_SEARCH_PILOT_READINESS.th.md`

## Decision

```text
not_ready
blocker: independent_refined_evaluation
```

The search apparatus passed equal-budget, replay, provenance, candidate-schema, exploit, and frozen-holdout mechanics. It is not ready for a bounded main campaign because no independent whole-vehicle stress/deformation evaluator exists. No candidate is declared a winner.

## Preregistered pilot

- treatments: `GRID`, `RANDOM`, `EVOLUTION`
- seeds: `101`, `202`, `303`
- attempted evaluations per treatment/seed: `32`
- attempts per treatment: `96`
- total attempted evaluations: `288`
- every grammar, structural, energy, or numerical failure consumes one attempt

All treatments used the same evaluator, Work 048 training/holdout cases, bounds, component library, and tolerances. Candidate code could change only five Work 047 grammar variables: core length, core width, ground-contact radius, source primitive size, and propulsor primitive size. Material density remained fixed because no admitted density-strength relation exists.

Candidate geometry was rebuilt and grammar-validated for every attempt. Analytical mass came from primitive volumes and fixed material densities. The bounded structural-capacity proxy depended on the relevant cross-section/radius/primitive scales. This creates a causal geometry path at Level 0, but it is not a stress solver.

## Treatment results

| Treatment | Attempts | Feasible | Feasible rate | Structural failures | Best training time |
|---|---:|---:|---:|---:|---:|
| `GRID` | 96 | 50 | `0.5208333333333334` | 46 | `34.1204253544251 s` |
| `RANDOM` | 96 | 71 | `0.7395833333333334` | 25 | `35.42349737959053 s` |
| `EVOLUTION` | 96 | 86 | `0.8958333333333334` | 10 | `34.16703235066346 s` |

These are descriptive pilot results, not evidence that one treatment or candidate is superior. The five-variable bounds and analytical proxy can explain the differences. `GRID` has the lowest provisional training objective; it is not a winner because refinement is unavailable.

## Promotion and readiness

One best training-feasible candidate per treatment/seed was promoted: nine candidates total. All nine remained feasible on the frozen Work 048 holdout cases. All nine received `refined_status=unavailable`; none was silently assigned a passing value. Therefore the promotion chain selected no winner.

Readiness checks:

| Check | Result |
|---|---:|
| exact replay | pass |
| equal budget | pass |
| same evaluator | pass |
| frozen holdout pass | pass |
| no exploit | pass |
| complete provenance | pass |
| independent refined evaluation | **fail** |

## Replay and ledger evidence

- record-set SHA-256: `b35beb7d8b08040c56ab26ec0633f4eb48d9f18ef3219b592cf5c2ffa62ed3bc`
- result/replay JSONL SHA-256: `15d20e607ddc0e60d6f70e5dc027be680f392a1c55c1a744edf0f1fdd0cbb7bb`
- budget-ledger SHA-256: `1c27bbe2a5917dd1334a140be3e1550d6028b3391af438bbdd6aa87bceb79224`
- ledger content equality: exact
- exploit controls rejected: `5`

Each record includes treatment, seed, attempt index, geometry variables, parent identity, RNG checkpoint, status/failure code, evaluator identity, and result hash. Evolution attempts after the initial random phase preserve parent ancestry. Result and budget ledgers are written sequentially; failed candidates remain visible and counted.

## Falsification and limitations

Before the admitted run, mutable material-density variables were removed because lower density without strength evidence would create an unphysical optimization exploit. They were replaced with source/propulsor geometry scales while material properties remained fixed.

The pilot cannot establish engineering merit. Missing evidence includes an independent whole-vehicle stress/deformation solver, mesh/refinement convergence, arbitrary topology, calibrated material strength, contact/preload/friction, transient loads, aerodynamics beyond the frozen proxy, thermal reliability, real-circuit admission, manufacturing, and physical tests.

The next work must implement and validate the independent refined evaluator. It must not merely rename the existing capacity-factor proxy. After that evidence exists, Work 050 should be rerun as a new remedial work item with the original ledgers retained.

## Reproduction

```powershell
.\scripts\run_work050.ps1
py -3.14 -m unittest tests.test_whole_vehicle_search -v
```
