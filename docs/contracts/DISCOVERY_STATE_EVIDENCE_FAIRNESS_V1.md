# Discovery State, Evidence and Fairness Contract V1

Thai companion: `DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Implementation: Work 098; schema `discovery_contract_v1`

Governing design: [Whole-Vehicle and Technology Discovery Protocol V1](WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md). This implementation establishes a software admission/accounting contract for the later geometry, controller and vehicle search. It does not establish any physical law, CAD execution, field solution or discovered vehicle.

## 1. Implemented modules and entry point

| File | Responsibility |
| --- | --- |
| `src/formula_ultimate/experiments/discovery_registration.py` | Strict registration envelope, coverage/gate declarations, budget/partition validation and immutable digest |
| `src/formula_ultimate/experiments/discovery_evidence.py` | Causal identity, orthogonal outcomes, scoped artifact admission, exploratory permission, promotion and conservative legacy annotations |
| `src/formula_ultimate/experiments/discovery_ledger.py` | Single-writer durable JSONL events, semantic replay, costs, recovery, selection and current scientific eligibility |
| `src/formula_ultimate/experiments/discovery_audit.py` | Score-independent stratified sampling, descriptive error accounting and numerical replay comparison |
| `scripts/experiments/run_discovery_contract.py` | Explicitly synthetic mixed-ledger execution and deterministic report comparison |
| `config/experiments/discovery_contract_fixture_v1.json` | Complete software fixture registration; all numerical values are test values |

Run from the repository root with an installed `formula_ultimate` package or the existing source import configuration:

```powershell
python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/run_a
python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/run_b --replay-reference artifacts/work098/run_a/result.json
python -m unittest tests.test_discovery_contract -v
```

Each runner output directory must be new or empty. Existing evidence is never deleted or overwritten to make replay pass. Outputs are `ledger.jsonl` and `result.json`; the report includes the registration, event-head, state and implementation hashes. These are software fixtures, including any `candidate_survivor` or `promotion_ready` events.

## 2. Frozen registration and trusted provenance

`freeze(body)` returns `{body, registration_sha256}`; `validate_registration(envelope, expected_sha256=...)` checks exact fields, finite values, identity and policy constraints. Every ledger row pins the registration hash. Changing a threshold and recomputing the registration hash creates a new registration; an existing ledger rejects it.

Required declarations cover hypotheses/alternatives, independent variables/controls, task/energy/material/representation/operator/environment identities, matched treatments and seeds, disjoint calibration/training/holdout datasets, evaluator coverage, physical/process/holdout/replay/safety/independent gates, intended promotion use, statistical plan, budget partitions, audit design and execution policy. The paired-seed sample size must match the seed list. Study effect sizes, error limits, test names, interval plans and stopping criteria cannot be missing. V1 validates statistical declarations; it does not perform power analysis or execute a scientific hypothesis test.

Each gate pins domain, fidelity and `fidelity_rank`, evaluator, metric, SI unit or dimensionless `1`, comparator, threshold, minimum refinement count, numerical error limit and evidence type. Field gates require at least three increasing refinement levels. An independent promotion evaluator needs a different implementation identity, a registered source evaluator and a higher declared fidelity rank than that source's survivor evidence. Rank ordering expresses a registered assumption; stronger physical fidelity still requires validation outside this software contract.

Registrations and evaluator coverage records are trusted study inputs. Hashes detect substitution relative to those inputs; they do not authenticate a dishonest source or prove that a solver ran. The current config explicitly registers only `software_fixture` evaluators. An admitted producer must independently establish its registry and validation-artifact provenance, geometry applicability and field evidence before using the `admitted_simulation` class. No such producer is installed by Work 098. Known synthetic flags, class mismatches and missing declared field execution cannot be relabeled as admitted science.

## 3. Candidate and evidence identity

Candidate declarations contain an executable-genotype declaration, its hash, parents, mutation trace, representation, treatment, seed, partition and dataset. This contract validates the declaration and provenance; execution of that genotype belongs to Work 099. A declaration is limited to `1048576` serialized UTF-8 bytes in V1.

The causal context is:

```text
candidate_id
genotype_sha256
geometry_sha256
material_sha256
boundary_sha256
controller_sha256
environment_sha256
task_sha256
registration_sha256
```

Geometry and boundary hashes may initially be unknown. The first measured-geometry/boundary event seals each identity once. All other context fields remain exact. Later design changes require a new descendant. Evidence transfer is deliberately limited to exact contexts in V1; numerical applicability envelopes and cross-candidate transfer are not implemented.

A scoped evaluation artifact contains a hashed body with producer/validation/class identities, context hash, gate, dataset, metric/unit/value, convergence, error, refinement levels, evidence type and diagnostic details. Outcome labels are checked against the registered threshold, not trusted merely because the producer wrote `physically_feasible`. Artifact hash, class, context, unit, producer, coverage or convergence mismatches reject admission.

## 4. Outcomes and integration permission

Separate fields preserve representation, boundary, physics by gate/domain/fidelity, manufacturing by process gate, and promotion by registered use. Initial promotion is explicitly `not_ready`. A physical pass at one fidelity may coexist with unresolved higher fidelity and a failed manufacturing process. Historical observations stay in the event ledger and per-candidate outcome history even when later attempts update a current view.

`physically_failed` requires a converged, in-scope result crossing its threshold. Timeout, divergence, mesh failure, unsupported physics and lost output remain separately reasoned unresolved outcomes. Budget exhaustion before invocation is recorded by `defer` as `not_evaluated` with execution disposition `budget_exhausted`. A rejected metadata submission raises `DiscoveryViolation`; the caller can retain its source digest and reason in a `quarantine` event with disposition `protocol_invalid`. Invalid physics payload details may be retained in settlement diagnostics without being admitted as a physical result.

`exploration_permission` requires measured geometry, resolved typed boundary identity, a named scope, declared missing domains and explicit approximations. It grants eligibility to attempt a bounded coupled evaluation, never a physical pass. It does not run an assembly solver or invent missing coefficients.

`promotion_decision` requires all registered survivor gates for `candidate_survivor`, and additional safety/independent gates for `promotion_ready`. Gate results must use the current context and registered use. Exploratory-class results cannot promote. Fixture promotion has `scientific_survivor: false` and `physical_validation: false`. Any new outcome resets the current promotion view to `not_ready`; historical decisions remain in the ledger.

Use `scientific_summary(state)` for current campaign counts. Pending work, unknown recovered actual costs or a stopped campaign block current scientific counts, including previously recorded decisions. Reading an old promotion event alone is not a final campaign-admission decision.

## 5. Events, resource accounting and recovery

| Event | Effect |
| --- | --- |
| `candidate` | Register immutable lineage and charge one proposal in the treatment/seed exploration pool |
| `reserve` | Check and reserve one operation's full resource vector; pin scope/context and optional retry/cache/selection source |
| `start` | Durably record that execution is about to begin; required before a result can settle |
| `settle` | Validate the result; retain observed costs and debit the registered charge exactly once |
| `recover` | Close a pending operation under the registered lost-output policy; never invent the missing result |
| `defer` | Prove that the requested allocation exceeds the remaining pool; record uninvoked evaluation explicitly |
| `select` | Replay deterministic audit, quality or bounded failed/unresolved selection from current training evidence |
| `explore` / `promote` | Record separate exploratory eligibility and evidence-based promotion decisions |
| `quarantine` | Retain a corrupt input's digest/reason without inventing a physical outcome |

Resources are `proposals`, `attempts`, `geometry_executions`, `cad_calls`, `mesh_attempts`, `elements`, `dof`, `solver_iterations`, `cpu_s`, `gpu_s`, `wall_s`, `peak_memory_bytes` and `cache_hits`. All counters are explicit; time is seconds and memory is bytes. Peak memory uses a maximum, not a sum. `observed_cost` represents producer measurements; `charged` represents the registered comparison debit. This library does not itself measure an external process.

Each treatment/seed has separate `exploration`, `audit`, `quality`, `stepping_stone` and `finalist` pools with the same configured resource opportunity. No automatic budget transfer is allowed. The primary resource is `cpu_s` or `wall_s`; every other vector limit is enforced too. Audit pools must have nonzero opportunity. One operation may be pending globally: this is a serial scheduler, not a distributed executor.

Retries require their own attempt identity, charge and link to the latest unresolved attempt in the same context/scope. They cannot evade the retry cap by reusing an older parent. A changed design is a descendant, not a successful retry of a physically failed parent. Repeated evaluation of an unchanged result requires the explicit cache path in this bounded V1 implementation; new refinement uses a separately registered gate/fidelity. General stochastic replication is not implemented.

The only V1 cache policy is `same_context_full_charge`. A cache hit must reuse exactly the source result and reserve at least its registered charge. The debit is the elementwise maximum of source charge and current observed costs, with one cache-hit count; actual cheap lookup time is still reported separately. Cross-candidate, cross-treatment and externally precomputed shared caches are not admitted by this implementation.

If actual cost exceeds the reservation or pool, record the full value and stop further campaign operations. No clamp hides the excess. There is no external process watchdog: a producer must bound/stop its solver and supply measurements. A reservation is not proof that real execution stayed below it.

Recovery before `start` charges one attempt and leaves physics uninvoked. Recovery after `start` debits the reservation, marks the actual cost unknown, records `lost_output`, and blocks scientific accounting completeness. It may support further explicitly non-admitted diagnosis. The reservation debit is not asserted to be an upper bound on actual lost work. No recovery silently reruns or duplicates a physical operation.

## 6. Replay, archives and holdouts

`DiscoveryLedger(path, registration, expected_head=...)` replays both the JSONL hash chain and every semantic event rule. Appends validate before writing, flush and call `fsync`. An exclusive lock file prevents simultaneous writers; an existing stale lock is not removed automatically. Inspect the writer/process and preserve evidence before explicit recovery. Truncated, malformed, duplicate-key or hash-inconsistent rows fail closed.

Hash chains alone cannot detect an adversary rewriting all hashes or deleting complete tail rows. A separately trusted `expected_head` detects rollback/substitution on reopen. Without that checkpoint, only internal chain and semantic consistency are established. A partial tail is not silently repaired. Hashes provide no signature or authenticity claim.

Exact decision replay reconstructs state, cost, selection and promotion from the same events. `compare_execution` separately checks pinned registration/evaluator/context/tolerance identities and per-field absolute/relative tolerances; it reports both timings and never claims bitwise equality. This comparison helper does not launch solvers.

Quality selection uses the declared proxy direction with deterministic candidate-ID ties, separately for each treatment/seed. Stepping-stone selection gives a bounded opportunity to failed or unresolved candidates, including unscored unresolved entries. Neither implements the Work 099 QD archive. Once a candidate receives a holdout-gate result it cannot feed a new training descendant or a later selection. Disjoint dataset registration prevents direct partition overlap; provenance of external learning remains the producer's responsibility.

## 7. Proxy audit meaning

Audit sampling groups by treatment, seed and representation, ranks candidate IDs with a seeded hash, and does not use proxy score in the ranking. Every selected record retains stratum population/sample sizes and its inclusion probability. Input order and changed proxy scores cannot change the selected identities for the same population/seed.

Ledger audit reports require a higher-ranked comparable physical gate in the same domain, metric and unit. Unknown reference outcomes remain unknown. Reports give reference-positive/reference-negative denominators, false-negative/false-positive counts and rates among known references **within each stratum**, together with sample identification bounds for missing reference labels. There is no biased pooled rate and no claim that these bounds are population confidence intervals. If reference evidence is entirely missing, the status is `not_estimable`; an unknown proxy label also blocks a fabricated rate.

Population inference, power and registered confidence procedures must be implemented for a later admitted experiment. The current audit establishes deterministic sampling and correct descriptive accounting only.

## 8. Acceptance mapping and preserved baselines

| Governing acceptance case | Implemented verification in `tests/test_discovery_contract.py` |
| --- | --- |
| 1 — Orthogonal states | Coexisting physics/process/fidelity outcomes, sealed identities, explicit `not_ready`, mixed runner promotion events |
| 2 — Distinct failures | Budget deferral, unstarted/started recovery, timeout/unsupported reasons, threshold-label rejection and quarantine |
| 3 — Exploratory versus promotion | Incomplete exploratory permission; missing each survivor gate; no unbound assembly or unsupported use |
| 4 — Evidence identity | Every causal field, unit, producer, class, refinement, field/scalar and artifact mismatch |
| 5 — Learning without rewriting | Immutable parents, new mutation trace, holdout/cross-treatment ancestry rejection and no repaired physical-failure retry |
| 6 — Resource integrity | Serial reservation, once-only settlement, retries, full-charge cache, peak memory, overshoot, per-pool opportunity and explicit lost costs |
| 7 — Two replay meanings | Identical runner outputs, reopened ledger, trusted checkpoints, truncated/tampered inputs and numerical tolerances |
| 8 — Audit integrity | Score/order invariance, inclusion probabilities, correct denominators, unknown bounds and stronger reference fidelity |
| 9 — Registration and claim classes | Complete immutable registration, fixture-class isolation, statistical/budget inputs and current scientific-count blocking |
| 10 — Legacy behavior | Conservative `legacy_annotation` for Work 095/097 plus unchanged existing benchmark regression suites |

Work 095 `accepted`/`repaired`/`rejected` labels remain synthetic pre-performance annotations, not measured manufacturing or physical admission. Work 097 `passed` remains scoped scalar benchmark evidence; its explicit solver-divergence `invalid` maps to numerical uncertainty. No legacy output is promoted automatically and neither legacy implementation was modified.

## 9. Limits and next work

This implementation is a contract and executable software fixture, with trusted producer inputs, exact-context applicability, serial scheduling and conservative cache/recovery policies. It does not validate arbitrary geometry, evaluate real manufacturability, execute CAD/field solvers, discover technology, prove fairness of a real search distribution, or authenticate dishonest scientific artifacts.

Work 099 must provide executable numerical morphology, evolving component/interfaces and bounded QD archives. Work 100 must supply independently validated local/coupled evaluators and actual preregistered contrasts; Work 101 must demonstrate full-vehicle evidence and stronger promotion. All require their own work logs, tests and commits. See [Work 098 result](../work_logs/2026-09-06_098_discovery-state-evidence-fairness-result.md) for exact validation evidence and remaining limitations.
