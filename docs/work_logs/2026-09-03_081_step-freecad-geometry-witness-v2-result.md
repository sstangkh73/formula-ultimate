# Work 081 Result: STEP to FreeCAD Geometry Witness V2

Thai companion: `2026-09-03_081_step-freecad-geometry-witness-v2-result.th.md`

## Status and outcome

Status: Completed

FreeCAD `1.1.3` / OCCT `7.8.1` independently re-imported the exact five canonical Work 078 STEP byte streams. Every artifact retained its frozen SHA-256, imported as exactly one valid solid without reported repair, and yielded finite SI volume, optimal bounding box, centre of mass, full inertia tensor, principal moments, and principal axes. Five semantic cylindrical interfaces were recovered uniquely from geometry signatures without face indices.

The largest FreeCAD-to-CadQuery volume relative residual was `1.3037757588616636e-13`; the largest optimal-bound absolute error was `4.28129753871076e-15 m`. Both are inside the frozen `1e-6` relative and `1e-9 m` absolute gates. Two FreeCAD runs and two comparator runs were byte-identical.

The result is a `toolchain_cross_check`, not physical validation, because the two routes can share OCCT. The reported masses use the explicitly synthetic density `2700 kg/m3`; material and process evidence remain synthetic, so `design_use_allowed=false`.

## Files changed

- `config/cad/step_freecad_geometry_witness_v2.json`
- `src/formula_ultimate/components/geometry_witness.py`
- `scripts/cad/inspect_geometry_witness_v2_freecad.py`
- `scripts/cad/compare_geometry_witness_v2.py`
- `tests/test_geometry_witness_v2.py`
- `docs/contracts/STEP_FREECAD_GEOMETRY_WITNESS_V2.md` and Thai companion
- this result and its Thai companion
- the Work 081 plan and Thai companion, whose statuses changed to `Completed`

Generated STEP, manifest, FreeCAD JSON, and comparison evidence under `artifacts/work081/` is ignored and was not committed.

## Decisions and evidence review

- Exact source-manifest and per-STEP hashes are verified before import; changed identities fail before measurement is admitted.
- `Part.Shape.read` is used with no healing call. Shape validity and one-solid topology are measured after import.
- FreeCAD's ordinary bounding box over-bounded the filleted shaft (`about +/-0.021647844 m` versus the exporter `about +/-0.0200000001 m`). This contradicting method evidence was retained and resolved by preregistering FreeCAD's non-mutating `optimalBoundingBox(True, False)` for the admitted comparison; no geometry was modified.
- Full inertia evidence is derived from FreeCAD's solid matrix. The geometric `m5` tensor is multiplied by the declared density to obtain `kg m2`; the comparator verifies symmetry, finite/positive diagonals, density scaling, principal-value trace, and orthonormal axes.
- Interfaces use radius, canonical unsigned axis, closest axis point to the world origin, and axial bounds. Surface-content hashes are independent of transient face numbering.
- Unsupported arbitrary wall minima, section/torsion constants, moving-assembly collision, and manufacturing properties remain explicit rather than inferred.

Supporting evidence: five exact one-solid imports, five unique interfaces, maximum volume residual `1.3037757588616636e-13`, maximum bound error `4.28129753871076e-15 m`, and exact replay. Contradicting evidence: ordinary FreeCAD bounds were unsuitable for the shaft fillet and are not used for admission. Alternative explanation: agreement may result from shared OCCT; evidence is therefore not called independent physical truth. Missing evidence: sourced material/process properties, physical density/mass, arbitrary wall/section convergence, exact part-to-part interference, experimental comparison, and safety evidence. Confidence is high for exact byte identity and deterministic software measurement under the pinned local toolchain, low for any real-world design claim.

## Exact validation commands and results

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_brep_feature_corpus.py `
  --config config\cad\brep_feature_grammar_v1.json `
  --output-root artifacts\work081\source_step `
  --manifest artifacts\work081\source_manifest.json
# exit 0; 5 candidates; manifest_sha256=
# fff5c0c74513fae1a2bc7cd55020affbbaf67bdd6e9c0908f5aa2ea4131b2448

# With FORMULA_ULTIMATE_W081_CONFIG, _SOURCE_MANIFEST, _SOURCE_ROOT,
# and _OUTPUT set to the recorded paths; script path passed in 8.3 form:
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" `
  scripts\cad\inspect_geometry_witness_v2_freecad.py
# run_a exit 0; run_b exit 0; each measured 5 parts
# report_sha256=34ad809df13ba746352107e952e67a6d187795c96e1cb1096a6efc9a7ba28132

python scripts\cad\compare_geometry_witness_v2.py `
  --config config\cad\step_freecad_geometry_witness_v2.json `
  --report artifacts\work081\run_a\freecad_report.json `
  --output artifacts\work081\run_a\comparison.json
# run_a exit 0; run_b exit 0; comparison_sha256=
# 7ea916aff72334bd47ccf7b4af36f8c3c64674037e5532ce2e5a961d53cc13b7

Get-FileHash artifacts\work081\run_a\freecad_report.json -Algorithm SHA256
Get-FileHash artifacts\work081\run_b\freecad_report.json -Algorithm SHA256
# both 01bfecefb35931da8d92b53a048186550686e0bd82d5c71b4346f1b1edaad15c

Get-FileHash artifacts\work081\run_a\comparison.json -Algorithm SHA256
Get-FileHash artifacts\work081\run_b\comparison.json -Algorithm SHA256
# both 0e0238afcc24bbf72ca8d552b291fafc5071f6ef1d734b50983dad7544540ec0

python -m unittest tests.test_geometry_witness_v2 tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -v
# exit 0; Ran 524 tests in 300.239s; OK (skipped=3 pinned CadQuery-environment tests)
```

## Limitations and follow-up

Work 081 completes geometry import and global-property/interface witness tooling for the five canonical fixtures only. It does not complete the Work 081 evidence-remediation gate for design use because Work 079's material/process sources are synthetic and the fixtures do not support every arbitrary manufacturing measurement. A separately planned remediation is required before Work 082 can make real-part capacity claims; without it, Work 082 is limited to software-coupling verification.
