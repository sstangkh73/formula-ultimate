# Design Search Agent v0: Research and Implementation Plan

Thai companion: `DESIGN_SEARCH_AGENT_V0_PLAN.th.md`

Report date: 2026-08-29

Status: Planned, not implemented

Evidence baseline: commit `3398459`, Research Experiment Protocol v1, and the
completed `FU-C0001` geometry-to-Level-0 pipeline run

## Executive Decision

Formula Ultimate should use a **repository-owned deterministic search agent**,
`DesignSearchAgentV0`, for the first design campaign. It should not use an LLM
as the numerical optimizer and should not give any agent authority to edit its
own evaluator, tolerances, energy limits, load cases, budget, or promotion
rules.

Codex remains the **Research Orchestrator**: it helps formulate hypotheses,
creates reviewed protocols, starts bounded runs, investigates failures, and
writes falsification reviews. CadQuery, STEP, FreeCAD, Level 0, and later
independent solvers remain non-agentic evaluators. Human approval remains the
gate for changing research questions, promoting expensive candidates, or
making external claims.

The first meaningful design task should be a **loaded interface plate** rather
than a whole vehicle. This task adds declared mechanical function to the proven
CAD route while remaining small enough to falsify and debug. The existing
`FU-C0001` remains pipeline evidence only and is not a performance baseline.

## 1. Research Question

Within one fixed set of interfaces, loads, material assumptions, geometry
limits, evidence gates, and candidate-evaluation budget, can a seeded
evolutionary search find lower-mass feasible interface-plate geometries more
reliably than matched random and fixed-grid search treatments?

This asks whether the search procedure adds value inside a deliberately narrow
functional boundary. It does not ask whether an agent can invent a complete
vehicle or a new technology.

### Preferred hypothesis H1

Across predeclared seeds and equal evaluation budgets,
`DesignSearchAgentV0` produces a lower median best-feasible mass than both
matched baselines while retaining the same geometry, interface, structural,
and replay gates.

### H0

The evolutionary treatment does not outperform the better matched baseline by
the predeclared practical threshold, or any apparent advantage disappears on
holdout load cases or independent re-evaluation.

### Alternative explanations to test

- The grammar encodes the winning family instead of the agent discovering it.
- Invalid candidates are omitted and give one treatment an unfair budget.
- The result comes from unequal wall time, solver calls, retries, or seed use.
- The Level-0 structural model rewards thin or disconnected geometry that a
  stronger solver rejects.
- STEP healing, meshing behavior, or numerical tolerance changes candidate
  ordering.
- Mass improvement is only a parameter effect and not a useful geometric
  discovery.

## 2. Agent and Tool Responsibilities

| Role | System | May do | Must not do |
|---|---|---|---|
| Research Orchestrator | Codex with human review | Draft protocol, inspect evidence, launch bounded campaigns, diagnose failures, write review | Change a completed run's preregistration or declare discovery from Level 0 |
| Design search | `DesignSearchAgentV0` seeded Python process | Propose candidate declarations, update its internal population from admitted result records | Edit evaluator/config/budget/tolerances, repair artifacts, execute arbitrary CAD code, or suppress failures |
| Geometry generator | constrained CadQuery adapter | Build only grammar-admitted geometry and export STEP | Choose fitness, alter loads, or claim feasibility |
| Geometry evaluator | FreeCAD adapter | Import the exact STEP hash and report topology/mass properties | Repair geometry silently or replace missing evidence |
| Functional evaluator | Level-0 structural contract to be implemented | Evaluate declared load cases and expose residuals/failures | Mutate geometry or hide non-convergence |
| Downstream evaluator | existing coupled Level 0 | Report mass-dependent vehicle/race consequences | Treat component mass alone as proof of race advantage |
| Promotion evaluator | independent FEA/mesh route, later work | Re-evaluate selected candidates and check convergence/holdouts | Train or tune the search treatment on holdout results |

The deterministic evaluator owns pass/fail. The agent receives structured
records but never a mutable evaluator handle.

## 3. First Functional Design Task

Working task ID: `loaded_interface_plate_v1`

The component transfers declared bearing loads from one bolt-hole pair to a
second bolt-hole pair inside a bounded envelope. The task is a synthetic
research fixture, not a certified vehicle component.

