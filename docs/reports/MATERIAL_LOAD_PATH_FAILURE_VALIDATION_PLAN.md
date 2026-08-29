# Material Load-Path and Failure Validation Plan

Thai companion: `MATERIAL_LOAD_PATH_FAILURE_VALIDATION_PLAN.th.md`

Report date: 2026-08-29

Status: Planned, not implemented or experimentally executed

## Executive Decision

Formula Ultimate must validate force and torque transmission through geometry
and material before structural fitness or whole-vehicle geometry search begins.
The next research phase will use six evidence families:

1. axial tension;
2. beam bending;
3. shaft torsion;
4. column buckling;
5. loaded-interface plate load transfer; and
6. deterministic structural-failure coupling to subsystem failure or `DNF`.

The design agent may make material arbitrarily thin or unfamiliar in form. The
evaluator must not replace physics with a human-preferred minimum thickness.
A thin candidate may yield, deform, buckle, fracture, accumulate fatigue, fail
its function, or become numerically unresolved. These outcomes must remain
distinct and observable.

This report supersedes the Work 032 planning language that treated minimum
feature or thickness rules as general feasibility constraints. Such limits may
exist only as declared CAD/solver resolution boundaries or as optional,
separately labelled manufacturing treatments—not as hidden physical laws.

## 1. Claim Boundary

Passing this planned suite would support only that the implemented structural
route reproduces selected analytical and numerical reference cases within
declared ranges. It would not prove:

- that arbitrary vehicle geometry is structurally safe;
- that material data represents a real purchased batch;
- that fracture, fatigue, joints, composites, impact, or post-buckling behavior
  is generally accurate;
- that one solver is independent validation of itself; or
- that a component is manufacturable, certified, or race-ready.

The evidence ladder is:

```text
equation/unit contract
  -> analytical reference
  -> mesh and boundary-condition verification
  -> solver-to-reference agreement
  -> loaded 3D interface evidence
  -> coupled failure event and replay
  -> independent solver/model promotion
  -> physical coupon/component testing
```

No lower rung may be renamed as a higher one.

## 2. Verified Local Tool Inventory

Read-only probes on 2026-08-29 found:

| Tool | Observed evidence | Boundary |
|---|---|---|
| FreeCAD | `1.1.3`; bundled Python imported `FreeCAD`, `Part`, and `Fem` | Import success only; no FEM solve executed |
| CalculiX | `ccx.exe` reported `2.22` | `-v` returned exit code `201`; runtime/artifact behavior is not accepted yet |
| Gmsh | version probe reported `4.15.0` | observed invocation returned exit code `201`; meshing is not accepted yet |
| CadQuery/STEP | previously verified deterministic geometry and STEP route | structural boundary conditions and mesh tags are not implemented |

Future launchers must verify all of the following:

- exact executable and version identity;
- input-deck and mesh hashes;
- expected output files newer than the run start;
- parsed solver completion/status markers;
- requested step/increment coverage;
- finite reaction/displacement/stress/energy fields;
- explicit non-convergence and fatal-message detection; and
- process exit behavior for the exact command mode.

Exit code `0` alone cannot prove evidence, and the observed version-command exit
code `201` alone cannot be treated as a physics failure.

## 3. Physics and Material Boundary

### 3.1 Initial material law

Begin with small-strain, homogeneous, isotropic, linear elasticity:

```text
sigma = C(E, nu) : epsilon
```

Each material record must declare:

- density `rho` in `kg/m^3`;
- Young's modulus `E` in `Pa`;
- Poisson ratio `nu`;
- shear modulus `G`, either declared or derived consistently;
- yield policy and source/uncertainty;
- valid temperature and strain-rate range;
- provenance, revision, and claim level.

The first linear suite uses yield only as an observable screening threshold; it
does not pretend to calculate plastic redistribution. Elastoplastic validation
must be a later, separately tested material-law phase before plastic reserve is
credited.

### 3.2 Failure-law staging

