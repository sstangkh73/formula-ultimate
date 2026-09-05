# Generation-First, Physics-Evaluation Roadmap V1

Thai companion: `GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.th.md`

## Decision

Formula Ultimate should not use known vehicle shapes, frozen component families, manufacturability heuristics, or a solver's current coverage to decide what may be born. The search should first instantiate an unfamiliar but finite and traceable candidate, then use geometry-derived physics to answer what it does, where forces and energy flow, how it fails, how much it carries, and whether it is better under the declared task.

Physics remains mandatory. Its role changes from **shape permission** to **measurement, explanation, comparison, and promotion evidence**. A physically failed candidate is a valid measured result. A numerically unresolved candidate is not a physical failure. A manufacturing-incompatible candidate may remain a research stepping stone but cannot be promoted as a buildable design.

This document records the before-state and the proposed architecture. It does not claim that the new architecture is implemented.

## 1. Before-state: what the repository actually does

| Layer | Demonstrated state | Consequence |
| --- | --- | --- |
| Work 050/090 whole-vehicle search | Five bounded scale variables modify a fixed primitive assembly. The 288-candidate census measured primitive fraction `1.0`, one topology signature, and one functional-path signature. | Many dimension combinations exist, but no architectural or functional-morphology search occurs. |
| Work 091 wire grammar | Twelve declared profiles exercise polygon, arc, conic, Bézier, B-spline, hole, trim, offset, and transform support. | Curves are executable, but the control points and profiles form a frozen test corpus rather than evolvable genes. |
| Work 092 solid grammar | Ten hand-declared candidates exercise sweep, loft, shell, ribs, booleans, fillets, patterns, and multi-solid construction. | Non-primitive CAD is possible, but the search does not invent new feature graphs or numerical parameters. |
| Work 093 topology genome | Six typed graphs represent different part/interface/path structures, with up to eight parts. Parts reference exact Work 092 source-solid identities. | Graph diversity can be represented, but geometry is selected from a library. |
| Work 094 mutation | Eight fixed operators act on the typed graphs. Solid replacement chooses another frozen source candidate; feature insertion adds only a parameter-free `transform`. The retained result says `cad_executed: false`; crossover is disabled. | Accepted mutations are graph proposals, not newly generated physical geometry. |
| Work 095 constructive/manufacturing gate | A pre-performance gate demonstrates rejection accounting over matched synthetic scalar fixtures. It did not measure the referenced STEP files. | Gate behavior is tested, but using it unchanged as an early search filter would encode process assumptions before functional value is known. |
| Work 096 semantic witness | FreeCAD measures ten exact STEP candidates and assigns fixed support/load/contact/thermal/fluid selectors. | Geometry measurements exist, but semantic boundary regions are not yet inherited from an arbitrary candidate's functional genotype. |
| Work 097 structural benchmark | Seven frozen source candidates map to seven frozen response models and expected beam/shell/solid/contact classes. | Reduced-order verification works for those adapters, not for an unseen candidate. A baseline state mismatch raises rather than becoming a normal search outcome. |

Evidence: [Work 090 result](../work_logs/2026-09-04_090_search-space-bias-diversity-contract-result.md), [Work 094 result](../work_logs/2026-09-04_094_reproducible-topology-mutation-recombination-result.md), [Work 095 result](../work_logs/2026-09-04_095_constructive-validity-manufacturing-gate-result.md), [Work 097 result](../work_logs/2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.md), and the independent [Work 102 simulator-gap review](LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md).

The central missing causal loop is:

```text
evolvable morphology parameters
  -> executable new geometry
  -> geometry-derived boundary conditions and fields
  -> measured outcome returned to search
  -> next morphology proposal
```

No current runner connects all five steps. Work 094 ends before CAD; Work 095 is a synthetic fixture; Work 097 starts from frozen Work 096 evidence.

## 2. Root cause, not symptom

Angular or familiar-looking parts are primarily a representation problem, not proof that physical law favors boxes.

