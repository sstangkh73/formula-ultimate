# Reproducible Topology Mutation V1

Thai companion: `REPRODUCIBLE_TOPOLOGY_MUTATION_V1.th.md`

## Boundary

This contract creates deterministic, typed, pre-evaluation proposals from the Work 093 corpus. Acceptance proves only that the child is a traceable bounded genotype under the declared grammar and policy. It does not prove CAD realizability, manufacturability, physical feasibility, safety, performance, or scientific validity.

## Fixed opportunities and lineage

Six initializer strata receive the same ordered eight operator slots. A rejected slot remains rejected; its budget cannot be transferred. Each ledger entry records parent genotype/topology identities, stratum seed, slot, operator and declared probability, RNG checkpoints, retry trace, child genotype/topology identities when accepted, and a lineage SHA-256. Retries are bounded by the frozen protocol.

The five topology operators are `grow_branch`, `prune_branch`, `split_part`, `add_crosslink`, and `reroute_path`. The three controls are `replace_solid_family`, `insert_feature`, and `mutate_material_process`; they may change the canonical genotype signature but are never labeled as topology operators. Crossover is explicitly disabled because V1 lacks a compatible typed cut-boundary contract.

## Fail-closed rules

Every attempted child is revalidated in the complete Work 093 corpus. Invalid containment cycles, untraced parts/terminals/domains, disconnected paths, impossible interface domain/DOF declarations, incompatible material/process pairs, no-op topology signatures, exhausted retries, or any proposal made after evaluation evidence is available fail visibly. No result-conditioned mutation or hidden retry is permitted.

## Replay

Canonical JSON hashing ignores mapping-key order but preserves arrays and all values. The same frozen inputs reproduce the exact ordered ledger and `result_sha256`; a changed reference must fail replay rather than be silently accepted.
