# Formula Ultimate: Project Status, Readiness, and Direction

Thai companion: `PROJECT_STATUS_AND_DIRECTION_2026-08-28.th.md`

## Report snapshot

| Field | Value |
|---|---|
| Report date | 2026-08-28 |
| Local branch | `main` |
| Evidence baseline | `0992f5c` — `feat(physics): complete digital race strategy model` |
| Completed work sequence | Work 001–019 |
| Physics queue | Work 010–019 completed |
| Current automated suite | 154 tests passing before this report |
| Strongest broad claim | Deterministic Level-0 software/analytical foundation |
| Claims not supported | Complete vehicle, autonomous discovery, physical validation, real race superiority, safety, or manufacturability |
| Remote status | Before Work 020, local `main` is 14 commits ahead of `origin/main`; after this report commit it will be 15 ahead. This work does not push. |

This report is the current status snapshot. Older “current phase” text in the
README and research charter predates Work 010–019 and understates the present
Level-0 module inventory. Those documents remain historical project inputs but
should be reconciled in a separate planned documentation work item before the
next experimental phase.

## Executive summary

Formula Ultimate is intended to test whether autonomous agents can discover
complete 3D racing-vehicle architectures and component technologies without
being forced into a conventional car layout. The design domain may eventually
include unfamiliar body topology, ground-contact arrangement, energy system,
cooling path, structure, joint, fastener, and internal component geometry.

The project does not remove physics, race discipline, energy accounting,
resources, safety, evidence, or reproducibility. “Fastest” means minimum total
race time among candidates that finish the same declared race and pass the same
evidence gates. All primary propulsion energy is onboard before the race; no
undeclared primary energy may be added during the race. Internal recovery is
allowed only when its physical source, conversion losses, and conservation
residuals remain observable.

The repository is now substantially beyond bootstrap. It has:

- a governed, bilingual, commit-backed research workflow;
- a constrained `CadQuery -> STEP -> FreeCAD -> Level 0` geometry evidence loop;
- ten source-audited real-circuit profiles;
- independent Level-0 models for longitudinal motion, track corridor,
  tyre-force saturation, energy topology, energy conservation, thermal state,
  race completion, lateral/yaw/load transfer, aerodynamics/cooling,
  suspension/braking/regeneration, and multi-event race strategy/reliability;
- deterministic replay, explicit invalid states, localized failure events, and
  conservation residuals; and
- 154 passing automated tests at the Work 019 baseline.

What does not yet exist is equally important: there is no autonomous design
agent, topology evolution engine, complete-vehicle 3D grammar, integrated
time-stepping vehicle simulator, optimized baseline campaign, higher-fidelity
promotion pipeline, empirical calibration, or validated technology discovery.

The correct next direction is therefore **integration before evolution**:
version one common experiment/candidate/state contract, couple the existing
Level-0 modules into one fixed-topology reference vehicle, establish fair
optimized baselines, and only then open free-topology agent search. This keeps
novelty from exploiting disconnected physics or unequal evidence.

## 1. Research direction that has been established

### 1.1 Long-term research question

Can autonomous agents create complete 3D racing vehicles and previously unseen
component technologies that outperform fairly optimized conventional baselines
in total race time across different real race environments, while surviving
progressively stronger physics and evidence gates?

For race environment `r`, the declared objective is:

```text
d*_r = arg min_d T_race(d, r)
```

subject to at least:

```text
RaceCompleted(d, r) = true
initial primary energy <= declared race energy budget
external primary-energy addition during race = 0
conservation residuals <= declared tolerances
complete 3D geometry is valid and physically accounted
required structural, thermal, aerodynamic, tyre, material,
manufacturing, numerical, and uncertainty gates pass
```

Peak speed, partial distance before failure, solver instability, hidden energy,
or an invalid geometry is not a winning result.

### 1.2 What is intentionally open

The research may eventually allow the agent to change:

- whole-vehicle topology, size, packaging, external surface, and aerodynamic
  architecture;
- number, location, and role of permitted ground-contact endpoints;
- source/store/converter/transmission/propulsor/cooling topology;
- structures, housings, ducts, rotors, joints, couplings, and fasteners;
- material distribution and internal component geometry; and
- race-specific strategy and controller parameters.

