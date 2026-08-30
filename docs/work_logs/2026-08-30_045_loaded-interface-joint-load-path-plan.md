# Work 045 Plan: Loaded Interface and Joint Load Path

Status: Completed

Thai companion: `2026-08-30_045_loaded-interface-joint-load-path-plan.th.md`

## Objective

Demonstrate that a finite resultant force entering one declared cylindrical interface flows through one connected plate solid and closes through two declared support interfaces, with persistent interface identity across CAD, STEP, FreeCAD, mesh, solver input, and parsed results.

## Scope and claim boundary

- Create `loaded_interface_plate_v1`: a rectangular prismatic plate with one loaded through-hole and two support through-holes defined by topology-neutral geometric signatures.
- Generate one CAD solid with CadQuery, export one hashed STEP, independently import/identify all cylindrical interfaces in FreeCAD, mesh the exact STEP with Gmsh, and solve linear elasticity with CalculiX.
- Apply a constant-direction consistent traction resultant on the loaded cylindrical surface and rigid bonded support constraints on the declared support cylindrical surfaces.
- Measure compliance, nominal bearing/net-section stress, support load share, force/moment closure, solver internal energy, field evidence, mesh convergence, and a one-support boundary-sensitivity case.

This validates only the declared bonded-interface plate fixture. It does not validate bolts, pins/contact, bearing failure, welds, adhesives, friction, preload, manufacturing tolerance, nonlinear material failure, arbitrary joints, or a vehicle chassis.

## Experiment design

- independent variables: mesh size, support interface set (`both_supports` versus `lower_support_only`), interface geometry, and load eccentricity fixed by the loaded-hole center;
- dependent variables: interface area/resultant/moment, compliance, reaction load share, nominal bearing/net-section stress, internal/external energy, stress field, mesh identity, and wall time;
- controls: one exact STEP hash, material, coordinate frame, geometric interface signatures, load resultant/direction, mesh family, solver/parser, and SI units;
- preferred hypotheses: last-two compliance change `<=5%`; force/moment residual `<=1e-5`; energy residual `<=1e-4`; all interface identities survive; and boundary sensitivity remains `<=10%` for transferability;
- falsification: retain the one-support result even if it rejects transferability; reject broken ligament, missing support, duplicated load ID, zero-area interface, and disconnected solid.

## Planned implementation and files

- `config/structural/loaded_interface_plate_v1.json`;
- interface grammar, mesh mapping, consistent load, deck, and result parser under `src/formula_ultimate/structural/`;
- CadQuery generator and FreeCAD independent interface inspector;
- Work 045 orchestrator/launcher and ignored evidence under `artifacts/work045/`;
- focused identity/load/negative-control tests;
- bilingual physics report and matching result records.

The proposed mesh sizes `6`, `4`, and `3 mm` are frozen before solver results. A mesh-only count may reject compute infeasibility but may not tune a level using structural response.

## Validation and success criteria

- exact interface IDs and STEP hash survive every declared stage;
- force/moment residual `<=1e-5` and internal/external energy residual `<=1e-4` for every admitted solve;
- last-two compliance and integrated-resultant change `<=5%`;
- a measured boundary-response change `>10%` must mark transferability `rejected` without invalidating completed execution evidence;
- all malformed/disconnected controls fail closed;
- focused/live/full tests, compile/static checks, staged-diff check, explicit commit, and clean-tree replay pass.

## Risks and explicit non-goals

STEP does not guarantee application-level face labels, so identity will use immutable center/radius/axis/area signatures verified independently at each stage. Linear tetrahedra may reject the convergence hypothesis near holes. Rigid bonded cylindrical supports can be stiffness-sensitive and are deliberately tested. No contact, bolt preload, plastic bearing, fracture, fatigue coupling, whole vehicle, push, or publication is included.
