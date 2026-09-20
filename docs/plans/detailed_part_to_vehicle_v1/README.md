# Detailed Work Plans: Part-to-Vehicle Discovery

Thai companion: `README.th.md`

Date: 2026-09-09 (Asia/Bangkok). Prepared by actual Work 107, begun on 2026-09-07.

Status: Planned implementation specifications; no future capability is implemented by this plan set.

## 1. Authority and numbering

Read the [Work 106 roadmap](../../reports/DETAILED_PART_TO_VEHICLE_DISCOVERY_ROADMAP_V1_2026-09-07.md) for the destination and the [Work 104 governing protocol](../../contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md) for scientific, physical, resource and promotion rules.

Actual Work 107 is this documentation expansion. Consequently, the previously tentative Work 106 package numbers 107–132 map to proposed implementation Works 108–133 below. This is an explicit forward mapping, not a rewrite of the old roadmap. The previous “next Work 107 = spatial material” proposal now maps to Work 108. Future numbers are not reservations: if intervening work consumes a number, allocate the next unused number and append a mapping at execution time.

These files are planning specifications, not started work logs. Before implementing a package, create its dated bilingual work-log plan with status `In progress`; do not mark all future packages in progress now. This request authorizes planning, not the physical tests described near the end.

## 2. Index and old-to-new mapping

Each linked plan includes entry evidence, proposed files, ordered implementation, variables/controls, negative tests, numerical registration, acceptance, artifacts, risks and handoff.

| Proposed work | Old package | Detailed plan | Capability dependencies |
|---|---|---|---|
| 108 | 107 | [Spatial material and void source of truth](work108-spatial_material.md) | Existing CAD |
| 109 | 108 | [Open free-form material generator](work109-freeform_material_generator.md) | 108 |
| 110 | 109 | [Actual geometry-to-mesh bridge](work110-geometry_mesh_bridge.md) | 108, 109 |
| 111 | 110 | [Vector solid fields from generated geometry](work111-vector_solid_fields.md) | 110 |
| 112 | 111 | [Physical terminals and assembly semantics](work112-physical_interface_graph.md) | 108 |
| 113 | 112 | [Detailed fastening and contact proof](work113-detailed_connection_contact.md) | 111, 112 |
| 114 | 113 | [Moving and compliant contact assembly](work114-moving_contact_assembly.md) | 113 |
| 115 | 114 | [Transient thermal and solid coupling](work115-coupled_thermal_solid.md) | 111, 113 |
| 116 | 115 | [Material provenance and scoped failure](work116-material_failure_scope.md) | 111, 114, 115 |
| 117 | 116 | [Bidirectional architecture and part tasks](work117-architecture_part_feedback.md) | 112, 114, 115 |
| 118 | 117 | [Ground interaction, stopping and direction control](work118-ground_interaction_tasks.md) | 114, 116 |
| 119 | 118 | [Realized transmission and actuation chain](work119-realized_actuation_chain.md) | 114, 115, 116 |
| 120 | 119 | [Detailed onboard energy realization](work120-onboard_energy_realization.md) | 115, 116, 119 |
| 121 | 120 | [Geometry-derived flow and heat exchange](work121-geometry_flow_heat_exchange.md) | 110, 115, 116 |
| 122 | 121 | [Controller, sensor and support hardware](work122-control_hardware_realization.md) | 119, 120 |
| 123 | 122 | [Coupled whole-candidate transient harness](work123-coupled_vehicle_transient.md) | 117, 118, 119, 120, 121, 122 |
| 124 | 123 | [Multiscale discovery and fair accounting](work124-multiscale_discovery_search.md) | 109, 117, 123 |
| 125 | 124 | [Registered detailed-part discovery comparison](work125-detailed_part_comparison.md) | 113, 114, 115, 116, 124 |
| 126 | 125 | [Complete detailed digital candidate](work126-detailed_vehicle_closure.md) | 118, 119, 120, 121, 122, 123, 124, 125 |
| 127 | 126 | [Optimized vehicle controls and causal substitution](work127-optimized_vehicle_controls.md) | 123, 126 |
| 128 | 127 | [Held-out race and robustness](work128-heldout_race_robustness.md) | 127 |
| 129 | 128 | [Independent higher-fidelity claim checks](work129-independent_claim_validation.md) | 125, 126, 127, 128 |
| 130 | 129 | [Manufacturing, tolerance and assembly handoff](work130-manufacturing_tolerance_handoff.md) | 126, 129 |
| 131 | 130 | [Authorized material and connection measurement](work131-physical_connection_correlation.md) | 113, 116, 130 |
| 132 | 131 | [Authorized subsystem correlation and endurance](work132-physical_subsystem_correlation.md) | 131 |
| 133 | 132 | [Authorized whole-vehicle validation program](work133-physical_vehicle_validation.md) | 128, 129, 130, 131, 132 |
| 135 | — | [Native detailed vehicle realization](work135-native_detailed_vehicle_realization.md) | 108, 110, 112–123, 125, 126, 129, 130 |
| 138 | — | [Geometry-general structural evaluator](work138-geometry_general_evaluator.md) | 062, 078, 092, 110, 111, 135 |

