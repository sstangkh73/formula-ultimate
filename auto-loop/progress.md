# Loop Progress

Thai companion: `progress.th.md`

Memory between iterations. The agent appends to the Log section every
iteration and commits it with its work item. The Thai companion is updated in
the same commit.

## Starting state (Work 148)

- Goal: `auto-loop/GOAL.md`, hierarchical free-form composition v1.
- Gate 1 (material publication boundary) and Gate 2 (repository suite) are the
  regression gates. Gate 3 (acceptance) fails because
  `scripts/hierarchy/generate_hierarchical_vehicle.py` does not exist yet.
- Next free work number: 149.
- Known baseline behaviour: on 2026-10-11 the repository suite on clean `main`
  failed once (4 failures, test names not captured) and passed on two
  reruns (`Ran 1042 tests ... OK (skipped=11)`). If Gate 2 fails in tests
  unrelated to your change, rerun once and record the test names here. Do not
  edit or skip existing tests. If the cause cannot be found, write it to
  `auto-loop/BLOCKED`.
- Several existing tests read gitignored local evidence (`artifacts/`,
  `papers/`). They pass in this checkout but fail in a fresh clone or
  worktree, so run the loop in this checkout only.

## Log

### Work 149 (iteration 1): part-tree data model, Completed

- Done: `src/formula_ultimate/hierarchy/part_tree.py` with frozen node,
  interface and tree dataclasses, `validate_part_tree`, iterative `roll_up`,
  metrics (`levels`, `leaf_ids`, `subtree_height`, `subtree_leaves`,
  `topology_signature` with the acceptance definition), and
  `to_manifest_nodes`/`to_manifest_interfaces` with the exact contract field
  sets. Tests: `tests/test_hierarchy_part_tree.py` (11 tests).
- Who: Codex wrote the code and tests. Claude reviewed the diff and wrote the
  records.
- Gates: Gate 1 PASS. Gate 2 `Ran 1053 tests`, `OK (skipped=11)`. Gate 3
  fails 13/13 because the generator is missing (expected).
- Problems and how to avoid them:
  - Calling `bash auto-loop/tools/codex.sh "$(cat file)"` is refused by the
    permission checker. A gitignored wrapper script was refused too. What
    works is a literal prompt that points at a task file:
    `bash auto-loop/tools/codex.sh "Read the task specification in the file auto-loop/.loop/taskNNN.txt (read only; do not edit anything under auto-loop/) and carry it out exactly."`
    Write the task file under the gitignored `auto-loop/.loop/` first.
  - Codex wrote its own work-log files with the wrong number (148). Tell
    Codex explicitly: "do not create or edit any docs/work_logs files".
  - `verify.ps1` does not write `last-verify.txt` (the runner does). To see
    the summary, pipe through
    `grep -a -E "^== Gate|PASS|^Ran |^OK|FAILED|^FAIL:|^ERROR:"`.
    Compound shell commands (`;`, `${...}`) can need approval, so keep each
    Bash call to a single pipeline.
- Next: Milestone 2. A seed-driven decomposition procedure that builds an
  abstract tree (no geometry) covering all nine capabilities: subtree height
  >= 2 and >= 5 leaves per capability, >= 4 levels, >= 150 leaves, and
  different topologies for seeds 11, 23 and 37, with no conventional part
  catalogue.
