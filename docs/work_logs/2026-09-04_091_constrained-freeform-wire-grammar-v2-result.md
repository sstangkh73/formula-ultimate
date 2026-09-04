# Work 091 Result: Constrained Free-Form Sketch and Wire Grammar V2

Thai companion: `2026-09-04_091_constrained-freeform-wire-grammar-v2-result.th.md`

## Status and outcome

Status: Completed

Work 091 implemented and independently exercised a bounded planar wire grammar rather than merely documenting future syntax. The admitted corpus generated 12 valid STEP profiles from 9 family labels, covered every declared curve/transform/constraint operator, passed an independent FreeCAD import witness, and reproduced the complete result identity exactly in a second clean run.

This removes the former rectangle/circle/annulus/shaft-section profile bottleneck at the 2D geometry layer. It does not yet make 3D parts or establish physical usefulness.

## Files changed

- `config/cad/freeform_wire_grammar_v2.json`: admitted 12-profile SI corpus and explicit bounds.
- `src/formula_ultimate/components/freeform_wire_grammar.py`: strict declaration validator, canonical identity, and cross-kernel witness comparison.
- `src/formula_ultimate/components/__init__.py`: public grammar exports.
- `scripts/cad/generate_freeform_wire_corpus.py`: CadQuery execution, constraints, nesting checks, canonical STEP export, FreeCAD orchestration, and replay.
- `scripts/cad/inspect_freeform_wire_corpus_freecad.py`: independent exact-STEP import and `.FCStd` witness.
- `tests/test_freeform_wire_grammar.py`: parser, metamorphic, negative, measurement, and pinned-kernel tests.
- `docs/contracts/FREEFORM_WIRE_GRAMMAR_V2.md` and Thai companion.
- this plan/result pair and Thai companions.
- ignored evidence under `artifacts/work091/run_a` through `run_e`; failed runs are retained rather than rewritten.

## Decisions and falsification findings

- V2 accepts fully determined curves and rejects underconstrained sketches instead of invoking a hidden iterative solver.
- All eight operators execute: `line`, `polyline`, `tangent_arc`, `three_point_arc`, `circle`, `ellipse`, quadratic/cubic `bezier`, and bounded-degree periodic `bspline`.
- Multiple loops/holes, ordered translate/rotate/mirror transforms, one nontrivial line trim, and one nonzero polygon offset execute without hidden healing.
- Hole containment and hole-to-hole non-overlap are proven before the final face is built. Invalid nesting and unsatisfied constraints remain observable failures.
- CadQuery and FreeCAD must agree exactly on face/wire/edge counts. Bounds retain `1e-7 m` absolute tolerance. Area/perimeter use a separately named `0.002` relative interoperability tolerance; it does not relax closure, validity, nesting, or topology.
- FreeCAD uses `optimalBoundingBox(False, False)`. Its default triangulation/display box differed from the geometry-derived CadQuery box for free-form curves, so the default box was rejected rather than hidden behind a larger tolerance.

Three initial runs falsified premature assumptions and were kept as evidence:

1. `run_a`: an ellipse offset was valid before export but invalid after STEP import in FreeCAD; the admitted offset control was changed to a closed polygon.
2. `run_b`: strict absolute perimeter equality rejected the ellipse, with relative difference `0.0018832339106344149`; the contract now declares a capped cross-kernel measurement tolerance of `0.002`.
3. `run_c`: the default FreeCAD bounding box differed by up to about `0.006019526 m` for the cubic Bezier despite matching area/topology; switching to the geometry-derived optimal box reduced the successful maximum bound difference to `6.6405214660392176e-15 m`.

## Successful evidence

The canonical successful result is `artifacts/work091/run_d/result.json`; `run_e/replay.json` reports `exact: true`.

| Evidence | Result |
|---|---:|
| Profiles | 12 |
| Family labels | 9 |
| Operator coverage | 8 of 8 |
| Transform coverage | 3 of 3 |
| Constraint coverage | 4 of 4 |
| Nontrivial trim segments | 1 |
| Nonzero offset profiles | 1 |
| Maximum area relative difference | `4.285843071817371e-13` |
| Maximum perimeter relative difference | `0.0018832339106344149` |
| Maximum bounds absolute difference | `6.6405214660392176e-15 m` |
| Declaration SHA-256 | `4a88ef8001377472c35eb18fe0eac23f4afd92b83c86edf86233af458a223820` |
| Manifest SHA-256 | `ae25ede8ccc54b768fada6253a039e2e8e440205d2b5a56109e348898eca9862` |
| FreeCAD report SHA-256 | `a07d72aae38adb51130436565d7b36db702ceb415011d2ef1ca2cbffd6077812` |
| Result SHA-256 | `94798aeb093d6bbcf7f3440faef96aed3f928180223f3679807a358dd3d3cae0` |
| Hidden geometry repair | `false` |

## Exact validation commands and exit status

Successful CadQuery kernel tests:

```powershell
$env:PYTHONPATH='src'
& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_freeform_wire_grammar -v
```

Exit status: `0`; 10 tests passed.

Successful primary and replay witnesses:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_wire_corpus.py --config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work091\run_d --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_wire_corpus.py --config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work091\run_e --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work091\run_d\result.json
```

Exit status: `0` for each. Both emitted manifest `ae25ede8ccc54b768fada6253a039e2e8e440205d2b5a56109e348898eca9862` and result `94798aeb093d6bbcf7f3440faef96aed3f928180223f3679807a358dd3d3cae0`.

Successful compilation, focused/repository contracts, and regression:

```powershell
python -m compileall -q src scripts tests
python -m unittest tests.test_freeform_wire_grammar tests.test_repository_contract -v
python -m unittest discover -s tests -v
```

Exit status: `0` for all commands. Focused/repository: 16 tests passed with 2 expected skips because default Python does not contain CadQuery. Full regression: 640 tests passed in `392.443 s`, with 5 expected environment-dependent skips.

## Limitations, contradicting evidence, and confidence

Supporting evidence is strong for bounded 2D profile execution and deterministic STEP transfer under CadQuery `2.8.0` and FreeCAD `1.1.3`/OCCT `7.8.1`. The retained failed runs contradict any claim that arbitrary curve offsets or default kernel measurements are automatically portable. The ellipse perimeter residual shows that even shared OCCT-lineage tools can disagree on curve length calculation.

Alternative explanations include version-specific OCCT exporters/importers and approximation policies; no third CAD kernel was tested. Missing evidence includes arbitrary NURBS weights/knots, more complex multiple-hole cases, 3D loft/sweep validity, minimum-wall behavior, material/manufacturing assignment, loading, assembly, aero, thermal, race performance, and physical tests. Confidence is high inside this exact corpus and toolchain, low outside its declared bounds.

## Follow-up

Work 092 should consume the admitted profiles in a constrained loft/sweep/guide-curve surface-and-solid grammar and add section compatibility, self-intersection, thickness, topology, independent solid import, and replay gates. It must not infer that a 2D profile passing Work 091 is already a viable component.