1. The old active search changes only dimensions of known primitives in [`whole_vehicle_search.py`](../../src/formula_ultimate/experiments/whole_vehicle_search.py).
2. The newer free-form capability is a corpus declared in JSON, not a generator distribution learned or mutated by the agent.
3. [`topology_mutation.py`](../../src/formula_ultimate/search/topology_mutation.py) mutates graph structure but carries source-solid IDs; it does not mutate section control points, path fields, wall fields, voids, branch radii, or material distribution.
4. [`generalized_geometry_benchmarks.py`](../../src/formula_ultimate/structural/generalized_geometry_benchmarks.py) selects physics by frozen case identity and expects frozen intact outcomes. It is a benchmark, not a search evaluator.
5. The current semantic selectors choose geometric extremes and largest faces. Those rules can misidentify function on an unfamiliar mechanism.

Adding more rounded templates would increase appearance variety but preserve the same cage. The required change is to make morphology and functional topology executable genes, not to add a larger catalog of named shapes.

## 3. Constraint reclassification

Every constraint must state when it acts and what state it produces.

| Constraint | New treatment | Reason |
| --- | --- | --- |
| Finite numeric values, SI units, bounded memory/time/evaluations | Hard before execution | Required for a defined, reproducible computation. |
| Seed, genotype, operator trace, code/tool identities | Hard before execution | Required for exact replay and fair comparison. |
| No undeclared energy/source, no hidden repair, no result leakage | Hard throughout | Prevents simulator exploitation and invalid scientific comparison. |
| External task terminals and environment | Hard task contract | Defines the job without prescribing the internal shape. |
| Conventional wheel count, chassis layout, symmetry, named part family | Not a constraint unless the task explicitly requires it | These are historical priors, not universal physics. |
| B-rep single-solid requirement | Replace with representation-specific status | Shells, lattices, multi-body mechanisms, and implicit fields may be legitimate. Require the declared representation to instantiate, not one solid for all designs. |
| Minimum wall/radius/feature, tool access, overhang, enclosed void | Measure after geometry; hard only for a declared manufacturing promotion route | These depend on process and may erase high-value research stepping stones if applied before function is measured. |
| Stress, displacement, buckling, fracture, fatigue, contact, heat, flow | Physics outputs | Return values, fields, uncertainty, failure locations, and thresholds; do not prevent candidate birth. |
| Solver convergence and meshability | Numerical evidence state | `numerically_unresolved` is distinct from `physically_failed`. |
| Safety, buildability, calibrated material evidence, holdout validation | Hard promotion requirements | Necessary before build/design claims, not before exploratory generation. |
| Novelty | Archive/selection objective only | Novelty cannot compensate for energy violation, physical failure, or missing evidence. |

## 4. Target candidate lifecycle

### Stage 0 — Freeze the task, not the solution

Declare only external functional terminals, load/energy/environment histories, usable envelope or interaction domain, finite resources, material evidence classes available to the study, evaluation budget, and success metrics. A ground-interaction trial may declare ground contact and body load terminals; it must not declare wheels, count, axle layout, or known suspension geometry.

### Stage 1 — Propose an evolvable causal genotype

The genotype contains a variable-length geometry/assembly program, typed functional terminals, material/process hypotheses, controller genes when motion is active, and provenance. It may refer to generic operators but not require a source candidate from the frozen Work 092 catalog.

### Stage 2 — Instantiate geometry

Execute the genotype into one or more declared representations: B-rep solids/shells, beam or shell networks, lattice/field structures, and later implicit/voxel fields. Record every kernel call and failure. No hidden healing is permitted. A failed instantiation becomes `representation_invalid`, consumes its declared budget, and remains in the ledger.

### Stage 3 — Measure geometry without judging performance

Recover volume, area, mass from material distribution, centre of mass, inertia, bounds, connected components, thickness samples, curvature, section fields, clearances, intersections, and semantic terminal geometry. Measurements and sampling uncertainty are outputs. Do not label a thin wall physically failed before applying load.

### Stage 4 — Bind function to geometry

Support, load, contact, fluid, thermal, electrical, and control regions must originate from typed terminal ancestry in the genotype and survive geometry exchange through signatures. Geometric rules such as largest face may be fallback hypotheses, never silent truth. Ambiguous or missing binding becomes `boundary_unresolved`.

### Stage 5 — Attempt physics

Run a declared multi-fidelity ladder against every representation-valid candidate within budget. Start with conservation and analytical bounds, then geometry-derived mesh/field solutions, contact/motion/thermal/flow solves, and coupled evaluation where relevant. Model choice must depend on measured geometry and error estimates, not candidate names.

### Stage 6 — Return an outcome, not a binary disappearance

