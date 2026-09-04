# Work 092 Result: Free-Form B-rep Solid Grammar V2

Thai companion: `2026-09-04_092_freeform-brep-solid-grammar-v2-result.th.md`

## Status and outcome

Status: Completed

Work 092 implemented a strict feature-DAG solid grammar and executed 10 non-primitive candidates from Work 091 profiles. All 18 admitted operators ran causally. CadQuery and independent FreeCAD inspection agreed on exact topology and bounded measurements/datums, and the complete result replayed exactly.

This is the first project milestone that produces varied curved, lofted, swept, hollow, treated, and multi-body B-rep geometry. It is geometry evidence only, not functional discovery or physical validation.

## Files changed

- `config/cad/freeform_brep_solid_grammar_v2.json`
- `src/formula_ultimate/components/freeform_solid_grammar.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/generate_freeform_solid_corpus.py`
- `scripts/cad/inspect_freeform_solid_corpus_freecad.py`
- `tests/test_freeform_solid_grammar.py`
- `docs/contracts/FREEFORM_BREP_SOLID_GRAMMAR_V2.md` and Thai companion
- this plan/result and Thai companions
- ignored retained evidence under `artifacts/work092/run_a` through `run_h`

## Decisions and falsification

- Feature inputs may reference only earlier typed states; final body count is an exact declaration.
- Empty/invalid intermediates, disconnected undeclared bodies, missing selectors, and shell self-erasure fail visibly.
- Fillet/chamfer use axis-parallel geometric signatures; shell opening uses an extreme-face signature. Raw edge/face indices are prohibited.
- Datums are declarations plus geometry-derived values, independently recomputed after STEP rather than copied from CadQuery measurements.
- `run_b` falsified the assumption that the final revolved intersection was a single body: it produced four disconnected bodies. The grammar now declares `expected_body_count: 4` and verifies it exactly; no auto-fuse occurred.
- `run_d` showed that exact floating-point datum JSON equality was too strict despite position residuals near `1e-15 m`. The comparison now preserves exact datum identity/kind and applies the declared `1e-7 m` coordinate tolerance.

## Successful evidence

Canonical evidence is `artifacts/work092/run_g`; `run_h/replay.json` reports `exact: true`.

| Evidence | Result |
|---|---:|
| Candidates / families | 10 / 10 |
| Operator coverage | 18 / 18 |
| Maximum volume relative difference | `2.9726979210197703e-09` |
| Maximum area relative difference | `3.935383817517682e-10` |
| Maximum position/datum difference | `1.413570801210573e-11 m` |
| Declaration SHA-256 | `a0e1c47ee15dbebac9dce2183a502c26199197b751fe427c74c2824dd1b4ad8a` |
| Manifest SHA-256 | `369750f5ebef5a72dcd63147cec251a9a88d3d05a289d68289d6a9cd501a90ea` |
| FreeCAD report SHA-256 | `bf211fd926730d5fcb9db9be9bd2db0a50b7834364677fb64091e3bb9125aff7` |
| Result SHA-256 | `2f3fd3fceb5be7df82eecf73f15802fe5a219fc251ed62c466a77ca5dcde4ac9` |
| Hidden geometry repair | `false` |

## Exact validation commands

```powershell
$env:PYTHONPATH='src'
& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_freeform_solid_grammar -v
# exit 0; 7 tests passed

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py --config config\cad\freeform_brep_solid_grammar_v2.json --wire-config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work092\run_g --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'
# exit 0

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py --config config\cad\freeform_brep_solid_grammar_v2.json --wire-config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work092\run_h --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work092\run_g\result.json
# exit 0; exact true

python -m compileall -q src scripts tests
python -m unittest tests.test_freeform_solid_grammar tests.test_repository_contract -v
python -m unittest discover -s tests -q
# exit 0; focused/repository 13 passed with 2 expected skips; full 647 passed in 396.855 s with 7 expected skips
```

## Limitations and follow-up

The corpus is strong evidence for the exact bounded CAD language under CadQuery `2.8.0` and FreeCAD `1.1.3`/OCCT `7.8.1`. It does not prove arbitrary loft/sweep robustness, manufacturing access, wall quality, structural strength, interfaces, or function. The four-body member is explicitly multi-body and not a connected part. Work 093 must now represent mutable typed part/interface/feature/path topology; Work 094 must mutate it reproducibly before any discovery claim.
