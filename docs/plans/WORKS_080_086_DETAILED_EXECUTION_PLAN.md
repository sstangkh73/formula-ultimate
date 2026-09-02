# Detailed Execution Plan: Works 080-086

Thai companion: `WORKS_080_086_DETAILED_EXECUTION_PLAN.th.md`

Status: Preregistered program plan; Work 080 is `In progress`, Works 081-086 are not started.

## 1. Purpose

This plan expands the seven remaining roadmap items required to move from separate bounded B-rep test parts toward Whole Mechanical Vehicle Candidate 001. It is an execution contract, not evidence that any listed capability exists.

Completed starting evidence:

- Work 077: fail-closed geometry-causal part declaration;
- Work 078: five deterministic one-solid B-rep/STEP fixtures and fifteen executed feature operators;
- Work 079: material, manufacturing-process, geometry-witness, and assignment contracts.

Important starting limitation: the Work 079 material, process limits, and measurement arrays are synthetic fixtures. They return `design_use_allowed=false`. A STEP hash is real toolchain evidence, but the dimensions have not yet been independently extracted by Work 081 and no sourced vehicle-design material/process record has been admitted.

## 2. Destination after Work 086

Candidate 001 may be called a **whole mechanical vehicle ready to begin bounded whole-vehicle research** only if it has:

1. separate reproducible B-rep parts with exact identities;
2. sourced material/process records and independently measured geometry where design-use claims require them;
3. assembly constraints with calculated joints and DOFs;
4. continuous geometry-realized load, torque, energy, thermal, and ground-contact paths;
5. geometry-derived mass, centre of mass, inertia, thickness, sections, lever arms, clearances, and interfaces;
6. mesh/solver evidence with observable yield, fracture-domain, fatigue, torsion, buckling, connection, and numerical failures;
7. failure propagation into subsystem state and deterministic `DNF` where required;
8. exact seed/config/toolchain replay without result-conditioned geometry changes;
9. all declared whole-vehicle Level 0 admission cases and controls.

This endpoint is not physical validation, safety certification, manufacturing approval, novelty, superiority, or a race-ready real vehicle.

## 3. Dependency and batch order

```text
Completed 077-079
      |
      v
080 Assembly and joint kernel
      |
      v
081 STEP -> FreeCAD geometry witness V2
      |
      +---- evidence remediation if material/process/measurement is not design-eligible
      |
      v
082 Geometry -> structural physics coupling
      |
      v
083 Ground-interaction module Candidate 001
      |
      v
084 Energy conversion and torque-path Candidate 001
      |
      v
085 Load structure, packaging, and thermal integration
      |
      v
086 Whole Mechanical Vehicle Candidate 001
```

Execution cadence remains `080-082`, `083-085`, then `086`. Within each batch, work is sequential because later items consume exact hashes and evidence from earlier items. A rejected dependency produces a separately numbered remedial work; it does not permit a relaxed downstream gate.

## 4. Program-wide rules

### 4.1 Frozen controls

Every admitted experiment freezes before its first admitted run:

- SI units and coordinate-frame convention;
- part/assembly/schema versions;
- CadQuery, OCCT, FreeCAD, Gmsh, CalculiX, Python, and library versions;
- material/process library version and evidence hashes;
- random seed and deterministic replay metadata;
- solver tolerances, element families, mesh policy, load cases, and timestep policy;
- component library, baseline/control candidates, and compute budget;
- training/holdout or design/control partition where search is present.

Changing one of these after seeing a result invalidates admission and requires a new config identity or remedial work.

### 4.2 Common numerical gates

Unless a work preregisters a stricter domain-specific gate:

- exact artifact/config/schema identities: byte-identical SHA-256;
- finite values only; `NaN`, infinity, invalid state, and solver divergence are observable failures;
- global and per-interface force/moment relative residual: `<=1e-5`;
- energy-ledger relative residual: `<=1e-4`;
- comparable CAD/FreeCAD mass-property relative residual: `<=1e-6`;
- last-two mesh change for admitted response metrics: `<=5%`;
- event-time change under declared refinement: relative `<=1e-6` where failure localization is claimed;
- no penetration, clearance, or mate error beyond the declared geometry/interface tolerance;
- no hidden repair, silent clipping, default material, default load path, or substituted lower-fidelity result.

