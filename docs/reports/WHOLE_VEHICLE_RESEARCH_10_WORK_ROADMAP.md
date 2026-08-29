# Whole-Vehicle Research: Ten-Work Roadmap

Thai companion: `WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.th.md`

## Purpose and current boundary

This roadmap defines the minimum ten validated work items between the current repository and a bounded whole-vehicle design-search pilot. It does not promise that ten items will be sufficient: a rejected hypothesis or solver limitation creates a new remedial work item rather than a relaxed gate.

Current evidence supports a deterministic coupled Level 0 reference, a bounded component `3D -> STEP -> FreeCAD -> Level 0` route, solver acceptance for tension, beam bending, and solid-shaft torsion, ideal eigenvalue buckling, and precritical nonlinear imperfection response. Work 039 rejected the full-range near-critical mesh-convergence and imperfection-shape-robustness hypotheses. Loaded-interface transfer, nonlinear material failure, connection failure coupling, and arbitrary whole-vehicle geometry remain unvalidated.

Execution dependency:

```text
041 numerical convergence
  -> 045 loaded interface
042 plasticity -> 043 fracture
              -> 044 fatigue
043 + 044 + 045 -> 046 failure coupling
046 -> 047 whole-vehicle grammar
047 + coupled Level 0 -> 048 vehicle load cases
048 -> 049 fixed-topology end-to-end baseline
049 -> 050 bounded search pilot and readiness review
```

All SI values and numeric gates below are preregistration proposals. Each work must pin its final config before its first admitted run and may not relax a gate after observing the result.

## Work 041 — Near-Critical Mesh and Element Verification

### Objective and dependency

Resolve the Work 039 numerical-convergence rejection before any post-buckling or vehicle structural claim. Depends on Works 037-039.

### Experiment

- independent variables: C3D4 mesh sizes `1.0`, `0.8`, and `0.65 mm`; a C3D10 route with a declared comparable degree-of-freedom budget; absolute compression `1857.580`, `2600.612`, and `3157.886 N` (`0.50`, `0.70`, and `0.85` of the Work 037 fine-mesh `Pcr=3715.160 N`);
- dependent variables: eigenvalue `Pcr`, nonlinear tip amplification, stress, strain energy, reaction closure, solver iterations, memory, wall time, and artifact hashes;
- controls: Work 039 geometry/material/support, `e0=0.1 mm`, cantilever eigenmode imperfection, fixed absolute loads, solver version, and output parser;
- falsification: keep the high-load case even if it rejects convergence; do not normalize each mesh by its own `Pcr` when computing the primary mesh-change metric.

### Implementation and deliverables

Add a higher-order mesh/deck route, element-aware result contract, deterministic launcher, unit fixtures, ignored solver evidence, and bilingual numerical-verification report.

### Completion gate

- all declared cases produce complete finite evidence and reaction residual `<=1e-5`;
- last-two C3D4 amplification change `<=5%` at every absolute load;
- refined C3D4 versus admitted C3D10 amplification difference `<=5%`;
- eigenmode secant error `<=15%` and no unexplained mode-family change;
- failure or non-convergence is recorded without substituting a lower load.

### Non-claim

Passing verifies precritical numerical adequacy for this fixture only. It is not post-buckling capacity, a safety factor, or proof that C3D4 is adequate for every vehicle part.

## Work 042 — Yield and Plasticity Solver Acceptance

### Objective and dependency

Verify that stress exceeding a declared yield law produces plastic strain, residual deformation, and plastic-work accounting instead of unlimited linear-elastic strength. Depends on Work 034; it may proceed in parallel with Work 041 but cannot enter vehicle fitness until Work 041 closes.

### Experiment

- independent variables: load/unload amplitude, hardening law, mesh, and monotonic versus reversed loading;
- dependent variables: yield-onset load, tangent stiffness, plastic strain, residual displacement, elastic/plastic energy, reactions, and convergence;
- controls: uniform tension coupon, SI geometry, temperature, strain rate, boundary surface, and synthetic material identity;
- fixtures: a pinned synthetic bilinear law (`E=70 GPa`, proposed `sigma_y=250 MPa`, proposed tangent `Et=1 GPa`) for solver verification plus a separately sourced material record before design use.

### Implementation and deliverables

Implement versioned elastic-plastic material records, CalculiX `*PLASTIC` deck generation, load/unload steps, multi-step evidence parsing, analytical bilinear references, negative controls, and bilingual report.

### Completion gate

- yield-onset error `<=2%`, post-yield tangent error `<=5%`, and residual-strain error `<=5%` against the declared bilinear reference;
- reaction residual `<=1e-5` and energy-ledger residual `<=1e-4`;
- below-yield control returns negligible plastic strain; missing/unsourced design material cannot enter fitness;
- mesh last-two change in nominal response `<=5%`.