- **Yield:** first crossing of the declared yield criterion is reported. A
  linear run beyond yield is outside its constitutive validity.
- **Plastic collapse:** requires an implemented and independently verified
  elastoplastic law; it cannot be inferred by continuing a linear solution.
- **Fracture:** exceeding an ultimate value is a screening failure, not a crack
  path prediction. Crack initiation/growth requires a calibrated damage or
  fracture-mechanics model.
- **Fatigue:** initial screening may use a versioned S-N curve and cumulative
  damage rule with uncertainty, but must not be called general fatigue
  validation. Load history and cycle counting remain evidence.
- **Buckling:** eigenvalue buckling identifies an idealized elastic instability
  mode/load factor. Physical capacity requires imperfection sensitivity and
  nonlinear post-buckling analysis.

### 3.3 Thin geometry policy

There is no arbitrary physical minimum thickness. A candidate may be as thin
as it chooses while remaining a valid finite 3D solid. The evaluator returns
one of these distinct states:

- `physically_admissible` — all declared laws and functional gates pass;
- `yielded`, `buckled`, `fractured`, `fatigue_failed`, or another declared
  physical failure;
- `numerically_unresolved` — mesh/solver cannot resolve the geometry within the
  common resource budget;
- `invalid_geometry` — no valid finite solid/interface exists;
- `unsupported_physics` — required material/joint/load behavior is outside the
  implemented model.

`numerically_unresolved` is not silently converted to either survival or
failure. It consumes an evaluation budget and blocks promotion.

## 4. Common Experiment Contract

Every specimen run must pin:

- `protocol_id`, `experiment_id`, `specimen_id`, and geometry hash;
- material-law ID and complete property provenance;
- load-case and boundary-condition IDs;
- coordinate frame, units, load surfaces, support surfaces, and reference
  points;
- mesher/solver/adapters and exact versions/source hashes;
- element family/order, mesh sizes, quality metrics, and degrees of freedom;
- nonlinear/eigenvalue/static step controls as applicable;
- tolerances and common resource budget;
- analytical reference implementation/hash;
- random seed when imperfections or sampling are used;
- result/failure status and claim level.

### Required common outputs

- nodal displacement and reaction evidence;
- strain/stress fields and named gauge values;
- total reaction force and moment about a declared origin;
- strain energy and external work where available;
- mass/volume and dimensional identity;
- mesh count/quality, solver iterations, residual/status, and wall time;
- analytical and mesh-sequence residuals;
- singular/excluded regions and averaging/extrapolation policy;
- exact artifacts and hashes.

### Common equilibrium gates

For applied force `F_app`, applied moment `M_app`, reactions `R_i` at positions
`r_i`, and declared origin `O`:

```text
force residual  = F_app + sum(R_i)
moment residual = M_app + sum((r_i - O) cross R_i) + sum(M_reaction_i)
```

Residuals remain observable even when within tolerance. No solver result is
admitted if the required reactions or load identities are absent.

### Common energy gate

For a linear static ramp from zero load:

```text
external work ~= strain energy ~= 0.5 * generalized_load * generalized_displacement
```

Energy agreement is a consistency check, not an independent material theory.

## 5. Numerical Verification Policy

Each canonical specimen uses at least three predeclared mesh levels. The final
implementation must freeze actual mesh sizes after a pilot, before comparison
results are read.

Recommended initial numerical gates:

- relative force/moment closure `<= 1e-6` where solver precision supports it;
- analytical displacement/twist/strain-energy error `<= 1%` in the linear
  reference range;
- analytical non-singular stress-gauge error `<= 2%`;
- relative change between the last two admitted meshes `<= 1%` for global
  displacement/strain energy and `<= 2%` for named non-singular stress gauges;
- all values finite, expected output steps complete, and solver converged.

These percentages are proposed numerical evidence thresholds, not physical
thickness rules. Pilot evidence may justify changing them only before the main
campaign and in a new plan.

