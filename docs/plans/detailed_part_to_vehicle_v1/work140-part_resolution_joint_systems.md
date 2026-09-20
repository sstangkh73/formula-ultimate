# Work 140: Part resolution and joint systems

Thai companion: `work140-part_resolution_joint_systems.th.md`

Status: Planned

Original Work 106 package: none. Forward corrective extension.

Dependencies: Work 092 (free-form grammar limits), Work 135 (native detailed vehicle), Work 138 (geometry-general evaluator), Work 139 (composition).

Mandatory common requirements: [index and execution rules](README.md).

## 1. Problem this work corrects

The detailed vehicle looks like a part list but is not modelled at part resolution. Measured on `config/development/native_detailed_vehicle_v1.json`:

- all 48 part definitions declare **exactly three features each**;
- the smallest declared dimension in the whole vehicle is `1.5 mm`, and the median smallest feature per part is `6.0 mm`;
- the fastener is a plain cylinder with a cylindrical head: no thread, no chamfer, no bearing face, no clearance fit.

Meanwhile the Work 092 grammar already permits a `1e-05 m` minimum feature and 32 features per part. The limit is the declarations, not the kernel.

Joints are equally thin: an attachment is a parent-child label with an axis, not a modelled interface. Work 138 evaluates each part in isolation, so no force has ever crossed a joint.

## 2. Outcome and claim boundary

Passing means only `passed_part_resolution_gate`: the gate itself ran, every subject part and joint carries one registered status, and all controls were rejected. The verdict on any given part is separate from the verdict on the run; an insufficient part is a finding, not a failure of the work.

This is a geometry-resolution and interface-evidence gate. It is not promotion, not manufacturability, not race time, and not physical validation.

## 3. Technology neutrality

The design may join parts however it likes. The gate never requires a bolt. It requires that whichever technology is declared is backed by measured geometry:

| Technology | Required measured evidence |
| --- | --- |
| `threaded` | helical or free-form engagement faces on both parts, a bearing face, and a clearance fit inside the declared range |
| `welded` | added fillet material at the interface and a continuous interface region |
| `bonded` | a bond-line gap inside the declared range and an overlap area at or above the declared minimum |
| `interference` | a measured negative clearance inside the declared range |
| `integral` | one continuous solid across the interface |

A declared joint with no measurable interface is `unsupported_joint_evidence`. A part may not claim a joint it does not geometrically have.

## 4. Resolution gates, measured on the built solids

1. **Manufacturability floor.** The smallest measured feature is at or above `minimum_feature_m`. A part below it is `unmanufacturable_feature`, because a sliver is not detail.
2. **Resolution requirement.** Each part class declares the minimum face count, curved-face count and distinct feature scales it must exhibit. A part below its requirement is `insufficient_resolution`.
3. **Mesh resolution.** The registered mesh must place at least `minimum_elements_across_feature` elements across the smallest declared feature. Otherwise the part is `unresolved_measurement` and no strength claim may rest on it.

## 5. Proposed files

- `src/formula_ultimate/assembly/part_resolution.py`
- `scripts/cad/measure_part_resolution.py` (pinned CadQuery runtime; also builds the reference detailed fastener)
- `scripts/development/run_part_resolution_gate.py`
- `config/development/part_resolution_gate_v1.json`
- `tests/test_part_resolution.py`
- `docs/contracts/PART_RESOLUTION_GATE_V1.md` and its Thai companion

## 6. Subjects for the admitted run

- `work135_bolt`: the existing vehicle fastener, expected to fail the resolution requirement.
- `reference_m8_bolt`: a fastener built at the required resolution, with a swept thread, hex head, hex socket and chamfer.
- Joints across the declared technologies, including at least one that passes and at least one existing Work 135 joint.

## 7. Mandatory controls

1. a part whose smallest feature is below the floor is rejected;
2. a part below its declared resolution requirement is rejected;
3. a mesh too coarse for the smallest feature yields `unresolved_measurement`, never `passed`;
4. a declared joint with no measurable interface is rejected;
5. a joint whose clearance is outside its declared range is rejected;
6. a technology outside the registry is rejected;
7. the run claims no discovery, promotion, race time or physical validation;
8. a clean replay reproduces the result SHA-256 exactly.

## 8. Acceptance

All eight controls rejected, one registered status per subject part and joint, every gate number measured rather than declared, and an exact replay.

## 9. Risks and handoff

- The existing vehicle is expected to fail. That result must be reported, not softened, and it must not trigger a quiet relaxation of the bar.
- Kernel limits are evidence. If a thread or a boolean cannot be built, the outcome is `unresolved_measurement` with the kernel message attached, not a silently simplified part.
- Force crossing a joint still needs contact or tied-surface analysis; this work measures interfaces, it does not yet solve them. That, and raising the whole Work 135 vehicle to the bar, are the follow-on works.
