# Geometry-Causal Part Contract V1

Thai companion: `GEOMETRY_CAUSAL_PART_CONTRACT_V1.th.md`

## Purpose

`geometry_causal_part_v1` is the minimum fail-closed declaration for something this repository may call a physical part. It replaces the implicit assumption that one functional box is a sufficient component model. It does not establish that the declared geometry exists, is manufacturable, carries load, or is physically validated.

The executable authority is `src/formula_ultimate/components/part_contract.py`. The canonical admitted example is `config/components/geometry_causal_part_contract_v1.json`.

## Required declaration

Every top-level field is required and unknown fields are rejected.

| Field | Required evidence |
|---|---|
| `contract_version` | Exact value `geometry_causal_part_v1` |
| `part_id` | Stable lower-case identity |
| `function_tags` | Non-empty unique functional claims |
| `feature_history` | Ordered feature IDs, operator names, SI parameters, and earlier-parent references |
| `material` | `material_id`, exact record SHA-256, and evidence status |
| `local_frame` | Origin and orthonormal right-handed `x/y/z` axes |
| `datums` | Unique point, axis, or plane witnesses, each with a complete frame |
| `interfaces` | Unique typed interfaces tied to a datum and geometry signature |
| `load_regions` | Unique geometry-signed application, support, contact, thermal, electrical, or fluid regions |
| `load_path` | At least two distinct declared regions in the intended transfer order |
| `manufacturing` | Declared process and evidence identity; feasibility is deferred to Work 079 |
| `tolerances` | Positive general length and angular tolerances in SI units |
| `minimum_feature_size_m` | Positive declared lower geometry scale |
| `parameter_provenance` | Exact one-to-one evidence record for every feature parameter and declared tolerance |
| `claim_boundary` | Non-empty admitted claims and an explicit `physical_validation` prohibition |

## Interface vocabulary

V1 accepts only `fixed_mount`, `revolute`, `prismatic`, `spherical`, `bearing_seat`, `shaft_coupling`, `spline_key`, `bolted`, `welded`, `ground_contact`, `thermal`, and `electrical_fluid`. Each interface declares a datum, SHA-256 geometry signature, mating role, positive `tolerance_m`, and unique allowed DOFs drawn from `tx`, `ty`, `tz`, `rx`, `ry`, and `rz`. A `fixed_mount` must declare no allowed DOF.

This vocabulary classifies intent. Work 080 must prove assembly constraint behavior, alignment, clearance, interference, and realized DOF.

## Units, values, and provenance

Feature parameters are accepted only with `_m`, `_m2`, `_m3`, `_rad`, `_ratio`, or `_count` suffixes. Values must be finite. A count is an integer of at least one; any parameter containing `thickness` must be positive. The general tolerance must be smaller than the minimum feature size, and each interface tolerance may not exceed it.

Every declared numeric design parameter has one provenance record containing source text, a lower-case SHA-256 source identity, and confidence in `[0, 1]`. Missing and extra provenance targets both fail. This is traceability, not proof that a source is suitable; Work 079 adds engineering-property source and domain checks.

## Frame and identity rules

Frames are checked at absolute tolerance `1e-9`: every axis has unit length, axes are mutually orthogonal, and `x cross y = z`. Feature parents must already exist earlier in history. Part, feature, datum, interface, load-region, function-tag, DOF, and claim identities are duplicate-free. No default frame, material, interface, or load path is inserted.

## Canonical replay

The admitted mapping is serialized as UTF-8 JSON with sorted object keys, compact separators, ASCII escapes, and `allow_nan=False`. The declaration identity is SHA-256 of those exact bytes. Reordering object keys therefore preserves identity; changing array order remains causal and changes identity.

Run the reference witness with:

```powershell
python scripts/components/validate_part_contract.py `
  --config config/components/geometry_causal_part_contract_v1.json `
  --output artifacts/work077/part_contract_evidence.json
```

## Fail-closed boundary

The parser rejects unknown/missing fields, unknown parameter-unit suffixes, non-finite values, non-positive thickness/minimum feature/tolerance, excessive tolerance, invalid or left-handed frames, unsupported interface/datum/region types, duplicates, forward feature references, incomplete provenance, and a load path with fewer than two distinct known regions.

Passing admits only `contract_complete` and `deterministic_declaration` for the reference. It does not admit CAD validity, STEP identity, material adequacy, manufacturing feasibility, assembly behavior, structural capacity, fatigue/fracture life, thermal behavior, or physical validation.
