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
