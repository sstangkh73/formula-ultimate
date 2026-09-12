# Work 126 Result: Detailed Vehicle Closure

Thai companion: `2026-09-12_126_detailed-vehicle-closure-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 126 created a deterministic G3 registry with 12 uniquely owned component regions covering all registered external functions and required hardware roles. Recomputed mass is `60.0 kg`, center is `[0.0, 0.0, 0.5] m`, diagonal inertia is `[0.9, 179.65, 179.65] kg m^2`, and occupied volume is `0.324 m^3`; all declared residuals are within `1e-9`. Energy, signal, heat and load graphs connect, the static assembly has no box interference, and five registered swept-motion samples have no collision.

Controls rejected removed fastener/support/seal/signal hardware, duplicate region ownership, out-of-envelope geometry, interference, open signal path and stale envelopes. The generated registry, exploded-view registry and section-view registry have pinned hashes. Result SHA-256 is `ce5f08c8a572b1ef5adbf88db7e7200616c8c1c9c431ba6d032236d8917e3171`; exact replay passed. Essential evidence remains unresolved, so status is `detailed_exploratory` and promotion is false.

Changed: implementation, configuration, runner, tests, bilingual `DETAILED_VEHICLE_CLOSURE_V1` contract, and this bilingual plan/result. Ignored evidence is under `artifacts/work126/run_a|run_b`.

## Bug report

- Symptom: the first unit test stalled while checking a connected path.
- Root cause: an obsolete pre-BFS loop placed `queue.popleft()` only inside the unselected branch of a conditional expression, so the queue never advanced for list adjacency data.
- Fix: removed the obsolete loop and retained one explicit, direction-independent BFS that always dequeues and enqueues unseen neighbors.
- Retest: all 6 Work 126 tests passed, both evidence runs completed with identical SHA-256, and all 63 affected regression tests passed.

## Validation and limitations

```powershell
python -m unittest tests.test_detailed_vehicle_closure -v
# first run stalled; after fix exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/assembly/detailed_vehicle_closure.py scripts/development/run_detailed_vehicle_closure.py tests/test_detailed_vehicle_closure.py
# exit 0
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_a
# exit 0; detailed_exploratory; result SHA-256 above
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_b --replay-reference artifacts/work126/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_ground_interaction_tasks tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_coupled_vehicle_transient tests.test_multiscale_discovery_search tests.test_detailed_part_comparison tests.test_detailed_vehicle_closure tests.test_repository_contract -v
# exit 0; 63 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 126 files
git diff --cached --check
# exit 0
```

The G3 registry uses axis-aligned box bounds and graph connectivity. It is not native whole/individual CAD and cannot establish detailed surfaces, tolerance-stack manufacturability, measured material survival, real collision behavior or physical validation. Work 127 may use its exact identity for fair optimized controls but must preserve the non-promotion boundary.
