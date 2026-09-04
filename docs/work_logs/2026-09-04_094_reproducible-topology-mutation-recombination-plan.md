# Work 094 Plan: Reproducible Topology Mutation and Recombination

Thai companion: `2026-09-04_094_reproducible-topology-mutation-recombination-plan.th.md`

## Status

Status: Completed

## Objective

Implement deterministic, bounded proposal machinery that changes Work 093 typed topology without hand-authoring each child. Every proposal must record exact parent identity, seed and RNG checkpoint, selected operator and probability, bounded attempt/retry accounting, mutation trace, validation outcome, and final genotype/topology identity.

## Scope and planned files

- `config/experiments/topology_mutation_v1.json`
- `src/formula_ultimate/search/topology_mutation.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/run_topology_mutation_pilot.py`
- `tests/test_topology_mutation.py`
- `docs/contracts/REPRODUCIBLE_TOPOLOGY_MUTATION_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored deterministic pilot/replay evidence under `artifacts/work094/`

## Independent/dependent variables and controls

- Independent inputs: frozen Work 093 parent corpus/identity, initializer stratum, RNG seed/checkpoint, operator probability table, attempt/retry budgets, typed part/interface/domain pools, material/process compatibility table, and mutation-after-observation policy.
- Dependent outputs: proposal sequence, selected operator, attempt/retry count, accepted/rejected state, failure code, child genotype and topology identities, topology-change status, and per-family opportunity/yield.
- Controls: same parent/seed/budget must replay exactly; key reordering must preserve protocol identity; changed seed/checkpoint/operator budget must change lineage; parent-cycle, disconnected mandatory terminal, impossible joint/domain, incompatible material/process, exhausted retry budget, and mutation after result observation must fail visibly.

## Admitted bounded proposal families

- `grow_branch`: add a typed child part, interface, sink terminal, and routed domain branch.
- `prune_branch`: remove an eligible terminal leaf and reroute/remove its covered declarations only when all mandatory domains remain traced.
- `split_part`: replace one routed part position with two serial parts and a compatible interface.
- `add_crosslink`: add a non-duplicate typed interface between existing parts.
- `reroute_path`: replace a route with an alternate compatible interface chain.
- `replace_solid_family`, `insert_feature`, and `mutate_material_process` as typed non-topology controls.

Optional crossover is represented in the protocol but disabled in this V1 pilot unless two parents expose exactly compatible typed cut boundaries. Disabled opportunity must remain recorded rather than silently reassigned.

## Fairness and success criteria

- Primitive, skeletal/serial, shell, rotary, branching, and hybrid initializer strata receive equal declared proposal slots; unused/invalid slots are not transferred.
- At least four topology-changing operator families produce Work 093-valid child genomes in the bounded pilot.
- Every accepted topology proposal has a topology signature different from its parent; non-topology controls must not be mislabeled as topology changes.
- Identical clean runs reproduce the exact ordered ledger and result SHA-256.
- Negative controls reject cycles, disconnected terminals/domains, impossible interface rules, incompatible material/process declarations, post-result mutation, and replay mutation.
- Focused tests, compilation, repository contracts, pilot/replay, and full regression pass.

## Risks and explicit non-goals

Mutation can bias toward easy small graphs, retry until a preferred outcome, accidentally transfer compute between initializer families, or create ID-only novelty. V1 uses fixed slots, deterministic operator selection, bounded retries, and Work 093 canonical signatures. It does not execute CAD/physics, perform result-conditioned repair, optimize operator probabilities, claim quality, or implement unrestricted graph crossover.