### 4.3 Evidence classes

Every report labels evidence as one of:

- `synthetic_verification`: validates implementation only;
- `toolchain_cross_check`: compares software paths that may share underlying geometry technology;
- `sourced_engineering`: traceable source with declared domain/condition/confidence;
- `independent_measurement`: extracted from the exact artifact by the declared independent route;
- `higher_fidelity_validation`: comparison against a stronger solver, experiment, or real data.

Only evidence classes explicitly allowed by a completion gate can support that claim.

### 4.4 Work-log and commit protocol

Before implementing each Work 081-086, create its separate EN/TH work-log plan and mark only that work `In progress`. On completion, create EN/TH result records containing changed files, decisions, exact commands, exit codes, relevant output, supporting/contradicting evidence, alternative explanations, missing evidence, confidence, and limitations.

Each completed work receives one scoped commit immediately after validation. Never use blanket staging. Inspect `git diff --cached --name-status`, run `git diff --cached --check`, commit, verify the hash, and run a post-commit replay. Do not push automatically.

## 5. Work 080 — Mechanical Assembly and Joint Kernel

### Objective

Represent how real parts are positioned and constrained, calculate the motion actually permitted by geometry/constraints, and reject assemblies that are misaligned, overconstrained, underconstrained, loose, interfering, or colliding through their declared motion.

### Entry gate

- Work 077 part/interface declarations pass;
- Work 078 exact part geometry/STEP identities exist;
- every assembly part has a local frame, persistent datums, typed interfaces, and tolerances;
- no Work 080 code assumes conventional wheel, suspension, steering, or powertrain layout.

### Proposed implementation artifacts

- `config/assembly/mechanical_assembly_joint_kernel_v1.json`;
- `src/formula_ultimate/assembly/joint_kernel.py` and package exports;
- `scripts/assembly/run_joint_kernel_acceptance.py`;
- `tests/test_joint_kernel.py`;
- bilingual `MECHANICAL_ASSEMBLY_JOINT_KERNEL_V1` contract/research record;
- `artifacts/work080/` manifests, motion samples, collision reports, and replay evidence.

Final filenames must be confirmed in the Work 080 implementation review; changes must be recorded, not silently substituted.

### Required capabilities

1. assemble by datum point, axis, plane, and interface-surface signature;
2. rigid, revolute, prismatic, and spherical joint constraints;
3. joint limits and declared home/reference state;
4. bearing-seat/shaft alignment, axial/radial clearance, and support spacing;
5. interference, minimum-gap, and continuous or conservatively bounded swept-motion checks;
6. fastener-preload declaration without claiming fastener capacity;
7. connection translational/rotational stiffness and compliance declaration;
8. constraint Jacobian/rank and realized six-DOF calculation;
9. deterministic canonical assembly, joint, and motion-evidence hashes.

### Preregistered experiment

- independent variables: mate type/count/order, part transforms, datum/axis position, joint limits, bearing spacing, clearance, tolerance, compliance, and motion coordinate;
- dependent variables: constraint rank, null-space DOFs, mate position/angular residual, coaxial error, clearance/gap, penetration, collision coordinate, and assembly hash;
- reference: one non-conventionality-neutral mechanism containing rigid, revolute, prismatic, and spherical examples in isolated fixtures plus one combined mechanism;
- controls: key-order permutation, mirrored frame, misaligned shaft, redundant two-bearing lock, missing constraint, excessive clearance, negative clearance, collision inside travel, wrong declared DOF, duplicate interface, missing datum, and non-finite transform.

### Implementation sequence

