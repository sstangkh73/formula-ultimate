# STEP to FreeCAD Geometry Witness V2

Thai companion: `STEP_FREECAD_GEOMETRY_WITNESS_V2.th.md`

## Purpose and authority

Work 081 re-imports the exact five canonical Work 078 STEP files through FreeCAD `Part.Shape.read`, performs no healing or substitution, and measures geometry in SI units. The frozen declaration is `config/cad/step_freecad_geometry_witness_v2.json`; the extractor is `scripts/cad/inspect_geometry_witness_v2_freecad.py`; and the fail-closed comparator is `scripts/cad/compare_geometry_witness_v2.py` backed by `src/formula_ultimate/components/geometry_witness.py`.

The admitted run used CadQuery `2.8.0` to reproduce the frozen STEP bytes and FreeCAD `1.1.3` / OCCT `7.8.1` to import them. Because both routes can share OCCT technology, the evidence class is `toolchain_cross_check`, not physical validation.

## Exact identities and measured properties

The source manifest identity is `fff5c0c74513fae1a2bc7cd55020affbbaf67bdd6e9c0908f5aa2ea4131b2448`. Each imported artifact must retain its exact SHA-256, contain exactly one valid solid, and report `hidden_geometry_repair=false`.

| Part | STEP SHA-256 prefix | FreeCAD volume (m3) | Synthetic-density mass (kg) | Centre of mass (m) |
|---|---|---:|---:|---|
| `shaft_001` | `34e81618e3cd` | `7.936733407181677e-05` | `0.2142918019939053` | `[-8.5441e-17, -6.9764e-19, 0.06595183958570189]` |
| `bracket_001` | `b06e3141f7a1` | `8.144352220392336e-05` | `0.21989750995059307` | `[0.0004628865601941557, 1.2298e-20, 0.005828531482650844]` |
| `hollow_housing_001` | `ef92f5215e56` | `0.0001304688570501225` | `0.35226591403533075` | `[-0.00046848910750642053, -8.5948e-19, 0.03272660375475765]` |
| `ribbed_plate_001` | `af73c6492c9c` | `9.9164928734969e-05` | `0.26774530758441634` | `[-3.5072e-17, -0.0009113784760267323, 0.006314811066097798]` |
| `hub_like_001` | `8b3ff2186103` | `0.0001451118244934476` | `0.3918019261323085` | `[1.5696e-15, 8.2571e-16, 0.014999999999999993]` |

Mass is a conversion of measured volume using the explicit Work 079 synthetic density `2700 kg/m3`. It is not a measured or sourced material mass and cannot support design use. The report also records the full geometric inertia tensor, converted mass inertia tensor, and principal moments/axes. The comparator verifies finiteness, symmetry, density scaling, trace preservation, and orthonormal principal axes.

## Interface recovery without face numbers

STEP face ordering is not treated as persistent identity. Each semantic interface uses a cylindrical-surface signature containing radius, canonical unsigned axis, closest axis point to the world origin, and axial bounds. The extractor hashes measured surface content, and the comparator requires exactly one match within the frozen radius, position, axial, and angular tolerances.

The admitted witnesses are the shaft bearing surface, bracket through hole, housing through bore, ribbed-plate relief hole, and hub central bore. All five recovered uniquely. A missing match and two matching surfaces fail with different causal codes.

FreeCAD's ordinary bounding box over-bounded the filleted shaft after STEP import. V2 therefore preregisters and uses FreeCAD's `optimalBoundingBox(True, False)` for the comparison. This changes only the measurement method; it does not alter the imported shape. All five optimal bounds match exporter evidence within the `1e-9 m + 1e-6 relative` gate, and all volume residuals are below `1.31e-13` relative.

## Reproduction

First regenerate the exact STEP corpus with the pinned CadQuery environment:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_brep_feature_corpus.py `
  --config config\cad\brep_feature_grammar_v1.json `
  --output-root artifacts\work081\source_step `
  --manifest artifacts\work081\source_manifest.json
```

Set `FORMULA_ULTIMATE_W081_CONFIG`, `FORMULA_ULTIMATE_W081_SOURCE_MANIFEST`, `FORMULA_ULTIMATE_W081_SOURCE_ROOT`, and `FORMULA_ULTIMATE_W081_OUTPUT`, then execute the extractor with `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe`. Paths containing spaces may require their Windows short-path form for the script argument. Compare with:

```powershell
python scripts\cad\compare_geometry_witness_v2.py `
  --config config\cad\step_freecad_geometry_witness_v2.json `
  --report artifacts\work081\run_a\freecad_report.json `
  --output artifacts\work081\run_a\comparison.json
python -m unittest tests.test_geometry_witness_v2 -v
```

## Controls, limitations, and next gate

Controls reject changed STEP/source-manifest identities, invalid or multiple solids, hidden repair, volume/bounds/mass/inertia drift, non-finite data, missing/ambiguous/tampered surface signatures, and changed limitation lists. Key-order permutation preserves canonical identities, while two independent FreeCAD/comparison runs produce byte-identical reports.

V2 does not solve arbitrary global minimum wall thickness, exact section torsion constants, part-to-part collision/interference, moving assembly clearance, material identification, process capability, strength, fatigue, safety, or manufacturability. These unsupported values remain explicit per part. Work 079's material and process records remain synthetic, so `design_use_allowed=false`. Work 082 may use this result only for software-coupling verification until a separate evidence-remediation work supplies sourced material/process evidence and complete independent manufacturing measurements.
