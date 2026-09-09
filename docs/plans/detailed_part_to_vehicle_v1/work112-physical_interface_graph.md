# Work 112: Physical terminals and assembly semantics

Thai companion: `work112-physical_interface_graph.th.md`

Status: Planned

Original Work 106 package: 111

Dependencies: Work 108

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Represent real load, motion, thermal and other declared interfaces without losing parallel paths or imposing conventional part roles.

Use Work 108 regions and the limitations of Work 105 uncolored simple-graph descriptors.

## 2. Proposed files

- `src/formula_ultimate/assembly/physical_interface_graph.py`
- `config/development/physical_interface_graph_v1.json`
- `scripts/development/run_physical_interface_graph.py`
- `tests/test_physical_interface_graph.py`

## 3. Implementation sequence

1. Define terminal frames, spatial regions, units, domain variables and sign conventions.
2. Represent typed multiedges, allowed motion and constitutive-law references.
3. Implement renaming-invariant identity without dropping roles, direction or multiplicity.
4. Transfer interfaces through geometry split/merge and emit evidence invalidation events.

## 4. Experiment

- IV: Terminal roles, orientation, multiplicity, part grouping and split/merge.
- DV: Connectivity, interface compatibility, conserved exchanges and identity stability.
- Controls: Equivalent geometry and physical interactions under identifier-only changes.

## 5. Tests and falsification

Renaming must preserve meaning; swapping source/sink or dropping a parallel edge need not. Reject incompatible units, missing mating surfaces and rigid/moving conflicts.

## 6. Registration and acceptance

Freeze supported interface laws, frame tolerances, identity limits and compatibility rules.

All equivalence and distinction fixtures pass; disconnected paths remain disconnected. Identity is a descriptor, never sole proof of a mechanism.

## 7. Deliverables and handoff

Interface schema, semantic graph corpus, region bindings and compatibility/identity reports.

Feeds Work 113 connections and Work 117 bidirectional task generation.

## 8. Risks and non-goals

Canonicalization can scale poorly. Bound runtime and preserve unresolved identity, without banning geometry. No general mechanism-discovery claim.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_physical_interface_graph tests.test_repository_contract -v
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_a
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_b --replay-reference artifacts/work112/run_a/result.json
```
