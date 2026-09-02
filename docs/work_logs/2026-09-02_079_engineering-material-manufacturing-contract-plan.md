# Work 079 Plan: Engineering Material and Manufacturing Contract

Status: Completed

Thai companion: `2026-09-02_079_engineering-material-manufacturing-contract-plan.th.md`

## Objective and scope

Implement fail-closed, hash-addressed engineering material and manufacturing-process contracts and bind them to a geometry witness. Material capability must come from declared density, elastic, strength, fracture, fatigue-evidence status, and thermal properties with source/domain/confidence records. Manufacturing admission must come from measured walls, holes, ligaments/webs, radii, tool access, and requested tolerance compared with an evidence-bearing process envelope.

The canonical record is a synthetic aluminium-like verification fixture. It validates equations and rejection behavior only and is explicitly ineligible for design use. No real coupon dataset was supplied in this work, so the implementation must preserve that missing-evidence boundary instead of inventing a sourced vehicle material.

## Experiment design

- Independent variables: material property values/evidence class/domain, fatigue evidence status/curve, process limits, geometry witness measurements, tool direction/clearance/depth ratio, requested tolerance, and record hashes.
- Dependent variables: material/process/assignment admission, elastic-consistency residual, property coverage, manufacturing margins/violation code, design-use eligibility, and deterministic record/report identities.
- Controls: canonical synthetic record and passing bracket-like witness; wrong unit/unknown field, `NaN`, negative property, invalid Poisson ratio, inconsistent `E/G/nu`, ultimate below yield, missing property source, unsupported fatigue claim, thin wall, small hole/ligament/web/radius, blocked tool access, excessive depth ratio, invalid tolerance, unsupported feature, and assignment-hash mismatch.
- Preferred hypothesis: complete internally consistent records and a witness inside every process limit replay exactly; every missing, inconsistent, unsupported, or out-of-envelope state fails before physics/fitness use.
- Falsification: accept a floating `maximum_force`, infer fatigue evidence, silently derive a missing source, clip a failing geometry dimension, treat a synthetic fixture as design material, or accept stale record hashes.

## Planned files

- `config/materials/engineering_material_manufacturing_v1.json`
- `src/formula_ultimate/components/engineering_contracts.py` and component exports
- `scripts/components/validate_engineering_contracts.py`
- `tests/test_engineering_contracts.py`
- `docs/contracts/ENGINEERING_MATERIAL_MANUFACTURING_CONTRACT_V1.md` and Thai companion
- this plan and matching bilingual result record
- ignored evidence under `artifacts/work079/`

## Validation and success criteria

Canonical serialization/hash replay must be exact. Elastic constants must satisfy `G = E / (2*(1+nu))` within the declared numerical tolerance; strength ordering, thermal range, fracture and thermal properties, full source mapping, fatigue status, and claim boundary must pass. The manufacturing witness must expose non-negative margins for every declared limit, and each negative control must fail with a stable causal code. Exact material/process hashes must bind to the assignment and geometry witness. Focused tests, full regression, compilation, bilingual contract, runner replay, scoped staging, `git diff --cached --check`, one commit, and post-commit replay must pass.

## Risks and explicit non-goals

Internal consistency cannot establish real material behavior. The synthetic fixture has no design allowables, coupon scatter, anisotropy, strain-rate/environment dependence, weld/heat-treatment state, multiaxial fatigue, crack growth, or production capability evidence. Passing process dimensions are screening rules, not proof of manufacturability, cost, quality, inspection, supplier capability, or structural safety.