A new-looking part is not automatically a discovery. It must have typed
interfaces, declared material/manufacturing assumptions, geometry-derived
properties, independently evaluated loads and failures, and a measurable
whole-race advantage under fair controls.

### 1.3 What remains constrained

- SI-unit physics and conservation;
- real race distance and circuit-specific environment;
- predeclared primary-energy budget with no mid-race replenishment;
- finite materials, resources, compute, and evaluation budget;
- numerical validity and deterministic replay metadata;
- safety and failure observability;
- fair fixed-topology baselines and matched random seeds; and
- promotion through stronger fidelity before a discovery claim.

Open-ended design means no prescribed conventional architecture **inside the
declared experimental boundary**. It does not mean no boundary.

## 2. Completed work: Work 001–019

| Work | Commit | Completed result | Evidence boundary |
|---:|---|---|---|
| 001 | `6b2d4cd` | Bootstrapped the physics-first repository, governance, package boundaries, research charter, design language, validation ladder, and work-log protocol. | Structure and methodology only. |
| 002 | `96e8db4` | Added deterministic one-dimensional longitudinal motion with traction, drag, rolling resistance, grade, stop localization, telemetry, replay, and analytical tests. | Narrow point-mass Level 0. |
| 003 | `50af600` | Added separate Thai companions and automated bilingual Markdown coverage. | Documentation contract, not physics. |
| 004 | `840f2b6` | Researched MCP-compatible engineering CAD tools and selected a layered CadQuery/FreeCAD/Fusion path. | Tooling research as of 2026-08-23. |
| 005 | `f598799` | Verified local Fusion MCP handshake, pinned CadQuery MCP, FreeCAD headless STEP flow, launchers, and environment evidence. | Tool/environment proof; no vehicle design. |
| 006 | `455a9d0` | Built `mounting_plate_v1` and the constrained `CadQuery -> STEP -> FreeCAD -> Level 0` evidence loop. Three valid candidates passed; one invalid candidate was rejected pre-CAD. | Pipeline coherence for one bounded component grammar. |
| 007 | `a4ef20f` | Established the open whole-vehicle research mission, technology-neutral energy comparison, finish-gated race objective, and discovery claim rules. | Research framing. |
| 008 | `774c66e` | Added ten deterministic, source-audited real Formula One circuit profiles with conflicting design pressures and width screening. | Profile-level circuit evidence, not surveyed racing lines. |
| 009 | `da9cc4c` | Made validated, explicit-scope commits mandatory for each completed work item. | Governance and traceability. |
| 010 | `37188b1` | Added a 3D piecewise corridor integrator and static/swept/steering vehicle-envelope gate. | Synthetic corridor validation; real circuits remain indeterminate without surveyed geometry. |
| 011 | `609329f` | Added a deterministic tyre friction circle/ellipse with requested/applied forces, saturation, utilization, and residuals. | Capacity law, not calibrated slip/transient tyre physics. |
| 012 | `d1a9c54` | Added deterministic typed source/converter/transmission/tyre/sink component graphs and fail-closed connection rules. | Topology/interface validity only. |
| 013 | `f1b4b90` | Added an independent energy audit that detects hidden energy, double-counted loss, missing evidence, and interface imbalance. | Declared algebra/conservation audit, not proof that upstream physics is correct. |
| 014 | `f3c3fce` | Added lumped heating/cooling, thermal derating, analytical overtemperature localization, latched failure, and thermal residuals. | Lumped Level-0 thermal behavior. |
| 015 | `19fd7bc` | Added deterministic whole-race distance completion with finish, depletion, timeout, thermal failure, and invalid outcomes across ten circuits. | Reduced-order completion gate, not lap-time prediction. |
| 016 | `abce996` | Added arbitrary full-rank ground-contact layouts, quasi-static normal loads, lateral/yaw dynamics, load transfer, combined tyre limits, and balance residuals. | Planar Level-0 rigid-body step. |
| 017 | `435750e` | Added provenance-bearing aerodynamic coefficient maps over speed, ride height, yaw, and active state, including force/moment/cooling outputs and envelope rejection. | Synthetic/declared maps, not CFD or measurement. |
| 018 | `f77d9c3` | Added topology-neutral contact suspension, tyre-limited mechanical/regen braking, storage/loss accounting, brake heat, derating, and failure localization. | Independent contact interval, not whole-vehicle braking safety. |
| 019 | `0992f5c` | Added multi-lap/multi-sector strategy, traffic, weather, degradation, damage, onboard-energy depletion, seeded reliability, deterministic replay, and event-localized terminal outcomes. | Level-0 strategy/failure selection, not real reliability or race prediction. |

