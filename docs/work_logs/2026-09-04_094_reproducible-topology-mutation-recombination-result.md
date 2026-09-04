# Work 094 Result: Reproducible Topology Mutation and Recombination

Thai companion: `2026-09-04_094_reproducible-topology-mutation-recombination-result.th.md`

## Status and outcome

Status: Completed

Work 094 implements a deterministic, bounded, pre-evaluation proposal ledger over the Work 093 typed topology corpus. All six initializer strata received exactly eight operator slots. The 48-slot pilot accepted four distinct topology-changing families: `grow_branch`, `split_part`, `add_crosslink`, and `reroute_path`. Exact replay reproduced the complete ordered result and SHA-256.

This establishes reproducible typed proposal mechanics only. It does not establish CAD realizability, constructive validity, manufacturability, physics, safety, performance, or discovery.

## Files changed

- `config/experiments/topology_mutation_v1.json`
- `src/formula_ultimate/search/topology_mutation.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/run_topology_mutation_pilot.py`
- `tests/test_topology_mutation.py`
- `docs/contracts/REPRODUCIBLE_TOPOLOGY_MUTATION_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored replay evidence under `artifacts/work094/`

## Decisions and evidence

- Proposal opportunity is fixed before execution: six strata by eight ordered operators. Rejections cannot transfer their slot or retry budget.
- Each accepted entry records parent genotype and topology identities, seed, slot, operator/probability, bounded retries, RNG checkpoints, trace, full child genotype, child identities, and lineage SHA-256.
- `reroute_path` retains the original traceable path and adds a typed alternate route; removing the original route during development made intermediate parts untraceable and was rejected.
- The protocol policy was aligned to the frozen Work 093 interface domains/DOF and material/process pairs. Unsupported extensions still fail closed.
- `prune_branch` accepted no child because no terminal leaf was redundant while preserving required traces. Its 18 failed attempts (six slots, three attempts each) remain visible.
- Non-topology controls are `declared_topology_change: false`. V1 crossover remains explicitly disabled because a compatible typed cut boundary is undefined.
- Mutation after observation raises before any proposal. Cycle, disconnected route, impossible interface policy, incompatible material/process, exhausted retry, protocol mutation, and replay mutation are negative controls.

## Pilot evidence

- Total slots: `48`; opportunities per stratum: `8`
- Accepted per stratum: primitive `5`, skeletal/serial `7`, shell `7`, rotary `7`, branching `6`, hybrid `7`
- Accepted per operator: `grow_branch=6`, `prune_branch=0`, `split_part=6`, `add_crosslink=5`, `reroute_path=4`; each non-topology control `=6`
- Protocol SHA-256: `1d475fbca89bf9395fe97d51f68a7c3ca1cb2cd063e9d4101cc4263a84c2cf10`
- Source Work 093 declaration SHA-256: `e1583e9aec9c3a4968ec5e35d1b81478d9023ca2392e08ec78ee0a48e9e5c69d`
- Result SHA-256: `75637c436e38452e588521402cf325e9b494bdcb77333d1fb72109e87e3b006f`
- `mutation_after_observation_allowed: false`; `cad_executed: false`

## Exact validation commands

```powershell
python -m unittest tests.test_topology_mutation -q
# exit 0; 9 tests passed

python scripts/experiments/run_topology_mutation_pilot.py --genome-config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --protocol config/experiments/topology_mutation_v1.json --output artifacts/work094/run_a/result.json
# exit 0; 48 slots; four accepted topology operator families

python scripts/experiments/run_topology_mutation_pilot.py --genome-config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --protocol config/experiments/topology_mutation_v1.json --output artifacts/work094/run_b/result.json --replay-reference artifacts/work094/run_a/result.json
# exit 0; exact complete-result replay

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; 663 tests passed in 523.121 s; 7 expected environment-dependent skips
```

An attempted convenience command, `python scripts/check_repository.py`, returned exit 2 because that script does not exist. It was not treated as a gate; the maintained `tests.test_repository_contract` gate was run before commit.

## Limitations and follow-up

Operator opportunity is fixed and fair, but acceptance rates are not calibrated. The corpus has no safely redundant leaf, so `prune_branch` is a visible bounded rejection. `reroute_path` adds rather than swaps an alternate route to preserve traceability. Work 095 must independently reject constructive and manufacturing failures; later work must generate CAD assemblies and evaluate physics without feeding observed results back into this ledger.
