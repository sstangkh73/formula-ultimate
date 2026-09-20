# Work 143 Result: CI Artifact-Skip Repair

Thai companion: `2026-09-20_143_ci-artifact-skip-repair-result.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Outcome

CI is green over the pushed history. The first CI run for Works 108–142 was red for one reason, and that reason is now repaired.

| Run | Commit | Result |
| --- | --- | --- |
| `35523292349` | `04e6421` (Work 141) | `Ran 1022 tests` — **FAILED (errors=6, skipped=38)** |
| `35524051329` | `6624a96` (Work 143) | `Ran 1022 tests` — **success**, 7m34s |

## Bug report

- **Symptom.** Six errors, all raised from `setUp` in `tests/test_independent_claim_validation.py` with `FileNotFoundError: .../artifacts/work128/run_a/telemetry.json`.
- **Root cause.** That module reads recorded Work 128 telemetry, and `.gitignore` excludes `artifacts/` because of its size, so the input is absent on every clean checkout. An exception in `setUp` is reported as an error, not a skip, so the suite could not be green anywhere the artifacts had not been generated locally.
- **Fix.** Decorate the class with the repository's existing `requires_artifacts("artifacts/work128/run_a/telemetry.json")` from `tests/artifact_requirements.py`, the same guard `test_campaign_physics.py`, `test_refined_housing_mesh.py` and `test_whole_mechanical_vehicle_candidate_001.py` already use. Nothing was deleted and no assertion was weakened.
- **Regression.** With the artifact present: `Ran 6 tests — OK`. With `artifacts/work128` moved aside: `Ran 6 tests — OK (skipped=6)`. Full suite: `Ran 1022 tests — OK (skipped=11)`. CI: success.

This is the same class of defect as Work 136, where a test imported CadQuery unconditionally. Both were found by the first environment that did not happen to have the input.

## Files changed

- `tests/test_independent_claim_validation.py`
- `EVIDENCE.md` and `EVIDENCE.th.md`: the CI section now records both runs, the fault and the repair, and adds the local Work 143 measurement.
- this bilingual plan and result

## Validation

```text
Command: python -m unittest tests.test_independent_claim_validation
Exit code: 0
Result: Ran 6 tests — OK (artifact present)

Command: same, with artifacts/work128 moved aside
Exit code: 0
Result: Ran 6 tests — OK (skipped=6)

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests in 379.509s — OK (skipped=11)

Command: git push origin main ; gh run watch 35524051329
Result: conclusion success
```

## Claims

- Supported: CI reaches success on a clean checkout at `6624a96`; the Work 129 assertions still execute wherever the recorded telemetry exists.
- Not supported: that the Work 129 logic is exercised on CI. It is skipped there, by name, and that is stated in `EVIDENCE.md`.

## Limitations and follow-up

A skipped test proves nothing about the code it covers. The general fix would be to commit a small fixture of the recorded telemetry so the assertions can run everywhere, or to generate it in CI. Either is a separate work item.
