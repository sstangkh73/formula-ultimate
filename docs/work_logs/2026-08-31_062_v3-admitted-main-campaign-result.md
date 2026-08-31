# Work 062 Result: Protocol v3 Admitted Main Campaign

Status: Completed

Thai companion: `2026-08-31_062_v3-admitted-main-campaign-result.th.md`

## Outcome

Executed admitted campaign `FU-BMC-003` from clean commit `bfa33a29bc92890628df0429351cef3e6eed017e`. The run completed `2,880/2,880` terminal attempts with no pending reservations, 72 promotions, 72 terminal holdouts, 72 terminal refinements, and 72 terminal CAD records. Refinement and STEP/FreeCAD witness passed for 51 candidates. Final decision: `completed_with_supported_finishers`; clean-tree verify-only replay was exact.

EVOLUTION produced supported finishers on 11/12 seeds versus RANDOM 9/12 and GRID 10/12. The primary EVOLUTION-minus-RANDOM rate difference was `+0.1667`, but exact McNemar `p = 0.5`; therefore this work does not claim algorithm superiority. Full interpretation and limitations are in `docs/research/BOUNDED_MAIN_CAMPAIGN_V3_RESULT.md`.

## Files changed

- Updated this work's English and Thai plan status to `Completed`.
- Added `docs/research/BOUNDED_MAIN_CAMPAIGN_V3_RESULT.md` and `.th.md`.
- Added this English result and `2026-08-31_062_v3-admitted-main-campaign-result.th.md`.
- Generated ignored immutable evidence under `artifacts/work062/`; no admitted code or protocol file changed.

## Exact commands and validation

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work062.ps1` → exit `0`; `2,880` attempts, `72` promotions, `51` refinement passes, `51` CAD passes, decision `completed_with_supported_finishers`.
- `py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind main --protocol config/experiments/bounded_whole_vehicle_main_campaign_v3.json --artifact-root artifacts/work062 --admission artifacts/work061/campaign_summary.json --verify-only` → exit `0`; replay `exact`, supported streams `30`.
- `py -3.14 -m unittest discover -s tests -q` → exit `0`; `Ran 372 tests in 32.872s`, `OK`.
- `py -3.14 -m compileall -q src scripts tests` → exit `0`.

## Evidence identities

- Protocol fingerprint: `9ef748f2719923632a05ef5fcbba95b8f2fa1b4156d2dbbf6cb9b4fbd02d4c36`.
- Training fingerprint: `503917192f3029c66e27cec2a2ef1f7521ebfba9c2872e3541945bf35a281176`.
- Stage fingerprint: `9e2554f865788b98c21cff736063d46857eff888e022299256222fad186e1182`.
- Analysis fingerprint: `f6a86288b3653b75d1d5c56f62b948344884911d946b91ef8ddbfc6e46dbef19`.
- Training feasible/structural failure: `2,107/773`; GRID unique: `960`.
- Holdout feasible: `72/72`; refinement passed/refined disagreement: `51/21`; CAD passed/not run: `51/21`.

## Decisions, limitations, and follow-up

Consumed failures were retained, holdout information did not enter selection, and all preregistered outcomes were reported. The primary exact test is non-significant, the evaluator remains bounded, and 21 Level-0-feasible candidates failed refined agreement. No physical validation, safety, manufacturability, arbitrary-topology, or algorithm-superiority claim is made.

Next work should preregister an independent replication and separately raise structural fidelity toward solid/contact/nonlinear behavior, calibrated material data, fatigue and failure propagation, and hardware correlation. The result commit and post-commit clean-tree replay are reported in the final handoff.
