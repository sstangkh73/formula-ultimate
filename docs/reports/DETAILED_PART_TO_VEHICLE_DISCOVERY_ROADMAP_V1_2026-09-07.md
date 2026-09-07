# Detailed Part-to-Vehicle Discovery Roadmap V1

Thai companion: `DETAILED_PART_TO_VEHICLE_DISCOVERY_ROADMAP_V1_2026-09-07.th.md`

Date: 2026-09-07 (Asia/Bangkok). Work 106. Baseline commit: `ea70f5f`.

Status: Proposed implementation roadmap; no new physical capability is delivered by this document.

## 1. Destination and authority

Build a system that generates a complete race vehicle, including functional internal geometry and assembly details down to fastening-scale features, by searching geometry, material distribution, interfaces, architecture and control together. It must not merely choose familiar catalog components, resize predefined cars, or decorate an idealized simulator with detailed CAD afterward.

The governing [Work 104 protocol](../contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md) remains authoritative for physics, race, energy, fairness and promotion. This roadmap refines implementation priorities after Work 105; it does not rewrite historical results or replace the external task. In particular, the Work 105 suggestion to first obtain more isolated survivors is not a universal integration prerequisite. Exploratory coupled design is allowed before every part passes alone; stronger claims still require adequate evidence for the actual assembly conditions.

The intended freedom is freedom from a prescribed catalog of shapes and vehicle layouts, not freedom from conservation laws or declared task conditions. No finite algorithm can represent or evaluate every mathematically possible shape. The engineering target is an extensible, resolution-controlled search space with visible coverage gaps, rather than a claim of literally unrestricted representation.

## 2. Current position: what exists and what does not

The following are historical results read from the repository, not experiments rerun for Work 106.

| Evidence | Demonstrated scope | Remaining gap |
|---|---|---|
| [Work 092](../work_logs/2026-09-04_092_freeform-brep-solid-grammar-v2-result.md) | 10 candidates, 18 CAD operators, curved/lofted/swept/hollow/multi-body B-rep; independent CAD inspection | Bounded corpus, not arbitrary geometry robustness or functional physics |
| [Work 097](../work_logs/2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.md) | 7 reduced-order benchmark adapters; beam/shell/solid/contact labels | Does not mesh STEP faces or resolve general local stress, buckling, plasticity, cracks or contact history |
| [Current morphology](../../src/formula_ultimate/search/executable_morphology.py) | Variable parts, nodes, edges, radii and interfaces in a swept-network language | The search backbone still favors members and graph mutations; broader CAD operators are not equivalent to broader evaluated search |
| [Current field solver](../../src/formula_ultimate/physics/functional_network_solver.py) | Scalar axial and thermal networks; fixed load/thermal interfaces; one source and sink | Coordinates are spatial, but response is not a general vector solid solution; solving two fields does not itself establish coupled thermoelastic physics |
| [Work 105](../work_logs/2026-09-07_105_survivor-causality-integration-intake-result.md) | 10 scoped survivors, 0 mechanism candidates under its definition, 4 inactive appendages and 4 shape variants | Only `load_structure` coverage; 8 capability gaps, 7 evidence-class gaps; no whole-vehicle candidate |
| [Work 088](../work_logs/2026-09-04_088_whole-mechanical-vehicle-candidate-001-result.md) | Audit of 17 solids and 11 cases | `not_ready`: 8 overlapping pairs, another zero-clearance pair, moving/rigid interface conflict, no integrated mesh convergence, synthetic material/process evidence |

Work 088's interface misalignment was `0.007 m` against `1e-6 m`; its Level-0 run was not attempted. A successfully completed audit is not a successfully completed vehicle.

Work 105's graph descriptor explicitly omits terminal coloring, direction and parallel-edge multiplicity. Its zero mechanism count does not prove that unchanged-topology shape optimization cannot discover a useful function, or that unfamiliar geometry cannot work. New studies must distinguish geometric novelty, causal functional difference, beneficial performance and external prior-art novelty. A response worsening is not an improvement even if its absolute change is large.

The main missing bridge is **generated material/void geometry → geometry-derived fields and contact → functioning assembly → coupled vehicle evidence**. Another checklist-only intake would not build that bridge.

## 3. Definition of complete detail

For a final digital candidate, every physically necessary item must have an identifiable geometric/material realization or a disclosed unresolved gap. The final promoted geometry may not contain unexplained ideal sources of force, power, cooling, sensing or restraint.

