# Spatial Material and Void Contract V1

Thai companion: `SPATIAL_MATERIAL_VOID_V1.th.md`

Status: Implemented by Work 108 for a bounded CAD evidence scope.

## Purpose and claim boundary

This contract makes occupied geometry the source of volume and makes material ownership the source of mass, centre of mass and inertia. It prevents a geometry revision, cavity, material assignment or placement from changing while downstream evidence silently retains old mass properties.

Passing this contract is software execution and numerical/CAD verification for the admitted Work 092 cases. It is not structural, thermal, flow, manufacturing, durability, vehicle, scientific-benefit or physical validation.

## Spatial representation

All coordinates are metres, density is `kg/m3`, mass is `kg`, and inertia is `kg m2`. Every case identifies one exact Work 092 candidate and its canonical STEP SHA-256. The admitted set includes a curved single body, a subtractive hollow body and a four-body shape.

Each occupied source solid has exactly one material-region owner. No source body may be unowned or multiply owned. Multi-body source solids are ordered canonically by centre coordinates and volume before the registered body indices are applied. Pairwise intersection above `1e-12 m3` is rejected; no fusion or overlap suppression is allowed.

A void is admitted only when the registered `outer_feature_id`, `cavity_feature_id` and `occupied_feature_id` match an actual Work 092 `boolean_subtract` ancestry. The occupied volume must close as `outer - cavity` within `1e-8` relative error. A void label without that geometry is not evidence.

## Material and placement

Work 108 uses constant synthetic densities solely to verify accounting. Their names do not establish measured engineering properties. Every density has a disclosed provenance and validity statement.

Rigid placement is a unit rotation axis, an angle in radians and a translation in metres. The runner applies the transform to the actual region B-rep before measurement. Volume and centroidal shape invariants must remain consistent; world-frame centres and inertia orientations may change. Each source STEP identity, ordered material ownership, void declaration and placement is hashed into a dependent-evidence identity.

## Mass-property calculation

CadQuery and FreeCAD each measure actual placed STEP regions. CAD volume moments are converted from `mm3`, `mm` and `mm5` to `m3`, `m` and `m5`. Region mass is `density * volume`; region centroidal inertia is `density * geometric volume moment`. System centre and inertia use mass weighting and the parallel-axis theorem. Symmetry, finite values and positive diagonals are mandatory.

The registered cross-tool limits are:

- volume relative error: `5e-7`;
- mass relative error: `5e-7`;
- centre absolute error: `1e-7 m`;
- inertia relative error: `2e-6`.

CadQuery and FreeCAD share OCCT-family geometry technology, so their agreement is strong exact-artifact consistency evidence but not independent physical validation.

## Mutation, replay and failure states

The admitted run fills the registered hollow cavity with its actual outer B-rep and requires both STEP identity and mass to change. Material and placement mutations must also change the dependent-evidence identity. Duplicate/incomplete ownership, unknown materials, non-finite coordinates, non-unit axes, stale upstream declaration/STEP hashes, invalid CAD, undeclared overlap, cavity non-closure, tolerance failure and non-exact replay all fail closed.

`result.json` preserves input identities, region and system properties, comparison residuals, controls, execution identities, supporting and contradicting evidence, alternative explanations, missing evidence and confidence. A second clean run must match the canonical result identity exactly.

## Handoff

Works 109 and 110 may use this contract to ensure generated or meshed geometry has causal material and void ownership. Work 112 may attach physical interfaces only to immutable spatial revisions. Any extension to spatially varying material inside one connected body requires a new bounded declaration, tests and independent measurement strategy.