### Non-claim

The synthetic law validates implementation, not real alloy allowables, temperature/rate effects, cyclic plasticity, fracture, or component safety.

## Work 043 — Fracture-Initiation Evidence

### Objective and dependency

Detect fracture initiation from a declared flaw and toughness record without treating a singular element peak as physical proof. Depends on Work 042 and the tension/bending acceptance fixtures.

### Experiment

- independent variables: crack length, nominal tension, thickness regime, mesh near the flaw, and toughness;
- dependent variables: `K_I` or another preregistered fracture parameter, initiation load, reaction/energy residuals, mesh sensitivity, and failure classification;
- analytical reference: `K_I = Y sigma sqrt(pi a)` for a declared geometry-factor domain;
- controls: flaw geometry, plane-stress/plane-strain assumption, material state, load surface, gauge definition, and no hidden crack healing.

### Implementation and deliverables

Add a fracture-material record with provenance, cracked-coupon grammar, fracture-parameter evaluator, initiation event contract, deliberate invalid-domain fixtures, and bilingual report. If the selected solver cannot provide admissible fracture evidence, record that limitation and use an independently verified evaluator rather than element deletion by fiat.

### Completion gate

- initiation-load error `<=5%` inside the analytical fixture domain;
- last-two refinement change `<=5%` for the admitted fracture parameter, not raw singular peak stress;
- exact rejection for missing flaw/toughness/thickness-regime evidence;
- reaction residual `<=1e-5`, energy residual `<=1e-4`, and deterministic event identity.

### Non-claim

This verifies initiation only unless stable/unstable crack propagation, path, and dissipated fracture energy are separately validated. It does not prove crashworthiness.

## Work 044 — Fatigue Damage and Life Acceptance

### Objective and dependency

Convert a load history into observable cumulative damage and a localized fatigue-failure event. Depends on Work 042; fracture initiation from Work 043 remains a separate mechanism.

### Experiment

- independent variables: constant/variable amplitude histories, mean stress, cycle count, material curve, and sequence;
- dependent variables: counted cycles, alternating/mean stress, per-bin damage, cumulative `D`, predicted life, event cycle, and uncertainty;
- controls: S-N or strain-life record, correction rule, rainflow version, temperature, surface/notch factors, and no damage clipping;
- analytical references: constant-amplitude life and Miner accumulation `D=sum(n_i/N_i)` within its declared limitations.

### Implementation and deliverables

Implement immutable fatigue records, deterministic rainflow counting, mean-stress correction, damage ledger, event localization, exact replay tests, deliberate overload/underload controls, and bilingual report.

### Completion gate

- exact cycle-count fixtures and constant-amplitude damage error `<=1%`;
- cumulative-damage arithmetic and replay are exact for the same input record;
- failure is emitted at the first admitted `D>=1` crossing without resetting or silently clipping damage;
- missing curve-domain or extrapolated stress is rejected/marked unsupported; uncertainty is reported, not hidden.

### Non-claim

Miner/S-N acceptance is not crack-growth validation, multiaxial fatigue proof, or a real component service-life claim without sourced material/process/environment data.

## Work 045 — Loaded Interface and Joint Load Path

### Objective and dependency

Prove that force and moment enter through one finite interface, flow through material, and close at other declared interfaces. Depends on Work 041 and the tension/bending/torsion fixtures.

### Experiment

- independent variables: interface geometry, hole/fastener arrangement, load direction and eccentricity, mesh, and support compliance;
- dependent variables: interface resultants, compliance, strain energy, nominal ligament/bearing stresses, load share, reaction closure, and field continuity;
- controls: persistent CAD-to-mesh interface tags, material, load/support surfaces, non-singular gauges, and topology-neutral interface definitions;
- negative controls: broken ligament, missing support, duplicated load tag, zero-area interface, and disconnected solid.

### Implementation and deliverables

Create `loaded_interface_plate_v1`, a constrained geometry grammar, FreeCAD interface verification, CalculiX surface mapping, resultant/energy parser, boundary-sensitivity matrix, negative controls, and bilingual report.

### Completion gate

- exact interface identity survives CAD, STEP, FreeCAD, mesh, and result stages;
- force and moment residuals `<=1e-5`, energy residual `<=1e-4`;
- last-two mesh change `<=5%` for compliance and integrated interface resultants;
- boundary-condition sensitivity is measured and any preregistered `>10%` response change rejects transferability;
- all disconnected/malformed controls fail closed.

### Non-claim

Passing one interface plate does not validate arbitrary bolts, welds, adhesives, contact friction, preload, manufacturing tolerances, or a vehicle chassis.

## Work 046 — Structural Failure Coupling and DNF

### Objective and dependency

