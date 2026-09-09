# Work 116: Material provenance and scoped failure

Thai companion: `work116-material_failure_scope.th.md`

Status: Planned

Original Work 106 package: 115

Dependencies: Work 111, Work 114, Work 115

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Replace unsupported strength/manufacturing assumptions with traceable applicability and selected verified failure models.

Geometry/field histories from prior works; candidate material/process evidence, clearly separating synthetic fixtures from measured data.

## 2. Proposed files

- `src/formula_ultimate/structural/material_failure_scope.py`
- `config/development/material_failure_scope_v1.json`
- `scripts/development/run_material_failure_scope.py`
- `tests/test_material_failure_scope.py`

## 3. Implementation sequence

1. Record material source, units, temperature/rate/history ranges, uncertainty and process dependence.
2. Implement evidence eligibility and domain checks before selecting constitutive/failure laws.
3. Verify the first applicable yielding/buckling models against reference cases with imperfection sensitivity.
4. Create separate extension slots for fatigue, fracture and wear; admit only tested/data-supported domains.

## 4. Experiment

- IV: Material/process choice, temperature, loading history and geometric imperfections.
- DV: Failure margins, uncertainty, sensitivity and evidence applicability coverage.
- Controls: Same geometry/load history and independent reference material cases.

## 5. Tests and falsification

Reject out-of-range properties, missing units, unjustified mixtures and synthetic-to-measured relabeling. Include known elastic-safe and failed fixtures.

## 6. Registration and acceptance

Freeze eligible sources, uncertainty treatment, constitutive assumptions and selected failure acceptance criteria.

Implemented failure laws pass references and applicability checks; missing failure domains remain explicit blockers to claims that need them.

## 7. Deliverables and handoff

Material/process evidence registry, law verification, uncertainty ranges and per-candidate missing-domain report.

Supplies admissible material/failure envelopes to all subsystem works and manufacturing Work 130.

## 8. Risks and non-goals

A universal fatigue/fracture model is outside one work. Split by law/data domain; a completed coverage registry is not complete physical survival.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_material_failure_scope tests.test_repository_contract -v
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_a
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_b --replay-reference artifacts/work116/run_a/result.json
```