## 3. Current repository capability map

```text
research constraints and experiment controls
  -> constrained candidate/geometry declarations
  -> CadQuery B-rep generation
  -> STEP artifact and hash
  -> independent FreeCAD geometry measurement
  -> typed component/power interfaces
  -> independent Level-0 physics evaluators
  -> conservation, failure, numerical, and replay evidence
  -> real-circuit distance and scenario gates
```

The arrows above describe available stages, not one fully coupled production
pipeline. Work 006 connects one constrained mounting plate to geometry-derived
mass and the early longitudinal kernel. Work 011–019 mostly expose independent
models and validators. The unified causal link from arbitrary whole-vehicle CAD
through every physics module to race fitness is still missing.

### 3.1 Governance and reproducibility

| Capability | Status | Evidence |
|---|---|---|
| Plan before implementation | Ready | Mandatory bilingual Work 001–020 records. |
| Result and limitation record | Ready | Matching result required for every completed plan. |
| Explicit validated commit | Ready | Selective staging, fail-fast validation, cached diff check, commit hash, clean-tree check. |
| Bilingual maintained Markdown | Ready | Repository test requires `.md` and `.th.md` companions. |
| Deterministic replay | Ready at module level | Immutable inputs/results and fixed seeds in physics tests and digital race. |
| Reproducible research run manifest | Partial | Individual metadata exists; no one schema yet spans CAD, component graph, solvers, circuit, seed, and artifact hashes. |

### 3.2 CAD and geometry

| Capability | Status | Evidence and limitation |
|---|---|---|
| CadQuery code-first solid generation | Ready for controlled local experiments | CadQuery 2.8.0 and pinned MCP were verified in Work 005; environment should be rechecked before a new CAD campaign. |
| STEP export and hashing | Ready | Work 005/006 preserve exchange artifact identity. |
| Independent FreeCAD import/measurement | Ready for current bounded loop | FreeCAD 1.1.3 independently measured solid count, bounds, and volume in the recorded environment. |
| Constrained component grammar | Partial | Only `mounting_plate_v1`; it proves grammar enforcement, not general component invention. |
| Complete vehicle assembly/B-rep | Not ready | No vehicle grammar, assembly interface solver, collision/packaging system, or complete CAD candidate exists. |
| Geometry-derived inertia/structure/flow | Not ready as an end-to-end gate | Mass/volume are demonstrated; general inertia, FEA, CFD, manufacturing, and material-failure promotion are absent. |

### 3.3 Circuits and race environments

Ten profiles are available:

1. Monaco
2. Monza
3. Spa-Francorchamps
4. Singapore
5. Suzuka
6. Silverstone
7. Hungaroring
8. Mexico City
9. São Paulo
10. Bahrain

Each profile supplies published lap length, race laps, race distance, circuit
metadata, design-pressure scores, strengths/weaknesses, source evidence, and
available width/altitude inputs. Work 019 preserves the published race-distance
residual explicitly in its final event.

Ready use: pre-design diversity, published-distance race gates, altitude-aware
air-density reference, and sourced static-width screening where evidence
applies.

Not ready: surveyed 3D centerline/corridor, local width, kerbs, barriers,
surface/friction map, bumps, drainage, wind field, racing line, pit lane, flag
zones, or empirical weather. Consequently, real-circuit swept-envelope
admission remains `indeterminate`, not passed.

### 3.4 Physics and race modules

