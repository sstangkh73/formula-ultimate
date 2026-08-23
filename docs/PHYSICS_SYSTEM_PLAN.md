# Physics System Plan

## 1. Purpose

The physics system is a staged evidence engine for evaluating candidate vehicle
graphs. Its first responsibility is fast, deterministic rejection and ranking
of one-dimensional powertrain candidates. It is not a substitute for detailed
vehicle validation.

## 2. Core Principles

1. **Conservation before performance:** energy and force balance failures
   invalidate a run before fitness is considered.
2. **Explicit assumptions:** every approximation has a fidelity level and a
   documented validity range.
3. **Typed interfaces:** component connections carry physical domains and SI
   quantities, not arbitrary untyped numbers.
4. **Observable failure:** solver divergence, clipping, thermal violation, and
   depleted energy are telemetry events.
5. **Deterministic replay:** identical version, configuration, and seed must
   reproduce the same candidate evaluation within declared tolerance.
6. **Promotion, not proof:** Level 0 selects candidates for stronger tests; it
   never certifies real-world performance or safety.

## 3. Fidelity Ladder

### Level 0: Analytical / 1D

- Longitudinal point-mass vehicle dynamics
- Typed energy-flow component graph
- Quasi-static component maps or bounded analytical models
- Basic tyre traction envelope
- Drag, rolling resistance, and road gradient
- Lumped energy and thermal states
- Deterministic failure and race-completion logic

### Level 1: Reduced Order

- Longitudinal/lateral/yaw vehicle dynamics
- Load transfer and combined tyre forces
- Reduced-order aerodynamics and cooling
- Higher-resolution component transients
- Control-system dynamics and track-following

### Level 2: 3D Candidate

- Generated geometry and packaging
- Collision and clearance checks
- Component placement, inertia, and centre of mass
- Mesh-ready geometry and manufacturability heuristics

#### Agent-designed component geometry

Level 2 is not limited to arranging catalog components. Agents may generate the
actual geometry and internal topology of components, including structures,
cooling paths, housings, rotors, couplings, ducts, and other parts expressible
by the versioned geometry language.

The agent does not get to declare that its own geometry is light, strong, cool,
or efficient. Promotion follows a trusted evaluation boundary:

```text
Functional requirement and interface ports
  -> agent-generated parametric CAD / B-rep / implicit geometry
  -> geometry validity and interface checks
  -> assigned material and manufacturing process
  -> independent mass, volume, inertia, and surface extraction
  -> reduced thermal/flow/structural screening
  -> selected CFD / FEA / detailed electromagnetic or mechanical analysis
  -> uncertainty-aware reduced-order component model
  -> Level-0/Level-1 vehicle and race evaluation
  -> telemetry and failures returned to the next design generation
```

This preserves genuine geometric invention while preventing a generator from
self-reporting impossible properties. A generated component is an immutable,
content-addressed artifact containing source representation, generator version,
seed, materials, interfaces, meshing settings, solver settings, and results.

Geometry promotion gates should include watertightness or valid solid topology,
minimum feature size, bounded envelope, interface alignment, collision,
material assignment, manufacturability assumptions, mesh convergence, solver
convergence, safety factors, and disagreement between surrogate and
authoritative analysis. Novel-looking geometry is not treated as new technology
unless its functional advantage survives these gates and comparison with known
baselines.

### Level 3: High Fidelity

- CFD, FEA, detailed tyre, cooling, and structural analysis
- Independent solver cross-checks
- Uncertainty bounds and model calibration

### Level 4: Digital Race

- Full race, strategy, reliability, traffic, weather, and control co-design
- Multi-event robustness rather than a single best lap

## 4. Level-0 System Boundary

### Inputs

- candidate component graph and parameters;
- vehicle envelope parameters held fixed by the experiment;
- track distance, gradient, and target event definition;
- ambient state;
- resource, safety-proxy, and race constraints;
- deterministic driver/controller policy;
- numerical configuration and seed.

### State Vector

The initial state vector should include at least:

- time and longitudinal position;
- vehicle speed and acceleration;
- per-source stored energy or fuel mass;
- component temperatures;
- component availability/degradation state;
- controller mode and race status;
- cumulative energy-conservation residual.

State is immutable across evaluation steps except through declared solver
updates. Hidden module-level state is forbidden.

### Outputs

- completion/failure status and reason;
- elapsed time and distance;
- energy use by source and recovered energy;
- force/power delivered to each tyre endpoint;
- component operating-point and limit histories;
- temperatures and thermal-limit duration;
- conservation residuals;
- cost, mass, and volume accounting;
- deterministic replay metadata.

## 5. Initial Equations and Contracts

The planned equations define implementation targets, not completed validation.

### Longitudinal balance

