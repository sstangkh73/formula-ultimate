# Geometric Design Diversity Roadmap V1

Thai companion: `GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.th.md`

## Purpose

Formula Ultimate needs more than rounded corners. The target is a search system that can invent unfamiliar **functional topology**, express it as valid parametric B-rep geometry, evaluate it with geometry-derived physics, and retain it only when it survives the same evidence gates as conventional-looking candidates.

An unusual appearance is not discovery. A candidate is potentially novel only when its topology or load/energy/motion path differs measurably from the comparison archive, its function is causal, it has no hidden geometry repair, it replays exactly, and it survives fair physical evaluation.

## Current boundary

The installed CadQuery `2.8.0` API exposes spline, arc, sweep, loft, fillet, and chamfer operations, so the CAD kernel is not the main source of angularity. The repository creates the bias at three narrower layers:

1. The functional vehicle grammar admits only boxes and axis-aligned cylinders.
2. B-rep Grammar V1 starts from rectangle, circle, annulus, or shaft-section profiles; it has no general wire, spline-control-point, 3D-path, sweep, or loft declaration.
3. `DesignSearchAgentV0` changes five scalar scale factors on a fixed component graph. Work 083, 084, and 087 use separately hand-authored procedural builders dominated by boxes and cylinders rather than the agent-facing feature grammar.

The present system therefore has real inspectable parts but not free-topology generative design.

## Non-negotiable definition of useful diversity

A design-diversity claim requires all of the following:

- **Representational reach:** the grammar can encode curved, tapered, branching, hollow, ribbed, shell-like, and hybrid solids without importing opaque meshes.
- **Topological reach:** mutations can add, remove, split, merge, branch, and reconnect parts/features/interfaces instead of only resizing them.
- **Functional closure:** required force, torque, motion, thermal, fluid, electrical, and control terminals are connected causally.
- **Physical consequence:** geometry determines mass, centre of mass, inertia, clearance, section properties, mesh, stress, deformation, heat/flow quantities, and failure.
- **Manufacturing consequence:** process constraints affect admissibility; they are not decorative metadata.
- **Search diversity:** the archive preserves different feasible niches rather than converging immediately to one easy primitive family.
- **Evidence discipline:** exact replay, immutable source identities, numerical failures, and missing evidence remain visible.

No work may reward novelty alone, prescribe a conventional car layout, or count a visually unusual but physically unevaluable shape as discovery.

## Sequence overview

| Batch | Works | Capability gained |
|---|---|---|
| 1 | 090–091 | Measure existing bias; declare arbitrary constrained 2D profiles |
| 2 | 092–093 | Build free-form solids; encode mutable part/feature/interface topology |
| 3 | 094–095 | Mutate topology reproducibly; enforce validity and manufacturing without hidden repair |
| 4 | 096–097 | Recover semantics from arbitrary geometry; mesh and physically evaluate it |
| 5 | 098–099 | Allocate compute fairly; search for quality and diversity together |
| 6 | 100–101 | Run subsystem discovery trials; integrate and promote only surviving candidates |

The first defensible opportunity to see a genuinely unfamiliar functional part is after Work 097, with actual discovery trials in Work 100. Curved parts may appear after Work 092, but they are not yet evidence-backed discoveries.

## Work 090 — Search-Space Bias and Diversity Contract

### Objective

Measure the current primitive/topology bias before expanding the grammar, and freeze metrics that cannot be changed after results are observed.

### Deliverables

- `design_diversity_v1` descriptor and distance contract.
- A deterministic census of current reference candidates and a bounded generated sample.
- Canonical topology signatures invariant to global translation, rotation, part naming, and uniform scale.
- Baseline reports for primitive fraction, profile/operator entropy, curvature distribution, part/interface graph diversity, phenotype duplication, load-path diversity, failure-mode diversity, and invalid-candidate causes.

### Required metrics

- `unique_topology_signatures / attempted_candidates`
- `unique_geometry_signatures / valid_candidates`
- duplicate phenotype rate
- Shannon entropy of feature operators and interface types
- curved-surface-area fraction and curvature-spectrum histogram
- graph-edit distance over typed part/interface graphs
- load/energy/motion path signature distance
- feasible archive coverage and failure-mode coverage

### Falsification and success gate

