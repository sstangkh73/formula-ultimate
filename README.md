# Formula Ultimate

Formula Ultimate is a research platform for studying open-ended engineering
discovery under explicit physical, safety, resource, and race constraints.

> No prescribed vehicle architecture beyond declared constraints.

The first research phase is deliberately narrow: discover and compare
one-dimensional powertrain topologies before introducing free vehicle geometry,
aerodynamics, structures, or control co-design.

## Current Status

The repository contains the research charter, physics-system plan,
design-language boundary, validation strategy, work protocol, package skeleton,
and a deterministic Level-0 longitudinal reference kernel. The kernel is an
analytical test foundation; it is **not** yet a validated race-car simulator.

## Repository Map

```text
config/                         Versioned simulation and experiment settings
docs/
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

Every work item starts with a Markdown plan and ends with a Markdown result
record containing reproducible test evidence. Read
[`docs/WORK_PROTOCOL.md`](docs/WORK_PROTOCOL.md) before making changes.

Run the current repository checks with:

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Research Boundary

The platform does not claim to remove all human assumptions. Its design
language, component models, numerical solvers, and objectives are explicit
experimental boundaries. Novelty claims are valid only within those boundaries.
