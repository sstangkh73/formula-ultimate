# Work 148 Result: Hierarchical Free-Form Composition Auto-Loop

Thai companion: `2026-10-11_148_hierarchical-composition-auto-loop-result.th.md`

Date: 2026-10-11

Plan: `2026-10-11_148_hierarchical-composition-auto-loop-plan.md`

Status: Completed

## Outcome

`auto-loop/` is now a repository-conforming Claude + Codex runner whose goal
is hierarchical free-form composition v1. The generator is not implemented,
and the loop has not been run. The loop's starting state was measured: Gates
1 and 2 pass, and Gate 3 fails 13 of 13 tests because
`scripts/hierarchy/generate_hierarchical_vehicle.py` does not exist.

## Files changed

- `auto-loop/GOAL.md`, `GOAL.th.md`: the goal, the manifest contract, seven
  acceptance criteria, boundaries, and what passing does not mean.
- `auto-loop/acceptance/test_hierarchical_composition.py`: 13 black-box
  acceptance tests. They recompute replay, hierarchy, capability coverage,
  mesh closure, volume and mass, centre of mass, box fraction, program hashes,
  interface contact, interpenetration and seed diversity independently from
  the generated meshes.
- `auto-loop/verify.ps1`: three fail-fast gates (material boundary,
  repository suite, acceptance). It clears `FU_ACCEPTANCE_GENERATOR`.
- `auto-loop/run-loop.ps1`: runs at the repository root with no `git init`.
  It requires a clean tree, refuses `main`, and works on
  `loop/hierarchical-composition`. It hashes 133 protected files (loop
  files, `AGENTS*.md`, `.github/`, every tracked test). It checks the branch,
  that history was not rewritten, and that `main` has not moved. It never
  stages or commits. It denies blanket staging, amend, reset, rebase, switch,
  push and web tools to the agent. It supports `-PreflightOnly`, and an agent
  can stop it by writing `auto-loop/BLOCKED`.
- `auto-loop/PROMPT.md`, `PROMPT.th.md`: one numbered work item per iteration
  under `AGENTS.md`.
- `auto-loop/README.md`, `README.th.md`, `progress.md`, `progress.th.md`,
  `.gitignore`, `tools/codex.sh`.
- Deleted the template demo `auto-loop/src/bahttext.py` and
  `auto-loop/tests/test_bahttext.py`. They were never tracked.
- `.gitattributes`: `/auto-loop/tools/*.sh text eol=lf`. This was not in the
  plan. It was added because `core.autocrlf=true` would check out
  `codex.sh` with CRLF and break bash.

## Decisions

- The goal translates the owner's request into measurable criteria (at least
  4 levels, at least 150 leaves, at least a 100x size span, all nine
  capabilities in depth, measured contact, seed diversity). It does not
  prescribe any conventional part list.
- The acceptance tests run under the system Python and check meshes directly.
  The generator runs under the pinned CadQuery runtime as a subprocess.
- Codex's last-message file is `.txt`, not `.md`, because
  `tests/test_repository_contract.py` requires a Thai companion for every
  `.md` outside excluded folders, and `auto-loop/.loop/` is not excluded.
- The agent commits its own work items with explicit staging. The runner only
  guards and judges.

## Validation

1. Acceptance self-check against a scratchpad fixture generator (synthetic
   triangular-prism chains, injected through `FU_ACCEPTANCE_GENERATOR`). The
   fixture is not committed.
   Command per case:
   `FIXTURE_BREAK=<case> python -m unittest discover -s auto-loop/acceptance`

   | Case | Result |
   |---|---|
   | valid | `OK` (13 tests) |
   | open_mesh | FAIL `test_leaf_meshes_closed_and_masses_measured` |
   | wrong_mass | FAIL `test_leaf_meshes_closed_and_masses_measured` |
   | missing_cap | FAIL `test_each_capability_has_a_deep_subtree`, `test_each_capability_varies_across_seeds` |
   | penetrate | FAIL `test_interfaces_touch_and_nothing_interpenetrates` |
   | gap | FAIL `test_interfaces_touch_and_nothing_interpenetrates` |
   | nondeterministic | FAIL `test_same_seed_is_byte_identical` |
   | template | FAIL `test_whole_trees_differ_across_seeds`, `test_each_capability_varies_across_seeds` |
   | boxes | FAIL `test_not_mostly_boxes` |
   | disconnected | FAIL `test_children_of_every_assembly_are_connected` |

2. `pwsh -NoProfile -File auto-loop/verify.ps1`, run with
   `FU_ACCEPTANCE_GENERATOR` set to a bogus command to prove that it is
   cleared. Exit 3. Gate 1 passed. Gate 2: `Ran 1042 tests in 287.832s`,
   `OK (skipped=11)`. Gate 3: `Ran 13 tests`, `FAILED (failures=13)`, every
   failure `missing: ...scripts\hierarchy\generate_hierarchical_vehicle.py`.
3. The PowerShell parser reported 0 errors for `run-loop.ps1` and
   `verify.ps1`, and `bash -n auto-loop/tools/codex.sh` passed.
4. Runner preflight in a throwaway worktree on branch
   `loop/preflight-check-148`, with the throwaway commit `2e855fb` (removed
   afterwards together with the worktree and branch):
   - The dirty tree was refused: `working tree is not clean`.
   - The first run showed that a helper named `Git` shadowed `git` and
     recursed (`call depth overflow`). It was renamed to `Invoke-Git`.
   - `-PreflightOnly -Branch loop/preflight-check-148`:
     `133 protected files hashed`, verify ran, and the runner exited 0.
   - Wrong branch refused: `on branch 'loop/preflight-check-148'; switch to
     'loop/hierarchical-composition' or main first`.
   - Bad branch name refused: `Branch must be named loop/<name>`.
5. The repository suite was run three times on unmodified `main` code. Run 1:
   `Ran 1042 tests in 354.374s`, `FAILED (failures=4, skipped=11)`. The test
   names were not captured because only the tail was saved. Runs 2 and 3
   passed (`OK (skipped=11)`). The cause was not found. It is recorded
   in `auto-loop/progress.md` as known intermittent behaviour.
6. In the fresh worktree, the suite gave `FAILED (failures=3, errors=6,
   skipped=41)`. The failures were in `test_design_diversity`,
   `test_vehicle_load_cases`, `test_whole_vehicle_baseline`,
   `test_whole_vehicle_search`, `test_paper_reviews` and
   `test_part_resolution`, all of which read gitignored local `artifacts/`
   or `papers/`. This is a pre-existing clean-checkout gap, not caused by this
   work.
7. Commit gates: `python -m unittest tests.test_repository_contract`, staged
   file inspection, and `git diff --cached --check` (see the final handoff for
   the commit hash).

## Limitations

- The loop has not been run, so the cost per iteration and the agent's real
  behaviour are unknown.
- `--max-turns` is used as in the original template, but it is not listed in
  `claude --help` (version 2.1.293), so it was not verified.
- Interpenetration checks sample vertices and centroids. The box fraction and
  three-seed diversity are proxies. Passing Gate 3 is a representation gate,
  not physical validation.
- An intermittent baseline failure (1 of 3 runs) remains unexplained.

## Follow-up work

- Review `auto-loop/GOAL.md` and the acceptance thresholds before the first
  run.
- Run `pwsh -File auto-loop/run-loop.ps1 -PreflightOnly`, then a short real
  run (for example `-MaxIterations 2`) to measure cost.
- Capture the names of any intermittent Gate 2 failures, and guard the
  artifact-dependent tests for clean checkouts.
- A later goal: couple the hierarchy to Level-0 physics and the race kernel.
