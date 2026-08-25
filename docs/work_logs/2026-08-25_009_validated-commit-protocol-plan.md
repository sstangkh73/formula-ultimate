# Work 009 Plan: Validated Commit Protocol

Status: Completed

Thai companion: `2026-08-25_009_validated-commit-protocol-plan.th.md`

## Objective

Make the user's instruction to commit every completed and validated work item a
mandatory repository protocol, and repair the Work 008 Markdown whitespace
issue exposed by the first staged validation attempt.

## Scope

- Add a mandatory post-validation commit section to the English and Thai
  project-agent instructions.
- Require explicit staging, cached-diff inspection, a failing-fast cached
  whitespace check, successful commit creation, and commit-hash reporting.
- Prohibit treating a failed validation command as success merely because a
  later command in the same shell invocation succeeds.
- Preserve unrelated user changes and prohibit blanket staging.
- Remove the trailing Markdown spaces identified in the committed Work 008
  documentation without rewriting the earlier commit.
- Create bilingual Work 009 result evidence and commit the completed work.

## Planned files

- `AGENTS.md`
- `AGENTS.th.md`
- affected Work 008 Markdown files with trailing whitespace
- this Work 009 plan/result pair in English and Thai

## Validation

```powershell
python -m unittest discover -s tests -v
git diff --check
git diff --cached --check
git status --short
git log -4 --oneline
```

Checks that must gate later actions will be executed separately or with
fail-fast control flow, never as an unconditional semicolon chain.

## Success criteria

- English and Thai project instructions both require a commit after validation.
- The protocol requires explicit scope, failure propagation, and hash reporting.
- Work 008 trailing whitespace is removed.
- Repository tests and whitespace checks pass.
- Work 009 itself is committed and its commit hash is reported.

## Risks

- A dirty worktree can contain unrelated user changes; staging must remain
  explicit.
- A commit hook or Git identity problem can block the commit after validation;
  this must be reported as incomplete rather than silently ignored.

## Explicit non-goals

- No history rewrite or amendment of completed Work 006–008 commits.
- No push to a remote repository.
- No change to physics, CAD, or experiment behavior.
