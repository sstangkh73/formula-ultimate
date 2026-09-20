# Work 143 Plan: CI Artifact-Skip Repair

Thai companion: `2026-09-20_143_ci-artifact-skip-repair-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

## Objective

Make the suite green on a clean checkout again. The first CI run over the pushed history, run `35523292349` at commit `04e6421`, failed with `Ran 1022 tests ... FAILED (errors=6, skipped=38)`.

## Entry evidence

All six errors are the same fault: `tests/test_independent_claim_validation.py` reads `artifacts/work128/run_a/telemetry.json` in `setUp`, and `.gitignore` excludes `artifacts/`, so the file is absent on CI. The traceback is `FileNotFoundError` inside `setUp`, which unittest reports as an error rather than a skip.

The repository already has the right mechanism: `tests/artifact_requirements.py` provides `requires_artifacts`, used by `test_campaign_physics.py`, `test_refined_housing_mesh.py` and `test_whole_mechanical_vehicle_candidate_001.py`. The Work 129 test module was written without it.

This is the same class of defect as Work 136: a test that needs an input the checkout does not carry must skip with a message naming the input, not fail.

## Scope

- `tests/test_independent_claim_validation.py`: decorate the test class with `requires_artifacts("artifacts/work128/run_a/telemetry.json")`.
- `EVIDENCE.md` and `EVIDENCE.th.md`: record the measured CI outcome for the pushed history, before and after this repair.
- This bilingual plan and its matching bilingual result.

## Validation

1. `python -m unittest tests.test_independent_claim_validation`: exit 0, 6 tests pass where the artifact exists.
2. The same command with `artifacts/work128` moved aside: exit 0, 6 tests skipped.
3. `python -m unittest discover -s tests`: exit 0.
4. A pushed CI run reaching conclusion `success`.

## Success and failure criteria

Success: the tests run where the evidence exists, skip where it does not, and CI reaches success on a clean checkout.

Failure: a test is deleted or weakened to obtain green, or a skip hides a genuine code failure.

## Risks and non-goals

- Risk: skipping hides a regression in the Work 129 logic on CI. Accepted and stated: those assertions only hold against recorded evidence, and they still run wherever that evidence exists.
- Non-goals: no change to the Work 129 logic or its recorded evidence, no other test touched, no history rewrite.
