# Work 109: Open free-form material generator

Thai companion: `work109-freeform_material_generator.th.md`

Status: Planned

Original Work 106 package: 108

Dependencies: Work 108

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Permit continuous boundary and topology edits without a named-part template; establish geometry coverage, not functional superiority.

Input: Work 108 region contract and material ownership; existing B-rep remains a comparison route.

## 2. Proposed files

- `src/formula_ultimate/search/freeform_material_generator.py`
- `config/development/freeform_material_generator_v1.json`
- `scripts/development/run_freeform_material_generator.py`
- `tests/test_freeform_material_generator.py`

## 3. Implementation sequence

1. Define an implicit/adaptive-volume representation with explicit resolution and material labels.
2. Implement boundary displacement, cavity routing, branching, split/merge and material redistribution.
3. Build surface/export adapters and measure approximation error against the source field.
4. Run seeded mutation chains and representation-enlargement trials; archive unsupported conversions.

## 4. Experiment

- IV: Representation, edit operator, spatial resolution and complexity cap.
- DV: Geometry error, reachable topology, preserved features and execution cost.
- Controls: Matched spatial domain, materials, random seeds and compute opportunity; fixed grammar reference.

## 5. Tests and falsification

Create and close a hole; split and reconnect regions; preserve asymmetric thin features. Detect self-intersection, vanished cavities, label mixing and renaming-only pseudo-novelty.

## 6. Registration and acceptance

Freeze minimum feature, field resolution, conversion tolerance, mutation bounds and per-attempt budget.

Registered valid cases retain occupancy/material identity within error bounds; invalid or unsupported conversions are explicit. No fixed target silhouette is an acceptance condition.

## 7. Deliverables and handoff

Generated corpus, mutation ancestry, source fields, inspectable surfaces and conversion-coverage matrix.

Supplies unfamiliar geometry to Work 110 and later search in Work 124.

## 8. Risks and non-goals

Kernel/grid bias may masquerade as physics. Record it and refine adapters. No invented mixed-material properties or universal arbitrary-shape guarantee.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_freeform_material_generator tests.test_repository_contract -v
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_a
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_b --replay-reference artifacts/work109/run_a/result.json
```