Required coverage is functional, not a mandatory bill of conventional parts:

- Load-carrying regions, cavities, passages, moving members and supports.
- Joining/constraint realization: threads, bonded regions, interference fits, compliant connections, interlocks or another modeled solution as applicable.
- Internal energy storage/conversion/transmission, containment, insulation and losses.
- Ground/environment interaction, direction control and stopping capability, without prescribing wheels, axles or steering linkages.
- Heat paths, exchange surfaces, fluid paths and sealing where needed.
- Actuator and sensor hardware, wiring or other physical signal paths, power supply, mounting and latency assumptions.
- Tolerances, assembly states, preload, lubrication where applicable, tool access, service and replacement requirements when the task demands them.

A selected threaded joint must eventually include its helix, flank/root geometry, engagement, mating geometry, clearances and seating faces. An integral compliant connection may need none of those features; it instead owes its own deformation, fatigue, manufacturing and failure evidence. A standard purchased part is permissible if the study allows it, but its geometry, properties and provenance must be represented and it must not be counted as a generated discovery.

For every material region, record identity, geometry, material law and provenance, ownership, placement, tolerance, function references and evidence references. For every required function, trace the complete physical path through those regions. A list of named functions with no material realization is incomplete.

## 4. Freedom, boundaries and bias controls

Do not pre-fix silhouette, symmetry, wheel count, axle count, part count, standard cross-section, powertrain family or one-part-per-function decomposition merely because they are familiar. Do not reward visual strangeness as a substitute for performance either. A conventional-looking winner is allowed if it wins fairly.

Separate four sources of restriction:

| Restriction | Treatment |
|---|---|
| Physical law or measured material applicability | Mandatory for a claim within that physical domain |
| External race, energy, environment and safety task | Freeze before admitted comparisons; do not quietly change it for a candidate |
| Numerical resolution, supported physics, geometry kernel, compute budget | Declare as coverage limits; failure to evaluate is not proof of physical impossibility |
| Manufacturing route, available stock or assembly process | Explicit stage-specific constraint; exploratory geometry can remain unresolved for manufacturing |

Finite minimum feature size, domain bounds and complexity caps are necessary computational choices. Register their purpose and perform enlargement/refinement studies; do not promote them into universal laws. Report which proposed shapes were rejected by representation, meshing, physical violation, cost exhaustion or manufacturing separately.

Known component examples are verification fixtures and optimized baselines, not the only admissible genome. Include unfamiliar test families with curved load paths, branching voids, asymmetric material fields and multifunctional regions. No predefined list of these families defines the eventual search space.

## 5. Representation: geometry and material first

Use a common spatial contract with multiple generator backends, not a universal list of named parts.

| Layer | Proposed content | Required behavior |
|---|---|---|
| Spatial material model | Occupied/void regions; material fields; coordinate frames; feature resolution | Non-overlapping physical ownership; explicit interfaces between materials; no negative density or hidden filled cavities |
| Geometry program | Existing B-rep features plus free-form surfaces, implicit fields and adaptive volumetric descriptions | Add/remove material, create/close holes, split/merge regions, move interfaces and change topology |
| Functional assembly | Typed, directed/undirected-as-appropriate multigraph of physical terminals and interactions | Preserve parallel paths, terminal roles, motion freedom and constitutive law; renaming must not change meaning |
| Physical models | Meshes, material laws, contacts, reduced models, boundary histories | Derived from the same candidate revision, with applicability bounds and numerical error |
| Evidence package | Genome, geometry, mesh, solver, materials, loads, environment, controller and accounting identities | Any causal input change invalidates dependent evidence unless transfer is explicitly justified |

Start by reusing proven B-rep export/inspection. Add an implicit/adaptive-volume route to permit material addition/removal and topological changes without enumerating named mechanical shapes. No claim that converting every implicit candidate to a watertight B-rep is already solved: conversion is a separately tested adapter, and an unsupported export remains visible. Direct mesh-based evaluation can be exploratory if geometry error and material interfaces are tracked; final engineering deliverables must satisfy the declared export/inspection contract.

Keep three identities separate: exact generative program identity, geometric equivalence within a declared tolerance, and functional equivalence under declared tasks. Different programs can create equivalent geometry; equal graph topology can produce different useful physics.

### 5.1. What the generator can actually change