The metric suite must classify translations, rotations, renaming, and uniform rescaling as non-novel controls while detecting a branch addition, path reroute, profile-family change, and interface-topology change. Success does not prove the search can create diversity; it only makes bias measurable.

## Work 091 — Constrained Free-Form Sketch and Wire Grammar V2

### Objective

Replace the four-profile bottleneck with a typed, bounded, replayable 2D profile language.

### Operators

- line segment, tangent arc, three-point arc, circle, ellipse
- quadratic/cubic Bezier and degree-bounded B-spline
- polyline and mixed-segment closed wire
- multiple loops for holes/islands
- mirror, rotate, translate, offset, trim, and bounded constraint solve
- dimensional, coincident, tangent, concentric, parallel, perpendicular, and symmetry constraints

### Safety boundary

Every wire declares local coordinates, units, control-point bounds, degree, knot/weight policy, closure tolerance, minimum radius, and provenance. Reject open loops, self-intersections, duplicate edges, zero-length segments, sub-tolerance features, invalid hole nesting, and non-deterministic constraint solutions.

### Success gate

A corpus of at least twelve profiles from at least six profile families must export identical canonical wire identities across two runs. Metamorphic tests must preserve identity under declaration-key reordering and change it under geometry mutation. This proves profile expressivity, not solid validity or physical usefulness.

## Work 092 — Free-Form B-rep Solid Grammar V2

### Objective

Turn Work 091 wires and bounded 3D paths into valid single- and multi-feature solids without opaque mesh substitution.

### Operators

- extrude/revolve with arbitrary local axes
- straight and curved sweep/pipe along a declared 3D path
- multi-section loft with correspondence/orientation controls
- taper/draft, shell, variable section, rib/web, gusset, pocket, bore, and local pattern
- bounded fillet/chamfer selected by geometry signature rather than unstable edge number
- boolean union/subtract/intersect and explicit multi-body output when the part contract permits it
- deterministic local transforms and datum creation

### Success gate

At least ten non-primitive solids—including curved branch, tapered hollow duct, lofted rotary member, organic-like load bridge, and variable-section shell—must be valid in CadQuery and FreeCAD, retain semantic datums through STEP, and replay to identical geometry identities. A visually curved solid alone does not prove topology mutation.

## Work 093 — Typed Morphology and Topology Genome V1

### Objective

Represent a candidate as a mutable typed graph rather than a fixed list of preselected components.

### Genome layers

1. Functional terminals and required domains.
2. Part graph and parent/child containment.
3. Interface and joint graph with allowed DOF.
4. Per-part feature DAG and material/process declaration.
5. Load, energy, motion, fluid, thermal, and control paths.
6. Symmetry as an optional gene, never a mandatory vehicle prior.

### Topology operations

Add/remove a part, split/merge a part, add/remove a branch, reroute a typed path, replace a solid family, add/remove a rib or shell, change section family, add/remove an interface, and change joint type within functional-domain rules.

### Success gate

The generator must produce valid genomes with different part counts and non-isomorphic typed graphs that cannot be reached through the old five scalar variables. Every functional terminal remains traceable or the candidate is rejected before CAD. This proves topology representation, not that CAD or physics can execute every genome.

## Work 094 — Reproducible Topology Mutation and Recombination

### Objective

Let agents explore Work 093 without hand-authored candidate geometry.

### Mutation families

- parametric perturbation
- feature insertion/removal/reordering where dependencies permit
- branch growth/pruning
- part split/fusion
- interface creation/deletion/rerouting
- material/process mutation within evidence class
- optional graph crossover restricted to compatible typed boundaries

Each proposal records parent identities, random seed/checkpoint, selected operator, proposal probabilities, bounded retries, and final genotype identity. Primitive, skeletal, shell, rotary, branching, and hybrid initializers receive declared, balanced opportunity budgets.

### Success gate

Given the same parent, seed, and operator budget, proposal sequences must replay exactly. Negative controls must reject cycles, disconnected mandatory terminals, impossible joint domains, invalid material/process combinations, and mutation after result observation. At least four topology-changing operator families must produce executable genomes in a bounded pilot.

## Work 095 — Constructive Validity and Manufacturing Gate

### Objective

Prevent complex geometry from becoming an exploit or a stream of unusable CAD failures.

