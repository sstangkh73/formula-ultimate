# Work 096 Plan: Semantic Geometry Witness V3

Thai companion: `2026-09-05_096_semantic-geometry-witness-v3-plan.th.md`

## Status

Status: Completed

## Objective

Independently inspect every Work 092 STEP candidate in FreeCAD/OCCT and recover physics-relevant, face-order-invariant semantic evidence. Bind declared datums and region intent to geometric signatures rather than unstable face indices, while making bounded sampling and unsupported interpretation explicit.

## Scope and planned files

- `config/cad/semantic_geometry_witness_v3.json`
- `src/formula_ultimate/components/semantic_geometry_witness.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/inspect_semantic_geometry_witness_v3_freecad.py`
- `scripts/cad/compare_semantic_geometry_witness_v3.py`
- `tests/test_semantic_geometry_witness_v3.py`
- `docs/contracts/SEMANTIC_GEOMETRY_WITNESS_V3.md` and Thai companion
- this plan/result and Thai companions
- ignored FreeCAD/replay/negative-control evidence under `artifacts/work096/`

## Independent/dependent variables and controls

- Independent inputs: exact Work 092 manifest/STEP identities, declared density, datum declarations, semantic region declarations, axis/path rule, section/thickness sample fractions, curvature sampling rule, sweep rule, and comparison tolerances.
- Dependent outputs: imported solid/shell/body counts; validity; volume; mass; centre of mass; full geometric/mass inertia and principal axes; axis-aligned and principal-oriented bounds; curvature class/area spectrum and sampled curvature radii; sampled material-span thickness field; section area/equivalent radius/second-moment proxy evolution; datums; signature-selected support/load/contact/thermal/fluid regions; path length/bend evidence; static clearance/interference and swept envelope; declaration/report identities; and residuals.
- Controls: mapping-key and face-record permutation; harmless report record ordering; changed STEP/interface/region signature; missing datum or region; ambiguous signature; report hash mutation; non-finite measurement; hidden repair; changed sampling protocol; and replay mutation.

## Bounded measurement definitions

- FreeCAD imports exact STEP bytes using `Part.Shape.read` without healing or mutation.
- Mass equals imported volume times declared synthetic density. The complete OCCT inertia tensor and deterministic principal decomposition are retained.
- Principal-oriented bounds project all imported vertices onto the measured inertia axes. Axis sign is canonicalized; near-degenerate axes are reported rather than claimed unique.
- Curvature spectra use surface class, face area, and finite `Face.curvatureAt` samples at fixed interior parameter fractions. Radius is `1/|curvature|` only above the declared zero-curvature tolerance.
- Thickness is a deterministic sampled material-span witness: exact B-rep intersections of axis-aligned probe lines at frozen grid fractions. It is not a guaranteed global minimum wall thickness.
- Section evolution uses thin exact B-rep slabs normal to the declared longest-bounds path. Area is slab-intersection volume divided by slab thickness; equivalent radius and centroidal second-moment proxy are derived from that sampled area/bounds.
- Region signatures use datum-relative extreme planes, surface class, normal alignment, centroid, area, and bounding signature. No face ordinal enters identity.
- Clearance/interference and swept envelope are self/static bounded witnesses for the single imported candidate. Assembly-pair clearance and arbitrary motion remain unsupported until typed mates exist.

## Success criteria

- All ten Work 092 STEP candidates, including the declared four-solid member, import validly and emit every mandatory V3 evidence section.
- Every declared datum and support/load/contact/thermal/fluid region matches exactly one independently inspected signature; altered or missing/ambiguous semantics fail closed.
- Curved, hollow/shell, branching/ribbed, rotary/hub, and multi-body families all produce finite bounded measurements with limitations recorded.
- Face/record permutation preserves semantic comparison identity; same clean FreeCAD rerun reproduces the complete report/comparison SHA-256.
- Focused tests, compilation, repository contracts, FreeCAD run/replay, negative controls, and full regression pass.

## Risks and explicit non-goals

Sampled thickness and section fields may miss local extrema; B-spline curvature depends on fixed sampling; inertia axes can be non-unique for symmetric bodies; region intent is bounded to declared datum-relative signatures; and static self-clearance is not assembly clearance. Passing proves exact inspection of this corpus, not structural validity, arbitrary future geometry support, manufacturability, contact behavior, motion safety, or physical validation. Work 097 owns generalized evaluation and convergence benchmarks.