A candidate may describe a continuous implicit boundary, sampled on an adaptive spatial grid, with material on one side and void on the other. This grid is a numerical basis, not an instruction to produce block-shaped parts. Refine the boundary until its geometric error satisfies the registered feature-scale tolerance. Alternatively, evolve free-form surface control data and B-rep feature programs. Test agreement where representations overlap instead of assuming that they are interchangeable.

Candidate mutations must eventually cover boundary displacement, spatially varying thickness, cavity creation and routing, local branching, material redistribution, interface relocation, part split/merge and assembly reorganization. Restrict material mixtures or gradients to declared constitutive/process support; do not interpolate properties arbitrarily to invent an unrealizable super-material. Surface smoothness and minimum radius are trial/process/numerical parameters, not requirements that every output resemble a known primitive.

Use a traceable hierarchy from vehicle to functional grouping to physical part to material region to feature, while allowing multiple groupings to refer to the same physical region without duplicating it. Assembly hierarchy is bookkeeping, not a fixed vehicle anatomy. Individual features may include thread roots, seal lands or a newly generated contact surface only when that candidate needs them. Store spatial resolution and approximation error with each representation so that small but mechanically important features cannot disappear silently.

To test openness, compare a fixed named-part template, the existing member grammar and the spatial-material route on the same functional task with matched resources. Measure accessible geometry/function diversity and verified utility, not only operator count. Include a preregistered task where a useful solution needs a cavity or surface change unavailable to the fixed template, but do not restrict the answer to a hand-drawn target shape. Also include tasks where the fixed family is competitive, so the benchmark is not constructed solely to favor the new representation.

## 6. Mass, geometry and multiscale consistency

Use SI units and a single physical ownership ledger. For material regions, compute mass from the integral of density over occupied volume; derive center of mass and the full inertia tensor in declared frames. Assembly aggregation must use each physical region once, with the appropriate frame transform and parallel-axis contribution. Multifunctional regions do not receive duplicate mass charges; intersecting CAD bodies do not silently become overlapping material.

Reconcile CAD, tessellated surface, volume mesh and reduced-model volumes/masses. Record discrepancy, geometric approximation error and acceptance tolerance. Sum-of-members volume is not automatically the volume of a union with blended junctions. Collision geometry, structure, thermal area and fluid passages must resolve the same revision and assembly state.

Geometry detail and simulation fidelity are independent axes:

| Geometry state | Meaning |
|---|---|
| `G0` | Conceptual occupied volumes and explicitly unresolved internal details; exploratory only |
| `G1` | Complete functional material paths and assembly interfaces for a declared subsystem |
| `G2` | Necessary internal geometry, fastening/contact detail, tolerances and mass closure |
| `G3` | Whole-candidate assembly and manufacturing handoff geometry with no unexplained required hardware |

These are new planning labels, not existing implemented statuses or replacements for the Work 104 orthogonal evidence states. A `G3` model can still be physically unverified.

Do not solve every thread flank in every vehicle time step. Derive a local detailed joint response over a registered load/temperature/preload range, reduce it with quantified error, and use that model in the vehicle. If the vehicle leaves that range, stop relying on the reduced model and refine/re-evaluate. Transfer forces, moments, heat and displacement consistently; include transferred-energy checks. Full detail must exist where required for final geometry even when a validated reduction is used at runtime.

## 7. The fastening-scale proof case

The first detailed assembly demonstration should be a small load-transferring connection, not another complete-looking car. Use a familiar threaded fixture only as a verification reference; permit the generated alternative to be threaded, non-threaded or integrated.

The frozen task specifies terminals, force/moment histories, allowable motion, envelope, temperature range, allowed material/process evidence and assembly requirements. Search the intervening occupied material, voids, connection placement and joining strategy. Its success is a functioning connection under those conditions, not resemblance to a nut.

Required evidence includes geometric engagement/clearance, preload or other constraint initialization, vector force/moment balance, contact opening/slip, local deformation/stress, thermal effects if relevant, and a failure-domain statement. Where torque creates preload, include uncertain friction rather than a universal deterministic torque-to-force conversion. Check loosening and fatigue only with models and data applicable to those claims; otherwise retain them as unresolved.

Falsification cases: remove the connection; sever a load-carrying region; reverse/off-axis the load; change engagement or root geometry; introduce a clearance/tolerance extreme; exceed the validated reduced-model envelope. The predicted physical path must respond accordingly. A disconnected candidate may fail or be a free mechanism; it must not receive an invented stabilizing support.