Couple yield/fracture/fatigue/interface evidence into a typed connection state so a failed load path stops or redistributes force and can cause subsystem failure or `DNF`. Depends on Works 042-045 and the coupled transaction/failure system through Work 030.

### Experiment

- independent variables: failure mechanism, event time/load, redundant versus critical connection topology, timestep, and arbitration ties;
- dependent variables: `intact -> degraded -> failed` state, transmitted wrench, redistribution, stored/dissipated energy, event time, subsystem state, and race outcome;
- controls: identical pre-failure state, deterministic seed, connection graph, failure thresholds, and energy policy;
- falsification: critical connection failure must not leave the original force path active, erase elastic energy, or let the vehicle finish through a disconnected required path.

### Implementation and deliverables

Add typed structural-health state, event localization, connection-wrench adapter, redistribution/no-path logic, energy ledger, `DNF` arbitration, replay metadata, negative tests, and bilingual report.

### Completion gate

- failed connections transmit no forbidden wrench after the localized event;
- redistributed force/moment residual `<=1e-5` and energy residual `<=1e-4`;
- event time converges within relative `1e-6` under timestep refinement;
- critical failure produces deterministic `DNF`; redundant topology either re-equilibrates within gates or fails observably;
- same inputs replay exactly and invalid evidence performs zero state writes.

### Non-claim

This is a verified coupling policy, not proof of real fracture dynamics, crash energy absorption, occupant safety, or repairability.

## Work 047 — Topology-Neutral Whole-Vehicle CAD and Assembly Grammar

### Objective and dependency

Represent a complete 3D vehicle candidate without prescribing a conventional car shape or fixed component count, while requiring every mass, contact, connection, and energy path to be explicit. Depends on Work 046 contracts and the existing CAD evidence route.

### Experiment

- independent variables: component count/type, geometry parameters, connection graph, contact arrangement, placement, and material assignment;
- dependent variables: valid-solid status, interface match, collision/keep-out violations, envelope, ground clearance, mass, center of mass, inertia, connectivity, and artifact identity;
- controls: component library/version, global coordinate frame, SI units, allowed operations, numerical resolution, and no hidden geometry repair;
- negative controls: floating component, overlapping protected volumes, unmatched interface, disconnected required path, invalid solid, and massless energy component.

### Implementation and deliverables

Create versioned vehicle/assembly schemas, topology-neutral grammar, deterministic candidate manifest, multi-component STEP export, FreeCAD assembly measurement, connection/contact tags, mass/inertia aggregation, invalid-case corpus, and bilingual report.

### Completion gate

- every admitted candidate has complete typed paths from energy source to propulsion and from external loads to supports/contact interfaces;
- all components are valid solids with persistent identities and exact STEP hashes;
- FreeCAD versus independent component-sum mass/center/inertia residuals `<=1e-6` relative where mathematically comparable;
- interface/envelope/keep-out/contact rules fail closed without auto-repair;
- candidate replay regenerates identical declarations and evidence hashes under pinned tools.

### Non-claim

Geometric admission does not prove structural feasibility, aerodynamics, cooling, manufacturability, safety, race completion, novelty, or superiority.

## Work 048 — Whole-Vehicle Load Cases and Structural Coupling

### Objective and dependency

Transform coupled Level 0 race states into balanced, traceable structural load cases on the complete assembly. Depends on Work 047, Work 046, and the coupled vehicle through Work 030.

### Experiment

- independent variables: circuit profile/evidence class, speed, acceleration, braking, cornering, aero state, grade, contact state, energy mass state, and selected time;
- dependent variables: component/interface forces and moments, inertial loads, load combinations, equilibrium residuals, structural response, failure margin/event, and provenance;
- controls: one immutable race snapshot per case, coordinate transforms, gravity, mass/inertia evidence, contact/aero adapter versions, and training/holdout partition;
- cases: straight acceleration, braking, steady cornering, combined manoeuvre, bump/load-transfer extreme, aero-load extreme, and thermal/mass-state extremes where supported.

### Implementation and deliverables

Add critical-state extraction, immutable load-case manifests, body/component coordinate transforms, inertia relief or declared supports, surface-load mapping, multi-case FEA orchestration, holdout partition, equilibrium audit, and bilingual report.

### Completion gate

- every applied structural wrench traces to one immutable Level 0 snapshot and exact geometry/material identity;
- global and per-interface force/moment residuals `<=1e-5`;
- mapped mass/inertia agree with FreeCAD evidence within `1e-6` relative;
- training/holdout cases are frozen before candidate search;
- unsupported dynamics/contact/aero evidence rejects promotion rather than receiving a neutral numeric default.

### Non-claim

Initially admitted quasi-static equivalent cases are not transient crash, vibration, random road, CFD, tyre-test, or physical-track validation.

