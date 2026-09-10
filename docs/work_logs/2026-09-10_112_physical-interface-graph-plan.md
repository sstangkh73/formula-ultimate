# Work 112 Plan: Physical Interface Graph

Thai companion: `2026-09-10_112_physical-interface-graph-plan.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a bounded, typed physical-interface multigraph bound to actual Work 108 material/void regions. Preserve terminal frames, physical domains, variables, units, direction, terminal roles, owner grouping, parallel interactions, allowed motion and constitutive-law references under identifier-only renaming.

The admitted corpus covers mechanical force, motion and thermal exchange without assigning conventional vehicle-component roles. It validates compatibility and conservation fixtures, transfers unambiguous bindings across declared split/merge maps, and emits evidence-invalidation events for changed, ambiguous or missing bindings.

## Variables, controls and files

- IV: terminal roles/orientations, edge direction and multiplicity, owner grouping, identifier names, split/merge mappings.
- DV: canonical identity, connected components, compatibility, exchange residual and invalidation events.
- Controls: identifier-only rename equivalence; source/sink swap, parallel-edge deletion, owner regrouping and disconnected paths as distinctions; incompatible units, missing surfaces and rigid/moving conflicts as fail-closed cases.
- Success: all equivalence/distinction fixtures pass, multiedges persist, conservation residuals meet the frozen tolerance, replay is exact and oversize identity returns unresolved rather than a name-derived fallback.

Planned files: `src/formula_ultimate/assembly/physical_interface_graph.py`, `config/development/physical_interface_graph_v1.json`, `scripts/development/run_physical_interface_graph.py`, `tests/test_physical_interface_graph.py`, bilingual `docs/contracts/PHYSICAL_INTERFACE_GRAPH_V1*`, this bilingual plan/result and ignored `artifacts/work112/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_physical_interface_graph tests.test_repository_contract -v
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_a
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_b --replay-reference artifacts/work112/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected regressions, `git diff --check`, explicit staging, cached-scope inspection and `git diff --cached --check`; commit immediately if all gates pass.

## Risks and non-goals

Exact canonicalization grows factorially, so the terminal bound is frozen and oversize graphs remain explicitly unresolved. Frame fixtures are declared semantic evidence, not geometric contact proof. Non-goals: general mechanism discovery, contact mechanics, solver-field prediction, physical validation, dependency installation, push or history rewrite.