```text
m_eff * dv/dt = F_tractive - F_drag - F_roll - m*g*sin(grade)
dx/dt = v
```

`m_eff` must explicitly state whether rotational inertia is reflected into the
vehicle mass or solved per rotating component.

### Aerodynamic drag

```text
F_drag = 0.5 * rho_air * CdA * v_rel^2 * sign(v_rel)
```

Level 0 uses a fixed `CdA`; downforce and aero maps are deferred.

### Rolling resistance

```text
F_roll = Crr * m * g * cos(grade) * sign(v)
```

A zero-speed regularization must prevent artificial launch resistance or
numerical sign chatter.

### Tyre traction gate

```text
abs(F_longitudinal) <= mu_longitudinal * F_normal
```

The first model is a bounded envelope, not a detailed tyre model. Saturated
force and requested force must both be logged so search cannot hide traction
violations.

### Mechanical power

```text
P_rotational = torque * angular_speed
P_translational = force * velocity
```

Each component declares sign convention, efficiency direction, operating
envelope, and the destination of losses.

### Lumped thermal state

```text
C_thermal * dT/dt = P_loss - Q_rejected(T, ambient, operating_state)
```

Temperature clipping is forbidden. A limit produces derating or failure
according to an explicit component policy.

### Energy audit

For each step and full run:

```text
energy_in - energy_out - stored_energy_change - declared_losses = residual
```

Residual tolerance must scale with transferred energy and numerical precision.
A run exceeding tolerance is invalid, not merely lower fitness.

## 6. Component Contract

Every Level-0 component model must declare:

- stable component type and model version;
- typed ports and sign conventions;
- parameters with SI units and valid ranges;
- dynamic state and initialization;
- mass, cost, and volume accounting;
- operating envelope;
- loss and thermal model;
- derating and failure behavior;
- deterministic step/evaluation interface;
- invariant and reference tests;
- fidelity limitations.

Candidate parameters may not override physical limits stored in the catalog.

## 7. Simulation Pipeline

```text
Candidate graph
  -> schema and graph validation
  -> static resource accounting
  -> graph compilation and solver ordering
  -> initial-state validation
  -> controller demand
  -> component-network solve
  -> tyre traction gate
  -> vehicle-state integration
  -> energy and thermal update
  -> invariant/failure checks
  -> telemetry append
  -> finish, fail, or next timestep
  -> independent post-run audit
```

Fitness is calculated only after the independent audit accepts the run.

## 8. Numerical Strategy

- Start with deterministic fixed-step integration for transparent replay.
- Keep solver choice behind an interface so reference integrators can be used.
- Declare absolute/relative tolerances in versioned configuration.
- Reject NaN, infinity, negative mass/energy, time reversal, and non-monotonic
  race distance unless an experiment explicitly supports reverse motion.
- Detect algebraic-loop non-convergence with bounded iterations and a recorded
  failure reason.
- Perform timestep-convergence tests before choosing a production timestep.
- Treat the forward-only zero-speed boundary as a unilateral constraint and
  record its impulse separately from unconstrained road-load force; never hide
  a prevented reverse-motion step as ordinary acceleration.

## 9. Failure Taxonomy

At minimum:

- invalid topology;
- invalid parameter or initial state;
- resource-budget violation;
- solver non-convergence;
- conservation violation;
- energy depletion;
- thermal limit/derating/failure;
- traction saturation;
- component envelope violation;
- timeout or failure to finish;
- numerical invalidity;
- successful completion.

Traction saturation may be a valid operating event; exceeding the model without
the saturation gate is a physics violation. The distinction must be preserved.

## 10. Package Boundaries

- `components`: reusable component physics and catalogs;
- `topology`: graph representation, compilation, mutation, and validity;
- `physics`: domain equations, units, integrators, and invariant checks;
- `simulation`: race loop and fidelity orchestration;
- `telemetry`: schemas, run records, audits, and replay metadata;
- `experiments`: baselines, search comparisons, seeds, and analysis entrypoints.

Search algorithms must not import internal solver state or bypass graph gates.
Physics code must not calculate evolutionary fitness.

## 11. Implementation Milestones

1. Units, quantity naming, schemas, and failure types.
2. Analytical point-mass coast-down and constant-force reference model.
3. Tyre traction gate and road-load models.
4. Minimal electrical source -> motor -> tyre baseline.
5. Telemetry and independent conservation audit.
6. Fixed EV/ICE/hybrid reference topologies.
7. Typed graph validation and compilation.
8. Topology mutation/search with equal-budget experiments.
9. Timestep convergence and Level-0/Level-1 promotion study.
10. Versioned geometry language and trusted 3D property-extraction pipeline.
11. Agent-generated component geometry with multi-fidelity promotion gates.

Each milestone requires its own pre-work plan and post-work result record.
