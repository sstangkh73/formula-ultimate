# Free-Form B-rep Solid Grammar V2

Thai companion: `FREEFORM_BREP_SOLID_GRAMMAR_V2.th.md`

## Purpose and authority

`freeform_brep_solid_grammar_v2` is the bounded Work 092 language for turning exact Work 091 profiles plus declared paths and feature ancestry into OCCT B-rep solids. The validator is `src/formula_ultimate/components/freeform_solid_grammar.py`; the CadQuery executor is `scripts/cad/generate_freeform_solid_corpus.py`; the independent STEP witness is `scripts/cad/inspect_freeform_solid_corpus_freecad.py`; and the admitted corpus is `config/cad/freeform_brep_solid_grammar_v2.json`.

Passing means geometry execution, exact declared body count, STEP survival, bounded independent measurements, datum recovery, and deterministic replay for the exact corpus. It is not manufacturing, load, fatigue, flow, thermal, race, or physical validation and is not topology discovery.

## Typed feature DAG

Every candidate declares `candidate_id`, a non-prescriptive coverage `family`, exact `expected_body_count`, ordered `features`, `final_feature_id`, and derived datums. A feature has a stable ID, operator, earlier inputs, and exact parameters. Unknown fields/operators, forward references, incompatible input kinds, missing Work 091 profiles, non-finite values, excessive dimensions, zero paths, invalid body count, or missing required datum kinds fail before CAD.

The source Work 091 declaration is pinned by SHA-256. Sections refer to those profiles and may apply bounded scale, local `z` rotation, and 3D translation. Paths are declared polylines or splines. Lengths are metres and angles radians at the contract boundary; the executor converts once to the kernel's millimetres/degrees.

## Admitted operators

- construction: `section`, `path`, `extrude` with taper, arbitrary-axis `revolve`, curved/straight `sweep`, and multi-section `loft`;
- modification: geometry-signature `shell`, `rib_web`, `gusset`, `pocket`, `bore`, fused or explicit-body `linear_pattern`, signature-selected `fillet`, and `chamfer`;
- composition: `boolean_union`, `boolean_subtract`, `boolean_intersect`, and deterministic `transform`.

Raw edge numbers are prohibited. Fillet/chamfer choose line edges parallel to a declared local axis and fail when the signature selects nothing. Shells choose geometry-extreme faces and reject thickness at or above half the minimum body span before the kernel can construct an unintended result. Empty/invalid/non-finite intermediate geometry fails. Final solid count must equal `expected_body_count`; disconnected bodies are never silently fused.

## Datums and independent witness

Each candidate declares exactly recoverable geometry-derived datum kinds: bounding-box centre, longest bounding-box axis, and a declared minimum/maximum plane on `x`, `y`, or `z`. CadQuery measures these from its geometry-derived optimal box. FreeCAD independently imports the exact canonical STEP and recomputes the same datums with `optimalBoundingBox(False, False)`. Datum identity/kind/direction and all coordinates are compared within `1e-7 m`; face/edge/solid counts are exact.

Volume and surface-area comparisons use a capped relative tolerance of `0.002`. This is a cross-kernel measurement allowance only; it does not repair shape, change topology, or relax body validity. `hidden_geometry_repair` is always `false`.

## Admitted corpus and replay

The 10-candidate corpus covers all 18 admitted operators across curved branch, tapered hollow duct, lofted rotary member, organic-like swept bridge, variable-section shell, tapered open shell, rib/gusset hybrid, bored/chamfered hub, fused/filleted pattern, and a declared four-body revolved intersection. The family labels are coverage labels, not required vehicle-component shapes.

Run two clean witnesses with:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py `
  --config config\cad\freeform_brep_solid_grammar_v2.json `
  --wire-config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work092\run_g `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py `
  --config config\cad\freeform_brep_solid_grammar_v2.json `
  --wire-config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work092\run_h `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work092\run_g\result.json
```

Only the STEP `FILE_NAME` timestamp is normalized. Replay demands complete result equality, including each STEP SHA-256, manifest, and independent FreeCAD report identity.

## Limitations

V2 does not provide general NURBS knots/weights, guide surfaces, persistent STEP product metadata, arbitrary topology-aware selectors, local thickness fields, lattice/mesh substitution, manufacturing construction, loads, meshing, or simulation. Datum recovery is deliberately limited to bounding geometry and does not yet identify arbitrary interface surfaces; Work 096 owns that stronger semantic witness. Work 093 adds a topology genome, but Work 092 by itself only proves a richer executable shape language.
