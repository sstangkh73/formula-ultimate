# Work 091 Plan: Constrained Free-Form Sketch and Wire Grammar V2

Thai companion: `2026-09-04_091_constrained-freeform-wire-grammar-v2-plan.th.md`

## Status

Status: Completed

## Objective

Implement a bounded agent-facing 2D wire grammar that removes the four-profile bottleneck measured by Work 090. The grammar must execute real line, polyline, tangent-arc, three-point-arc, circle, ellipse, quadratic/cubic Bezier, and degree-bounded B-spline geometry; support multiple loops/holes, deterministic trim/offset, and local transforms; and reject ambiguous or invalid profiles before Work 092 uses them to create solids.

The first version accepts only fully determined geometry and validates declared geometric constraints. It deliberately rejects underconstrained sketches instead of using a non-deterministic iterative sketch solver.

## Scope and planned files

- `config/cad/freeform_wire_grammar_v2.json`
- `src/formula_ultimate/components/freeform_wire_grammar.py`
- `scripts/cad/generate_freeform_wire_corpus.py`
- `scripts/cad/inspect_freeform_wire_corpus_freecad.py`
- `tests/test_freeform_wire_grammar.py`
- `docs/contracts/FREEFORM_WIRE_GRAMMAR_V2.md` and Thai companion
- this plan/result and Thai companions
- ignored STEP/manifest/FreeCAD witness evidence under `artifacts/work091/`

## Independent/dependent variables and controls

- Independent inputs: profile family, ordered segment operators/control points, loops/roles, transform list, trim fractions, offset distance/kind, constraints, SI bounds, and tolerance policy.
- Dependent outputs: closed-wire validity, edge/wire counts, planar area, perimeter, bounds, operator coverage, curved-edge count, STEP identity, FreeCAD witness, and replay equality.
- Negative controls: open loop, self-intersection, duplicate segment/loop identity, zero-length segment, invalid arc/tangent, degree/control-point mismatch, invalid hole nesting, excessive/sub-tolerance offset, non-finite values, unsupported operator, constraint failure, and unknown field.
- Metamorphic controls: declaration-key reordering preserves identity; a control-point mutation changes declaration and STEP identity.

## Validation and success criteria

- At least twelve profiles from at least six families.
- All declared operator families execute causally in the corpus, including nonzero trim and offset examples.
- Each profile forms one positive-area planar face with a closed outer loop and zero or more correctly nested hole loops.
- CadQuery and independent FreeCAD inspection agree on wire/edge count, bounds, area, and perimeter within declared tolerances.
- Two clean output roots reproduce identical canonical STEP files, manifests, and result identities.
- Focused, repository-contract, compilation, and full regression tests pass.

## Risks and explicit non-goals

B-spline/Bezier endpoint continuity, offset topology changes, STEP edge ordering, and tolerance sensitivity can make apparently simple profiles invalid. All such outcomes must be explicit; no hidden healing is allowed. This work creates planar profile/wire capability only. It does not create 3D solids, loft/sweep parts, topology mutation, physical evaluation, manufacturing admission, or discovery.
