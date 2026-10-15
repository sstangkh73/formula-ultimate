# Work 150 Plan: Seed-Driven Abstract Decomposition

Thai companion: `2026-10-11_150_seeded-decomposition-plan.th.md`

Date: 2026-10-11

Status: Completed

## Objective

Milestone 2 of `auto-loop/GOAL.md`: a seed-driven decomposition procedure
that builds an abstract hierarchy (no geometry) covering the nine
capabilities of `REQUIRED_CAPABILITIES`, without any conventional part
catalogue. Later work items realize leaf geometry and interfaces from it.

## Scope

- New module `src/formula_ultimate/hierarchy/decomposition.py`:
  - `DecompositionConfig` (frozen) with declared constraints: total leaf
    budget range, minimum levels, per-capability minimum height and leaves,
    branching range, maximum depth, capability merge probability, root
    characteristic length (m), child scale-fraction ranges, minimum leaf size
    ratio, maximum search attempts;
  - `decompose(seed, config)` that uses only `random.Random` seeded from
    `(seed, attempt)`: groups capabilities (single or merged pairs), allocates
    a leaf budget per group, recursively partitions each budget into 2..k
    children (one anchor child per assembly), assigns characteristic lengths
    from declared scale fractions, and declares abstract attachments (each
    non-anchor child's anchor leaf to the anchor child's anchor leaf) with a
    seed-chosen joint kind. Attempts that miss a declared constraint are
    rejected and the next attempt is tried; the accepted attempt index is
    recorded;
  - `config_sha256(config)` via `canonical_sha256`;
  - an abstract-tree validator and metrics (levels, leaves, subtree height,
    topology signature with the acceptance definition).
- New tests `tests/test_hierarchy_decomposition.py`.

## Planned files

- `src/formula_ultimate/hierarchy/decomposition.py` (new)
- `tests/test_hierarchy_decomposition.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_decomposition -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gates 1 and 2 must pass;
   Gate 3 still fails because the generator does not exist yet).

## Success criteria

- For seeds 11, 23, 37 and a sweep of other seeds: >= 4 levels, >= 150
  leaves, each capability named by an assembly of height >= 2 with >= 5
  leaves, leaf characteristic-length ratio >= 100, every assembly with >= 2
  children connected by attachments.
- Seeds 11, 23, 37 give pairwise different whole-tree signatures and every
  capability has >= 2 distinct signature sets across them.
- Same seed gives an identical tree; the root carries no capability so it
  cannot satisfy the capability criterion by itself.
- No seed-specific branches in code. Gates 1 and 2 pass.

## Risks

- Characteristic lengths are planning targets, not measured geometry; the
  acceptance size ratio is measured from meshes later and may differ.
- The rejection search could loop for long; bounded by `max_attempts` with an
  explicit error.

## Non-goals

- No geometry, CadQuery, STL, masses, materials or generator CLI.
- No claim that a decomposition is physically useful.
