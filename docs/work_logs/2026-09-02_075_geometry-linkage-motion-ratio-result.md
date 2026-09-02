# Work 075 Result: Geometry-Derived Linkage Motion Ratio

Status: Completed

Thai companion: `2026-09-02_075_geometry-linkage-motion-ratio-result.th.md`

## Outcome and files

Implemented 3D projected-lever motion-ratio derivation and virtual-work transformation of Work 073 suspension stiffness, damping, and travel. Added configuration, simulation module/exports, runner, eight focused tests, bilingual research, and this result. Deterministic evidence is ignored under `artifacts/work075/`.

## Evidence

Powered contacts derive ratio `0.7999999999999999`; rear derives `1.0`. The selected coupled run finished with maximum heave `0.0008656698982980348 m`, travel `0.019278824606844512 m`, minimum load `266.8789268655951 N`, and energy residual `5.0778645277023315e-9`. Unit ratio preserved Work 073 exactly; mutation changed identities; normalization, mirror, permutation, and degeneracy controls passed.

Application/result/canonical evidence/file hashes are `51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487`, `7fd4af71e95dc49be5330762efe284a20a0ac86bc73b19df6a17c41d0e0b552a`, `69d4ad48f82026fdca4134a0c00519f9dc4df837cb43c2ad0608b7eafe16c939`, and `37864D0AE558AFBEB4E2E90B63DE1A48D84C17D4C6B8EC6EB106414E02A2DE64`.

## Validation record

```text
python -m unittest tests.test_linkage_motion_ratio -v
Exit: 0
Ran 8 tests in 9.323s — OK

python scripts/experiments/run_linkage_motion_ratio.py --config config/vehicle/geometry_linkage_motion_ratio_v1.json --vehicle-root config/vehicle --output artifacts/work075/experiment_evidence.json
Exit: 0; status=passed

same command with --output artifacts/work075/replay/experiment_evidence.json
Exit: 0; byte-identical SHA-256 37864D0AE558AFBEB4E2E90B63DE1A48D84C17D4C6B8EC6EB106414E02A2DE64

python -m unittest discover -s tests -q
Exit: 0
Ran 471 tests in 206.598s — OK
```

Full regression, repository contract, compilation, commit, and post-commit replay follow before handoff.

## Limitations and follow-up

Geometry is synthetic and small-angle, not extracted from CAD. Work 076 integrates the selected transform with sustained closed-loop motion, but cannot upgrade these points to physical validation.
