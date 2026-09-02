# Engineering Material and Manufacturing Contract V1

Thai companion: `ENGINEERING_MATERIAL_MANUFACTURING_CONTRACT_V1.th.md`

## Purpose and evidence boundary

Work 079 replaces floating component force limits with hash-addressed material properties, evidence domains, and geometry-measured manufacturing constraints. The executable authority is `src/formula_ultimate/components/engineering_contracts.py`; the canonical binding is `config/materials/engineering_material_manufacturing_v1.json`; and the runner is `scripts/components/validate_engineering_contracts.py`.

The canonical material/process records are **synthetic verification fixtures**. They exercise equations and fail-closed behavior and return `design_use_allowed=false`. They are not coupon results, handbook allowables, supplier capabilities, or vehicle-design inputs. A future sourced record must replace them without weakening any gate.

## Engineering material record

`engineering_material_v1` requires identity, display name, `synthetic` or `sourced` evidence status, exact properties, fatigue evidence state, evidence records, one source mapping per property, validation tolerance, and claim boundary.

Required SI properties are:

- `density_kg_per_m3`;
- `youngs_modulus_pa`, `poisson_ratio`, and `shear_modulus_pa`;
- `yield_strength_pa` and `ultimate_strength_pa`;
- `fracture_toughness_pa_sqrt_m`;
- `thermal_conductivity_w_per_m_k`, `specific_heat_capacity_j_per_kg_k`, and `thermal_expansion_per_k`;
- `allowable_temperature_min_k` and `allowable_temperature_max_k`.

Every property must be finite and every magnitude that is physically required positive must be positive. Poisson ratio must be in `(-1, 0.5)`, yield may not exceed ultimate strength, and the temperature interval must increase. Elastic consistency is checked by:

```text
G_expected = E / (2 * (1 + nu))
relative residual = abs(G_declared - G_expected) / G_expected
```

The residual must not exceed the declared tolerance, which itself is capped at `0.05`.

## Source, domain, and fatigue rules

Each evidence record has a stable source ID, citation, source SHA-256, evidence class, confidence in `[0, 1]`, and a temperature/material/process domain. `property_sources` must map every required property to an existing record. A material labeled `sourced` cannot use synthetic evidence.

Fatigue is either explicitly `missing` with no model, curve, or source, or `available` as an evidenced `sn_curve` with at least two points. Cycles must strictly increase and alternating stress must not increase. Missing fatigue evidence is observable and prohibits a fatigue-life claim; it is never replaced with a neutral curve.

The record must prohibit `maximum_force_without_geometry` and `physical_validation`. Unknown fields such as `maximum_force_n` fail. Only a fully sourced record can declare `design_use_allowed=true`; Work 079's synthetic fixture must and does declare `false`.

## Manufacturing process record

`manufacturing_process_v1` requires a typed process, evidence status, dimensional limits, tool-access envelope, tolerance class, `reject` policy for unsupported features, exact source mapping, and claim boundary.

The V1 dimensional gates are minimum wall thickness, hole diameter, ligament, web thickness, internal radius, and bend radius, all in metres. Tool evidence declares required clearance, maximum depth-to-diameter ratio, and allowed approach directions. The tolerance class declares the minimum achievable tolerance; a requested value smaller than that evidence is too tight and fails.

A process labeled `sourced` cannot use synthetic limit evidence. Only a sourced process can declare `production_use_allowed=true`. Even a passing sourced envelope must prohibit `manufacturability_proof`, because dimensional screening does not prove supplier, tooling, quality, inspection, cost, or production capability.

## Geometry witness and causal margins

`manufacturing_geometry_witness_v1` binds one part ID to an exact geometry SHA-256 and supplies measurement-evidence status/method/report SHA-256 plus arrays for walls, holes, ligaments, webs, internal radii, bend radii, tool-access checks, unsupported features, and requested tolerance. Empty measurement arrays fail rather than receiving defaults. Work 079's fixture marks these arrays `synthetic` because they were not independently extracted from the STEP file. Design use additionally requires `independently_measured` evidence; Work 081 owns that route.

For every dimensional family:

```text
margin = minimum(measured geometry values) - declared process minimum
```

A negative margin fails with a stable causal code: `wall_too_thin`, `hole_too_small`, `ligament_too_small`, `web_too_thin`, `internal_radius_too_small`, or `bend_radius_too_small`. Tool direction, clearance, depth ratio, tolerance, and unsupported features similarly fail with distinct codes. No dimension is clipped and no geometry is repaired.

## Hash binding and replay

Material, process, assignment, witness report, and final result use canonical sorted compact JSON SHA-256 identities. The assignment must exactly match part ID, geometry hash, material ID/hash, and process ID/hash. Any stale identity fails with `assignment_identity_mismatch`.

Run and replay with:

```powershell
python scripts/components/validate_engineering_contracts.py `
  --config config/materials/engineering_material_manufacturing_v1.json `
  --output artifacts/work079/run_a/evidence.json
```

Repeat to another output and compare exact file SHA-256. The canonical fixture remains synthetic even when replay is exact.

## Limitations and next evidence

Internal equation consistency is not real material validation. V1 does not model anisotropy, plastic hardening law, strain rate, environment/corrosion, heat-treatment/weld state, property scatter/statistical allowables, multiaxial fatigue, crack growth, creep, wear, surface finish, residual stress, or process simulation. Work 082 must apply a sourced admitted record to geometry-derived mesh/load cases before any structural claim. Higher-fidelity comparison and real evidence remain mandatory.
