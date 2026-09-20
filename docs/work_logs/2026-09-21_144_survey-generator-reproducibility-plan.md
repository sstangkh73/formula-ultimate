# Work 144 Plan: Survey Generator Reproducibility

Thai companion: `2026-09-21_144_survey-generator-reproducibility-plan.th.md`

Date: 2026-09-21 (Asia/Bangkok)

Status: Completed

## Objective

Make `scripts/development/build_vehicle_part_resolution_config.py` reproduce both committed survey declarations byte for byte, so the Work 141 and Work 142 admitted results stay derivable from the repository.

## Entry evidence

Work 142 added an `--upgrade` mode to the generator and, with it, an `upgraded_definitions` key that the generator wrote into every declaration, including a plain run. Regenerating the Work 141 declaration therefore produced a file one key larger than the committed `config/development/vehicle_part_resolution_v1.json`.

That matters because the Work 141 result records `config_sha256` and `protocol_sha256` over exactly that file. A declaration that cannot be regenerated is a declaration whose admitted result cannot be re-derived, which is the property the replay discipline exists to protect. The working tree showed the drift as a modified `vehicle_part_resolution_v1.json` after the Work 142 commit.

## Scope

- `scripts/development/build_vehicle_part_resolution_config.py`: emit `upgraded_definitions` only for an upgrade run.
- Restore `config/development/vehicle_part_resolution_v1.json` from the repository and confirm both declarations regenerate with no diff.
- This bilingual plan and its matching bilingual result.

## Validation

1. `git checkout -- config/development/vehicle_part_resolution_v1.json`, then regenerate both declarations and confirm `git status` reports no change to either.
2. `python -m unittest tests.test_part_resolution tests.test_repository_contract`: exit 0.
3. `python -m compileall -q scripts src tests`, `git diff --check`, `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: both declarations regenerate with no diff, and the tests pass.

Failure: a committed declaration is rewritten to match the generator, which would silently invalidate a recorded result hash.

## Risks and non-goals

- Risk: the same drift returns the next time the generator grows a field. The result records the rule that a generator change must keep older declarations regenerable.
- Non-goals: no change to any declaration content, no re-run of Works 141 or 142, no change to the gate.