### Immutable interfaces and controls

- four cylindrical bolt-interface regions with fixed centres and diameter;
- left interface pair: declared support boundary;
- right interface pair: declared distributed bearing-load boundary;
- fixed maximum outer envelope and thickness bounds in SI units;
- protected interface ligaments and a declared central keep-out region;
- one versioned material record with density, elastic constants, allowable
  policy, provenance, and uncertainty;
- identical training load cases, holdout load cases, mesh policy, solver
  tolerances, and failure policy for every treatment;
- no geometry or material outside the declared envelope/library;
- no silent contact, thickness, or material correction.

Numerical loads and allowables must be sourced or explicitly labelled
synthetic before the implementation experiment. They are not specified by this
planning report because choosing them requires a separate load/interface
work item and validation review.

### Searchable design variables for v0

- bounded outer contour control points or admitted profile parameters;
- thickness within declared manufacturing and solver bounds;
- number, position, and size of admitted relief features outside protected
  interfaces and keep-outs;
- web widths and fillet radii within versioned minimum-feature rules.

Bolt locations, load locations, material identity, envelope, keep-outs,
failure thresholds, solver settings, and budget are not searchable.

The v0 grammar is intentionally fixed-topology or narrowly variable-topology.
This isolates search/evaluator errors. It is not evidence about open-ended
vehicle topology. Later grammars should express functional interfaces rather
than require conventional component shapes.

## 4. Candidate Evidence Contract

Each immutable candidate declaration must contain at least:

```text
protocol_id
campaign_id
treatment_id
candidate_id
parent_candidate_ids
generation_index
grammar_version
operator_id
seed and RNG state/fingerprint
geometry parameters in SI units
material_id
interface/load_case_set IDs
evaluation-budget counters
source/config/commit identity
```

Each attempted evaluation consumes budget, including grammar rejection, CAD
failure, STEP failure, FreeCAD failure, meshing failure, numerical failure, and
constraint failure. Failed candidates remain append-only observations.

The output record must retain:

- exact stage and failure code;
- CAD validity, solid count, bounds, volume, centre of mass, and inertia when
  available;
- STEP hash and generator/evaluator source hashes;
- interface and keep-out residuals;
- structural outputs, solver residuals, mesh evidence, and convergence status;
- mass, feasible/infeasible status, and objective values;
- wall time, CPU time when measurable, peak memory when measurable, and solver
  call count;
- downstream Level-0 outputs as evidence, not as a substitute for structural
  function;
- supporting/contradicting/missing evidence and claim level.

## 5. Search Algorithm v0

Use a seeded `(mu + lambda)` evolutionary strategy implemented in ordinary
Python with deterministic selection and serialization. The first version does
not need an LLM, neural surrogate, novelty model, or self-modifying code.

Proposed mechanics:

1. Initialize a population from grammar-valid declarations using one recorded
   RNG stream.
2. Evaluate every attempted candidate once through the same bounded pipeline.
3. Rank feasible candidates lexicographically: all hard gates pass first, then
   lower mass. Preserve diversity only as a secondary tie-break or separately
   reported metric.
4. Select parents deterministically from admitted records.
5. Apply versioned parameter and feature mutation operators.
6. Do not retry failed geometry for free. Any retry is a new candidate and
   consumes budget.
7. Checkpoint population, RNG state, budget ledger, and artifact references
   after every generation.
8. Replay a completed campaign from its manifest and compare the semantic
   result sequence exactly or within declared numerical tolerances.

Mass must not be optimized until a structural feasibility contract exists.
Using the current mass-only `FU-C0001` Level-0 path as fitness would reward
removing material without proving that the component transfers load.

## 6. Experimental Treatments and Fair Budget

The scientific campaign should compare three treatments on the same grammar:

| Treatment | Method | Purpose |
|---|---|---|
| `GRID` | deterministic space-filling/fixed grid over admitted parameters | transparent tuned fixed-search baseline |
| `RANDOM` | seeded uniform or explicitly declared prior sampling | unguided search baseline |
| `EVOLUTION` | `DesignSearchAgentV0` `(mu + lambda)` search | tested agent treatment |

Initial development smoke runs may use `8–16` evaluations and one seed, but
they support software debugging only. The preregistered comparison should start
with the following provisional budget and may change only in its own plan
before results are observed:

