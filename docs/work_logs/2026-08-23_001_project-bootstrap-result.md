# Work Result 001: Project Bootstrap and Physics-System Planning

Date: 2026-08-23
Status: Completed

## Summary

Created the initial Formula Ultimate repository as a physics-first research
platform. The work defines the Phase-1 research boundary, Level-0 physics
contracts, typed topology design language, validation ladder, package layout,
and mandatory plan/result evidence workflow. A private GitHub repository was
created for the initial commit.

This result establishes structure and methodology only. It does not claim that
a vehicle physics implementation exists or has been validated.

## Deliverables

### Project governance

- `AGENTS.md`: mandatory plan-before-work and result-after-work instructions.
- `CONTRIBUTING.md`: minimum evidence and unit conventions.
- `docs/WORK_PROTOCOL.md`: naming, required record content, and commit rules.

### Research and physics design

- `docs/RESEARCH_CHARTER.md`: primary question, Phase-1 question, falsifiable
  hypotheses, alternative explanations, and non-goals.
- `docs/DESIGN_LANGUAGE_BOUNDARY.md`: fixed experimental controls, topology
  freedoms, typed domains, graph gates, and versioning requirements.
- `docs/PHYSICS_SYSTEM_PLAN.md`: fidelity ladder, Level-0 state and I/O,
  equations/contracts, pipeline, numerical strategy, failures, and milestones.
- `docs/VALIDATION_STRATEGY.md`: evidence ladder, required future physics
  tests, experiment controls, and bounded claim language.

### Repository skeleton

- `src/formula_ultimate/` package boundaries for components, topology, physics,
  simulation, telemetry, and experiments.
- `config/README.md` for versioned SI-unit configuration conventions.
- `pyproject.toml` for the Python package.
- `.github/workflows/tests.yml` for GitHub structural validation.
- `.gitignore` for generated simulations, caches, local tools, and artifacts.

### Automated validation

- `tests/test_repository_contract.py` validates required documents, package
  boundaries, TOML syntax, and plan/result pairing.

## Key Decisions

1. Phase 1 fixes the body envelope and four abstract contact patches so
   powertrain topology is the controlled independent variable.
2. Physical connections use typed effort/flow domains and explicit power sign
   conventions.
3. Conservation and graph validity are gates before fitness calculation.
4. Level 0 is a deterministic selection model, not real-world certification.
5. Physics implementation begins later with analytical reference cases rather
   than untested full-system code.
6. The GitHub repository is private to avoid publishing a new research project
   without a separate visibility decision.

## Validation Evidence

### Structural test suite

Command:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

Result:

```text
test_declared_package_boundaries_exist ... ok
test_every_result_has_a_matching_plan ... ok
test_pyproject_is_valid_toml ... ok
test_required_governance_and_physics_documents_exist ... ok

Ran 4 tests
OK
```

### Python compilation check

Command:

```powershell
python -m compileall -q src tests
```

Environment: Windows, Python 3.14.3

Exit code: `0`

Result: all current Python source and tests compiled without syntax errors.

### Pre-commit diff validation

Command:

```powershell
git diff --cached --check
```

Final exit code: `0`

Breadcrumb: the first run exited `2` and identified trailing blank lines in 19
new files. Only those formatting defects were removed; the structural tests and
compilation check were then rerun and remained successful.

### GitHub repository

- URL: `https://github.com/sstangkh73/formula-ultimate`
- Visibility: `PRIVATE`
- Remote: `origin`
- Initial branch: `main`

The push and remote-branch verification are performed after this record is
included in the initial commit; Git history and the remote branch are the
authoritative evidence for that final step.

## Claims Supported

- The repository has an explicit, testable physics-system plan.
- The design-language assumptions and initial experimental controls are
  documented.
- The repository structure and work-log pairing pass automated checks.

## Claims Not Yet Supported

- Correctness of any vehicle, powertrain, tyre, thermal, or race simulation.
- Successful topology discovery.
- Performance against fixed EV, ICE, or hybrid baselines.
- Numerical convergence, real-world accuracy, manufacturability, or safety.

## Deviations from Plan

- The private GitHub repository was created before the initial local commit so
  its verified URL and visibility could be preserved in this result record.
  The initial commit is pushed only after final validation.
- No provisional numerical configuration was added because unvalidated default
  timesteps or tolerances would look more authoritative than the evidence
  supports.

## Known Limitations

- Current tests validate repository structure, not physics.
- GitHub Actions will provide independent CI evidence only after the first push.
- Component schemas, units layer, telemetry schema, and equations remain future
  implementation milestones.

## Recommended Next Work Item

Implement the Level-0 analytical reference kernel: explicit units and failure
types, constant-force acceleration, drag-only coast-down, road gradient, and
timestep-convergence tests. That work must begin with Work Plan 002.
