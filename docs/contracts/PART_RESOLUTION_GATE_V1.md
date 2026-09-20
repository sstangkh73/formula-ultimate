# Part Resolution and Joint System Gate v1

Thai companion: `PART_RESOLUTION_GATE_V1.th.md`

Protocol version: `part_resolution_gate_v1`. Implemented by Work 140.

## 1. What this contract covers

Two questions that the project could not previously answer about its own
geometry: is a part modelled at part resolution, and is a declared joint a real
interface? Both are answered by measurement on the built solid, never by the
declaration.

```text
part declaration (STEP file or reference build)
  -> CadQuery build and measurement: faces, edges, surface types,
     shortest edge, tenth-percentile edge, volume, bounding box
  -> Gmsh mesh at the registered size factor
  -> resolution gates -> one registered part status

joint declaration (technology, two parts, placement, fit range)
  -> measured minimum distance, interference volume, penetration depth,
     mating face pairs, overlap area, engagement faces
  -> technology evidence check -> one registered joint status
```

## 2. Two feature metrics, two purposes

- `smallest_feature_m` is the shortest edge the part has. It answers whether
  the part contains a sliver, and is compared against `minimum_feature_m`.
- `feature_scale_m` is the tenth-percentile edge length. It answers what scale
  the part is modelled at, and is what the mesh must resolve.

Using the shortest edge for both would let one tiny fillet edge demand an
unaffordable mesh on an otherwise coarse part.

## 3. Part statuses

| Status | Meaning |
| --- | --- |
| `passed_resolution` | Above the manufacturing floor, meets its class requirement, and the mesh resolves its feature scale |
| `insufficient_resolution` | Below the declared face, curved-face, edge or feature-scale requirement for its class |
| `unmanufacturable_feature` | Shortest edge below the registered floor: a sliver is not detail |
| `unresolved_measurement` | No measurement, no mesh, or a mesh too coarse to resolve the feature scale |

Geometry verdicts are decided before mesh verdicts. Whether a part is
under-modelled does not depend on whether a mesher happened to succeed, and a
mesh failure is still recorded in the part's `mesh_failure` field.

## 4. Joint technologies and their required evidence

The design may join parts however it likes. The gate never requires a
fastener; it requires that the declared technology is backed by measurement.

| Technology | Required measured evidence |
| --- | --- |
| `threaded` | `engagement_faces` (at least two non-planar, non-cylindrical faces across the pair), `bearing_face` (at least one mating face pair), `clearance_in_range` |
| `welded` | `added_fillet_material` (interference volume above zero), `continuous_interface` |
| `bonded` | `bond_line_in_range`, `overlap_area` at or above the declared minimum |
| `interference` | `interference_in_range`, measured as a negative clearance from the penetration depth `2V/A` of the intersection solid |
| `integral` | `single_continuous_solid` |

| Status | Meaning |
| --- | --- |
| `passed_joint_evidence` | Every required evidence item was measured |
| `out_of_range_fit` | Only the fit requirement failed; the interface exists |
| `unsupported_joint_evidence` | A required geometric feature is absent from the parts |
| `unresolved_joint_measurement` | The kernel refused, or a joined part was not measured |

## 5. Claim boundary

`passed_part_resolution_gate` means the gate ran, every subject carries one
registered status, and all eight controls were rejected. A subject that fails
is a finding about that subject, not a failure of the run, and the run must
report it rather than relax the bar.

No force is solved across any joint in this protocol. The measured mating
faces, clearances and interferences are interface evidence only. The result
carries `discovery_claim`, `promotion_allowed`, `race_time_claim` and
`physical_validation` as false.

## 6. Mandatory controls

`sliver_below_manufacturing_floor`, `primitive_below_resolution_requirement`,
`mesh_too_coarse_for_feature`, `joint_without_measurable_interface`,
`fit_outside_declared_range`, `technology_outside_registry`,
`no_discovery_claim` and `exact_replay`. All eight must be rejected, and a
clean replay must reproduce the result SHA-256 exactly.

The mesh control selects a subject that already clears the geometry gates,
because a resolution shortfall would otherwise mask what the control tests.

## 7. Registration discipline

The mesh size factor, the manufacturing floor, the elements-across-feature
requirement and every part-class requirement are frozen in
`config/development/part_resolution_gate_v1.json` before the admitted run. A
pilot may inform those numbers; changing them after an admitted result is
post-observation repair and is forbidden.
