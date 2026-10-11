# Work 149 Plan: Hierarchical Part-Tree Data Model

Thai companion: `2026-10-11_149_hierarchical-part-tree-model-plan.th.md`

Date: 2026-10-11

Status: Completed

## Objective

Milestone 1 of `auto-loop/GOAL.md`: a pure-Python recursive part-tree data
model with validation, mass and centre-of-mass roll-up, and manifest
serialization. Later work items (decomposition, CadQuery leaf geometry,
interfaces, generator CLI) build on it.

## Scope

- New package `src/formula_ultimate/hierarchy/` with `part_tree.py`:
  - frozen dataclasses for a part (leaf) node, an assembly node, an interface
    and the whole tree;
  - `canonical_sha256` with the exact canonical JSON the acceptance suite uses;
  - `validate_part_tree` that raises `PartTreeViolation` for: duplicate ids,
    unknown children, more than one parent, cycles, unreachable nodes, a
    non-assembly or missing root, empty assemblies, non-finite or
    non-positive mass/density, interface endpoints that are not leaves,
    self-interfaces, unknown joint kinds, `interference_m` on a non-interference
    joint or outside `(0, 1e-4]` m, contact tolerance outside `(0, 5e-4]` m,
    and a mismatched program hash;
  - `roll_up` that computes assembly mass (sum) and centre of mass
    (mass-weighted) bottom-up from leaves;
  - structural metrics: levels, leaf count, subtree height, leaf set, and a
    topology signature matching the acceptance definition;
  - `to_manifest` producing the node and interface lists with exactly the
    field sets the goal contract defines.
- New test file `tests/test_hierarchy_part_tree.py`.

## Planned files

- `src/formula_ultimate/hierarchy/__init__.py` (new)
- `src/formula_ultimate/hierarchy/part_tree.py` (new)
- `tests/test_hierarchy_part_tree.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_part_tree -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gates 1 and 2 must pass;
   Gate 3 is expected to still fail because no generator exists yet).

## Success criteria

- Focused tests pass, including negative tests for every violation listed.
- Gates 1 and 2 pass.

## Risks

- The model could drift from the acceptance contract. Mitigation: field sets
  and constants are taken directly from `auto-loop/GOAL.md`.
- Floating-point roll-up must match the acceptance tolerances (mass 1e-9
  relative, centre of mass 1e-5 m). Use plain float sums in child order.

## Non-goals

- No geometry, no CadQuery, no STL, no decomposition procedure, no generator
  CLI. No physical validation claim of any kind.
- No material values; the model stores whatever density it is given.
