# Constrained Free-Form Wire Grammar V2

Thai companion: `FREEFORM_WIRE_GRAMMAR_V2.th.md`

## Purpose and claim boundary

`constrained_freeform_wire_grammar_v2` is a bounded, deterministic language for agent-generated planar profiles in SI metres and radians. The declaration validator is `src/formula_ultimate/components/freeform_wire_grammar.py`, the CadQuery executor is `scripts/cad/generate_freeform_wire_corpus.py`, the independent STEP witness is `scripts/cad/inspect_freeform_wire_corpus_freecad.py`, and the admitted corpus is `config/cad/freeform_wire_grammar_v2.json`.

Passing this contract establishes only that the exact declarations produce valid closed planar faces in the pinned CAD kernels, satisfy the declared geometric constraints, survive STEP transfer, and replay deterministically. It is not evidence of a useful vehicle component, a 3D solid, material or manufacturing feasibility, structural adequacy, assembly compatibility, aerodynamic value, thermal safety, or physical validation.

## Exact declaration and bounds

The root contains exactly `grammar_version`, `units`, `limits`, and `profiles`. Each profile declares an identity, a non-prescriptive family label, ordered loops, ordered transforms, one offset policy, and geometric constraints. It has exactly one first `outer` loop and may have bounded `hole` loops. Every loop and segment has a stable identity. Unknown fields, units, operators, malformed identities, non-finite numbers, out-of-bound coordinates, excessive segment/point/loop counts, or open endpoints fail closed.

V2 accepts fully determined geometry only. It has no iterative constraint solver and does not infer missing dimensions, tangencies, closure, or topology. Lengths are metres at the contract boundary and are converted exactly once to the millimetre convention of the CAD kernels. Angles are radians.

Declared limits are:

- closure and bounding-box absolute tolerance: `1e-7 m`;
- independent area/perimeter measurement relative tolerance: `0.002` (`0.2%`);
- minimum feature: `1e-5 m`;
- maximum coordinate magnitude: `1.0 m`;
- maximum offset magnitude: `0.02 m`;
- at most 32 points per segment, 16 segments per loop, and 4 loops per profile.

The `0.2%` measurement tolerance is solely an interoperability bound for CadQuery-versus-FreeCAD length/area algorithms. It does not relax wire closure, hole nesting, bounding boxes, validity, or topology, and it performs no repair. The successful corpus records the actual maximum residuals.

## Segment operators

| Operator | V2 behavior |
|---|---|
| `line` | One finite start-to-end edge; nontrivial parameter trim is admitted only here |
| `polyline` | Explicitly closed ordered points with no zero/sub-tolerance edge or proper self-intersection |
| `tangent_arc` | Arc from declared start, nonzero tangent vector, and end |
| `three_point_arc` | Arc through non-collinear start, intermediate, and end points |
| `circle` | Closed circle from centre and positive radius |
| `ellipse` | Closed ellipse from centre, two positive radii, and rotation |
| `bezier` | Quadratic or cubic Bezier from exactly three or four control points |
| `bspline` | Degree `2..5`, bounded control-point list, and explicit periodic flag |

Closed primitives and periodic splines must be the sole segment in their loop. Other segments must meet in declaration order within `1e-7 m`, including the last-to-first junction.

## Transforms, offset, and constraints

Transforms execute in declared order: translation by a 2D SI vector, rotation around the local origin, and mirror about local `x` or `y`. Offset distance is bounded and uses explicit `arc`, `intersection`, or `tangent` join behavior. V2 rejects any offset that changes the expected single-wire topology.

Every profile declares at least one of `positive_area`, `minimum_perimeter`, `hole_count`, or `symmetric_axis`. The executor independently constructs each hole as a face, proves it is fully contained in the outer face, rejects overlapping holes, then creates exactly one positive-area face. It never moves, shrinks, heals, or drops a hole to obtain validity.

## Corpus and evidence

The admitted corpus contains 12 profiles from 9 family labels and causally covers all eight segment operators, all three transforms, all four constraint kinds, one nontrivial trim, one nonzero polygon offset, curved profiles, and an annulus. Each output records face/wire/edge counts, curved-edge count, area, perimeter, optimal geometry-derived bounds, and exact canonicalized STEP SHA-256.

FreeCAD imports each exact STEP file, checks the file identity and validity, and writes an `.FCStd` witness. Agreement is exact for face/wire/edge topology; bounds use the strict absolute tolerance; area/perimeter use the declared relative interoperability tolerance. Display-triangulation bounds are prohibited: FreeCAD uses `optimalBoundingBox(False, False)` to match the geometry-derived CadQuery calculation.

Run and replay with:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_freeform_wire_corpus.py `
  --config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work091\run_d `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"

& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_freeform_wire_corpus.py `
  --config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work091\run_e `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work091\run_d\result.json
```

The output root must be absent or empty. STEP timestamps alone are normalized to `1970-01-01T00:00:00`; geometry and other STEP content are unchanged. Replay requires complete result equality and therefore identical declaration, manifest, independent witness, and every STEP identity.

## Limitations and next work

This grammar is deliberately two-dimensional and bounded. It cannot yet express general NURBS knot/weight vectors, solver-driven dimensional constraints, surface patches, lofts, sweeps, guide rails, variable sections, shell/thickness fields, topology mutation, or semantic interfaces. The family labels are coverage labels, not conventional component prescriptions. Work 092 may consume these profiles for constrained 3D loft/sweep generation, but it must add its own validity, self-intersection, thickness, and independent solid-witness gates.
