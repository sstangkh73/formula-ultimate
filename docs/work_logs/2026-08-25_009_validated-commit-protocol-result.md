# Work 009 Result: Validated Commit Protocol

Status: Completed

Thai companion: `2026-08-25_009_validated-commit-protocol-result.th.md`

## Outcome

The project-agent instructions now require every completed and validated work
item to be committed immediately. Completion requires a successful commit,
explicit staging, staged-diff inspection, fail-fast validation, and reporting
the resulting short hash.

Previously completed uncommitted work was separated and committed by work item:

- Work 006: `455a9d0` — constrained CAD evidence loop
- Work 007: `a4ef20f` — main research direction
- Work 008: `774c66e` — ten real-circuit physics profiles

## Files changed

- `AGENTS.md`
- `AGENTS.th.md`
- `docs/physics/CIRCUIT_MODEL.md`
- `docs/physics/CIRCUIT_MODEL.th.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.th.md`
- `docs/work_logs/2026-08-25_008_real-circuit-physics-result.th.md`
- this Work 009 plan/result pair in English and Thai

## Decisions

1. A work item is not complete until its commit succeeds.
2. Staging must use an explicit file list; blanket `git add -A` is prohibited in
   a mixed worktree.
3. Validation gates must run separately or with fail-fast control flow so a
   later success cannot mask an earlier failure.
4. `git diff --cached --check` is mandatory before commit.
5. Commit amendment, history rewrite, squash, push, and publication remain
   separate actions requiring explicit user authorization.
6. Work 006–008 history was preserved rather than rewritten.

## Corrective evidence

During the Work 008 staged check, `git diff --cached --check` correctly reported
trailing whitespace. The shell invocation used unconditional semicolon
sequencing, so the later `git commit` still ran. Work 009 removes those spaces,
records the event transparently, and adds the failure-propagation rule to
prevent recurrence.

## Validation

### Repository tests

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`

```text
Ran 42 tests in 0.573s
OK
```

### Working-tree whitespace check

```powershell
git diff --check
```

Exit status: `0`. Git emitted only LF-to-CRLF conversion warnings; no whitespace
errors remained.

### Staged validation and commit

`git diff --cached --check`, staged-scope inspection, commit creation, and
post-commit verification are performed after this result record is staged. The
successful Work 009 short hash is reported in the final handoff.

## Limitations

- This protocol governs local commits; it does not authorize a remote push.
- Git hooks and repository configuration can still block a commit. Such a
  blocker must keep the work incomplete and be reported.

## Follow-up

Apply this protocol to every later numbered work item and keep one auditable
commit boundary per completed work item unless its plan explicitly justifies a
different structure.
