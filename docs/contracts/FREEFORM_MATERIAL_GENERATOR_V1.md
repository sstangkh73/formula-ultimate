# Free-Form Material Generator V1

Thai companion: `FREEFORM_MATERIAL_GENERATOR_V1.th.md`

Status: Implemented by Work 109 for a bounded Cartesian field.

## Claim boundary

This contract permits material/void occupancy and topology to change without selecting a named part or target silhouette. Passing establishes deterministic geometry coverage inside the registered grid, operator and budget bounds. It does not establish functional benefit, smooth-CAD equivalence, physical feasibility, manufacturing or physical validation.

## Representation and dependency

The source is a finite Cartesian cell field in metres. Each occupied cell has exactly one scalar material label; absence is void. Domain, resolution, minimum feature, material vocabulary, maximum occupied cells, maximum changed cells per edit and maximum surface triangles are frozen. Work 109 pins the Work 108 commit and English spatial-contract SHA-256; stale dependency evidence fails closed.

The admitted domain is `[-0.12, 0.12] m` on each axis. The main resolution is `0.01 m`; refinement evidence uses `0.02`, `0.01` and `0.008 m`. These levels measure representation sensitivity, not physical convergence.

## Causal operators and accounting

The registered operators are `boundary_displacement`, `cavity_route`, `branch`, `split`, `merge` and `material_redistribution`. Every slot has a fixed seed and parameters. A mutation records before/after geometry identities and changed-cell cost. No-op edits, invalid materials, non-finite geometry, zero-length paths and budget overflow fail visibly.

Geometry identity hashes sorted cell coordinates plus material labels; case names are excluded. Renaming without changed occupancy/material therefore cannot be promoted as novelty. The source retains a tagged asymmetric thin feature, and the admitted chain requires at least `0.8` of its original cells to remain.

## Surface adapter and topology

Every exterior cell face becomes two consistently oriented OBJ triangles. Shared vertices are canonical. Every edge must have exactly two incident triangles; edge-only contacts that create a non-manifold boundary are rejected, never healed. Signed triangle volume must equal occupied cell volume within `1e-10` relative error.

Occupied and enclosed-void components use six-neighbour flood fill. The boundary Euler characteristic and connected surface count derive total genus. The admitted controls require a through-hole to change genus `0 -> 1`, its fill to return `1 -> 0`, a split to change occupied components `1 -> 2`, and a merge to return `2 -> 1`.

## Evidence and handoff

`result.json` retains the registered protocol/dependency identities, all snapshots, operator ancestry, cell/triangle counts, surface residuals, refinement trials, unsupported adapters, negative controls, resource counts and scientific review. A second clean run must reproduce `result_sha256` exactly.

Work 110 may convert only admitted field/surface artifacts and must preserve material/void identity while measuring mesh approximation. Smooth B-rep conversion, mixed-cell homogenization, fields below the cell scale and all physical claims remain unsupported in V1.
