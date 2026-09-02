# Work 079 Result: Engineering Material and Manufacturing Contract

Status: Completed

Thai companion: `2026-09-02_079_engineering-material-manufacturing-contract-result.th.md`

## Outcome and files changed

Implemented hash-addressed `engineering_material_v1`, `manufacturing_process_v1`, and `manufacturing_geometry_witness_v1` contracts plus exact assignment binding. The contracts require SI material properties, evidence/source/domain/confidence, explicit fatigue-evidence status, internally consistent elastic constants, process-limit evidence, geometry measurement evidence, causal manufacturing margins, and fail-closed identity checks.

The canonical material, process, and geometry measurements are synthetic verification fixtures. They pass contract logic but return `design_use_allowed=false`, `production_use_allowed=false`, measurement evidence `synthetic`, and fatigue evidence `missing`. No real material, supplier capability, independent STEP measurement, fatigue life, or manufacturability claim is admitted.

Changed files are the Work 079 plan/result pairs; `docs/contracts/ENGINEERING_MATERIAL_MANUFACTURING_CONTRACT_V1.md` and Thai companion; `config/materials/engineering_material_manufacturing_v1.json`; `src/formula_ultimate/components/engineering_contracts.py`; component exports; `scripts/components/validate_engineering_contracts.py`; and `tests/test_engineering_contracts.py`.

## Decisions and evidence

- `E`, `G`, and `nu` obey `G=E/(2*(1+nu))`; the fixture relative residual is `1.4495849609375002e-16` against tolerance `1e-12`.
- Yield cannot exceed ultimate strength; fracture and thermal fields are required; every required property/limit maps to existing source evidence.
- Fatigue is explicitly `missing`; no neutral or inferred S-N curve is created.
- A floating `maximum_force_n`, wrong unit field, `NaN`, negative property, impossible Poisson ratio, inconsistent elasticity, invalid strength ordering, missing source, unsupported fatigue claim, and stale assignment hash all fail closed.
- Walls, holes, ligaments, webs, internal/bend radii, tool direction/clearance/depth ratio, tolerance, and unsupported features each have distinct causal rejection codes. Geometry is never clipped or repaired.
- Measurement evidence is a separate identity. The fixture states `declared Work 079 gate fixture; not extracted from STEP`, preventing the Work 078 geometry hash alone from being mistaken for independent measurements.

The passing synthetic witness margins are wall `0.006 m`, hole `0.006 m`, ligament `0.003 m`, web `0.0035 m`, internal radius `0.001 m`, bend radius `0.001 m`, tolerance `0.0001 m`, tool clearance `0.005 m`, and depth/diameter-ratio margin `6.0`.

## Deterministic identities

```text
material_record_sha256=72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097
process_record_sha256=76837d5d53dd678f7aac3dc1869e099726b91d66023cda970e4fb753a6253558
geometry_sha256=b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89
manufacturing_report_sha256=3f4cdc35c1e50c652a164c471683fb3d446b0e30765106552d4fbb60f6ccc87e
result_sha256=a949bbe856ae5062094c3ce86dae1216641f268b58df3c41f081dbf5453a4052
evidence_file_sha256=3AEF84E5331552A98BA0033B7A66527D513D71BBF4A689B6EF5F6A487B2AC595
```

## Exact validation record

```text
python -m unittest tests.test_engineering_contracts -v
Exit: 0
Ran 8 tests in 0.007s — OK

python scripts\components\validate_engineering_contracts.py --config config\materials\engineering_material_manufacturing_v1.json --output artifacts\work079\run_a\evidence.json
Exit: 0; status=passed; design_use_allowed=false

python -m unittest tests.test_engineering_contracts tests.test_repository_contract -q
Exit: 0
Ran 14 tests in 0.657s — OK

python -m compileall -q src scripts\components tests\test_engineering_contracts.py
Exit: 0

runner replay to artifacts\work079\run_b\evidence.json plus SHA-256 comparison
Exit: 0; byte-identical
evidence_sha256=3AEF84E5331552A98BA0033B7A66527D513D71BBF4A689B6EF5F6A487B2AC595

python -m unittest discover -s tests -q
Exit: 0
Ran 504 tests in 291.653s — OK (skipped=3 CadQuery-only tests)
```

The three skipped CadQuery tests were executed and passed in Work 078's pinned CadQuery environment. Work 079 introduces no CadQuery-only test.

## Falsification, alternative explanations, and confidence

All preregistered record and process controls rejected. Eleven manufacturing mutations localized wall, hole, ligament, web, internal radius, bend radius, tool direction, tool clearance, depth ratio, tolerance, and unsupported-feature causes. This supports the contract logic but does not support the fixture's physical values.

Contradicting/missing evidence is explicit: the material/process limits are synthetic; fatigue data is absent; measurement arrays were not independently extracted from STEP. An exact geometry hash prevents substitution of another STEP file but cannot prove the declared measurements are correct. Alternative explanations for passing include hand-selected fixture margins and internally consistent invented properties.

Confidence is high for the tested schema, arithmetic, causal codes, identity binding, and replay. Confidence is intentionally absent for real material response, process capability, and the bracket's actual measured dimensions.

## Limitations and follow-up

Before design use, a later work must import real coupon/handbook/test evidence with conditions and uncertainty, independently extract manufacturing measurements from the exact STEP artifact, and preserve those report hashes. Work 081 owns independent geometry measurement; Work 082 owns mesh/load/material coupling. Work 079 does not validate plasticity, fracture propagation, fatigue life, thermal duration, manufacturability, structural safety, or physical performance.
