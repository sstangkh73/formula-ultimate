# Work 047 Plan: Topology-Neutral Whole-Vehicle CAD and Assembly Grammar

Status: Completed

Thai companion: `2026-08-30_047_topology-neutral-vehicle-assembly-plan.th.md`

## Objective

Represent and verify one complete multi-component 3D vehicle candidate without prescribing a conventional vehicle shape, wheel count, component count, or layout, while making every solid, material, interface, connection, contact, energy path, and external-load path explicit.

## Scope and claim boundary

Create a versioned assembly grammar using a small initial library of neutral solid primitives, deterministic placement, typed point interfaces, graph connections, contacts, envelope and keep-out rules, and material-density records. Export exact per-component STEP files plus one multi-solid assembly STEP, inspect them independently with FreeCAD, and compare geometry-derived mass properties. This is geometric admission only, not structural, aerodynamic, thermal, manufacturing, safety, race, novelty, or superiority proof.

## Experimental design

- Independent variables: component count, primitive type/parameters, placement, material, interface declaration, connection graph, contact count/arrangement, energy graph, load-support graph, envelope, and keep-outs.
- Dependent variables: solid validity/count, STEP identity, interface position residual, overlap/keep-out/envelope/ground-clearance status, mass, centre of mass, inertia tensor, graph connectivity, and replay hashes.
- Controls: grammar/library version, SI global frame, translation-only v1 transform, material records, exact tolerances, tool paths, no hidden healing/repair, and exact Work 046 failure-contract identity.
- Preferred hypothesis: the admitted fixture regenerates identical declarations/STEP identities, every typed path is complete, all solids are valid, and FreeCAD versus independent component-sum mass/centre/inertia residuals are each `<=1e-6` relative.
- Failure criteria: floating component, overlapping protected volumes, unmatched interface, disconnected required energy/load path, invalid/duplicate identity, invalid solid, massless energy component, envelope violation, or undeclared ground contact fails closed.

## Planned files

- `config/vehicle/topology_neutral_vehicle_v1.json`
- `src/formula_ultimate/topology/vehicle_assembly.py` and exports
- CadQuery generator and FreeCAD inspector under `scripts/cad/`
- `scripts/topology/run_vehicle_assembly_acceptance.py`
- `scripts/run_work047.ps1`
- `tests/test_vehicle_assembly.py`
- `docs/physics/TOPOLOGY_NEUTRAL_VEHICLE_ASSEMBLY.md` and `.th.md`
- matching Work 047 bilingual result records
- ignored CAD/STEP/evidence under `artifacts/work047/`

## Validation

Run focused grammar/negative-control tests, two independent CAD exports, FreeCAD inspection, deterministic Work 047 experiment, Work 046 regression, full repository tests, Python compilation, repository-contract checks, staged-diff checks, explicit scoped commit, and clean-tree replay.

## Success criteria

- Component and assembly STEP artifacts are deterministic and every solid is valid.
- Interface residuals and forbidden-overlap residuals pass declared tolerances without repair.
- Required source-to-propulsion and external-load-to-contact paths exist explicitly.
- FreeCAD and analytical/component-sum mass, centre, and inertia agree within `1e-6` relative.
- All negative controls fail closed and same-input replay identity is exact.

## Risks

STEP does not reliably preserve application labels, so identity must use per-component hashes plus geometric signatures. Primitive-only v1 grammar is expressive infrastructure, not open-ended shape discovery. Translation-only placement excludes arbitrary orientation in this work item.

## Explicit non-goals

No conventional-car template, fixed wheel/contact count, FEA load cases, aerodynamics, cooling, manufacturing, controls, race fitness, design search, push, or publication is included.