### Rules

- Prefer grammar-preserving construction over post-hoc repair.
- A deterministic repair may occur only before evaluation, within a preregistered operation list and budget, and must become part of genotype/provenance identity.
- Never change geometry after observing performance, collision, stress, or failure results.
- Record each rejected or repaired proposal and the exact cause.
- Apply declared process-specific limits: minimum wall/ligament/radius, tool access, overhang/support, enclosed void, tolerance, joining access, and material/process compatibility.

### Success gate

Injected self-intersection, sliver, zero-thickness, inaccessible feature, unsupported wall, and hidden-repair controls must fail visibly. Validity yield and rejection causes must be reported by representation family so primitive candidates do not receive an invisible advantage.

## Work 096 — Semantic Geometry Witness V3

### Objective

Recover physics-relevant semantics from arbitrary curved and branching STEP geometry without depending on unstable face numbers.

### Required measurements

- solid/shell/body count, volume, mass, centre of mass, full inertia
- oriented bounds, curvature classes/spectra, thickness field, minimum radius, section properties along paths
- datum axes/planes/points and signature-based interface surfaces
- load/support/contact/thermal/fluid regions
- path length, bend radius, cross-sectional evolution, clearances, interference, swept motion envelope
- semantic correspondence between declared and independently inspected geometry

### Success gate

FreeCAD must independently recover all mandatory semantics for the Work 092 corpus after STEP export. Face-order permutation and harmless export changes must preserve semantic matches; altered interfaces or missing regions must fail closed. This proves inspection, not structural validity.

## Work 097 — Generalized Meshing, Contact, and Failure Evaluation

### Objective

Make unfamiliar geometry evaluable rather than selecting primitives merely because the solver understands them.

### Capability

- automatic solid/shell/beam model choice with declared justification
- curvature-, thickness-, interface-, and stress-gradient-aware meshing
- arbitrary signature-selected load/support/contact regions
- bonded, sliding, bearing, preload, and declared friction/contact laws
- bending, torsion, buckling, yield/plasticity, fracture-domain, fatigue, thermal stress, and solver-invalid states
- geometry-family-aware mesh convergence and independent equilibrium/energy residuals
- failure propagation back into the typed connection graph

### Benchmarks and success gate

Use analytical and cross-solver benchmarks for curved cantilever, tapered beam, hollow shell, branched joint, lattice/rib junction, bearing seat, and contact pair. Each admitted benchmark must pass convergence and residual gates; divergence remains an output. Passing these benchmarks does not validate arbitrary future topology or real materials.

## Work 098 — Multi-Fidelity Compute and Fairness Protocol

### Objective

Avoid rewarding boxes simply because they are cheaper to generate, mesh, and solve.

### Evaluation ladder

1. grammar/connectivity/identity checks
2. B-rep validity and coarse collision/manufacturing checks
3. geometry-derived analytical bounds
4. coarse mesh/contact/thermal evaluation
5. refined convergence for survivors
6. holdout and independent higher-fidelity evaluation

Budgets must be reported as attempts, CAD-kernel calls, mesh elements, nonlinear iterations, solver time, and total compute. Representation families receive matched opportunity or explicit cost-normalized budgets. Cheap proxy rejection must be audited for false negatives using a stratified sample promoted regardless of proxy score.

### Success gate

Primitive and free-form families must face the same functional cases and evidence thresholds. The protocol must demonstrate deterministic promotion, fail-fast behavior, and measured proxy false-negative/false-positive rates. Fair compute does not imply equal outcomes.

## Work 099 — Quality-Diversity Search Agent V1

### Objective

Search for high-performing feasible designs across multiple niches instead of collapsing to one easiest shape.

### Method

Implement a deterministic MAP-Elites or equivalent quality-diversity archive. Candidate descriptors combine typed topology, part count, interface graph, curvature spectrum, section variation, load-path branching, mass distribution, motion strategy, heat-rejection strategy, and failure mode. Objective quality is evaluated only among candidates that pass mandatory gates.

Compare equal-budget GRID/RANDOM/scalar EVOLUTION/free-form QD treatments using frozen seeds, operators, cases, and evaluator identities. Novelty must never compensate for failure, undeclared energy, missing evidence, or numerical invalidity.

### Success gate