Record forces, reactions, moments, energy transfers, displacement/stress/temperature/flow fields, contact states, eigenmodes, margins, failure initiation, failed paths, residual histories, mesh convergence, uncertainty, compute, and limitations. The evaluator returns one of the state classes below; it does not raise merely because a candidate is weak.

### Stage 7 — Evaluate manufacturing independently

Evaluate all declared compatible processes where affordable. Return process-specific wall/access/support/tolerance/cost outcomes. A design can be incompatible with machining but compatible with additive or an unmodeled future process. Manufacturing status does not rewrite physics status.

### Stage 8 — Archive and select

Use quality-diversity selection over functional and causal descriptors. Maintain separate feasible, physically failed, manufacturing-incompatible, and numerically unresolved archives. Sample across these archives so that a near-feasible unusual mechanism can become a stepping stone rather than vanish.

### Stage 9 — Promote with stronger evidence

Only promotion requires all mandatory physical, numerical, manufacturing, safety, holdout, replay, and independent-validation gates. A promoted candidate may be called a survivor only at the fidelity actually passed.

## 5. Required state taxonomy

| State | Meaning | Search use | Promotion |
| --- | --- | --- | --- |
| `generated` | Genotype serialized with complete provenance | Await execution | No |
| `representation_invalid` | Declared geometry representation could not instantiate | Retain failure cause; may inform mutation | No |
| `geometry_measured` | Geometry exists and required measurements completed | Continue | No |
| `boundary_unresolved` | Function-to-geometry terminal binding is missing or ambiguous | Retain separately; attempt declared binding refinement | No |
| `numerically_unresolved` | Mesh/solver/error gates could not produce a trustworthy result within budget | Retain separately; never call physical failure | No |
| `physically_failed` | A converged/evidence-admitted solve crossed a declared physical limit | Retain fields, margins, and failure path as evolutionary information | No |
| `physically_feasible` | Passed current physical fidelity only | Eligible for manufacturing and next fidelity | Not automatically |
| `manufacturing_incompatible` | No tested process met the declared production target | Retain as research stepping stone | No |
| `candidate_survivor` | Passed the trial's preregistered physics, process, holdout, and replay gates | Eligible for subsystem comparison | Trial scope only |
| `promotion_ready` | Passed independent higher-fidelity and safety evidence required by the declared use | May enter later integration | Yes, only for declared scope |

These states must be mutually distinguishable in data and reporting. `invalid`, `failed`, and `not ready` must not be collapsed into one Boolean.

## 6. Genotype and operator redesign

### Geometry genes

- variable-length feature DAGs with executable parameters;
- curve/surface control points, knots, degree, continuity and local refinement;
- paths, sections, taper/twist fields and wall-thickness fields along normalized material coordinates;
- branch/merge/split operations with junction blending determined by genes rather than named family;
- constructive void and material-add/remove regions;
- beam/shell/lattice graphs with continuous node positions and section fields;
- optional implicit scalar fields and material occupancy after an independent extractor exists;
- multi-body and moving-pair declarations;
- spatially varying material hypotheses, limited to declared material evidence classes.

### Functional genes

- external terminal identity and domain;
- source/sink/bidirectional role;
- allowed motion and contact hypothesis;
- load/energy/fluid/thermal/control path ancestry;
- sensor/actuator/controller parameters where behavior depends on control;
- failure propagation edges that are derived from the candidate graph, not manually assigned after results.

### Mutation/recombination operators

- perturb, insert, delete, split, merge, rewire and duplicate control points or field regions;
- grow/prune branches without forcing every new part to carry every domain;
- change representation locally while preserving terminal mapping;
- add/remove voids, ribs, shells, lattices, compliant regions and moving pairs without selecting a named vehicle part;
- change local material/process hypotheses without preselecting one manufacturing winner;
- recombine typed cut boundaries after compatibility is proven;
- co-mutate geometry and controller genes for active mechanisms.

Every operator must produce an executable parameter trace. A morphology operator that only changes an ID, label, or rigid transform does not count as new geometry.

## 7. Physics as an observer

The search-facing evaluator must accept an unseen geometry record and return evidence rather than require a case name from a frozen list.