| Module | Ready now | Important boundary |
|---|---|---|
| Longitudinal | Analytical Level-0 reference and deterministic telemetry | External force command; no complete drivetrain coupling. |
| Corridor | Synthetic 3D path integration and rigid swept-envelope rejection | No admission-capable surveyed real geometry. |
| Tyre | Combined longitudinal/lateral force capacity and saturation | No slip ratio/angle, load sensitivity, temperature, wear, or transient contact model. |
| Energy graph | Typed topology/interface compiler | Does not create or validate energy values. |
| Energy audit | Independent balance and transfer evidence | Depends on correct upstream energy evidence. |
| Thermal | Lumped heating/cooling/derating/failure | No calibrated distributed thermal network. |
| Race completion | Deterministic distance/energy/thermal outcome gate | Reduced-order and not a lap-time model. |
| Lateral/yaw | Planar step, arbitrary contacts, load projection, combined tyre use | Quasi-static load transfer and no full multibody suspension. |
| Aerodynamics | Interpolated coefficient maps, forces/moments, cooling flow | Map evidence may be synthetic; no CFD or wind-tunnel validation. |
| Suspension/braking/regen | Independent contact travel, torque limits, heat, storage, localized failure | No centrally coupled chassis, wheel-speed dynamics, ABS, or stopping-distance validation. |
| Digital race | Multi-lap strategy, traffic/weather events, wear/damage, seeded reliability | Abstract sector coefficients and uncalibrated scenario multipliers. |

## 4. What is ready now

The following work can be performed defensibly today **inside the declared
Level-0 boundary**:

1. Create versioned, deterministic unit/reference experiments in SI units.
2. Generate and independently measure constrained CadQuery components that fit
   an approved grammar such as `mounting_plate_v1`.
3. Reject invalid geometry parameters before CAD and reject mismatched CadQuery/
   FreeCAD measurements after STEP exchange.
4. Screen candidates against ten different circuit pressure profiles before
   design and exact published race distances after design.
5. Compile declared power/energy component graphs and reject invalid carrier,
   direction, fan-out, cycle, endpoint, or required-port topology.
6. Audit declared energy flows independently and expose hidden or double-counted
   energy.
7. Evaluate individual Level-0 laws for tyre capacity, thermal failure,
   lateral/yaw/load transfer, aerodynamic maps, suspension/braking/regen, and
   event-level race strategy.
8. Force and distinguish finish, depletion, reliability, damage, degradation,
   thermal failure, timeout, saturation, non-convergence, and invalid numerical
   outcomes.
9. Reproduce a declared module/scenario exactly with the same inputs and seed.
10. Use the current suite as a regression foundation; the Work 019 baseline
    passed 154 tests.

These capabilities are ready for software research, interface design,
falsification fixtures, and selection-gate development. They are not ready for
a physical race-car claim.

## 5. What is partially ready

### 5.1 The CAD pipeline

The local generation/exchange/measurement loop is proven, but only for a
bounded mounting plate. It needs assembly semantics, more component families,
materials, loads, contact interfaces, manufacturing rules, and solver promotion
before an agent can invent vehicle-scale technology.

### 5.2 The circuit set

The ten profiles create valuable conflicting objectives and real size/distance
constraints. They are not complete digital twins. Geometry-dependent admission
or realistic lap optimization must remain unavailable until better circuit
evidence is versioned.

### 5.3 The physics stack

The modules are individually useful and well tested, but the repository does
not yet propagate one shared state through all of them. For example, an
aerodynamic load is not yet automatically distributed to contacts, tyre forces
do not automatically update a common multibody vehicle state, brake recovery is
not yet a central energy-graph transaction, and component degradation is not
derived from geometry/material stress histories.

### 5.4 Race strategy

Work 019 can test declared pace/weather/traffic/failure scenarios and replay
seeded uncertainty. Its sector rates are inputs, not outputs of the detailed
vehicle modules. Strategy comparison is therefore suitable for contract and
event testing, not a real strategy recommendation.

## 6. What is not ready

- An autonomous agent that generates, mutates, repairs, and selects designs.
- A topology-evolution algorithm or experiment runner in the currently empty
  topology/simulation orchestration packages.
- A complete 3D vehicle representation and assembly/interface grammar.
- Automatic extraction of full mass distribution, inertia tensor, stiffness,
  stress, fatigue, cooling, flow, or electromagnetic behavior from arbitrary
  candidate geometry.
