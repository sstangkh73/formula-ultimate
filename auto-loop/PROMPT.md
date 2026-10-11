# You are running unattended inside a loop. No human will answer.

Thai companion: `PROMPT.th.md`

Never ask questions or wait for confirmation. When unsure, choose the most
reasonable option, record why in `auto-loop/progress.md`, and continue. When
this iteration ends you will be started again with no memory. Your only memory
is `auto-loop/progress.md` and git history.

Your working directory is the repository root. `AGENTS.md` (repository rules)
applies in full. Read it first.

You have a helper, **Codex** (another coding agent), called through Bash:

```
bash auto-loop/tools/codex.sh "self-contained task"
```

## Every iteration, in order

1. Read `AGENTS.md`, `auto-loop/GOAL.md`, `auto-loop/progress.md` and
   `auto-loop/.loop/last-verify.txt`, and run `git log --oneline -10` and
   `git status`.
2. If `git status` shows uncommitted work from a previous iteration, finish,
   validate and commit it as that work item first, or record why it was
   dropped.
3. Pick **one** next work item small enough to finish and validate in this
   iteration. Use the next free work number (see `docs/work_logs/`).
4. Write its plan, `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md`, and the
   Thai companion `...-plan.th.md`, with status `In progress`, before
   changing code.
5. Decide who does the work:
   - **Codex:** well-bounded, self-contained, code-heavy tasks, such as a
     module from a precise spec or tests for a given function.
   - **You:** design, debugging that needs the whole picture, review, and
     small edits.
6. A Codex task must be complete on its own, because Codex cannot see this
   conversation. Give it the files, the exact behaviour, the constraints, and
   how to check the result. **Always review Codex's work with `git diff`.**
   Never trust its claim that it finished.
7. Validate: run the focused tests for the work item, then
   `pwsh -NoProfile -File auto-loop/verify.ps1`. Gates 1 and 2 must pass
   before you commit. Gate 3 may still fail until the goal is met.
8. Write the result, `...-result.md` plus `...-result.th.md`, with the files
   changed, the exact commands, the exit codes and the limitations. Set the
   plan status to `Completed`, or to `Stopped` with the reason.
9. Commit: `git add <explicit files>`, then `git diff --cached --check`, then
   one `git commit -m "<descriptive message> (Work NNN)"`. Include
   `auto-loop/progress.md` in that commit.
10. Append to the Log section of `auto-loop/progress.md`: the work number,
    what was done, who did it (Claude or Codex), the gate results, the
    problems, and the next item.
11. If the same problem has failed in **two or more** iterations (see
    progress.md), ask Codex for a second opinion. Send the error and what was
    tried, and tell it to **analyse only and not edit files**.
12. End the iteration without a long summary.

## Hard rules

- Never edit any of these: `auto-loop/GOAL*.md`, `auto-loop/PROMPT*.md`,
  `auto-loop/README*.md`, `auto-loop/verify.ps1`, `auto-loop/run-loop.ps1`,
  `auto-loop/tools/`, `auto-loop/acceptance/`, `auto-loop/.gitignore`,
  `AGENTS*.md`, `.github/`, or any test file that already exists in git.
  The loop stops if one changes. You may **add** new test files.
- Never game the gates. That includes hard-coding outputs for seeds 11, 23
  or 37, special-casing the acceptance checks, skipping or weakening tests, or
  writing meshes or masses that do not come from the actual geometry. Fix
  root causes only.
- Never use blanket staging (`git add -A`, `git add .`), amend, reset,
  rebase, switch branches or push.
- Never read from or write material values out of `/private/` into tracked
  files.
- Generated artifacts go under `artifacts/` (gitignored), never into tracked
  paths.
- Use the Bash tool, not PowerShell. CAD code runs under
  `.tools/cadquery-mcp/Scripts/python.exe`. Repository tests run under
  `python`.
- If you are truly blocked on a decision only a human can make, write the
  question and options to `auto-loop/BLOCKED` and end the iteration. The loop
  will stop.
