# Work 092 Plan: Free-Form B-rep Solid Grammar V2

Thai companion: `2026-09-04_092_freeform-brep-solid-grammar-v2-plan.th.md`

## Status

Status: Completed

## Objective

Implement a bounded, deterministic solid grammar that consumes admitted Work 091 planar profiles and declared three-dimensional paths/sections to create genuine OCCT B-rep solids rather than opaque or decorative meshes. The corpus must demonstrate at least ten non-primitive solids, including a curved branch, tapered hollow duct, lofted rotary member, organic-like load bridge, and variable-section shell.

Passing Work 092 establishes geometry execution and independent STEP survival only. It does not establish topology search, manufacturing feasibility, structural adequacy, functional usefulness, or physical validation.

## Scope and planned files

- `config/cad/freeform_brep_solid_grammar_v2.json`
- `src/formula_ultimate/components/freeform_solid_grammar.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/generate_freeform_solid_corpus.py`
- `scripts/cad/inspect_freeform_solid_corpus_freecad.py`
- `tests/test_freeform_solid_grammar.py`
- `docs/contracts/FREEFORM_BREP_SOLID_GRAMMAR_V2.md` and Thai companion
- this plan/result and Thai companions
- ignored STEP/manifest/FreeCAD/replay evidence under `artifacts/work092/`

## Independent and dependent variables

- Independent inputs: Work 091 profile identity, operator DAG, local axes/datums, section scale/rotation/translation, 3D path control points, wall/pocket/bore/rib dimensions, transform parameters, boolean ancestry, and declared SI bounds.
- Dependent outputs: solid/body/face/edge counts, validity, volume, area, centre of mass, bounds, curved-face evidence, recovered datum signatures, STEP identity, FreeCAD residuals, and replay equality.
- Controls: simple extrude as a reference; invalid ancestry, missing profile, non-finite/out-of-range value, zero path, incompatible loft sections, shell self-erasure, disconnected union, empty intersection/subtraction, unstable selector, invalid multi-body declaration, altered datum, and unknown field as failures.
- Metamorphic controls: declaration key ordering preserves identity; a section/path/control-point mutation changes genotype and exported geometry identity.

## Grammar and execution boundary

- Admit bounded extrude/revolve, straight or curved sweep, multi-section loft, taper/variable section, shell-by-boolean, rib/web, gusset, pocket, bore, local pattern, signature-selected fillet/chamfer, union/subtract/intersect, local transforms, and derived datum point/axis/plane declarations.
- Feature inputs may reference earlier features only. Each operation must expose invalid, empty, disconnected, non-finite, or multi-solid outcomes unless the declaration explicitly permits a multi-body result.
- Edge treatment selectors must use geometric signatures and deterministic tie-breaking; raw edge indices are prohibited.
- Datums are verified after STEP from measurable geometry/bounds rather than trusted from volatile face numbering or display metadata.
- No voxel, STL, triangle-mesh, silent healing, fallback primitive, or result-conditioned repair is permitted.

## Validation and success criteria

- At least ten corpus members, all valid in CadQuery and after independent FreeCAD STEP import.
- Required named families are present: curved branch, tapered hollow duct, lofted rotary member, organic-like load bridge, and variable-section shell.
- The corpus causally executes all admitted V2 operator families and includes both single-feature ancestry and multi-feature booleans.
- Each non-multi-body corpus member contains exactly one positive-volume solid; any admitted multi-body member must declare and reproduce its exact body count.
- FreeCAD agrees on body/solid topology, volume, centre of mass, geometry-derived bounds, and datum signatures within declared tolerances.
- Two clean runs reproduce exact canonical STEP hashes, manifest identity, and result identity.
- Pinned CadQuery kernel tests, default-Python parser tests, repository contracts, compilation, and full regression pass.

## Risks and explicit non-goals

Lofts can twist through section correspondence, sweeps can self-intersect at tight curvature, booleans can create slivers or multiple solids, shell subtraction can erase a body, and fillet selection can become ambiguous. These must remain visible failures. Work 092 does not implement search-space mutation, manufacturing admission, automatic meshing, FEA/contact, flow/thermal evaluation, subsystem discovery, whole-vehicle integration, or a claim that curved appearance is functional novelty.
