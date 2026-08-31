# Work 066 Plan: Functional Vehicle Architecture v2

Status: Completed

Thai companion: `2026-08-31_066_functional-vehicle-architecture-v2-plan.th.md`

## Objective

Replace the four-placeholder Work 047 vehicle fixture as the next-generation research input with a technology-neutral, multi-component functional vehicle architecture. Every admitted candidate must contain derivable 3D solids, materials, typed ports, compatible connections, explicit energy/torque/control/thermal/structural paths, and failure-relevant limits. A propulsion label without a physically connected conversion and transmission path must not create force.

This work creates and validates the architecture grammar plus one fixed reference fixture. It does not yet replace the frozen Work 062 campaign or claim that the reference fixture is optimized.

## Research question and hypothesis

Question: can one architecture contract represent a visibly multi-part vehicle while remaining neutral to component count, layout, energy technology, conversion method, transmission type, and ground-interaction mechanism?

Preferred hypothesis: the reference fixture and independently regenerated CAD satisfy all typed graph, geometry, mass, packaging, energy, torque, thermal, control, and structural-path contracts; deliberate broken-path and incompatible-port controls fail closed with deterministic codes.

Falsification includes any accepted floating component, undeclared force source, domain-mismatched connection, absent storage-to-ground power path, absent load-to-ground structural path, absent heat-source-to-sink path, uncontrolled actuator, nonpositive/invalid physical limit, overlapping solid, invalid STEP, mass/inertia mismatch, nondeterministic identity, or negative control that passes.

## Functional contract

Candidates may use any topology or technology, but must instantiate capabilities equivalent to:

1. energy storage;
2. energy conversion;
3. torque or power transmission;
4. ground interaction/propulsion;
5. direction control;
6. braking;
7. load-bearing structure;
8. thermal management;
9. sensing/control.

No conventional engine, motor, gearbox, wheel count, body form, or layout is mandatory. Capabilities are recognized through declared function tags and connected typed ports, not component names.

## Typed physical domains

- `structural`: six-component load path through declared mount interfaces.
- `electrical`: energy/power transfer with voltage, current, efficiency, and capacity limits where applicable.
- `mechanical_rotary`: torque, angular speed, inertia, ratio, and efficiency limits.
- `thermal`: heat flow, temperature limit, and heat-rejection capacity.
- `control`: command/sensor connectivity; it carries no mechanical energy.
- `ground`: declared external contact that can transmit bounded longitudinal/lateral/normal force.

Connections must join compatible domains and reference exact component ports. Energy and mechanical losses become heat; control edges cannot substitute for power edges.

## Geometry and CAD scope

Each functional component must have one declared primitive solid, SI dimensions, pose, material density, ports located on or inside its solid, and explicit limits. Work 066 will generate one STEP per component plus a multi-solid assembly STEP, then inspect the assembly independently with FreeCAD. Geometry-derived mass, centre of mass, inertia, solid count, component identities, and hashes must replay.

The reference fixture may use simple boxes/cylinders because this work validates architecture and evidence plumbing, not detailed manufacturing geometry. Each solid remains a distinct functional component rather than one decorative body.

## Planned files

- `src/formula_ultimate/topology/functional_vehicle.py`
- exports in `src/formula_ultimate/topology/__init__.py`
- `config/vehicle/functional_vehicle_architecture_v2.json`
- `scripts/cad/generate_functional_vehicle_v2.py`
- `scripts/cad/inspect_functional_vehicle_v2_freecad.py`
- `tests/test_functional_vehicle_architecture.py`
- bilingual research/result documentation and ignored evidence under `artifacts/work066/`

## Independent variables, controls, and metrics

- Independent variables: component count, function allocation, primitive geometry, material, pose, port domains/locations, connection topology, energy/conversion/transmission parameters, ground contacts, and thermal/control routing.
- Dependent variables: admission status/codes, path completeness, port compatibility, power/torque/heat limits, component and assembly mass properties, overlap/containment, STEP validity, FreeCAD residuals, and replay fingerprints.
- Controls: SI units, right-handed `x` forward/`y` left/`z` up frame, frozen material records, deterministic ordering/serialization, explicit external environment node, zero silent repair, and fixed numerical tolerances.
- Metrics: required-capability coverage, path count, component/connection/contact count, declared versus geometry-derived mass residual, centre/inertia residual, solid count, invalid-control rejection count, and SHA-256 replay.

## Validation and success criteria

1. Reference architecture passes exact schema and physics-path validation.
2. Storage reaches every ground-propulsion capability through compatible energy/conversion/transmission edges.
3. Every non-ground component has a structural path to a declared ground contact.
4. Every heat-producing component has a thermal path to a heat-rejection capability.
5. Conversion, direction, and braking actuators have control paths from a controller.
6. All declared limits are finite, positive where required, and locally conservative; efficiency is in `(0, 1]`.
7. Deliberate broken-path, mismatched-domain, floating-component, overlap, invalid-limit, and force-from-nowhere controls are rejected.
8. CAD generation and FreeCAD inspection pass with exact component count/identity, valid solids, no hidden repair, and relative mass/centre/inertia residuals `<= 1e-6`.
9. Focused and full tests, compilation, bilingual evidence, scoped commit, and post-commit clean-tree replay pass.

## Risks and explicit non-goals

The first reference architecture can bias later search if treated as a preferred layout; it is only a fixed validation baseline. Primitive geometry cannot resolve gear teeth, bearings, windings, seals, fasteners, fluid passages, local joints, crash structures, or manufacturing tolerances. Work 066 does not implement transient drivetrain dynamics, efficiency maps, combustion/electromagnetic physics, tyre/suspension coupling, detailed cooling flow, structural FEA, contact, fatigue, fracture, controls optimization, race fitness, independent replication, physical validation, safety certification, or a discovery claim. Those require separately numbered work items.