Deliver detailed geometry, exploded/section inspection views, assembly state, material map, mesh, fields, convergence, mass reconciliation and a coarse-model comparison. Visual inspection supports geometric review but is not structural validation.

## 8. Physics capability ladder

Only activate domains whose models and dependencies are actually supported. A technology outside available constitutive models remains an unresolved research direction, not forbidden physics.

| Domain | Geometry-causal target | Verification before design claims |
|---|---|---|
| Solid mechanics | Vector displacement/stress, real surfaces and supports | Rigid-body modes, patch/reference tests, force/moment/energy residuals, at least 3 refinement levels and independent reference cases |
| Joints and contact | Separation, sliding, friction, preload, compliance | Unilateral contact and friction limits, reaction recovery, energy accounting and contact/time-step refinement |
| Motion | Rigid/flexible multibody dynamics and changing contact | Constraint consistency, free motion, momentum/energy checks and event/reversal tests |
| Thermal | Transient conduction, actual interfaces and heat sources | Heat balance, time/space refinement; temperature-dependent laws where used |
| Coupled thermo-mechanics | Temperature changes dimensions/preload/material response; losses change temperature | Nonzero bidirectional coupling tests and comparison with decoupled controls |
| Material failure | Relevant plasticity, buckling, fatigue, fracture, wear | Applicable material data, imperfection/history sensitivity and explicit omitted failure modes |
| Fluid/air interaction | Internal passage and external flow geometry | Mass/momentum/energy closure, boundary/mesh/time sensitivity and independent reference/measurement |
| Energy and actuation | Storage/conversion/transmission with containment and losses | Domain-specific conservation, capacity/rate/temperature limits, hardware mass and failure envelope |
| Control and sensing | Finite hardware authority, power, latency, noise and mounting | Causal signal/actuation path, saturation, delay, faults and controller adaptation cost |

An electromagnetic, electrochemical, combustion or other route requires its own constitutive and validation chain when selected. A generic efficiency number cannot establish that the corresponding internal hardware exists. Start with a tractable, documented reference route to exercise integration, label that trial's limitation, and preserve the interface for other routes. This is a staged implementation choice, not a permanent technology whitelist.

For every solve store recovered reactions, boundary work/heat/energy, numerical failures, conditioning/quality diagnostics, error bounds and missing domains. A residual reconstructed to equal the imposed load by definition is not an independent conservation check. Singular stresses at idealized sharp corners require a declared regularization/quantity of interest; do not claim mesh-converged point stress there by silently averaging it away.

## 9. Search loop: vehicle and parts evolve together

The operational loop is:

```text
Frozen external task and evidence rules
  -> architecture + spatial material proposal + controller proposal
  -> candidate-derived interface/load envelopes
  -> detailed part/connection generation and local evaluation
  -> exploratory coupled assembly and vehicle evaluation
  -> revised loads, packaging, heat, energy, failure and control requirements
  -> mutate architecture AND parts; retain bounded useful hypotheses
  -> evidence promotion only for the actual declared use conditions
```

Local tasks are versioned hypotheses, not permanent human decompositions. A region may simultaneously transfer load, transmit power and reject heat; evaluate the interaction and count its material once. An architecture proposal may remove an interface by merging regions or introduce one to make motion/assembly possible.

Early vehicle feedback can use explicit reduced models, provisional parameter intervals and unresolved domains. It cannot invent favorable coefficients for missing systems. If the intervals make the decision indeterminate, report that and allocate an evaluation/refinement task. The first coupled exercise should happen after basic fields and interfaces, not after every possible energy technology is implemented.

Use local geometry/material optimization where meaningful derivatives exist, topology/program mutations where they do not, and a diverse archive rather than one compulsory optimizer. Maintain feasible, near-feasible and informative unresolved candidates under preregistered caps. Novel appearance or a changed graph cannot bypass feasibility; unchanged topology cannot block a real, uncertainty-resolved improvement.

Compare substitution under both a common controller and matched-cost controller adaptation. Derive each candidate's loads from the same external task rules, then re-evaluate local evidence when vehicle feedback changes its applicability envelope.

## 10. Evidence and resource infrastructure

Attach input identities through the whole chain: task, candidate, CAD/material field, mesh, material data, contact laws, solver/version/settings, controller, environment, random seed, admission decisions and source artifacts. Verify the source evidence being used, not only a summary that asserts admission. Historical observed data cannot become a fresh holdout by renaming it.