1. define exact assembly/joint schemas and canonical serialization;
2. implement frame transforms and right-handed datum resolution;
3. generate constraint equations and rank/null-space evidence;
4. implement joint limits and deterministic motion sampling/refinement;
5. add clearance, interference, and swept-volume collision checks;
6. add compliance/preload declarations as evidence only;
7. run isolated fixtures, combined reference, falsification controls, and replay;
8. document contradictory/missing evidence and freeze the admitted config.

### Completion gates

- calculated DOF count/type equals the reference declaration exactly;
- reference mate position residual `<=1e-6 m` and angular residual `<=1e-6 rad`, while always remaining inside stricter declared tolerances;
- coaxial bearing/shaft error and clearances remain inside declared limits;
- zero forbidden penetration beyond geometry tolerance throughout the declared motion envelope;
- over/underconstraint, looseness, misalignment, and collision controls reject for distinct causal codes;
- mapping-key permutation preserves exact identity; causal array/order/geometry changes alter identity;
- invalid evidence performs zero downstream state writes.

### Proposed validation commands

```powershell
python -m unittest tests.test_joint_kernel -v
python scripts/assembly/run_joint_kernel_acceptance.py --config config/assembly/mechanical_assembly_joint_kernel_v1.json --output artifacts/work080/evidence.json
python -m unittest discover -s tests -q
python -m compileall -q src scripts tests
```

### Non-claims and stop conditions

Do not claim bearing life, friction/wear, bolt/weld strength, dynamic vibration, crash response, or physical validation. Stop Work 080 if continuous collision cannot be bounded, constraint rank is numerically ambiguous under declared refinement, or the reference mechanism requires auto-alignment/repair.

## 6. Work 081 — STEP to FreeCAD Geometry Witness V2

### Objective

Independently import the exact canonical STEP artifacts and derive the physical inputs that downstream assembly and physics must use instead of manually typed substitutes.

### Entry gate

- Work 080 completed with stable assembly/interface/datum identities;
- exact per-part and assembly STEP hashes frozen;
- semantic interfaces have geometry signatures and datum witnesses that do not depend on transient face numbers.

### Proposed implementation artifacts

- `config/cad/step_freecad_geometry_witness_v2.json`;
- `src/formula_ultimate/components/geometry_witness.py`;
- `scripts/cad/inspect_geometry_witness_v2_freecad.py`;
- `scripts/cad/compare_geometry_witness_v2.py`;
- `tests/test_geometry_witness_v2.py`;
- bilingual `STEP_FREECAD_GEOMETRY_WITNESS_V2` report;
- `artifacts/work081/` FreeCAD JSON, FCStd, comparison, and replay evidence.

### Required measurements

- STEP SHA-256, part count, solid count, shape validity, and no-repair status;
- volume, material-linked mass, centre of mass, full inertia tensor, principal axes, and bounding box;
- hole/bore/shaft diameters, wall thickness samples/minima, section area/centroid/second moments/torsion proxy where supported;
- interface positions/orientations/signatures, joint axes, load/support/contact surfaces;
- part-to-part clearances, minimum gap, interference volume/depth, and motion-envelope witnesses;
- measurement method, resolution/tolerance, tool versions, report hash, and unsupported measurements.

### Preregistered experiment

- independent variables: part family, STEP export/reimport, measurement resolution, interface signature, transformed placement, and deliberate geometry mutations;
- dependent variables: measurement values, CAD-to-FreeCAD residuals, signature recovery, invalid/repair state, and report identity;
- controls: five Work 078 parts, Work 080 reference assembly, key-order replay, changed STEP byte, extra/missing solid, renamed/reordered faces, geometry-signature collision, thin-wall mutation, and deliberate interference.

### Implementation sequence

1. freeze exact STEP and declaration hashes;
2. import with FreeCAD in read-only/no-heal mode where exposed;
3. extract global mass properties and local feature measurements;
4. recover datums/interfaces by geometry signature plus spatial witness, never `Face17`;
5. measure clearance/interference and declared motion states;
6. compare against CadQuery/declaration evidence and classify shared-technology limitations;
7. bind measurement report hashes into the Work 079 geometry-witness contract;
8. run mutation/falsification corpus and exact replay.

