# Work 096 Result: Semantic Geometry Witness V3

Thai companion: `2026-09-05_096_semantic-geometry-witness-v3-result.th.md`

## Status and outcome

Status: Completed

Work 096 independently imported and inspected all ten exact Work 092 STEP candidates with FreeCAD `1.1.3` / OCCT `7.8.1`. It recovered mandatory bounded semantic sections without face ordinals, including the four-solid candidate. Two clean runs produced byte-identical reports and the same normalized semantic comparison SHA-256.

This proves deterministic semantic inspection for the frozen corpus. It does not prove structural validity, global minimum thickness, assembly clearance, manufacturability, safety, or physical validity.

## Files changed

- `config/cad/semantic_geometry_witness_v3.json`
- `src/formula_ultimate/components/semantic_geometry_witness.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/inspect_semantic_geometry_witness_v3_freecad.py`
- `scripts/cad/compare_semantic_geometry_witness_v3.py`
- `tests/test_semantic_geometry_witness_v3.py`
- `docs/contracts/SEMANTIC_GEOMETRY_WITNESS_V3.md` and Thai companion
- this plan/result and Thai companions
- ignored retained evidence under `artifacts/work096/run_a` and `run_b`

## Decisions and evidence

- Exact source manifest and STEP SHA-256 identities are checked before import. Import uses `Part.Shape.read_step_no_repair`; hidden repair remains false.
- A compound has no shape-level inertia property in this FreeCAD API. V3 therefore combines each solid's geometric inertia about the aggregate centre with the parallel-axis theorem. This keeps the four-solid member rather than excluding it.
- Body/solid/shell count, volume, area, declared-density mass, centre of mass, full inertia, principal moments/axes, axis degeneracy, axis-aligned bounds, and tessellated principal-oriented bounds are retained.
- The report contains 139 order-independent face signatures and 417 fixed-parameter curvature samples. Curvature class/area/radius spectra are independently recomputed by the comparator.
- Thickness probes use exact B-rep line/face intersections at 27 global grid lines plus three centre lines per solid. Material intervals are selected by midpoint containment. The observed minimum sampled span range is `0.00030120991794767293–0.015805462099021627 m`; these are not guaranteed global wall minima.
- Section evolution uses exact thin-slab intersection volume. Zero section area remains an output for paths that cross empty space; it is not filled or repaired.
- Support/load/contact/thermal/fluid region identities hash sorted face-signature sets selected by declared geometric rules. Candidate, face, datum, and region record permutations preserve normalized semantic comparison identity.
- The four-solid member reports six internal solid pairs, minimum clearance `0.035443617196894 m`, and zero measured pairwise interference volume.
- The strengthened comparator recomputes mass/inertia consistency, curvature spectra, datum/region correspondence, thickness minima, section/path correspondence, clearance pair count, and static swept-envelope volume.

## Identity evidence

- Config SHA-256: `b6233a5a8e07a74b77c4e59bf6e5164b01d7f4d954bfb3fa230724f51b31c41a`
- FreeCAD report SHA-256: `96cf848f1dc1482be4b408eb146c36cca324f71b21c74a4b5b5de243412c6c08`
- Report-file SHA-256, both runs: `97e2259c1cf230c8be8e0f37c244c419c34db86afba41505ef5da87bd6e2ba2a`
- Normalized comparison SHA-256: `731ba8b6c167f36703a278da959cf8f586714262995c811ede38b2892599cf7d`
- Candidate count: `10`; `hidden_geometry_repair: false`; `structural_validity: false`

## Exact validation commands

```powershell
$env:PYTHONPATH='C:\Program Files\FreeCAD 1.1\bin'
$env:FORMULA_ULTIMATE_W096_CONFIG=(Resolve-Path 'config/cad/semantic_geometry_witness_v3.json').Path
$env:FORMULA_ULTIMATE_W096_MANIFEST=(Resolve-Path 'artifacts/work092/run_g/manifest.json').Path
$env:FORMULA_ULTIMATE_W096_SOURCE_ROOT=(Resolve-Path 'artifacts/work092/run_g').Path
$env:FORMULA_ULTIMATE_W096_OUTPUT=(Join-Path (Resolve-Path 'artifacts/work096/run_a').Path 'report.json')
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' 'scripts/cad/inspect_semantic_geometry_witness_v3_freecad.py'
# exit 0; 10 candidates measured

python scripts/cad/compare_semantic_geometry_witness_v3.py --config config/cad/semantic_geometry_witness_v3.json --report artifacts/work096/run_a/report.json --output artifacts/work096/run_a/comparison_strict.json
# exit 0; comparison passed

# The same FreeCAD command with W096_OUTPUT under run_b, then:
python scripts/cad/compare_semantic_geometry_witness_v3.py --config config/cad/semantic_geometry_witness_v3.json --report artifacts/work096/run_b/report.json --output artifacts/work096/run_b/comparison.json --replay-reference artifacts/work096/run_a/comparison.json
# exit 0; report JSON exact=true and file SHA-256 identical

python -m unittest tests.test_semantic_geometry_witness_v3 tests.test_repository_contract -q
# exit 0; 14 tests passed

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; 680 tests passed in 341.326 s; 7 expected environment-dependent skips
```

## Limitations and follow-up

The thickness field is sampled, B-spline curvature is sampled at fixed parameter fractions, and section second moment is a bounding proxy. Principal axes may be non-unique for symmetric geometry. Region semantics are geometric selection rules rather than physical boundary-condition evidence. Clearance is only between solids inside one imported candidate and the swept envelope is static identity motion. Work 097 must now exercise unfamiliar geometry families through declared model selection, meshing, contact/failure controls, convergence, and independent residual gates.
