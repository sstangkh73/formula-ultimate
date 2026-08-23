# Auditable Work Protocol

## Rule

Every discrete work item has two Markdown records sharing the same date,
sequence number, and slug in each language:

```text
docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md
docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.th.md
docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.md
docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.th.md
```

## Bilingual Markdown Rule

Every maintained English Markdown file has a separate Thai companion in the
same directory:

```text
document.md -> document.th.md
```

Create and update both in the same work item. The Thai file identifies the
English source filename and preserves technical identifiers, equations,
commands, paths, units, numeric evidence, statuses, claims, and limitations.
The files remain separate; do not append the complete translation to the
English document.

## Before Work: Plan Record

Create both language versions of the plan before task-specific changes. Include:

- objective;
- scope and non-goals;
- planned deliverables/files;
- ordered work sequence;
- validation plan;
- success and failure criteria;
- risks and controls;
- status (`In progress`).

Repository inspection needed to write an accurate plan is allowed, but no
implementation or task-specific mutation happens before the plan exists.

## During Work

- Keep scope aligned with the plan.
- If a material new objective appears, create a new numbered plan rather than
  silently expanding the current one.
- Record failures and rejected approaches for the result report.
- Do not weaken tests merely to obtain a pass.

## After Work: Result Record

Before the final commit, create the matching English and Thai result records
containing:

- status (`Completed`, `Partial`, or `Stopped`);
- summary of completed work;
- changed files grouped by purpose;
- key decisions and why;
- exact validation commands and exit codes;
- concise test output or artifact references;
- claims supported and explicitly unsupported;
- deviations from plan;
- known limitations and next recommended work.

Then update the plan status to match the outcome.

## Test-Evidence Format

```text
Command: python -m unittest discover -s tests -v
Environment: Python X.Y.Z, operating system
Exit code: 0
Result: N tests passed
Evidence: concise terminal output or versioned artifact path
```

Do not write "tests passed" without the command and result. Do not copy a prior
run as evidence for changed code.

## Commit Boundary

Normally both plans, implementation, tests, and both matching result records are
one reviewable commit. The commit hash cannot be embedded in that same commit;
Git history is the authoritative link. For experiment artifacts, both result
records must still capture the simulator/configuration commit used to generate
them.