Peak stress at an ideal fixed edge or point load is not a convergence metric.
Loads should be distributed over finite surfaces, and stress gauges must be
predeclared away from known singular boundaries. Both structured canonical
meshes and the intended Gmsh unstructured route should be tested so an element
or mesher artifact cannot masquerade as material behavior.

## 6. Experiment A — Axial Tension Specimen

### Preferred hypothesis

Within the small-strain elastic range, the solver reproduces axial
displacement, strain, stress, reactions, and strain energy of a prismatic bar.

### Geometry and boundary conditions

- prismatic bar with declared `L` and cross-section `A`;
- one end constrained only as required to remove rigid-body motion;
- uniform traction on the opposite end with resultant `F`;
- finite load surface; no point force;
- named mid-span gauge region away from end effects.

### Analytical references

```text
sigma = F / A
epsilon = sigma / E
delta = F * L / (A * E)
U = F * delta / 2
```

### Independent variables

- load magnitude inside and approaching the declared elastic-validity range;
- mesh level;
- aspect ratio in a predeclared range;
- optional material-property fixture.

### Dependent variables

- end displacement, gauge strain/stress, reaction force, strain energy;
- analytical residuals, mesh sensitivity, and solver status;
- first yield-screen crossing.

### Falsification cases

- reverse the load and require signed symmetry;
- double `F` and require doubled elastic displacement/stress;
- double `E` and require half displacement with unchanged axial stress;
- deliberately omit a restraint and require rigid-body/singularity failure;
- exceed linear-law validity and require `outside_constitutive_validity`, not a
  false elastic pass.

## 7. Experiment B — Beam Bending Specimen

### Preferred hypothesis

A slender cantilever with a finite end traction reproduces Euler-Bernoulli
reference displacement and bending stress in its declared slender/small-
deflection range.

### Analytical references for rectangular section

For width `b`, bending depth `h`, length `L`, end resultant `P`, and
`I = b*h^3/12`:

```text
tip deflection = P * L^3 / (3 * E * I)
root moment = P * L
nominal outer-fibre stress = P * L * (h/2) / I
U = P * tip_deflection / 2
```

### Controls and measurements

- finite traction patch at the free end;
- displacement and stress gauges away from the ideal clamp singularity;
- declared beam slenderness where the reference is applicable;
- consistent load resultant and moment.

### Falsification cases

- reverse `P` and require displacement/stress sign reversal;
- double `P` in the linear range and require linear response;
- vary `h` and test the predicted `I` scaling;
- compare overly short/deep beams and require the Euler-Bernoulli claim to be
  marked out of range rather than forced to pass;
- perturb clamp representation and report boundary sensitivity.

## 8. Experiment C — Solid Circular Shaft Torsion

### Preferred hypothesis

Applied torque propagates through the shaft and produces the correct reaction
torque, shear-stress distribution, twist angle, and strain energy in the linear
elastic range.

### Analytical references

For radius `R`, length `L`, torque `T`, shear modulus `G`, and
`J = pi*R^4/2`:

```text
tau(r) = T * r / J
tau_max = T * R / J
theta = T * L / (J * G)
U = T * theta / 2
```

### Boundary conditions

- one end constrained against rigid rotation while avoiding unnecessary local
  over-constraint;
- distributed tangential traction or kinematic coupling on the opposite face
  with exact resultant `T`;
- named radial shear-stress gauges away from end effects.

### Falsification cases

- reverse `T` and require shear/twist sign reversal;
- double `T` and require linear response;
- vary `R` and test the `R^4` twist sensitivity;
- change `G` and require inverse twist scaling;
- apply a force pair with the same moment and compare away from load-introduction
  regions;
- remove rotational restraint and require solver invalidity.

Passing this specimen proves only continuum shaft torsion for the declared law;
it does not yet prove gear teeth, splines, bearings, joints, wheel inertia, or a
complete drivetrain.

## 9. Experiment D — Column Buckling

### Preferred hypothesis

An ideal slender column eigenvalue analysis reproduces the Euler critical load
and mode family within the declared slenderness and support model.

