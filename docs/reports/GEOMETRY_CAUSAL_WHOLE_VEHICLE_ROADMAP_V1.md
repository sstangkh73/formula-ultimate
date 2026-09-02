# Geometry-Causal Whole-Vehicle Roadmap V1: Works 077-086

Thai companion: `GEOMETRY_CAUSAL_WHOLE_VEHICLE_ROADMAP_V1.th.md`

## Destination and claim boundary

A candidate becomes a **whole mechanical vehicle ready to begin whole-vehicle research** only when it has separable physical parts rather than one functional box per role; every part has geometry, material, interface, and tolerance evidence; assembly joints and DOFs are checkable; force and power paths are realized by geometry; STEP/FreeCAD supplies mass, centre of mass, inertia, thickness, section properties, and moment arms; loads enter a mesh and produce stress/deformation; yield, fracture, fatigue, torsion, buckling, and connection failures can occur; damage propagates into the vehicle and may cause `DNF`; seed/config replay is deterministic; and geometry cannot be changed after observing an admitted result.

This destination is research readiness, not physical validation. Higher-fidelity and real-data comparison remain mandatory before stronger claims.

```text
Functional requirement
  -> agent proposes topology and parts
  -> parametric 3D B-rep
  -> assembly joints and interfaces
  -> STEP hash
  -> independent FreeCAD inspection
  -> geometry-derived physics inputs
  -> FEA / kinematics / torque / thermal tests
  -> failure or survival
  -> mutation and deterministic replay
  -> whole-vehicle Level 0 admission
```

## Three-work execution cadence

Implementation proceeds in bounded batches: `077-079`, `080-082`, `083-085`, then `086`. “Three at a time” limits active scope; it does not remove dependencies or merge evidence. Each work is executed and committed sequentially after its own validation passes. A rejected hypothesis or blocked dependency creates a new remedial work rather than weakening a gate. No automatic push is authorized.

## Work 077 — Geometry-Causal Part Contract V1

Define the minimum formal part declaration: identity, function tags, ordered feature provenance, material record identity, local frame, datums/reference axes, typed interfaces, load/application regions and path, allowed manufacturing process, tolerances, minimum feature size, parameter provenance, and claim boundary. Initial interfaces cover fixed, revolute, prismatic, spherical, bearing, shaft/spline, bolted, welded, ground, thermal, and electrical/fluid intent.

Controls reorder keys and inject unknown fields/units, missing material/interface/load path, `NaN`, negative thickness, invalid tolerance/frame/provenance, and unsupported interfaces. Success requires deterministic canonical bytes/hash and exact fail-closed rejection. Passing defines what a declared part is; it does not prove geometry, material, manufacturing, or strength.

## Work 078 — Parametric B-rep Feature Grammar V1

Create bounded SI CAD instructions for sketch profile, extrude, revolve, pocket/cut, through hole, stepped bore, shaft shoulder, rib/web, shell/wall thickness, linear/circular pattern, bounded fillet/chamfer, and boolean union/subtract/intersect. Every operator has explicit parameter bounds, provenance, solid-validity checks, and rejection of zero thickness and self-intersection.

The admitted corpus contains at least a shaft, bracket, hollow housing, ribbed plate, and hub-like rotating part. Same config/toolchain replay must reproduce the same canonical STEP hash. Passing enables real single-part design within the admitted grammar; it does not validate arbitrary CAD topology, structural capacity, or manufacturing feasibility.

## Work 079 — Engineering Material and Manufacturing Contract

Connect evidence-bearing material records to physical parts. Records declare density, Young's modulus, Poisson ratio, shear modulus, yield/ultimate strength, fracture toughness, fatigue/S-N evidence or explicit absence, thermal conductivity, heat capacity, thermal expansion, allowable temperature range, source, confidence, and domain. Manufacturing records declare minimum wall, hole, ligament/web, tool access, machining/bend radius, unsupported-feature policy, tolerance class, process, and evidence.

Independent variables include material/process selection and geometry dimensions; dependent outputs include admission, mass/stiffness/strength/thermal property availability, and manufacturing violations. Controls cover inconsistent elastic constants, impossible strength ordering, missing units/source/domain, unsupported fatigue claims, thin walls, small holes/webs, tool-access failure, and invalid tolerances. Geometry may become thinner only while receiving its causal mass, stiffness, stress, buckling, fatigue, thermal, and manufacturing consequences. Passing prohibits a floating “maximum force” substitute for material/geometry evidence.

## Work 080 — Mechanical Assembly and Joint Kernel

Implement datum/axis/surface mating; rigid, revolute, prismatic, and spherical joints; limits; bearing alignment; axial/radial clearance; interference and minimum gap; fastener preload declaration; connection stiffness/compliance; and intended-DOF calculation.

Falsification includes misaligned shafts, overconstrained two-bearing arrangements, collision through the motion envelope, excessive tolerance looseness, and realized DOF different from declaration. Passing distinguishes fixed, sliding, rotating, and colliding behavior. It does not validate bearing life, fastener/weld strength, friction, wear, or full multibody dynamics.

