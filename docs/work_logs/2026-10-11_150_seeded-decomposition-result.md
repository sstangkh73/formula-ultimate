# Work 150 Result: Seed-Driven Abstract Decomposition

Thai companion: `2026-10-11_150_seeded-decomposition-result.th.md`

Date: 2026-10-11

Plan: `2026-10-11_150_seeded-decomposition-plan.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/decomposition.py` (new)
- `tests/test_hierarchy_decomposition.py` (new, 12 tests)
- `docs/work_logs/2026-10-11_150_seeded-decomposition-{plan,result}{,.th}.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## What was built

- `DecompositionConfig` declares every constraint (leaf budget 170 to 230,
  minimum 150 leaves, 4 levels, capability height 2 and 5 leaves, branching
  2 to 5, maximum depth 7, merge probability 0.3, root length 4.0 m, anchor
  scale 0.55 to 0.85, satellite scale 0.12 to 0.45, leaf length floor
  0.004 m, leaf size ratio 100, at most 64 attempts).
- `decompose(seed, config)`: `random.Random(seed * 1000003 + attempt)` only.
  Capabilities are shuffled and grouped singly or in merged pairs; each group
  gets a weighted leaf budget; every budget is split recursively by a uniform
  random composition (a capability group never splits into leaves only, so
  its height is at least 2). Each assembly's anchor is its largest-budget
  child. Every non-anchor child gets an abstract attachment from its anchor
  leaf to a seed-chosen leaf of the anchor subtree, with a seed-chosen joint
  kind. Attempts that miss a constraint are rejected; the accepted attempt
  index is stored. The root carries no capability.
- `constraint_violations`, `levels`, `leaves`, `subtree_height`,
  `subtree_leaf_count`, `topology_signature` (acceptance definition),
  `config_sha256`.

## Decisions

- Written by Claude, not Codex: the design choices (anchor rule, budget
  partition, rejection search) needed the whole goal context, and the module
  is short.
- Characteristic lengths are planning targets for later geometry; the
  acceptance size ratio is measured from meshes and is not proven here.
- Leaves carry no functions; sub-assemblies inherit their group's functions.

## Validation

1. `python -m unittest tests.test_hierarchy_decomposition -v`: exit 0,
   `Ran 12 tests`, `OK`.
2. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 PASS; Gate 2
   `Ran 1065 tests`, `OK (skipped=11)`; Gate 3 FAILED 13/13 because
   `scripts/hierarchy/generate_hierarchical_vehicle.py` does not exist yet
   (expected).

Sweep evidence (seeds 0 to 39 plus 11, 23, 37): 175 to 229 leaves, 7 to 8
levels, planned leaf length ratio 103 to 277, accepted at attempt 0 to 2,
maximum fan-out 12 (at the depth limit).

## Limitations

- No geometry, masses or interfaces with measured contact yet.
- Fan-out at the depth limit can reach about 12 children, which geometry
  placement must accommodate.
- Diversity across seeds is topological only; usefulness is not measured.

## Follow-up

- Milestone 3: realize leaf geometry from the abstract tree with the existing
  free-form grammar and CadQuery, export STL in metres, and measure mass from
  the mesh.
