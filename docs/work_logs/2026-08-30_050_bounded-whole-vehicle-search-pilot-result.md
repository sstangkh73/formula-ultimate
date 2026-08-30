# Work 050 Result: Bounded Whole-Vehicle Search Pilot and Readiness Review

Status: Completed

Thai companion: `2026-08-30_050_bounded-whole-vehicle-search-pilot-result.th.md`

## Outcome

Completed the preregistered `288`-attempt equal-budget pilot. Search mechanics, exact replay, frozen holdouts, ancestry, budget accounting, provenance, and exploit rejection passed. The readiness decision is `not_ready` because `independent_refined_evaluation` is unavailable. No candidate is a winner and no main campaign is authorized.

## Files changed

- `config/experiments/bounded_whole_vehicle_search_pilot_v1.json`
- `src/formula_ultimate/experiments/whole_vehicle_search.py` and experiment exports
- `scripts/experiments/run_whole_vehicle_search_pilot.py`
- `scripts/run_work050.ps1`
- `tests/test_whole_vehicle_search.py`
- `docs/reports/BOUNDED_WHOLE_VEHICLE_SEARCH_PILOT_READINESS.md` and `.th.md`
- matching Work 050 bilingual plan/result records

Ignored ledgers/evidence are under `artifacts/work050/`.

## Decisions and evidence

- `GRID`, `RANDOM`, and `EVOLUTION` each consumed `96` attempts; total `288`.
- Feasible counts were `50`, `71`, and `86`; structural failures were `46`, `25`, and `10`.
- Best provisional training times were `34.1204253544251/35.42349737959053/34.16703235066346 s`.
- Nine selected candidates passed frozen holdouts; zero received refined-evaluator evidence.
- Complete same-seed replay was exact: result/replay ledger SHA-256 `15d20e607ddc0e60d6f70e5dc027be680f392a1c55c1a744edf0f1fdd0cbb7bb`.
- Budget ledger SHA-256 was `1c27bbe2a5917dd1334a140be3e1550d6028b3391af438bbdd6aa87bceb79224`; failures were counted.
- Five exploit controls failed closed.
- Mutable density variables were removed before the admitted run because density without coupled strength evidence was an exploit; fixed materials and geometry scales replaced them.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_whole_vehicle_search -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work050.ps1
# exit 0; status=passed; attempts=288
# budgets GRID=96 RANDOM=96 EVOLUTION=96
# promotions=9; holdout_passed=9; refined_passed=0
# replay=exact; decision=not_ready
# blockers=[independent_refined_evaluation]; exploit_controls=5

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 334 tests in 35.459s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Staged checks, explicit commit, and clean-tree replay are performed after this record exists and reported in the final handoff.

## Limitations and follow-up

This is a bounded search-mechanics pilot with a five-variable primitive grammar and analytical structural proxy. It does not authorize a main campaign or support superiority, discovery, physical validity, safety, real-circuit, aero, thermal, or manufacturing claims. The next required remedial work is an independent refined whole-vehicle stress/deformation evaluator followed by a preserved-gate pilot rerun.