- `64` attempted candidates per treatment per seed;
- `10` predeclared independent seeds;
- the same grammar, initialization domain, candidate directory limits, CAD and
  solver versions, training loads, holdouts, and promotion gates;
- no free retries; every attempted evaluation counts;
- report both evaluation count and measured compute because solver failures can
  change cost;
- cap per-candidate wall time and memory identically;
- tune baseline operators before freezing the campaign, without reading
  holdout results.

This is `1,920` attempted evaluations across the three treatments. A pilot must
measure real wall time and failure rate before confirming that budget.

## 7. Variables, Metrics, and Decision Rules

### Independent variable

- search treatment: `GRID`, `RANDOM`, or `EVOLUTION`

### Controlled variables

- grammar and candidate domain;
- interfaces, material, envelope, keep-outs, loads, constraints, and units;
- evaluator versions, mesh policy, tolerances, failure policy, and promotion
  rules;
- candidate-attempt budget, seeds, machine class, and resource limits.

### Dependent variables

- best feasible mass at each attempted-evaluation count;
- feasible-candidate rate and failure-code distribution;
- evaluations and wall time to reach predeclared mass targets;
- final best feasible mass per seed;
- holdout survival and independent-evaluator promotion survival;
- geometry/interface/structural residuals;
- diversity after removing parameter-identical and geometry-equivalent results;
- deterministic replay agreement.

### Primary metric

Median final best-feasible mass across seeds, compared pairwise at exactly 64
attempts. Lower is better only when every hard geometry, interface, structural,
numerical, and evidence gate passes.

### Provisional success criterion

Before the campaign, freeze a practical-effect threshold. The initial proposal
is that `EVOLUTION` must reduce median best-feasible mass by at least `2%`
relative to the better of `GRID` and `RANDOM`, with a paired bootstrap `95%`
confidence interval for improvement remaining above `0%`, while its selected
candidates pass all holdout cases and independent promotion checks.

If the criterion is not met, report H1 as unsupported. Do not relabel a visual
difference, one lucky seed, or a Level-0-only winner as success.

### Failure criteria

- evaluator or budget mutation by the search process;
- missing/duplicate candidate identity or incomplete ledger;
- non-deterministic replay outside declared tolerances;
- unequal attempts, seeds, load cases, solver settings, or promotion rules;
- systematic hidden retry or loss of invalid candidates;
- no feasible candidate in a treatment/seed;
- winner failure on a preregistered holdout or independent solver;
- mesh non-convergence, invalid geometry, interface violation, or numerical
  residual beyond tolerance;
- evidence that grammar bias or an evaluator exploit explains the advantage.

## 8. Falsification Plan

The campaign should try to defeat the preferred result through:

1. **Replay:** reproduce candidate order, ancestry, budget ledger, and admitted
   metrics from the same manifest.
2. **Operator ablation:** remove selection pressure or geometry-feature
   mutations while preserving budget.
3. **Grammar ablation:** compare a parameter-only grammar with the feature-
   mutation grammar under equal opportunity.
4. **Holdout loads:** evaluate promoted candidates on loads not used for search.
5. **Mesh/timestep refinement:** test candidate ordering under tighter numerical
   settings.
6. **Independent solver route:** re-evaluate selected candidates without using
   the search evaluator's cached outputs.
7. **Known alternative:** competitively tune the best simple solid/webbed
   baseline rather than comparing against an arbitrary default plate.
8. **Exploit audit:** inspect whether wins depend on minimum-feature boundaries,
   topology healing, tolerance edges, failure localization, or omitted physics.

The final review must record supporting evidence, contradicting evidence,
alternative explanations, missing evidence, and confidence.

## 9. Security and Authority Boundary

`DesignSearchAgentV0` should run as a narrow candidate-declaration process:

- write only inside a fresh candidate/campaign artifact root;
- use an allowlisted schema and operators rather than arbitrary generated
  Python;
- have no network access or project secrets;
- receive evaluator results as immutable records;
- have read-only access to frozen protocol/config hashes;
- have no Git, shell, evaluator-source, tolerance, load, or promotion mutation
  authority;
