# Typed Morphology and Topology Genome V1

Thai companion: `TYPED_MORPHOLOGY_TOPOLOGY_GENOME_V1.th.md`

## Purpose and claim boundary

`typed_morphology_topology_genome_v1` represents a candidate as bounded typed graphs rather than a fixed five-part list controlled by five scalar dimensions. The validator and identifier-independent topology signature are in `src/formula_ultimate/search/topology_genome.py`; the admitted corpus is `config/genomes/typed_morphology_topology_genome_v1.json`; and the deterministic report is produced by `scripts/experiments/inspect_topology_genome_corpus.py`.

Passing proves representation and pre-CAD functional traceability only. V1 does not mutate a genome, construct a full assembly, prove interface geometry, run physics, or establish that any represented topology is useful.

## Root and source identity

The root declares the exact genome version, Work 092 solid-grammar SHA-256, all six required domains, bounded counts, and genomes. Limits admit at most 8 parts, 24 interfaces, 32 features per part, and 24 paths. Unknown fields or identities fail closed. Legacy scalar parameters have no admitted field and cannot affect the topology signature.

Each part declares parent containment, exact Work 092 source candidate/family, material/process identity, an ordered feature DAG using Work 092 operator identities, and a final feature. Material/process IDs are declarations only; they are not evidence of availability or manufacturability.

## Interfaces, terminals, and paths

Interfaces connect two distinct known parts and declare interface type, supported functional domains, and allowed DOF. Duplicate typed edges, self-interfaces, unsupported domains/DOF, and excessive counts fail. Parent containment must be acyclic.

All terminals are mandatory and typed as source, sink, or bidirectional across one or more of `load`, `energy`, `motion`, `fluid`, `thermal`, and `control`. Every required domain must have a source-to-sink path. A path declares ordered parts and exact interface identities; every adjacent step must match the interface endpoints and the interface must support every domain carried by that path. Every terminal and part must participate in at least one valid route. A disconnected list cannot claim functional closure.

Symmetry is an explicit optional gene: `none`, `mirror`, or `rotational`. `none` cannot carry a hidden axis/order, so symmetry is not a mandatory prior.

## Canonical topology identity

For the bounded maximum of eight parts, V1 enumerates part permutations and selects the lexicographically minimum complete typed representation. It includes part family/source/material/process, identifier-independent feature ancestry, directed containment, typed interfaces/DOF, terminal roles/domains, functional routes, and symmetry. SHA-256 of that representation is the topology signature.

Consistent renaming of part, feature, interface, terminal, and path IDs therefore preserves the signature. Changing a part/branch, containment relation, interface, route, feature dependency, material/process declaration, or symmetry changes the signature. This is exact within the V1 schema and bound, not a claim about unbounded graph canonicalization.

## Corpus and replay

The six admitted examples are monolithic, serial-three, branching-four, cyclic-four, nested/cross-linked-five, and asymmetric-hybrid-six. Their part counts are `[1, 3, 4, 5, 6]`; all six topology signatures are distinct. The corpus includes branching vertices and interface cycles and is not reachable by changing the old five scalar values alone.

```powershell
python scripts/experiments/inspect_topology_genome_corpus.py `
  --config config/genomes/typed_morphology_topology_genome_v1.json `
  --solid-config config/cad/freeform_brep_solid_grammar_v2.json `
  --output artifacts/work093/run_a/result.json

python scripts/experiments/inspect_topology_genome_corpus.py `
  --config config/genomes/typed_morphology_topology_genome_v1.json `
  --solid-config config/cad/freeform_brep_solid_grammar_v2.json `
  --output artifacts/work093/run_c/result.json `
  --replay-reference artifacts/work093/run_a/result.json
```

## Limitations and next work

V1 does not yet define proposal probabilities, mutation eligibility, retry budgets, crossover, repair, lineage checkpoints, or archive selection. It also does not guarantee that all valid graphs can be assembled geometrically or evaluated physically. Work 094 must implement reproducible topology mutation and reject invalid proposals; Work 095–097 must then establish construction, semantics, meshing, and physics before these graphs can support discovery trials.
