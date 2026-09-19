# Work 136 Plan: CadQuery-Optional Test Guard and Status Documentation

Thai companion: `2026-09-20_136_cadquery-optional-test-guard-and-status-docs-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Numbering note

Work 135 documents name "Work 136" as the downstream physics rerun on the Work 135 native solids. The detailed-plan index states that future numbers are not reservations and that an intervening work takes the next unused number. This repair consumes number 136; the native-solid physics rerun therefore maps to the next unused number (currently 137). Historical Work 135 records are not rewritten.

## Objective

1. Make the default suite pass again in an environment without CadQuery. At commit `ed5dae3`, `python -m unittest discover -s tests` on Python 3.14.3 without CadQuery reported `Ran 956 tests ... FAILED (errors=1, skipped=8)`. The cause is a module-level `from scripts.cad.build_native_detailed_vehicle import ...` in `tests/test_native_detailed_vehicle.py`, and that script runs `import cadquery as cq` at import time. `pyproject.toml` declares CadQuery an optional extra ("CadQuery-backed CAD kernel tests skip themselves when it is absent"), and CI installs only `pip install -e .`. The Ubuntu CI run would therefore fail when the 29 unpushed commits are pushed.
2. Correct stale status statements in `EVIDENCE.md`, `README.md` and their Thai companions.

## Scope

- `tests/test_native_detailed_vehicle.py`: keep the six declaration/admission tests unconditional. Move the three kernel-dependent tests (closed-flag regression, fan fusion regression, signed-zero signature) into a class guarded by `unittest.skipUnless(HAS_CADQUERY, ...)` that imports the build script lazily in `setUpClass`, which is the existing pattern in `tests/test_brep_grammar.py`.
- `EVIDENCE.md` / `EVIDENCE.th.md`: replace the 7 September test counts with measured current counts, state that the 29 local commits after `2c2bf36` have no CI run yet, and disclose that the Work 125, 127, 128 and 129 comparison outcomes are config-declared synthetic fixtures, not simulator outputs.
- `README.md` / `README.th.md`: update "Current Implementation Status" to reflect the Level-0 kernel, bounded campaign v3, the Works 108–135 package and the native Work 135 geometry. Remove the stale claim that two open problems keep Ubuntu CI red.
- This bilingual plan and the matching bilingual result.

## Non-goals

No change to `scripts/cad/build_native_detailed_vehicle.py`, source modules, configurations, artifacts or the Work 125–135 records. No weakening of test assertions. The kernel tests must still run and pass where CadQuery is present. No push, CI trigger or history rewrite.

## Validation

1. `python -m unittest tests.test_native_detailed_vehicle -v` on system Python without CadQuery: exit 0, 6 passed, 3 skipped.
2. `.tools/cadquery-mcp/Scripts/python.exe -m unittest tests.test_native_detailed_vehicle -v`: exit 0, 9 passed, 0 skipped.
3. `python -m unittest discover -s tests`: exit 0 with no errors.
4. `python -m unittest tests.test_repository_contract -v`: exit 0.
5. `git diff --check` and `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: all validation gates pass and the documents state only measured counts. Failure: any kernel test is lost rather than skipped, any assertion is weakened, or the suite still errors.

## Risks

- Counts quoted in documents go stale. Mitigation: date them and keep the reproducing command as the authority.
- The config-declared outcome disclosure could be read as a retraction of Works 125–129. It is scoped: those works verified gate, control and replay logic, and their numeric outcomes are synthetic fixtures.
