# Formula Ultimate

[ฉบับภาษาไทย](README.th.md)

Formula Ultimate is a research platform for open-ended autonomous engineering
discovery. Its long-term mission is to let agents design a complete 3D racing
vehicle—from whole-vehicle architecture down to internal component geometry—
without prescribing the conventional layout, dimensions, powertrain, wheel
arrangement, body form, or known component shapes that human racing regulations
historically assume.

> No prescribed conventional vehicle architecture beyond declared physics,
> race, energy, resource, safety, and evidence constraints.

The goal is not merely to generate unusual-looking cars. The research asks
whether agents can discover functionally distinct vehicle architectures or
component technologies that minimize total race time for each race environment,
beat fairly optimized conventional baselines, and retain their advantage when
evaluated at progressively stronger levels of physics fidelity.

## Primary Research Question

Under a versioned Formula One-derived race and energy protocol, where all
primary propulsion energy must be carried before the race and no primary energy
may be replenished during the race, can autonomous agents discover complete 3D
racing-vehicle architectures and component technologies—without prescribing a
conventional vehicle layout—that outperform optimized conventional baselines in
total race time while surviving multi-fidelity physics validation?

For race environment `r`, the primary objective is:

```text
d*_r = arg min_d T_race(d, r)
```

subject to at least:

```text
RaceCompleted(d, r) = true
initial primary energy <= declared race energy budget
external primary-energy addition during the race = 0
conservation residuals <= declared tolerances
complete 3D CAD is valid and physically accounted
structural, thermal, aerodynamic, tyre, material, and numerical gates pass
```

“Fastest” therefore means the lowest total time among candidates that complete
the declared race and pass the required evidence gates. It does not mean peak
speed, a short-lived run before failure, or a numerical exploit.

## Formula One-Derived Race and Energy Contract

Formula Ultimate removes legacy architecture prescriptions, not race discipline
or energy accounting. The current reference is the published 2026 FIA Formula
One rule set:

- Sporting Regulation B5.1.4 prohibits adding or removing fuel after a car has
  left the Pit Lane for its reconnaissance laps until the end-of-session signal.
- Technical Regulation C6.4.4 states that fuel may not be added to or removed
  from a car during a Race.

Official sources: [2026 FIA Section B, Sporting Regulations, Issue
08](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_b_sporting_-_iss_08_-_2026-08-05_7.pdf)
and [2026 FIA Section C, Technical Regulations, Issue
20](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf),
both published 5 August 2026.

Each experiment must pin its regulatory profile. The inherited core rule is:

```text
all declared primary propulsion energy is onboard before the race
no undeclared external primary-energy inflow is permitted during the race
```

Internal energy recovery may be designed freely when the experiment permits it,
but every recovered joule must trace to braking, exhaust, heat, suspension, or
another declared physical flow. Conservation losses remain observable; energy
cannot be counted twice or created by a control edge.

The project does **not** automatically impose every current FIA ICE/ERS geometry
or architecture-specific limit. Comparisons involving batteries, chemical fuel,
flywheels, compressed media, thermal stores, or an agent-proposed energy system
need a versioned, technology-neutral energy-equivalent profile. Every treatment
must receive the same declared initial primary-energy opportunity, unless the
energy budget itself is the predeclared independent variable.

## Open 3D Design Domain

Agents may eventually change or create:

- complete vehicle topology and packaging;
- body dimensions, external surfaces, and aerodynamic devices;
- the number, placement, and assignment of permitted ground-contact endpoints;
- energy stores, converters, propulsion paths, cooling paths, and controllers;
- structures, housings, ducts, rotors, joints, couplings, fasteners, and other
  components not present in a conventional catalog;
- internal material distribution and component geometry, within the declared
  material and manufacturing language.

A previously unseen bolt or fastener is allowed as a candidate. It does not
become a discovery merely because its shape is new. Its interfaces, material,
manufacturing assumptions, loads, contact behavior, failure modes, and effect on
the complete race vehicle must survive the same evidence gates as known parts.