1. Determine candidate analysis representations from geometry/error criteria. Several models may be attempted; disagreement is evidence.
2. Generate meshes from the actual candidate geometry. Store node/element sets tied to terminal signatures.
3. Apply loads and constraints from terminal ancestry.
4. Recover reactions independently from the solve. Do not construct zero residual by adding a load to its manually negated value.
5. Store displacement, stress/strain, contact traction/penetration, temperature/flux, flow/pressure, and state histories when applicable.
6. Run at least three declared refinement levels for a promoted structural result; record non-monotonicity and solver failures.
7. Separate model-form disagreement, discretization error, material uncertainty, and numerical failure.
8. Return continuous margins and localized failure evidence even when the candidate fails.

Physics determines whether a candidate survives the declared task. It does not decide which shapes are allowed to be proposed.

## 8. Quality-diversity and stepping-stone retention

The archive should index what the candidate causally does, not merely how curved it looks. Candidate descriptors may include typed topology, terminal-to-terminal path structure, branch/cycle rank, deformation mode, load-path redundancy, motion class, energy conversion path, heat-rejection route, mass/inertia distribution, section-field variation, material occupancy, and failure mode/location.

Within each niche, store at least:

- best physically feasible quality;
- nearest physical margin below feasibility;
- best manufacturing-compatible quality;
- least expensive unresolved candidate worth fidelity escalation;
- novelty and ancestry without allowing novelty to erase failure.

An infeasible candidate may reproduce under a bounded stepping-stone policy if it improves a continuous margin, opens a new functional niche, or resolves a previously missing path. Reproduction rights and compute must be explicit so the infeasible archive cannot consume the campaign silently.

## 9. Multi-fidelity and fair compute

Primitive geometry often meshes faster than free-form, multi-body, or contact-rich geometry. Equal candidate count alone is unfair. Record and control attempted proposals, CAD-kernel calls, meshing attempts, elements/DOF, nonlinear iterations, wall time, memory, and fidelity promotions.

Use a staged budget:

1. cheap representation/measurement for all generated candidates;
2. physics proxy for all representation-valid candidates;
3. stratified promotion independent of proxy score to estimate false negatives;
4. score-based and novelty-based promotion under separately reported budgets;
5. refined/independent solves for finalists.

A cheap proxy may prioritize compute but may not define physical truth. Proxy false-negative and false-positive rates must be measured on promoted samples.

## 10. Revised execution of Works 098–101

### Work 098 — Generation-First State and Fairness Protocol

- replace the linear pass/reject ladder with the state taxonomy in this document;
- define which checks are pre-execution invariants, measured outcomes, and promotion gates;
- specify budget accounting for CAD, meshing, solver, unresolved and stepping-stone paths;
- add an ablation protocol comparing pre-manufacturing rejection against evaluate-first manufacturing annotation;
- preserve the existing multi-fidelity/fairness goal while preventing cheap proxies from deleting all unfamiliar candidates.

Exit condition: a frozen protocol can replay a mixed ledger containing every state class, with no state conflation and no post-result hidden repair.

### Work 099 — Executable Morphology and Quality-Diversity Agent V1

- extend the genome with numerical geometry parameters and terminal ancestry;
- implement morphology-changing CAD operators, not library replacement alone;
- connect proposal to CAD execution and geometry measurement;
- implement feasible/infeasible/unresolved quality-diversity archives;
- prove that a morphology operator changes executable geometry hash and measured fields while preserving replay.

Exit condition: multiple seeds generate previously undeclared geometry identities and non-isomorphic functional graphs; failures remain measured ledger entries. This does not yet prove useful physics.

### Work 100 — Isolated Functional Discovery Trials

- freeze only external terminals, loads/environment, resources, evaluator identities, and budget for each subsystem trial;
- run generation-first search with actual geometry-derived field solvers;
- compare conventional, random, graph-only, morphology-only, and joint morphology/controller controls;
- retain rejected and unresolved archives; promote stratified samples to audit proxy bias.

Exit condition: at least one previously undeclared, non-primitive, non-isomorphic candidate reaches `candidate_survivor` under converged physics, replay and the declared manufacturing route. It need not beat an optimized baseline yet.

### Work 101 — Free-Topology Integration and Evidence Promotion

- integrate only subsystem survivors through typed terminals;
- allow integration failures to flow back as interface/load/control evidence rather than forcing a conventional chassis;
- run coupled transient, energy, thermal, contact, failure, holdout and independent higher-fidelity gates;
- compare against fair optimized fixed-topology baselines.

Exit condition: a whole candidate completes the declared task and passes all promotion gates. This remains simulation evidence until independent physical validation exists.

## 11. Falsifiable experiments

