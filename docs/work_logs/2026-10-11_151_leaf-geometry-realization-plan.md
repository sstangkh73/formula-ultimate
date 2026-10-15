# Work 151 Plan: Leaf Geometry Realization

Thai companion: `2026-10-11_151_leaf-geometry-realization-plan.th.md`

Date: 2026-10-11

Status: Completed

## Objective

Milestone 3(a) of `auto-loop/GOAL.md`: turn one abstract leaf into a recorded
free-form program, execute it through the existing Work 091/092 grammar
executors under CadQuery, export a closed binary STL in metres, and measure
mass and centre of mass from the exported mesh (not from the CAD kernel).

## Scope

- New pure-Python module `src/formula_ultimate/hierarchy/leaf_geometry.py`:
  - `leaf_program(rng, characteristic_length_m, placement)` that returns a
    program dict made of a Work 091-style profile (one outer loop: a closed
    polyline or a periodic B-spline, star-shaped around the origin with a
    declared inscribed radius) and a Work 092-style candidate
    (`section -> extrude` along +z, then `transform` features for placement),
    plus tessellation tolerances. The extrusion has flat end faces at local
    `z = 0` and `z = h` for later planar contact;
  - `validate_leaf_program(program)` with exact field sets and bounds;
  - binary STL writer/reader, closure check, signed volume and centroid, and
    `measure_mesh(triangles, density)` returning mass and centre of mass.
- New CadQuery script module `scripts/hierarchy/leaf_realization.py`:
  `realize_leaf(program, stl_path)` reusing `execute_loop`
  (`scripts/cad/generate_freeform_wire_corpus.py`) and `execute_candidate`
  (`scripts/cad/generate_freeform_solid_corpus.py`), scaling mm to m,
  tessellating with the declared tolerances, writing a deterministic binary
  STL, and rejecting meshes that are not closed and consistently oriented.
- New tests `tests/test_hierarchy_leaf_geometry.py`: pure tests under `python`
  and a CadQuery round trip run through the pinned CAD interpreter in a
  subprocess (skipped when the interpreter is absent).

## Planned files

- `src/formula_ultimate/hierarchy/leaf_geometry.py` (new)
- `scripts/hierarchy/__init__.py`, `scripts/hierarchy/leaf_realization.py` (new)
- `tests/test_hierarchy_leaf_geometry.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_leaf_geometry -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gates 1 and 2 must pass;
   Gate 3 still fails because the generator does not exist yet).

## Success criteria

- Programs for lengths from 0.004 m to 4 m build, export and re-read as
  closed, consistently oriented meshes with positive volume.
- The exported bounding-box diagonal is within a declared factor of the
  characteristic length; the box-fill fraction is below 0.999.
- Mass equals mesh volume times density exactly as computed from the float32
  STL; the same program gives byte-identical STL bytes twice.
- `program_sha256` is the canonical-JSON SHA-256 of the program.

## Risks

- OpenCascade tessellation might not share boundary nodes exactly between
  faces after float32 rounding; this is checked and fails loudly, never
  repaired silently.
- Very small parts may give degenerate float32 triangles.

## Non-goals

- No placement search, interfaces, materials, manifest or generator CLI.
- No physical validation of any part.
