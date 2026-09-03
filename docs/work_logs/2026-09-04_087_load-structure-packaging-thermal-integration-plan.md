# Work 087 Plan: Load Structure, Packaging, and Thermal Integration

Thai companion: `2026-09-04_087_load-structure-packaging-thermal-integration-plan.th.md`

## Status

Status: Partial

## Objective

Execute the integration scope originally numbered Work 085 after the two recorded structural-remediation works. Package the exact Work 083 ground-interaction and Work 084 energy/torque parts inside one geometry-causal load frame with explicit mounts, coolant routes, control route, service envelope, load/energy/thermal ledgers, failure controls, and a complete STEP/FCStd witness.

This is one topology-neutral integration candidate, not a prescribed chassis form. Because material/process evidence remains synthetic, and the new integration frame is not covered by the Work 086 component meshes, the implementation is expected to close as `Partial` unless those blockers are independently resolved.

## Frozen scope

- Import the exact five Work 083 and seven Work 084 part STEP files without mutation.
- Generate five integration solids from frozen SI parameters: `upper_load_bridge`, `ground_mount_adapter`, `energy_mount_adapter`, `coolant_inlet_route`, and `coolant_outlet_route`.
- Export seventeen per-part STEP identities, a seventeen-solid integration STEP, and a FreeCAD FCStd with seventeen named objects.
- Calculate mass, centre of mass, and full geometry inertia from the exact B-reps and declared synthetic densities.
- Check every pair for overlap; distinguish declared contact/coupling interfaces from forbidden pairs.
- Check Work 083 motion envelope, energy-store removal path, routing clearances, bend-radius declarations, ground clearance, and external envelope.
- Close acceleration, braking, cornering, combined, bump, and torque-reaction force/moment ledgers to `1e-5`; close energy/thermal ledgers to `1e-4`.
- Identity-couple the component structural cases to Work 086 result `ec818c21ea45f4a129f762bac3130e06628c7b560bb1d74dff8a8c9555cdf827`.
- Run disconnected mount, blocked service path, routing collision, inadequate rejection, asymmetric load, weakened mount, thin-frame, mirror, and replay controls.

## Planned files

- `config/candidates/load_structure_integration_001.json`
- `src/formula_ultimate/subsystems/load_structure_integration.py`
- `scripts/candidates/build_load_structure_integration_001.py`
- `scripts/candidates/inspect_load_structure_integration_freecad.py`
- `tests/test_load_structure_integration_001.py`
- `docs/contracts/LOAD_STRUCTURE_INTEGRATION_001.md` and Thai companion
- this plan/result and Thai companions
- ignored evidence under `artifacts/work087/`

## Validation and gates

- Exact upstream hashes, seventeen valid separate solids, no forbidden overlap above `1e-12 m3`, forbidden clearance `>=0.5 mm`, routing/service clearance `>=2 mm`, and ground clearance `>=5 mm`.
- Geometry-derived mass/COM/inertia and exact replay.
- Force/moment residual `<=1e-5`; energy/thermal residual `<=1e-4`.
- All controls cause their preregistered rejection/degraded/`DNF` consequence.
- Focused, repository-contract, compilation, and full regression tests pass.

## Explicit non-goals and stop conditions

No chassis, monocoque, crashworthiness, fatigue, physical thermal, production, safety, or physical-validation claim. Do not call Gate C complete without meshed convergence evidence for the new load frame or design-eligible material/process evidence. Stop or return `Partial` on any missing identity, overlap suppression, blocked service path, discarded heat/load, non-causal control, or replay mismatch.
