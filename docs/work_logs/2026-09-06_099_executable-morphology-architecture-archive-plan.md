# Work 099 Plan: Executable Morphology, Architecture and Archive Search

Thai companion: `2026-09-06_099_executable-morphology-architecture-archive-plan.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Objective and starting evidence

Implement the bounded Work 099 deliverable defined by `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` after reviewing completed Work 098 commit `ec0004b`. Work 098 established candidate/evidence identity, immutable event history, cost settlement and decision replay, but deliberately did not execute morphology or implement a quality-diversity archive. Work 099 will add an executable numerical solid-network representation, architecture-changing operators and bounded archives while preserving that contract.

This remains a software and CAD execution work item. Geometry measurements establish that the proposed computational objects exist and differ; they do not establish useful physics, manufacturing feasibility, race performance, technology novelty or physical validation.

## Scope and planned files

- `src/formula_ultimate/search/executable_morphology.py`: strict variable-length numerical geometry, material-region/part, interface, terminal-ancestry and optional controller-gene validation; deterministic mutation traces; perturb/grow/split/merge/rewire/radius/controller operators; ID-invariant functional signatures.
- `src/formula_ultimate/search/morphology_archive.py`: deterministic bounded niches with separate feasible, failed and unresolved slots, explicit evidence scope, tie-breaking, lineage/novelty retention, capacity and reproduction/escalation accounting.
- `config/experiments/executable_morphology_qd_v1.json`: seeds, representation bounds, operator schedule, CAD measurement fields, archive descriptors/capacities and software-fixture claim boundary.
- `scripts/experiments/run_executable_morphology_qd.py`: deterministic proposals, CadQuery execution and STEP export, geometry/terminal measurement, Work 098 ledger events, archive updates, failure retention, replay reopening and tolerance-based cross-run comparison.
- `tests/test_executable_morphology_qd.py`: adversarial schema/operator/archive/identity tests plus optional real-CAD integration under the pinned local CadQuery environment.
- `docs/contracts/EXECUTABLE_MORPHOLOGY_ARCHIVE_V1.md` and `.th.md`: executable interface, state/archive semantics, commands, evidence and limitations.
- This bilingual plan and matching bilingual result. Generated evidence remains ignored under `artifacts/work099/`.

## Experiment variables and controls

- Independent variables: mutation operator and registered seed; archive disposition is tested with the same descriptor and capacity rules.
- Dependent evidence: genotype identity, canonical functional-graph signature, CAD STEP digest, measured volume/surface/bounds/centre/topology counts, terminal positions and ancestry, niche coverage, archive replacement/retention and exact ledger decision replay.
- Controls: same root representation, numerical bounds, material hypothesis, external terminal roles/domains, CAD implementation, operator schedule, per-seed proposal count, archive capacities and Work 098 software-fixture registration.
- Success: repeated seeds execute previously undeclared geometry identities; at least one morphology mutation changes both geometry digest and a measured geometric field; split and merge change decomposition; multiple canonical functional signatures occur; failed/unresolved examples remain separately bounded; reopening the ledger reproduces decision state exactly.
- Failure: identity-only or rigid-transform-only diversity, hidden geometry repair, unbounded archive growth, overwritten failures, stale evidence reuse, nondeterministic proposal lineage, or any physical/manufacturing/discovery claim from this CAD-only evidence.

## Validation and success criteria

1. Run `python -m unittest tests.test_executable_morphology_qd -v`, including negative finite/bounds/ancestry/identity cases, all registered operators, deterministic replay, split/merge behavior, archive capacity/tie rules and claim-boundary checks.
2. Run the real CAD fixture twice with `.tools/cadquery-mcp/Scripts/python.exe`, using separate `artifacts/work099/run_a` and `run_b`; compare deterministic genotype, functional, geometry and measured-field evidence under declared numerical tolerances while reporting variable timing separately.
3. Reopen each Work 098 ledger at its trusted head and verify exact decision/state replay. Confirm representation-invalid and boundary-unresolved attempts remain charged and distinct from successful geometry.
4. Run targeted regressions `python -m unittest tests.test_discovery_contract tests.test_topology_genome tests.test_topology_mutation tests.test_freeform_solid_grammar tests.test_repository_contract -q`, then `python -m compileall -q src scripts tests` and `python -m unittest discover -s tests -q` as final gates.
5. Verify the English/Thai documentation pairs, local links and claim wording; run `git diff --check`; stage only declared files; inspect `git diff --cached --name-only`; run `git diff --cached --check`; commit this work and verify the new commit.

Every validation gate is fail-fast. A blocker leaves this plan `In progress` or changes it to `Stopped` with the exact reason; completion requires a successful scoped commit.

## Risks, controls and explicit non-goals

Risks include CAD-kernel nondeterminism, topology changes that do not alter executable shape, terminal ancestry becoming stale after split/merge, archive novelty overriding failure, and software-fixture labels being mistaken for physical outcomes. Controls are canonical genotype/signature hashing, measured geometry identities, ancestry validation after every mutation, deterministic tie-breaking, separate evidence scopes and ledger-based cost/history retention. CAD timing is observable but excluded from exact numerical identity comparisons.

Non-goals: Work 100 physics or coupled trials, Work 101 vehicle promotion, field solvers, physical feasibility, manufacturability, race-time optimization, statistical superiority, unrestricted representations, distributed/asynchronous scheduling, external publication, push or changes to completed Work 098 evidence. V1 supports a bounded swept-solid network and registered operators; it does not claim arbitrary CAD or universal component discovery.
