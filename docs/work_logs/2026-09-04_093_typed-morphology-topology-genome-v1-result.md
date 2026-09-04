# Work 093 Result: Typed Morphology and Topology Genome V1

Thai companion: `2026-09-04_093_typed-morphology-topology-genome-v1-result.th.md`

## Status and outcome

Status: Completed

Work 093 replaced the fixed-list representation boundary with a bounded typed topology genome. Six admitted genomes span five distinct part counts and six pairwise distinct ID-invariant topology signatures. Every load, energy, motion, fluid, thermal, and control terminal is traced through exact compatible interfaces before CAD.

This proves topology representation and traceability only. No genome mutation, CAD assembly, physics, or discovery was executed.

## Files changed

- `config/genomes/typed_morphology_topology_genome_v1.json`
- `src/formula_ultimate/search/topology_genome.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/inspect_topology_genome_corpus.py`
- `tests/test_topology_genome.py`
- `docs/contracts/TYPED_MORPHOLOGY_TOPOLOGY_GENOME_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored replay evidence under `artifacts/work093/`

## Decisions and evidence

- The genome includes part containment, Work 092 source solid family, per-part feature DAG, material/process identity, typed interfaces/DOF, terminals, ordered functional paths, and optional symmetry.
- Every adjacent path step must cite an interface joining the exact parts and supporting every carried domain.
- All terminals and parts must participate in a valid path. Parent containment must be acyclic.
- The topology signature enumerates all permutations up to the declared eight-part bound and hashes the lexicographically minimal full typed representation. Consistent identifier renaming preserves it.
- Legacy five-scalar fields are outside the schema and fail closed.
- Initial corpus validation exposed domain-incompatible cross-links in the nested and asymmetric examples. Separate electrical and fluid/thermal interfaces were declared; domains were not silently added to physically different interface types.

## Successful corpus evidence

| Genome | Parts | Interfaces | Paths | Branch parts | Cycle rank |
|---|---:|---:|---:|---:|---:|
| `monolithic_crossdomain_001` | 1 | 0 | 1 | 0 | 0 |
| `serial_three_001` | 3 | 2 | 1 | 0 | 0 |
| `branch_four_001` | 4 | 3 | 3 | 1 | 0 |
| `cyclic_four_001` | 4 | 4 | 2 | 0 | 1 |
| `nested_crosslink_five_001` | 5 | 7 | 3 | 3 | 3 |
| `asymmetric_hybrid_six_001` | 6 | 7 | 3 | 2 | 2 |

- Distinct part counts: `[1, 3, 4, 5, 6]`
- Unique topology signatures: `6 / 6`
- Source Work 092 declaration: `a0e1c47ee15dbebac9dce2183a502c26199197b751fe427c74c2824dd1b4ad8a`
- Genome declaration SHA-256: `e1583e9aec9c3a4968ec5e35d1b81478d9023ca2392e08ec78ee0a48e9e5c69d`
- Result SHA-256: `65599c0b3153609c2b532d10b95051c339d1766ffbd345dfefded711e6bfab0e`
- `legacy_five_scalar_dependency: false`
- `cad_executed: false`

## Exact validation commands

```powershell
python -m unittest tests.test_topology_genome -v
# exit 0; 7 tests passed

python scripts/experiments/inspect_topology_genome_corpus.py --config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --output artifacts/work093/run_a/result.json
# exit 0

python scripts/experiments/inspect_topology_genome_corpus.py --config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --output artifacts/work093/run_c/result.json --replay-reference artifacts/work093/run_a/result.json
# exit 0; complete result equality

python -m compileall -q src scripts tests
python -m unittest tests.test_topology_genome tests.test_repository_contract -v
# exit 0; 13 tests passed

python -m unittest discover -s tests -q
# exit 0; 654 tests passed in 475.837 s; 7 expected environment-dependent skips
```

An earlier full-regression process completed outside the retained execution session, so it was not counted as evidence. The full suite above was rerun and its exit status was observed directly.

## Limitations and follow-up

The material/process IDs are declarations, not evidence. Interface domains express routing compatibility but do not yet prove matching geometry or conservation. The bounded permutation canonicalizer is exact within eight parts but intentionally unsuitable for unbounded graphs. Work 094 must add reproducible add/remove/split/merge/branch/reroute proposals with lineage and bounded retries; Work 095 must reject construction/manufacturing failures visibly.
