# Work 136 Result: CadQuery-Optional Test Guard and Status Documentation

Thai companion: `2026-09-20_136_cadquery-optional-test-guard-and-status-docs-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Summary

The default suite passes again without CadQuery. The three kernel-dependent Work 135 tests now skip when CadQuery is absent, and they still run and pass in the pinned CadQuery environment. `EVIDENCE.md`, `README.md` and their Thai companions now state the measured test status, the absence of CI runs for unpushed commits, and which Works 125–129 outcomes are config-declared synthetic fixtures.

## Bug report

- Symptom: at `ed5dae3`, `python -m unittest discover -s tests` with Python 3.14.3 and no CadQuery reported `Ran 956 tests ... FAILED (errors=1, skipped=8)` with `ModuleNotFoundError: No module named 'cadquery'`.
- Root cause: `tests/test_native_detailed_vehicle.py` imported `scripts.cad.build_native_detailed_vehicle` at module level, and that script runs `import cadquery as cq` at import time. CadQuery is an optional extra (`pyproject.toml`), and CI installs only `pip install -e .`. The Work 135 bootstrap fix addressed the opposite direction (the CadQuery environment lacking the local package).
- Fix: added `HAS_CADQUERY = importlib.util.find_spec("cadquery") is not None`. The closed-flag, fan-fusion and signed-zero tests moved unchanged into `NativeDetailedVehicleKernelTests`, which is guarded by `unittest.skipUnless(HAS_CADQUERY, ...)` and imports the build script in `setUpClass`. This matches `tests/test_brep_grammar.py`. No assertion was changed.
- Retest: see Validation.

## Files changed

- Test: `tests/test_native_detailed_vehicle.py`.
- Documentation: `EVIDENCE.md`, `EVIDENCE.th.md`, `README.md`, `README.th.md`.
- Records: this bilingual Work 136 plan and result.

## Decisions

- **Numbering.** This repair consumed number 136. The native-solid physics rerun that Work 135 records call "Work 136" maps to the next unused number (currently 137), following the detailed-plan index rule that future numbers are not reservations. Work 135 records were not edited.
- **README status.** The stale "Phase 1 is one-dimensional powertrain only" paragraph was replaced with a dated inventory: Level-0 kernel, campaign v3 (`p = 0.5`), the Works 108–133 package and Work 135 native geometry.
- **Stale CI wording.** The README statement that "two open problems keep the Ubuntu CI run red" was stale; `EVIDENCE.md` already recorded the fix. It was replaced with the true current condition: the latest pushed commit `2c2bf36` is green on CI, and the later local commits have no CI run.
- **Synthetic fixture disclosure.** `EVIDENCE.md` now states that Works 125, 127, 128 and 129 compute numeric outcomes from configuration-declared values. For example, the Work 128 `0.5 s` improvement is `base_time_s: 100.0` minus `99.5` in `config/development/heldout_race_robustness_v1.json`. It also states that Works 126–130 used a `60.0 kg` box registry while Work 135 native geometry is `1023.65 kg`. These statements come from inspecting the configurations and modules in this session. The gate, control and replay logic those works tested is not retracted.

## Validation

Environment: Windows 11, system Python 3.14.3 (no CadQuery); pinned `.tools/cadquery-mcp` Python 3.12.14 with CadQuery.

```text
Command: python -m unittest tests.test_native_detailed_vehicle -v
Exit code: 0
Result: Ran 9 tests — OK (skipped=3); the 3 skips name the CadQuery kernel environment

Command: .tools/cadquery-mcp/Scripts/python.exe -m unittest tests.test_native_detailed_vehicle -v
Exit code: 0
Result: Ran 9 tests — OK (no skips)

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 964 tests in 380.405s — OK (skipped=11)
Before fix (ed5dae3): Ran 956 tests — FAILED (errors=1, skipped=8)

Command: python -m unittest tests.test_repository_contract -v
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

The count rose from 956 to 964 because the failed module previously counted as one error test. It now contributes nine tests, three of them skipped: 956 − 1 + 9 = 964, and 8 + 3 = 11 skipped.

## Claims

- Supported: the suite passes locally with the CI dependency set, and the Work 135 kernel regressions still pass where CadQuery exists.
- Not supported: that CI on Ubuntu is green for the unpushed commits. No push was made and no CI run exists. Other elementary-function or platform differences in Works 108–135 remain untested on Linux.

## Limitations and follow-up

- Push to obtain the first Ubuntu CI result for Works 108–136. The user must request that separately.
- Next research work (number 137 or the next unused number): rerun structural, thermal, flow, ground, actuation, energy and controller evaluation on the exact Work 135 solids.
- Replace the config-declared outcomes in the Work 125/127/128/129 comparison gates with simulator-derived outcomes before any comparative claim.