Complete 3D design is a causal simulation input, not a decorative render:

```text
functional requirements and typed interfaces
  -> agent-generated complete 3D CAD / B-rep / implicit geometry
  -> independent geometry validity and interface checks
  -> geometry-derived volume, mass, centre of mass, and inertia
  -> packaging, collision, clearance, and manufacturing gates
  -> structural, thermal, flow, electromagnetic, and aerodynamic evaluation
  -> uncertainty-aware component models
  -> vehicle and race simulation
  -> failures and evidence returned to the next design generation
```

No generated component may self-report that it is light, strong, cool,
efficient, safe, or manufacturable. Those properties must come from declared
materials, geometry, boundary conditions, and independent evaluators.

## What Counts as a Discovery

A design is only a **technology-discovery candidate** when:

1. its functional architecture or operating principle differs from the declared
   baselines, rather than only its appearance;
2. it improves total race time or another predeclared metric under matched
   constraints, evaluation budget, component opportunity, and random seeds;
3. the advantage is not explained by a solver bug, hidden energy, invalid
   material, objective loophole, or unequal compute;
4. the candidate remains valid when promoted to the next fidelity level and is
   checked by an independent model where practical;
5. source, geometry, configuration, regulatory profile, solver settings,
   artifacts, hashes, and replay metadata are preserved.

“Generated,” “simulation-valid,” “promoted,” “physically validated,” and
“discovered” are different evidence claims and must not be used interchangeably.

## Current Implementation Status

The ultimate mission is intentionally broader than the current implementation.
The repository currently contains governance and validation documents, a
deterministic Level-0 longitudinal reference kernel, and the first constrained
`CadQuery -> STEP -> FreeCAD -> Level 0` component evidence loop. The first 3D
grammar is a bounded mounting-plate experiment, not a full vehicle and not a
physically validated racing component.

Phase 1 remains deliberately narrow: discover and compare one-dimensional
powertrain topologies under matched budgets before opening whole-vehicle 3D
geometry, aerodynamics, structures, and control co-design. The fidelity ladder
is a promotion path, not permission to claim later-stage capability early.

## Repository Map

```text
config/                         Versioned simulation and experiment settings
docs/
  3d/                           CAD environments and constrained 3D grammars
  DESIGN_LANGUAGE_BOUNDARY.md  What the search can and cannot discover
  PHYSICS_SYSTEM_PLAN.md       Physics domains, contracts, solvers, and roadmap
  RESEARCH_CHARTER.md           Research question, hypotheses, and scope
  VALIDATION_STRATEGY.md        Evidence required before scientific use
  WORK_PROTOCOL.md              Plan-before-work and result-after-work rules
  work_logs/                    Auditable plan/result records
src/formula_ultimate/
  components/                   Physical component models and typed ports
  topology/                     Candidate graphs, mutation, and graph validation
  physics/                      Equations, units, and numerical solvers
  simulation/                   Race execution and fidelity orchestration
  telemetry/                    Reproducible outputs and failure evidence
  experiments/                  Baselines, sweeps, and multi-seed studies
tests/                          Unit, invariant, integration, and regression tests
```

## Development Workflow

Every work item starts with separate English and Thai Markdown plans and ends
with separate English and Thai result records containing equivalent,
reproducible test evidence. Every maintained English Markdown document has a
sibling `.th.md` file. Read
[`docs/WORK_PROTOCOL.md`](docs/WORK_PROTOCOL.md) before making changes.

Run the current repository checks with:

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Research Boundary

Formula Ultimate does not claim to remove all human assumptions. The race
definition, energy profile, physics models, material/manufacturing language,
component and geometry grammars, numerical solvers, fidelity gates, and
objective are explicit experimental boundaries. Open-ended search means no
prescribed conventional architecture **within those declared boundaries**; it
does not mean no constraints.

Novel appearance is not evidence of new technology, and Level-0 success is not
physical validation. The preferred hypothesis must be actively falsified at
each promotion stage.
