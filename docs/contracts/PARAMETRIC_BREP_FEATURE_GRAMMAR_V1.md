# Parametric B-rep Feature Grammar V1

Thai companion: `PARAMETRIC_BREP_FEATURE_GRAMMAR_V1.th.md`

## Purpose and authority

`parametric_brep_feature_grammar_v1` is a bounded agent-facing language for creating real single-part B-rep solids in SI units. The declaration validator is `src/formula_ultimate/components/brep_grammar.py`; the pinned CadQuery/OCCT executor is `scripts/cad/generate_brep_feature_corpus.py`; and the admitted corpus is `config/cad/brep_feature_grammar_v1.json`.

Passing this contract means only that the exact declaration is bounded, all V1 operators execute in the tested corpus, each required final part is one valid positive-volume solid, and canonical STEP replay is stable under the pinned toolchain. It is not material, manufacturing, structural, assembly, thermal, or physical validation.

## Declaration topology

The root requires exactly `grammar_version` and `candidates`. Each candidate requires `candidate_id`, one admitted `family`, ordered `features`, and `final_feature_id`. Each feature requires exactly `feature_id`, `operator`, `inputs`, and `parameters`. Inputs may reference only earlier features; sketch profiles take zero inputs, booleans take two, and every other operator takes one.

Five families are mandatory: `shaft`, `bracket`, `hollow_housing`, `ribbed_plate`, and `hub_like_rotating_part`. All operator identities below must appear in the admitted corpus.

## V1 operators

| Operator | Bounded behavior |
|---|---|
| `sketch_profile` | Rectangle, circle, annulus, or axial shaft-section profile on a declared local plane convention |
| `extrude` | Positive-distance linear solid from rectangle/circle/annulus |
| `revolve` | Positive angle through at most `2*pi`; V1 executes an axial shaft section |
| `pocket_cut` | Bounded rectangular partial-depth cut that may not erase or split the blank |
| `through_hole` | Geometry-derived full-height cylindrical subtraction |
| `stepped_bore` | Through bore plus larger, shallower counterbore |
| `shaft_shoulder` | Coaxial bounded cylinder fused onto a shaft |
| `rib_web` | Bounded prismatic rib tool located in the part frame |
| `shell_wall` | Inward constant wall thickness with declared top opening |
| `linear_pattern` | `2..64` translated copies along `x`, `y`, or `z` |
| `circular_pattern` | `2..64` rotated copies around local `z` within a positive declared angle |
| `fillet_chamfer` | Bounded fillet or chamfer over declared vertical or circular edge selection |
| `boolean_union` | Exact OCCT union; no implicit gap closing |
| `boolean_subtract` | Exact OCCT subtraction; an empty result fails |
| `boolean_intersect` | Exact OCCT intersection; an empty result fails |

Length parameters use metres and are converted exactly once to the CadQuery millimetre kernel convention. Angles use radians and counts are integers in `[2, 64]`. Positive dimensions are bounded at `5 m`; coordinates are finite with magnitude at most `5 m`. Unknown fields, parameter names, units, profiles, selectors, directions, modes, operators, families, or ancestry fail closed.

## Kernel-state rules

Every executed non-profile feature must return a valid, non-empty, finite positive-volume OCCT shape. A representation-only `Compound` containing exactly one solid is unwrapped; multiple solids are never auto-fused or repaired. The candidate final feature must contain exactly one solid. Boolean self-erasure and a disconnected pattern used as a final part are explicit negative controls.

The executor records every feature ID/operator/status/solid count. It exports the exact final shape to STEP, replaces only the volatile `FILE_NAME` timestamp with `1970-01-01T00:00:00`, then hashes the exact bytes. It does not rename faces, heal invalid solids, close gaps, change parameters, or select a fallback feature.

## Admitted corpus and replay

The corpus causally exercises the operator set across:

- a revolved shaft with a shoulder and bounded edge treatment;
- an extruded bracket with a partial pocket, through hole, and chamfer;
- an extruded cylindrical housing with inward shell and offset stepped bore;
- an extruded plate with rib seed, linear pattern, union, subtract, and intersect;
- an annular hub with a lug seed, circular pattern, and union.

Run two independent witnesses with:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_brep_feature_corpus.py `
  --config config\cad\brep_feature_grammar_v1.json `
  --output-root artifacts\work078\run_a\step `
  --manifest artifacts\work078\run_a\manifest.json
```

Repeat with `run_b` and compare `manifest_sha256` plus every `step_sha256`. Output paths are excluded from the canonical manifest payload; STEP base filenames remain identical.

## Claim boundary and limitations

The V1 family names are test fixtures, not required future vehicle architecture. The grammar does not prescribe wheel count, suspension form, powertrain technology, body form, or known component shapes. It is intentionally bounded and cannot yet express freeform splines, lofts/sweeps, complex datum transforms, arbitrary edge queries, threads/gears, sheet-metal process history, composites, topology optimization fields, or persistent STEP semantic signatures.

CadQuery and STEP export share OCCT technology, so successful replay is toolchain evidence rather than an independent geometric truth source. Work 079 adds material/manufacturing contracts; Work 081 must independently inspect exact STEP artifacts and recover interfaces by geometry signatures/datums rather than face numbers.