### Completion gates

- imported STEP hash equals the frozen exporter hash exactly;
- part/solid counts and valid-solid state match declarations; any repair flag rejects;
- volume/mass/COM/inertia residual `<=1e-6` relative where directly comparable;
- interface/datum positions and axes remain within declared tolerances;
- every required semantic interface/load/contact region is uniquely recovered without face-number dependence;
- thickness/section measurements converge within the preregistered resolution study; proposed last-two change `<=1%` for smooth canonical fixtures;
- altered hash, solid count, signature ambiguity, missing region, or hidden repair fails closed;
- repeated FreeCAD run produces identical canonical measurement/report identity.

### Proposed validation commands

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\python.exe" scripts/cad/inspect_geometry_witness_v2_freecad.py --config config/cad/step_freecad_geometry_witness_v2.json --output-root artifacts/work081
python scripts/cad/compare_geometry_witness_v2.py --artifact-root artifacts/work081 --output artifacts/work081/comparison.json
python -m unittest tests.test_geometry_witness_v2 -v
python -m unittest discover -s tests -q
```

### Non-claims and stop conditions

CadQuery and FreeCAD may share OCCT technology, so agreement is a toolchain cross-check, not independent physical validation. Stop if semantic regions cannot be recovered without face numbers, measurements require hidden repair, or resolution sensitivity exceeds the frozen gate.

### Required evidence-remediation gate before Work 082 design use

Work 081 must replace Work 079's synthetic measurement arrays with `independently_measured` evidence. In addition, at least one material/process record used for a design-use structural claim must be sourced with condition/domain/confidence. If this evidence is unavailable, create a remedial work. Work 082 may test software coupling with synthetic fixtures but cannot complete a design-material or real-part capacity claim from them.

## 7. Work 082 — Geometry-to-Structural Physics Coupling

### Objective

Transfer exact geometry-witness regions and sourced engineering properties into a meshed structural solve, classify deformation/failure/numerical states, and propagate connection failure into the vehicle connection graph.

### Entry gate

- Work 081 exact independent measurement report passes;
- support/load/contact surfaces are uniquely recovered;
- material/process/measurement evidence satisfies the claim class being attempted;
- existing solver-acceptance fixtures for tension, bending, torsion, yield, fracture initiation, fatigue, buckling, and failure coupling remain passing.

### Proposed implementation artifacts

- `config/structural/geometry_structural_coupling_v1.json`;
- `src/formula_ultimate/structural/geometry_coupling.py`;
- `scripts/structural/run_geometry_structural_coupling.py`;
- `tests/test_geometry_structural_coupling.py`;
- bilingual `GEOMETRY_STRUCTURAL_COUPLING_V1` report;
- `artifacts/work082/` meshes, decks, solver files, parsed fields, convergence, and failure ledgers.

### Required pipeline

1. select exact support/load regions from Work 081 witnesses;
2. generate at least three declared mesh refinements without changing geometry;
3. assign exact Work 079 material identity and domain;
4. apply immutable load cases with force/moment provenance;
5. solve and parse displacement, strain, stress, plastic variables, reactions, and energies;
6. evaluate elastic deformation, yield/plasticity, ultimate-domain violation, fracture-domain violation, fatigue state, torsion, local/global buckling, and numerical failure;
7. map failure to typed connection state and remove/redistribute forbidden wrench paths;
8. emit deterministic result/failure/replay identities.

### Preregistered experiment

- independent variables: exact part geometry, thickness/section mutation, material record, mesh level/element family, load/support regions, load magnitude/direction, flaw/fatigue state, and connection topology;
- dependent variables: stiffness/compliance, stress/strain/displacement, reactions, energy, residuals, convergence, failure mode/location/time, transmitted wrench, and `DNF`/subsystem state;
- controls: analytical accepted fixtures, thicker/ thinner geometry, severed load path, missing surface, reversed load, below-yield load/unload, deliberate overload, fatigue crossing, buckling fixture, redundant/critical connection, and solver divergence injection.

### Completion gates

- exact geometry/material/load identities trace through mesh, deck, result, and failure ledger;
- force/moment residual `<=1e-5`, energy residual `<=1e-4`;
- last-two mesh change `<=5%` for admitted compliance, displacement, integrated reactions, and non-singular stress/failure metrics;
- thicker control may not be less stiff without a recorded geometric/mode explanation;
- severed path transmits no forbidden wrench;
- failure changes connection state and downstream response; critical path failure causes deterministic `DNF` where declared;
- unsupported fracture/fatigue/material domain rejects instead of assigning neutral capacity;
- solver divergence/invalid state is an experiment result with zero silent correction;
- exact replay under pinned tools/seeds.

### Proposed validation commands

```powershell
python scripts/structural/run_geometry_structural_coupling.py --config config/structural/geometry_structural_coupling_v1.json --artifact-root artifacts/work082 --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
python -m unittest tests.test_geometry_structural_coupling -v
python -m unittest discover -s tests -q
```

### Non-claims and stop conditions

Passing one bounded part/load family is not arbitrary-component strength, crashworthiness, fatigue life, or physical validation. Stop if convergence fails, reactions do not close, material domain is unsupported, critical regions are singular/unresolved, or failure does not causally alter the connection graph.

## 8. Work 083 — Ground-Interaction Module Candidate 001

### Objective

Create the first inspectable multi-part mechanical subsystem that carries ground forces and torque into structural mounts while allowing declared motion, braking, and steering/force-direction behavior without prescribing a conventional suspension or wheel architecture.

### Entry gate

- Works 080-082 completed;
- real-part claim uses design-eligible material/process/measurement evidence;
- allowed topology/function requirements and compute budget frozen before candidate generation.

### Proposed implementation artifacts

- `config/candidates/ground_interaction_candidate_001.json`;
- per-part CadQuery configs and exact STEP artifacts;
- complete subsystem STEP and FCStd;
- `src/formula_ultimate/subsystems/ground_interaction.py`;
- `scripts/candidates/build_ground_interaction_candidate_001.py`;
- `tests/test_ground_interaction_candidate_001.py`;
- bilingual candidate design/experiment report;
- `artifacts/work083/` assembly, motion, load-path, structural, and replay evidence.

### Functional requirements

- ground contact and positive/observable normal-force state;
- longitudinal and lateral force transfer;
- torque receipt/transmission and braking path;
- force-direction change where declared;
- vertical motion envelope;
- structural-mount load path;
- unwanted-DOF constraint;
- failure state that alters subsystem behavior.

### Preregistered experiment

- independent variables: topology, part count, joint locations/types, section geometry, wall thickness, material, bearing/support spacing, contact radius, motion ratio, and declared travel;
- dependent variables: mass/inertia, stiffness, stress/fatigue/buckling margins, steering/force-direction response, travel, torque efficiency, unsprung-equivalent inertia, clearance, and failure mode;
- controls: mirrored candidate, rigid/no-travel control, disconnected mount, blocked joint, seized bearing/connection, broken torque path, undersized section, contact-loss case, and replay.

### Implementation sequence

1. freeze functional requirements without selecting a conventional layout;
2. propose topology and separate part contracts;
3. build B-reps, interfaces, material/process assignments, and exact STEP hashes;
4. assemble with Work 080 joints and create FCStd evidence;
5. inspect with Work 081 and update only through new config identities before admission;
6. run kinematics, clearance, force/torque path, and Work 082 structural cases;
7. inject causal failures and propagate subsystem state;
8. run mirror/control/refinement/replay and produce candidate report.

### Completion gates

- FCStd/STEP shows separate physical parts, not one functional solid;
- calculated joint DOFs and travel equal declarations within Work 080 gates;
- unique continuous paths exist from ground forces to structural mounts and from braking/drive torque to contact;
- force/moment residual `<=1e-5`, energy residual `<=1e-4`;
- no forbidden interference through motion; ground clearance and service envelope pass declared tolerances;
- required structural cases converge under Work 082 gates;
- each injected break/seizure changes measurable behavior and required critical failure can cause subsystem failure/`DNF`;
- mirror/control results follow declared symmetries or record a causal asymmetry;
- exact seed/config replay reproduces declaration, STEP, assembly, and evidence hashes.

### Non-claims and stop conditions

Do not call this a validated suspension, wheel, steering, brake, tyre, or production subsystem. Stop if the only passing solution relies on a conventional topology hard-coded by the evaluator, synthetic design evidence, hidden geometry edits, or an unresolved load/torque path.

## 9. Work 084 — Energy Conversion and Torque-Path Candidate 001

### Objective

Replace the abstract energy-converter box and scalar ratio with real geometry, mounts, supports, torque-transfer interfaces, losses, braking-energy route, and thermal rejection while retaining technology neutrality.

### Entry gate

- Work 083 ground-interaction torque/contact interface frozen;
- candidate declares a specific technology and evidence domain without making the evaluator prefer a historical powertrain layout;
- energy-equivalent race profile, onboard pre-race energy, and recovery accounting remain enforced.

### Proposed implementation artifacts

- `config/candidates/energy_torque_path_candidate_001.json`;
- separate store/converter/shaft-or-equivalent/support/coupling/housing/cooling part STEP files;
- assembly STEP and FCStd;
- `src/formula_ultimate/subsystems/energy_torque_path.py`;
- `scripts/candidates/build_energy_torque_path_candidate_001.py`;
- `tests/test_energy_torque_path_candidate_001.py`;
- bilingual torque/energy/thermal experiment report;
- `artifacts/work084/` torque, speed, bearing, structural, energy, thermal, failure, and replay ledgers.

### Required functions

- energy-store interface and mass/state identity;
- converter geometry and real mounting load path;
- input/output shaft or mechanically equivalent torque path;
- torque multiplication/transformation mechanism and supports;
- bearings or alternative reaction supports;
- output coupling to Work 083;
- housing plus lubrication/cooling interfaces;
- braking-energy path and conserved recovery source;
- explicit loss and thermal-rejection ledger.

### Preregistered experiment

- independent variables: declared technology, topology, ratio/mechanism geometry, shaft/equivalent section, support spacing, speed/torque schedule, efficiency/loss model, cooling interface, and failure injection;
- dependent variables: torque equilibrium, torsional stress/twist, bearing/support reaction, housing deformation, rotational limit, delivered power, energy residual, loss/heat rate, required rejection, and failure propagation;
- controls: locked converter, seized support, broken coupling, zero-loss exploit, efficiency over one, reversed torque, overspeed, inadequate cooling, disconnected housing reaction, and equal-energy replay.

### Completion gates

- continuous geometry/interface torque path from converter to Work 083 contact;
- torque/reaction residual `<=1e-5` and energy residual `<=1e-4`;
- no efficiency outside `[0,1]`; recovered energy has an observable conserved source and losses;
- shaft/equivalent, support, and housing structural cases pass Work 082 gates or fail observably;
- speed, temperature, and material domains are enforced without clipping;
- heat-generation and rejection requirements close for the declared duration;
- seized/broken controls remove or redirect torque and propagate failure deterministically;
- same energy-equivalent profile and compute/evidence opportunity as controls/baselines.

### Non-claims and stop conditions

Do not claim a validated motor, engine, battery, fuel, transmission, cooling system, or technology superiority. Stop on undeclared energy, energy creation, unsupported property evidence, missing reaction path, unclosed heat ledger, or evaluator bias toward a conventional technology/layout.

## 10. Work 085 — Load Structure, Packaging, and Thermal Integration

### Objective

Create a geometry-causal load structure and package Works 083/084 plus control/routing/thermal interfaces without interference, replacing the abstract `load_spine` with an agent-designed structure caused by loads and spatial constraints.

### Entry gate

- Works 083 and 084 complete with frozen mount/interface/motion/heat identities;
- whole-system load cases and packaging envelopes preregistered;
- service/removal and routing requirements declared before topology generation.

### Proposed implementation artifacts

- `config/candidates/load_structure_integration_001.json`;
- separate structure/mount/routing/support STEP artifacts, complete integration STEP, and FCStd;
- `src/formula_ultimate/subsystems/load_structure_integration.py`;
- `scripts/candidates/build_load_structure_integration_001.py`;
- `tests/test_load_structure_integration_001.py`;
- bilingual packaging/load/thermal report;
- `artifacts/work085/` interference, service path, routing, structural, thermal, failure, and replay evidence.

### Required functions and cases

- real mounting geometry for every subsystem;
- no forbidden interference at static and motion-envelope states;
- declared service/removal swept paths;
- power/control/fluid routing with bend/clearance limits;
- heat-source and heat-rejection interfaces;
- ground clearance and external envelope;
- acceleration, braking, cornering, combined, bump/vertical, aero where admitted, and torque-reaction loads;
- bending, torsion, buckling, fatigue-domain, and mount-failure evaluation.

### Preregistered experiment

- independent variables: structural topology, member/skin sections, material, mount positions, subsystem placement, routing, thermal-interface location, and service path;
- dependent variables: total mass/COM/inertia, package volume, clearance/interference, service feasibility, route length/loss, temperature/heat rejection, stiffness, stress/fatigue/buckling margins, mount reactions, and failure mode;
- controls: box-like placeholder baseline, disconnected mount, blocked service path, routing collision, inadequate thermal rejection, asymmetric load, weakened mount, thin/buckling structure, and mirror/replay.

### Completion gates

- every subsystem has unique, inspectable, geometry-realized mount/load/torque/thermal interfaces;
- no forbidden interference beyond declared tolerance through all motion/service envelopes;
- routing and service paths pass clearance/bend/tool rules or fail explicitly;
- mass/COM/inertia come from Work 081 geometry evidence;
- all declared load cases close force/moment residual `<=1e-5` and energy residual `<=1e-4`;
- structural mesh/convergence/failure satisfies Work 082;
- heat generation, storage, transfer, and rejection close for declared duration;
- weakened/disconnected controls cause the expected structural/subsystem consequence;
- exact replay and no result-conditioned topology repair.

### Non-claims and stop conditions

Do not call this a chassis, monocoque, crash structure, cooling package, or production assembly unless those exact claims are independently validated. Stop if packaging passes only by overlap suppression, service requirements are deleted after results, heat is discarded without a sink, or the structure is merely a decorative vehicle-shaped box.

## 11. Work 086 — Whole Mechanical Vehicle Candidate 001

### Objective

Integrate every admitted subsystem into one deterministic candidate and decide whether it is ready to enter bounded whole-vehicle research under the declared Level 0/evidence gates.

### Entry gate

- Works 080-085 completed with no unresolved numerical, identity, material, interface, load-path, energy, packaging, or thermal blocker;
- final training/control/admission cases frozen;
- no geometry or evidence mutation allowed after the first admitted whole-vehicle run.

### Mandatory artifacts

- individual STEP for every part and exact per-file hashes;
- complete assembly STEP and FreeCAD FCStd;
- assembly tree and joint/DOF manifest;
- material/process/measurement manifest;
- mass/COM/full-inertia report;
- clearance/interference/motion/service report;
- structural load-case and convergence report;
- torque/power/energy/thermal ledger;
- failure-propagation and `DNF` report;
- deterministic seed/config/toolchain/replay manifest;
- integrated Level 0 result plus mirrored/control candidate evidence.

### Proposed implementation artifacts

- `config/candidates/whole_mechanical_vehicle_candidate_001.json`;
- `src/formula_ultimate/experiments/whole_mechanical_vehicle_candidate.py`;
- `scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py`;
- `tests/test_whole_mechanical_vehicle_candidate_001.py`;
- bilingual admission/result report;
- `artifacts/work086/` complete immutable evidence bundle.

### Mandatory admission cases

1. static support and stable contact;
2. straight acceleration;
3. braking;
4. steady cornering;
5. combined braking/cornering;
6. bump/vertical event and motion envelope;
7. converter/drive torque reaction;
8. declared thermal-duration case;
9. single critical connection failure;
10. redundant connection/control failure where declared;
11. mesh/timestep/refinement and exact replay;
12. mirrored/control candidate;
13. integrated Level 0 lap/race gate using geometry-derived inputs.

### Preregistered experiment

- independent variables: complete topology/config, seed, control/mirror identity, load/admission case, refinement level, and injected failure;
- dependent variables: artifact validity, mass properties, contacts/DOFs, residuals, structural/thermal/energy margins, failures, progress/lap/race outcome, `DNF`, compute use, and complete evidence identity;
- controls: mirrored candidate, deliberate weak/disconnected connection, heavy feasible control, no-hidden-repair exploit control, energy exploit control, geometry-hash mutation, unsupported-evidence control, and replay.

### Completion gates

- all mandatory artifacts exist, cross-reference exact identities, and replay;
- no placeholder functional box substitutes for required physical parts/paths;
- every external load closes through geometry to contact/support and every drive/brake torque closes through real interfaces;
- mass/COM/inertia, clearances, sections, lever arms, and interfaces are geometry-derived;
- all admitted cases meet the common numerical gates or produce a declared causal failure/`DNF`;
- deliberate weak/disconnected/exploit controls reject or fail for the expected reason;
- no training/control/admission case, solver tolerance, evidence class, or geometry is changed after observing the admitted result;
- exact repeat reproduces the immutable evidence bundle hashes;
- final verdict is exactly `ready_for_bounded_whole_vehicle_research` or `not_ready`, with blockers.

### Proposed validation commands

```powershell
python scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py --config config/candidates/whole_mechanical_vehicle_candidate_001.json --artifact-root artifacts/work086
python -m unittest tests.test_whole_mechanical_vehicle_candidate_001 -v
python -m unittest discover -s tests -q
python -m compileall -q src scripts tests
```

### Non-claims and stop conditions

Even a `ready` verdict authorizes only bounded research. It does not prove real race completion, safety, manufacturability, legality, novelty, optimized superiority, or physical validity. Stop and return `not_ready` for any missing artifact, stale hash, unsupported evidence, non-convergence, unclosed force/energy/thermal path, hidden repair, unfair control, or non-reproducible result.

## 12. Program stop/go review

### Gate A — Real part mechanics

Works 080-082 pass with calculated DOFs, independent geometry measurements, design-eligible evidence for any capacity claim, converged structural response, and causal failure propagation. Passing Gate A is the earliest point at which a bounded tested item may be called a geometry/material/load-causal research part.

### Gate B — Functional mechanical subsystems

Works 083-084 pass with real multi-part ground and torque/energy paths. Passing Gate B permits integration work; it does not validate either subsystem physically.

### Gate C — Vehicle-scale integration

Work 085 passes packaging, load structure, routing, and thermal integration without hidden overlap or discarded loads/heat.

### Gate D — Whole-vehicle research readiness

Work 086 returns the exact admission verdict. Any rejected hypothesis, missing real evidence, or solver limitation creates a new remedial work. No gate may be weakened after observing results.

## 13. Definition of progress visible to the user

- now: five viewable real B-rep/STEP test-part shapes, but not design-eligible vehicle parts;
- after Work 080: parts visibly assembled with verified calculated joints/DOFs;
- after Work 081: FreeCAD-visible parts with independently extracted dimensions, mass properties, interfaces, and clearances;
- after Work 082: bounded parts visibly deform/fail from geometry/material/load evidence;
- after Work 083: first real multi-part ground-interaction subsystem in FCStd;
- after Work 084: real geometry torque/energy path connected to that subsystem;
- after Work 085: integrated load structure and packaging at vehicle scale;
- after Work 086: Whole Mechanical Vehicle Candidate 001 evidence bundle and research-readiness verdict.