Numbers 136 and 137 were consumed by executed work items: 136 repaired the CadQuery-optional test guard and the status documents, and 137 authored the Work 138 card below. The Work 135 records name "Work 136" for the downstream physics rerun on native solids; that rerun keeps the next unused number at execution time. Work 138 is a forward corrective extension: the evaluator used by the bounded campaign reads five scale variables rather than geometry, so no shape outside its template can be scored. Work 139 (open the free-form grammar to vehicle candidates) and Work 140 (feed evaluator output into race time) are named in that card but are not yet specified.

Dependencies in this table denote the complete scope's capability inputs, not a requirement to wait before all preparatory work. Work 110 may start on B-rep before the new representation branch is ready; Work 112 may proceed after spatial geometry while meshing develops; local Work 124 search can start after Work 117, while its vehicle mode also requires Work 123. Never claim a complete package while its declared required branch is missing.

Work 132 additionally requires every implemented domain relevant to its selected subsystem. Work 133 requires the relevant physical subsystem evidence, qualified safety review and separate authorization. An integer dependency alone does not transfer evidence outside the original load/material/temperature/geometry envelope.

## 3. Common execution contract

Every individual plan inherits the following requirements; omitting them from a short card does not waive them.

1. Re-read applicable repository instructions and verify the current checkout, source state and upstream artifact identities. Preserve unrelated edits and historical evidence.
2. Freeze a bounded question, physical domain, SI conventions, external task, material/data eligibility, inputs and non-goals. Separate software fixtures, exploratory pilots and admitted comparisons.
3. Implement the actual geometry/model/adapter with tests for every physical law or component model. A declaration or coverage label alone is not implementation.
4. Execute real CAD/mesh/solver dependencies for the claimed capability. Python in each plan's command block means the verified runtime containing those dependencies; replace it with its resolved executable in the execution log. A skipped required dependency test blocks completion of that capability.
5. Validate at the declared scope and run affected upstream/downstream regressions. Choose the full suite when change risk warrants it; document any environment exclusions and never count them as physical evidence.
6. Create bilingual result logs with exact commands, exits, outputs, limitations and follow-up. Mark the execution plan `Completed` only after its gates pass, commit explicit scope immediately, verify the hash, and report it. Commit failure leaves work incomplete. No push or history rewrite.
7. Preserve all prior experiment outcomes. Failed scientific hypotheses can be completed experiments when execution and reporting gates pass; they do not achieve a positive discovery milestone.

The proposed files in each card are initial implementation seams, not an instruction to duplicate existing modules. At execution, inspect existing APIs and reuse them where appropriate. Record justified path changes in the new plan. Also create a bilingual contract under `docs/contracts/` and the required bilingual work logs for every implemented package. Each proposed CLI must be implemented and tested before use; none is runnable merely because it is printed here.

## 4. Numerical registration: mandatory values before admitted runs

Every card names domain-specific values to freeze. The execution registration must supply actual values, units, provenance and rationale for all applicable fields:

| Category | Required content |
|---|---|
| Task and inputs | Geometry/material/controller/environment identities; load, motion, heat and boundary histories; initial state |
| Representation | Spatial domain, minimum feature, approximation tolerance, topology/complexity caps and enlargement policy |
| Numerics | Mesh/DOF/iteration/time limits; at least 3 structural refinement levels; convergence/error/residual definitions |
| Materials and physics | Constitutive validity range, measured versus synthetic source, property uncertainty, omitted domains |
| Experiment | IV, DV, controls, outcome estimand, sample/seed design, effect direction, meaningful effect and statistical treatment |
| Holdout | Untouched data/condition identity, access policy and leakage detection; observed data is not fresh holdout |
| Resources | Pre-call reservations; complete budget partitions; failures/retries/tuning/audits; hardware/concurrency and measured peaks |
| Decision | Geometry invalid versus physics violated versus numerical unresolved versus not evaluated; claim-specific promotion rules |
| Safety for physical work | Explicit authorization, qualified review, approved bounds, stop/recovery and measurement plan |

No field that matters to a decision may be left unspecified in an admitted run. Use disclosed pilots/calibration to set values, then freeze them before the separate admitted evaluation. This plan deliberately does not fabricate universal tolerances, sample counts, safe loads or time estimates. Record a new registration if the task/evaluator/thresholds change; never lower a threshold after observing failure and call the original run passed.

## 5. Evidence package and acceptance layers

The proposed runner contract produces `result.json` under the declared output directory plus an artifact manifest. Required contents are: status and claim scope; immutable configuration/input identities; exact/toleranced replay metadata; execution/cost records; all pass/fail/unresolved/not-evaluated cases; numerical uncertainty; negative controls; supporting evidence; contradicting evidence; alternative explanations; missing evidence and confidence.

Geometry packages additionally retain actual source/export geometry, material/void regions and mass-property discrepancies. Field packages retain actual meshes, region/boundary maps, recovered reactions/fluxes, field outputs and convergence. Assembly packages retain physical path closure, internal parts, motion/contact and complete hardware/material accounting. Physical studies retain raw measurements, calibration/approval references and specimen/configuration identities; their runner is offline analysis only.

Distinguish these gates:

- **Software execution:** intended implementation and negative-control behavior are tested.
- **Numerical verification:** equations/geometry mappings and discretization are checked within scope.
- **Candidate feasibility:** the exact candidate passes required physical/model gates at the declared fidelity.
- **Scientific benefit:** a signed task-relevant effect exceeds uncertainty under fair controls and holdout.
- **Physical validation:** independent measurements support the precise tested use conditions.

Passing one layer does not automatically pass later layers. Unsupported physics is not a physical impossibility, an unfamiliar shape is not a defect, and unchanged graph topology cannot disqualify a useful shape-induced effect.

## 6. Milestones and scheduling

- **Geometry-to-field milestone:** Works 108–111. Actual generated material/void geometry drives verified vector fields.
- **Detailed assembly milestone:** Works 112–117. A realized connection, moving/thermal behavior and a traced architecture/part feedback cycle.
- **Whole digital candidate milestone:** applicable domain Works 118–123 and search/comparison/closure Works 124–126. Required internal hardware is explicit.
- **Evidence-backed comparison milestone:** Works 127–130. Optimized baselines, untouched race conditions, independent checks and manufacturing/tolerance scope.
- **Measured validation milestone:** authorized Works 131–133, in progressively larger tested scope.

The order is a dependency map, not a calendar promise. Run cost pilots before sizing studies. If a package requires more than one distinct solver domain, data collection program or safety approval, split it into bounded numbered execution works before implementation. In particular, detailed contact, material failure, internal/external flow, energy conversion and whole-vehicle physical testing can need several such works.

Do not postpone exploratory architecture feedback until every technology has been implemented. Equally, do not promote a vehicle while essential hardware or physics is unresolved. No named part, wheel count, symmetry, standard fastener or powertrain is compulsory unless an explicitly frozen task requires it.

## 7. Immediate start

Start with [Work 108](work108-spatial_material.md): validate actual material/void ownership and geometry-derived mass properties. Then open the implicit generator and actual meshing/solid-field paths. This gives downstream search causal geometry rather than only new descriptors.

This documentation set is completed through its own [Work 107 result](../../work_logs/2026-09-07_107_detailed-work-package-plans-result.md). Completion of that record does not mean Works 108–133 have started or passed.

## 8. Corrective extension after Work 133

Actual Work 134 added the proposed Work 135 plan after execution showed that Work 126 had closed a box-based registry rather than delivering the native whole/individual CAD requested by its original card. Work 135 is forward corrective work: it does not rewrite Work 126 and does not inherit its geometry as a detailed candidate. Its bounding boxes remain a function checklist only.