| Experiment | Independent variables and controls | Dependent evidence | Success / failure |
| --- | --- | --- | --- |
| Representation freedom | Old five-scalar search, frozen-library topology mutation, executable morphology mutation; matched seeds and compute | New geometry hashes, topology/path signatures, control-point/field changes, CAD success, duplicate rate | Success requires executable geometry not present in the source corpus and causal descriptor diversity. Failure if diversity is only scale, transform, rename, or cached-library substitution. |
| Gate-order ablation | Pre-performance manufacturing rejection versus evaluate-first annotation; same proposals and physics budget | Candidates reaching physics, functional niche coverage, physical margins, later process compatibility, compute | Success if the new order recovers credible functional stepping stones without increasing unsupported promotions. Failure if recovered candidates are only invalid/exploitative or compute is uncontrolled. |
| Boundary binding | Fixed geometric selectors versus genotype-terminal ancestry; same geometry/load cases | Region correspondence, reactions, path continuity, ambiguity rate | Success if terminal-derived binding survives transformations and matches independent fixtures. Failure if largest/extreme faces silently change function. |
| Physics outcome integrity | Current reduced adapter versus actual geometry mesh/solver at three refinements | Fields, recovered reactions, residual histories, convergence, failure location, disagreement | Success requires independent residual/reaction evidence and bounded refinement disagreement. Failure if residual is true by construction, fields are absent, or a solver error is labeled physical failure. |
| Stepping-stone archive | Feasible-only selection versus bounded feasible/infeasible/unresolved archive | Feasible niche coverage, time to survivor, lineage from failed states, compute share | Success requires preregistered improvement across paired seeds. Failure if unresolved candidates dominate compute or no survivor uses retained stepping stones. |
| Manufacturing timing | Single early process gate versus post-physics multi-process evaluation | Functionally valuable candidates lost early, process-specific feasibility, final promotion rate | Success if early annotations preserve useful alternatives while final promotions remain equally strict. Failure if buildability claims weaken. |

Thresholds and statistical tests must be frozen in Work 098 before observing the admitted experiment. One attractive candidate is not evidence that the new system is better.

## 12. System-level success criteria

The new architecture is working only when all of the following are evidenced:

1. a search child can contain executable geometry parameters absent from every source candidate;
2. proposal, CAD, measurement, boundary binding, physics, outcome, archive and next proposal run in one replayable loop;
3. an unseen geometry can be evaluated without a frozen case/candidate ID;
4. physical failure returns measured margins, fields and affected paths rather than an evaluator exception;
5. numerical inability is never mislabeled as physical failure;
6. manufacturing incompatibility is process-specific and blocks promotion without erasing early evidence;
7. physics and energy constraints remain identical across conventional and unfamiliar candidates;
8. free-form representations receive audited compute opportunity rather than losing automatically because they cost more;
9. a candidate survives holdout and independent higher fidelity before any performance/discovery claim;
10. optimized fixed-topology baselines remain the comparison, not the prescribed answer.

## 13. Risks and controls

- **Search explosion:** variable-length geometry has enormous dimensionality. Control with staged budgets, developmental encodings, lineage-aware archives, and multi-fidelity promotion—not named-shape restriction.
- **Kernel fragility:** B-rep operations may fail frequently. Retain exact failure causes and add alternative representation routes; never heal silently.
- **Proxy exploitation:** audit conservation, boundary work, contact energy, mesh dependence, and out-of-distribution promotion samples.
- **Unresolved archive growth:** cap reproduction and escalation budgets separately while retaining metadata for diagnosis.
- **Manufacturing deferred too far:** measure early when cheap, but make it destructive only at a declared promotion stage.
- **Novelty theater:** require functional/topological/field distinctions and fair baseline performance, not visual unusualness alone.
- **Physics coverage bias:** publish unsupported domains and solver applicability; unsupported physics blocks promotion but does not retroactively prohibit the genotype language.

## 14. Explicit non-goals

This plan does not remove conservation, finite resources, race rules, safety, manufacturing, evidence, holdouts, or independent validation. It does not promise unrestricted mathematical forms, infinite parts, magic materials, free compute, or acceptance of invalid solver output. It does not call a simulation survivor a real-world validated component.

The change is narrower and more important: **allow unfamiliar candidates to exist as traceable computational objects, then let measured physics determine what they mean and how far they may be promoted.**
