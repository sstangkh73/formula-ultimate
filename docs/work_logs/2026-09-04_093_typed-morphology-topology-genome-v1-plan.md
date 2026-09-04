# Work 093 Plan: Typed Morphology and Topology Genome V1

Thai companion: `2026-09-04_093_typed-morphology-topology-genome-v1-plan.th.md`

## Status

Status: Completed

## Objective

Implement a bounded, canonical typed genome that represents a candidate as mutable part containment, interface/joint, per-part feature DAG, material/process, and functional-path graphs instead of the old fixed component list plus five scalar dimensions. Reject any genome whose mandatory load, energy, motion, fluid, thermal, or control terminals are not causally traceable before CAD execution.

This work defines and validates topology representation. Work 094, not Work 093, will implement stochastic mutation/recombination.

## Scope and planned files

- `config/genomes/typed_morphology_topology_genome_v1.json`
- `src/formula_ultimate/search/topology_genome.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/inspect_topology_genome_corpus.py`
- `tests/test_topology_genome.py`
- `docs/contracts/TYPED_MORPHOLOGY_TOPOLOGY_GENOME_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored deterministic evidence under `artifacts/work093/`

## Genome layers

1. Required functional domains and typed source/sink terminals.
2. Part graph with bounded parent/child containment and exact Work 092 solid-family declaration.
3. Interface/joint graph with admitted domains and allowed degrees of freedom.
4. Per-part acyclic feature graph plus material/process declaration.
5. Ordered load, energy, motion, fluid, thermal, and control paths.
6. Optional symmetry gene (`none`, mirror, or rotational), never a mandatory vehicle prior.

## Independent/dependent variables and controls

- Independent inputs: part count/types/parents, feature ancestry/operators, interface endpoints/type/domains/DOF, terminal placement/role/domain, ordered path routing, material/process IDs, and optional symmetry.
- Dependent outputs: validity, exact traceability, part/interface/path counts, topology-canonical signature, graph degree/branch/cycle descriptors, feature-operator coverage, and replay identity.
- Negative controls: duplicate IDs, missing/forward feature ancestry, parent cycle, self-interface, duplicate edge, unsupported domain/DOF, missing source or sink, orphan mandatory terminal, path endpoint mismatch, interface/path domain mismatch, disconnected route, symmetry misuse, non-finite or excessive bounds, and unknown fields.
- Metamorphic controls: key order and consistent identifier renaming preserve topology signature; adding/removing a branch, part, interface, feature dependency, or path changes it.

## Validation and success criteria

- A corpus of at least six valid genomes with at least four distinct part counts.
- Every required domain has a source-to-sink path; every mandatory terminal appears in a valid path; each adjacent part step uses the declared interface supporting that domain.
- At least six pairwise distinct canonical typed-graph signatures, including monolithic, serial, branching, cyclic, nested/cross-linked, and asymmetric hybrid examples.
- At least one valid genome has a different part count from every fixed Work 050 five-part assumption, and topology signatures must not depend on the old five scalar dimensions.
- Identifier-renaming and declaration-key-order controls replay; branch/reroute/feature-dependency mutations change identity.
- Focused tests, repository contracts, compilation, deterministic inspector replay, and full regression pass.

## Risks and explicit non-goals

A weak signature could confuse renamed isomorphic graphs with genuine topology changes; path lists could claim connectivity not supported by interfaces; optional symmetry could become an accidental prior; and family labels could reintroduce conventional layouts. V1 therefore canonicalizes bounded typed graphs independently of IDs and validates each route edge. This work does not mutate genomes, execute every genome in CAD, repair invalid topology, evaluate physics/manufacturing, optimize a vehicle, or claim discovery.
