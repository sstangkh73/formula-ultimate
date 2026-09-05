# Whole-Vehicle and Technology Discovery Protocol V1

Thai companion: `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Protocol ID: `FU-WHOLE-VEHICLE-DISCOVERY-V1-2026-09-06`

Status: Normative design protocol; implementation pending

Documentation work: Work 104; implementation sequence: Works 098–101

## 1. Authority, purpose, and preserved predecessor

This protocol governs the next implementation of Works 098–101. It supersedes their execution guidance in the [generation-first roadmap](../reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md), including the requirement that only isolated subsystem survivors may enter any integration experiment. That restriction is replaced by separate exploratory-integration and evidence-promotion rules. Existing work logs and experiment evidence remain historical records; this document does not retroactively change their results.

The mission is to generate a complete three-dimensional racing vehicle and discover useful component geometries, mechanisms, multifunctional structures, and system architectures that were not prescribed as the answer. The design may change how the vehicle is divided into parts and how those parts cooperate. Human component names and conventional vehicle layouts are optional baselines, not a mandatory construction grammar.

Exact pre-change backups dated 2026-09-06 are preserved in [English](../reports/backups/2026-09-06_104/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md) and [Thai](../reports/backups/2026-09-06_104/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.th.md). Their SHA-256 values are:

| File | SHA-256 |
| --- | --- |
| `GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` | `686b81df2f98b566775010aabcf225ae32a8552f9ec1818d43b1457070dbc449` |
| `GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.th.md` | `f86ee5472f5afe02f18ac14685dcf755de7a56bd82c5ade960cc2b51d71338c3` |

Backup contents are immutable byte copies; their internal relative links retain the original `docs/reports/` context. See [Work 104 plan](../work_logs/2026-09-06_104_whole-vehicle-discovery-protocol-plan.md) and [result](../work_logs/2026-09-06_104_whole-vehicle-discovery-protocol-result.md) for change evidence.

## 2. Ultimate objective and claim boundary

For a registered race environment `r`, optimize:

```text
d*_r = arg min_d T_race(d, r)
subject to RaceCompleted(d, r) = true
initial primary energy <= registered energy budget
external primary-energy addition during the race = 0
all required physical, numerical, safety, manufacturing and evidence gates pass
```

All primary propulsion energy is onboard before the race. Recovery must trace to declared physical flows with observable losses; no double counting or undeclared external energy is allowed. Use SI units and a pinned race/energy profile. Technology-neutral comparisons account for energy-carrier mass, containment, conversion hardware, losses, and thermal consequences. A joule allowance alone is not a complete vehicle model.

Race time is the ultimate objective. Intermediate task metrics and diversity preserve useful search directions; they do not waive final feasibility. An unusual shape is not by itself a new mechanism, a simulated survivor is not a physically validated product, and a design absent from this repository is not automatically novel in the wider world.

This document establishes requirements only. It implements no generator, arbitrary-geometry solver, vehicle discovery loop, scheduler, or validated technology. A completed software protocol fixture establishes software behavior only.

## 3. Freeze the external task; evolve the internal solution

| Frozen for an admitted comparison | Evolvable within the registered language and resources |
| --- | --- |
| Track, environment, task histories, race completion and safety requirements | Whole-vehicle architecture, shape, packaging and dimensions |
| Initial energy opportunity, resource limits, material evidence classes | Energy storage/conversion/recovery arrangement and physical paths |
| External interaction requirements and permitted exchanges with the environment | Ground-interaction mechanism, number/location of contacts and internal motion |
| Evaluator versions, applicability rules, evidence gates and budgets | Part count, part boundaries, interfaces and material distribution |
| Analysis plan, baseline opportunities and holdout policy | Controller, sensors, actuators and geometry/control coordination |

Do not impose wheels, axle count, chassis arrangement, symmetry, named powertrains, or named part families unless a particular registered task explicitly requires them. Any such restriction must be reported as a study boundary, not a universal physical law.

A local trial may freeze external functional terminals to isolate a question. At vehicle level, the choice of local tasks and internal terminals may evolve through versioned task proposals. Changing an internal decomposition does not permit changing the external race, energy or safety requirements. Candidate-specific loads must be derived under the same vehicle/environment evaluation rules, not hand-selected to favor a design.

Every generated proposal has finite values, bounded representation complexity, a seed/lineage, executable parameters, and code/tool identities. These are execution invariants. Manufacturing preferences and evaluator coverage are not permissions to define which conventional shapes may exist.

## 4. Evolvable representation and multifunctional organization

The genome is a variable-length executable geometry/assembly program with material hypotheses, functional terminal ancestry, motion/contact declarations, and controller genes where relevant. It may instantiate solids, shells, beam/lattice networks, multi-body systems, or other explicitly supported representations. A universal single-solid condition is prohibited.

Operators must be able to change numerical geometry, add/remove material and voids, grow/prune/rewire paths, split/merge components, and relocate or redefine internal interfaces while maintaining typed physical meaning. Control parameters and geometry may co-evolve. A source-catalog identity, label change, or transform-only operation is not evidence of a new shape. A changed arrangement may still be functionally meaningful and must be assessed as arrangement evidence.

One physical region may serve multiple functions; one function may span multiple regions. Do not require one component per function or require every component to support every physical domain. For example, a proposed load-bearing region may also contain a cooling path; its stiffness, heat transfer, pressure loss and mass must be measured rather than asserted by the genome. This example is a permitted hypothesis, not a prescribed design or demonstrated discovery.

Mass, energy, volume and material ownership must remain consistent across overlapping functional descriptions. A multifunctional region is not counted as separate physical copies. Multi-body contact and permitted motion must be distinguished from unintended overlap; shell/network validity must use the declared representation's rules.

## 5. Coupled discovery loop and two integration permissions

```text
whole-vehicle architecture and controller proposal
  -> task and interface hypotheses derived from vehicle behavior
  -> executable geometry, material and mechanism proposals
  -> measured local evidence and applicability limits
  -> exploratory coupled vehicle evaluation
  -> race/task effects, failure paths and uncertainties
  -> revised architecture, decomposition, geometry and controller
  -> stronger evidence and eventual promotion
