# Work 100 Plan: Functional and Coupled Discovery Trial V1

Thai companion: `2026-09-06_100_functional-coupled-discovery-trial-plan.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Objective and starting evidence

Implement the bounded Work 100 trial required by `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md`, starting from clean Work 099 commit `e6f3196`. Work 099 executes numerical swept-solid morphology, measures CAD geometry and preserves architecture/archive lineage, but explicitly has no field solver. Work 100 will add a geometry-derived coupled axial-load/thermal-network evaluator, a distinct closed-form reference implementation, preregistered treatment contrasts, proxy audit, bounded vehicle-feedback metrics and Work 098 ledger admission.

The declared scope is a terminal-to-terminal multifunctional load/heat path, not a complete racing vehicle. A `candidate_survivor` result will mean only that a candidate passed this registered low-fidelity simulated subsystem task, process-envelope check, untouched holdout load case and replay gate. It will not mean race superiority, technology novelty, complete-vehicle feasibility, independent promotion or physical validation.

## Scope and planned files

- `src/formula_ultimate/physics/functional_network_solver.py`: geometry-derived variable-radius axial and thermal conductance assembly; multi-refinement field solve; reactions, conservation/energy residuals, stresses, temperatures, margins, failure locations, numerical applicability and bounded component-to-vehicle burden feedback.
- `src/formula_ultimate/physics/functional_network_reference.py`: separate exact linear-radius resistance integration and network solution for cross-method validation; no reuse of numerical subdivision results.
- `src/formula_ultimate/experiments/functional_discovery.py`: strict trial-config validation, five registered treatment builders, task/material/process binding, outcome/admission artifact construction and deterministic analysis.
- `config/experiments/functional_discovery_trial_v1.json`: frozen physical assumptions in SI, seeds, treatments, task loads, training/holdout conditions, material model, refinement/error/physics/process thresholds, analysis and claim boundary.
- `config/experiments/functional_discovery_registration_v1.json`: final Work 098 `admitted_simulation` registration, created only after implementation/validation identities are known and before the first admitted observation.
- `scripts/experiments/run_functional_discovery.py`: execute CAD, task-derived proxy/refined/holdout fields, ledger costs, score-independent audits, process/replay gates, survivor decision, archives/results and cross-run comparison.
- `tests/test_functional_discovery.py`: analytical chain/parallel checks, conservation and energy, refinement/reference agreement, task/boundary/material tampering, physical failure versus numerical failure, treatment determinism, process and promotion/admission negatives.
- `docs/contracts/FUNCTIONAL_COUPLED_DISCOVERY_TRIAL_V1.md` and `.th.md`: equations, assumptions, registration, evidence, commands, outcomes and limitations.
- This bilingual plan and matching bilingual result. Generated calibration/fixture/admitted evidence remains ignored under `artifacts/work100/`.

## Experiment variables, controls and falsification

- Independent variable: treatment among `FIXED_TOPOLOGY`, `RANDOM_CONTROL`, `GRAPH_ONLY`, `MORPHOLOGY_ONLY` and `JOINT_MORPHOLOGY_CONTROLLER`, paired across registered seeds. The controller gene remains observable; no credit is assigned unless the declared task model gives it a causal path.
- Dependent evidence: coupled utilization, maximum axial stress/displacement/temperature, nodal fields, edge forces/heat flux, recovered reactions, force/heat/energy residuals, refinement/reference disagreement, process-envelope result, CAD/mass burden, survivor count, proxy false-negative/positive accounting and compute.
- Controls: external terminal ancestry/roles, load and heat histories, material law, process envelope, evaluator identities, numerical levels, training/holdout split, optimization opportunity, thresholds, archive rules, random streams, hardware/concurrency declaration and total treatment/seed budgets.
- Preferred hypothesis: generation-first treatments can produce at least one previously undeclared multifunctional candidate that survives the registered subsystem task without conservation, numerical, process, holdout or replay violations.
- Competing explanations: apparent gain comes from radius/mass advantage, task/controller loophole, singular network, proxy error, unequal compute, CAD/field identity mismatch or post-result threshold choice.
- Falsification: sever paths and perturb boundary/material/evaluator identities; check analytical series/parallel networks; require independently recovered reactions and energy; promote score-independent proxy samples; preserve failures/unresolved results; do not alter frozen thresholds after admitted outcomes.

## Registration and observation boundary

Implementation and validation hashes will be computed after code/tests exist. Before any admitted run, the final registration will pin those hashes plus the task, material, representation, operator and environment identities. Development tests and any threshold calibration are software/calibration evidence only and must not be relabeled as untouched training/holdout evidence. Once the admitted registration is frozen, numerical thresholds, paired seeds, treatment rules and holdout conditions cannot change in this work item.

The primary numerical evaluator uses increasing subdivision levels and reports full scalar-network fields. The reference evaluator uses exact resistance integration for linear radius variation; both may use the same linear-algebra library, so this is cross-method corroboration, not an independent software stack or physical experiment. Stronger independent promotion remains Work 101.

## Validation and success criteria

1. Run `python -m unittest tests.test_functional_discovery -v`; validate equations against closed-form series/parallel cases, fields/reactions/residuals, three refinements, exact-reference disagreement, treatment replay, process envelope, identity binding and negative admission.
2. Run targeted regressions for Works 098–100 and morphology/topology/geometry behavior.
3. Freeze and validate the final `admitted_simulation` registration before executing `artifacts/work100/run_a`; record its SHA-256 and confirm implementation/validation source hashes match the executing files.
4. Execute admitted runs A and B independently with the pinned CadQuery environment. Compare deterministic CAD/field/selection/survivor evidence under registered tolerances while reporting timing separately. Reopen each ledger at its trusted head.
5. Run `python -m compileall -q src scripts tests` and `python -m unittest discover -s tests -q` with durable exit evidence.
6. Verify bilingual files/local links/technical tokens, run `git diff --check`, stage only declared files, inspect exact cached scope, run `git diff --cached --check`, commit immediately and verify the commit hash.

Success requires at least one previously undeclared candidate to pass all preregistered subsystem survivor gates with causal geometry/field evidence and admissible accounting. If none survives, Work 100 may still complete as a negative trial only if the implementation, registration, falsification and evidence gates pass without weakening criteria. A failed validation or commit leaves the work `In progress` or `Stopped` with the exact blocker.

## Risks, controls and explicit non-goals

Risks include calling a scalar network full 3D mechanics, using synthetic material assumptions as real validation, post-result threshold tuning, singular/disconnected graphs, proxy exploitation, controller energy creation, hidden CAD repair and an admitted label escaping its scope. Controls are explicit one-dimensional axial/conduction equations, declared material-model scope, frozen registration, terminal ancestry, conservation/energy residuals, exact-reference comparison, score-independent audit, immutable ledger identities, no hidden repair and narrow survivor wording.

Non-goals: full 3D elasticity/contact/CFD, nonlinear failure, fatigue/fracture, arbitrary material distribution, manufacturing proof, race completion/time, optimized conventional vehicle baselines, whole-vehicle energy/race integration, `promotion_ready`, real-world novelty, physical validation, distributed scheduling, external publication or push. Work 101 remains responsible for whole-vehicle co-design and stronger evidence promotion.

## Prospective execution addendum after frozen V1 stopped

Registration V1 (`aa5012d3b0a85b9f6c42b1ede5561681713cb9c9832577f6d2bf88e09d96a871`) was frozen before its first admitted execution. That execution stopped after proxy and refined evaluations because eight of ten proxy results were honestly `numerically_unresolved` under the frozen `0.005` refinement-change limit, while the Work 098 proxy-audit reporter requires a Boolean proxy label. No survivor, contrast or holdout outcome was produced. The partial ledger remains under `artifacts/work100/run_a/` and will not be resumed or relabeled.

Before another admitted observation, create a distinct V2 registration and fresh output directory. V2 must preserve every physical threshold, task, seed, treatment, audit selection rule and claim boundary from V1. Its only prospective execution change is to emit a deterministic `not_estimable_due_to_unresolved_proxy_labels` audit result when selected proxy labels are unresolved, including known/unresolved counts instead of inventing FNR/FPR. V2 receives new runner/test/operator/registration hashes and does not reuse V1 evidence.

Final portability control: because evaluator identities use raw file SHA-256 and this Windows checkout enables `core.autocrlf`, add a path-scoped `.gitattributes` rule for the byte-addressed Work 099/100 sources and Work 100 records. This prevents a clean checkout from converting their committed LF bytes to CRLF and falsely invalidating the frozen registration.
