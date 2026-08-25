# Project Instructions for Formula Ultimate

## Mandatory Work-Log Protocol

Before any task-specific code, configuration, research document, or experiment
change:

1. Create `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md` and its separate Thai
   companion `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.th.md`.
2. State objective, scope, planned files, validation, success criteria, risks,
   and explicit non-goals.
3. Mark its status `In progress` before starting the task.

After the work and before its final commit:

1. Create the matching
   `docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.md` and
   `docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.th.md`.
2. Record files changed, decisions, exact test commands, exit status, relevant
   output, limitations, and follow-up work.
3. Change the plan status to `Completed` only after validation passes, or to
   `Stopped` with the reason when the task cannot be completed.

Plans and result records are append-oriented evidence. Do not rewrite an older
record to make a later outcome look planned; create a new numbered work item.

## Mandatory Validated-Commit Protocol

Every work item that reaches `Completed` must be committed immediately after
its declared validation passes. A work item is not complete until the commit
succeeds.

1. Stage only the explicit files belonging to the work item. Never use blanket
   staging such as `git add -A` in a mixed worktree.
2. Inspect the staged scope and run `git diff --cached --check` before commit.
3. Run validation gates with fail-fast control flow or as separate commands. A
   failed command must stop the commit; a later successful command must never
   mask its exit status.
4. Create one descriptive commit for the completed work item unless an explicit
   plan justifies multiple commits.
5. Verify the new commit and report its short hash in the result or final handoff.
6. Preserve unrelated user changes. Do not amend, rewrite, squash, push, or
   publish history unless the user explicitly requests that separate action.

If validation, a commit hook, or Git configuration prevents the commit, leave
the plan `In progress` or mark it `Stopped` as appropriate and report the exact
blocker. Do not claim the work item is complete.

## Mandatory Bilingual Markdown Protocol

- Every maintained English Markdown file `name.md` must have a separate Thai
  companion named `name.th.md` in the same directory.
- Create or update both files in the same work item and commit.
- The Thai file must identify its English source by filename.
- Preserve code identifiers, equations, commands, paths, units, numeric
  evidence, statuses, and limitations across both languages.
- Do not mix the full Thai translation into the English file.
- A missing or stale companion means the documentation work is incomplete.

## Engineering Rules

- Work from explicit physics assumptions and SI units.
- Separate feasibility validation from simulation and scientific validation.
- Treat conservation residuals, numerical failures, and invalid states as
  observable outputs, never silent corrections.
- Never call a design physically validated from Level-0 simulation alone.
- Keep fixed-topology baselines and free-topology experiments comparable by
  compute budget, component library, constraints, and random seeds.
- Preserve deterministic replay metadata for every experiment.
- Add tests with every implemented physical law or component model.

## Review Discipline

For experiment changes, explicitly define independent variables, dependent
variables, controls, metrics, success criteria, and failure criteria. Attempt to
falsify the preferred hypothesis and record supporting evidence, contradicting
evidence, alternative explanations, missing evidence, and confidence.