- stop on budget/resource exhaustion and preserve its checkpoint;
- require human approval before cloud tools, expensive solvers, publication,
  or claims beyond the registered level.

Codex may implement and operate the harness in reviewed work items, but the
scientific pass/fail decision must remain executable in deterministic code.

## 10. Implementation Roadmap

Each milestone should be a separate bilingual, validated, committed work item.

### Milestone 1 — Functional task and load contract

- version `loaded_interface_plate_v1` interfaces, keep-outs, material record,
  training/holdout loads, synthetic/source labels, and failure policy;
- add analytical fixtures and invalid cases;
- do not begin search until this contract is frozen.

Completion gate: all interface/load/unit/schema tests pass and no numerical
allowable is undocumented.

### Milestone 2 — Geometry grammar and independent measurement

- implement the constrained grammar and candidate manifests;
- export STEP and independently verify exact interfaces, bounds, volume, mass
  properties, protected regions, and topology in FreeCAD;
- record all rejections and no hidden repair.

Completion gate: controlled valid and invalid specimens traverse the evidence
route reproducibly.

### Milestone 3 — Structural Level-0 feasibility gate

- implement a conservative declared structural model or a project-owned
  solver adapter with loads, boundary conditions, mesh evidence, residuals, and
  convergence tests;
- test analytical references and deliberate failure fixtures;
- separate solver validity from physical pass/fail.

Completion gate: mass cannot improve fitness unless load transfer and all
structural/numerical gates pass.

### Milestone 4 — Search harness and budget ledger

- implement candidate IDs, ancestry, operators, RNG checkpoint, append-only
  result ledger, equal-budget enforcement, and structured failures;
- add `GRID`, `RANDOM`, and `EVOLUTION` treatments behind one evaluator API;
- run only smoke fixtures.

Completion gate: treatment replay and budget accounting are exact, including
failed candidates.

### Milestone 5 — Pilot and protocol freeze

- measure candidate wall time, memory, failure distribution, and feasible rate;
- tune resource caps and confirm or revise the provisional `64 x 10 x 3`
  campaign before observing holdout comparisons;
- freeze hypotheses, metrics, seeds, baseline tuning, and statistical rules.

Completion gate: a signed/versioned campaign manifest exists before the main
results are produced.

### Milestone 6 — Main campaign and falsification

- execute all treatments under matched opportunity;
- promote only preregistered selected candidates;
- run holdout, refinement, independent-solver, and ablation checks;
- report failures and contradictory evidence.

Completion gate: conclude only whether H1 is supported inside
`loaded_interface_plate_v1`; do not generalize to complete-vehicle discovery.

### Milestone 7 — Controlled scope expansion

Only after Milestone 6, consider progressively adding component selection,
typed connection mutation, variable topology, packaging, ground-contact
arrangement, and whole-vehicle co-design. Every expansion requires matched
baselines and stronger geometry-to-physics evidence.

## 11. Deliverables for the Future Implementation

The implemented system should eventually provide:

- versioned protocol, task, grammar, material, load, and campaign schemas;
- `DesignSearchAgentV0` with deterministic checkpoint/replay;
- one evaluator interface shared by all treatments;
- immutable candidate/result/budget ledgers;
- constrained CadQuery and FreeCAD adapters;
- structural Level-0 and independent-promotion adapters;
- unit, invariant, integration, numerical, replay, exploit, and negative tests;
- campaign summary tables and plots generated from admitted result records;
- bilingual plan/result reports with exact commands, hashes, commit, seeds,
  limitations, and claim level.

## 12. What This Report Does Not Establish

- `DesignSearchAgentV0` does not yet exist in code.
- No loaded-interface grammar, load case, structural solver, baseline campaign,
  or autonomous candidate has been run.
- The provisional budget and `2%` effect threshold are planning choices to be
  reviewed and frozen before the experiment, not observed results.
- `FU-C0001` proves only the geometry evidence route; it is not a structural
  baseline.
- Nothing here supports complete-vehicle feasibility, safety,
  manufacturability, race superiority, novelty, or discovery.

## Recommendation

Proceed next with **Milestone 1: Functional Task and Load Contract**. Do not
implement the evolutionary loop first. A search agent without a load-bearing
feasibility evaluator would optimize missing physics and produce persuasive but
scientifically empty geometry.