Reserve compute before work begins, charge failed CAD/mesh/solver attempts and retries, and retain aborted/unreached proposals. Record wall time, measured CPU/GPU use where available, hardware, concurrency, mesh/DOF, iterations, cache use and peak memory. Unknown measurement is not zero cost. Include search, controller tuning, audits and final validation in matched budgets.

Before a comparison, freeze the resource unit, total budget and allocations for broad search, score-independent representation audits, quality promotion, unresolved-candidate escalation and finalists. Use a separate pilot to choose affordable counts and tolerances; do not invent a universal seed count or full-vehicle runtime now. Record changes in a new registration, not a rewritten result.

Report representation-specific evaluation coverage and false-negative audits. If unfamiliar shapes disproportionately fail meshing, investigate the adapter before declaring those shapes physically poor. Log exact decision replay separately from toleranced floating-point execution replay.

## 11. Delivery map and dependencies

The following work numbers are proposed, not reserved or already completed. Allocate the next unused number when each work starts, with its own bilingual plan/result and immediate validated commit. If a package proves too large, split it before implementation and preserve this roadmap as the original proposal.

| Proposed work | Scope and concrete artifact | Depends on | Exit evidence |
|---|---|---|---|
| 107 | Common spatial material/void contract, B-rep adapter and ownership/mass closure | Existing CAD | Real generated solids with declared cavities/material regions; fresh geometry changes measured mass/inertia; no hidden overlap or loss |
| 108 | Free-form implicit/adaptive-volume generator and conversion adapter | 107 | Add/remove/merge/split material without a named-part template; topology and geometry-error checks; unsupported conversion visible |
| 109 | Geometry-derived volume/surface meshing and semantic boundary transfer | 107; 108 for new route | Actual candidate geometry creates meshes at 3 levels; valid elements, cavity preservation, boundary coverage, mass discrepancy and repeatability |
| 110 | Vector solid solver on generated meshes | 109 | Reference/rigid-mode/patch tests plus unfamiliar candidates; independent reactions, force/moment/energy balance and convergence |
| 111 | Physical terminal and assembly interface semantics | 107 | Frames, parallel paths, material boundaries and motion roles survive renaming/split/merge; severing interface changes connectivity |
| 112 | Detailed connection geometry and contact/preload submodel | 110, 111 | Threaded reference and open-shape alternative; actual engagement/clearance, load transfer and contact convergence; reduction error bounded |
| 113 | Moving and compliant assembly with contact history | 112 | Motion envelope, constraints, collisions and energy validated on a small assembly; no incompatible rigid/moving connection |
| 114 | Transient thermal field and thermo-mechanical coupling | 110, 112 | Heat balance, expansion/preload response, space/time convergence and failure outside reduced-model range |
| 115 | Material/process provenance and applicable failure models | 110; 113/114 where required | Property ranges traced to evidence; selected failure cases verified; missing fatigue/fracture/process evidence remains unresolved |
| 116 | Bidirectional architecture-to-part task loop | 111, 113, 114 | Small exploratory assembly changes loads/heat and regenerates a part; actual coupled improvement or documented negative result |
| 117 | Ground-interaction and stopping/direction-control task sandbox | 113, 115 | Causal ground forces and dissipation; slip/contact changes and stopping behavior; no prescribed wheel count |
| 118 | Detailed transmission/actuation reference chain and extensible domain adapter | 113, 114, 115 | Internal load/motion/power path, losses/supports/containment included; removal/saturation tests; no ideal unexplained torque |
| 119 | Detailed onboard energy reference route | 114, 115, 118 | Storage/conversion internals, capacity/rate, containment and losses; complete primary-energy ledger under frozen task |
| 120 | Cooling/fluid-path and external-flow geometry evaluation | 109, 114, 115 | Passage/surface perturbation causes verified heat/flow response; flow and heat conservation and reference comparisons |
| 121 | Realized controller/sensor/actuator support hardware | 118, 119 | Geometry/mass/power/latency and mounting accounted; fault/saturation checks; matched adaptation budget |
| 122 | Coupled transient whole-candidate simulation harness | 116–121 | Explicit state exchange, interface work/heat consistency, time-step sensitivity, replay; no claims for unresolved required domains |
| 123 | Multiscale search with complete provenance and fair accounting | 108, 116; 122 for vehicle runs | Shape and topology proposals both eligible; budget reserved before calls; score-independent audits, typed statuses, signed effect and uncertainty |
| 124 | Registered detailed-part discovery comparison | 112–115, 123 | Optimized fixed and random controls; geometry-to-function ablations; held-out task conditions; full costs and uncertainty; positive or negative outcome accepted |
| 125 | Complete detailed digital candidate and assembly closure | 117–124 | Every required hardware/function path realized; `G3` checklist, exploded/section inspection, mass/energy/clearance/motion closure |
| 126 | Optimized whole-vehicle baselines and causal substitution | 122, 125 | Equal task/material-library/resource opportunity; common-control and matched-adaptation comparisons; transferred costs included |
| 127 | Frozen held-out race and robustness evaluation | 126 | Completion/time/energy/failure margins across declared unseen conditions; numerical uncertainty; no post-result task repairs |
| 128 | Independent higher-fidelity checks of decisive claims | 124–127 | Independently constructed/implemented analysis of critical differences, discrepancy disposition and evidence bounds |
| 129 | Manufacturing/assembly/tolerance handoff for a selected candidate | 125, 128 | Process/access/material availability review, tolerance propagation and inspection plan; unresolved process routes not silently approved |
| 130 | Authorized physical material/connection benchmark | 112, 115, 129 | Safe test plan, calibrated measurements, preregistered comparison and model discrepancy; validates only tested scope |
| 131 | Authorized physical subsystem correlation and endurance | 130 plus relevant domain packages | Correlated subsystem response, losses/failure limits and updated model envelope; new held-out checks after calibration |
| 132 | Authorized whole-vehicle validation program | 127–131 | Independent safety review, staged test envelope and measured whole-system evidence; claims limited to actual tested conditions |

