# Work 049 Result: Fixed-Topology End-to-End Whole-Vehicle Baseline

Status: Completed

Thai companion: `2026-08-30_049_fixed-topology-end-to-end-baseline-result.th.md`

## Outcome

The reviewed fixed baseline completed the current bounded CAD-to-Level-0 chain. The reference and heavy control finished; the weak and disconnected controls produced explicit `DNF`. Timestep and declared-capacity sensitivity passed their frozen gates, and same-input replay was exact. This validates orchestration, not whole-vehicle stress or physical feasibility.

## Files changed

- `config/vehicle/fixed_topology_end_to_end_baseline_v1.json`
- `src/formula_ultimate/experiments/whole_vehicle_baseline.py` and experiment exports
- `scripts/experiments/run_whole_vehicle_baseline.py`
- `scripts/run_work049.ps1`
- `tests/test_whole_vehicle_baseline.py`
- `docs/reports/FIXED_TOPOLOGY_END_TO_END_BASELINE.md` and `.th.md`
- matching Work 049 bilingual plan/result records

Ignored evidence is under `artifacts/work049/`.

## Decisions and evidence

- Reference: `finished`, `40.0 s`, `108000 J`, maximum utilization `0.715678478993928`.
- Heavy control: `finished`, `43.81780460041329 s`, `128763.56092008266 J`, maximum utilization `0.8588141747927136`.
- Weak control: `DNF` by structural failure. Disconnected control: `DNF` by explicit load-path loss.
- Finish-time relative change was `0`; declared-capacity sensitivity was `0.007035175879396918`, below `0.01`.
- Reference/matrix replay SHA-256 values were `12774be503f21212cd35cc10b48f1eb60ab5740005ab264dfa17b35f87eb1097` and `237b2454eb0d4d83c750177ce96964d3fdadbcf52e456687f47e2c43f28fb71c`.
- Four malformed/unregistered controls failed closed.
- The first incomplete-case control removed the overload control instead of a nominal case. The runner correctly rejected the test premise; the fixture was corrected to remove a named training case without changing evaluator logic or thresholds.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_whole_vehicle_baseline -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work049.ps1
# exit 0; reference=finished; weak=DNF; disconnected=DNF; heavy=finished
# reference_time_s=40.0; heavy_time_s=43.81780460041329
# timestep_relative=0; structural_relative=0.007035175879396918
# replay=exact; negative_controls=4

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 330 tests in 33.589s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Staged checks, explicit commit, and clean-tree replay are performed after this record exists and reported in the final handoff.

## Limitations and follow-up

This baseline uses a synthetic `1000 m` Level 0 fixture and analytical capacity sensitivity. It has no whole-vehicle stress FEA, independent refined evaluator, transient/contact/aero fidelity, physical calibration, real circuit, safety, or manufacturing evidence. Work 050 may test proposal/evaluation fairness but must return `not_ready` if these blockers remain.
