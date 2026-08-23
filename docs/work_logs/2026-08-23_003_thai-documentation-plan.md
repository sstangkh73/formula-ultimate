# Work Plan 003: Separate Thai Documentation

Date: 2026-08-23
Status: Completed

## Objective

Create a separate Thai companion for every maintained English Markdown file in
the Formula Ultimate repository and enforce the bilingual-documentation rule in
the repository workflow and automated tests.

## Scope

- Use the suffix `.th.md` for Thai companion files.
- Translate all current maintained Markdown documentation, including root
  governance files, configuration guidance, research/physics documents, and all
  work plans/results.
- Keep identifiers, equations, commands, paths, units, test values, statuses,
  and evidence equivalent across languages.
- Update repository instructions so future Markdown work creates or updates the
  Thai companion in the same work item.
- Add an automated repository-contract test that detects a missing Thai
  companion.

## Non-Goals

- Translating Python source, TOML, YAML, Git metadata, or generated artifacts.
- Replacing English documents with mixed-language content.
- Changing physics behavior or research claims.
- Automatically asserting semantic translation quality from a file-existence
  test.

## Planned Deliverables

- Thai companions for every current maintained English `.md` file.
- Updates to `AGENTS.md`, `CONTRIBUTING.md`, `docs/WORK_PROTOCOL.md`, and
  `README.md` describing the bilingual rule.
- An automated test enforcing English-to-Thai Markdown companion coverage.
- English and Thai Work 003 result records with reproducible evidence.

## Naming Rule

```text
document.md          -> document.th.md
<slug>-plan.md       -> <slug>-plan.th.md
<slug>-result.md     -> <slug>-result.th.md
README.md            -> README.th.md
```

## Work Sequence

1. Inventory maintained Markdown files outside ignored/generated directories.
2. Translate root and configuration documents.
3. Translate research, physics, validation, and workflow documents.
4. Translate historical work plans and result evidence without changing their
   original meaning.
5. Update bilingual workflow instructions and repository navigation.
6. Add and run the companion-coverage test.
7. Review exact identifiers, equations, paths, commands, units, and test values.
8. Write separate English and Thai result records.
9. Run all tests, compilation, and staged-diff checks; commit and push.

## Validation Plan

- Enumerate all maintained English Markdown files and verify a sibling `.th.md`
  file exists.
- Verify every Thai companion is non-empty and references its English source.
- Run the full Python test suite.
- Run Python compilation and `git diff --cached --check`.
- Verify GitHub Actions after push.

## Success Criteria

- Every maintained English Markdown file has a separate Thai companion.
- Future missing companions fail the repository-contract test.
- Work-log plan/result pairing remains valid in both languages.
- No Python physics behavior changes in this work item.
- Local and GitHub Actions test suites pass.

## Risks and Controls

- Translation drift: preserve technical identifiers/equations verbatim and link
  each Thai file to its source.
- Ambiguous naming: use one repository-wide `.th.md` convention.
- Maintenance overhead: enforce companion coverage automatically and require
  both files in the same work item.
- False confidence: automated tests prove coverage and structure, not perfect
  semantic equivalence; translation review remains a human/agent responsibility.
