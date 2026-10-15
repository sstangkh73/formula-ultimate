# Work 149 Result: Hierarchical Part-Tree Data Model

Thai companion: `2026-10-11_149_hierarchical-part-tree-model-result.th.md`

Plan: `2026-10-11_149_hierarchical-part-tree-model-plan.md`

Date: 2026-10-11

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/__init__.py` (new)
- `src/formula_ultimate/hierarchy/part_tree.py` (new)
- `tests/test_hierarchy_part_tree.py` (new, 11 tests)
- `docs/work_logs/2026-10-11_149_hierarchical-part-tree-model-{plan,result}{,.th}.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## What was built

- Frozen dataclasses `PartNode`, `AssemblyNode`, `Interface`, `PartTree`.
- `validate_part_tree` raises `PartTreeViolation` for every case listed in the
  plan (ids, parents, cycles, reachability, numeric fields, mesh paths,
  programs, functions, contact tolerance in `(0, 5e-4]` m, joint kinds,
  `interference_m` in `(0, 1e-4]` m and only on interference joints).
- `roll_up`: assembly mass is the sum of child masses and the centre of mass is
  mass-weighted, both in child order. All traversals are iterative; a
  3000-level chain is tested.
- Metrics `levels`, `leaf_ids`, `subtree_height`, `subtree_leaves`, and
  `topology_signature`, which uses the same definition as the acceptance suite.
- `to_manifest_nodes` and `to_manifest_interfaces` emit exactly the field sets
  from `auto-loop/GOAL.md`.

## Who did it

Codex wrote the module and tests from a precise specification. Claude
reviewed the full diff. Codex also created four misnumbered work-log files
(`2026-10-11_148_hierarchy-part-tree-*`). Claude deleted them because they
duplicated this record, and they were never committed.

## Validation

| Command | Exit | Output |
|---|---|---|
| `python -m unittest tests.test_hierarchy_part_tree -v` | 0 | `Ran 11 tests in 0.036s`, `OK` |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 (Gate 3) | Gate 1 `PASS`; Gate 2 `Ran 1053 tests in 337.261s`, `OK (skipped=11)`; Gate 3 13 failures, all `missing: scripts/hierarchy/generate_hierarchical_vehicle.py` (expected) |

## Limitations

- This is a representation model only. It has no geometry, no meshes, and no
  physical validation.
- The metric helpers re-validate the tree on every call, which costs O(n) each
  time. That is fine for about 10^3 nodes. Batch helpers may be needed later.
- `PartNode.program` is stored by reference. Callers must not mutate it after
  construction.

## Follow-up

Next: Milestone 2, a seed-driven decomposition procedure over the nine
capabilities that produces an abstract `PartTree` skeleton (no geometry)
without any conventional part catalogue.
