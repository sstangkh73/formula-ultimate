# Work 151 Result: Leaf Geometry Realization

Thai companion: `2026-10-11_151_leaf-geometry-realization-result.th.md`

Date: 2026-10-11

Status: Completed

Plan: `2026-10-11_151_leaf-geometry-realization-plan.md`

## Files changed

- `src/formula_ultimate/hierarchy/leaf_geometry.py` (new): `leaf_program`,
  `placement_transforms`, `with_placement`, `transform_points`,
  `validate_leaf_program`, `program_sha256`, `stl_bytes`, `read_binary_stl`,
  `closure_problems`, `volume_and_centroid`, `box_fill_fraction`,
  `measure_mesh`.
- `scripts/hierarchy/leaf_realization.py` (new): `build_shape`,
  `tessellate_m`, `realize_leaf` and a small CLI.
- `tests/test_hierarchy_leaf_geometry.py` (new, 9 tests).
- This plan/result pair, `auto-loop/progress.md`, `auto-loop/progress.th.md`.

## Decisions

- A leaf is a Work 091-style star-shaped profile (closed polyline of 5..11
  vertices or periodic B-spline through 6..12 points, jittered angles, radii
  0.62..1.0 of a radius of 0.22..0.5 L) extruded straight along local +z by
  0.12..0.9 L. The flat end caps are the planar contact faces for later
  placement. The program records `contact.height_m`,
  `contact.inscribed_radius_m` (exact polygon in-radius; for B-splines
  `0.8 * min radius * cos(pi/n)`) and `contact.outer_radius_m`.
- Execution reuses `execute_candidate` (Work 092) and therefore `execute_loop`
  (Work 091) unchanged. The corpus-level validators are not called because
  they validate whole corpora (>= 10 candidates, >= 12 profiles);
  `validate_leaf_program` checks the exact subset leaf programs use.
- Placement is part of the program (Work 092 `transform` features), so the
  program fully determines the placed mesh and its hash. `transform_points`
  reproduces it in pure Python for layout planning.
- The STL is written by our own deterministic binary writer (fixed header,
  float32 vertices, computed normals). Mass and centre of mass are measured
  from the re-read float32 triangles with the same formulas as the acceptance
  suite; nothing is repaired.

## Validation

| Command | Exit | Output |
|---|---|---|
| `.tools/cadquery-mcp/Scripts/python.exe artifacts/work151/probe.py 600` (exploratory, gitignored) | 0 | `fails 0 time 18.9 fill max 0.8575 diag/L 0.442 .. 1.502` |
| `python -m unittest tests.test_hierarchy_leaf_geometry -v` | 0 | `Ran 9 tests ... OK` |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1074 tests`, `OK (skipped=11)`; Gate 3 13/13 FAIL (generator missing, expected) |

The first focused run failed one check: the placement bounding-box comparison
used a float32-only bound, but the placed shape is tessellated afresh, so the
difference is bounded by the declared linear tolerance (2e-3 L). The bound was
corrected to `2e-3 * L + 1e-6` m (observed 1.9e-6 m at L = 0.03 m).

## Evidence

- 600 random leaves (L from 0.004 to 4 m, random axis, flip, spin and
  translation) all exported as closed, consistently oriented meshes in 18.9 s
  total; maximum box-fill 0.858 (< 0.999); bounding-box diagonal 0.44..1.50 L.
- Cap vertices stay within `[inscribed, outer]` radii for the tested leaves;
  the same program gives byte-identical STL bytes.

## Limitations

- Side faces deviate from the exact surface by up to the linear tolerance, so
  contact must use the flat caps, not side faces.
- The B-spline inscribed radius is a declared margin, verified only on the
  tested cases, not proven.
- Only one shape family (straight extrusion) so far; other Work 092 operators
  (loft, revolve, sweep, bore) are not yet used.
- Materials and density are inputs; catalog selection is later work.
- No physical validation.

## Follow-up

- Milestone 4: placement of subtrees with flat-cap contacts and no
  interpenetration (AABB-disjoint layout; the acceptance check only tests
  pairs whose boxes overlap by more than the tolerance).
