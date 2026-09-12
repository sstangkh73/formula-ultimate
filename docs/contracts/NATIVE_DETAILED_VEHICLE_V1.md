# Native Detailed Vehicle Contract V1

Thai companion: `NATIVE_DETAILED_VEHICLE_V1.th.md`

Protocol ID: `native_detailed_vehicle_v1`

## Purpose and claim boundary

This contract admits one exact candidate only when its required physical occurrences are realized as deterministic native OCCT B-rep solids, connected into one explicit assembly, and imported by FreeCAD from the exact STEP bytes without hidden repair. The only passing status is `passed_native_detailed_geometry`.

That status establishes geometry, assembly, ownership, interface and boundary availability only. It does not establish performance benefit, physics validity, manufacturing readiness, safety, physical validation or promotion. All downstream physics must be rerun on these exact solids in Work 136.

## Frozen identity and inputs

The declaration shall contain:

- a candidate ID distinct from `final_126_r1`, revision, external task, primary-energy boundary, digital-only safety scope and `native_geometry_and_assembly_only` claim scope;
- exact commit, contract, result-log, artifact-file and inner-result SHA-256 pins for Works 108, 110, 112–123, 125, 126, 129 and 130;
- per-file SHA-256 audits for reusable upstream geometry from Works 83, 84, 87, 108 and 113, with an explicit `reuse_exact` or `regenerate_for_candidate` disposition;
- exact CadQuery Python, CadQuery, FreeCAD Python, FreeCAD, OCCT, Gmsh and CalculiX identities;
- SI units, deterministic thresholds, experiment variables, controls, metrics, success/failure criteria and falsification review fields.

Any missing file, changed byte hash, missing commit or changed runtime identity fails closed.

## Native parts and occurrences

Each definition declares revision-stable identity, material or zero-mass void ownership, material/process ID, eligible provenance, `native_occt_brep` representation, one-closed-solid policy, finished-form flag, construction-feature inventory and semantic face selectors. Raw persistent `FaceN` or `EdgeN` identifiers are forbidden.

A same-envelope primitive is inadmissible unless that primitive is the intended finished form and contains all required seats, holes, passages and end features. Purchased geometry requires supplier, source URI and source hash with `proxy: false`; an unsupported proxy blocks admission.

Every applicable occurrence needs a unique instance ID, region ID, placement, occurrence classes and mass ownership. Required classes cover structure, ground bodies and supports, actuation/transmission, onboard energy, controls/sensors, cooling/flow, external wetted geometry/openings, fastening/sealing, harnesses and service/load/thermal paths. Coverage shall be exactly `1.0`, with zero unknown essential occurrences.

## Assembly, tolerance, route and motion gates

All non-root instances shall reach one root through an explicit joint or an approved non-contact relation with justification. Contact relations declare semantic mating faces, coincident anchors, unit axes, nominal and worst-case tolerance state, interface ownership and any fastening or sealing hardware.

Acceptance limits are:

- mating residual `<= 1e-6 m`;
- non-contact penetration `<= 1e-12 m^3`, with Boolean failures observable and fatal;
- acyclic assembly and no floating component or duplicate material/void region;
- positive fastener engagement and seal compression inside its declared range;
- route endpoints distinct, actual bend radius at least the required radius, and minimum clearance nonnegative;
- at least 101 motion samples and refinement change `<= 1e-5 m`, with analytic swept envelope and disclosed between-sample risk for the registered motion.

## STEP and FreeCAD evidence

CadQuery exports canonical-timestamp STEP for every definition and occurrence, plus separate material and void assemblies. It derives volume, mass, center and full inertia from native geometry and declared density. The preview STL is non-evidence and uses chord tolerance `<= 0.00025 m`.

FreeCAD reads the exact occurrence and assembly STEP hashes without repair, requires one valid solid per occurrence, and recomputes native properties. Cross-application limits are relative volume and mass `<= 1e-8`, absolute center `<= 1e-7 m`, and inertia `<= 1e-7` relative to the registered component scale.

Semantic faces match by surface type, area and centroid at declared numeric tolerances. Planar orientation, bounds and edge count also match. A periodic curved face may move its parameter seam during STEP transfer, so curved-face axis-aligned bounds and seam-edge count are diagnostic rather than physical identity. All declared selector groups must still match one-to-one; survival shall equal `1.0`.

The FCStd witness is canonicalized only for archive timestamps, document creation/modification strings, document UUID and transient object numeric IDs. Native `Shape.bin` geometry is not changed or healed.

## Physics-boundary availability

The declaration maps semantic faces or regions for structural, thermal, internal-flow, external-aerodynamic, ground-motion, energy and controller/sensor domains. This proves only that an owned boundary exists on the exact geometry. Missing domain coverage, unknown instances or lost selectors fail.

## Required evidence and replay

Admitted output includes per-definition and per-instance STEP, separate material/void assembly STEP, FCStd, CadQuery and FreeCAD reports, semantic/interface/material-void/physics maps, mass-inertia, collision-clearance, motion and tolerance reports, native-derived exploded/section manifests, independent component audit, eighteen negative-control records and `result.json`.

`pilot` output is never admitted. `run_a` and clean `run_b` shall match exact declaration, artifact and result hashes. Replay drift fails.

## Falsification controls

The runner must reject all eighteen classes specified by the Work 135 plan: primitive substitution; missing occurrences; floating components; duplicate ownership; invalid solids; edited STEP; hidden repair; semantic loss; axis/engagement failure; worst-case failure; swept collision; cyclic/trapped assembly; route failure; structural-density void; missing external-flow opening; unsupported purchased proxy; changed upstream identity; and render-only evidence.

At least one material component is selected deterministically from a SHA-256-derived index without proxy-score preference and audited for features, sections, interfaces, ownership and access. A missing component-specific service relation remains an explicit limitation rather than an invented pass.

## Statuses and non-goals

Failing evidence remains observable as `invalid_native_geometry`, `incomplete_part_realization`, `assembly_unresolved`, `physics_mapping_unresolved` or a precise validation exception. No silent repair or manual aggregate override is allowed.

This contract does not prescribe conventional wheel count, symmetry, body style or powertrain; authorize fabrication; inherit Work 123–130 physics conclusions from box geometry; or call Level-0/cross-application evidence physical validation.