### Analytical reference

```text
P_cr = pi^2 * E * I / (K * L)^2
```

The first canonical case uses a declared pinned-pinned representation with
`K = 1`. Other support conditions are separate fixtures, not hidden changes.

### Required evidence

- pre-stress/load identity;
- eigenvalue/load factor and normalized mode shape;
- reaction closure in the pre-buckling state;
- mesh convergence of the lowest relevant eigenvalue;
- support and imperfection sensitivity.

### Falsification and limitation cases

- change `L`, `E`, or `I` and test analytical scaling;
- compare support models and require the correct declared `K` case;
- introduce a small predeclared imperfection and run a later nonlinear study;
- never use an ideal eigenvalue alone as allowable physical load;
- classify local element/constraint modes separately from the intended global
  column mode.

## 10. Experiment E — Loaded Interface Plate

### Purpose

Verify that loads applied at declared component interfaces cross an arbitrary
admitted 3D solid and close force, moment, deformation, stress, and energy
evidence. This is the bridge from canonical specimens to agent geometry.

### Interface definition

- exact tagged support and load-bearing surfaces preserved from source geometry
  through STEP and mesh;
- finite bearing/contact traction distributions rather than point loads;
- declared load origin and coordinate frame;
- central keep-out and outer envelope only when required by the component task;
- no arbitrary minimum thickness or conventional web shape.

### Preferred hypothesis

For the reference plate, all applied force/moment resultants are recovered at
the declared supports, global displacement and strain energy converge, and
stress/deformation/failure fields respond consistently to load and material
changes.

### Independent variables

- load direction and magnitude;
- geometry candidate;
- material-law record;
- mesh level and local refinement policy;
- boundary-condition fixture variants.

### Dependent variables

- reaction force/moment closure;
- load-path stress/strain fields and named gauges;
- displacement, strain energy, mass, and stiffness-to-mass evidence;
- yield/buckling/failure indicators;
- mesh/boundary sensitivity and solver status.

### Falsification cases

- disconnect the load path and require invalid/disconnected or failed evidence;
- make a ligament progressively thinner and allow physics/numerics—not a fixed
  thickness rule—to determine the outcome;
- reverse and permute loads while checking signed reactions;
- shift load introduction over equivalent finite regions and quantify
  sensitivity;
- compare reaction and energy closure before trusting local stress;
- promote selected cases to an independent solver/model route.

No single analytical stress formula is expected for arbitrary plate geometry.
Admission therefore requires canonical-solver verification first, plus mesh,
equilibrium, energy, boundary, and independent-promotion evidence.

## 11. Experiment F — Failure Coupling to the Vehicle

### Component connection state

Each load-carrying connection has explicit state:

```text
intact -> degraded -> failed
```

The transition must identify:

- component and connection IDs;
- governing failure law and evidence record;
- load history and event time;
- capacity before/after the event;
- force/moment path removed or changed;
- stored elastic energy and the release/dissipation policy;
- downstream signals and terminal outcome;
- replay fingerprint.

### First implementation policy

The safest first coupling terminates the race at the localized first
load-path-critical structural failure and reports `DNF`. It does not simulate
post-break debris or redistribute loads without a validated transient failure
model. This prevents force and stored energy from disappearing through an
unmodelled connection removal.

Later redundant systems may continue only after explicitly implementing:

- connection removal and load redistribution;
- released elastic energy partition into kinetic, fracture, heat, and other
  declared sinks;
- transient dynamics and new contact/collision states;
- cascading structural and subsystem failures.

### Coupling tests

1. Below-threshold fixture remains intact and replays exactly.
2. Known threshold crossing localizes the failure time within declared
   tolerance.
3. A critical connection failure produces `DNF` and no later race progress.
4. A non-critical/degraded fixture changes capacity only as declared.
5. Missing structural evidence blocks the step; it never implies survival.
6. Tied structural/energy/thermal/finish events use a declared deterministic
   arbitration priority.
