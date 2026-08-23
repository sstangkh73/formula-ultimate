# Work Result 003: Separate Thai Documentation

Date: 2026-08-23
Status: Completed

## Summary

Created a separate Thai companion for every maintained English Markdown file in
Formula Ultimate and made bilingual Markdown coverage a mandatory, automated
repository contract. English and Thai plans now precede each work item, and
separate English and Thai result records close each work item.

No Python physics behavior changed in this work item.

## Changes

### Thai companions

Added Thai companions for:

- root project overview, agent instructions, and contribution guidance;
- configuration guidance;
- research charter, design-language boundary, physics-system plan, validation
  strategy, and work protocol;
- Work 001 bootstrap plan and result;
- Work 002 reference-kernel plan and result;
- Work 003 documentation plan and result.

After this result is included, the maintained documentation set contains 15
English Markdown files and 15 separate Thai companions.

### Workflow enforcement

- Updated `AGENTS.md` to require separate `.md` and `.th.md` plans/results and
  companion updates in the same work item.
- Updated `CONTRIBUTING.md` and `docs/WORK_PROTOCOL.md` with the bilingual rule.
- Updated `README.md` with a Thai-language entry point and bilingual workflow.
- Added a repository-contract test that recursively checks each maintained
  English Markdown file for a non-empty Thai companion that identifies its
  English source filename.

## Naming Decision

The repository uses one convention:

```text
document.md -> document.th.md
```

This keeps language files separate, predictable, and discoverable without
mixing complete translations into technical source documents.

## Validation Evidence

### Full test suite

Command:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

Result:

```text
8 longitudinal physics tests ... ok
6 repository contract tests ... ok

Ran 14 tests
OK
```

The new contract verifies:

- every maintained English Markdown file has a `.th.md` sibling;
- every Thai companion is non-empty;
- every Thai companion names its English source;
- completed plans still have matching result records.

### Coverage inventory

Final maintained-document count:

```text
English Markdown files: 15
Thai companion files:   15
Missing companions:      0
```

### Compilation and staged diff

Commands:

```powershell
python -m compileall -q src tests
git diff --cached --check
```

Exit code for each: `0`.

All commands are rerun after both result files are staged. GitHub Actions runs
the complete suite independently on Python 3.11 after push.

## Claims Supported

- Every currently maintained English Markdown file has a separate Thai file.
- Future missing Thai companions fail an automated repository test.
- Work plans and results now exist separately in both languages.
- Technical paths, commands, equations, units, values, claims, and limitations
  were intentionally preserved during translation.

## Claims Not Fully Automated

- File coverage tests cannot prove perfect semantic equivalence.
- Natural-language translation quality still requires review when either source
  changes materially.
- The test does not currently detect a stale Thai companion when both files
  exist but only the English content changed.

## Deviations from Plan

- None. The work remained documentation- and contract-only.

## Recommended Next Work

Resume the physics roadmap with a new bilingual plan/result pair. The next
physics work should implement the energy/work conservation audit recommended by
Work 002 before adding motors, batteries, or topology evolution.
