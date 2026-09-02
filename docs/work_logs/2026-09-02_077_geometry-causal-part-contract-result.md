# Work 077 Result: Geometry-Causal Part Contract V1

Status: Completed

Thai companion: `2026-09-02_077_geometry-causal-part-contract-result.th.md`

## Outcome and files changed

Implemented the fail-closed `geometry_causal_part_v1` declaration, canonical example, validator, component exports, eight focused tests, bilingual executable-contract documentation, and the Work 077-086 geometry-causal whole-vehicle roadmap. The roadmap records the requested three-work cadence as `077-079`, `080-082`, `083-085`, then `086`, while retaining a separate validated commit for every completed work.

Changed files are the Work 077 plan/result pairs; `docs/contracts/GEOMETRY_CAUSAL_PART_CONTRACT_V1.md` and Thai companion; `docs/reports/GEOMETRY_CAUSAL_WHOLE_VEHICLE_ROADMAP_V1.md` and Thai companion; `config/components/geometry_causal_part_contract_v1.json`; `src/formula_ultimate/components/part_contract.py`; component exports; `scripts/components/validate_part_contract.py`; and `tests/test_part_contract.py`.

## Decisions and experiment evidence

- Unknown and missing fields fail; the implementation does not strip or default them.
- Feature parameters require explicit admitted SI suffixes and finite values. Thickness, minimum feature size, and tolerances must be positive.
- Frames must be orthonormal and right-handed. Feature ancestry, identities, datum/interface references, and load-region paths are explicit.
- Every feature/tolerance parameter requires exactly one provenance record. Material and geometry-region evidence is hash-addressed.
- Canonical JSON sorts object keys but preserves causal array order. The reference declaration and recursively key-reordered control produced the same SHA-256.
- Passing admits only contract completeness and deterministic declaration. CAD validity, manufacturability, structural capacity, and physical validation remain prohibited claims.

The reference canonical byte count is `4319`; declaration SHA-256 is `8336bb69762d3263286db84e7e5435c7676a8df56fa73638c8f7839b930b0396`. The two runner evidence files were byte-identical with SHA-256 `825597A81E4E2DF37A1A7C49B6A7D37206752B7C2E0F38DEA387CDE709FFE03B`.

## Exact validation record

```text
python -m unittest tests.test_part_contract -v
Exit: 0
Ran 8 tests in 0.005s — OK

python scripts\components\validate_part_contract.py --config config\components\geometry_causal_part_contract_v1.json --output artifacts\work077\part_contract_evidence.json
Exit: 0
status=passed; canonical_byte_count=4319
declaration_sha256=8336bb69762d3263286db84e7e5435c7676a8df56fa73638c8f7839b930b0396

python -m unittest tests.test_part_contract tests.test_repository_contract -q
Exit: 0
Ran 14 tests in 3.275s — OK

python -m compileall -q src scripts\components tests\test_part_contract.py
Exit: 0

runner replay plus SHA-256 byte-identity comparison
Exit: 0
evidence_sha256=825597A81E4E2DF37A1A7C49B6A7D37206752B7C2E0F38DEA387CDE709FFE03B

python -m unittest discover -s tests -q
Exit: 0
Ran 487 tests in 333.822s — OK
```

Scoped staging inspection, `git diff --cached --check`, commit creation, and post-commit verification follow this record and are reported in the final handoff.

## Supporting and contradicting evidence

Supporting evidence: every declared negative control rejected for its intended cause; key-order replay was exact; the bilingual repository contract and all prior tests passed.

Contradicting evidence: none inside the declaration-only hypotheses. A passing declaration provides no evidence that CadQuery can construct the feature history or that FreeCAD can recover its semantic regions.

Alternative explanations: deterministic identity here may reflect JSON canonicalization only; it cannot predict STEP determinism. Missing evidence includes B-rep execution, self-intersection/solid validity, independent STEP inspection, real material-property provenance, manufacturing-domain validation, mesh/solver evidence, and physical correlation. Confidence is high for the tested Python declaration boundary and intentionally absent for downstream physical claims.

## Limitations and follow-up

Work 078 must execute bounded feature operators and prove deterministic valid-solid/STEP behavior on five canonical part families. Work 079 must replace the minimal material/manufacturing references with engineering-property and process-domain contracts. No Work 077 artifact is a load-capacity, manufacturing, safety, or physical-validation result.
