# Work 030 Plan: Integration Falsification and Promotion Gate

Status: Completed

Thai companion: `2026-08-29_030_integration-falsification-promotion-gate-plan.th.md`

## Objective

Close the coupled Level-0 implementation queue with deliberate transaction/integration fault injection, bounded timestep-refinement evidence, explicit uncertainty and cross-model requirements, and a release/promotion decision that cannot label unsupported candidates as discoveries or real-circuit performers.

## Scope

- Define a strict, fingerprinted integration release-gate protocol.
- Inject missing adapter, version mismatch, duplicate residual, failed residual, undeclared output, and state-time regression faults into the v4 transaction.
- Require every declared fault to fail closed with no committed state.
- Execute the Work 029 analytical reference at multiple timesteps under otherwise identical reduced controls.
- Record pairwise time/energy sensitivity, finish residuals, budgets, and the analytical boundary; do not infer convergence order when the steady reference is exactly invariant.
- Define typed independent higher-fidelity evidence requirements for geometry/mass/inertia, surveyed circuit corridor, aero, structure/safety, thermal/reliability, and quantified uncertainty.
- Evaluate the completed Work 029 campaign through falsification, refinement, real-circuit, and cross-model gates.
- Produce a release review that may authorize gated Level-0 experimentation while blocking discovery, real-race, safety, manufacturability, and physical-validation claims.
- Record and resolve every discovered defect in a separate bilingual problem report.

## Planned Files

- `config/simulation/integration_promotion_gate_v1.json`
- `src/formula_ultimate/simulation/integration_release.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_integration_release.py`
- `scripts/validate_integration_release.py`
- `docs/simulation/INTEGRATION_FALSIFICATION_PROMOTION_GATE.md`
- `docs/simulation/INTEGRATION_FALSIFICATION_PROMOTION_GATE.th.md`
- Work 030 problem reports if required
- implementation queue, this plan, and matching bilingual result records

## Experiment Definition

- Independent variables: injected fault class and timestep `(2000, 1000, 500) s`.
- Dependent variables: failure code, rollback state, fault-detection completeness, finish time, primary energy, finish residual, refinement sensitivity, promotion status, missing evidence, and release status.
- Controls: architecture v4, transaction start state/signals, adapter versions and declared outputs, Work 029 family/opportunity, selected calibration/holdout profiles, seed `17`, energy/environment, timeout, and sufficiently high common step budget.
- Metrics: detected fault fraction, false-positive control status, committed-state absence on faults, maximum relative time/energy variation, all-residual pass, missing evidence coverage, and discovery-claim denial.
- Success criteria: control commits; all injected defects fail with the expected observable code and rollback; refinement samples finish under budget and meet declared tolerances; missing higher-fidelity evidence blocks promotion; a complete independent evidence fixture reaches only review eligibility, never automatic discovery.
- Failure criteria: any injected defect commits, control fails, timestep sensitivity exceeds tolerance without blocking, missing evidence is silently accepted, proxy evidence becomes real-circuit admission, or the software automatically declares discovery.
- Falsification attempt: omit adapter, corrupt version, duplicate evidence identity, fail a residual, emit undeclared signal, regress state time, provide divergent refinement samples, remove a required evidence type, mark evidence dependent/failed, and attempt proxy promotion.

## Validation

1. Focused Work 021/022/028/029/030 tests.
2. Entire repository test suite.
3. Standalone Work 030 validator including the full Work 029 campaign.
4. Python bytecode compilation.
5. `git diff --check` and `git diff --cached --check`.
6. Explicit staged-scope review before commit.

## Success Criteria

- Every declared integration fault is detected and rolled back.
- The refinement matrix is deterministic and records its limited interpretation.
- Current Level-0 proxy evidence is blocked from cross-model promotion for explicit reasons.
- Even a complete evidence fixture becomes `eligible_for_independent_review`, not automatically discovered.
- Release review authorizes only gated Level-0 experimentation.
- Work items 021-030 and the queue are marked completed only after validation.
- English and Thai documentation agree.
- Work 030 is committed as one validated commit.

## Risks

- Exact steady-state invariance can be mistaken for proof of convergence.
- Synthetic fault adapters may test transaction enforcement without exercising every domain model.
- A release status can be over-read as physical readiness.
- Required evidence types may be present but not independent or valid.
- Re-running the full 30-run campaign increases validation time.

## Explicit Non-goals

- No claim of physical validation, real lap time, safety, manufacturability, or discovered technology.
- No fabricated higher-fidelity or independent evidence.
- No autonomous topology search or candidate optimization in this work item.
- No automatic promotion from Level 0 to a discovery claim.
- No replacement for CFD, FEA, surveyed geometry, track testing, or expert review.