- A unified vehicle state and causal solver that couples Work 011–019.
- A conventional fixed-topology baseline optimized with comparable effort.
- A fair free-topology versus fixed-topology experimental campaign.
- Multi-seed statistics, holdout circuits, ablations, uncertainty calibration,
  or surrogate auditing.
- CFD, FEA, multibody, detailed tyre, crash, or empirical cross-validation.
- Manufacturing feasibility, cost model, supply/material constraints, safety
  certification, or real FIA eligibility.
- Evidence that any novel technology has been discovered.
- Evidence that any design is faster than an actual Formula One car.

## 7. Evidence and readiness interpretation

| Claim | Current status |
|---|---|
| Repository structure is governed and reproducible | Supported locally |
| Individual declared Level-0 laws match tests/references | Supported for implemented cases |
| Ten circuit profiles and distance gates execute deterministically | Supported |
| Constrained CAD can survive independent STEP measurement | Supported for `mounting_plate_v1` fixtures |
| Independent modules form one coherent vehicle simulation | Not yet supported |
| Level 0 is numerically converged for the future integrated vehicle | Not yet supported |
| Candidate ordering survives a stronger independent model | Not tested |
| Free topology beats optimized conventional baselines | Not tested |
| A new technology has been discovered | Not supported |
| A design is manufacturable or safe | Not supported |
| Real race performance is predicted accurately | Not supported |

The present confidence is high for the implemented deterministic contracts,
analytical references, invalid-state handling, event localization, and internal
accounting. Confidence is low or absent for integrated-vehicle accuracy,
calibrated uncertainty, real performance, manufacturability, and safety.

## 8. Main gaps and research risks

### 8.1 Integration gap

The largest technical risk is that independently correct modules may behave
incorrectly when coupled. Load, energy, thermal state, timestep, and failure
ordering need one causal contract and residual aggregation policy.

### 8.2 Design-language bias

If the future grammar only contains conventional components, the agent cannot
discover non-conventional architecture. If it is too unconstrained, most
candidates will be invalid or exploit missing physics. The grammar must be open
in topology but strict in typed physical interfaces and evidence requirements.

### 8.3 Baseline fairness

An apparently novel result is meaningless if the conventional baseline receives
less optimization, fewer evaluations, weaker component options, different
energy, different seeds, or weaker failure gates.

### 8.4 Fidelity and calibration gap

Synthetic coefficient maps and reduced-order failure multipliers can rank
candidates incorrectly. Promotion to independent solvers and eventually data
must test whether ordering survives.

### 8.5 Objective exploitation

An agent may exploit incomplete race completion, numerical tolerance, hidden
energy, omitted material, unbounded dimensions, or missing failure modes. The
existing fail-closed and residual discipline must remain part of fitness, not a
post-processing check.

### 8.6 Documentation drift

README and charter “current phase/status” sections still describe an earlier
state. They should be updated in a separate auditable work item so the project
entry point does not understate completed modules or confuse the original
narrow Phase-1 plan with the now broader Level-0 foundation.

## 9. Recommended direction: integration before evolution

### Stage A — Reconcile the experiment contract

Create one versioned experiment manifest that pins:

- candidate/design-language version and immutable geometry hashes;
- material/component catalog and typed interfaces;
- circuit profile and regulatory/energy profile;
- initial energy and permitted recovery paths;
- solver/model versions, timestep/tolerances, event priority, and failure policy;
- random seeds, evaluation/compute budget, artifact paths, and code commit; and
- claim level and required promotion gates.

Also reconcile README/research-charter status language with the Work 019
baseline without changing the long-term open-ended mission.

### Stage B — Build one coupled fixed-topology Level-0 reference vehicle

Define a common state and deterministic execution order such as:

```text
circuit/environment/strategy command
  -> aerodynamic forces and cooling
  -> chassis force/moment and normal-load solution
  -> per-contact tyre/suspension/brake limits
  -> longitudinal/lateral/yaw state update
  -> typed energy transfer and conservation audit
  -> thermal/degradation/damage/reliability events
  -> race progress, finish, failure, telemetry, and replay
```

The first integrated vehicle should be fixed topology, not because the project
prefers conventional cars, but because integration errors must be separated
from topology-search errors. Every step must aggregate force, moment, energy,
distance, and state residuals and expose which module caused invalidity.

