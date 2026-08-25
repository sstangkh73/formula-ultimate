# Work 012 Plan: Typed Energy and Powertrain Component Graph

Status: Completed

Thai companion: `2026-08-26_012_typed-energy-graph-plan.th.md`

## Objective

Implement a deterministic typed component graph for vehicle energy flow so an
agent can compose sources, converters, transmissions, tyres, and sinks only
through compatible directed power ports before any energy simulation runs.

## Scope

- Define strict component, port, connection, graph, and compiled-graph
  contracts.
- Use explicit energy carriers: chemical, electrical, mechanical rotational,
  mechanical translational, and thermal.
- Use directed input/output ports with power capacity in watts.
- Provide constructors for source, converter, transmission, tyre, and sink
  component roles.
- Compile a graph through deterministic lexical topological ordering.
- Reject carrier mismatch, direction mismatch, missing ports, duplicate
  component/port/connection identities, unconnected required ports, implicit
  output fan-out, multiple sources into one input, self-loops, and cycles.
- Preserve the original graph and return an explicit compiled order; do not
  silently repair invalid topology.
- Add analytical valid-chain, permutation/replay, and falsifying invalid-graph
  tests plus a validator and bilingual documentation.
- Validate and commit Work 012 separately before Work 013 begins.

## Planned files

- `src/formula_ultimate/physics/energy_graph.py`
- `src/formula_ultimate/physics/__init__.py`
- `scripts/validate_energy_graph.py`
- `tests/test_energy_graph.py`
- `docs/physics/ENERGY_COMPONENT_GRAPH.md`
- `docs/physics/ENERGY_COMPONENT_GRAPH.th.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.th.md`
- this Work 012 plan/result pair in English and Thai
- a separate bilingual problem report only if a material problem is found

## Model boundary

Every port carries nonnegative directed power capacity in watts. Connection
direction defines positive flow from an output to an input. A connection is
type-compatible only if both ports declare the same carrier.

Work 012 validates topology and interface meaning only. It does not assign
instantaneous power, integrate joules, apply efficiency, track stored energy,
or prove conservation. Those operations belong to Work 013 and later.

The baseline compiler requires each port to have exactly one connection. Output
fan-out is rejected because duplicating a power output into multiple branches
would create ambiguous energy accounting; a future explicit splitter must
declare allocation and conservation.

## Experiment definition

### Preferred hypothesis

A typed, fail-closed graph rejects physically ambiguous powertrain topologies
before simulation while compiling a valid source-to-tyre chain identically
regardless of component and connection input ordering.

### Independent variables

- component roles and identifiers;
- port carriers, directions, and capacities;
- connection endpoints and input ordering.

### Dependent variables

- compile success/failure and explicit reason;
- deterministic component order;
- deterministic connection order;
- derived connection capacity.

### Controls

- fixed carrier vocabulary and role factories;
- lexical tie-breaking in topological sort;
- all ports required and one-to-one in the Work 012 baseline;
- no numerical randomness or silent topology repair.

### Falsification and failure criteria

- A chemical output connected directly to a mechanical input must fail.
- Output-to-output, input-to-input, missing endpoint, duplicate input source,
  implicit fan-out, self-loop, and cycle must fail.
- A disconnected required port must fail.
- Permutations of the same valid graph must compile to identical metadata.
- Invalid/non-finite/negative capacities and unsupported carrier/direction/role
  values must fail.

## Validation

```powershell
python -m unittest tests.test_energy_graph -v
python -m unittest discover -s tests -v
python scripts/validate_energy_graph.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Commands will use fail-fast exit handling.

## Success criteria

- A source → converter → transmission → tyre → sink graph compiles.
- Compiled order is deterministic across input permutations.
- Every declared falsifying topology is rejected with an observable error.
- Full tests, validator, compilation, bilingual Markdown contract, whitespace,
  explicit staging, commit, and post-commit verification pass.

## Risks

- A generic graph can appear physically meaningful while containing no actual
  conservation law; documentation and status must keep that boundary explicit.
- One-to-one ports limit branching and regenerative loops, which require
  explicit future components and temporal semantics.
- Capacity compatibility alone does not determine operating power.

## Explicit non-goals

- No energy integration, efficiency loss, storage depletion, conservation
  audit, thermal flow, regenerative loop, or controller.
- No claim that a compiled graph is physically validated or manufacturable.
- No Work 013 audit before the Work 012 commit.
- No remote push.
