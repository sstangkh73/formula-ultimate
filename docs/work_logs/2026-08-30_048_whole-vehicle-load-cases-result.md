# Work 048 Result: Whole-Vehicle Load Cases and Structural Coupling

Status: Completed

Thai companion: `2026-08-30_048_whole-vehicle-load-cases-result.th.md`

## Outcome

Implemented and validated a bounded quasi-static tree-wrench adapter for the exact Work 047 assembly. Seven frozen training/holdout cases balanced and remained running; one deliberate overload crossed the critical support capacity and coupled to Work 046 as `DNF`. This closes the Work 048 algebraic load-traceability gate, not the missing whole-vehicle stress-FEA evidence.

## Files changed

- `config/vehicle/whole_vehicle_load_cases_v1.json`
- `src/formula_ultimate/simulation/vehicle_load_cases.py` and simulation exports
- `scripts/simulation/run_vehicle_load_cases.py`
- `scripts/run_work048.ps1`
- `tests/test_vehicle_load_cases.py`
- `docs/physics/WHOLE_VEHICLE_LOAD_CASES.md` and `.th.md`
- matching Work 048 bilingual plan/result records

Ignored evidence is under `artifacts/work048/`.

## Decisions and evidence

- Frozen five training cases and two holdouts before Work 050; partition SHA-256 values are `d19f8e33c1259e64632e6e89f9768fddeb8c6e54f4a204994e200037c6beba38` and `5045fd461c740e4edc461a702dc96bf3e93fba0b4dbb0bbeeca8adcaf4d5cf41`.
- Regenerated assembly STEP SHA-256 was `f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9`.
- Maximum FreeCAD mass-property error was `1.7042240975184457e-15`.
- Maximum global/component/interface residuals were `1.5631940186722204e-13`, `2.2737367544323206e-13`, and `0`.
- Seven nominal cases remained `running`; deliberate overload returned `DNF`; same-input replay hash was `da4848de71c19f9d76cad00cdf5013791e5b0d6f5b544293dcf9e094d782bb03`.
- Seven malformed/unsupported controls failed closed.
- Focused tests first exposed early typed-result serialization, then disproved the assumption that overload would fail only one connection. The implementation retained the physical multi-capacity exceedance and changed only that over-specific test expectation.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_vehicle_load_cases -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work048.ps1
# exit 0; status=passed; cases=8; nominal=7; overload=DNF
# max_global_residual=1.5631940186722204e-13
# max_component_residual=2.2737367544323206e-13
# mass_property_error=1.7042240975184457e-15; replay=exact; negative_controls=7

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 326 tests in 35.360s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Staged checks, explicit commit, and clean-tree replay are performed after this record exists and reported in the final handoff.

## Limitations and follow-up

The structural response is rigid-component cut-load algebra with synthetic declared capacities, not stress FEA. There is no arbitrary-geometry meshing, local stress/strain, contact, preload, friction, transient load, vibration, crash, or physical calibration. Work 049 may test an end-to-end fixed baseline using this exact evidence class, but its report must retain this blocker for Work 050 readiness.