7. Injected stale hashes, wrong connection IDs, and hidden energy release are
   rejected with zero committed state.

## 12. Experiment Matrix and Order

| Phase | Specimens | Model level | Promotion gate |
|---:|---|---|---|
| 0 | unit/equation fixtures | pure Python analytical references | equations, units, signs, invalid inputs pass |
| 1 | tension, bending, torsion | linear elastic CalculiX route | analytical, equilibrium, energy, mesh gates pass |
| 2 | buckling | eigenvalue then nonlinear imperfection study | mode/eigenvalue/refinement and scope limits pass |
| 3 | loaded interface plate | arbitrary admitted solid, linear range first | tags, load path, equilibrium, energy, mesh/boundary gates pass |
| 4 | material nonlinearity/failure | separately verified plastic/damage/fatigue models | dedicated references and provenance pass |
| 5 | failure coupling | coupled Level-0 event | rollback, localization, DNF, conservation, replay pass |
| 6 | independent promotion | second solver/model and physical coupons later | ordering and failure classification survive |

Do not implement Phase 5 from unverified Phase 1–4 outputs.

## 13. Implementation Roadmap

Each milestone must be a separate bilingual, validated, committed work item.

### Milestone 1 — Solver acceptance harness

- pin and probe FreeCAD, Gmsh, and CalculiX invocation behavior;
- create bounded artifact directories and fail-closed parsers;
- reject stale/missing/incomplete output even when a process appears successful;
- record tool/config/source/input/output hashes and resource use.

### Milestone 2 — Material and load-case contracts

- implement typed SI material, geometry-interface, boundary-condition, mesh,
  solver, and structural-result schemas;
- preserve property provenance, validity range, uncertainty, and unsupported
  behavior;
- add malformed/non-finite/unknown-field tests.

### Milestone 3 — Linear canonical specimens

- implement analytical references and CAD/mesh/solver adapters for tension,
  bending, and torsion;
- run mesh sequences and boundary-condition audits;
- preserve all failed attempts and solver evidence.

### Milestone 4 — Buckling verification

- add Euler fixtures, mode classification, mesh refinement, and support
  sensitivity;
- add nonlinear imperfect-column work separately before using buckling capacity
  in fitness.

### Milestone 5 — Loaded-interface plate

- add persistent interface tags from geometry to mesh;
- run reference and deliberately broken/thin load paths;
- audit reactions, moments, strain energy, stress gauges, mesh/boundary
  sensitivity, and independent promotion.

### Milestone 6 — Nonlinear material and fatigue staging

- validate elastoplastic response before crediting post-yield capacity;
- define fracture screening versus fracture prediction explicitly;
- add versioned fatigue histories/S-N evidence and uncertainty before fatigue
  influences fitness.

### Milestone 7 — Failure coupling

- translate admitted structural failure evidence into typed connection events;
- terminate at critical first failure initially;
- test event arbitration, rollback, energy policy, `DNF`, and replay.

### Milestone 8 — Search release gate

- allow `DesignSearchAgentV0` to consume structural fitness only after all
  required specimen/replay/promotion gates pass;
- keep unresolved and failed candidates in the budget ledger;
- require stronger independent review before any discovery claim.

## 14. Required Falsification Review

Every milestone result must record:

- supporting evidence;
- contradicting evidence;
- alternative explanations;
- missing evidence;
- confidence and exact claim level.

Preferred hypotheses must be challenged by sign/scaling tests, deliberate
missing constraints, disconnected geometry, mesh/order changes, boundary
variants, solver disagreement, stale artifacts, non-convergence, and failure-
event inconsistencies.

## 15. Immediate Next Work

Implement **Milestone 1: Solver Acceptance Harness** first. The installed tools
exist, but no structural solve has been accepted. The first implementation
should generate a disposable, analytically trivial tension specimen and prove
the exact Gmsh/CalculiX/FreeCAD process and artifact contract before building
the full specimen suite.