## Work 081 — STEP to FreeCAD Geometry Witness V2

Independently inspect the exact CadQuery STEP hash and extract solid count, volume, mass, centre of mass, inertia tensor, bounding box, principal axes, hole/shaft diameters, local wall thickness, section properties, interface positions, joint axes, load/contact surfaces, and clearance/interference. Part/solid counts and mass properties must close within preregistered tolerances with no hidden geometry repair.

Semantic interfaces must survive exchange through geometry signatures and datum witnesses rather than fragile face numbers such as `Face17`. Passing removes manually typed motion ratios, lever arms, shaft radii, and mass where CAD measurement is possible. It does not make OCCT-family cross-checks fully independent physics validation.

## Work 082 — Geometry-to-Structural Physics Coupling

Select support/load surfaces from witnesses, mesh exact geometry, run a mesh-convergence study, apply Work 079 materials and declared load cases, parse stress/strain/displacement/reactions, evaluate failure, and feed state into the connection graph. Observable modes include elastic deformation, yield/plasticity, ultimate overload, fracture-domain violation, fatigue, torsion, local/global buckling, and solver divergence/invalid state.

Controls require thicker geometry not to become less stiff without explanation, severed load paths not to transfer force, reaction closure, mesh convergence, failed connections not to retain forbidden load transfer, and numerical failure never to be silently repaired. Passing makes “too thin and broke” geometry/material/load causal within tested cases; it is not whole-vehicle or real-world validation.

## Work 083 — Ground-Interaction Module Candidate 001

Build the first multi-part subsystem without prescribing conventional suspension or wheel architecture. It must contact the ground; carry normal, longitudinal, and lateral force; receive/transmit torque; redirect force; permit declared vertical motion; transfer force to structural mounts; brake; and constrain unwanted DOFs.

Independent variables are topology, part count, joint positions, section geometry, thickness, material, support spacing, contact radius, and motion ratio. Dependent measures are mass, stiffness, stress/fatigue/buckling margin, steering response, travel, torque efficiency, unsprung-equivalent inertia, and failure mode. Success is an inspectable FCStd assembly of real parts with verified joint motion and a continuous ground-to-structure load path.

## Work 084 — Energy Conversion and Torque-Path Candidate 001

Replace an abstract `energy_converter` box and numeric ratio with declared energy-store interface, converter geometry and mounting, input/output shaft or equivalent, torque multiplication, bearings/supports, output coupling, housing, lubrication/cooling interfaces, braking-energy path, and thermal-loss ledger. Technology remains neutral, but each candidate must name its technology and evidence.

Test torque equilibrium, shaft torsion, bearing reactions, housing deformation, rotational-speed limit, energy conservation, efficiency/loss, heat rejection, and seized/broken connection injection. Success requires torque to traverse real parts and interfaces from converter to the ground-interaction module. It does not establish a physically validated motor/engine/battery/fuel system.

## Work 085 — Load Structure, Packaging, and Thermal Integration

Replace `load_spine` with an agent-designed load structure supporting every subsystem through real mounts. Require interference-free placement, declared service/removal paths, power/control/fluid routing, heat-source/rejection interfaces, ground clearance, motion envelopes, and braking/cornering/bump/torque-reaction load transfer. Evaluate bending, torsion, buckling, fatigue, and mount failure.

Success is a structure caused by load paths and packaging constraints rather than a vehicle-looking box. It does not prove crashworthiness, occupant safety, production assembly, cooling correlation, or regulatory compliance.

## Work 086 — Whole Mechanical Vehicle Candidate 001

Integrate all subsystems. Minimum artifacts are individual STEP files, complete assembly STEP, FCStd, assembly tree, joint/DOF manifest, material manifest, mass/COM/inertia report, interference report, structural load-case report, torque/power/energy ledger, failure-propagation report, deterministic replay manifest, and Level 0 result.

Admission cases include static support, acceleration, braking, steady cornering, combined braking/cornering, bump/vertical event, torque reaction, thermal duration, one-connection failure, refinement/replay, and mirrored/control candidate. Success yields a mechanical vehicle with real parts ready to begin whole-vehicle research. It remains unvalidated until higher-fidelity and real-data evidence pass.

## Common experimental contract

Controls remain SI units, toolchain version, material-library version, random seed, solver tolerances, mesh policy, load cases, component library, compute budget, and baseline candidate. Every work records independent/dependent variables, controls, metrics, success/failure criteria, supporting evidence, contradicting evidence, alternative explanations, missing evidence, residuals, solver failures, and confidence.

Every completed work must have EN/TH plan and result records, unit/acceptance tests, exact commands and exit codes, explicit staged-scope inspection, `git diff --cached --check`, and an immediate scoped commit. Geometry/config is frozen before admitted results; no result-conditioned hidden geometry edits are allowed.
