# Work 053 Result: Section-Force Refined Whole-Vehicle Evaluator

Status: Completed

Thai companion: `2026-08-30_053_section-force-refined-evaluator-result.th.md`

## Outcome

The corrected evaluator is available within the declared linear-elastic beam-network domain. The finest analytical benchmark maximum error was `3.4276%`; 54 candidate states produced 162 isolated-section CalculiX processes; all seven negative controls behaved as expected; deterministic project replay was exact. Seven of nine proxy-promoted candidates passed both holdouts. The other two remain rejected by the unchanged `8%` project/CalculiX stress-difference gate.

Decision: `independent_refined_evaluator_available`. Candidate-set decision: `partially_supported` (`7/9`).

## Files changed

- `config/structural/section_force_vehicle_frame_refinement_v2.json`
- `src/formula_ultimate/structural/vehicle_frame_refinement.py` and structural package exports
- `src/formula_ultimate/experiments/whole_vehicle_search.py` and experiment package exports for the public deterministic geometry mutation adapter
- `scripts/structural/run_vehicle_frame_refinement.py` and `scripts/run_work053.ps1`
- `tests/test_vehicle_frame_refinement.py`
- `docs/physics/WHOLE_VEHICLE_SECTION_FORCE_REFINED_EVALUATOR.md` and `.th.md`
- matching Work 053 bilingual plan/result records
- trailing-blank-line repair in the stopped Work 052 English result

Ignored raw evidence is under `artifacts/work053/`.

## Decisions and evidence

- CalculiX `SECTION FORCES` output is converted to rectangular-section surface stress from `N`, `V1`, `V2`, `T`, `M1`, and `M2`; integration-point material stress is retained as evidence but is not compared to analytical root surface stress.
- The preregistered refinements remained `4/8/16`; the `5%` analytical/refinement and `8%` cross-model thresholds were not relaxed.
- Fine analytical errors were `0.08648%` CalculiX displacement, `3.4276%` CalculiX stress, approximately zero project displacement, and `0.00375%` project stress.
- Maximum candidate reaction residual was `2.2293e-11` relative.
- For seven admitted candidates, maximum last-two change was `2.0489%`, maximum fine cross-model difference was `5.0207%`, minimum yield margin was `379.45`, and maximum displacement was `6.1326e-6 m`.
- `candidate-9b03158dc541df18` failed with fine stress differences `16.69%/17.66%`; `candidate-372db49a7cbceba5` failed with `32.24%/33.51%`. Their large yield margins did not override contradictory solver evidence.
- Config SHA-256 was `a21cd3ad14f2b1c4e2e1b378101c2b1322fd17d41ba79ce2af20d85cfff26ed4`; deterministic project replay fingerprint was `e5b28abfa37224b8bc855d28f43626744401b79c03d084f1b6fb1953fe37020d`; CalculiX executable SHA-256 was `2ff89a72b6aac9c361cb716e44220dfcd01d2bb3e66abd6b6455b01b7250f350`.

## Observed non-admitted failures

The first Work 053 runner invocation completed the physics stages but exited `1` at final reporting because the renamed summary field `structural_states` was still printed as `holdout_solves`. This key-only defect was fixed and the entire experiment rerun. The next complete run exposed a decision-schema defect: evaluator availability was incorrectly coupled to all nine candidates passing, even though the plan required every candidate to pass or fail explicitly. The schema was separated into evaluator decision and candidate-set decision without changing any threshold or candidate metric, and the entire experiment was rerun again.

The predecessor Work 052 evidence commit `37359db` was created after `git diff --cached --check` had reported one blank line at EOF because the shell sequence did not fail fast. Work 053 preserves that history, repairs the file, and uses separate fail-fast validation for this commit.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_vehicle_frame_refinement -q
# exit 0; Ran 5 tests; OK

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work053.ps1
# exit 0; status=passed
# decision=independent_refined_evaluator_available
# candidate_set_decision=partially_supported; passed_candidates=7/9
# structural_states=54; candidate_calculix_processes=162
# fine_benchmark_max_error=0.03427617134482464
# negative_controls=7; replay=exact

py -3.14 -m unittest tests.test_vehicle_frame_refinement tests.test_whole_vehicle_search tests.test_repository_contract -q
# exit 0; Ran 15 tests; OK

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 339 tests in 32.391s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

Repository-contract checks, staged `git diff --cached --check`, the explicit scoped commit, and clean-tree Work 053 replay are verified after this result exists and are reported in the final handoff.

## Limitations and follow-up

This work closes only evaluator availability. It does not validate solid/contact stress concentrations, nonlinear material response, real joints, local buckling, fatigue life, vibration, crash, certified material allowables, manufacturing variation, or hardware. A successor readiness work item must consume only the seven supported candidates, preserve treatment fairness and all Work 050 evidence identities, and must not rewrite the two rejected results.