Works 107–110 are the immediate geometry-to-field bridge. Work 111 can proceed alongside meshing once the spatial contract is stable; this is a dependency option, not authorization to launch parallel agents. Works 116 and 122 prevent local part optimization from drifting away from system benefit. Works 130–132 require separate user authority, facilities and qualified safety review; this planning request does not authorize fabrication or testing.

## 12. Milestones: outcomes rather than document counts

### M1 — Unfamiliar material geometry causes verified field response

Complete the capability represented by Works 107–110. A generated asymmetric/curved/void-containing shape is meshed from actual geometry and changes vector structural response under geometric mutation. A same-topology shape may qualify. Report geometric and discretization error independently. This is the first major engineering advance required, not a new vehicle-ready label.

### M2 — Detailed functional connection and small coupled assembly

Complete the relevant Works 111–116. Show a real connection at fastening-scale detail, moving/contact behavior where required, and a coupled thermal/mechanical or architecture/part feedback case. Produce section views, internal geometry and causal negative controls. It remains a subsystem proof, not a complete car.

### M3 — Digitally complete vehicle candidate

Complete relevant domain packages and Works 122–125. Every necessary physical path is realized, not all possible technologies. Show an assembly, internal parts, bill of material regions, motion/clearance audit, geometry-derived mass/inertia and a coupled simulation with explicit uncertainties. If essential physics is unresolved, call it a detailed exploratory candidate, not a promoted vehicle.

### M4 — Evidence-backed discovery claim

Complete Works 126–129 for the declared claim. Demonstrate robust whole-vehicle benefit beyond numerical uncertainty against fairly optimized baselines and independent analysis. A negative comparison is useful evidence, but does not achieve a performance-discovery milestone. External novelty requires a separate prior-art investigation; unusual geometry alone does not prove it.

### M5 — Physical validation in progressively larger scope

Carry out authorized Works 130–132. Numerical convergence and independent solvers increase confidence but are not substitutes for measurements. Calibration evidence and validation evidence remain separate. A coupon pass does not certify a whole vehicle, and no roadmap guarantees a new racing technology or superiority over existing race cars.

## 13. Immediate next work specification: Work 107

Objective: make physical material/void geometry the shared source of truth before expanding the optimizer. Deliver executable code and generated evidence, not another report-only readiness gate.

Proposed files, to confirm against current package boundaries when execution begins:

- `src/formula_ultimate/components/spatial_material.py`: region/material/void/frame schema and physical ownership.
- `src/formula_ultimate/components/spatial_material_cad.py`: adapter from existing free-form B-rep construction and independent measurements.
- `config/cad/spatial_material_corpus_v1.json`: frozen positive and negative geometry cases.
- `scripts/cad/run_spatial_material_corpus.py`: build, inspect, record provenance and replay.
- `tests/test_spatial_material.py` and `tests/test_spatial_material_cad.py`: pure-contract and actual-CAD tests, separately identified.
- `docs/contracts/SPATIAL_MATERIAL_V1.md` and Thai companion; new bilingual work logs.