```

**Exploratory integration** may combine candidates with incomplete local evidence to test coupled effects. It requires traceable geometry/model inputs, typed interfaces, declared missing domains, explicit approximations, resource accounting, and no hidden repairs. If missing evidence prevents a meaningful coupled solve, record an unresolved result; do not supply invented coefficients. Results cannot claim complete physical feasibility or promotion. Proven violations block claims but may inform a new descendant.

**Evidence promotion** requires all gates for the declared scope. Local verification remains essential for checking physical laws and identifying causes, but isolated superiority is not required of every component. A component whose benefit depends on coupling may be validated within a declared assembly. Its evidence must cover the actual assembly conditions; an isolated pass does not automatically transfer to a different vehicle.

The search must be allowed to revise architecture and controller after integration feedback. It is not limited to assembling a final vehicle from a fixed catalog of independently optimized winners. Integration failure returns affected interfaces, loads, control states, losses and uncertainty to the next proposal.

## 6. Evidence identity and orthogonal outcome state

Evidence is attached to an evaluation attempt, not to a candidate name alone. Its identity includes `candidate_id`, `genotype_sha256`, geometry/material identities, boundary/load history, controller, environment, evaluator/configuration versions, fidelity, seed, evidence class, and artifact hashes. Geometry exchange records terminal signatures and binding assumptions. Missing or ambiguous binding is an explicit outcome.

Store an append-only event history with separate dimensions:

| Dimension | Required distinctions |
| --- | --- |
| Lifecycle/representation | `generated`, `representation_invalid`, `geometry_measured` |
| Boundary binding | `not_evaluated`, `boundary_resolved`, `boundary_unresolved` |
| Physics, per domain/fidelity/load scope | `not_evaluated`, `numerically_unresolved`, `physically_failed`, `physically_feasible` |
| Manufacturing, per declared process | `not_evaluated`, `manufacturing_unresolved`, `manufacturing_compatible`, `manufacturing_incompatible` |
| Promotion, per declared use | `not_ready`, `candidate_survivor`, `promotion_ready` |
| Execution disposition | `pending`, `completed`, `budget_exhausted`, `cancelled`, `protocol_invalid` |

These are orthogonal fields, not a single mutually exclusive candidate enum. A candidate can be physically feasible at one fidelity, numerically unresolved at another, and incompatible with one manufacturing process. Manufacturing status never overwrites physics status. No tested process passing does not imply that every possible process is impossible; untested or unresolved routes remain unknown.

`physically_failed` requires evidence-admitted physical limit exceedance in its declared scope; divergence, unsupported physics, or a timeout is not proof of physical failure. A failed mesh/solve attempt is `numerically_unresolved` with its reason and execution disposition. Exhausting the budget before invoking a solver leaves physics `not_evaluated`. An admitted bound may establish a scoped failure only if its applicability was preregistered.

Missing evidence is not zero error. Invalid protocol/schema/hash/provenance must fail admission and retain diagnostic context, rather than be silently mapped into a scientific outcome. Campaign policy may quarantine a candidate-specific corrupt record; corruption of shared protocol or ledger integrity stops the affected campaign. Expected candidate failures remain ledger results, not campaign-crashing assertions.

## 7. Physics coverage and evaluator obligations

Maintain a versioned coverage registry connecting representation, physical domain, constitutive assumptions, boundary types, geometry applicability, solver, validation fixtures, error estimates and maximum evidence level. Unsupported behavior is reported as `unsupported_physics` or `unsupported_representation` under an unresolved/not-evaluated outcome as appropriate. It does not retroactively forbid the genotype language.

Evaluators must derive mass properties, interfaces and applicable response from actual geometry, materials and task conditions. Solver selection cannot depend solely on a frozen candidate name. Terminal ancestry must survive exchange; geometric selectors are declared fallback hypotheses with ambiguity checks. Coarse models need demonstrated applicability and discrepancy evidence, not merely a fidelity label.

For each relevant domain, retain fields or scoped response quantities, reactions/fluxes, residual histories, margins, failure locations, numerical errors, model-form uncertainty and material limitations. Independently recover conservation evidence where the model supports it. A balance constructed by manually negating the imposed input is not independent validation. A scalar constitutive check is not a full field-equilibrium check.

Promoted structural field results require at least three declared refinement levels, recorded failures/non-monotonicity and preregistered error gates. Exact analytical or reduced-model checks must be labeled separately and cannot substitute for missing spatial convergence evidence. Other domains require their own registered verification and convergence rules.

The search can discover new arrangements and mechanisms within represented physics; it cannot establish an unmodeled physical law by proposing a shape. Adding a physical law, constitutive model or solver capability is a separately validated work item with tests and a new evaluator identity. An admitted comparison using that change must restart under a new registration with equal access for all treatments.

## 8. Component value, vehicle value, and control fairness

Record local quality, interaction costs and complete-vehicle effects separately. Local evidence includes relevant mass, loss, capacity, response range and failure margins. Vehicle evidence includes race completion, total time, energy, thermal/structural margins and burdens transferred to other systems. An apparent component gain is not a vehicle gain if it moves cost into cooling, containment, supports or control.

Use both registered comparisons where applicable:

- **Controlled substitution:** change the target design while freezing the declared surroundings, with interface feasibility checked. This isolates a causal effect within that context.
- **Matched adaptation:** allow each treatment to adapt its vehicle and controller under the same total optimization budget, component opportunity and evidence requirements. Report design and controller spending separately. This compares achievable system benefit rather than compatibility with one inherited controller.

Do not require every exploratory child to improve race time immediately. Keep bounded archives of feasible quality, near-feasible margins, distinct functional behavior and informative unresolved hypotheses. Reproduction privileges, escalation caps and diversity descriptors must be fixed by the registration. Archive membership never grants promotion.

## 9. Resource accounting, scheduling, and proxy audits

Report proposal attempts, geometry executions, CAD calls, meshing attempts, elements/DOF, solver iterations, CPU/GPU time where available, wall time, peak memory, retries, cache hits and fidelity promotions. Peak memory is a peak, not an additive charge. Record hardware, worker count and concurrency. Unknown counters remain unknown; declared mandatory counters missing blocks fairness claims.

Each experiment defines a primary compute constraint and a resource vector with enforcement rules. Counting equal candidates alone is insufficient. Reserve resources before starting an operation; settle observed cost afterwards. Define timeout/overshoot handling, retries, duplicate work, reservation recovery after crashes, and campaign-stop conditions. All failed or unresolved attempts consume their declared cost. A retry receives its own attempt identity and must not erase the previous charge.

Partition the budget explicitly into broad cheap evaluation, score-independent stratified audits, quality/novelty promotion, unresolved/stepping-stone escalation, and finalist validation. Register each allocation and any reallocation rule before the experiment. Reserve a nonzero audit opportunity for applicable unfamiliar representations; do not spend the audit budget only on high proxy scores. Candidates not reached before budget exhaustion remain visible as `not_evaluated`.

Cache policy must disclose construction cost, reuse scope and amortization. Shared caches and precomputed models must be equally available or have their unequal opportunity reported and charged by a frozen rule. Deterministic logical scheduling uses registered ordering and tie-breaking; asynchronous execution cannot silently favor the fastest-finishing representation.

Audit proxy false negatives and false positives against stronger admitted evidence using score-independent stratified samples. Record strata, inclusion probabilities, denominators, unresolved reference outcomes and uncertainty. Correct aggregate estimates for unequal sampling or report them only within strata. Unknown higher-fidelity outcomes are not labeled negative; insufficient evidence is `not_estimable`, not a fabricated rate.

## 10. Replay, learning, and no retrospective repair

Separate two replay claims:

- **Decision replay:** consume the same immutable events, random streams, protocol and tie-break rules to reconstruct proposal identities, budget decisions, state transitions and promotion decisions exactly.
- **Execution replay:** rerun geometry/physics with pinned tools and environment; compare registered numerical tolerances and separately report timing and nondeterminism. Do not promise identical wall time or bitwise field values without evidence.

Learning from a result is allowed. Revising geometry, material, architecture, controller, interfaces or task decomposition creates a new candidate/task identity with parent links, a mutation trace and a fresh evaluation charge. The failed parent remains unchanged. Refining the same candidate creates a new evaluation attempt with its fidelity/tool identity. Explicit geometry healing that changes a design also creates a new descendant; it must not silently overwrite the parent's geometry.

Forbidden retrospective repair includes changing a previous result, criterion, load, identity or accounting record to make it pass. New results append; they do not rewrite history. Changes to the external task, evidence gates, evaluator or statistical plan require a new experiment registration. Previously observed data may be exploratory/calibration evidence but cannot be relabeled as untouched holdout evidence.

## 11. Registration and experiment design

Separate exploratory/calibration runs, software fixtures, and admitted comparisons. Work 098 freezes the protocol schema, transition rules and registration requirements. Each specific study must supply and freeze its numerical values before observing admitted outcomes; missing values block admitted execution. This document does not invent universal tolerances or sample sizes for physical domains not yet implemented.

Every registration includes:

- hypothesis, competing explanations, independent variables and controlled factors;
- task/energy/material profile, representations, operators, evaluators and applicability;
- treatment/baseline identities, seeds, optimization opportunity and controller policy;
- primary metric, direction, minimum meaningful effect, secondary metrics and units;
- physical/numerical/promotion thresholds and failure/unresolved handling;
- sample size rationale or power/precision target, statistical test, uncertainty intervals and multiplicity policy;
- budget partition, stopping rule, audit sampling, cache/retry and scheduling policy;
- exploratory/training/holdout split, leakage controls and immutable registration hash;
- supporting evidence, contradicting evidence, alternative explanations, missing evidence and confidence in the result record.

Minimum planned contrasts are:

| Experiment | Independent variable / controls | Dependent evidence and falsification |
| --- | --- | --- |
| Gate-order diagnostic | Same frozen proposals; early manufacturing rejection versus evaluate-first annotation; matched task/evaluator and declared diagnostic budget | Credible function lost early, process outcomes, compute. Falsified if recovered examples are only invalid/exploitative or unsupported promotions increase. |
| Gate-order search | Adaptive searches under matched seeds and total budgets; proposal streams may diverge | Feasible niches, time/cost to survivor, vehicle utility. A same-proposal claim is invalid once different feedback changes search. |
| Coupled discovery | Isolated-survivor-only assembly versus exploratory architecture/component/controller co-design; matched opportunity | Vehicle benefit, useful multifunctional mechanisms and validated interaction effects. Falsified if gains vanish with full cost accounting or stronger physics. |
| Representation and morphology | Frozen-library, graph-only, morphology-only and joint search controls where applicable | Executed geometry change, functional behavior, duplication and causal diversity; renaming or hash change alone is insufficient. |
| Archive retention | Feasible-only versus bounded feasible/failed/unresolved retention | Paired-seed survivor utility, ancestry and compute share; failure includes no credible benefit or uncontrolled escalation. |
| Controller fairness | Controlled substitution and matched adaptation | Local and vehicle effects plus design/controller cost; report when a benefit is controller-dependent. |

Use fair optimized conventional/fixed-topology and random controls where relevant. Equivalent opportunity does not require identical physical outcomes. Calibration-driven threshold choices must disclose the calibration set and be locked before a separate admitted run.

## 12. Promotion and discovery evidence

`candidate_survivor` means a candidate or declared coupled assembly passed its trial's registered physical, numerical, manufacturing, holdout and replay requirements within a named scope. Exploratory integration eligibility does not require this state. `promotion_ready` additionally requires independent stronger-fidelity and safety evidence for the intended use; it is not a universal property of a part.

Whole-vehicle promotion requires complete accounted three-dimensional geometry or explicitly justified representations covering the vehicle, interfaces, mass/inertia, energy carriers, motion/contact, structure, thermal behavior, flow/aerodynamics, controls and every other relevant domain. Untested relevant behavior blocks a complete-vehicle claim. Local evidence may transfer only within its registered applicability envelope; changed interfaces or loads trigger an applicability check and any required reevaluation.

Any alternative representation must still instantiate the relevant complete three-dimensional physical design. Reduced-order vehicle execution may use validated response models derived from that design; it does not exempt internal hardware, containment or interfaces from geometry and physical accounting.

Report novelty and evidence strength separately:

| Novelty question | Required basis |
| --- | --- |
| New geometry or arrangement? | Executable differences beyond identity changes; scope of corpus comparison |
| New functional behavior or mechanism? | Causal load/energy/motion/field evidence and controlled removal/substitution tests |
| Useful component or system improvement? | Registered local/vehicle metric, optimized baselines, uncertainty and matched adaptation where relevant |
| Broader technology-discovery candidate? | Prior-art/literature comparison plus independent validation; distinguish corpus novelty from external novelty |

Graph non-isomorphism is a diversity descriptor, not a mandatory condition for every discovery: changed continuous geometry or material distribution may change function while the connection graph remains the same. Conversely, a different graph does not prove a different useful mechanism. Keep separate labels for software fixture, exploratory simulation, admitted simulation, independently corroborated simulation and physical validation. A real-world validated technology claim requires corresponding physical evidence.

## 13. Revised implementation boundary for Works 098–101

| Work | Required deliverable | Exit gate and explicit limit |
| --- | --- | --- |
| 098 — Whole-Vehicle Discovery State, Evidence and Fairness Contract | Versioned schemas/validators, orthogonal states, evidence identity and applicability, exploratory/promotion separation, append-only ledger/replay, budget/scheduling/audit rules, registration validator and minimal legacy adapters | Mixed-ledger decision replay; tamper/invalid-promotion rejection; budget/resume correctness; registration completeness; evidence classes cannot masquerade as physical survivors. Software contract only. |
| 099 — Executable Morphology, Architecture and Archive Search | Numerical geometry execution, part/interface split/merge, typed ancestry, optional registered controller genes, bounded feasible/failed/unresolved archives | Repeated seeds produce executed changes with measured geometry and reproducible lineage; demonstrate changing decomposition and useful descriptor measurement. No claim of useful new physics from geometry alone. |
| 100 — Functional and Coupled Discovery Trials | Bounded geometry-derived local/assembly solvers, task-derived loads, registered isolated and coupled contrasts, proxy audits and vehicle feedback at a declared fidelity | At least one previously undeclared functional candidate or coupled assembly passes `candidate_survivor` gates, with causal evidence and ledger integrity. If none survives, record a negative/partial outcome; do not weaken gates. No requirement that every component wins in isolation or has a non-isomorphic graph. |
| 101 — Whole-Vehicle Co-Design and Evidence Promotion | Iterative architecture/geometry/controller integration, coupled transient evaluation, full accounting, holdouts, independent stronger evidence and optimized vehicle baselines | A complete candidate finishes the registered task and passes all vehicle promotion gates. Performance superiority and technology novelty require their separate registered evidence. Simulation remains simulation until physically validated. |

Exploratory integration starts in Work 100 at a bounded declared scope; it does not wait for Work 101. Work 101 is a program-level milestone, not a promise that arbitrary full-vehicle discovery fits into one implementation task. Split large implementations into new bilingual numbered work items with explicit dependencies, validations and commits. Do not treat completion of this document as completion of Work 098.

## 14. Required acceptance cases before admitted execution

Work 098 must implement tests demonstrating all of the following, using clearly labeled fixtures:

1. Every original roadmap state is distinguishable, with simultaneous physics/manufacturing states and per-fidelity uncertainty retained.
2. Never-invoked physics, timeout, divergence, unsupported domain, physical failure and corrupt provenance cannot be conflated.
3. Exploratory assembly accepts declared incomplete evidence only within its permitted scope; promotion rejects missing mandatory evidence, even if proxy quality is excellent.
4. Changed geometry/material/controller/boundary/evaluator identities cannot reuse inapplicable evidence or fake a survivor.
5. A new descendant may learn from failure; its parent and original criteria remain immutable.
6. Interruption/resume, retry, duplicate results, cache reuse and budget exhaustion cannot create free work, double settlement or hidden deletion; spent external work with lost output is recorded by the registered recovery rule.
7. Decision replay reproduces selection and accounting; execution replay reports its numerical tolerance and timing limitations separately.
8. Audit selection ignores score within its registered strata, retains inclusion probabilities and handles unknown reference labels without manufacturing a false-negative rate.
9. An incomplete or altered registration cannot begin or continue an admitted run under its old identity; software promotion fixtures cannot enter scientific result counts.
10. Existing benchmark behavior remains regression-tested. Legacy `accepted`, `intact`, `passed` or `invalid` labels are interpreted from their evidence scope; they are not automatically mapped to physical feasibility or failure.

Passing these cases establishes contract readiness. Actual discovery requires the later experiments and evidence above.

## 15. Non-goals and enduring constraints

This protocol does not guarantee discovery, permit infinite search or magic materials, weaken conservation/safety, or require immediate implementation of every physics domain. It does not prescribe a conventional car as the only valid outcome. Manufacturing may be annotated early when cheap, but only declared promotion requirements make it exclusionary for claims. Unresolved research hypotheses may persist under bounded budgets without being advertised as functioning technology.

The intended outcome is a traceable learning loop in which whole-vehicle needs and component mechanisms can reshape one another, while every promoted claim remains tied to the physics, resources and evidence actually demonstrated.