The QD treatment must improve feasible niche coverage or topology diversity over controls under a preregistered analysis. A pretty outlier, one lucky seed, or diversity consisting only of rescaled duplicates is a failure.

## Work 100 — Isolated Functional Subsystem Discovery Trials

### Objective

Give unusual geometry a tractable place to emerge before whole-vehicle integration.

### Trial domains

- ground interaction and vertical compliance
- torque transfer and speed conversion
- branching load bridge or structural mount
- heat collection/rejection and fluid routing
- energy containment/interface support

Each trial freezes only external functional terminals, loads, envelope, energy/resources, evidence class, evaluator, and compute budget—not known human component shape or arrangement. Use training, holdout, mirror, disconnected-path, weakened-material, blocked-motion, and replay controls.

### Success gate

At least one non-primitive, non-isomorphic candidate must survive CAD/FreeCAD identity, manufacturing, motion/clearance, converged physics, failure controls, and exact replay. It need not beat the optimized baseline yet; survival establishes the first credible unfamiliar functional part. Any performance claim still requires fair optimized-baseline and holdout comparison.

## Work 101 — Free-Topology Integration and Evidence Promotion

### Objective

Integrate surviving subsystem genomes without reverting to a prescribed rectangular frame, then decide whether any complete candidate merits whole-vehicle Level-0 research.

### Required gates

- all parts and interfaces present as exact STEP/FCStd geometry
- no forbidden interference across the full motion/thermal/service envelope
- causal force, torque, energy, control, fluid, and heat paths
- geometry-derived mass/COM/inertia and full structural/thermal ledgers
- integrated mesh/contact convergence and failure propagation to DNF
- static, acceleration, braking, cornering, combined, bump, torque, duration, single-failure, mirror, and replay cases
- equal-budget optimized fixed-topology and free-topology comparisons
- holdout plus independent higher-fidelity review before any discovery claim

### Success gate

Only a candidate passing every admission gate may enter whole-vehicle Level 0. A novel candidate is a discovery candidate only if it then outperforms fair optimized baselines and survives higher-fidelity challenge. It remains not physically validated without real material/process evidence and physical testing.

## Artifact architecture

Future implementations should separate four identities:

1. `genotype_sha256`: typed topology and feature declaration.
2. `geometry_sha256`: canonical STEP/FCStd witness.
3. `evaluation_sha256`: frozen evaluator, cases, materials, mesh, solver, and outputs.
4. `lineage_sha256`: parents, seed/checkpoint, mutation trace, repair trace, and archive insertion.

Any mismatch fails closed. Cached results may be reused only when all four relevant identities match.

## Decision rules

- Curved but topologically identical: **shape variation**, not topology discovery.
- Different graph but broken functional path: **invalid proposal**, not novelty.
- Valid and unusual but only analytically evaluated: **promising candidate**, not admitted.
- Passes converged component physics: **subsystem survivor**, not whole vehicle.
- Passes integrated Level 0: **whole-candidate research admission**, not physical validation.
- Beats fair baselines and survives independent higher fidelity: **discovery candidate**, still bounded by evidence class.

## Principal risks and mitigations

| Risk | Required mitigation |
|---|---|
| Curves are added but search still changes only scales | Work 093–094 must mutate typed topology and feature DAGs |
| Novelty reward produces useless sculptures | Mandatory functional gates precede quality/novelty ranking |
| Free-form CAD fails more often and loses unfairly | Work 095 rejection accounting and Work 098 matched compute |
| Hidden repair leaks result information | Preregistered pre-evaluation repair only; repair trace enters identity |
| Semantic face references break after STEP | Signature/datums and independent Work 096 recovery |
| Solver supports only easy primitives | Work 097 benchmark coverage before discovery trials |
| One exotic candidate is overclaimed | Multiple seeds, optimized baselines, holdout, higher fidelity, evidence boundaries |
| Complexity explodes | Bounded graph/feature budgets expanded only after validity and solver audits |

## Recommended execution cadence

Execute two works per batch and commit each independently: `090–091`, `092–093`, `094–095`, `096–097`, `098–099`, then `100–101`. Do not start Work 100 until Work 097 can evaluate non-primitive benchmark geometry, and do not start whole-vehicle integration until a subsystem survivor exists.