Proposed contract fields: `schema_version`, `candidate_id`, `revision`, `units`, `frames`, `material_regions`, `void_regions`, `interfaces`, `geometry_source`, `material_source`, `tolerances`, `evidence_refs`. These are planned identifiers, not fields currently supported by the code.

The initial corpus must exercise a curved variable section, an asymmetric cavity, a branch/merge region, touching multi-material regions, and disconnected declared bodies. These are contract tests, not the only admissible shapes. Negative controls include undeclared overlap, cavity loss during export, non-finite geometry, missing material provenance, duplicated ownership and stale evidence after mutation. Homogeneous mass-property reference cases are allowed to verify the machinery.

Required run products: candidate definition, actual geometry export, material/void manifest, mass/center-of-mass/inertia measurements, independent CAD comparison, discrepancy report, source hashes and replay report. A controlled cavity or material change must change the appropriate physical quantities; rigid placement changes must transform inertia correctly without changing intrinsic mass.

Before admitted execution, use a disclosed pilot to fix length/volume/mass/inertia tolerances based on kernel behavior and the smallest intended feature. Record those values in the Work 107 plan/config before the comparison. Success requires every positive case to satisfy its declared invariant, every negative case to fail visibly for its intended reason, and replay to satisfy the registered exact/toleranced identity rules. Do not weaken thresholds after seeing an admitted failure.

Validation layers: pure Python schema/math tests; actual CAD build/export; independent geometry inspection; mutation-causality tests; unit/frame invariance; deterministic provenance; repository bilingual checks. CAD-dependent tests must actually run in the CAD environment before claiming the adapter works; a skipped dependency test is not a pass for this exit gate.

Non-goals: a new universal implicit solver, arbitrary threads, nonlinear contact, whole-vehicle simulation or a discovery win. The handoff to Work 108/109 is a trustworthy geometry/material input, not a physically validated part. Fix only existing code defects that block this contract and log that scope explicitly; schedule other intake/accounting corrections with their owning future package.

## 14. Experimental design and falsification

Each admitted study must register the following, with numerical choices calibrated separately and frozen before results:

| Item | Detailed-part study | Whole-vehicle study |
|---|---|---|
| Independent variables | Representation, material/void edits, joining strategy, topology, optimizer/fidelity policy | Architecture, part variants, interaction paths, controller policy and fidelity policy |
| Dependent variables | Mass, compliance, losses, capacity, thermal response, failure margins, compute cost | Race completion/time, primary energy, thermal/structural margins, robustness and total search/validation cost |
| Controls | Same terminal task, materials/process assumptions, seed pairing, total budget, optimized fixed family and random search | Same external race/environment/energy rules, library opportunity, optimized baseline and controller adaptation resources |
| Causal interventions | Remove/sever/reconnect paths; perturb active surfaces; suppress coupling; same-topology shape substitution | Exchange one subsystem, keep vs retune controller, include cooling/support/containment changes, disable proposed mechanism |
| Success | Registered useful effect exceeds numerical/measurement uncertainty and constraints hold within scope | Registered whole-system benefit survives fair comparison, holdout, uncertainty and independent checks |
| Failure | Benefit disappears under geometry-derived fields, defects exploit coarse models, or cost/constraints invalidate comparison | Race incomplete, benefit moves into omitted hardware/energy, failure margins violated, holdout or stronger physics contradicts claim |

Track improved, worsened and indistinguishable outcomes separately. Convert error estimates to the same units as the compared quantity before assessing detectability; correlated errors require an appropriate comparison method. Never use absolute response difference as a signed improvement.

Use score-independent audits of candidates rejected by cheap evaluators. Distinguish physical infeasibility from meshing/solver failure and unevaluated proposals. Reusing the same mathematical implementation behind two wrappers is not an independent physical reference. Verify current holdout provenance before any fresh scientific comparison; previously inspected conditions remain calibration/exploratory evidence.

Every result includes supporting evidence, contradicting evidence, alternative explanations, missing evidence and confidence. Candidate failure is a legitimate experiment outcome; passing the software tests does not make the scientific hypothesis true.

## 15. Practical compute and scheduling strategy

