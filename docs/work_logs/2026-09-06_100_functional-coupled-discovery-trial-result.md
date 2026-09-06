# Work 100 Result: Functional and Coupled Discovery Trial V1

Thai companion: `2026-09-06_100_functional-coupled-discovery-trial-result.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Outcome

Work 100 implemented and executed a bounded geometry-derived scalar axial/thermal subsystem evaluator on the Work 099 executable morphology. The primary midpoint-subdivision solver emits nodal fields, segment flows, reactions, equilibrium/energy residuals, stresses, temperatures, utilization, geometry-derived mass and vehicle-burden feedback. A separate exact linear-radius resistance implementation supplies cross-method numerical corroboration. Task terminal ancestry, material identity, environment, source hashes, budgets, partitions and claim limits are frozen and checked before execution.

Registration V2 SHA-256 is `2c3aaa21ffb6ed36da532493c82c6e1f0195b13990180dc5d055c75fb47bdd45`. Independent admitted runs A and B returned exit `0` and identical deterministic evidence SHA-256 `652ba7d9db9d76ed841d5b2c24af421075cc2d266a9098bc065fe4a8ac45da61`. Both trusted ledgers reopened exactly. All ten candidates passed refined training, computational process-envelope, untouched holdout and decision-replay gates, producing ten scientifically accounted but narrowly scoped `candidate_survivor` records. At least one graph/joint signature differed from the fixed signature, satisfying the preregistered survivor condition.

This is not evidence of functional superiority. The graph-only and joint mean difference from fixed was about `-1.51e-14`; the added branch carried essentially zero source-to-sink flow. Morphology-only paired differences opposed one another with mean `-0.0031219`; random-control mean difference was `+0.0159315`. With `n = 2`, analysis remains descriptive only. The result establishes executable distinct architectures and bounded simulated feasibility, not a new useful load path, whole-vehicle feasibility, race advantage, technology novelty, manufacturing proof, `promotion_ready` status or physical validation.

## Frozen V1 stop and V2 handling

Registration V1 SHA-256 `aa5012d3b0a85b9f6c42b1ede5561681713cb9c9832577f6d2bf88e09d96a871` was frozen before observation. Its run stopped after proxy/refined evaluation because eight proxy labels were `numerically_unresolved` under the frozen `0.005` refinement-change gate and the inherited Work 098 reporter required Boolean proxy labels. No V1 holdout, survivor or contrast result was produced. The ledger was not resumed and no threshold was widened.

V2 kept every scientific threshold, task, treatment, seed, selection rule and claim boundary. Before observation it added only a deterministic report for the unestimable-label case. The V2 audit reports `proxy_boolean_count = 2`, `proxy_unresolved_count = 8`, ten refined-feasible labels and `false_negative_rate = null`, `false_positive_rate = null`. Unknown labels were not relabeled.

## Files changed

- Added the primary and reference solvers under `src/formula_ultimate/physics/`.
- Added the trial implementation and runner under `src/formula_ultimate/experiments/` and `scripts/experiments/`.
- Added the frozen trial configuration and V1/V2 registrations under `config/experiments/`.
- Added `tests/test_functional_discovery.py` with 14 analytical, conservation, refinement, registration, binding, failure, treatment and audit tests.
- Added the bilingual contract and this bilingual plan/result evidence.
- Generated ignored evidence under `artifacts/work100/`: stopped `run_a`, admitted `run_v2_a`, and replay `run_v2_b`.

## Exact validation evidence

1. `python -m unittest tests.test_functional_discovery -q`: exit `0`; `Ran 14 tests`; `OK`.
2. CadQuery targeted Works 098-100/topology/geometry regression: exit `0`; `Ran 131 tests in 27.745s`; `OK`.
3. V2 run A: exit `0`; `candidate_count = 10`; `survivor_count = 10`; audit `not_estimable_due_to_unresolved_proxy_labels`; deterministic SHA shown above.
4. V2 run B with `--replay-reference artifacts/work100/run_v2_a/result.json`: exit `0`; the same counts and exact deterministic SHA.
5. `python -m compileall -q src scripts tests`: exit `0`.
6. `python -m unittest discover -s tests -q`: exit `0`; `Ran 785 tests in 421.299s`; `OK (skipped=8)`.
7. `git diff --check`: exit `0`; no output.

## Decisions, limitations and follow-up

- Numerical failures remain unresolved, never silently converted into physical failure.
- The exact reference shares equations, genotype and NumPy; independent/safety promotion gates remain unevaluated, so no candidate is `promotion_ready`.
- CAD establishes executable geometry identity, while this scalar gene-derived network is not a volumetric finite-element solve.
- The process check is only a declared envelope, not manufacturing proof.
- Timing is diagnostic. Peak native memory is not measured; zero is recorded rather than claiming a measured bound.
- A path-scoped `.gitattributes` keeps every raw-byte-hashed source at LF under Windows `core.autocrlf=true`, preventing false identity drift after checkout.
- Work 101 should require task-relevant nonzero-flow topology changes, stronger whole-vehicle coupling, powered comparisons and independent/safety evidence.

The validated commit hash is reported in the final handoff after the exact-scope commit succeeds.
