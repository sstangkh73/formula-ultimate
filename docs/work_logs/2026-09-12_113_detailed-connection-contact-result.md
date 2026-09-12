# Work 113 Result: Detailed Connection Contact

Thai companion: `2026-09-12_113_detailed-connection-contact-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and numerical evidence

Work 113 produced deterministic mating STEP solids and three-level discrete contact fields for the threaded reference and segmented-ramp alternative. All four solids were valid and each male/female overlap was `0 m3`. The rounded reference helix has `8` turns; the alternative has `6` engagement ramps.

Final result SHA-256 is `a0b9fe19fbc9a3105a5bcac65a40d682e41a05d793d8063095e3be00afa58148`; replay is exact. At 48 patches, the reference normal stiffness was `4643562042.262461 N/m`, shear displacement `2.691898996122744e-7 m`, and maximum patch pressure `29265773.701437008 Pa`. The alternative values were `923076923.076923 N/m`, `1.3541666666666667e-6 m`, and `145212606.229031 Pa`. Both remained stick at the baseline. Last-two pressure changes were `0.012639112850523751` and `0.000525835058853858`; stiffness/displacement changes were zero. Maximum reduced-model error over the registered stick samples was zero.

Low preload/friction caused slip at `240 N` capacity. Half engagement halved reference stiffness; clearance increased axial displacement from `1.0172281535751857e-5 m` to `5.017228153575186e-5 m`; reverse shear reversed displacement. Removed and severed joints were rejected.

Changed: the four proposed implementation/config/runner/test files, bilingual `DETAILED_CONNECTION_CONTACT_V1` contract, and this bilingual plan/result. Ignored evidence is under `artifacts/work113/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_detailed_connection_contact -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/structural/detailed_connection_contact.py scripts/development/run_detailed_connection_contact.py
# exit 0
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_a
# exit 0; result SHA-256 above
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_b --replay-reference artifacts\work113\run_a\result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_physical_interface_graph tests.test_detailed_connection_contact tests.test_repository_contract -v
# exit 0; 23 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 113 files
git diff --cached --check
# exit 0
```

The patch law, rounded thread and synthetic properties do not establish local flank/root stress, nonlinear solver convergence, loosening, fatigue, manufacturing or physical safety. The verified commit hash is reported in the final handoff.