Do not promise a finish date from the number of remaining work IDs. Run cost pilots at each new geometry/physics scale, measure bottlenecks and revise the execution plan transparently. A work ID is a bounded deliverable, not a fixed number of hours.

Use coarse-to-fine screening, local submodels and validated reductions. Cache only when all causal input identities and validity envelopes match. Exploit sparse/local structure and warm starts with accounting; never turn solver non-convergence into an artificially favorable score. Allocate detailed simulation to uncertainty-sensitive decisions and audit a score-independent sample of unfamiliar representations.

A whole-car mesh resolving every small thread and every transient fluid scale simultaneously is not the starting computation. Partition by physical interactions and transfer quantities with residual checks. Refine the influential local regions while retaining complete geometry and keeping reduction error observable. If the compute budget cannot resolve a decisive mechanism, report an unresolved comparison rather than declaring a winner.

At each milestone report progress in realized functions, geometry coverage, verified domains, model applicability, complete-path closure and wall-time-to-evidence. Do not report percentage completion solely from number of documents, operators or passing tests.

## 16. Risks, stop rules and recovery

| Risk or observation | Required response |
|---|---|
| CAD kernel rejects unfamiliar but plausible shapes | Preserve proposal and failure diagnostics; refine representation/export and audit bias; no physical-impossibility claim |
| Mesh or solver fails on thin/slender/contact geometry | Classify unresolved; inspect quality, scaling and missing formulation; no hidden geometry repair or fictitious supports |
| Local improvement disappears in assembly | Record negative evidence; revise the architecture/part pair and re-derive loads; do not hide transferred mass or heat |
| Apparent novelty is an inactive appendage | Causal ablation; exclude the inactive addition from functional novelty while preserving provenance |
| Same graph has a useful shape-induced effect | Admit to functional/performance analysis; graph change is not required |
| Optimizer exploits omitted physics/material limits | Block stronger claims, add an evaluator/coverage task and new registration; preserve the exploit as a regression case |
| Cost accounting or source provenance is incomplete | Block fairness/admission claims; do not backfill unknown measurements with zero |
| Physical testing is unsafe or unauthorized | Stop that test stage; retain digital work and request the necessary authority/facility review |

## 17. Tooling boundary and primary references

Retain the existing CAD stack where its measured behavior is adequate. Evaluate candidate meshing/solver/coupling backends against the roadmap fixtures, reproducibility, Windows availability, licensing, inspectability and measured cost before choosing or installing them. No backend is selected or installed by Work 106.

Possible infrastructure directions, verified against primary documentation on 2026-09-07:

- Gmsh documents OpenCASCADE/discrete model entities and mesh-size fields; that makes it a candidate for a geometry-to-mesh adapter, not evidence that this repository already has one. [Gmsh reference manual](https://gmsh.info/doc/texinfo/gmsh.html).
- MFEM provides finite-element examples including linear and nonlinear elasticity. Such examples can inform verification and backend trials; they do not validate this project's contact, materials or vehicle. [MFEM examples](https://mfem.org/examples/).
- OpenMDAO documents coupled multidisciplinary analysis/optimization. A coupling framework may organize solvers and derivatives, but does not supply missing physical models or turn topology mutations into smooth variables. [OpenMDAO documentation](https://openmdao.org/newdocs/versions/latest/).

The representation, multiscale design and delivery sequence here are project proposals, not claims established by those external manuals. Future method-specific implementations require their own source review and validation plans.

## 18. Final acceptance checklist

The detailed digital destination is reached only when the selected whole candidate has:

- Complete required physical geometry, internals and connection details, inspectable both assembled and sectioned.
- Traceable material regions and real functional paths; no unexplained hardware, double-counted matter or free ideal resources.
- Geometry-derived mass/inertia, packaging, motion/contact, structure, thermal and relevant flow/energy/control evidence.
- Coupled simulation tied to that exact geometry revision, with declared numerical and model uncertainty.
- Appropriate manufacturing/tolerance evidence for the claimed readiness level.
- Fair optimized baseline comparison and falsification evidence for any claimed benefit.
- Explicitly bounded claims: digital completeness, numerical verification, scientific validation and physical validation are different achievements.

The immediate direction is therefore not “make another familiar-looking vehicle with more bolts.” It is “make spatial material geometry causally evaluable, prove a detailed connection, couple parts and architecture early, and expand verified coverage until every required path of a complete vehicle is realized.”