### Stage C — Expand geometry-to-physics coverage

Move from one mounting plate to a small composable library of **functional
interfaces**, not a catalog of prescribed conventional shapes. Candidate
families should expose mounting/load surfaces, ports, material regions,
clearance volumes, and failure evidence. Add:

- assembly and collision/packaging rules;
- FreeCAD-derived mass, centre of mass, and inertia;
- material and manufacturing declarations;
- load-case export and independent structural/thermal checks; and
- provenance from geometry artifact to every derived property.

### Stage D — Establish fair optimized baselines

Create fixed-topology EV, ICE, hybrid, or other predeclared reference families
only as comparison treatments. Give each the same energy opportunity, component
library, circuit set, constraint gates, compute/evaluation budget, seeds, and
promotion criteria. Tune them competitively before comparing free topology.

### Stage E — Introduce autonomous search in controlled layers

Recommended progression:

1. parameter optimization on one fixed topology;
2. component selection and sizing on the same topology;
3. typed connection/topology mutation with fixed vehicle envelope;
4. component-geometry mutation through constrained grammars;
5. packaging and ground-contact arrangement changes; and
6. whole-vehicle topology/geometry co-design.

At each layer, compare against the previous layer under matched budget and use
multiple seeds. Invalid candidates should return structured failure evidence to
the agent, not disappear from the dataset.

### Stage F — Promote and attempt to falsify discoveries

Promote only race-finishing, non-dominated candidates. Recheck them with
independent geometry/physics solvers, finer timesteps, uncertainty sweeps,
holdout circuits, ablation of the allegedly novel feature, and optimized known
alternatives. A candidate becomes a discovery only if its functional advantage
survives these attempts to explain it away.

## 10. Recommended immediate next work item

The next implementation should be:

> **Unified Level-0 Experiment Contract and Coupled-Vehicle Architecture**

It should produce schemas and an executable fixed-topology integration
reference before implementing free-topology evolution.

Minimum completion gate:

1. One immutable manifest identifies candidate, geometry, components, circuit,
   energy profile, solvers, tolerances, seed, and commit.
2. One fixed-topology vehicle traverses the same deterministic coupled pipeline
   on all ten circuit profiles.
3. Aerodynamic loads, contact loads, tyre forces, brake/regen energy, thermal
   state, degradation, damage, and race progress affect one shared state rather
   than independent fixtures.
4. Force, moment, energy, distance, and event residuals remain observable.
5. Finish and every major failure mode replay exactly.
6. A deliberately inconsistent coupling is rejected by tests.
7. The result remains explicitly Level 0 and makes no real-performance claim.

This work is the shortest credible bridge between the current foundations and
the intended autonomous discovery research.

## 11. Decisions recommended now

1. Treat Work 001–019 as the completed **foundation phase**, not as a completed
   simulator or vehicle.
2. Do not begin whole-vehicle agent evolution before a coupled fixed-topology
   reference passes all residual and failure gates.
3. Preserve open topology by defining functions and typed interfaces rather
   than prescribing human component shapes.
4. Make the experiment manifest and fair-baseline policy part of the evaluator,
   not informal lab notes.
5. Keep all primary energy onboard before race start; recovered energy must
   retain source/loss evidence.
6. Use all ten circuits for environmental diversity, but do not claim surveyed
   geometry where evidence is absent.
7. Revalidate the CAD tool environment before the next geometry campaign.
8. Update stale top-level status text in its own validated work item.
9. Keep the repository private and do not push local Work 006–020 history until
   the user explicitly authorizes publication/synchronization.

## 12. Current conclusion

Formula Ultimate now has a serious, auditable Level-0 research foundation. It
can express constrained CAD, independently measure a bounded component,
represent typed energy topology, evaluate many individual physical boundaries,
run deterministic circuit/race scenarios, expose failures, and preserve
evidence. This is enough to begin **integration research**.

It is not yet enough to release an agent and interpret its output as an invented
race car or new technology. The next scientific milestone is not “generate a
stranger car.” It is proving that one ordinary reference candidate can pass a
single coupled, conserved, replayable, race-completing pipeline. Once that
reference is stable and fair baselines exist, the project can open topology and
geometry progressively and ask the real discovery question with defensible
evidence.
