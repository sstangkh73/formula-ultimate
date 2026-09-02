# Work 077 Plan: Geometry-Causal Part Contract V1

Status: Completed

Thai companion: `2026-09-02_077_geometry-causal-part-contract-plan.th.md`

## Objective and scope

Define the first fail-closed repository contract for a geometry-causal physical part and record the user-supplied Work 077-086 whole-vehicle roadmap. An admitted part must declare its functional identity, ordered feature history, material assignment, local frame, datums, interfaces, load/application regions and load path, manufacturing process, tolerances, minimum feature size, parameter provenance, and claim boundary.

This work defines and validates declarations. It does not generate B-rep geometry, inspect STEP, solve structural response, validate a manufacturing process, or prove that a declared part is physically feasible.

## Experiment design

- Independent variables: field presence/order, interface type, coordinate-frame basis, parameter unit suffix and value, tolerance, minimum feature size, material evidence identity, load-region connectivity, and provenance completeness.
- Dependent variables: admission/rejection, exact failure reason, canonical serialized bytes, declaration SHA-256, and replay identity.
- Controls: one canonical admitted bracket declaration; key-order permutation; unknown-field, wrong-unit, missing-material, missing-interface, missing-load-path, `NaN`, negative-thickness, invalid-tolerance, invalid-frame, and unsupported-interface controls.
- Preferred hypothesis: semantically identical declarations produce identical canonical bytes and SHA-256 while every malformed or incomplete declaration fails before downstream geometry or physics work.
- Falsification: silent field removal, implicit unit conversion, non-finite data admission, default material/interface/load path, hash drift under key reordering, or a permissive unknown interface.

## Planned files

- `docs/reports/GEOMETRY_CAUSAL_WHOLE_VEHICLE_ROADMAP_V1.md` and Thai companion
- `docs/contracts/GEOMETRY_CAUSAL_PART_CONTRACT_V1.md` and Thai companion
- `config/components/geometry_causal_part_contract_v1.json`
- `src/formula_ultimate/components/part_contract.py` and component exports
- `scripts/components/validate_part_contract.py`
- `tests/test_part_contract.py`
- this plan and matching bilingual result record
- ignored evidence under `artifacts/work077/`

## Validation and success criteria

The canonical example and key-order permutation must yield byte-identical serialization and the same SHA-256. Unknown fields or units, missing material/interface/load path, non-finite values, non-positive thickness or minimum feature size, invalid tolerance, non-orthonormal/right-handed frame, duplicate identities, and unsupported interface types must fail closed with tested reasons. Focused tests, full regression, compilation, bilingual repository contract, runner replay, scoped staging, `git diff --cached --check`, one commit, and post-commit verification must pass.

## Risks and explicit non-goals

A truthful declaration can still describe geometry that a CAD kernel cannot construct or a structure that fails. Interface geometry signatures are declarations in Work 077 and are not yet verified after STEP exchange. Material evidence is referenced but its engineering-property/manufacturing contract is deferred to Work 079. Work 077 must not be used to claim CAD validity, load capacity, manufacturability, assembly validity, or physical validation.