## Work 049 — Fixed-Topology End-to-End Whole-Vehicle Baseline

### Objective and dependency

Run one reviewed fixed-topology vehicle through the complete evidence chain before allowing design search. Depends on Work 048 and all structural/failure gates.

### Experiment

- independent variables: pinned baseline design, declared training/holdout load cases, mesh level, timestep, and circuit/environment evidence class;
- dependent variables: CAD validity, mass/inertia, structural margins/events, energy/thermal state, race completion or `DNF`, convergence, compute cost, and replay hashes;
- controls: no geometry mutation, fixed solver/settings, fixed seeds, fixed component library, and explicit unsupported-evidence states;
- falsification: deliberately weakened/disconnected variants must fail structurally or `DNF`; a heavy but feasible control checks that mass optimization is not the only path to passing.

### Implementation and deliverables

Create a fixed baseline manifest, end-to-end orchestrator for `3D -> STEP -> FreeCAD -> load cases -> structural/failure -> coupled Level 0`, refinement matrix, exploit fixtures, complete telemetry bundle, and bilingual baseline report.

### Completion gate

- the reviewed baseline produces one complete deterministic result for every declared training and holdout case, whether finish or explicit failure;
- at least one baseline is structurally feasible for the declared training set before search is opened;
- deliberate weak/disconnected controls are rejected or produce the expected `DNF`;
- timestep/mesh changes satisfy their pinned convergence gates and repeated runs preserve exact identity/provenance;
- no Level 0 outcome is relabeled as physical validation.

### Non-claim

A fixed baseline is not autonomous research, an optimized car, real-circuit admission, safety certification, or discovery.

## Work 050 — Bounded Whole-Vehicle Search Pilot and Readiness Review

### Objective and dependency

Verify that whole-vehicle candidates can be proposed, evaluated, failed, compared, and replayed fairly before authorizing a main research campaign. Depends on Work 049.

### Experiment

- treatments: `GRID`, `RANDOM`, and `EVOLUTION` through one evaluator API;
- independent variables: treatment and preregistered seed; candidate variables are limited to the Work 047 grammar;
- dependent variables: feasible rate, failure-code distribution, objective among gate-passing candidates, holdout survival, refined-evaluator survival, wall time, memory, and budget use;
- controls: equal attempted-evaluation budget, component library, loads, seeds, compute cap, evaluator, tolerances, baselines, and immutable result ledger;
- pilot budget proposal: `32` attempted evaluations per treatment per seed across `3` seeds, including grammar/CAD/solver failures in the budget. The final value must be frozen before the first admitted pilot.

### Implementation and deliverables

Implement `DesignSearchAgentV0`, candidate ancestry/RNG checkpoints, append-only result and budget ledgers, equal-budget treatment adapters, holdout/refinement promotion, exploit tests, pilot summary tables/plots, falsification review, and bilingual readiness report.

### Completion gate

- exact same-seed replay and exact budget accounting including every failed candidate;
- all treatments use the same evaluator and opportunity set; the agent cannot edit code, configs, loads, tolerances, or evidence;
- selected candidates must pass preregistered holdouts and independent refined evaluation or be reported as failures;
- no numerical exploit, hidden repair, missing evidence, or unequal compute opportunity can create a winner;
- readiness review explicitly returns `ready_for_bounded_main_campaign` or `not_ready` with blockers.

### Non-claim

Pilot success authorizes only a bounded main campaign. It does not prove superiority, novelty, manufacturability, safety, physical validity, or discovery. Promotion beyond Level 0 still requires independent Level 1 evidence, real circuit admission, structural safety, cross-model aerodynamics, thermal reliability, and quantified uncertainty under the existing promotion gate.

## Program-level stop/go gates

### Gate A — Structural subsystem ready

Requires Works 041-046 completed with no unresolved numerical, material, interface, or failure-coupling blocker. Only then may structural fitness affect a whole-vehicle candidate.

### Gate B — Whole-vehicle evaluator ready

Requires Works 047-049 completed, one end-to-end fixed baseline, deliberate failure controls, frozen training/holdout loads, and reproducible evidence. Only then may Work 050 search begin.

### Gate C — Main research campaign ready

Requires Work 050 to return `ready_for_bounded_main_campaign`. This means the experimental apparatus is ready; it is not physical validation. If any work rejects its preferred hypothesis, the dependency chain pauses and a separately numbered remedial work item is required.

## Definition of the endpoint

After Work 050, Formula Ultimate may begin a bounded, evidence-constrained whole-vehicle research campaign with explicit 3D candidates, coupled physics, structural failures, fair baselines, holdouts, and deterministic replay. Claims remain limited to the exact grammar, loads, materials, solvers, evidence classes, and fidelity levels tested.
